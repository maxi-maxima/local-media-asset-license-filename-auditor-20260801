# Local Media Asset License Filename Auditor

AI-generated demos and content tools create piles of images, audio, and video clips. This CLI audits local media assets and flags files whose filename or sidecar metadata does not show license or provenance.

## Why now

Open-source projects increasingly ship screenshots, short videos, generated images, and social clips. Rights and provenance mistakes can block releases, demos, and community sharing.

## Install and run

```bash
python -m local_media_asset_license_filename_auditor_20260801.cli examples/assets
python -m unittest discover -s tests
```

## Example

```json
{
  "assets": [
    {"path": "Demo Shot.PNG", "status": "missing_license_marker", "suggested_filename": "demo-shot--license-needed.png"}
  ]
}
```

## Roadmap

- Optional safe rename mode
- SPDX-style sidecar templates
- Release archive gate for CI
