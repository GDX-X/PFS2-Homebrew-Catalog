# PFS2 Homebrew Catalog

Homebrew catalog, download sources and PFS resources for PFS2 HDD Manager.
Application binaries are downloaded from their authors; this repository does not bundle a PS2 BIOS.

## Use in PFS2 HDD Manager

Open **Homebrew Browser → Update catalog…**. The default manifest address is:

https://github.com/GDX-X/PFS2-Homebrew-Catalog/releases/latest/download/manifest.json

You can also download `catalog.zip` from Releases and use **Import catalog ZIP…**.
The updater validates the package and keeps a backup of the previous catalog.
A version of PFS2 HDD Manager supporting catalog schema 2 is required.

## Maintain the catalog

Edit `catalog/SystemSoftwareCatalog.json` and the files in `catalog/assets/`.
Keep each application's ID stable. Set `browser_visible: false` for identity-only entries.
Download URLs, including Ember and launcHER sources, are defined in the catalog.
See [catalog documentation](catalog/README.md) for installation and PFS resource fields.

## Publish a new version

1. Increase `catalog_version` in `catalog/manifest.json`, using X.Y.Z.
2. Commit and push your changes to `main`.
3. Create and push a matching tag, for example `v1.3.1`.
4. The **Publish catalog** GitHub Actions workflow builds and publishes `catalog.zip`
   and its download `manifest.json` as release assets.

For a local build, run `python tools/build_release.py` from this repository.
Generated files are written to `dist/`. The publication manifest includes the
version-specific package URL and SHA-256. Do not copy it into the source catalog:
`catalog/manifest.json` only holds the catalog and schema versions.

New applications using existing installer types need only a catalog update.
New installation procedures still require a PFS2 HDD Manager code update.
