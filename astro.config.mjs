import { defineConfig } from 'astro/config';

// Site statique pour GitHub Pages.
// - `site`   : l'URL publique (adapte le pseudo/repo si besoin).
// - `base`   : le sous-dossier du repo Pages (doit valoir "/<nom-du-repo>/").
// Si tu déploies le repo sous le nom "avenir-web", laisse tel quel.
export default defineConfig({
  site: 'https://borrak1503.github.io',
  base: '/avenir-web',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
