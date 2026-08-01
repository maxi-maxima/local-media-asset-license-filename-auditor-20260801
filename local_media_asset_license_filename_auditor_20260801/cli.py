import argparse, json, re
from pathlib import Path
MEDIA={'.png','.jpg','.jpeg','.gif','.webp','.mp4','.mov','.wav','.mp3'}
LICENSE_WORDS=re.compile(r'\b(cc0|cc-by|mit|apache|licensed|owned|generated|public-domain)\b', re.I)

def audit(root):
    root=Path(root)
    rows=[]
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() in MEDIA:
            sidecars=[p.with_suffix(p.suffix+'.json'), p.with_suffix('.license'), p.with_suffix('.txt')]
            side=' '.join(s.read_text(encoding='utf-8', errors='ignore') for s in sidecars if s.exists())
            hay=p.name+' '+side
            ok=bool(LICENSE_WORDS.search(hay))
            rows.append({'path':str(p.relative_to(root)).replace('\\','/'),'status':'ok' if ok else 'missing_license_marker','suggested_filename':suggest(p.name) if not ok else p.name})
    return rows

def suggest(name):
    stem=Path(name).stem; suffix=Path(name).suffix
    clean=re.sub(r'[^a-zA-Z0-9]+','-',stem).strip('-').lower() or 'asset'
    return clean+'--license-needed'+suffix.lower()

def main(argv=None):
    ap=argparse.ArgumentParser(description='Audit media assets for filename or sidecar license provenance markers.')
    ap.add_argument('directory')
    ns=ap.parse_args(argv)
    print(json.dumps({'assets':audit(ns.directory)}, indent=2))
if __name__=='__main__': main()
