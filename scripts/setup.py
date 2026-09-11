#!/usr/bin/env python3
"""Generate first-install secrets. Never replace an existing environment file."""
import argparse
import os
from pathlib import Path
import re
import secrets

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-name', default='open-webui-stack')
    parser.add_argument('--admin-email', default='admin@example.com')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', args.project_name):
        parser.error('Project name must use lowercase letters, digits, underscores or hyphens.')
    if not re.fullmatch(r'[A-Za-z0-9_.+%-]+@[A-Za-z0-9.-]+', args.admin_email):
        parser.error('Use a plain email address without whitespace or shell characters.')
    target = ROOT / '.env'
    if target.exists() or target.is_symlink():
        print('.env already exists; left unchanged. Edit it locally if needed.')
        return
    lines = []
    for line in (ROOT / '.env.example').read_text().splitlines():
        name, separator, value = line.partition('=')
        if separator and value == 'GENERATE_ME':
            value = secrets.token_hex(32)
            if name == 'LITELLM_MASTER_KEY':
                value = 'sk-' + value
            line = name + '=' + value
        elif name == 'COMPOSE_PROJECT_NAME':
            line = name + '=' + args.project_name
        elif name == 'WEBUI_ADMIN_EMAIL':
            line = name + '=' + args.admin_email
        lines.append(line)
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as output:
        output.write('\n'.join(lines) + '\n')
    print('Created .env (mode 0600) with independent random secrets. Keep it private.')


if __name__ == '__main__':
    main()
