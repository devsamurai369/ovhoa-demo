# OVHOA Website (static rebuild)

A fast, fully responsive static rebuild of https://ovhoarefs.com (Ohio Valley
Hockey Officials Association). No WordPress, no plugins, no database — just
HTML, one stylesheet, one small JS file, and the site's images/documents.

## Structure

```
ovhoa-site/
├── build.py                # generates all *.html pages from one shared template
├── index.html              # Home
├── history.html            # About / History
├── board-of-directors.html
├── official-documents.html
├── contact-us.html         # email contact cards (old WP form was broken)
├── file-a-report.html
├── become-an-official.html
├── rule-books.html
├── scorekeepers-guide.html
└── assets/
    ├── css/style.css       # the entire design system
    ├── js/nav.js           # mobile menu + dropdowns
    ├── img/                # logo, hero, partner logos (downloaded from live site)
    └── docs/               # OVHOA manual PDF, bylaws placeholder, ACHA report form
```

## Editing content

Edit the page bodies in `build.py` (the `HOME`, `HISTORY`, `BOARD`, … strings
near the bottom), then regenerate:

```
python build.py
```

Or just edit the generated `.html` files directly if you prefer — they're
plain HTML. The build script only exists so the header/footer/nav stay
identical across all nine pages.


## Known content gaps carried over from the old site

- Bylaws PDF is still the "Coming Soon" placeholder.
- OVHOA Manual is the 2016–2017 edition.
- Board bios are all "coming soon" with a placeholder avatar.
- Rule Books / Scorekeeper's Guide pages were "coming soon" on the old site;
  the rebuild adds direct links to the governing bodies' rulebooks meanwhile.
- The old Contact Us page said "fill out this form" but rendered no form (the
  WP form plugin was broken). The rebuild replaces it with email contact cards
  for the relevant board roles.
