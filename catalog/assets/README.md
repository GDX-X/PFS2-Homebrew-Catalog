# Application images

Each application has its own directory. Use `icon.png` for its icon and
`screenshot-01.png`, `screenshot-02.png`, etc. for screenshots.

Descriptions, creators, versions, copyright notices and image paths remain in
`libs/HomebrewCatalog/SystemSoftwareCatalog.json`. Images must be referenced in that catalog;
the first two screenshot paths are already configured for every catalog application.

Example paths for POPS:

```json
"image": ["libs", "HomebrewCatalog", "assets", "POPS", "icon.png"],
"screenshots": [
  ["libs", "HomebrewCatalog", "assets", "POPS", "screenshot-01.png"],
  ["libs", "HomebrewCatalog", "assets", "POPS", "screenshot-02.png"]
]
```

Drop `screenshot-01.png` and `screenshot-02.png` into the application's directory,
then reopen the software browser. No JSON change is needed for these two slots.
Missing images display "Not available". Additional screenshots need catalog entries.
Applications with an APPS ID use that ID as their directory name.
The current catalog includes wLaunchELF, Open PS2 Loader, POPS, Ember and HDD-OSD.
The shared `github.png` icon stays at this directory's root.
