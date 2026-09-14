#!/usr/bin/env node
/**
 * Audit du site — CCF Conseil
 *
 * Zéro dépendance. À lancer avant chaque mise en ligne :
 *
 *   npm run audit
 *
 * Vérifie, page par page :
 *   · référencement  — titre, description, h1 unique, canonique, données structurées
 *   · liens          — aucun lien interne mort, aucune ressource manquante
 *   · sécurité       — politique de sécurité du contenu, referrer, fichiers attendus
 *   · contenu        — valeurs « À REMPLACER » encore présentes
 *
 * Sort en code 1 si une erreur bloquante est trouvée : utilisable en intégration continue.
 */

'use strict';

const fs = require('fs');
const path = require('path');

const RACINE = path.resolve(__dirname, '..');
const IGNORER = new Set(['.git', 'node_modules', '__pycache__', 'tools', '.well-known', 'admin']);

const C = {
  gras: (s) => `\x1b[1m${s}\x1b[0m`,
  vert: (s) => `\x1b[32m${s}\x1b[0m`,
  rouge: (s) => `\x1b[31m${s}\x1b[0m`,
  jaune: (s) => `\x1b[33m${s}\x1b[0m`,
  gris: (s) => `\x1b[90m${s}\x1b[0m`,
};

let erreurs = 0;
let avertissements = 0;

function erreur(page, message) { erreurs++; console.log(`  ${C.rouge('✗')} ${C.gras(page)} — ${message}`); }
function alerte(page, message) { avertissements++; console.log(`  ${C.jaune('!')} ${C.gras(page)} — ${message}`); }

/* ------------------------------------------------------------------------- */
function listerPages(dossier = RACINE, pages = []) {
  for (const entree of fs.readdirSync(dossier, { withFileTypes: true })) {
    if (IGNORER.has(entree.name)) { continue; }
    const complet = path.join(dossier, entree.name);
    if (entree.isDirectory()) { listerPages(complet, pages); }
    else if (entree.name.endsWith('.html')) { pages.push(path.relative(RACINE, complet)); }
  }
  return pages;
}

function decoder(s) {
  return s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
          .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ');
}

/* ------------------------------------------------------------------------- */
function auditReferencement(page, html) {
  const titre = html.match(/<title>(.*?)<\/title>/s);
  const desc = html.match(/<meta name="description" content="(.*?)">/s);
  const h1 = html.match(/<h1[\s>]/g) || [];

  if (!titre) { return erreur(page, 'aucune balise title'); }
  const lt = decoder(titre[1]).length;
  if (lt < 28) { alerte(page, `titre court (${lt} caractères, viser 28 à 65)`); }
  else if (lt > 65) { alerte(page, `titre long (${lt} caractères, tronqué par Google au-delà de 65)`); }

  if (!desc) { erreur(page, 'aucune meta description'); }
  else {
    const ld = decoder(desc[1]).length;
    if (ld < 70) { alerte(page, `description courte (${ld} caractères, viser 110 à 165)`); }
    else if (ld > 165) { alerte(page, `description longue (${ld} caractères, tronquée au-delà de 165)`); }
  }

  if (h1.length === 0) { erreur(page, 'aucun h1'); }
  else if (h1.length > 1) { erreur(page, `${h1.length} balises h1 — il en faut exactement une`); }

  if (!/<link rel="canonical"/.test(html)) { erreur(page, 'aucune URL canonique'); }
  if (!/property="og:image"/.test(html)) { alerte(page, 'aucune image de partage'); }
  if (!/<html lang="fr">/.test(html)) { erreur(page, 'attribut lang manquant sur <html>'); }

  // Hiérarchie de titres continue : pas de saut de niveau.
  const niveaux = [...html.matchAll(/<h([1-4])[\s>]/g)].map((m) => Number(m[1]));
  for (let i = 1; i < niveaux.length; i++) {
    if (niveaux[i] - niveaux[i - 1] > 1) {
      alerte(page, `saut de titre h${niveaux[i - 1]} → h${niveaux[i]}`);
      break;
    }
  }

  // Données structurées : lisibles par une machine, donc vérifiables.
  for (const bloc of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try { JSON.parse(bloc[1].trim()); }
    catch (e) { erreur(page, `données structurées invalides : ${e.message}`); }
  }
}

function auditLiens(page, html) {
  const base = path.dirname(path.join(RACINE, page));
  const cibles = [...html.matchAll(/(?:href|src)="([^"#][^"]*)"/g)].map((m) => m[1]);

  for (const cible of cibles) {
    if (/^(https?:|mailto:|tel:|data:|#)/.test(cible)) { continue; }
    const propre = cible.split('?')[0].split('#')[0];
    if (!propre) { continue; }
    const absolu = propre.startsWith('/')
      ? path.join(RACINE, propre)
      : path.resolve(base, propre);
    if (!fs.existsSync(absolu)) { erreur(page, `lien mort : ${cible}`); }
  }
}

function auditSecurite(page, html) {
  if (!/Content-Security-Policy/.test(html)) { erreur(page, 'aucune politique de sécurité du contenu'); }
  if (!/name="referrer"/.test(html)) { alerte(page, 'aucune politique de référent'); }
  for (const lien of html.matchAll(/<a[^>]+target="_blank"[^>]*>/g)) {
    if (!/rel="[^"]*noopener/.test(lien[0])) { erreur(page, 'lien target="_blank" sans rel="noopener"'); }
  }
  if (/localStorage|sessionStorage/.test(html)) { alerte(page, 'stockage navigateur détecté'); }
}

function auditContenu(page, html) {
  const restes = [
    ['À REMPLACER', 'valeur de démonstration'],
    ['à compléter', 'information manquante'],
    ['00000', 'code postal de démonstration'],
    ['ccf-conseil.fr', 'domaine de démonstration'],
  ];
  for (const [motif, libelle] of restes) {
    if (html.includes(motif)) { alerte(page, `${libelle} : « ${motif} »`); break; }
  }
}

/* ------------------------------------------------------------------------- */
function auditFichiers() {
  console.log(C.gras('\n  Fichiers attendus\n'));
  const attendus = [
    ['sitemap.xml', true], ['robots.txt', true], ['404.html', true],
    ['.nojekyll', true], ['.well-known/security.txt', true],
    ['assets/img/og.png', true], ['assets/css/fonts.css', true],
    ['_headers', false], ['.htaccess', false],
  ];
  for (const [f, bloquant] of attendus) {
    const existe = fs.existsSync(path.join(RACINE, f));
    if (existe) { console.log(`  ${C.vert('✓')} ${f}`); }
    else if (bloquant) { erreur(f, 'fichier manquant'); }
    else { alerte(f, 'fichier absent (optionnel selon l\'hébergeur)'); }
  }

  // Le sitemap doit couvrir toutes les pages indexables.
  const sitemap = path.join(RACINE, 'sitemap.xml');
  if (fs.existsSync(sitemap)) {
    const xml = fs.readFileSync(sitemap, 'utf8');
    for (const page of listerPages()) {
      if (page === '404.html') { continue; }
      const attendu = page === 'index.html' ? '/' : '/' + page.replace(/\\/g, '/');
      if (!xml.includes(attendu)) { alerte('sitemap.xml', `${page} absent du sitemap`); }
    }
  }
}

/* ------------------------------------------------------------------------- */
function main() {
  const pages = listerPages().sort();
  console.log(C.gras(`\n  Audit de ${pages.length} pages\n`));

  for (const page of pages) {
    const html = fs.readFileSync(path.join(RACINE, page), 'utf8');
    const avant = erreurs + avertissements;
    auditReferencement(page, html);
    auditLiens(page, html);
    auditSecurite(page, html);
    auditContenu(page, html);
    if (erreurs + avertissements === avant) { console.log(`  ${C.vert('✓')} ${page}`); }
  }

  auditFichiers();

  console.log('');
  console.log('  ─────────────────────────────────────────────');
  if (erreurs === 0 && avertissements === 0) {
    console.log(`  ${C.vert('Aucun problème détecté.')}`);
  } else {
    console.log(`  ${erreurs ? C.rouge(erreurs + ' erreur(s)') : '0 erreur'}` +
                `   ${avertissements ? C.jaune(avertissements + ' avertissement(s)') : '0 avertissement'}`);
    if (erreurs === 0) {
      console.log(C.gris('  Les avertissements ne bloquent pas la mise en ligne, mais méritent un regard.'));
    }
  }
  console.log('');
  process.exit(erreurs > 0 ? 1 : 0);
}

main();
