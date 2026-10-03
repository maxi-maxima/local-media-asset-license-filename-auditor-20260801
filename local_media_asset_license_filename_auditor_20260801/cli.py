import argparse
import json
import re
from pathlib import Path

MEDIA = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.wav', '.mp3'}
LICENSE_WORDS = re.compile(r'\b(cc0|cc-by|mit|apache|licensed|owned|generated|public-domain)\b', re.I)


def audit(root, *, include_ok=True):
    root = Path(root)
    rows = []
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.suffix.lower() in MEDIA:
            sidecars = [p.with_suffix(p.suffix + '.json'), p.with_suffix('.license'), p.with_suffix('.txt')]
            side = ' '.join(s.read_text(encoding='utf-8', errors='ignore') for s in sidecars if s.exists())
            hay = p.name + ' ' + side
            ok = bool(LICENSE_WORDS.search(hay))
            if ok and not include_ok:
                continue
            rows.append({
                'path': str(p.relative_to(root)).replace('\\', '/'),
                'status': 'ok' if ok else 'missing_license_marker',
                'suggested_filename': suggest(p.name) if not ok else p.name,
            })
    return rows


def summarize(rows):
    missing = sum(1 for row in rows if row['status'] == 'missing_license_marker')
    return {'total_assets': len(rows), 'missing_license_markers': missing, 'ok': len(rows) - missing}


def suggest(name):
    stem = Path(name).stem
    suffix = Path(name).suffix
    clean = re.sub(r'[^a-zA-Z0-9]+', '-', stem).strip('-').lower() or 'asset'
    return clean + '--license-needed' + suffix.lower()


def main(argv=None):
    ap = argparse.ArgumentParser(description='Audit media assets for filename or sidecar license provenance markers.')
    ap.add_argument('directory')
    ap.add_argument('--summary', action='store_true', help='include aggregate asset counts in the JSON output')
    ap.add_argument('--missing-only', action='store_true', help='omit assets that already have a license/provenance marker')
    ap.add_argument('--fail-on-missing', action='store_true', help='exit with status 1 when any asset lacks a license/provenance marker')
    ns = ap.parse_args(argv)
    rows = audit(ns.directory, include_ok=not ns.missing_only)
    payload = {'assets': rows}
    if ns.summary:
        payload['summary'] = summarize(rows)
    print(json.dumps(payload, indent=2))
    if ns.fail_on_missing and any(row['status'] == 'missing_license_marker' for row in rows):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
