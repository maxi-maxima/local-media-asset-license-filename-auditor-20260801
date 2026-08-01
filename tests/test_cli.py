import tempfile
import unittest
from pathlib import Path

from local_media_asset_license_filename_auditor_20260801.cli import audit


class AuditTests(unittest.TestCase):
    def test_flags_missing_license_marker(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'Demo Shot.PNG').write_bytes(b'x')
            rows = audit(root)
        self.assertEqual(rows[0]['status'], 'missing_license_marker')
        self.assertTrue(rows[0]['suggested_filename'].endswith('--license-needed.png'))

    def test_accepts_sidecar_license(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'clip.mp4').write_bytes(b'x')
            (root / 'clip.mp4.json').write_text('{"license":"CC-BY"}', encoding='utf-8')
            self.assertEqual(audit(root)[0]['status'], 'ok')


if __name__ == '__main__':
    unittest.main()
