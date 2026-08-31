#!/usr/bin/env python3
"""Generates the OVHOA static site: one shared header/footer/template, nine pages.

Run:  python build.py
Output: *.html in this directory. Edit page content in the PAGES dict below.
"""
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
    ("Education & Development", None, [
        ("Become an Official", "become-an-official.html"),
        ("Rule Books", "rule-books.html"),
        ("Scorekeeper's Guide", "scorekeepers-guide.html"),
    ]),
    ("Important Links", None, [
        ("USAH Registration", "https://membership.usahockey.com/"),
        ("Arbiter Sports Login", "https://www1.arbitersports.com/shared/signin/signin.aspx"),
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
          <li><a href="become-an-official.html">Become an Official</a></li>
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
          <li><a href="https://www.ncaa.com/" target="_blank" rel="noopener">NCAA</a></li>
          <li><a href="https://www.nfhs.org/" target="_blank" rel="noopener">NFHS</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Ohio Valley Hockey Officials Association</span>
      <span><a href="https://www1.arbitersports.com/shared/signin/signin.aspx" target="_blank" rel="noopener">Arbiter Sports Login</a></span>
    </div>
  </div>
</footer>
<script src="assets/js/nav.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Page bodies
# ---------------------------------------------------------------------------

HOME = """
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
      <span class="kicker">2025&ndash;2026 Season</span>
      <h2>OVHOA General Meetings</h2>
    </div>
    <ul class="meeting-list card">
      <li><span class="when">Sunday, November 16, 2025 &middot; 7 PM</span> <span class="badge-pill">Zoom</span></li>
      <li><span class="when">Sunday, December 14, 2025 &middot; 7 PM</span> <span class="badge-pill">Zoom</span></li>
      <li><span class="when">Monday, January 26, 2026 &middot; 7 PM</span> <span class="badge-pill">Zoom</span></li>
      <li><span class="when">Tuesday, February 24, 2026 &middot; 7 PM</span> <span class="badge-pill">Zoom</span></li>
      <li><span class="when">Sunday, March 15, 2026 &middot; 7 PM</span> <span class="badge-pill in-person">In Person &middot; Location TBA</span></li>
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
    return f"""
      <div class="board-card">
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
    <div class="board-grid">
      {board_member("Brian Siuda", "Executive President", "president@ovhoarefs.com")}
      {board_member("Jeremy MacWalter", "Executive Vice President", "vicepresident@ovhoarefs.com")}
      {board_member("Chris Sharon", "Executive Treasurer", "treasurer@ovhoarefs.com")}
      {board_member("Nick Doud", "Executive Secretary", "secretary@ovhoarefs.com")}
      {board_member("Ken Handley", "Referee-in-Chief", "ric@ovhoarefs.com")}
      {board_member("Bryan Thurnauer", "Scheduler", "scheduler@ovhoarefs.com")}
      {board_member("Earl Dalton", "Mentoring Coordinator", "mentoring@ovhoarefs.com")}
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
        <a class="btn dark" href="assets/docs/ComingSoon.pdf" target="_blank" rel="noopener">View PDF</a>
      </div>
      <div class="doc-item card">
        <div>
          <span class="doc-name">OVHOA Manual</span>
          <span class="doc-meta">2016&ndash;2017 edition &middot; PDF</span>
        </div>
        <a class="btn dark" href="assets/docs/OVHOA_Manual_2016-2017.pdf" target="_blank" rel="noopener">View PDF</a>
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
    <div class="contact-grid">
      <div class="card contact-card">
        <h3>General Inquiries</h3>
        <p class="role">Executive President &mdash; Brian Siuda</p>
        <p><a href="mailto:president@ovhoarefs.com">president@ovhoarefs.com</a></p>
      </div>
      <div class="card contact-card">
        <h3>Officiating &amp; Rules</h3>
        <p class="role">Referee-in-Chief &mdash; Ken Handley</p>
        <p><a href="mailto:ric@ovhoarefs.com">ric@ovhoarefs.com</a></p>
      </div>
      <div class="card contact-card">
        <h3>Game Scheduling</h3>
        <p class="role">Scheduler &mdash; Bryan Thurnauer</p>
        <p><a href="mailto:scheduler@ovhoarefs.com">scheduler@ovhoarefs.com</a></p>
      </div>
      <div class="card contact-card">
        <h3>New Official Mentoring</h3>
        <p class="role">Mentoring Coordinator &mdash; Earl Dalton</p>
        <p><a href="mailto:mentoring@ovhoarefs.com">mentoring@ovhoarefs.com</a></p>
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
        <p>To report penalties for USA Hockey games, you must use the online USA Hockey tool. For questions, contact <a href="mailto:ric@ovhoarefs.com">Ken Handley</a>.</p>
        <div class="actions"><a class="btn" href="https://www.usahockey.com/officials" target="_blank" rel="noopener">USA Hockey Reporting Tool</a></div>
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
        <div class="actions"><a class="btn" href="http://officials.myohsaa.org/Logon" target="_blank" rel="noopener">OHSAA Officials Login</a></div>
      </div>
    </div>

    <div class="card report-block">
      <div class="org-logo"><img src="assets/img/logo-acha.png" alt="ACHA" loading="lazy"></div>
      <div>
        <h2>ACHA (Collegiate) Games</h2>
        <p>To report penalties for ACHA games, use this Microsoft Word form. When completed, email it <strong>as an attachment</strong> to the appropriate ACHA Commissioner, ACHA Referee-in-Chief, and <a href="mailto:ric@ovhoarefs.com">Ken Handley</a>.</p>
        <div class="actions"><a class="btn" href="assets/docs/ACHA_Incident_Report.docx" download>Download the ACHA Form</a></div>
      </div>
    </div>

  </div>
</section>
"""

BECOME = """
<section class="page-banner">
  <div class="container">
    <h1>Become an Official</h1>
    <p class="lede">Everything you need to know about the USA Hockey Officials Registration Program.</p>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <h2>Registration Basics</h2>
    <p><strong>Registration season.</strong> The registration season for the Officiating Program begins on August 1 and ends on May 9 of the following year. USA Hockey officials registration is valid for the entire season in any district or state in the United States. Membership in a state or local officials association is not required for USA Hockey officials registration.</p>
    <p><strong>Minimum/maximum ages.</strong> USA Hockey has no minimum or maximum ages for officials. It is highly recommended that, regardless of level attained, officials not work games of their own age classification or higher. Generally, officials can successfully officiate as young as age 10.</p>
    <p><strong>New officials (never been registered).</strong> All persons who have never officiated must register at Level 1 for the first season. Only the District Referee-in-Chief, prior to registration, may make exceptions in extreme cases where the applicant has extensive officiating experience that would foster registration at Level 2. No first-time registered official may register above Level 2 for the first season.</p>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="section-title">
      <h2>USA Hockey Officiating Requirements by Level</h2>
    </div>
    <div class="table-wrap">
      <table class="levels">
        <thead><tr><th>Level</th><th>Requirements</th></tr></thead>
        <tbody>
          <tr>
            <td class="level-name">Level 1</td>
            <td><ul>
              <li>Complete the <a href="https://membership.usahockey.com/register/age" target="_blank" rel="noopener">online Membership Application</a></li>
              <li>Submit Officiating Membership fee ($55.00)</li>
              <li>Score 35/50 or higher on the <a href="https://www.usahockey.com/openbookexam" target="_blank" rel="noopener">Open Book Exam</a></li>
              <li>Attend and complete a Level 1 Virtual Classroom Seminar sanctioned by USA Hockey (1.5&ndash;2 hours) taught by national staff</li>
              <li>Attend and complete a local Level 1 In-Person Classroom Seminar sanctioned by USA Hockey that includes an on-ice session (1.5&ndash;3 hours)</li>
            </ul></td>
          </tr>
          <tr>
            <td class="level-name">Level 2</td>
            <td><ul>
              <li>Must have been Level 1 (Complete) within the last two seasons</li>
              <li>Complete the <a href="https://membership.usahockey.com/register/age" target="_blank" rel="noopener">online Membership Application</a></li>
              <li>Submit Officiating Membership fee ($110.00)</li>
              <li>Score 60/75 or higher on the <a href="https://www.usahockey.com/openbookexam" target="_blank" rel="noopener">Open Book Exam</a></li>
              <li>Attend and complete a <a href="https://www.usahockey.com/officialseminars" target="_blank" rel="noopener">Level 2 Virtual Classroom Seminar</a></li>
              <li>Complete the <a href="https://www.usahockey.com/officiatingonlineseminarmodules" target="_blank" rel="noopener">Level 2 Online Education Module curriculum</a></li>
            </ul></td>
          </tr>
          <tr>
            <td class="level-name">Level 3</td>
            <td><ul>
              <li>Must have been Level 2 or higher (Complete) during the previous season</li>
              <li>Complete the <a href="https://membership.usahockey.com/register/age" target="_blank" rel="noopener">online Membership Application</a></li>
              <li>Submit Registration Fee ($110.00)</li>
              <li>Score 85/100* or higher on the <a href="https://www.usahockey.com/openbookexam" target="_blank" rel="noopener">Open Book Exam</a></li>
              <li>Attend and complete a <a href="https://www.usahockey.com/officialseminars" target="_blank" rel="noopener">Level 3 Officiating Virtual Classroom Seminar</a></li>
              <li>Complete the <a href="https://www.usahockey.com/officiatingonlineseminarmodules" target="_blank" rel="noopener">Level 3 Online Education Module curriculum</a></li>
              <li><em>*Level 3 Tenured Officials must attain an Open Book Exam score of 45/50.</em></li>
            </ul></td>
          </tr>
          <tr>
            <td class="level-name">Level 4</td>
            <td><ul>
              <li>Must have been Level 3 or 4 (Complete) last season</li>
              <li>Complete the <a href="https://membership.usahockey.com/register/age" target="_blank" rel="noopener">online Membership Application</a></li>
              <li>Submit Registration Fee ($110.00)</li>
              <li>Score 90/100* or higher on the <a href="https://www.usahockey.com/openbookexam" target="_blank" rel="noopener">Open Book Exam</a></li>
              <li>Attend and complete a <a href="https://www.usahockey.com/officialseminars" target="_blank" rel="noopener">Level 4 Officiating Virtual Classroom Seminar</a></li>
              <li>Complete the <a href="https://www.usahockey.com/officiatingonlineseminarmodules" target="_blank" rel="noopener">Level 4 Online Education Module curriculum</a></li>
              <li><em>*Level 4 Tenured Officials must attain an Open Book Exam score of 45/50.</em></li>
            </ul></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="callout mt-2">
      <p style="margin:0 0 0.5rem"><strong>All levels require:</strong></p>
      <ul style="margin:0">
        <li>Completion of <a href="https://www.usahockey.com/safesportprogram" target="_blank" rel="noopener">SafeSport training</a> (if 2006 birth year or older)</li>
        <li>Completion and maintenance of a USA Hockey sanctioned criminal <a href="https://www.usahockey.com/backgroundscreen" target="_blank" rel="noopener">Background Screen</a> if 18+ years old on June 1</li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <h2>Program Details</h2>
    <details class="info">
      <summary>Complete vs. incomplete registration</summary>
      <div class="info-body">
        <p>&ldquo;Complete&rdquo; means an official has met all the criteria (testing and seminars) at the level for which they applied. &ldquo;Incomplete&rdquo; means an official has filed an application but has not completed all the necessary criteria for that level.</p>
        <p>A new official (not registered the previous year) may not officiate until completely registered. A returning official (complete the previous season) may not officiate after November 30 (the expiration date on the previous year&rsquo;s card) unless completely registered for the new season.</p>
      </div>
    </details>
    <details class="info">
      <summary>Open book rules exam</summary>
      <div class="info-body">
        <p>Each season all officials must complete the open book rules exam. Officials who do not receive the minimum score for the appropriate level will be sent a retake notice and a new answer sheet. Only one retake exam per official is allowed, and it must be completed within 30 days. If an official fails the exam twice, they become completely registered at the highest level for which the retake exam score would qualify.</p>
      </div>
    </details>
    <details class="info">
      <summary>Renewal officials</summary>
      <div class="info-body">
        <p>Renewal officials may apply for one level higher than their completed registration level from the previous season. Officials are allowed to take one season as unregistered or incomplete and return at the same level they were last completely registered at. Level 1 completely registered officials are allowed to take one season off and still be eligible for Level 2 the following season.</p>
        <p>The eligible level for each renewal official is designated on the pre-printed officiating application. An official may apply for a lower level than their eligible level; however, once the application has been received at the National Office, an official cannot change the level they applied for.</p>
      </div>
    </details>
    <details class="info">
      <summary>Returning after a season (or more) away</summary>
      <div class="info-body">
        <p>We are always happy to have officials return to the USA Hockey Officiating Program after some time away. Because of your past experience you may be able to register at a level higher than Level 1, depending on the level at which you were last registered. As a general rule, officials may take one season off (unregistered or incomplete) without forfeiting current level status. If an official is off for the previous two seasons, they must apply for registration one level lower (except Level 1) than the last season completely registered. A Level 4 official who takes 3 or more seasons off will be required to return at Level 2.</p>
      </div>
    </details>
    <details class="info">
      <summary>Seminar attendance</summary>
      <div class="info-body">
        <p>Attendance at a sanctioned USA Hockey Officials Seminar is required for all applicants, regardless of level. The seminar must consist of both classroom and ice time, conducted by USA Hockey Trained Instructors. Every official and instructor in attendance must sign in on the official USA Hockey Seminar Attendance Form, which is returned to the National Office and recorded in each official&rsquo;s record.</p>
        <p>Level 4 applicants must attend a Level 4&ndash;specific seminar. There is no opportunity to complete the Level 2, 3, or 4 closed book testing except at the USA Hockey seminar you attend.</p>
      </div>
    </details>
    <details class="info">
      <summary>Championships eligibility &amp; game scheduling</summary>
      <div class="info-body">
        <p>To be eligible to officiate in any State, Regional or National Championships, an official must be completely registered on or before December 31 of the current season. Only Level 4 officials are eligible to referee National Championships.</p>
        <p>Registration with the USA Hockey Officiating Program does not guarantee any game assignments. Officials are responsible for obtaining their own game assignments from local game schedulers as designated in each District.</p>
        <p>Any game scheduler who assigns incompletely registered officials is subject to serious liability, as this jeopardizes the insurance coverage of the officials and both teams involved. Whenever possible, only qualified officials should be assigned to games. Updated listings of currently registered officials are available from the District Referee-in-Chief on a regular basis.</p>
      </div>
    </details>
    <p class="center mt-2"><a class="btn" href="https://membership.usahockey.com/" target="_blank" rel="noopener">Register with USA Hockey</a></p>
  </div>
</section>
"""

RULE_BOOKS = """
<section class="page-banner">
  <div class="container">
    <h1>Rule Books</h1>
    <p class="lede">Rule references for the leagues we officiate.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="callout coming-soon">
      <h2>Rule reference book links coming soon</h2>
      <p>In the meantime, the current rulebooks are available directly from each governing body:</p>
      <p>
        <a class="btn dark" href="https://www.usahockey.com/rulebook" target="_blank" rel="noopener">USA Hockey Rulebook</a>
        <a class="btn dark" href="https://www.achahockey.org/" target="_blank" rel="noopener">ACHA</a>
        <a class="btn dark" href="https://www.ohsaa.org/sports/ihk" target="_blank" rel="noopener">OHSAA Ice Hockey</a>
      </p>
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

PAGES = {
    "index.html": ("Home", "Greater Cincinnati and Northern Kentucky ice hockey officials association.", HOME),
    "history.html": ("History", "The history of the Ohio Valley Hockey Officials Association, officiating hockey since the early 1970s.", HISTORY),
    "board-of-directors.html": ("Board of Directors", "Meet the OVHOA Executive Board of Directors.", BOARD),
    "official-documents.html": ("Official Documents", "OVHOA bylaws, manual, and other important documents.", DOCUMENTS),
    "contact-us.html": ("Contact Us", "Contact the OVHOA Board of Directors.", CONTACT),
    "file-a-report.html": ("File a Report", "Penalty and incident reporting tools for USA Hockey, OHSAA, and ACHA games.", FILE_REPORT),
    "become-an-official.html": ("Become an Official", "How to register as a USA Hockey official: levels, requirements, exams, and seminars.", BECOME),
    "rule-books.html": ("Rule Books", "Rule reference books for USA Hockey, ACHA, and OHSAA games.", RULE_BOOKS),
    "scorekeepers-guide.html": ("Scorekeeper's Guide", "Scorekeeping resources for OVHOA off-ice officials.", SCOREKEEPERS),
}


def main():
    for fname, (title, desc, body) in PAGES.items():
        html = page(title, desc, fname, body)
        with io.open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print(f"wrote {fname} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
