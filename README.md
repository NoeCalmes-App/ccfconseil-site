# CCF Conseil — site vitrine

Site statique (HTML + CSS + JavaScript natif), sans framework ni dépendance à installer.
Hébergeable gratuitement sur GitHub Pages.

---

## Démarrer

```bash
npm run dev
```

C'est tout. Aucun `npm install` : le serveur de développement n'utilise que les modules
fournis avec Node, il n'y a donc **aucune dépendance à installer, à mettre à jour ou à
auditer**. Un dossier `node_modules` absent, c'est aussi zéro faille héritée d'un paquet
tiers.

Il ouvre `http://localhost:5173` et affiche aussi une adresse réseau, pour tester sur un
téléphone connecté au même wifi. À chaque sauvegarde d'un fichier source, les pages se
régénèrent et le navigateur se rafraîchit tout seul. Les en-têtes de sécurité de la
production sont appliqués en local, et une URL inconnue renvoie la vraie page 404 avec le
bon code HTTP : ce que vous voyez est ce que verra le visiteur.

Port occupé : `PORT=5174 npm run dev`.

| Commande | Effet |
|---|---|
| `npm run dev` | Serveur local, régénération et rafraîchissement automatiques |
| `npm run build` | Régénère les 19 pages |
| `npm run audit` | Contrôle référencement, liens, sécurité et contenu |
| `npm run check` | Régénère puis audite — à lancer avant chaque mise en ligne |
| `npm run serve` | Serveur statique simple, sans outillage |

### L'audit

`npm run audit` parcourt les 19 pages et vérifie, sans rien installer :

- **Référencement** — longueur des titres et des descriptions, unicité du `h1`, continuité
  de la hiérarchie de titres, présence de l'URL canonique, de l'image de partage et de
  l'attribut de langue, et **validité JSON de chaque bloc de données structurées**.
- **Liens** — chaque lien interne et chaque ressource pointent vers un fichier qui existe.
- **Sécurité** — politique de sécurité du contenu présente, politique de référent, aucun
  `target="_blank"` sans `rel="noopener"`, aucun stockage navigateur.
- **Contenu** — signale les valeurs de démonstration encore en place (`À REMPLACER`,
  `à compléter`, le domaine d'exemple). C'est le garde-fou contre une mise en ligne avec
  le faux code postal.

Le script sort en code 1 s'il trouve une erreur bloquante : utilisable tel quel dans une
action GitHub.

## Régénérer les pages

Les pages sont produites par `build.py` afin de ne pas dupliquer l'en-tête, le pied de
page et les métadonnées dans 19 fichiers. **Le site livré reste du HTML pur** : ni Node ni
Python ne tournent en production, l'hébergeur ne sert que des fichiers.

Pour un changement ponctuel (un mot, une coordonnée), éditer directement le fichier HTML
concerné est parfaitement valable — mais il sera écrasé au prochain `npm run build`.

## Polices

Fraunces et Archivo sont **auto-hébergées** dans `assets/fonts` (licence SIL Open Font),
sous-ensembles latin et latin-ext uniquement. Trois raisons, et chacune se suffirait :

- **aucune requête vers un tiers au chargement** — le site n'appelle strictement rien
  d'extérieur tant que le visiteur ne clique pas sur le calendrier, ce qui simplifie
  radicalement la conformité RGPD ;
- **affichage plus rapide** — la police part du même serveur que la page, sans résolution
  DNS ni poignée de main TLS supplémentaires ;
- **politique de sécurité du contenu plus stricte** — `font-src 'self'`, aucun domaine
  externe autorisé.

---

## Navigation

Le menu reprend les cinq entrées de la maquette : **Cabinet, Expertises, Méthode, Procédures,
Contact**. « Ressources » n'y figure pas tant que les fiches ne sont pas rédigées : une entrée
de menu qui mène à une page vide dessert autant le référencement que la crédibilité. La page
reste accessible depuis le pied de page, le plan du site et le `sitemap.xml`. Pour la remettre
au menu une fois les articles publiés, ajouter une ligne à `NAV_ITEMS` dans `build.py`.

## Structure

```
.
├── index.html                    Accueil
├── cabinet.html                  Le cabinet
├── methode.html                  La méthode en 4 étapes
├── procedure-fiscale.html        Frise des délais (page SEO principale)
├── contact.html                  Contact
├── rendez-vous.html              Prise de rendez-vous
├── mentions-legales.html
├── confidentialite.html
├── plan-du-site.html
├── 404.html
├── expertises/
│   ├── index.html                Sommaire des expertises
│   ├── conseil-fiscal.html
│   ├── controle-fiscal.html
│   ├── controle-urssaf.html
│   ├── entreprises-en-difficulte.html
│   ├── creation-entreprise.html
│   ├── social-paie-dsn.html
│   └── procedures-et-recours.html
├── ressources/
│   └── index.html
├── assets/
│   ├── css/style.css             Feuille de style unique et commentée
│   ├── js/main.js                Menu, apparitions, formulaires
│   └── img/favicon.svg
├── build.py                      Générateur
├── sitemap.xml
├── robots.txt
└── .nojekyll                     Indispensable sur GitHub Pages
```

---

## À compléter avant la mise en ligne

Tout est regroupé dans le dictionnaire `SITE` en haut de `build.py`. Les valeurs marquées
`À REMPLACER` doivent être renseignées, puis le site régénéré.

| Champ | Utilisé pour |
|---|---|
| `email` | En-tête, pied de page, barre mobile, formulaires, mentions légales |
| `calendly` | Page de rendez-vous |
| `telephone`, `telephone_lien` | **Laissés vides** : tant qu'ils le sont, l'email prend leur place partout. Dès qu'ils sont renseignés, le téléphone réapparaît seul dans l'en-tête, le pied de page, la barre mobile et les données structurées. |
| `adresse`, `code_postal`, `ville` | Pied de page, contact, **référencement local** |
| `siren`, `forme` | Mentions légales |
| `domaine` | URL canoniques, `sitemap.xml`, `robots.txt` |

La ville est la donnée la plus importante pour le référencement : elle conditionne le
positionnement sur les recherches locales et la cohérence avec la fiche Google Business
Profile.

Restent également à ajouter avant publication : le logo vectoriel définitif, une
photographie du dirigeant, le directeur de la publication, le capital social et
l'assurance de responsabilité civile professionnelle.

---

## Mise en ligne sur GitHub Pages

1. Créer un dépôt et pousser le contenu de ce dossier.
2. `Settings` → `Pages` → *Source* : `Deploy from a branch`, branche `main`, dossier `/ (root)`.
3. Renseigner le domaine personnalisé dans *Custom domain*, puis cocher *Enforce HTTPS*.
4. Chez le registrar, créer les enregistrements DNS :

```
A     @   185.199.108.153
A     @   185.199.109.153
A     @   185.199.110.153
A     @   185.199.111.153
AAAA  @   2606:50c0:8000::153
AAAA  @   2606:50c0:8001::153
AAAA  @   2606:50c0:8002::153
AAAA  @   2606:50c0:8003::153
CNAME www <utilisateur>.github.io.
```

Le fichier `.nojekyll` empêche GitHub de traiter le dossier avec Jekyll. Ne pas le supprimer.

---

## Prise de rendez-vous

La réservation passe par un agenda en ligne externe, configuré sur son offre gratuite (un seul
type d'événement, ce qui suffit : le motif est demandé dans le formulaire de réservation).

**Configuration** — renseigner `calendly` dans `SITE` (`build.py`) avec l'URL de l'événement,
puis régénérer. Côté agenda, créer un événement « Premier échange — 15 minutes » et y ajouter
trois questions personnalisées, dans cet ordre :

1. **Motif de votre demande** (liste déroulante : les sept expertises + « Autre »)
2. **Votre situation en quelques lignes** (texte libre)
3. **Échéance éventuelle** (texte court)

L'ordre compte : le site pré-remplit la **première** question via le paramètre `a1`.

**Pré-sélection du motif** — chaque page d'expertise renvoie vers
`rendez-vous.html?motif=controle-fiscal`. Le script convertit ce paramètre en libellé lisible et
le transmet à l'agenda. Les valeurs possibles sont les noms de fichiers des pages d'expertise.

**Chargement différé** — le script de l'agenda n'est appelé qu'après un clic sur « Afficher le
calendrier ». Conséquences : aucune requête tierce au chargement de la page, aucun cookie déposé
sans action du visiteur, donc **aucune bannière de consentement nécessaire**, et une page de
rendez-vous qui reste aussi rapide que les autres. Si le script échoue, un message de repli
affiche le téléphone et l'adresse email.

## Formulaire de contact

Le formulaire de `contact.html` est fonctionnel côté navigateur (validation, piège à robots,
blocage des soumissions trop rapides) mais **un site statique ne peut pas envoyer d'email par
lui-même**.

Renseigner `form_endpoint` dans `SITE` avec l'URL d'un service d'acheminement de formulaire.
Tant que le champ est vide, un avertissement visible s'affiche au-dessus du formulaire : il
disparaît dès que l'URL est renseignée. Penser à ajouter le domaine du service à la directive
`form-action` de la politique de sécurité du contenu, dans `layout()`.

---

## Référencement

Déjà en place :

- **Une page par intention de recherche.** Le titre place le mot-clé en premier et la marque en
  dernier, la description tient entre 110 et 165 caractères — la fourchette réellement affichée
  par Google.
- **La ville s'insère automatiquement** dans tous les titres dès que `ville` est renseigné dans
  `SITE` (« Contrôle fiscal : se faire accompagner à Rodez | CCF Conseil »). C'est le levier
  numéro un du référencement local, et il ne demande qu'une seule saisie.
- **Données structurées** : `ProfessionalService` et `WebSite` sur l'accueil, `Service` sur chaque
  page d'expertise, `FAQPage` partout où il y a des questions, `BreadcrumbList` sur toutes les
  pages intérieures. Ce sont elles qui produisent les résultats enrichis et le fil d'Ariane
  affiché sous le lien dans Google.
- **Image de partage** `assets/img/og.png` (1200 × 630) avec les balises Open Graph et Twitter :
  un lien collé dans un email, LinkedIn ou WhatsApp affiche une vignette propre.
- URL canoniques, `sitemap.xml` avec priorités, `robots.txt`, page 404 en `noindex`.
- HTML sémantique, fil d'Ariane visible, un seul `h1` par page, hiérarchie de titres continue.
- Aucune dépendance JavaScript lourde, images vectorielles, chargement quasi instantané :
  les Core Web Vitals sont un critère de classement direct.

Un audit rapide avant chaque mise en ligne (longueur des titres, des descriptions, unicité du
`h1`, présence des données structurées) :

```bash
python3 - <<'EOF'
import os, re, html
for dp, dn, fn in os.walk('.'):
    dn[:] = [d for d in dn if d not in ('.git', '__pycache__', '.well-known')]
    for f in sorted(fn):
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f).replace('./', '')
        s = open(p, encoding='utf-8').read()
        ti = re.search(r'<title>(.*?)</title>', s, re.S)
        de = re.search(r'<meta name="description" content="(.*?)">', s, re.S)
        tl = len(html.unescape(ti.group(1))) if ti else 0
        dl = len(html.unescape(de.group(1))) if de else 0
        h1 = len(re.findall(r'<h1[ >]', s))
        ok = 28 <= tl <= 65 and 70 <= dl <= 165 and h1 == 1
        print(f"{p:42} titre {tl:>3}  desc {dl:>3}  h1 {h1}  {'' if ok else '<-- a revoir'}")
EOF
```

Reste à faire après la mise en ligne :

1. créer et vérifier la fiche **Google Business Profile** (premier levier en local) ;
2. déclarer le site sur **Google Search Console** et soumettre le `sitemap.xml` ;
3. compléter la ville dans `SITE` et l'intégrer aux titres des pages d'expertise ;
4. publier progressivement les fiches pratiques listées dans `ressources/index.html`.

---

## Sécurité

Déjà en place :

- **Politique de sécurité du contenu** (CSP) restrictive déclarée sur chaque page : seuls les
  polices Google, le script de l'agenda et les ressources du site peuvent se charger. Tout
  script injecté par un tiers est bloqué par le navigateur.
- `Referrer-Policy: strict-origin-when-cross-origin` — les URL internes ne fuitent pas vers
  les sites externes.
- **Aucun stockage navigateur**, aucun cookie propre, aucun traceur.
- Liens externes en `rel="noopener"`.
- Formulaire protégé par un champ piège et un contrôle de vitesse de soumission.
- `/.well-known/security.txt` — point de contact pour signaler une faille (RFC 9116).
- Page `404.html` en `noindex`, sans message technique ni information sur la structure du site.

À faire côté hébergement, car une page statique ne peut pas les déclarer elle-même :

| En-tête | Valeur recommandée |
|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=()` |

GitHub Pages ne permet pas de définir ces en-têtes. Ils se configurent en plaçant le site
derrière Cloudflare (offre gratuite), ce qui apporte aussi le HSTS et un certificat géré.
Sans cela, le site reste sûr — il n'y a ni base de données, ni code serveur, ni session à
compromettre — mais ces en-têtes ferment les derniers angles morts.

## Accessibilité et compatibilité

- Navigation au clavier complète, focus visible, lien d'évitement.
- `prefers-reduced-motion` respecté : toutes les animations sont désactivées.
- Contrastes conformes AA sur l'ensemble des fonds.
- Testé de 320 px à 1920 px, sans débordement horizontal.
- Aucun `localStorage`, aucun cookie : pas de bandeau de consentement nécessaire.

---

## Notes de conception

- Une seule feuille de style, organisée en 21 sections numérotées et commentées.
- Les couleurs, espacements et typographies passent par des variables CSS (`:root`).
- Les icônes sont des SVG en ligne : pas de requête réseau, couleur héritée du texte.
- Les expertises sont décrites une seule fois, dans la liste `EXPERTISES` de `build.py`.
  Ajouter un pôle revient à ajouter une entrée : la page, la navigation, le pied de page,
  le sommaire et le `sitemap.xml` se mettent à jour seuls.
