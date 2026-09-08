export const locales = ['fr', 'en', 'nl'] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = 'fr';

type Dict = {
  tag: string;
  tracks: string;
  curriculum: string;
  home: string;
  solutions: string;
  langName: string;
  footer: string;
  solutionsTitle: string;
  solutionsIntro: string;
  statement: string;
  answer: string;
  backToModule: string;
};

export const ui: Record<Locale, Dict> = {
  fr: {
    tag: 'Asset Management & Risk',
    tracks: 'Parcours',
    curriculum: 'Programme',
    home: 'Accueil',
    solutions: 'Solutions',
    langName: 'Français',
    footer: 'Plateforme pédagogique · Asset Management & Financial Risk Management · Contenu multilingue FR / EN / NL',
    solutionsTitle: 'Solutions des exercices',
    solutionsIntro: 'Réponses courtes de tous les exercices chiffrés, regroupées par module. Cliquez sur un identifiant pour ouvrir le module correspondant.',
    statement: 'Énoncé',
    answer: 'Réponse',
    backToModule: 'Ouvrir le module',
  },
  en: {
    tag: 'Asset Management & Risk',
    tracks: 'Tracks',
    curriculum: 'Curriculum',
    home: 'Home',
    solutions: 'Solutions',
    langName: 'English',
    footer: 'Educational platform · Asset Management & Financial Risk Management · Multilingual content FR / EN / NL',
    solutionsTitle: 'Exercise solutions',
    solutionsIntro: 'Short answers to all numerical exercises, grouped by module. Click an identifier to open the matching module.',
    statement: 'Problem',
    answer: 'Answer',
    backToModule: 'Open the module',
  },
  nl: {
    tag: 'Asset Management & Risk',
    tracks: 'Trajecten',
    curriculum: 'Programma',
    home: 'Home',
    solutions: 'Oplossingen',
    langName: 'Nederlands',
    footer: 'Educatief platform · Asset Management & Financial Risk Management · Meertalige inhoud FR / EN / NL',
    solutionsTitle: 'Oplossingen van de oefeningen',
    solutionsIntro: 'Korte antwoorden op alle cijferoefeningen, gegroepeerd per module. Klik op een identificatie om de bijbehorende module te openen.',
    statement: 'Opgave',
    answer: 'Antwoord',
    backToModule: 'Open de module',
  },
};

/** Remplace le jeton @@BASE@@ des fragments par le vrai base path Astro. */
export function withBase(html: string): string {
  return html.replaceAll('@@BASE@@', import.meta.env.BASE_URL);
}
