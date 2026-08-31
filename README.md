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

## Previewing locally

```
python -m http.server 8000
```

then open http://localhost:8000.

## Deploying to Hostinger

1. In hPanel → **Files → File Manager**, open `public_html`.
2. Back up / move aside the WordPress install (or deploy to a subfolder first
   to test).
3. Upload the contents of this folder (all `.html` files + the `assets/`
   folder). `build.py` and `README.md` don't need to be uploaded.
4. **Fix the SSL certificate** (hPanel → Security → SSL): the current cert is
   expired, which blocks browsers from loading the site at all. Install/renew
   the free Let's Encrypt cert and turn on auto-renewal + Force HTTPS.

## Known content gaps carried over from the old site

- Bylaws PDF is still the "Coming Soon" placeholder.
- OVHOA Manual is the 2016–2017 edition.
- Board bios are all "coming soon" with a placeholder avatar.
- Rule Books / Scorekeeper's Guide pages were "coming soon" on the old site;
  the rebuild adds direct links to the governing bodies' rulebooks meanwhile.
- The old Contact Us page said "fill out this form" but rendered no form (the
  WP form plugin was broken). The rebuild replaces it with email contact cards
  for the relevant board roles.
