#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
python3 scripts/setup.py "$@"
docker compose config --quiet
printf 'Configuration validated. No services have been started. See README.md.\n'
