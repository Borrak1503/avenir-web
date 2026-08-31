/* ==========================================================================
   AVENIR — Scripts partagés
   Sélecteur de langue FR/EN, thème clair/sombre, sommaire actif, quiz
   ========================================================================== */
(function () {
  "use strict";

  var LS_LANG = "avenir-lang";
  var LS_THEME = "avenir-theme";

  function safeGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function safeSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* ---------- Langue ---------- */
  function detectLang() {
    var saved = safeGet(LS_LANG);
    if (saved === "fr" || saved === "en") return saved;
    var nav = (navigator.language || "fr").toLowerCase();
    return nav.indexOf("en") === 0 ? "en" : "fr";
  }

  function setLang(lang) {
    document.body.setAttribute("data-active-lang", lang);
    document.documentElement.setAttribute("lang", lang);
    safeSet(LS_LANG, lang);
    document.querySelectorAll(".lang-toggle button").forEach(function (b) {
      b.classList.toggle("active", b.getAttribute("data-set-lang") === lang);
    });
  }

  /* ---------- Thème ---------- */
  function detectTheme() {
    var saved = safeGet(LS_THEME);
    if (saved === "light" || saved === "dark") return saved;
    return null; // suit le système
  }

  function applyTheme(theme) {
    if (theme) {
      document.documentElement.setAttribute("data-theme", theme);
      safeSet(LS_THEME, theme);
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    updateThemeIcon();
  }

  function currentTheme() {
    var attr = document.documentElement.getAttribute("data-theme");
    if (attr) return attr;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function updateThemeIcon() {
    var btn = document.getElementById("theme-btn");
    if (btn) btn.textContent = currentTheme() === "dark" ? "☀" : "☾";
  }

  /* ---------- Initialisation ---------- */
  document.addEventListener("DOMContentLoaded", function () {
    setLang(detectLang());
    applyTheme(detectTheme());

    document.querySelectorAll(".lang-toggle button").forEach(function (b) {
      b.addEventListener("click", function () { setLang(b.getAttribute("data-set-lang")); });
    });

    var themeBtn = document.getElementById("theme-btn");
    if (themeBtn) themeBtn.addEventListener("click", function () {
      applyTheme(currentTheme() === "dark" ? "light" : "dark");
    });

    var menuBtn = document.getElementById("menu-btn");
    var navLinks = document.querySelector(".nav-links");
    if (menuBtn && navLinks) menuBtn.addEventListener("click", function () {
      var open = navLinks.style.display === "flex";
      navLinks.style.display = open ? "" : "flex";
      navLinks.style.position = "absolute";
      navLinks.style.flexDirection = "column";
      navLinks.style.top = "64px";
      navLinks.style.right = "16px";
      navLinks.style.background = "var(--surface)";
      navLinks.style.border = "1px solid var(--border)";
      navLinks.style.borderRadius = "12px";
      navLinks.style.padding = "8px";
      navLinks.style.boxShadow = "var(--shadow-lg)";
    });

    /* Sommaire actif + barre de progression (pages module) */
    var toc = document.querySelector(".toc");
    var bar = document.querySelector(".progress-bar");
    if (toc || bar) {
      var headings = Array.prototype.slice.call(document.querySelectorAll(".module-body h2[id]"));
      var links = toc ? Array.prototype.slice.call(toc.querySelectorAll("a")) : [];
      var onScroll = function () {
        if (bar) {
          var h = document.documentElement;
          var pct = h.scrollTop / (h.scrollHeight - h.clientHeight);
          bar.style.width = Math.max(0, Math.min(1, pct)) * 100 + "%";
        }
        if (headings.length && links.length) {
          var pos = window.scrollY + 120, current = headings[0].id;
          headings.forEach(function (hd) { if (hd.offsetTop <= pos) current = hd.id; });
          links.forEach(function (a) {
            a.classList.toggle("active", a.getAttribute("href") === "#" + current);
          });
        }
      };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
  });

  /* ---------- Quiz (exposé globalement pour les onclick) ---------- */
  window.avenirAnswer = function (btn, correct) {
    var q = btn.closest(".q");
    if (q.getAttribute("data-done") === "1") return;
    q.setAttribute("data-done", "1");
    var opts = q.querySelectorAll(".opt");
    opts.forEach(function (o) { o.disabled = true; });
    if (correct) {
      btn.classList.add("correct");
    } else {
      btn.classList.add("wrong");
      opts.forEach(function (o) { if (o.getAttribute("data-correct") === "1") o.classList.add("correct"); });
    }
    var ex = q.querySelector(".explain");
    if (ex) ex.classList.add("show");
  };
})();
