import importlib.util
import pathlib
import subprocess
import tempfile
import unittest

SCANNER = pathlib.Path(__file__).resolve().parents[1] / 'scripts/check_secrets.py'
spec = importlib.util.spec_from_file_location('scanner', SCANNER)
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)

class TestSecrets(unittest.TestCase):
    def test_clean_text(self):
        self.assertFalse(scanner.suspicious(b'Bienvenue dans notre atelier.'))

    def test_fake_password(self):
        self.assertTrue(scanner.suspicious(b'pass' + b'word=' + b'FAUX_SECRET_ATELIER'))

    def test_staged_content_not_working_copy(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(['git', 'init', '-q', d], check=True)
            p = pathlib.Path(d) / 'config.txt'
            p.write_bytes(b'api_' + b'key=' + b'FAUX_SECRET_ATELIER')
            subprocess.run(['git', '-C', d, 'add', 'config.txt'], check=True)
            p.write_text('contenu sain non indexe')
            result = subprocess.run(['python3', str(SCANNER)], cwd=d, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn(b'FAUX_SECRET_ATELIER', result.stderr)
            subprocess.run(['git', '-C', d, 'add', 'config.txt'], check=True)
            result = subprocess.run(['python3', str(SCANNER)], cwd=d, capture_output=True)
            self.assertEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()
