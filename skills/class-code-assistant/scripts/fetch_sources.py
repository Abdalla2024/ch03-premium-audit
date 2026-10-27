"""Download the classification guide and employer files from the locations the auditor gave.

Reads references/sources.json, writes into a cache directory:

    <cache>/classification-guide.md
    <cache>/employers/<employer-slug>/<file>
    <cache>/manifest.json   (source URL, sha256 and fetch time for every file)

Standard library only. The Drive links are public "anyone with the link" shares; no credentials are used or stored.
"""

import argparse
import datetime
import hashlib
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
FOLDER_LISTING = "https://drive.google.com/embeddedfolderview?id={id}"
FILE_DOWNLOAD = "https://drive.google.com/uc?export=download&id={id}"
ENTRY = re.compile(
    r'href="https://drive\.google\.com/(?P<kind>file/d|drive/folders)/(?P<id>[\w-]+)[^"]*".*?'
    r'<div class="flip-entry-title">(?P<name>[^<]+)</div>',
    re.S,
)


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "class-code-assistant/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def drive_id(url):
    m = re.search(r"/(?:file/d|folders)/([\w-]+)", url)
    if not m:
        raise ValueError(f"not a Google Drive file or folder link: {url}")
    return m.group(1)


def list_folder(folder_id):
    """Return [(kind, id, name)] for the entries of a public Drive folder."""
    page = _get(FOLDER_LISTING.format(id=folder_id)).decode("utf-8")
    return [(m["kind"], m["id"], html.unescape(m["name"]).strip()) for m in ENTRY.finditer(page)]


def download_file(file_id):
    data = _get(FILE_DOWNLOAD.format(id=file_id))
    if data.lstrip()[:15].lower().startswith((b"<!doctype html", b"<html")):
        raise RuntimeError(f"Drive returned an HTML page instead of file {file_id}; is it shared publicly?")
    return data


def fetch(cache_dir, sources, only=None):
    cache_dir = Path(cache_dir)
    manifest = {"fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "files": {}}

    def save(rel, data, url):
        path = cache_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        manifest["files"][rel] = {"source": url, "sha256": hashlib.sha256(data).hexdigest()}

    guide_url = sources["classification_guide"]
    save("classification-guide.md", download_file(drive_id(guide_url)), guide_url)

    for kind, folder_id, name in list_folder(drive_id(sources["employer_files"])):
        if kind != "drive/folders" or (only and name not in only):
            continue
        for fkind, file_id, fname in list_folder(folder_id):
            if fkind == "file/d":
                save(f"employers/{name}/{fname}", download_file(file_id), f"https://drive.google.com/file/d/{file_id}/view")

    if only:
        missing = set(only) - {Path(k).parts[1] for k in manifest["files"] if k.startswith("employers/")}
        if missing:
            raise RuntimeError(f"employer folder(s) not found at the source location: {', '.join(sorted(missing))}")
    (cache_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--cache", default=".cache/sources", help="directory to download into (default: .cache/sources)")
    ap.add_argument("--sources", default=SKILL_DIR / "references" / "sources.json", type=Path)
    ap.add_argument("--employer", action="append", help="employer folder slug to fetch (repeatable; default all)")
    args = ap.parse_args(argv)
    manifest = fetch(args.cache, json.loads(args.sources.read_text()), args.employer)
    print(f"fetched {len(manifest['files'])} files into {args.cache}")


if __name__ == "__main__":
    sys.exit(main())
