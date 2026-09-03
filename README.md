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

## Board-editable content via Google Sheets

The homepage **meeting schedule** and the **Board of Directors** roster can be
driven by a Google Sheet so board members can update the site without touching
code. Setup (one time):

1. Create a Google Sheet with two tabs named exactly `Meetings` and `Board`:
   - **Meetings** headers (row 1): `Date | Time | Format | Note`
     (e.g. `9/2/2026` / `7:30 PM` / `Zoom` / `Board Meeting`, or
     `March 15, 2026` / `7 PM` / `In Person` / `Location TBA`)
   - **Board** headers (row 1): `Name | Role | Email` — rows appear on the
     site in sheet order, so reorder rows to reorder the cards.
2. Share → General access → **Anyone with the link → Viewer**.
3. Copy the sheet ID from its URL
   (`https://docs.google.com/spreadsheets/d/<ID>/edit`) and paste it into
   `SHEET_ID` at the top of `assets/js/sheets.js`. Paste **only the ID** —
   the part between `/d/` and `/edit`, not the whole URL.
4. Only give **edit** access to board members' Google accounts. Everything in
   these two tabs is publicly readable — no phone numbers or private notes.

Changes to the sheet appear on the site within a few minutes (Google caches
the published CSV briefly). If the sheet is ever unreachable, the site falls
back to the content baked into the HTML, so nothing breaks. To refresh that
fallback occasionally, update the meeting/board content in `build.py` and
rebuild.

### Contact details come from the Board tab too

The email addresses on **Contact Us**, the two buttons on **Mentoring**, and the
Referee-in-Chief link on **Rule Books** are all filled in from the Board tab —
so if the association ever changes email domains, updating the sheet updates
every page at once. Nothing in the HTML needs editing.

Cards are matched to people by their **Role**, using these keys:

| Key | Matches a Role of |
| --- | --- |
| `president` | President, Executive President |
| `vicepresident` | Vice President, Executive Vice President |
| `treasurer` | Treasurer, Executive Treasurer |
| `secretary` | Secretary, Executive Secretary |
| `ric` | RIC, Local RIC, Referee-in-Chief |
| `scheduler` | Scheduler, Game Scheduler, Assignor |
| `mentoring` | Mentoring, Mentoring Coordinator |

Matching ignores case, spaces and punctuation, so `Referee-in-Chief` and
`referee in chief` both work. If a key matches no row (the position is vacant,
or the Role was renamed to something not listed), that spot simply keeps the
address baked into the HTML rather than going blank. A card listing two people
is all-or-nothing: it will not show one live address next to one stale one.

To point a card at a different person, change its `data-contact` key in
`build.py` and rebuild — e.g. the "New Officials & Mentoring" card uses
`data-contact="ric,president"` and could become `data-contact="mentoring"`
once a Mentoring Coordinator is appointed.

### Season years update themselves

The **Become an Official** page carries the membership year in ~15 places
(`2026–27`, `May 1, 2026`, the SafeSport birth year, and so on). Those are
marked `data-season="..."` in the HTML and filled in at page load from the
current membership year, which rolls over every **May 1** — so the page stops
being wrong the moment the new season opens, with no edit needed.

Derived keys: `label`, `prev-label`, `open`, `close-apps`, `expire-prev`,
`seminars-end`, `close`, `safesport-year` (season start year minus 17).

**These are derived, not authoritative.** Fees, Playing Rules Exercise question
counts, and any actual rule changes still need a human to check them against
usahockey.com/registrationrules each season. If USA Hockey ever moves one of
the derived dates, add a **`Season`** tab to the Google Sheet with `Key` and
`Value` columns and any key listed above will be overridden — no code change:

| Key | Value |
| --- | --- |
| `close-apps` | November 18, 2027 |

### Past meetings drop off automatically

A meeting disappears from the site once it is more than **`GRACE_DAYS`** days
old (set at the top of `assets/js/sheets.js`; currently `1`, so a meeting is
still listed the day after it happened and is gone the day after that). The
board never has to delete rows — leave them in the sheet as a record and the
site simply stops showing them. Set `GRACE_DAYS = 2` for a longer grace period.

Notes on how dates are read:

- Understood formats: `9/2/2026`, `2026-09-02`, `March 15, 2026`,
  `Sunday, March 15, 2026`, `15 March 2026`.
- A date the site **can't** read is always shown, never hidden — so a typo
  makes a meeting linger rather than vanish silently. (`TBD` in the Date
  column therefore stays on the site until you give it a real date.)
- When every meeting has passed, the section shows
  "No meetings are currently scheduled — check back soon."
- The fallback rows baked into `build.py` need a `data-date="YYYY-MM-DD"`
  attribute so they expire the same way.

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
