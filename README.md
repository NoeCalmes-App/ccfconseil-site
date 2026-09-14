# CCF Conseil — site vitrine

Site statique (HTML + CSS + JavaScript natif), sans framework ni dépendance à installer.
Hébergeable gratuitement sur GitHub Pages.

---

## Démarrer

Ouvrir `index.html` dans un navigateur suffit. Pour un rendu identique à la production
(chemins absolus, polices), servir le dossier :

```bash
python3 -m http.server 8000
# puis http://localhost:8000
```

## Régénérer les pages

Les pages sont produites par `build.py` afin de ne pas dupliquer l'en-tête, le pied de
page et les métadonnées dans 19 fichiers. **Le site livré reste du HTML pur** : le script
n'est nécessaire que pour modifier une structure commune.

```bash
python3 build.py
```

Pour un changement ponctuel (un mot, un numéro), éditer directement le fichier HTML
concerné est parfaitement valable.

---

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
| `telephone`, `telephone_lien` | En-tête, pied de page, barre mobile, données structurées |
| `email` | Formulaires, mentions légales, confidentialité |
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

## Formulaires

Les formulaires sont fonctionnels côté navigateur (validation, piège à robots, blocage des
soumissions trop rapides) mais **leur attribut `action` est vide** : un site statique ne peut
pas envoyer d'email par lui-même.

Deux options au choix au moment de la mise en ligne :

- **Service d'envoi de formulaire** : renseigner l'URL fournie dans `action` des formulaires
  `data-form`. Aucune autre modification n'est nécessaire.
- **Widget de réservation externe** : remplacer le bloc `.lead-card` de `rendez-vous.html`
  par le code d'intégration du service retenu. Le bloc de commentaire en fin de page indique
  l'emplacement exact.

La pré-sélection du motif fonctionne déjà : un lien vers `rendez-vous.html?motif=controle-fiscal`
sélectionne automatiquement la bonne option. Les valeurs disponibles correspondent aux noms
de fichiers des pages d'expertise.

---

## Référencement

Déjà en place :

- une page par intention de recherche, avec titre et description propres ;
- URL canoniques, `sitemap.xml`, `robots.txt`, page 404 ;
- données structurées `ProfessionalService` sur l'accueil et `FAQPage` sur les pages à questions ;
- HTML sémantique, fil d'Ariane, hiérarchie de titres cohérente ;
- aucune dépendance JavaScript lourde, images vectorielles, chargement quasi instantané.

Reste à faire après la mise en ligne :

1. créer et vérifier la fiche **Google Business Profile** (premier levier en local) ;
2. déclarer le site sur **Google Search Console** et soumettre le `sitemap.xml` ;
3. compléter la ville dans `SITE` et l'intégrer aux titres des pages d'expertise ;
4. publier progressivement les fiches pratiques listées dans `ressources/index.html`.

---

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
