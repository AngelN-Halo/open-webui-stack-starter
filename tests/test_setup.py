"""Regression checks for secret generation and preserving existing installations."""
import contextlib
import importlib.util
import io
from pathlib import Path
import re
import stat
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('setup_script', ROOT / 'scripts/setup.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / '.env.example').write_bytes((ROOT / '.env.example').read_bytes())
        self.root_patch = patch.object(setup, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def run_setup(self, *args):
        with patch('sys.argv', ['setup.py', *args]), contextlib.redirect_stdout(io.StringIO()):
            setup.main()

    def test_fresh_independent_private_credentials(self):
        self.run_setup('--project-name', 'test-stack', '--admin-email', 'test@example.com')
        path = self.root / '.env'
        values = dict(line.split('=', 1) for line in path.read_text().splitlines()
                      if line and not line.startswith('#'))
        names = [line.split('=', 1)[0] for line in (self.root / '.env.example').read_text().splitlines()
                 if line.endswith('=GENERATE_ME')]
        tokens = [values[name] for name in names]
        self.assertEqual(len(tokens), len(set(tokens)))
        for name in names:
            pattern = r'sk-[0-9a-f]{64}' if name == 'LITELLM_MASTER_KEY' else r'[0-9a-f]{64}'
            self.assertRegex(values[name], '^' + pattern + '$')
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertEqual(values['COMPOSE_PROJECT_NAME'], 'test-stack')
        self.assertEqual(values['WEBUI_ADMIN_EMAIL'], 'test@example.com')

    def test_existing_environment_is_untouched(self):
        self.run_setup()
        path = self.root / '.env'
        original = path.read_bytes()
        self.run_setup('--project-name', 'different')
        self.assertEqual(path.read_bytes(), original)

    def test_symlink_is_not_followed_or_replaced(self):
        destination = self.root / 'missing-target'
        (self.root / '.env').symlink_to(destination)
        self.run_setup()
        self.assertFalse(destination.exists())
        self.assertTrue((self.root / '.env').is_symlink())

    def test_invalid_input_cannot_inject_environment(self):
        for args in [('--project-name', '../live'), ('--admin-email', 'a@example.com\nPOSTGRES_PASSWORD=x')]:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.run_setup(*args)
            self.assertFalse((self.root / '.env').exists())


if __name__ == '__main__':
    unittest.main()
