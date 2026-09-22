#!/usr/bin/env python3
"""Extrait le contenu trilingue des fichiers HTML existants vers des fragments
mono-langue propres, pour le projet Astro. Aucune reprise manuelle du contenu."""
import json, re, os
from bs4 import BeautifulSoup

SRC = "/root/avenir"
OUT = "/root/avenir-web/src/data"
os.makedirs(OUT + "/modules", exist_ok=True)
LOCALES = ["fr", "en", "nl"]

def rewrite_href(href, locale):
    if href is None:
        return href
    h = href.strip()
    if h.startswith("#"):
        return h  # ancre interne, même page
    if h.startswith("http") or h.startswith("mailto:"):
        return h
    # normalise en enlevant les ../
    h = h.replace("../", "")
    # index.html (avec ancre éventuelle) -> accueil localisé
    m = re.match(r"index\.html(#.*)?$", h)
    if m:
        return f"@@BASE@@{locale}/" + (m.group(1) or "")
    # modules/xxx.html OU xxx.html (lien inter-module, avec ancre éventuelle) -> route module localisée
    m = re.match(r"(?:modules/)?([a-z0-9\-]+)\.html(#.*)?$", h)
    if m:
        raw = m.group(1)
        anchor = m.group(2) or ""
        slug = raw
        # ⚠ sous-modules d'abord (préfixes plus longs) pour ne PAS les rabattre sur "am4"
        for pref in ("am4-actions", "am4-obligations", "am4-immobilier", "am4-matieres", "am4-monetaire",
                     "am1", "am2", "am3", "am4", "am5", "am6", "am7", "am8", "frm1", "frm3", "frm4", "frm5", "frm6", "frm7", "frm8", "fmp1", "fmp2", "fmp3", "fmp4", "fmp5", "vrm1", "qa1", "qa2", "qa3", "qa4", "qa5", "var"):
            if raw.startswith(pref):
                slug = pref; break
        return f"@@BASE@@{locale}/modules/{slug}/{anchor}"
    return h

def localize(node_html, locale):
    """Filtre un fragment HTML pour ne garder qu'une langue et réécrit les liens."""
    frag = BeautifulSoup(node_html, "html.parser")
    # supprime les variantes des autres langues
    for el in frag.select("[data-lang]"):
        if getattr(el, "decomposed", False):
            continue
        if el.get("data-lang") != locale:
            el.decompose()
    # nettoie l'attribut sur les éléments restants
    for el in frag.select("[data-lang]"):
        if not getattr(el, "decomposed", False):
            del el["data-lang"]
    # réécrit les liens
    for a in frag.find_all("a"):
        if a.get("href"):
            a["href"] = rewrite_href(a["href"], locale)
    return str(frag)

def get_title(soup, locale):
    """Titre = h1 du module (ou hero de l'accueil) pour la langue."""
    h1 = None
    for cand in soup.select("h1[data-lang], .hero h1[data-lang]"):
        if cand.get("data-lang") == locale:
            h1 = cand; break
    if h1 is None:
        h1 = soup.find("h1")
    return h1.get_text(" ", strip=True) if h1 else "Avenir"

# ---------- ACCUEIL ----------
soup = BeautifulSoup(open(f"{SRC}/index.html", encoding="utf-8").read(), "html.parser")
sections = soup.find_all("section")
home = {"titles": {}, "body": {}}
for loc in LOCALES:
    joined = "\n".join(str(s) for s in sections)
    home["body"][loc] = localize(joined, loc)
    # titre accueil = eyebrow/hero — on met un libellé simple
    home["titles"][loc] = {"fr": "Accueil", "en": "Home", "nl": "Home"}[loc]
json.dump(home, open(f"{OUT}/home.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("home.json OK")

# ---------- MODULES ----------
MODS = [("var", "var.html"), ("am1", "am1-fondamentaux.html"), ("am2", "am2-portefeuille.html"), ("am3", "am3-capm.html"), ("am4", "am4-classes-actifs.html"), ("am5", "am5-construction-allocation.html"), ("am6", "am6-actif-passif.html"), ("am7", "am7-performance-attribution.html"), ("am8", "am8-facteurs.html"), ("frm1", "frm1-panorama.html"), ("frm3", "frm3-volatilite.html"), ("frm4", "frm4-taux-duration.html"), ("frm5", "frm5-greeks.html"), ("frm6", "frm6-credit.html"), ("frm7", "frm7-stress-testing.html"), ("frm8", "frm8-reglementation-capital.html"), ("am4-actions", "am4-actions.html"), ("am4-obligations", "am4-obligations.html"), ("am4-immobilier", "am4-immobilier.html"), ("am4-matieres", "am4-matieres.html"), ("am4-monetaire", "am4-monetaire.html"), ("qa1", "qa1-probabilites.html"), ("qa2", "qa2-echantillons.html"), ("qa3", "qa3-regression.html"), ("qa4", "qa4-series-temporelles.html"), ("qa5", "qa5-simulation-ml.html"), ("fmp1", "fmp1-institutions.html"), ("fmp2", "fmp2-derives.html"), ("fmp3", "fmp3-futures-forwards.html"), ("fmp4", "fmp4-options-strategies.html"), ("fmp5", "fmp5-taux-obligations-swaps.html"), ("vrm1", "vrm1-mesures-risque-var.html")]
index_meta = []
for slug, fname in MODS:
    raw = open(f"{SRC}/modules/{fname}", encoding="utf-8").read()
    soup = BeautifulSoup(raw, "html.parser")
    shell = soup.select_one(".wrap-mod")
    track_am = "track-am" in (soup.body.get("class") or [])
    # script calculateur = dernier <script> sans src
    calc = ""
    for sc in soup.find_all("script"):
        if not sc.get("src") and sc.string:
            calc = sc.string
    mod = {"slug": slug, "trackAm": track_am, "titles": {}, "body": {}, "calc": calc, "exercises": []}
    for loc in LOCALES:
        mod["titles"][loc] = get_title(soup, loc)
        mod["body"][loc] = localize(str(shell), loc)
    # exercices structurés pour la page Solutions
    for exo in soup.select(".exo"):
        eid_el = exo.select_one(".eid")
        eid = eid_el.get_text(strip=True) if eid_el else ""
        entry = {"id": eid, "statement": {}, "answer": {}}
        for loc in LOCALES:
            st = None
            for c in exo.select(".estatement[data-lang]"):
                if c.get("data-lang") == loc: st = c; break
            an = None
            for c in exo.select(".ans[data-lang]"):
                if c.get("data-lang") == loc: an = c; break
            entry["statement"][loc] = localize(str(st), loc) if st else ""
            entry["answer"][loc] = localize(str(an), loc) if an else ""
        mod["exercises"].append(entry)
    json.dump(mod, open(f"{OUT}/modules/{slug}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    index_meta.append({"slug": slug, "titles": mod["titles"], "trackAm": track_am, "nExo": len(mod["exercises"])})
    print(f"{slug}.json OK — exercices: {len(mod['exercises'])}")

json.dump(index_meta, open(f"{OUT}/modules/_index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("index modules OK")
