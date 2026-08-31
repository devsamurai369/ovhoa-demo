// Mobile nav toggle + dropdown submenus (click on mobile, hover handled by CSS-free JS for accessibility)
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll(".site-nav .submenu-toggle").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var li = btn.parentElement;
      var wasOpen = li.classList.contains("open");
      document.querySelectorAll(".site-nav li.open").forEach(function (other) {
        other.classList.remove("open");
        var b = other.querySelector(".submenu-toggle");
        if (b) b.setAttribute("aria-expanded", "false");
      });
      if (!wasOpen) {
        li.classList.add("open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  // Close dropdowns when clicking outside
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".site-nav")) {
      document.querySelectorAll(".site-nav li.open").forEach(function (li) {
        li.classList.remove("open");
        var b = li.querySelector(".submenu-toggle");
        if (b) b.setAttribute("aria-expanded", "false");
      });
    }
  });

  // Close on Escape
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll(".site-nav li.open").forEach(function (li) {
        li.classList.remove("open");
      });
      if (nav && nav.classList.contains("open")) {
        nav.classList.remove("open");
        if (toggle) toggle.setAttribute("aria-expanded", "false");
      }
    }
  });
})();
