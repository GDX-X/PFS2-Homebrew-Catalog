# Homebrew catalog

This directory is external data, stored in `libs/HomebrewCatalog` beside the
executable. `make_exe.bat` copies it into the distribution. It is not embedded
in the PyInstaller runtime.

- `manifest.json`: independent content version and format version.
- `SystemSoftwareCatalog.json`: single source for categories, application IDs,
  display titles, descriptions, download links and image paths.
- `assets/`: icons and screenshots, grouped by application ID where available.
  System packages without an APPS ID retain their named directories.

Keep `application_id` stable when renaming an application. Change its `title`
in the JSON. Entries with `browser_visible: false` reserve their IDs and provide
disk display titles without appearing in the browser. Remove that flag when
their browser entry is ready. Use image paths such as
`["libs", "HomebrewCatalog", "assets", "APPS_000.01", "browser", "icon.png"]`.
Missing screenshots show a placeholder.

The resources for APPS_000.01 are organized as follows:

```text
assets/APPS_000.01/
  browser/      # Browser icon and screenshots
  pfs/header/   # list.ico and del.ico for the partition header
  pfs/res/      # Application-specific partition resources (jackets)
```

Set `"pfs_resources": ["assets", "APPS_000.01", "pfs"]` on the application
entry to enable its PFS resources. The installer starts from the shared
template, overlays `header/list.ico`, `header/del.ico`, optional
`header/icon.sys`, and the files in `res/`, then fills in the application's
title and ID. Applications without this field use the common template.
The manual is generated from the entry's screenshots, copied into the staging
directory `res/image/` without modifying the original browser images. Page
IDs are unique; unused sample screenshots are removed from the staging copy.
The final display must still be verified on a PS2.

## Publish and update

Ember's entry contains `downloads.ember` and `downloads.launcher`. These are
read from the current catalog each time a download starts, including downloads
started outside the Homebrew Browser. Ember accepts either `type: direct`
with an HTTPS `url`, or `type: github_releases` with an API `url`, `asset_name`
and an HTTPS `asset_url_prefix` ending in `/`. The launcher uses `type: direct`
and `url`. Change these fields to update download locations without rebuilding
the program; keep `installer: ember` unchanged. ELF validation remains in code.

1. Edit the catalog and assets, keeping application IDs stable. Entries using
   `elf_download` need an `application_id` and an HTTPS `download_url`.
   New installation methods still require a program update.
2. Increase `catalog_version` in `manifest.json` (X.Y.Z). Keep `schema_version`
   at 2 for this format.
3. From the project root, build a local package:

   `python -m libs.catalog_update --build build/catalog-release`

   To prepare online publication, add `--package-url` followed by the HTTPS
   address where you will host `catalog.zip`. This creates a ZIP containing
   the catalog files at its root, plus a separate publication `manifest.json`
   with the package URL and SHA-256 checksum. Do not put the publication
   manifest inside the ZIP (its checksum describes that ZIP).
4. Publish both generated files at HTTPS addresses on your chosen host.
   A GitHub release can hold them; no separate account is required.
5. In Homebrew Browser, use **Update catalog…** and enter the publication
   manifest URL. A successful URL is remembered in `settings.ini`, outside
   this replaceable directory. Alternatively use **Import catalog ZIP…**
   for a local package, without any hosting.

The updater accepts newer versions only. It validates format compatibility,
IDs, resource paths, image presence and supported installers before replacing
anything. Downloads also require a matching SHA-256 checksum from the HTTPS
manifest. ZIP extraction has size limits and rejects traversal and symbolic
links. The previous directory is retained alongside this one as
`HomebrewCatalog.backup-<unique suffix>`; a failed replacement restores it.
The browser and application title lookup reload after a successful update.
Updates replace catalog data only; they do not install applications on a PS2
disk. To restore a retained backup manually, close the program, move the
current catalog aside, and rename the chosen backup to `HomebrewCatalog`.
