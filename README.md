# Local Media Asset License Filename Auditor

AI-generated demos and content tools create piles of images, audio, and video clips. This CLI audits local media assets and flags files whose filename or sidecar metadata does not show license or provenance.

## Why now

Open-source projects increasingly ship screenshots, short videos, generated images, and social clips. Rights and provenance mistakes can block releases, demos, and community sharing.

## Install and run

```bash
python -m local_media_asset_license_filename_auditor_20260801.cli examples/assets --summary
python -m local_media_asset_license_filename_auditor_20260801.cli examples/assets --missing-only --summary
python -m local_media_asset_license_filename_auditor_20260801.cli examples/assets --fail-on-missing
python -m unittest discover -s tests
```

Use `--fail-on-missing` in release or CI jobs. The command still emits the JSON report, then exits with status 1 when any audited asset lacks a license/provenance marker.

## Example

```json
{
  "assets": [
    {"path": "Demo Shot.PNG", "status": "missing_license_marker", "suggested_filename": "demo-shot--license-needed.png"}
  ],
  "summary": {"total_assets": 1, "missing_license_markers": 1, "ok": 0}
}
```

## Roadmap

- Optional safe rename mode
- SPDX-style sidecar templates
