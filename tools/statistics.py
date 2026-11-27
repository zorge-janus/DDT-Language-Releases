import json,re,hashlib
from pathlib import Path
m=json.loads(Path("manifest.json").read_text())
lines=["## Published language inventory","","| Language | Version | Entries | Bytes | File integrity |","|---|---:|---:|---:|---|"]
for lang,v in sorted(m["languages"].items()):
    if not re.fullmatch(r"[a-z]{2,3}(-[a-z0-9]{2,8})*",lang): raise ValueError("Invalid language")
    version=int(v["version"])
    p=Path("packs")/f"{lang}-{version}.ddtlang"
    ok=p.is_file() and p.stat().st_size==v["size"] and hashlib.sha256(p.read_bytes()).hexdigest()==v["sha256"]
    lines.append(f"| {lang} | {version} | {int(v['entries'])} | {int(v['size'])} | {'SHA-256 matches' if ok else 'Mismatch'} |")
lines+=["","Quality and model provenance are not available in the signed release catalog. File hash checks are not signature verification."]
p=Path("README.md");s=p.read_text(encoding="utf-8")
a="<!-- ANALYTICS START -->";b="<!-- ANALYTICS END -->"
block=a+"\n"+"\n".join(lines)+"\n"+b
s=s.split(a,1)[0]+block+s.split(b,1)[1] if a in s and b in s else s.rstrip()+"\n\n"+block+"\n"
p.write_text(s,encoding="utf-8")
