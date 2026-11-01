"""Build the catalog release using Python's standard library only."""
import hashlib
import json
import os
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'catalog'
OUTPUT = ROOT / 'dist'
metadata = json.loads((SOURCE / 'manifest.json').read_text(encoding='utf-8-sig'))
version = metadata['catalog_version']
if not re.fullmatch(r'\d+\.\d+\.\d+', version) or metadata['schema_version'] != 2:
    raise ValueError('Unsupported catalog version or schema')
tag = os.environ.get('GITHUB_REF_NAME', 'v' + version)
if tag != 'v' + version:
    raise ValueError('Tag must match catalog_version: v' + version)
repository = os.environ.get('GITHUB_REPOSITORY', 'GDX-X/PFS2-Homebrew-Catalog')
if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
    raise ValueError('Invalid repository name')
entries = json.loads((SOURCE / 'SystemSoftwareCatalog.json').read_text(encoding='utf-8-sig'))
ids = set()
for category in entries:
    for entry in category['items']:
        app_id = entry.get('application_id')
        if app_id:
            if not re.fullmatch(r'APPS_\d{3}\.\d{2}', app_id) or app_id in ids:
                raise ValueError('Invalid or duplicate application ID: ' + app_id)
            ids.add(app_id)
        for parts in ([entry['image']] if entry.get('image') else []) + entry.get('screenshots', []):
            if parts[:2] != ['libs', 'HomebrewCatalog']:
                raise ValueError('Invalid image path')
            path = SOURCE.joinpath(*parts[2:]).resolve()
            if SOURCE.resolve() not in path.parents or not path.is_file():
                raise ValueError('Missing or unsafe image: ' + str(path))
OUTPUT.mkdir(exist_ok=True)
archive = OUTPUT / 'catalog.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as package:
    for path in sorted(SOURCE.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symbolic links cannot be published')
        if path.is_file():
            package.write(path, path.relative_to(SOURCE).as_posix())
manifest = dict(metadata)
manifest['package_url'] = f'https://github.com/{repository}/releases/download/{tag}/catalog.zip'
manifest['sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
(OUTPUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print('Built catalog', version, 'with', len(ids), 'application IDs')
