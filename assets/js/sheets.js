/* ==========================================================================
   OVHOA — Google Sheets content loader
   Board members edit a Google Sheet; this script pulls the data in when a
   page loads. If the sheet is unreachable (or SHEET_ID is empty), the page
   keeps the content baked into the HTML — nothing breaks.

   SETUP (one time):
   1. Create a Google Sheet with two tabs, named exactly:  Meetings  and  Board
      - Meetings columns (row 1 headers): Date | Time | Format | Note
        e.g.  "9/2/2026"        | "7:30 PM" | Zoom      | Board Meeting
              "March 15, 2026"  | "7 PM"    | In Person | Location TBA
      - Board columns (row 1 headers): Name | Role | Email
        Rows appear on the site in the same order as the sheet, so reorder
        rows in the sheet to reorder the cards on the site.
   2. Share → General access → "Anyone with the link" → Viewer.
   3. Copy the sheet ID from its URL:
      https://docs.google.com/spreadsheets/d/<THIS-LONG-ID>/edit
   4. Paste the ID into SHEET_ID below and redeploy.

   PAST MEETINGS: a meeting disappears from the site automatically once it is
   more than GRACE_DAYS days old, so the board never has to delete old rows —
   leave them in the sheet as a record and the site just stops showing them.
   A row whose Date can't be understood is always shown (better to show a
   meeting than to hide one by accident).

   NOTE: everything in these two tabs is publicly readable — names, roles and
   the ovhoarefs.com addresses are already public on the site, but don't add
   personal phone numbers or private notes to them.
   ========================================================================== */

var SHEET_ID = "1ydw-_uRCqfUadJOkA0rkSs6o215mdGB0YRl7UtYnw0k"; // just the ID: the part of the sheet URL between /d/ and /edit

var GRACE_DAYS = 1; // days a meeting stays listed after its date (set to 2 for a longer grace period)

(function () {

  /* ---------- season-dependent years -------------------------------------

     USA Hockey restates the same requirements each season with the years
     rolled forward. Rather than hand-editing the Become an Official page
     every summer, elements marked data-season="..." are filled in from the
     current membership year, which opens on May 1.

     These are DERIVED, not authoritative. Fees, exam question counts and
     any rule changes still need a human to check them against
     usahockey.com/registrationrules each season. If USA Hockey changes one
     of the derived dates, add a "Season" tab to the Google Sheet with
     Key | Value columns to override any key below.
     ---------------------------------------------------------------------- */

  function seasonStartYear() {
    var now = new Date();
    // The membership year opens May 1 (month index 4).
    return now.getMonth() >= 4 ? now.getFullYear() : now.getFullYear() - 1;
  }

  function seasonValues(y) {
    var short = function (n) { return String(n).slice(2); };
    return {
      "label": y + "–" + short(y + 1),          // 2026-27
      "prev-label": (y - 1) + "–" + short(y),   // 2025-26
      "open": "May 1, " + y,
      "close-apps": "November 20, " + y,
      "expire-prev": "November 30, " + y,
      "seminars-end": "December 15, " + y,
      "close": "December 31, " + y,
      // SafeSport applies from the season's 17-and-older birth year.
      "safesport-year": String(y - 17),
      // Illustrative dates in the SafeSport 12-month renewal example.
      "example-trained": "September 15, " + (y - 1),
      "example-renew": "September 15, " + y
    };
  }

  function applySeason(overrides) {
    var values = seasonValues(seasonStartYear());
    if (overrides) {
      Object.keys(overrides).forEach(function (k) {
        if (overrides[k]) values[k] = overrides[k];
      });
    }
    Array.prototype.slice.call(document.querySelectorAll("[data-season]"))
      .forEach(function (el) {
        var v = values[el.getAttribute("data-season")];
        if (v) el.textContent = v;
      });
  }

  var seasonEls = document.querySelector("[data-season]");
  if (seasonEls) applySeason(null);

  /* ---------- dates ----------------------------------------------------- */

  var MONTHS = {
    jan: 0, feb: 1, mar: 2, apr: 3, may: 4, jun: 5,
    jul: 6, aug: 7, sep: 8, oct: 9, nov: 10, dec: 11
  };

  // Understands "9/2/2026", "2026-09-02", "Sunday, March 15, 2026",
  // "March 15, 2026" and "15 March 2026". Returns a local-midnight Date,
  // or null when the text can't be read as a date.
  function parseMeetingDate(raw) {
    if (!raw) return null;
    var s = String(raw).trim().replace(/^[A-Za-z]+,\s*/, ""); // drop weekday
    if (!s) return null;
    var m, mo;

    m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/); // 2026-09-02
    if (m) return new Date(+m[1], +m[2] - 1, +m[3]);

    m = s.match(/^(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{2,4})/); // 9/2/2026
    if (m) {
      var y = +m[3];
      if (y < 100) y += 2000;
      return new Date(y, +m[1] - 1, +m[2]);
    }

    m = s.match(/^([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})/); // March 15, 2026
    if (m) {
      mo = MONTHS[m[1].slice(0, 3).toLowerCase()];
      if (mo !== undefined) return new Date(+m[3], mo, +m[2]);
    }

    m = s.match(/^(\d{1,2})\s+([A-Za-z]+),?\s*(\d{4})/); // 15 March 2026
    if (m) {
      mo = MONTHS[m[2].slice(0, 3).toLowerCase()];
      if (mo !== undefined) return new Date(+m[3], mo, +m[1]);
    }

    return null;
  }

  // True only when the date was readable AND is well past.
  function isExpired(date) {
    if (!date) return false;
    var today = new Date();
    today.setHours(0, 0, 0, 0);
    return Math.round((today - date) / 86400000) > GRACE_DAYS;
  }

  function showEmptyState(list) {
    if (list.children.length) return;
    var li = document.createElement("li");
    li.className = "meeting-empty";
    li.textContent = "No meetings are currently scheduled — check back soon.";
    list.appendChild(li);
  }

  /* ---------- CSV ------------------------------------------------------- */

  function csvUrl(tab) {
    return "https://docs.google.com/spreadsheets/d/" + SHEET_ID +
      "/gviz/tq?tqx=out:csv&sheet=" + encodeURIComponent(tab);
  }

  // Minimal CSV parser (handles quoted fields with commas and newlines)
  function parseCSV(text) {
    var rows = [], row = [], field = "", inQuotes = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (inQuotes) {
        if (c === '"') {
          if (text[i + 1] === '"') { field += '"'; i++; }
          else { inQuotes = false; }
        } else { field += c; }
      } else if (c === '"') {
        inQuotes = true;
      } else if (c === ",") {
        row.push(field); field = "";
      } else if (c === "\n" || c === "\r") {
        if (c === "\r" && text[i + 1] === "\n") i++;
        row.push(field); field = "";
        if (row.length > 1 || row[0] !== "") rows.push(row);
        row = [];
      } else { field += c; }
    }
    if (field !== "" || row.length) { row.push(field); rows.push(row); }
    return rows;
  }

  // Turn rows into objects keyed by lowercased header names
  function toRecords(rows) {
    if (rows.length < 2) return [];
    var headers = rows[0].map(function (h) { return h.trim().toLowerCase(); });
    return rows.slice(1).map(function (r) {
      var rec = {};
      headers.forEach(function (h, i) { rec[h] = (r[i] || "").trim(); });
      return rec;
    }).filter(function (rec) {
      return Object.keys(rec).some(function (k) { return rec[k] !== ""; });
    });
  }

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  function fetchTab(tab) {
    return fetch(csvUrl(tab)).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.text();
    }).then(function (text) { return toRecords(parseCSV(text)); });
  }

  // Google returns the FIRST tab (not an error) when the requested tab name
  // doesn't exist, so a missing "Rinks" tab would otherwise render the
  // Meetings rows as rinks. Each consumer names a column it expects, and we
  // check the HEADER row - a tab that exists but has no data rows yet is
  // legitimate and must not be mistaken for the wrong tab.
  function fetchTabWithColumns(tab, names) {
    return fetch(csvUrl(tab)).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.text();
    }).then(function (text) {
      var rows = parseCSV(text);
      if (!rows.length) return [];
      var headers = rows[0].map(function (h) { return h.trim().toLowerCase(); });
      var matches = names.some(function (n) { return headers.indexOf(n) !== -1; });
      if (!matches) {
        console.warn("Sheet tab \"" + tab + "\" is missing (or its headers changed); ignoring.");
        return [];
      }
      return toRecords(rows);
    });
  }

  /* ---------- meetings --------------------------------------------------- */

  var meetingList = document.querySelector("[data-sheet-meetings]");

  // Expire the meetings baked into the HTML first, so stale dates never show
  // even when the sheet is unreachable or not yet configured.
  if (meetingList) {
    Array.prototype.slice.call(meetingList.querySelectorAll("li[data-date]"))
      .forEach(function (li) {
        if (isExpired(parseMeetingDate(li.getAttribute("data-date")))) {
          li.parentNode.removeChild(li);
        }
      });
    showEmptyState(meetingList);
  }

  if (!SHEET_ID) return;

  if (meetingList) {
    fetchTabWithColumns("Meetings", ["date", "when"]).then(function (records) {
      // An empty Meetings tab means "not filled in yet" — keep the baked-in
      // list rather than blanking the section. Rows that all expired do
      // correctly produce the "no meetings" message.
      if (!records.length) return;
      var upcoming = records.filter(function (m) {
        return !isExpired(parseMeetingDate(m.date || m.when));
      });
      meetingList.innerHTML = upcoming.map(function (m) {
        var fmt = (m.format || "").toLowerCase();
        var pillClass = fmt.indexOf("person") !== -1 ? "badge-pill in-person" : "badge-pill";
        var label = m.format || "";
        if (m.note) label += " · " + m.note;
        // Separate Date + Time columns, joined for display; a legacy single
        // "When" column still works as-is.
        var when = m.when || (m.date || "") + (m.time ? " · " + m.time : "");
        return "<li><span class=\"when\">" + esc(when) + "</span> " +
          (label ? "<span class=\"" + pillClass + "\">" + esc(label) + "</span>" : "") +
          "</li>";
      }).join("");
      showEmptyState(meetingList);
    }).catch(function (e) { console.warn("Meetings sheet unavailable:", e); });
  }

  /* ---------- contact details keyed off the Board tab ---------------------

     Any element carrying data-contact / data-contact-btn / data-contact-link
     has its name + address filled in from the Board tab, so changing an
     address in the sheet (or moving the whole association to a new domain)
     updates every page at once. Keys map to Role values as below; a key that
     matches no row simply leaves the baked-in fallback text in place.
     ---------------------------------------------------------------------- */

  var ROLE_KEYS = {
    president: ["president", "executivepresident"],
    vicepresident: ["vicepresident", "executivevicepresident"],
    treasurer: ["treasurer", "executivetreasurer"],
    secretary: ["secretary", "executivesecretary"],
    ric: ["ric", "localric", "refereeinchief"],
    scheduler: ["scheduler", "gamescheduler", "assignor"],
    mentoring: ["mentoring", "mentoringcoordinator"]
  };

  function normalizeRole(s) {
    return String(s || "").toLowerCase().replace(/[^a-z]/g, "");
  }

  // Find the board row whose Role matches a key like "ric" or "president".
  function findByKey(records, key) {
    var aliases = ROLE_KEYS[normalizeRole(key)];
    if (!aliases) return null;
    for (var i = 0; i < records.length; i++) {
      if (aliases.indexOf(normalizeRole(records[i].role)) !== -1) return records[i];
    }
    return null;
  }

  function lookupAll(records, keyList) {
    var people = String(keyList).split(",").map(function (k) {
      return findByKey(records, k.trim());
    });
    // Only rewrite when every key resolved, so a card never ends up
    // half-updated with one live address and one stale one.
    return people.indexOf(null) === -1 ? people : null;
  }

  function applyContacts(records) {
    // Cards: rewrite the role line and the address block.
    Array.prototype.slice.call(document.querySelectorAll("[data-contact]")).forEach(function (card) {
      var people = lookupAll(records, card.getAttribute("data-contact"));
      if (!people) return;

      var roleEl = card.querySelector("[data-contact-role]");
      if (roleEl) {
        roleEl.innerHTML = people.length === 1
          ? esc(people[0].role) + " &mdash; " + esc(people[0].name)
          : people.map(function (p) {
              return esc(p.name) + " (" + esc(p.role) + ")";
            }).join(" or ");
      }

      var mailEl = card.querySelector("[data-contact-email]");
      if (mailEl) {
        mailEl.innerHTML = people.filter(function (p) { return p.email; })
          .map(function (p) {
            return "<a href=\"mailto:" + esc(p.email) + "\">" + esc(p.email) + "</a>";
          }).join("<br>");
      }
    });

    // Buttons: "Email <name>" plus the mailto target.
    Array.prototype.slice.call(document.querySelectorAll("[data-contact-btn]")).forEach(function (btn) {
      var person = findByKey(records, btn.getAttribute("data-contact-btn"));
      if (!person || !person.email) return;
      btn.setAttribute("href", "mailto:" + person.email);
      btn.textContent = "Email " + person.name;
    });

    // Inline links: the link text is the person's name.
    Array.prototype.slice.call(document.querySelectorAll("[data-contact-link]")).forEach(function (link) {
      var person = findByKey(records, link.getAttribute("data-contact-link"));
      if (!person || !person.email) return;
      link.setAttribute("href", "mailto:" + person.email);
      link.textContent = person.name;
    });
  }

  /* ---------- optional Season overrides ----------------------------------- */

  if (seasonEls && SHEET_ID) {
    fetchTabWithColumns("Season", ["key"]).then(function (records) {
      if (!records.length) return;
      var overrides = {};
      records.forEach(function (r) {
        if (r.key) overrides[r.key.trim()] = r.value;
      });
      applySeason(overrides);
    }).catch(function () { /* no Season tab: derived values stand */ });
  }

  /* ---------- homepage announcement banner --------------------------------

     Banner tab: Header | Text  (an optional Author column is used as a
     by-line if present). The banner stays hidden unless a row has content,
     so clearing the row removes it from the site.
     ---------------------------------------------------------------------- */

  var banner = document.querySelector("[data-sheet-banner]");
  if (banner && SHEET_ID) {
    fetchTabWithColumns("Banner", ["header", "text"]).then(function (records) {
      var row = records.filter(function (r) {
        return (r.header || "") !== "" || (r.text || "") !== "";
      })[0];
      if (!row) return;
      var html = "";
      if (row.header) html += "<h2>" + esc(row.header) + "</h2>";
      if (row.text) html += "<p>" + esc(row.text) + "</p>";
      if (row.author) html += "<p class=\"byline\">&mdash; " + esc(row.author) + "</p>";
      banner.querySelector(".container").innerHTML = html;
      banner.hidden = false;
    }).catch(function (e) { console.warn("Banner sheet unavailable:", e); });
  }

  /* ---------- rink locations ----------------------------------------------

     Rinks tab: Name | Address | Notes
     The address is turned into a tap-to-navigate maps link.
     ---------------------------------------------------------------------- */

  var rinkGrid = document.querySelector("[data-sheet-rinks]");
  if (rinkGrid && SHEET_ID) {
    fetchTabWithColumns("Rinks", ["name", "rink"]).then(function (records) {
      var rinks = records.filter(function (r) { return (r.name || r.rink || "") !== ""; });
      if (!rinks.length) return;
      rinkGrid.innerHTML = rinks.map(function (r) {
        var name = r.name || r.rink || "";
        var addr = r.address || "";
        var maps = "https://www.google.com/maps/search/?api=1&query=" +
          encodeURIComponent(name + (addr ? " " + addr : ""));
        return "<div class=\"card rink-card\">" +
          "<h3>" + esc(name) + "</h3>" +
          (addr ? "<p class=\"rink-address\">" + esc(addr) + "</p>" : "") +
          (r.notes ? "<p class=\"rink-notes\">" + esc(r.notes) + "</p>" : "") +
          "<p><a class=\"btn dark\" href=\"" + maps + "\" target=\"_blank\" rel=\"noopener\">Directions</a></p>" +
          "</div>";
      }).join("");
    }).catch(function (e) { console.warn("Rinks sheet unavailable:", e); });
  }

  /* ---------- board of directors ----------------------------------------- */

  var boardGrid = document.querySelector("[data-sheet-board]");
  var needsContacts = document.querySelector("[data-contact], [data-contact-btn], [data-contact-link]");

  if (!boardGrid && needsContacts) {
    // Pages that show contact details but not the full roster.
    fetchTabWithColumns("Board", ["name"]).then(function (records) {
      if (records.length) applyContacts(records);
    }).catch(function (e) { console.warn("Board sheet unavailable:", e); });
  }

  if (boardGrid) {
    fetchTabWithColumns("Board", ["name"]).then(function (records) {
      if (!records.length) return;
      applyContacts(records);
      boardGrid.innerHTML = records.map(function (p) {
        var slug = (p.name || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
        return "<div class=\"board-card\" id=\"" + slug + "\">" +
          "<img src=\"assets/img/avatar-placeholder.png\" alt=\"\" loading=\"lazy\">" +
          "<div><h3>" + esc(p.name || "") + "</h3>" +
          "<p class=\"role\">" + esc(p.role || "") + "</p>" +
          (p.email ? "<p><a href=\"mailto:" + esc(p.email) + "\">" + esc(p.email) + "</a></p>" : "") +
          "</div></div>";
      }).join("");
      // If the page was opened with an anchor (#ken-handley), re-jump to it
      // now that the cards have been re-rendered. Use an instant jump: the
      // browser's smooth-scroll animation can be skipped entirely (reduced
      // motion, background tabs), which would leave the visitor at the top
      // of the page instead of on the person they clicked through to see.
      if (location.hash) {
        var target = document.getElementById(location.hash.slice(1));
        if (target) {
          try { target.scrollIntoView({ behavior: "instant", block: "start" }); }
          catch (e) { target.scrollIntoView(); }
        }
      }
    }).catch(function (e) { console.warn("Board sheet unavailable:", e); });
  }
})();
