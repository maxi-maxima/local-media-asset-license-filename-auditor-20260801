import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from local_media_asset_license_filename_auditor_20260801.cli import audit, main, summarize


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

    def test_missing_only_filters_ok_assets_and_summary_counts_filtered_rows(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'clip.mp4').write_bytes(b'x')
            (root / 'clip.mp4.json').write_text('{"license":"CC-BY"}', encoding='utf-8')
            (root / 'Demo Shot.PNG').write_bytes(b'x')
            rows = audit(root, include_ok=False)
        self.assertEqual([row['path'] for row in rows], ['Demo Shot.PNG'])
        self.assertEqual(summarize(rows), {'total_assets': 1, 'missing_license_markers': 1, 'ok': 0})

    def test_main_can_emit_summary(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'Demo Shot.PNG').write_bytes(b'x')
            with patch('builtins.print') as mocked_print:
                main([str(root), '--summary'])
        payload = json.loads(mocked_print.call_args.args[0])
        self.assertEqual(payload['summary']['total_assets'], 1)
        self.assertEqual(payload['summary']['missing_license_markers'], 1)

    def test_fail_on_missing_sets_process_exit_code(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'Demo Shot.PNG').write_bytes(b'x')
            result = subprocess.run(
                [
                    sys.executable,
                    '-m',
                    'local_media_asset_license_filename_auditor_20260801.cli',
                    str(root),
                    '--fail-on-missing',
                    '--summary',
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
            )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)['summary']['missing_license_markers'], 1)

    def test_fail_on_missing_allows_licensed_assets(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'clip.mp4').write_bytes(b'x')
            (root / 'clip.mp4.json').write_text('{"license":"CC-BY"}', encoding='utf-8')
            with patch('builtins.print'):
                exit_code = main([str(root), '--fail-on-missing'])
        self.assertEqual(exit_code, 0)


if __name__ == '__main__':
    unittest.main()
