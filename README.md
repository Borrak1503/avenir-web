# Avenir — version Astro

Plateforme pédagogique trilingue (FR / EN / NL) — Asset Management & Financial Risk Management.
Site statique construit avec [Astro](https://astro.build). Contenu par langue via le routage (`/fr/`, `/en/`, `/nl/`), composants réutilisables, page « Solutions » générée automatiquement à partir des exercices.

## Structure
```
src/
├── i18n.ts                     # langues + libellés d'interface + helper de base path
├── layouts/Base.astro          # en-tête, nav, sélecteur de langue, thème clair/sombre, JS partagé (quiz, sommaire)
├── styles/global.css           # design system (identique à la version HTML d'origine)
├── data/
│   ├── home.json               # contenu de l'accueil (fr/en/nl)
│   └── modules/
│       ├── var.json            # module Value at Risk (corps trilingue + script du calculateur)
│       ├── am1.json            # module Fondamentaux (corps + calculateur + exercices structurés)
│       └── _index.json         # index des modules
└── pages/
    ├── index.astro                     # redirige vers /fr/
    ├── [locale]/index.astro            # accueil
    ├── [locale]/modules/[slug].astro   # une page par module et par langue
    └── [locale]/solutions/index.astro  # page Solutions (auto-générée depuis les exercices)
```

## Développer en local (optionnel)
```bash
npm install
npm run dev      # http://localhost:4321/avenir-web/
npm run build    # génère le site statique dans dist/
```

## Mise en ligne — GitHub Pages (déploiement automatique)
Le fichier `.github/workflows/deploy.yml` compile et publie le site à chaque `git push` sur `main`.

1. Créer un dépôt **public** nommé `avenir-web` (le nom doit correspondre au `base` de `astro.config.mjs` ; si tu choisis un autre nom, change `base: '/<nom-du-repo>'`).
2. Y pousser ce projet (voir « Premier envoi » ci-dessous).
3. Dépôt → **Settings → Pages → Build and deployment → Source : GitHub Actions**.
4. Le workflow se lance ; après ~1–2 min le site est en ligne sur `https://<pseudo>.github.io/avenir-web/`.

Ensuite : chaque modification suivie d'un `git commit` + `git push` redéploie automatiquement. Plus besoin de zip ni de build manuel.

### Premier envoi (en local, une seule fois)
```bash
git init
git add .
git commit -m "Avenir — site Astro"
git branch -M main
git remote add origin https://github.com/<pseudo>/avenir-web.git
git push -u origin main
```

## Ajouter un module
1. Créer `src/data/modules/<slug>.json` sur le modèle de `am1.json` (corps `fr/en/nl`, éventuel `calc`, `exercises`).
2. Ajouter le `slug` dans le tableau `slugs` de `src/pages/[locale]/modules/[slug].astro` et dans la liste importée de la page Solutions.
3. Lier le module depuis la carte correspondante de l'accueil (`src/data/home.json`).

La page « Solutions » se met à jour toute seule à partir des `exercises` déclarés.
