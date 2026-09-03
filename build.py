#!/usr/bin/env python3
"""Generates the OVHOA static site: one shared header/footer/template, nine pages.

Run:  python build.py
Output: *.html in this directory. Edit page content in the PAGES dict below.
"""
import datetime
import io
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ("Home", "index.html", None),
    ("About OVHOA", None, [
        ("History", "history.html"),
        ("Board of Directors", "board-of-directors.html"),
        ("Official Documents", "official-documents.html"),
        ("Contact Us", "contact-us.html"),
    ]),
    ("File a Report", "file-a-report.html", None),
    ("Rinks", "rinks.html", None),
    ("Education & Development", None, [
        ("Become an Official", "become-an-official.html"),
        ("Mentoring", "mentoring.html"),
        ("Rule Books", "rule-books.html"),
        ("Scorekeeper's Guide", "scorekeepers-guide.html"),
    ]),
    ("Important Links", None, [
        ("USAH Registration", "https://membership.usahockey.com/"),
        ("Horizon Web Ref Login", "https://horizonwebref.com/"),
        ("USA Hockey", "https://www.usahockey.com/"),
        ("OHSAA", "https://www.ohsaa.org/"),
        ("ACHA", "https://www.achahockey.org/"),
        ("NFHS", "https://www.nfhs.org/"),
        ("NCAA", "https://www.ncaa.com/"),
    ]),
]


def nav_html(active):
    parts = []
    for label, href, children in NAV:
        if children is None:
            current = ' aria-current="page"' if href == active else ""
            parts.append(f'<li><a href="{href}"{current}>{label}</a></li>')
        else:
            items = []
            for clabel, chref in children:
                external = chref.startswith("http")
                attrs = ' target="_blank" rel="noopener"' if external else ""
                if not external and chref == active:
                    attrs += ' aria-current="page"'
                items.append(f'<li><a href="{chref}"{attrs}>{clabel}</a></li>')
            parts.append(
                '<li class="has-sub">'
                f'<button type="button" class="submenu-toggle" aria-expanded="false">{label} <span class="caret"></span></button>'
                f'<ul class="sub-menu">{"".join(items)}</ul></li>'
            )
    return "".join(parts)


def page(title, description, active, body):
    full_title = "Ohio Valley Hockey Officials Association" if active == "index.html" \
        else f"{title} – OVHOA"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="icon" type="image/png" href="assets/img/ovhoa-logo-300.png">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html">
      <img class="badge" src="assets/img/ovhoa-logo-300.png" alt="OVHOA logo" width="48" height="48">
      <span class="brand-text">
        <span class="brand-name">Ohio Valley Hockey Officials Association</span>
        <span class="brand-sub">Greater Cincinnati &amp; Northern Kentucky</span>
      </span>
    </a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Toggle navigation">
      <span class="bar"></span><span class="bar"></span><span class="bar"></span>
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Primary">
      <ul>{nav_html(active)}</ul>
    </nav>
  </div>
</header>
<div class="stripe" aria-hidden="true"></div>
<main id="main">
{body}
</main>
<div class="stripe" aria-hidden="true"></div>
<footer class="site-footer">
  <div class="container">
    <div class="footer-main">
      <div>
        <div class="footer-brand">
          <img src="assets/img/ovhoa-logo-300.png" alt="" width="54" height="54">
          <span class="name">Ohio Valley Hockey<br>Officials Association</span>
        </div>
        <p><em>Pursuing perfection every time we step on the ice.</em></p>
      </div>
      <div>
        <h4>About</h4>
        <ul>
          <li><a href="history.html">History</a></li>
          <li><a href="board-of-directors.html">Board of Directors</a></li>
          <li><a href="official-documents.html">Official Documents</a></li>
          <li><a href="contact-us.html">Contact Us</a></li>
        </ul>
      </div>
      <div>
        <h4>Officials</h4>
        <ul>
          <li><a href="file-a-report.html">File a Report</a></li>
          <li><a href="rinks.html">Rink Locations</a></li>
          <li><a href="become-an-official.html">Become an Official</a></li>
          <li><a href="mentoring.html">Mentoring</a></li>
          <li><a href="rule-books.html">Rule Books</a></li>
          <li><a href="scorekeepers-guide.html">Scorekeeper's Guide</a></li>
        </ul>
      </div>
      <div>
        <h4>Partners</h4>
        <ul>
          <li><a href="https://www.usahockey.com/" target="_blank" rel="noopener">USA Hockey</a></li>
          <li><a href="https://www.ohsaa.org/" target="_blank" rel="noopener">OHSAA</a></li>
          <li><a href="https://www.achahockey.org/" target="_blank" rel="noopener">ACHA</a></li>
          <li><a href="https://www.usphl.com/" target="_blank" rel="noopener">USPHL</a></li>
          <li><a href="https://www.ncaa.com/" target="_blank" rel="noopener">NCAA</a></li>
          <li><a href="https://www.nfhs.org/" target="_blank" rel="noopener">NFHS</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Ohio Valley Hockey Officials Association</span>
      <span><a href="https://horizonwebref.com/" target="_blank" rel="noopener">Horizon Web Ref Login</a></span>
    </div>
  </div>
</footer>
<script src="assets/js/nav.js"></script>
<script src="assets/js/sheets.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Page bodies
# ---------------------------------------------------------------------------

HOME = """
<!-- Filled from the Banner tab of the Google Sheet; stays hidden while the
     tab has no content, so clearing the row removes it from the site. -->
<section class="announce" data-sheet-banner hidden>
  <div class="container"></div>
</section>

<section class="hero">
  <div class="container">
    <h1>Ohio Valley Hockey Officials Association</h1>
    <p class="tagline">Greater Cincinnati and Northern Kentucky ice hockey officials association &mdash; roughly 150 registered officials serving youth, high school, and collegiate hockey.</p>
    <p class="motto">Pursuing perfection every time we step on the ice</p>
    <p class="mt-2">
      <a class="btn" href="become-an-official.html">Become an Official</a>
      <a class="btn ghost" href="file-a-report.html">File a Report</a>
    </p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Upcoming</span>
      <h2>OVHOA General Meetings</h2>
    </div>
    <!-- Live content comes from the Meetings tab of the Google Sheet (see
         assets/js/sheets.js). The rows below are only a fallback for when the
         sheet is unreachable; each needs data-date="YYYY-MM-DD" so that past
         meetings drop off automatically. -->
    <ul class="meeting-list card" data-sheet-meetings>
      <li data-date="2026-09-02"><span class="when">September 2, 2026 &middot; 7:30 PM</span> <span class="badge-pill">Zoom &middot; Board Meeting</span></li>
    </ul>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Affiliations</span>
      <h2>Who We Officiate For</h2>
    </div>
    <div class="logo-row">
      <a href="https://www.usahockey.com/" target="_blank" rel="noopener"><img src="assets/img/logo-usah.png" alt="USA Hockey" loading="lazy"></a>
      <a href="https://www.achahockey.org/" target="_blank" rel="noopener"><img src="assets/img/logo-acha.png" alt="ACHA - American Collegiate Hockey Association" loading="lazy"></a>
      <a href="https://www.ohsaa.org/" target="_blank" rel="noopener"><img src="assets/img/logo-ohsaa.png" alt="OHSAA - Ohio High School Athletic Association" loading="lazy"></a>
      <a href="https://www.usphl.com/" target="_blank" rel="noopener"><img src="assets/img/logo-usphl.png" alt="USPHL - United States Premier Hockey League" loading="lazy"></a>
      <a href="https://www.ncaa.com/" target="_blank" rel="noopener"><img src="assets/img/logo-ncaa.png" alt="NCAA" loading="lazy"></a>
    </div>
  </div>
</section>
"""

HISTORY = """
<section class="page-banner">
  <div class="container">
    <h1>About the OVHOA</h1>
    <p class="lede">Five decades of officiating hockey in the Ohio Valley.</p>
  </div>
</section>
<section class="section">
  <div class="container prose">
    <p>The Ohio Valley Hockey Officials Association (OVHOA) began in the early 1970&rsquo;s with guys officiating youth games. The need for ice hockey officials was formalized as ice hockey programs for all ages began to expand in correlation to the rise in popularity of the World Hockey League Cincinnati Stingers. There were about 18 officials in the OVHOA in 1975.</p>
    <p>In 1975 USA Hockey was known as &ldquo;AHAUS&rdquo; (Amateur Hockey Association of the United States). The name was changed in the early 1980&rsquo;s but AHAUS is still maintained as a legal entity of USA Hockey.</p>
    <p>By 1984, the OVHOA was made up of approximately 20&ndash;25 officials. There were no &ldquo;seminars&rdquo;, and games were held at the open air &ldquo;Dixie Bowl&rdquo; in northern Kentucky (a converted drive-in movie theater), Northland Ice Center was &ldquo;the new place&rdquo;, and Sports Plus was just a field.</p>
    <p>Currently, the OVHOA has approximately 150 officials.</p>
    <div class="callout">
      <p style="margin:0">The OVHOA is a not-for-profit organization that supplies qualified ice hockey officials to our customers. We operate under by-laws which define the purpose, organization, membership, governance, appointments and procedures that we employ as we go about our business. We utilize an elected and appointed board to carry out the business of the organization, and have monthly general membership meetings.</p>
    </div>
  </div>
</section>
"""


def board_member(name, role, email):
    slug = name.lower().replace(" ", "-")
    return f"""
      <div class="board-card" id="{slug}">
        <img src="assets/img/avatar-placeholder.png" alt="" loading="lazy">
        <div>
          <h3>{name}</h3>
          <p class="role">{role}</p>
          <p><a href="mailto:{email}">{email}</a></p>
        </div>
      </div>"""


BOARD = f"""
<section class="page-banner">
  <div class="container">
    <h1>Board of Directors</h1>
    <p class="lede">Elections for the Executive Board are held each spring. Executive Board Members are elected to two-year terms by the organization&rsquo;s general body; non-voting members are appointed by the Executive Board.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="board-grid" data-sheet-board>
      {board_member("Brian Siuda", "President", "president@ovhoarefs.com")}
      {board_member("Jeremy MacWalter", "Vice President", "vicepresident@ovhoarefs.com")}
      {board_member("David Christensen", "Treasurer", "treasurer@ovhoarefs.com")}
      {board_member("Nick Doud", "Secretary", "secretary@ovhoarefs.com")}
      {board_member("Ken Handley", "Local RIC", "ovhoaric@gmail.com")}
      {board_member("Bryan Thurnauer", "Scheduler", "scheduler@ovhoarefs.com")}
    </div>
  </div>
</section>
"""

DOCUMENTS = """
<section class="page-banner">
  <div class="container">
    <h1>Official Documents</h1>
    <p class="lede">Home for all OVHOA important documents.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="doc-list">
      <div class="doc-item card">
        <div>
          <span class="doc-name">OVHOA Bylaws</span>
          <span class="doc-meta">Updated bylaws coming soon</span>
        </div>
        <a class="btn" href="assets/docs/ComingSoon.pdf" target="_blank" rel="noopener">View PDF</a>
      </div>
      <div class="doc-item card">
        <div>
          <span class="doc-name">OVHOA Manual</span>
          <span class="doc-meta">2016&ndash;2017 edition &middot; PDF</span>
        </div>
        <a class="btn" href="assets/docs/OVHOA_Manual_2016-2017.pdf" target="_blank" rel="noopener">View PDF</a>
      </div>
    </div>
  </div>
</section>
"""

CONTACT = """
<section class="page-banner">
  <div class="container">
    <h1>Contact Us</h1>
    <p class="lede">Reach out and a member of the Board of Directors will get back to you.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <!-- Names and addresses below are only a fallback. Live values come from
         the Board tab of the Google Sheet, matched on each card's data-contact
         key (see assets/js/sheets.js). -->
    <div class="contact-grid">
      <div class="card contact-card" data-contact="president">
        <h3>General Inquiries</h3>
        <p class="role" data-contact-role>President &mdash; Brian Siuda</p>
        <p data-contact-email><a href="mailto:president@ovhoarefs.com">president@ovhoarefs.com</a></p>
      </div>
      <div class="card contact-card" data-contact="ric">
        <h3>Officiating &amp; Rules</h3>
        <p class="role" data-contact-role>Local RIC &mdash; Ken Handley</p>
        <p data-contact-email><a href="mailto:ovhoaric@gmail.com">ovhoaric@gmail.com</a></p>
      </div>
      <div class="card contact-card" data-contact="scheduler">
        <h3>Game Scheduling</h3>
        <p class="role" data-contact-role>Scheduler &mdash; Bryan Thurnauer</p>
        <p data-contact-email><a href="mailto:scheduler@ovhoarefs.com">scheduler@ovhoarefs.com</a></p>
      </div>
      <div class="card contact-card" data-contact="ric,president">
        <h3>New Officials &amp; Mentoring</h3>
        <p class="role" data-contact-role>Ken Handley (Local RIC) or Brian Siuda (President)</p>
        <p data-contact-email><a href="mailto:ovhoaric@gmail.com">ovhoaric@gmail.com</a><br><a href="mailto:president@ovhoarefs.com">president@ovhoarefs.com</a></p>
      </div>
    </div>
    <p class="center mt-2">Looking for someone else? See the full <a href="board-of-directors.html">Board of Directors</a>.</p>
  </div>
</section>
"""

FILE_REPORT = """
<section class="page-banner">
  <div class="container">
    <h1>File a Report</h1>
    <p class="lede">Penalty and incident reporting tools for USA Hockey, OHSAA, and ACHA games.</p>
  </div>
</section>
<section class="section">
  <div class="container grid" style="gap:1.5rem">

    <div class="card report-block">
      <div class="org-logo"><img src="assets/img/logo-usah.png" alt="USA Hockey" loading="lazy"></div>
      <div>
        <h2>USA Hockey Games</h2>
        <p>To report penalties for USA Hockey games, you must use the online USA Hockey tool. For questions, contact <a href="board-of-directors.html#ken-handley">Ken Handley</a>.</p>
        <div class="actions"><a class="btn dark" href="https://www.usahockey.com/incidentreport" target="_blank" rel="noopener">USA Hockey Incident Report</a></div>
      </div>
    </div>

    <div class="card report-block">
      <div class="org-logo"><img src="assets/img/logo-ohsaa.png" alt="OHSAA" loading="lazy"></div>
      <div>
        <h2>OHSAA (High School) Games</h2>
        <p>Officials shall file a written report with the school and the OHSAA office whenever a coach or player is ejected from an athletic contest, using the &ldquo;Official&rsquo;s Report&rdquo; form. The report shall be filed with the reported school and the OHSAA <strong>within 48 hours of the ejection</strong>, and the ejecting official shall speak with the offender&rsquo;s principal/athletic director no later than the first school day following the ejection. An official failing to follow the ejection protocol may be penalized in accordance with Section 7 of the OHSAA Handbook for Officials.</p>
        <details class="info">
          <summary>More about the Official&rsquo;s Report form</summary>
          <div class="info-body">
            <p>The &ldquo;Official&rsquo;s Report&rdquo; form is also used to report good or poor sportsmanship, severe injuries, facility problems, or equipment problems. Ejections other than players or coaches and other items of which the Commissioner should be made aware must be provided.</p>
            <p>Please use only one form per school &mdash; each offending school will need its own copy. The reporting official will receive notification of resolution upon receipt of the reported school&rsquo;s reply.</p>
            <p><strong>It is the official&rsquo;s responsibility to send a copy of the form to the reported school and the OHSAA.</strong> There is a list of school contacts on the OHSAA website so you can email the report, or email it to <a href="mailto:rmoore@ohsaa.org">rmoore@ohsaa.org</a>.</p>
            <p>Please write legibly and include the ejected person&rsquo;s first and last names. Make sure the form is complete at the bottom with the date and name of the administrator you spoke with at the school.</p>
          </div>
        </details>
        <div class="actions"><a class="btn dark" href="http://officials.myohsaa.org/Logon" target="_blank" rel="noopener">OHSAA Officials Login</a></div>
      </div>
    </div>

    <div class="card report-block">
      <div class="org-logo"><img src="assets/img/logo-acha.png" alt="ACHA" loading="lazy"></div>
      <div>
        <h2>ACHA (Collegiate) Games</h2>
        <p>To report penalties for ACHA games, use this Microsoft Word form. When completed, email it <strong>as an attachment</strong> to the appropriate ACHA Commissioner, ACHA Referee-in-Chief, and <a href="board-of-directors.html#ken-handley">Ken Handley</a>.</p>
        <div class="actions"><a class="btn dark" href="assets/docs/ACHA_Incident_Report.docx" download>Download the ACHA Form</a></div>
      </div>
    </div>

  </div>
</section>
"""

BECOME = """
<section class="page-banner">
  <div class="container">
    <h1>Become an Official</h1>
    <p class="lede">USA Hockey Officiating Membership requirements for the <span data-season="label">2026&ndash;27</span> season.</p>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <h2><span data-season="label">2026&ndash;27</span> Key Dates</h2>
    <ul class="meeting-list stacked card" style="max-width:none">
      <li><span class="when"><span data-season="open">May 1, 2026</span></span> <span class="how">Membership applications open for <span data-season="label">2026&ndash;27</span></span></li>
      <li><span class="when"><span data-season="close-apps">November 20, 2026</span></span> <span class="how">Applications close &mdash; no one may begin the membership process after this date</span></li>
      <li><span class="when"><span data-season="expire-prev">November 30, 2026</span></span> <span class="how">All <span data-season="prev-label">2025&ndash;26</span> memberships expire</span></li>
      <li><span class="when"><span data-season="seminars-end">December 15, 2026</span></span> <span class="how">Classroom seminars for <span data-season="label">2026&ndash;27</span> conclude</span></li>
      <li><span class="when"><span data-season="close">December 31, 2026</span></span> <span class="how">Membership closes &mdash; all education requirements must be complete</span></li>
    </ul>
    <p class="mt-1">An official without a completed <span data-season="label">2026&ndash;27</span> membership after <span data-season="expire-prev">November 30, 2026</span> becomes ineligible to work USA Hockey sanctioned games until they complete their current season membership and receive their referee card and crest.</p>
    <p>USA Hockey Officiating Membership is valid for the entire current season in any district or state in the United States. Membership in a local officials association or local hockey league is not required for USA Hockey Officiating Program membership.</p>

    <h2 class="mt-2">Registration Basics</h2>
    <p><strong>Minimum/maximum ages.</strong> USA Hockey has no minimum or maximum ages for officials. It is strongly recommended that, regardless of membership level attained, officials not work games of their own age classification or higher. Generally, officials can successfully officiate as young as age 10. Some states have restrictive child labor laws that do not exempt amateur sport officials &mdash; it is the obligation of the parent who registers a minor to determine the specific labor laws in their state prior to registering.</p>
    <p><strong>New game officials.</strong> All persons who have never registered with USA Hockey as an ice hockey game official must register at Level 1 for the first season. All registration requirements must be completed, and you must have your USA Hockey Referee Card and Sweater Crest in hand before accepting any game assignments.</p>
    <div class="callout">
      <p style="margin:0"><strong>New Level 1 officials:</strong> after you register, message Referee-in-Chief <a href="board-of-directors.html#ken-handley">Ken Handley</a> or President <a href="board-of-directors.html#brian-siuda">Brian Siuda</a> so we know you're joining us &mdash; we'll get you set up with a <a href="mentoring.html">mentor</a> and into the game-assignment system.</p>
    </div>
    <p><strong>Returning game officials.</strong> Returning officials may apply for one membership level higher than their completed membership level the previous season. Once completely registered, an official under 16 years old may remain at Level 1 or choose to advance to Level 2.</p>
    <div class="callout">
      <p style="margin:0"><strong>New for <span data-season="label">2026&ndash;27</span>:</strong> An official who is 16 years old (or older) and has completed Level 1 officiating membership <strong>must advance to Level 2</strong> this season.</p>
    </div>
    <p><strong>Note:</strong> Once the online membership application has been submitted, an official cannot change the registration level they applied for.</p>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="section-title">
      <span class="kicker"><span data-season="label">2026&ndash;27</span> Season</span>
      <h2>Membership Education Requirements by Level</h2>
    </div>
    <div class="table-wrap">
      <table class="levels">
        <thead><tr><th>Level</th><th>Requirements</th></tr></thead>
        <tbody>
          <tr>
            <td class="level-name">Level 1</td>
            <td><ul>
              <li>Submit the <a href="https://membership.usahockey.com/" target="_blank" rel="noopener">online Officiating Membership application</a> and fee ($75.00)</li>
              <li>Complete a Level 1 officiating classroom seminar sanctioned by USA Hockey</li>
              <li>Complete Level 1 Online Education Module training</li>
              <li>Complete the online Level 1 Playing Rules Exercise (40 questions)</li>
            </ul></td>
          </tr>
          <tr>
            <td class="level-name">Level 2</td>
            <td><ul>
              <li>Must have completed Level 1 membership within the last two seasons</li>
              <li>Submit the <a href="https://membership.usahockey.com/" target="_blank" rel="noopener">online Level 2 Officiating Membership application</a> and fee ($135.00)</li>
              <li>Complete a Level 2 officiating classroom seminar sanctioned by USA Hockey</li>
              <li>Complete Level 2 Online Education Module training</li>
              <li>Complete the online Level 2 Playing Rules Exercise (60 questions)</li>
            </ul></td>
          </tr>
          <tr>
            <td class="level-name">Level 3</td>
            <td><ul>
              <li>Must have completed Level 2 (or higher) membership during the previous season</li>
              <li>Submit the <a href="https://membership.usahockey.com/" target="_blank" rel="noopener">online Level 3 Officiating Membership application</a> and fee ($135.00)</li>
              <li>Complete a Level 3 officiating classroom seminar sanctioned by USA Hockey</li>
              <li>Complete Level 3 Online Education Module training</li>
              <li>Complete the online Level 3 Playing Rules Exercise (80 questions; 40 for tenured officials)</li>
            </ul></td>
          </tr>
          <tr>
            <td class="level-name">Level 4</td>
            <td><ul>
              <li>Must have completed Level 3 or Level 4 membership last season</li>
              <li>Submit the <a href="https://membership.usahockey.com/" target="_blank" rel="noopener">online Level 4 Officiating Membership application</a> and fee ($135.00)</li>
              <li>Complete a Level 4 officiating classroom seminar sanctioned by USA Hockey</li>
              <li>Complete Level 4 Online Education Module training</li>
              <li>Complete the online Level 4 Playing Rules Exercise (80 questions; 40 for tenured officials)</li>
            </ul></td>
          </tr>
          <tr>
            <td class="level-name">Affiliated (L0)</td>
            <td><ul>
              <li>Submit the online L0 Non-Skating Affiliate Officiating Membership application and fee ($55.00)</li>
              <li><em>An Affiliated member is not eligible to work any USA Hockey sanctioned games.</em></li>
            </ul></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="callout mt-2">
      <p style="margin:0 0 0.5rem"><strong>All levels also require:</strong></p>
      <ul style="margin:0">
        <li>Completion of <a href="https://www.usahockey.com/safesportprogram" target="_blank" rel="noopener">SafeSport training</a> (if <span data-season="safesport-year">2009</span> birth year or older)</li>
        <li>Completion and maintenance of a USA Hockey sanctioned NCSI <a href="https://www.usahockey.com/backgroundscreen" target="_blank" rel="noopener">Background Screen</a> if 18+ years old on <span data-season="open">May 1, 2026</span></li>
      </ul>
      <p style="margin:0.5rem 0 0"><em>All USA Hockey officiating membership fees are non-refundable.</em></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <h2>Program Details</h2>
    <details class="info">
      <summary>Playing Rules Exercise</summary>
      <div class="info-body">
        <p>Every membership level includes a Playing Rules Exercise requirement. Playing Rules Exercises consist of answering a series of questions using the current 2025&ndash;29 USA Hockey Playing Rules, and the exercise is completed when the game official answers the required number of questions correctly:</p>
        <ul>
          <li>Level 1 &mdash; 40 questions</li>
          <li>Level 2 &mdash; 60 questions</li>
          <li>Level 3 &mdash; 80 questions</li>
          <li>Level 4 &mdash; 80 questions</li>
          <li>Tenured (L3 or L4) &mdash; 40 questions</li>
        </ul>
        <p>It is strongly recommended that you use your copy of the 2025&ndash;29 USA Hockey Playing Rules to answer the questions.</p>
      </div>
    </details>
    <details class="info">
      <summary>Classroom seminar attendance</summary>
      <div class="info-body">
        <p>Attendance at a sanctioned USA Hockey Officiating Classroom Seminar is required for all applicants, regardless of level and years of experience. Once the seminar is complete, the attendance roster is submitted to the USA Hockey National Office for credit within 24&ndash;48 hours; questions about attendance credit should be directed to the course facilitator.</p>
        <p>An official is not required to attend a seminar in their own state or USA Hockey District &mdash; any sanctioned seminar in any district counts toward membership.</p>
      </div>
    </details>
    <details class="info">
      <summary>Online education modules</summary>
      <div class="info-body">
        <p>Every membership level includes Online Education Module requirements. An official must complete their module training, which includes written and video content and short quizzes.</p>
      </div>
    </details>
    <details class="info">
      <summary>SafeSport training</summary>
      <div class="info-body">
        <p>Officials with a <span data-season="safesport-year">2009</span> birth year or older are required to complete the online U.S. Center for SafeSport education program. The online program is free of charge and is hosted on the U.S. Center for SafeSport web platform.</p>
        <p>All returning officials must renew SafeSport training within 12 months of the previous season&rsquo;s training (e.g., if you completed training on <span data-season="example-trained">September 15, 2025</span>, you must renew by <span data-season="example-renew">September 15, 2026</span>). An official who does not maintain annual training within 12 months becomes ineligible to work any USA Hockey sanctioned game.</p>
      </div>
    </details>
    <details class="info">
      <summary>Background screening</summary>
      <div class="info-body">
        <p>All officials who are 18+ years old by May 1 of the current year must submit to a USA Hockey coordinated criminal background screen. Background screens are valid for two seasons, and no background screen performed by an outside entity or governing body will be accepted.</p>
      </div>
    </details>
    <details class="info">
      <summary>Complete vs. incomplete membership</summary>
      <div class="info-body">
        <p>&ldquo;Complete&rdquo; membership means an official has completed all education requirements at the level for which they applied. &ldquo;Incomplete&rdquo; means an official has submitted a membership application but has not completed all education requirements.</p>
        <p>A new incomplete official may not officiate any USA Hockey sanctioned games until they are completely registered and receive their current season referee card and sweater crest. If a member official does not complete their education requirements by <span data-season="close">December 31, 2026</span>, their membership is closed as &ldquo;incomplete&rdquo; and the membership fee is not refunded.</p>
        <p>Once complete, a membership is valid through November 30 of the following season. All member officials are responsible for tracking their own progress with membership education requirements.</p>
      </div>
    </details>
    <details class="info">
      <summary>Returning after time away (&ldquo;Welcome Back&rdquo; program)</summary>
      <div class="info-body">
        <p>USA Hockey&rsquo;s &ldquo;Welcome Back&rdquo; program assists experienced officials in returning to membership, offering a two-year amnesty to return at the level they last left.</p>
        <ul>
          <li>Away 3&ndash;10 seasons: may return at Level 2 by requesting a paper application from the USA Hockey Office.</li>
          <li>Away 3&ndash;10 seasons but officiating under another governing body (NFHS, NCAA, etc.): submit a letter of request to the USA Hockey National Office and you may be allowed to return at the level you last completed.</li>
          <li>Away more than 10 seasons: contact your District Referee-in-Chief for a level recommendation.</li>
        </ul>
      </div>
    </details>
    <details class="info">
      <summary>Tournament eligibility &amp; game scheduling</summary>
      <div class="info-body">
        <p>To be eligible to officiate in any State, District or National Tournaments, an official must be completely registered on or before December 31 of the current season.</p>
        <p>Registration with the USA Hockey Officiating Program does not guarantee any game assignments. Officials are responsible for obtaining their own game assignments from Local Game Schedulers as designated in each District.</p>
        <p>Any game scheduler who assigns incompletely registered officials is subject to serious liability, as this jeopardizes the insurance coverage of the officials and both teams involved. Whenever possible, only level-qualified officials should be assigned to games. Updated listings of currently registered officials are available from the District Referee-in-Chief on a regular basis.</p>
      </div>
    </details>
    <p class="center mt-2"><a class="btn dark" href="https://membership.usahockey.com/" target="_blank" rel="noopener">Register with USA Hockey</a></p>
    <p class="center" style="color:var(--gray);font-size:0.88rem">Requirements summarized from the official <a href="https://www.usahockey.com/registrationrules" target="_blank" rel="noopener">USA Hockey <span data-season="label">2026&ndash;27</span> Membership Rules &amp; Policies</a>. Always check the USA Hockey page for the latest rules.<br>Season years and dates on this page roll forward automatically each May 1. <strong>Fees, exam question counts and any rule changes still need to be checked by hand each season.</strong></p>
  </div>
</section>
"""

MENTORING = """
<section class="page-banner">
  <div class="container">
    <h1>Mentoring</h1>
    <p class="lede">We take pride in what we do &mdash; and in the officials who come after us.</p>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <h2>Helping New Officials Succeed</h2>
    <p>Officiating is a craft, and nobody masters it alone. The OVHOA takes pride in the quality of our work on the ice, and we take just as much pride in developing the next generation of officials. Every experienced official in this association started out nervous before their first game &mdash; and every one of them got better because someone took the time to help.</p>
    <p>Our mentoring program pairs new officials with experienced members who can answer questions, work games alongside you, and give honest, constructive feedback. The goal is simple: help you succeed as an official, keep you in the game, and improve the game itself &mdash; better officiating makes hockey better for players, coaches, and fans alike.</p>
    <h3>What you can expect</h3>
    <ul>
      <li>Guidance from experienced officials on positioning, signals, penalty standards, and game management</li>
      <li>Support working your first games and honest feedback afterward</li>
      <li>Help navigating registration, seminars, and the game-assignment system</li>
      <li>A group of officials who want you to succeed &mdash; on and off the ice</li>
    </ul>
    <div class="callout">
      <p style="margin:0"><strong>New Level 1 officials:</strong> once you've registered with USA Hockey, message Referee-in-Chief <a href="board-of-directors.html#ken-handley">Ken Handley</a> or President <a href="board-of-directors.html#brian-siuda">Brian Siuda</a> to get connected with a mentor and into the assignment system.</p>
    </div>
    <p class="center mt-2">
      <a class="btn" href="become-an-official.html">Become an Official</a>
      <a class="btn dark" data-contact-btn="ric" href="mailto:ovhoaric@gmail.com">Email Ken Handley</a>
      <a class="btn dark" data-contact-btn="president" href="mailto:president@ovhoarefs.com">Email Brian Siuda</a>
    </p>
  </div>
</section>
"""

RULE_BOOKS = """
<section class="page-banner">
  <div class="container">
    <h1>Rule Books</h1>
    <p class="lede">Know which rulebook governs your game. OVHOA officials work under three different rule sets depending on the league &mdash; USA Hockey rules for youth games, NCAA rules for ACHA and USPHL games, and NFHS/OHSAA regulations for high school games.</p>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Start Here</span>
      <h2>Rules Comparison: USA Hockey vs. NFHS vs. NCAA</h2>
    </div>
    <div class="card" style="padding:1.75rem">
      <p>If you work more than one level, this is the most useful document on this page. Published by the USA Hockey and NFHS Playing Rules Committees, it puts the three rule sets side by side &mdash; rink, equipment, penalties, officiating systems and playing rules &mdash; so you can see exactly what changes when you step onto a different sheet.</p>

      <details class="info">
        <summary>Differences officials notice most</summary>
        <div class="info-body">
          <div class="table-wrap">
            <table class="levels">
              <thead><tr><th>Situation</th><th>USA Hockey</th><th>NFHS</th><th>NCAA</th></tr></thead>
              <tbody>
                <tr><td class="level-name">High stick definition</td><td>Above normal shoulder height</td><td>Above 4 feet</td><td>Above normal shoulder height</td></tr>
                <tr><td class="level-name">Major penalties</td><td>All majors carry a game misconduct</td><td>Stand-alone major option</td><td>Stand-alone major option</td></tr>
                <tr><td class="level-name">Goalkeeper serves own major/misconduct</td><td>No</td><td>Yes</td><td>Yes</td></tr>
                <tr><td class="level-name">Officiating systems</td><td>RR, RLL or 2R-2L (not RRL)</td><td>RR, RRL or 2R-2L</td><td>2R-2L</td></tr>
                <tr><td class="level-name">Face-off to start periods &amp; after goals</td><td>Referee</td><td>Referee; linesperson option</td><td>Linesperson</td></tr>
                <tr><td class="level-name">Icing stoppage</td><td>Immediate when puck crosses goal line</td><td>Immediate when puck crosses goal line</td><td>Hybrid icing</td></tr>
                <tr><td class="level-name">Half-shield facemask for officials</td><td>Required</td><td>Required</td><td>Not required</td></tr>
                <tr><td class="level-name">Period length</td><td>20 minutes maximum</td><td>15 minutes (up to 17 by state)</td><td>20 minutes</td></tr>
                <tr><td class="level-name">Shorthanded team may ice the puck</td><td>Above 14U yes; 14U &amp; younger no</td><td>Allowed</td><td>Allowed</td></tr>
                <tr><td class="level-name">Mercy rule (ending a game early)</td><td>No</td><td>Permitted</td><td>No</td></tr>
                <tr><td class="level-name">Maximum players in uniform</td><td>20 total, 18 skaters</td><td>20 including goalkeepers</td><td>19 players; 2&ndash;3 goalkeepers</td></tr>
              </tbody>
            </table>
          </div>
          <p class="mt-1"><em>A sample only &mdash; the full chart runs 11 pages. Throughout it, a Match Penalty (USA Hockey) and a Disqualification (NFHS &amp; NCAA) are treated as identical: a 5-minute penalty, immediate ejection, and additional suspension.</em></p>
        </div>
      </details>

      <div class="callout">
        <p style="margin:0"><strong>One caution on the NCAA column.</strong> This is the 2025&ndash;26 edition of the chart, built against the <em>2024&ndash;26</em> NCAA rules. The NCAA has since published the 2026&ndash;28 rulebook, which changed several items shown here &mdash; including hand passes (now permitted in the defensive zone), checking from behind (&ldquo;in open ice&rdquo; removed), the goalkeeper&rsquo;s privileged area (removed), the definition of fighting, and offside (the puck must now be controlled with the stick). For NCAA, ACHA and USPHL games, treat the <a href="assets/docs/NCAA_Rulebook_2026-28.pdf" target="_blank" rel="noopener">2026&ndash;28 NCAA rulebook</a> as authoritative.</p>
      </div>

      <p class="center" style="margin-bottom:0"><a class="btn" href="assets/docs/Rules_Comparison_USAH_NFHS_NCAA_2025-26.pdf" target="_blank" rel="noopener">Rules Comparison Chart (PDF)</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container grid" style="gap:1.5rem">

    <div class="card report-block">
      <div class="org-logo"><img src="assets/img/logo-usah.png" alt="USA Hockey" loading="lazy"></div>
      <div>
        <h2>USA Hockey</h2>
        <p><strong>Governs:</strong> all USA Hockey sanctioned youth, high school club, and adult games.</p>
        <p>The current rulebook is the <strong>2025&ndash;29 USA Hockey Playing Rules</strong>. Every registered official needs it &mdash; it is also the reference for your annual Playing Rules Exercise.</p>
        <div class="actions">
          <a class="btn dark" href="https://www.usahockey.com/rulebook" target="_blank" rel="noopener">USA Hockey Rulebook</a>
        </div>
      </div>
    </div>

    <div class="card report-block">
      <div class="org-logo"><img src="assets/img/logo-ncaa.png" alt="NCAA" loading="lazy"></div>
      <div>
        <h2>NCAA Rules</h2>
        <p><strong>Governs:</strong> ACHA and USPHL games. If you are working collegiate club or USPHL junior hockey, this is your rulebook &mdash; not USA Hockey&rsquo;s.</p>
        <details class="info">
          <summary>Major rule changes in the 2026&ndash;28 NCAA rulebook</summary>
          <div class="info-body">
            <ul>
              <li><strong>Helmets (Rule 9.4):</strong> A player who intentionally removes their helmet during play is assessed a minor penalty. A goalkeeper who intentionally removes their helmet/facemask on an opposing breakaway concedes an awarded goal.</li>
              <li><strong>Coincidental penalties (Rule 19):</strong> In the last five minutes of regulation or any time in overtime, a minor to Team A and a major to Team B at the same stoppage means the three-minute differential (one minute against a double minor) is served immediately.</li>
              <li><strong>Major penalties (Rule 20):</strong> A second major penalty in the same game is an automatic game misconduct.</li>
              <li><strong>Goalkeeper penalties (Rule 28.2):</strong> A goalkeeper is not sent to the penalty bench for an offense incurring a major and/or misconduct penalty.</li>
              <li><strong>Goalkeeper&rsquo;s privileged area (Rule 28.4):</strong> Removed.</li>
              <li><strong>Fighting (Rule 48.1):</strong> Fighting is defined as punching or attempting to punch an opponent <em>repeatedly</em>; a single punch is penalized as roughing.</li>
              <li><strong>Checking from behind (Rule 50):</strong> &ldquo;In open ice&rdquo; removed from the rule.</li>
              <li><strong>Hitting after the whistle (Rule 53.3):</strong> Eliminated as its own infraction &mdash; classified as roughing or unsportsmanlike conduct.</li>
              <li><strong>Throwing the stick (Rule 55.5):</strong> Throwing a stick outside the playing area is upgraded from a misconduct to a game misconduct.</li>
              <li><strong>Spitting (Rule 79.5):</strong> Penalized as a game disqualification.</li>
              <li><strong>Faceoffs (Rule 81):</strong> The blade of the stick must be flat on the ice.</li>
              <li><strong>Offside (Rule 86.1):</strong> A player must control the puck with their stick before their skates enter the offensive zone.</li>
              <li><strong>Hand pass (Rule 84):</strong> Hand passes initiated and completed in the defensive zone are permitted.</li>
              <li><strong>Delay of game (new rule):</strong> A dump-in from the attacking team&rsquo;s own side of center that the goalkeeper freezes results in an end-zone faceoff in the defending zone with no defensive substitutions.</li>
              <li><strong>Timeouts (Rule 92.2):</strong> Not usable when your team cannot change players due to an infraction; one timeout per stoppage; no extra regular-season overtime timeout.</li>
              <li><strong>Coach&rsquo;s challenge (Rule 93.4):</strong> A disallowed-goal minor for goalkeeper interference may be challenged; one challenge per stoppage per team.</li>
            </ul>
          </div>
        </details>
        <details class="info">
          <summary>NCAA penalty terminology for USA Hockey officials</summary>
          <div class="info-body">
            <p><strong>Game misconduct (Rule 22):</strong> Suspension for the balance of the game; a substitute may replace the player immediately. With a major + game misconduct, the team places a substitute in the box to serve the major.</p>
            <p><strong>Disqualification (Rule 23):</strong> The NCAA&rsquo;s equivalent of a match-type removal &mdash; the player is removed for the remainder of the game <em>plus</em> a major penalty, with progressive suspensions for repeat disqualifications (first DQ: that game plus one; second: plus two; and so on). DQs carry over season to season for players with remaining eligibility.</p>
            <p>There is no &ldquo;match penalty&rdquo; category in the NCAA book &mdash; conduct that draws a match penalty under USA Hockey rules is generally a disqualification under NCAA rules.</p>
          </div>
        </details>
        <div class="actions">
          <a class="btn" href="assets/docs/NCAA_Rulebook_2026-28.pdf" target="_blank" rel="noopener">2026&ndash;28 NCAA Rulebook (PDF)</a>
        </div>
      </div>
    </div>

    <div class="card report-block">
      <div class="org-logo"><img src="assets/img/logo-acha.png" alt="ACHA" loading="lazy"></div>
      <div>
        <h2>ACHA</h2>
        <p><strong>Governs:</strong> American Collegiate Hockey Association (collegiate club) games.</p>
        <p>The ACHA plays under the <strong>NCAA rulebook</strong> &mdash; use the 2026&ndash;28 NCAA rules above. The ACHA does not publish a separate rule-modifications list; any division-specific directives come through the league and your assigner. Questions about ACHA rule application should go to our Referee-in-Chief, <a data-contact-link="ric" href="mailto:ovhoaric@gmail.com">Ken Handley</a>.</p>
        <p>Penalty reporting for ACHA games is on our <a href="file-a-report.html">File a Report</a> page.</p>
        <div class="actions">
          <a class="btn dark" href="https://www.achahockey.org/" target="_blank" rel="noopener">ACHA Website</a>
        </div>
      </div>
    </div>

    <div class="card report-block">
      <div class="org-logo"><img src="assets/img/logo-usphl.png" alt="USPHL - United States Premier Hockey League" loading="lazy"></div>
      <div>
        <h2>USPHL</h2>
        <p><strong>Governs:</strong> USPHL (NCDC and Premier) junior games.</p>
        <p>The USPHL plays under the <strong>2026&ndash;28 NCAA rulebook</strong> with league-specific exceptions. The official 2026&ndash;27 Officiating Team Handbook below covers the league&rsquo;s protocols and variances &mdash; read it in full before your first USPHL assignment.</p>
        <details class="info">
          <summary>Key USPHL variances from NCAA rules</summary>
          <div class="info-body">
            <ul>
              <li><strong>Fighting:</strong> In lieu of a game disqualification, a player receives a game misconduct. Any <em>secondary</em> fight is a major + disqualification. Non-participating players must clear to their benches (Rule 48.2) &mdash; strictly enforced.</li>
              <li><strong>Helmet removal in an altercation:</strong> Treated as grasping the facemask (Rule 47.1) and penalized as a disqualification &mdash; no game-misconduct option.</li>
              <li><strong>Coincidental minors:</strong> On-ice strength stays 5-on-5 in all divisions.</li>
              <li><strong>High-sticking a player with a half shield:</strong> Escalating options based on severity &mdash; minor (no injury), double minor (accidental), major + game misconduct, or major + disqualification.</li>
              <li><strong>Overtime:</strong> Games cannot end in a tie &mdash; 5-minute 3-on-3 overtime, then a 3-man shootout, then sudden-death shootout with new shooters until the roster is exhausted.</li>
              <li><strong>Mercy rule (Premier):</strong> After the first period, an 8+ goal differential runs the clock (except power plays). Any major during mercy-rule time is an automatic disqualification.</li>
              <li><strong>Video review (NCDC only):</strong> One coach&rsquo;s challenge per game, contested goals only; officials may not initiate a review.</li>
            </ul>
          </div>
        </details>
        <div class="actions">
          <a class="btn" href="assets/docs/USPHL_Officiating_Handbook_2026-27.pdf" target="_blank" rel="noopener">USPHL Officiating Handbook 2026&ndash;27 (PDF)</a>
        </div>
      </div>
    </div>

    <div class="card report-block">
      <div class="org-logo"><img src="assets/img/logo-ohsaa.png" alt="OHSAA" loading="lazy"></div>
      <div>
        <h2>OHSAA / NFHS</h2>
        <p><strong>Governs:</strong> Ohio varsity high school games.</p>
        <p>OHSAA ice hockey is played under NFHS rules with OHSAA regulations. Rulebooks and officials&rsquo; materials are distributed through your OHSAA officials account.</p>
        <div class="actions">
          <a class="btn dark" href="https://www.ohsaa.org/sports/ihk" target="_blank" rel="noopener">OHSAA Ice Hockey</a>
          <a class="btn dark" href="http://officials.myohsaa.org/Logon" target="_blank" rel="noopener">OHSAA Officials Login</a>
        </div>
      </div>
    </div>

  </div>
</section>
"""

SCOREKEEPERS = """
<section class="page-banner">
  <div class="container">
    <h1>Scorekeeper's Guide</h1>
    <p class="lede">Resources for off-ice officials.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="callout coming-soon">
      <h2>Scorekeeper's guide coming soon</h2>
      <p>Questions in the meantime? <a href="contact-us.html">Contact the board</a>.</p>
    </div>
  </div>
</section>
"""

RINKS = """
<section class="page-banner">
  <div class="container">
    <h1>Rink Locations</h1>
    <p class="lede">Where we work. Addresses and directions for the rinks OVHOA officials are assigned to across Greater Cincinnati and Northern Kentucky.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <!-- Filled from the Rinks tab of the Google Sheet (Name | Address | Notes).
         Until that tab exists the empty state below is shown. -->
    <div class="board-grid" data-sheet-rinks>
      <div class="callout coming-soon" style="grid-column:1/-1">
        <h2>Rink list coming soon</h2>
        <p>We&rsquo;re putting together addresses, parking notes and locker-room details for every rink we cover. Working a rink you don&rsquo;t know? Ask your <a href="board-of-directors.html#bryan-thurnauer">scheduler</a> in the meantime.</p>
      </div>
    </div>
  </div>
</section>
"""

PAGES = {
    "index.html": ("Home", "Greater Cincinnati and Northern Kentucky ice hockey officials association.", HOME),
    "history.html": ("History", "The history of the Ohio Valley Hockey Officials Association, officiating hockey since the early 1970s.", HISTORY),
    "board-of-directors.html": ("Board of Directors", "Meet the OVHOA Executive Board of Directors.", BOARD),
    "official-documents.html": ("Official Documents", "OVHOA bylaws, manual, and other important documents.", DOCUMENTS),
    "contact-us.html": ("Contact Us", "Contact the OVHOA Board of Directors.", CONTACT),
    "rinks.html": ("Rink Locations", "Addresses and directions for the rinks OVHOA officials work across Greater Cincinnati and Northern Kentucky.", RINKS),
    "file-a-report.html": ("File a Report", "Penalty and incident reporting tools for USA Hockey, OHSAA, and ACHA games.", FILE_REPORT),
    "become-an-official.html": ("Become an Official", "How to register as a USA Hockey official: levels, requirements, exams, and seminars.", BECOME),
    "mentoring.html": ("Mentoring", "The OVHOA mentoring program helps new officials succeed and improves the game.", MENTORING),
    "rule-books.html": ("Rule Books", "Rule reference books for USA Hockey, ACHA, and OHSAA games.", RULE_BOOKS),
    "scorekeepers-guide.html": ("Scorekeeper's Guide", "Scorekeeping resources for OVHOA off-ice officials.", SCOREKEEPERS),
}


SITE_URL = "https://ovhoarefs.com"
NL = chr(10)

# Pages we most want search engines to surface.
SITEMAP_PRIORITY = {
    "index.html": "1.0",
    "become-an-official.html": "0.9",
    "file-a-report.html": "0.8",
    "rinks.html": "0.8",
    "rule-books.html": "0.8",
    "contact-us.html": "0.7",
}


def write_sitemap():
    '''robots.txt + sitemap.xml, generated so they cannot drift from PAGES.'''
    today = datetime.date.today().isoformat()
    urls = []
    for fname in PAGES:
        loc = SITE_URL + "/" if fname == "index.html" else SITE_URL + "/" + fname
        urls.append(
            "  <url>" + NL
            + "    <loc>" + loc + "</loc>" + NL
            + "    <lastmod>" + today + "</lastmod>" + NL
            + "    <priority>" + SITEMAP_PRIORITY.get(fname, "0.6") + "</priority>" + NL
            + "  </url>"
        )
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>' + NL
               + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + NL
               + NL.join(urls) + NL + "</urlset>" + NL)
    with io.open(os.path.join(OUT_DIR, "sitemap.xml"), "w",
                 encoding="utf-8", newline=NL) as f:
        f.write(sitemap)
    print("wrote sitemap.xml (%d urls)" % len(PAGES))

    robots = ("User-agent: *" + NL
              + "Allow: /" + NL
              + NL
              + "Sitemap: " + SITE_URL + "/sitemap.xml" + NL)
    with io.open(os.path.join(OUT_DIR, "robots.txt"), "w",
                 encoding="utf-8", newline=NL) as f:
        f.write(robots)
    print("wrote robots.txt")


def main():
    for fname, (title, desc, body) in PAGES.items():
        html = page(title, desc, fname, body)
        with io.open(os.path.join(OUT_DIR, fname), "w",
                     encoding="utf-8", newline=NL) as f:
            f.write(html)
        print("wrote %s (%d bytes)" % (fname, len(html)))
    write_sitemap()


if __name__ == "__main__":
    main()
