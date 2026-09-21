#!/usr/bin/env node
/**
 * Serveur de développement — CCF Conseil
 *
 * Zéro dépendance : uniquement les modules fournis avec Node.
 * Rien à installer, rien à mettre à jour, rien qui casse dans six mois.
 *
 *   npm run dev
 *
 * Il fait trois choses :
 *   1. sert le site en local, avec les en-têtes de sécurité de la production,
 *      pour voir exactement ce que verra le visiteur ;
 *   2. régénère les pages dès qu'un fichier source change ;
 *   3. rafraîchit le navigateur tout seul, sans extension.
 */

'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn } = require('child_process');

const RACINE = path.resolve(__dirname, '..');
const PORT = Number(process.env.PORT) || 5173;

/* -------------------------------------------------------------------------
   Types de contenu
   ------------------------------------------------------------------------- */
const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
};

/* Les mêmes en-têtes qu'en production : autant les voir dès le développement. */
const SECURITE = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'geolocation=(), microphone=(), camera=(), payment=(self "https://calendly.com"), usb=()',
  'Cross-Origin-Opener-Policy': 'same-origin',
};

/* -------------------------------------------------------------------------
   Rafraîchissement automatique
   ------------------------------------------------------------------------- */
const clients = new Set();

const SCRIPT_RELOAD = `// Rafraîchissement automatique — présent uniquement en développement.
(function () {
  var source = new EventSource('/__dev/flux');
  source.addEventListener('recharger', function () { window.location.reload(); });
  source.addEventListener('error', function () {
    // Le serveur redémarre : on retente sans saturer la console.
    setTimeout(function () { window.location.reload(); }, 1200);
  });
})();
`;

function prevenirNavigateurs() {
  for (const client of clients) {
    try { client.write('event: recharger\ndata: 1\n\n'); } catch (_) { clients.delete(client); }
  }
}

/* -------------------------------------------------------------------------
   Reconstruction
   ------------------------------------------------------------------------- */
let enCours = false;
let redemander = false;

function reconstruire(raison) {
  if (enCours) { redemander = true; return; }
  enCours = true;
  const debut = Date.now();
  process.stdout.write(`\n  ↻ ${raison} — reconstruction…`);

  const py = spawn(process.platform === 'win32' ? 'python' : 'python3', ['build.py'], {
    cwd: RACINE,
  });
  let erreur = '';
  py.stderr.on('data', (d) => { erreur += d.toString(); });

  py.on('close', (code) => {
    enCours = false;
    if (code === 0) {
      console.log(` terminé en ${Date.now() - debut} ms`);
      prevenirNavigateurs();
    } else {
      console.log('\n\n  ✗ La génération a échoué :\n');
      console.log(erreur.split('\n').map((l) => '    ' + l).join('\n'));
    }
    if (redemander) { redemander = false; reconstruire('nouvelle modification'); }
  });

  py.on('error', () => {
    enCours = false;
    console.log('\n  ✗ python3 est introuvable. Installez-le, ou éditez les fichiers HTML directement.');
  });
}

/* Surveillance des sources, avec anti-rebond : un éditeur écrit plusieurs fois par sauvegarde. */
const SOURCES = ['build.py', 'content.py', 'assets/css', 'assets/js'];
let minuteur = null;

for (const cible of SOURCES) {
  const complet = path.join(RACINE, cible);
  if (!fs.existsSync(complet)) { continue; }
  fs.watch(complet, { recursive: fs.statSync(complet).isDirectory() }, (_, fichier) => {
    if (fichier && /\.(pyc|swp|tmp)$/.test(fichier)) { return; }
    clearTimeout(minuteur);
    minuteur = setTimeout(() => {
      if (cible.endsWith('.py')) { reconstruire(`${cible} modifié`); }
      else { console.log(`\n  ↻ ${fichier} modifié`); prevenirNavigateurs(); }
    }, 120);
  });
}

/* -------------------------------------------------------------------------
   Serveur
   ------------------------------------------------------------------------- */
function servir(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  let chemin = decodeURIComponent(url.pathname);

  if (chemin === '/__dev/flux') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    });
    res.write(': connecté\n\n');
    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }

  if (chemin === '/__dev/reload.js') {
    res.writeHead(200, { 'Content-Type': TYPES['.js'], 'Cache-Control': 'no-store' });
    return res.end(SCRIPT_RELOAD);
  }

  if (chemin.endsWith('/')) { chemin += 'index.html'; }

  // Aucun échappement hors du dossier du site.
  const fichier = path.join(RACINE, chemin);
  if (!fichier.startsWith(RACINE)) {
    res.writeHead(403, SECURITE);
    return res.end('403');
  }

  fs.readFile(fichier, (err, donnees) => {
    const ext = path.extname(fichier).toLowerCase();

    if (err) {
      // Même comportement qu'en production : la page 404 du site, avec le bon statut.
      const page404 = path.join(RACINE, '404.html');
      if (fs.existsSync(page404)) {
        const html = injecter(fs.readFileSync(page404, 'utf8'));
        res.writeHead(404, { ...SECURITE, 'Content-Type': TYPES['.html'] });
        return res.end(html);
      }
      res.writeHead(404, SECURITE);
      return res.end('404');
    }

    const entetes = {
      ...SECURITE,
      'Content-Type': TYPES[ext] || 'application/octet-stream',
      'Cache-Control': 'no-store',
    };

    if (ext === '.html') {
      return res.writeHead(200, entetes).end(injecter(donnees.toString('utf8')));
    }
    res.writeHead(200, entetes).end(donnees);
  });
}

/** Ajoute le script de rafraîchissement, en respectant la politique de sécurité de la page. */
function injecter(html) {
  return html.replace('</body>', '<script src="/__dev/reload.js"></script>\n</body>');
}

/* -------------------------------------------------------------------------
   Démarrage
   ------------------------------------------------------------------------- */
function adresseReseau() {
  for (const cartes of Object.values(os.networkInterfaces())) {
    for (const carte of cartes || []) {
      if (carte.family === 'IPv4' && !carte.internal) { return carte.address; }
    }
  }
  return null;
}

const serveur = http.createServer(servir);

serveur.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.log(`\n  ✗ Le port ${PORT} est déjà utilisé.`);
    console.log(`    Essayez :  PORT=${PORT + 1} npm run dev\n`);
    process.exit(1);
  }
  throw err;
});

serveur.listen(PORT, () => {
  const lan = adresseReseau();
  console.log('');
  console.log('  CCF Conseil — serveur de développement');
  console.log('  ─────────────────────────────────────────────');
  console.log(`  Local      http://localhost:${PORT}`);
  if (lan) { console.log(`  Réseau     http://${lan}:${PORT}   (pour tester sur téléphone)`); }
  console.log('');
  console.log('  Les pages se régénèrent et le navigateur se rafraîchit à chaque modification.');
  console.log('  Ctrl+C pour arrêter.');
  reconstruire('démarrage');
});
