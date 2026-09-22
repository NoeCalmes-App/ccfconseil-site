#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCF Conseil — générateur de site statique.

Le site livré est du HTML pur : ce script sert uniquement à régénérer les
pages sans dupliquer l'en-tête, le pied de page et les métadonnées à la main.

    python3 build.py

Le texte éditorial (expertises, procédure) est dans content.py.
Les coordonnées du cabinet sont dans le dictionnaire SITE ci-dessous.
"""

import hashlib
import html
import os
from datetime import date

from content import CABINET, EXPERTISES, PROCEDURE, RESSOURCES

ROOT = os.path.dirname(os.path.abspath(__file__))
ANNEE = date.today().year

# ---------------------------------------------------------------------------
# Coordonnées du cabinet
# Elles vivent dans content/cabinet.json, modifiable depuis /admin.
# ---------------------------------------------------------------------------
SITE = CABINET

# ---------------------------------------------------------------------------
# Icônes — tracés SVG 24×24, couleur héritée du texte
# ---------------------------------------------------------------------------
I = {
"doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/>',
"search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
"users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
"brief": '<rect x="2" y="7" width="20" height="14" rx="1"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/><path d="M2 13h20"/>',
"scale": '<path d="M12 3v18M7 21h10M12 6l-7 2 3 6a3.5 3.5 0 0 0 8 0l-4-8"/><path d="m12 6 7 2-3 6a3.5 3.5 0 0 1-8 0"/>',
"shield": '<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
"clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
"phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
"video": '<rect x="2" y="6" width="14" height="12" rx="1"/><path d="m16 11 6-3v8l-6-3z"/>',
"mail": '<rect x="2" y="4" width="20" height="16" rx="1"/><path d="m2 7 10 6 10-6"/>',
"pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
"calendar": '<rect x="3" y="5" width="18" height="16" rx="1"/><path d="M8 3v4M16 3v4M3 11h18"/>',
"check": '<path d="m4 12.5 5 5 11-11"/>',
"arrow": '<path d="M4 12h15M13 6l6 6-6 6"/>',
"target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>',
"hand": '<path d="m11 14-3-3a2 2 0 0 1 3-3l5 5"/><path d="m3 11 4-4 6 6 3-3 5 5-6 6z"/>',
"menu": '<path d="M3 7h18M3 12h18M3 17h18"/>',
"close": '<path d="M6 6l12 12M18 6 6 18"/>',
"lock": '<rect x="4" y="10" width="16" height="11" rx="1"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
}


def icon(name, cls="", w=1.4):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">{I[name]}</svg>')


# Reprend les entrées de la maquette : Cabinet, Expertises, Méthode, Procédures, Contact.
# « Ressources » reste accessible par le pied de page et le plan du site tant que
# les fiches ne sont pas rédigées : une entrée de menu qui mène à une page vide
# dessert le référencement autant que la crédibilité.
NAV_ITEMS = [
    ("cabinet.html", "Cabinet"),
    ("expertises/index.html", "Expertises"),
    ("methode.html", "Méthode"),
    ("procedure-fiscale.html", "Procédures"),
    ("contact.html", "Contact"),
]


def rel(path, root):
    return root + path


def empreinte(path):
    """Somme courte du contenu d'un fichier, ajoutée à son adresse.

    GitHub Pages sert les fichiers avec un cache de dix minutes. Sans cette
    empreinte, un visiteur déjà venu reçoit le nouveau HTML avec l'ancien CSS
    et l'ancien script : la page s'affiche à moitié refaite. L'empreinte change
    dès que le fichier change, donc le navigateur le retélécharge aussitôt.
    """
    try:
        with open(path, "rb") as fichier:
            return hashlib.sha1(fichier.read()).hexdigest()[:8]
    except OSError:
        return ""


def rel_v(path, root):
    """Comme rel(), mais avec l'empreinte du fichier en paramètre d'adresse."""
    marque = empreinte(path)
    return rel(path, root) + ("?v=" + marque if marque else "")


def a_adresse():
    """Les blocs d'adresse ne s'affichent que si elle est renseignée."""
    return bool(SITE["adresse"].strip())


def a_ville():
    return bool(SITE["ville"].strip())


def adresse_html(separateur="<br>"):
    morceaux = [SITE["adresse"], f'{SITE["code_postal"]} {SITE["ville"]}'.strip()]
    return separateur.join(m for m in morceaux if m.strip())


def a_tel():
    """Le téléphone n'est affiché que s'il est renseigné dans SITE."""
    return bool(SITE["telephone"].strip())


def lien_email(classe="", texte=None):
    """Lien mailto : ouvre la messagerie du visiteur (Gmail, Outlook, Mail…)."""
    c = f' class="{classe}"' if classe else ""
    return f'<a{c} href="mailto:{SITE["email"]}">{icon("mail")} {texte or SITE["email"]}</a>'


def contact_direct(classe="arrow"):
    """Moyen de contact secondaire : téléphone s'il existe, sinon email."""
    if a_tel():
        return (f'<a class="{classe}" href="tel:{SITE["telephone_lien"]}">'
                f'{icon("phone")} {SITE["telephone"]} {icon("arrow")}</a>')
    return (f'<a class="{classe}" href="mailto:{SITE["email"]}">'
            f'{icon("mail")} Nous écrire {icon("arrow")}</a>')


# ---------------------------------------------------------------------------
# Fragments de gabarit
# ---------------------------------------------------------------------------
def brand_mark():
    """Sceau gravé : un écu, une balance stylisée, tracé au filet."""
    return (
        '<svg class="brand__mark" viewBox="0 0 34 40" fill="none" aria-hidden="true">'
        '<path d="M17 1.6 32.2 7v14.4C32.2 30.4 25.4 36.3 17 38.4 8.6 36.3 1.8 30.4 1.8 21.4V7z" '
        'stroke="#C9A961" stroke-width="1.2"/>'
        '<path d="M17 10.4v17.2M11.4 27.6h11.2" stroke="#F3F1EB" stroke-width="1.1" stroke-linecap="round"/>'
        '<path d="M17 13 11.6 14.6l2 4.4a3 3 0 0 0 5.6 0l-2.2-6z" stroke="#F3F1EB" stroke-width="1.1" '
        'stroke-linejoin="round"/>'
        '<path d="m17 13 5.4 1.6-2 4.4a3 3 0 0 1-5.6 0" stroke="#F3F1EB" stroke-width="1.1" '
        'stroke-linejoin="round"/>'
        '</svg>'
    )


def brand(root, tag=True):
    tagline = f'<span class="brand__tag">{SITE["baseline"]}</span>' if tag else ""
    return f"""<a class="brand" href="{rel('index.html', root)}" aria-label="{SITE['nom']}, accueil">
      {brand_mark()}
      <span class="brand__text">
        <span class="brand__name">CCF<em>&nbsp;Conseil</em></span>
        {tagline}
      </span>
    </a>"""


def header(current, root):
    parts = []
    for href, label in NAV_ITEMS:
        aria = ' aria-current="page"' if href == current else ""
        parts.append(f'<a href="{rel(href, root)}"{aria}>{label}</a>')
    links = "\n      ".join(parts)

    return f"""<a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="site-header">
  <div class="container header-inner">
    {brand(root)}

    <nav class="nav" id="nav-principal" aria-label="Navigation principale">
      {links}
      <span class="nav__cta">
        <a class="btn btn--primary" href="{rel('rendez-vous.html', root)}">Prendre rendez-vous</a>
      </span>
    </nav>

    <div class="header-cta">
      <a class="btn btn--primary" href="{rel('rendez-vous.html', root)}">Prendre rendez-vous</a>
      <button class="nav-toggle" type="button" aria-expanded="false"
              aria-controls="nav-principal" aria-label="Ouvrir le menu">
        <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true">{I['menu']}</svg>
        <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true">{I['close']}</svg>
      </button>
    </div>
  </div>
</header>"""


def footer(root):
    exp = "\n          ".join(
        f'<li><a href="{rel("expertises/" + e["slug"] + ".html", root)}">{e["nav"]}</a></li>'
        for e in EXPERTISES
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-grid">
        <div class="footer-brand">
          {brand(root)}
          <p>Conseil et assistance en matière fiscale, sociale, administrative,
             financière et de gestion.</p>
          <p style="margin-top:16px;color:var(--brass-lt);font-size:.72rem;
                    letter-spacing:.16em;text-transform:uppercase">{SITE['signature']}</p>
        </div>

        <div>
          <h2 class="footer-titre">Expertises</h2>
          <ul>
          {exp}
          </ul>
        </div>

        <div>
          <h2 class="footer-titre">Le cabinet</h2>
          <ul>
            <li><a href="{rel('cabinet.html', root)}">Notre approche</a></li>
            <li><a href="{rel('methode.html', root)}">Notre méthode</a></li>
            <li><a href="{rel('procedure-fiscale.html', root)}">La procédure fiscale</a></li>
            <li><a href="{rel('ressources/index.html', root)}">Ressources</a></li>
            <li><a href="{rel('contact.html', root)}">Contact</a></li>
          </ul>
        </div>

        <div>
          <h2 class="footer-titre">Nous joindre</h2>
          <ul>
            {'<li><a href="tel:' + SITE['telephone_lien'] + '">' + SITE['telephone'] + '</a></li>' if a_tel() else ''}
            <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
            {'<li>' + adresse_html() + '</li>' if a_adresse() else ''}
            <li>{SITE['horaires']}</li>
          </ul>
          <p style="margin-top:26px">
            <a class="arrow arrow--light" href="{rel('rendez-vous.html', root)}">Prendre rendez-vous {icon('arrow')}</a>
          </p>
        </div>
      </div>
    </div>

    <p class="footer-note">
      {SITE['nom']} exerce une activité de conseil et d'assistance en matière fiscale, sociale,
      administrative, financière et de gestion. Le cabinet n'exerce pas la profession d'avocat et
      intervient dans les limites légalement autorisées, en coordination avec les professionnels
      compétents lorsque la situation l'exige. Les informations publiées sur ce site sont fournies
      à titre général et ne constituent pas une consultation personnalisée.
    </p>

    <div class="footer-legal">
      <span>© <span data-year>{ANNEE}</span> {SITE['nom']}</span>
      <span>
        <a href="{rel('mentions-legales.html', root)}">Mentions légales</a> ·
        <a href="{rel('confidentialite.html', root)}">Confidentialité</a> ·
        <a href="{rel('plan-du-site.html', root)}">Plan du site</a>
      </span>
    </div>
  </div>
</footer>

<div class="mobile-bar">
  {'<a class="mb-alt" href="tel:' + SITE['telephone_lien'] + '">' + icon('phone') + ' Appeler</a>'
   if a_tel() else
   '<a class="mb-alt" href="mailto:' + SITE['email'] + '">' + icon('mail') + ' Écrire</a>'}
  <a class="mb-book" href="{rel('rendez-vous.html', root)}">{icon('calendar')} Rendez-vous</a>
</div>"""


def cta(root,
        titre="Un premier échange de quinze minutes",
        texte="Présentez brièvement votre situation. Nous identifions ensemble la nature du besoin "
              "et les prochaines étapes. Sans engagement."):
    return f"""<section class="cta">
  <span class="cta__motif" aria-hidden="true"></span>
  <div class="container">
    <div class="cta__inner">
      <div class="reveal">
        <span class="label label--rule">Prendre rendez-vous</span>
        <h2>{titre}</h2>
        <p>{texte}</p>
      </div>
      <div class="cta__actions reveal reveal-d1">
        <a class="btn btn--primary" href="{rel('rendez-vous.html', root)}">Réserver un créneau</a>
        {contact_direct("arrow arrow--light")}
      </div>
    </div>
  </div>
</section>"""


def cta_rdv_seul(titre, texte, bouton=("rendez-vous.html", "Réserver un créneau")):
    """Variante du bandeau d'appel sans rappel de l'email : utilisée sur la page
    contact, où écrire est déjà l'action principale."""
    return f"""<section class="cta">
  <span class="cta__motif" aria-hidden="true"></span>
  <div class="container">
    <div class="cta__inner">
      <div class="reveal">
        <span class="label label--rule">Prendre rendez-vous</span>
        <h2>{titre}</h2>
        <p>{texte}</p>
      </div>
      <div class="cta__actions reveal reveal-d1">
        <a class="btn btn--primary" href="{bouton[0]}">{bouton[1]}</a>
      </div>
    </div>
  </div>
</section>"""


def crumb(items, root):
    lis = []
    for label, href in items:
        if href is None:
            lis.append(f'<li><span aria-current="page">{label}</span></li>')
        else:
            lis.append(f'<li><a href="{rel(href, root)}">{label}</a></li>')
    return ('<nav class="crumb" aria-label="Fil d\'Ariane"><div class="container"><ol>'
            + "".join(lis) + "</ol></div></nav>")


def page_head(label, h1, texte, meta=None):
    metas = ""
    if meta:
        metas = '<div class="page-head__meta">' + "".join(f"<span>{m}</span>" for m in meta) + "</div>"
    paragraphe = f"<p>{texte}</p>" if texte else ""
    return f"""<section class="page-head">
  <span class="page-head__motif" aria-hidden="true"></span>
  <div class="container">
    <div class="page-head__inner">
      <span class="label label--rule">{label}</span>
      <h1>{h1}</h1>
      {paragraphe}
      {metas}
    </div>
  </div>
</section>"""


def index_rows(rows, root="", niveau=3):
    """Sommaire éditorial : numéro, titre, description, flèche.

    `niveau` suit la hiérarchie de la page : h2 quand la liste vient juste après
    le h1, h3 quand elle est introduite par un titre de section. L'apparence est
    identique dans les deux cas, seule la sémantique change.
    """
    out = []
    for i, (href, titre, desc) in enumerate(rows, 1):
        out.append(f"""<a class="index__row reveal" href="{rel(href, root)}">
      <span class="index__n">{i:02d}</span>
      <h{niveau} class="index__titre">{titre}</h{niveau}>
      <span class="index__desc">{desc}</span>
      <span class="index__go">{icon('arrow', w=1.2)}</span>
    </a>""")
    return '<div class="index">' + "\n    ".join(out) + "</div>"


def steps_block(etapes):
    return '<div class="steps">' + "\n      ".join(
        f"""<div class="step reveal reveal-d{min(i, 4)}">
        <span class="step__n">{i:02d}</span>
        <h3>{t}</h3>
        <p>{d}</p>
      </div>""" for i, (t, d) in enumerate(etapes, 1)
    ) + "</div>"


def checklist(points):
    return '<ul class="checklist">' + "".join(
        f'<li>{icon("check", w=1.6)}<span>{p}</span></li>' for p in points
    ) + "</ul>"


def faq_block(pairs):
    return '<div class="faq">' + "".join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
        for i, (q, a) in enumerate(pairs)
    ) + "</div>"


def form(root, compact=False, fid="contact"):
    options = "".join(f'<option value="{e["slug"]}">{e["nav"]}</option>' for e in EXPERTISES)
    inactif = "" if SITE["form_endpoint"] else (
        '<p class="form-warn" role="note"><b>Formulaire non encore raccordé</b>'
        'Renseignez « form_endpoint » dans build.py avant la mise en ligne, '
        'sinon les messages ne partiront pas.</p>')
    message = "" if compact else f"""
      <div class="field">
        <label for="{fid}-message">Votre situation en quelques lignes</label>
        <textarea id="{fid}-message" name="message" placeholder="Décrivez brièvement votre situation et, le cas échéant, l'échéance à laquelle vous êtes confronté."></textarea>
      </div>"""
    return f"""{inactif}<form data-form id="{fid}" method="post" action="{SITE['form_endpoint']}" novalidate>
      <div class="hp-field" aria-hidden="true">
        <label for="{fid}-site">Ne pas remplir</label>
        <input type="text" id="{fid}-site" name="site" tabindex="-1" autocomplete="off">
      </div>

      <div class="field-row">
        <div class="field">
          <label for="{fid}-nom">Nom et prénom</label>
          <input type="text" id="{fid}-nom" name="nom" required autocomplete="name" placeholder="Marie Durand">
        </div>
        <div class="field">
          <label for="{fid}-tel">Téléphone</label>
          <input type="tel" id="{fid}-tel" name="telephone" required autocomplete="tel" placeholder="06 12 34 56 78">
        </div>
      </div>

      <div class="field">
        <label for="{fid}-email">Adresse email</label>
        <input type="email" id="{fid}-email" name="email" required autocomplete="email" placeholder="marie.durand@entreprise.fr">
      </div>

      <div class="field">
        <label for="{fid}-motif">Motif de votre demande</label>
        <select id="{fid}-motif" name="motif" required>
          <option value="">Sélectionnez un motif</option>
          {options}
          <option value="autre">Autre demande</option>
        </select>
      </div>{message}

      <div class="form-consent">
        <input type="checkbox" id="{fid}-consent" name="consentement" required>
        <label for="{fid}-consent">J'accepte d'être recontacté au sujet de ma demande.
          <a href="{rel('confidentialite.html', root)}">Politique de confidentialité</a>.</label>
      </div>

      <button class="btn btn--primary btn--block" type="submit">Envoyer mon message</button>
      <p class="form-note">Réponse sous 24 heures ouvrées</p>
    </form>"""


def rdv_url(root, motif=None):
    """Lien vers la page de réservation, motif pré-sélectionné le cas échéant."""
    base = rel("rendez-vous.html", root)
    return f"{base}?motif={motif}" if motif else base


def booking_card(root, motif=None, titre="Réservez votre premier échange",
                 sous="Choisissez directement un créneau dans l'agenda du cabinet. "
                      "Confirmation immédiate par email."):
    """Carte de conversion : elle mène à la page de réservation, sans script tiers."""
    return f"""<div class="panel reveal reveal-d2">
      <span class="panel__label">15 minutes offertes</span>
      <h2>{titre}</h2>
      <p class="panel__sub">{sous}</p>
      <ol class="mini-steps">
        <li><span>1</span> Vous choisissez un créneau disponible</li>
        <li><span>2</span> Vous indiquez votre téléphone et le motif</li>
        <li><span>3</span> Vous recevez la confirmation par email</li>
      </ol>
      <a class="btn btn--primary btn--block" href="{rdv_url(root, motif)}">
        {icon('calendar')} Choisir mon créneau
      </a>
      <p class="form-note">Téléphone · 15 minutes · Sans engagement</p>
      <p class="panel__alt">
        Vous préférez écrire&nbsp;?
        <a href="{rel('contact.html', root)}">Formulaire de contact</a>
        · <a href="mailto:{SITE['email']}">Nous écrire</a>
      </p>
    </div>"""


def motifs_json():
    """Correspondance slug → libellé, pour pré-remplir la question « motif »."""
    import json
    table = {e["slug"]: e["nav"] for e in EXPERTISES}
    table["autre"] = "Autre demande"
    return json.dumps(table, ensure_ascii=False).replace("'", "&#39;")


def calendly_embed():
    """Widget de réservation, chargé en même temps que la page.

    Le module du prestataire est appelé dès l'ouverture de la page : il peut
    déposer ses cookies sans action préalable du visiteur. La page
    « Confidentialité » l'indique explicitement.
    """
    return f"""<div class="booking" id="reservation">
      <div class="booking__intro">
        <span class="panel__label">Agenda en ligne</span>
        <h2 class="index__titre">Choisissez votre créneau</h2>
        <p>
          Sélectionnez le jour et l'heure qui vous conviennent : la confirmation
          vous parvient aussitôt par courriel.
        </p>
      </div>
      <div class="booking__widget" id="booking-widget"
           data-calendly="{html.escape(SITE['calendly'], quote=True)}"
           data-motifs='{motifs_json()}'>
        <p class="booking__loading">Chargement du calendrier&#8230;</p>
      </div>
      <p class="booking__fallback">
        Vous préférez ne pas passer par l'agenda&nbsp;? Écrivez-nous à
        <a href="mailto:{SITE['email']}">{SITE['email']}</a>, nous fixons le créneau ensemble.
      </p>
    </div>"""


# ---------------------------------------------------------------------------
# Données structurées
# ---------------------------------------------------------------------------
def jsonstr(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def jsonlist(items):
    return "[" + ",".join(jsonstr(x) for x in items) + "]"


def offres_schema():
    return ",".join(
        '{"@type":"Offer","itemOffered":{"@type":"Service","name":%s,"url":%s}}'
        % (jsonstr(e["titre"]), jsonstr(SITE["domaine"] + "/expertises/" + e["slug"] + ".html"))
        for e in EXPERTISES
    )


def adresse_schema():
    """Bloc PostalAddress : on ne déclare que ce qui existe réellement."""
    champs = ['"addressCountry":"FR"']
    if SITE["adresse"].strip():
        champs.insert(0, f'"streetAddress":"{SITE["adresse"]}"')
    if SITE["code_postal"].strip():
        champs.insert(-1, f'"postalCode":"{SITE["code_postal"]}"')
    if SITE["ville"].strip():
        champs.insert(-1, f'"addressLocality":"{SITE["ville"]}"')
    return '"address":{"@type":"PostalAddress",' + ",".join(champs) + "},"


def schema_org():
    """Fiche du cabinet : c'est elle que Google lit pour le panneau de connaissance."""
    tel = f'"telephone":"{SITE["telephone_lien"]}",' if a_tel() else ""
    mots = ["conseil fiscal", "contrôle fiscal", "contrôle URSSAF",
            "proposition de rectification", "réclamation contentieuse",
            "recours hiérarchique", "entreprises en difficulté", "sauvegarde",
            "redressement judiciaire", "création d'entreprise", "paie",
            "déclaration sociale nominative"]
    return f"""<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ProfessionalService",
"@id":"{SITE['domaine']}/#cabinet",
"name":"{SITE['nom']}",
"description":"Conseil et assistance en matière fiscale, sociale, administrative, financière et de gestion.",
"url":"{SITE['domaine']}",{tel}"email":"{SITE['email']}",
{adresse_schema()}
"areaServed":{{"@type":"Country","name":"France"}},
"priceRange":"€€","currenciesAccepted":"EUR",
"slogan":"{SITE['signature']}",
"logo":"{SITE['domaine']}/assets/img/og.png",
"image":"{SITE['domaine']}/assets/img/og.png",
"knowsAbout":{jsonlist(mots)},
"makesOffer":[{offres_schema()}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebSite","name":"{SITE['nom']}",
"url":"{SITE['domaine']}","inLanguage":"fr-FR"}}
</script>"""


def article_schema(titre, resume, page):
    """Page pédagogique : Google la traite comme un article de référence."""
    return ('<script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"Article",'
            f'"headline":{jsonstr(titre)},"description":{jsonstr(resume)},'
            f'"inLanguage":"fr-FR","datePublished":"{date.today().isoformat()}",'
            f'"dateModified":"{date.today().isoformat()}",'
            '"author":{"@type":"Organization","name":%s},'
            '"publisher":{"@type":"Organization","name":%s,"logo":{"@type":"ImageObject","url":%s}},'
            '"mainEntityOfPage":{"@type":"WebPage","@id":%s},'
            '"image":%s}</script>'
            % (jsonstr(SITE["nom"]), jsonstr(SITE["nom"]),
               jsonstr(SITE["domaine"] + "/assets/img/og.png"),
               jsonstr(SITE["domaine"] + "/" + page),
               jsonstr(SITE["domaine"] + "/assets/img/og.png")))


def breadcrumb_schema(items):
    """Fil d'Ariane exploitable par Google (affiché sous le titre des résultats)."""
    el = []
    for i, (label, href) in enumerate(items, 1):
        url = SITE["domaine"] + "/" + (href or "").lstrip("./")
        el.append('{"@type":"ListItem","position":%d,"name":%s,"item":%s}'
                  % (i, jsonstr(label), jsonstr(url)))
    return ('<script type="application/ld+json">'
            f'{{"@context":"https://schema.org","@type":"BreadcrumbList",'
            f'"itemListElement":[{",".join(el)}]}}</script>')


def service_schema(e):
    """Décrit chaque pôle comme un service rendu par le cabinet."""
    return ('<script type="application/ld+json">'
            '{"@context":"https://schema.org","@type":"Service",'
            f'"name":{jsonstr(e["titre"])},'
            f'"description":{jsonstr(e["resume"])},'
            f'"serviceType":{jsonstr(e["titre"])},'
            '"provider":{"@type":"ProfessionalService","name":%s,"url":%s},'
            '"areaServed":{"@type":"Country","name":"France"},'
            '"audience":{"@type":"BusinessAudience","audienceType":"Dirigeants et entreprises"}}'
            '</script>' % (jsonstr(SITE["nom"]), jsonstr(SITE["domaine"])))


def faq_schema(pairs):
    items = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (jsonstr(q), jsonstr(a)) for q, a in pairs
    )
    return ('<script type="application/ld+json">'
            f'{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}</script>')


# ---------------------------------------------------------------------------
# Gabarit de page
# ---------------------------------------------------------------------------
def layout(path, titre, description, body, root="", schema=""):
    canonical = SITE["domaine"] + "/" + ("" if path == "index.html" else path)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{'noindex, follow' if path == '404.html' else 'index, follow'}">
<meta name="theme-color" content="#0B1B30">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; base-uri 'self'; object-src 'none'; form-action 'self' https://formspree.io https://api.web3forms.com; img-src 'self' data:; style-src 'self' 'unsafe-inline' https://assets.calendly.com; font-src 'self'; script-src 'self' https://assets.calendly.com; frame-src https://calendly.com; connect-src 'self' https://calendly.com">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{SITE['nom']}">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['domaine']}/assets/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{SITE['nom']} — {SITE['baseline']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel('assets/img/favicon.svg', root)}" type="image/svg+xml">
<link rel="alternate" hreflang="fr-FR" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<link rel="preload" as="font" type="font/woff2" crossorigin
      href="{rel('assets/fonts/fraunces-normal-latin.woff2', root)}">
<link rel="preload" as="font" type="font/woff2" crossorigin
      href="{rel('assets/fonts/archivo-normal-latin.woff2', root)}">
<link rel="stylesheet" href="{rel_v('assets/css/fonts.css', root)}">
<link rel="stylesheet" href="{rel_v('assets/css/style.css', root)}">
{schema}
</head>
<body>
{header(path, root)}
<main id="contenu">
{body}
</main>
{footer(root)}
<script src="{rel_v('assets/js/main.js', root)}" defer></script>
</body>
</html>
"""


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("  ·", path)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_accueil():
    rows = index_rows([(f"expertises/{e['slug']}.html", e["titre"], e["resume"]) for e in EXPERTISES])

    body = f"""<section class="hero">
  <span class="hero__motif" aria-hidden="true"></span>
  <div class="container">
    <div class="hero__inner">
      <div>
        <span class="label label--rule">{SITE['baseline']}</span>
        <h1>Il est temps<br>d'<em>agir</em>.</h1>
        <p class="hero__text">
          Face aux difficultés de votre entreprise, chaque étape mérite d'être préparée.
          Un accompagnement clair et structuré pour comprendre votre situation
          et avancer avec méthode.
        </p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="#rdv-accueil">Réserver 15 minutes</a>
          <a class="arrow arrow--light" href="expertises/index.html">Nos expertises {icon('arrow')}</a>
        </div>
        <dl class="hero__proof">
          <div><dt>15 min</dt><dd>Premier échange offert</dd></div>
          <div><dt>24 h</dt><dd>Délai de réponse</dd></div>
          <div><dt>7</dt><dd>Pôles d'expertise</dd></div>
        </dl>
      </div>

      {booking_card("", None, "Un premier échange par téléphone",
             "Faites le point sur votre situation et identifiez les prochaines étapes.")}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="label label--rule">Nos expertises</span>
      <h2>Sept pôles pour accompagner l'entreprise</h2>
      <p>Fiscalité, contrôles, création, paie, gestion, difficultés et recours.
         Chaque situation appelle une préparation différente.</p>
    </div>
    {rows}
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head reveal">
      <span class="label label--rule">Notre méthode</span>
      <h2>Une démarche structurée en quatre étapes</h2>
      <p>Une méthode lisible pour comprendre les enjeux et construire un dossier
         qui tient devant l'administration.</p>
    </div>
    {steps_block([
      ("Analyser", "Comprendre votre situation, vos documents et le contexte de l'entreprise."),
      ("Identifier", "Repérer les enjeux, les risques et les priorités du dossier."),
      ("Préparer", "Organiser les éléments et construire un dossier exploitable."),
      ("Coordonner", "Mobiliser l'expert-comptable, l'avocat fiscaliste ou le professionnel compétent."),
    ])}
    <p class="mt"><a class="arrow" href="methode.html">La méthode en détail {icon('arrow')}</a></p>
  </div>
</section>

<section class="section section--ivory">
  <div class="container">
    <div class="grid grid--2" style="align-items:start;gap:clamp(36px,6vw,90px)">
      <div class="reveal">
        <span class="label label--rule">Comprendre la procédure</span>
        <h2>Chaque étape a un délai. Le dépasser vous coûte vos droits.</h2>
        <p class="lede mt">
          De la proposition de rectification jusqu'au tribunal administratif, la procédure
          fiscale suit un calendrier strict. Nous l'avons détaillée étape par étape.
        </p>
        <p class="mt"><a class="arrow" href="procedure-fiscale.html">Voir les huit étapes {icon('arrow')}</a></p>
      </div>
      <div class="reveal reveal-d2">
        <div class="delay-card">
          <div class="tl-delay__label">Pour répondre à une proposition de rectification</div>
          <div class="tl-delay__value">30 jours</div>
          <div class="tl-delay__from">Passé ce délai, l'absence de réponse vaut acceptation tacite
            des redressements proposés.</div>
        </div>
        <div class="delay-card">
          <div class="tl-delay__label">Pour la réponse à une réclamation contentieuse</div>
          <div class="tl-delay__value">6 mois</div>
          <div class="tl-delay__from">L'administration doit répondre de manière explicite et motivée.</div>
        </div>
        <div class="delay-card">
          <div class="tl-delay__label">Pour saisir le tribunal administratif</div>
          <div class="tl-delay__value">2 mois</div>
          <div class="tl-delay__from">Après la décision de rejet, ou après six mois de silence
            de l'administration.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <span class="label label--rule">Le cabinet</span>
      <h2>Une approche globale et personnalisée</h2>
    </div>
    <div class="grid grid--3">
      <div class="note reveal">
        {icon('lock', 'note__icon')}
        <h3>Confidentialité</h3>
        <p>Vos documents et votre situation restent strictement confidentiels.
           C'est la condition d'un échange utile.</p>
      </div>
      <div class="note reveal reveal-d1">
        {icon('target', 'note__icon')}
        <h3>Anticipation</h3>
        <p>Prévenir les risques et sécuriser les décisions avant qu'une échéance
           ne les impose.</p>
      </div>
      <div class="note reveal reveal-d2">
        {icon('users', 'note__icon')}
        <h3>Coordination</h3>
        <p>Un réseau de professionnels mobilisés selon les besoins réels
           de votre dossier.</p>
      </div>
    </div>
  </div>
</section>

{cta("")}
"""
    return layout("index.html",
                  seo_titre("Conseil fiscal, contrôles et entreprises"),
                  "Contrôle fiscal, contrôle URSSAF, entreprise en difficulté, création, paie et DSN : "
                  "conseil et assistance aux dirigeants. Premier échange de 15 minutes offert.",
                  body, "", schema_org())


def seo_titre(debut):
    """Titre de page : mot-clé d'abord, marque à la fin, ville si renseignée."""
    ville = SITE["ville"].strip()
    lieu = f" à {ville}" if ville and "compléter" not in ville.lower() else ""
    return f"{debut}{lieu} | {SITE['nom']}"


def page_expertise(e):
    root = "../"
    autres = [x for x in EXPERTISES if x["slug"] != e["slug"]][:4]
    body = f"""{page_head("Expertise", e['titre'], e['accroche'] + " — " + e['resume'], e['tags'])}

{crumb([("Accueil", "index.html"), ("Expertises", "expertises/index.html"), (e['titre'], None)], root)}

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="align-items:start;gap:clamp(36px,6vw,90px)">
      <div class="reveal">
        <span class="label label--rule">Le contexte</span>
        <h2>{e['accroche']}</h2>
        <p class="lede mt">{e['intro']}</p>
        <hr class="divider">
        <h3 class="mb">Ce que nous prenons en charge</h3>
        {checklist(e['points'])}
      </div>
      {booking_card(root, e['slug'], "Parlons de votre dossier",
             "Un premier échange téléphonique pour comprendre votre situation et identifier "
             "l'accompagnement adapté.")}
    </div>
  </div>
</section>

<section class="section section--ivory">
  <div class="container">
    <div class="section-head reveal">
      <span class="label label--rule">Déroulé</span>
      <h2>Comment nous procédons</h2>
    </div>
    {steps_block(e['etapes'])}
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div class="section-head reveal">
      <span class="label label--rule">Questions fréquentes</span>
      <h2>Ce que l'on nous demande</h2>
    </div>
    {faq_block(e['faq'])}
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head reveal">
      <span class="label label--rule">Autres expertises</span>
      <h2>Poursuivre votre lecture</h2>
    </div>
    {index_rows([(a['slug'] + '.html', a['titre'], a['resume']) for a in autres])}
  </div>
</section>

{cta(root)}
"""
    return layout(f"expertises/{e['slug']}.html", seo_titre(e['titre_seo']),
                  e["meta"], body, root,
                  faq_schema(e["faq"]) + service_schema(e) + breadcrumb_schema(
                      [("Accueil", ""), ("Expertises", "expertises/"),
                       (e["titre"], "expertises/" + e["slug"] + ".html")]))


def page_expertises_index():
    root = "../"
    body = f"""{page_head("Nos expertises", "Sept pôles pour accompagner l'entreprise",
      "Fiscalité, contrôles, création, paie, gestion, difficultés et recours. Chaque situation "
      "appelle une préparation différente et un calendrier propre.")}

{crumb([("Accueil", "index.html"), ("Expertises", None)], root)}

<section class="section">
  <div class="container">
    {index_rows([(e['slug'] + '.html', e['titre'], e['resume']) for e in EXPERTISES], niveau=2)}
  </div>
</section>

{cta(root)}
"""
    return layout("expertises/index.html", seo_titre("Nos sept pôles d'expertise"),
                  "Conseil fiscal, contrôle fiscal, contrôle URSSAF, entreprise en difficulté, "
                  "création, paie et DSN, procédures et recours : sept pôles d'accompagnement.",
                  body, root,
                  breadcrumb_schema([("Accueil", ""), ("Expertises", "expertises/index.html")]))


def page_cabinet():
    body = f"""{page_head("Le cabinet", "Une approche globale et personnalisée",
      "Conseil et assistance en matière fiscale, sociale, administrative, financière et de gestion, "
      "pour les dirigeants, les entreprises et les entrepreneurs.")}

{crumb([("Accueil", "index.html"), ("Le cabinet", None)], "")}

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="gap:clamp(36px,6vw,90px);align-items:start">
      <div class="reveal">
        <span class="label label--rule">Notre positionnement</span>
        <h2>Comprendre avant de décider</h2>
        <p class="lede mt">
          La plupart des dossiers qui arrivent au cabinet ont un point commun : ils ont commencé
          par une lettre ouverte trop tard, ou par une décision prise sans en avoir mesuré
          les conséquences.
        </p>
        <p>
          Notre rôle est d'abord de comprendre la situation réelle de l'entreprise, puis
          d'identifier ce qui est en jeu, de préparer les éléments nécessaires et, lorsque le
          dossier l'exige, de mobiliser le professionnel compétent.
        </p>
        <p>
          Nous n'exerçons pas la profession d'avocat. Nous intervenons sur l'analyse, la
          préparation administrative des dossiers et la coordination, dans les limites légalement
          autorisées. C'est un périmètre clair, et c'est aussi ce qui nous permet de travailler
          efficacement aux côtés des avocats fiscalistes et des experts-comptables plutôt qu'en
          concurrence avec eux.
        </p>
      </div>
      <div class="stack reveal reveal-d2">
        <div class="note">
          {icon('lock', 'note__icon')}
          <h3>Confidentialité</h3>
          <p>Les situations que nous traitons touchent au plus sensible de la vie d'une entreprise.
             Vos documents et vos échanges restent strictement confidentiels.</p>
        </div>
        <div class="note">
          {icon('target', 'note__icon')}
          <h3>Anticipation</h3>
          <p>Prévenir les risques et sécuriser les décisions avant qu'une échéance ne les impose.
             Un dossier préparé se défend toujours mieux qu'un dossier subi.</p>
        </div>
        <div class="note">
          {icon('users', 'note__icon')}
          <h3>Coordination</h3>
          <p>Expert-comptable, avocat fiscaliste, mandataire : nous mobilisons le bon interlocuteur
             au bon moment, et nous assurons le lien entre eux.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head reveal">
      <span class="label label--rule">Périmètre d'intervention</span>
      <h2>Ce que recouvre notre activité</h2>
    </div>
    <div class="grid grid--2">
      <div class="reveal">{checklist([
        "Conseil, assistance et prestations de services en matière fiscale, sociale, administrative, financière et de gestion",
        "Assistance à la création, la constitution, la reprise, l'organisation et le développement des entreprises",
        "Gestion administrative de la paie, préparation et suivi des déclarations sociales et fiscales",
      ])}</div>
      <div class="reveal reveal-d2">{checklist([
        "Conseil et assistance dans le cadre des contrôles fiscaux, contrôles URSSAF et procédures administratives",
        "Conseil et assistance aux entreprises en difficulté, dans les limites légalement autorisées",
        "Analyse, préparation de dossiers et de documents, assistance administrative",
      ])}</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div class="section-head reveal">
      <span class="label label--rule">Questions fréquentes</span>
      <h2>Avant de nous contacter</h2>
    </div>
    {faq_block([
      ("Êtes-vous avocats ?", "Non. CCF Conseil exerce une activité de conseil et d'assistance. Nous intervenons sur l'analyse, la préparation administrative des dossiers et la coordination des professionnels compétents, dans les limites légalement autorisées. Lorsqu'un dossier appelle une intervention juridique ou une représentation devant une juridiction, nous coordonnons un avocat fiscaliste."),
      ("Travaillez-vous avec mon expert-comptable ?", "Oui, et c'est souvent la meilleure configuration. L'expert-comptable connaît vos chiffres, nous apportons la préparation du dossier et le suivi de la procédure. Les deux interventions se complètent."),
      ("Le premier échange est-il vraiment gratuit ?", "Oui. Quinze minutes par téléphone, sans engagement, pour comprendre votre situation et vous dire honnêtement si nous sommes le bon interlocuteur."),
      ("Intervenez-vous partout en France ?", "Oui. Les échanges se font par téléphone, en visioconférence ou au cabinet selon votre préférence et la nature du dossier."),
    ])}
  </div>
</section>

{cta("")}
"""
    return layout("cabinet.html", seo_titre("Le cabinet de conseil fiscal"),
                  "Cabinet de conseil et d'assistance en matière fiscale, sociale et administrative. "
                  "Confidentialité, anticipation et coordination des professionnels compétents.",
                  body, "", breadcrumb_schema([("Accueil", ""), ("Le cabinet", "cabinet.html")]))


def page_methode():
    detail = [
        ("Analyser", "Comprendre votre situation et vos documents",
         "Nous partons de ce qui existe : vos documents comptables et fiscaux, les courriers reçus, "
         "l'historique de l'entreprise. Cette lecture prend du temps et c'est normal : un dossier "
         "mal compris au départ se défend mal ensuite.",
         ["Lecture des documents comptables et fiscaux", "Analyse des courriers et actes reçus",
          "Compréhension de l'activité et du contexte", "Identification des pièces manquantes"]),
        ("Identifier", "Repérer les enjeux, les risques et les priorités",
         "Tous les points d'un dossier n'ont pas le même poids. Nous distinguons ce qui est solide "
         "de ce qui est fragile, ce qui est urgent de ce qui peut attendre, et ce qui relève de "
         "notre périmètre de ce qui appelle un autre professionnel.",
         ["Hiérarchisation des points de vigilance", "Identification des délais applicables",
          "Évaluation des suites possibles", "Définition de la stratégie de réponse"]),
        ("Préparer", "Organiser les éléments et construire le dossier",
         "Un dossier exploitable est un dossier où chaque affirmation est justifiée par une pièce. "
         "C'est la partie la plus longue du travail, et celle qui fait la différence devant "
         "l'administration.",
         ["Collecte et organisation des justificatifs", "Rédaction des observations argumentées",
          "Construction d'un dossier structuré", "Respect strict des délais"]),
        ("Coordonner", "Mobiliser le professionnel compétent",
         "Certaines étapes relèvent de l'avocat, du notaire ou de l'expert-comptable. Nous les "
         "mobilisons au bon moment, avec un dossier déjà préparé, ce qui réduit leur temps "
         "d'intervention et donc son coût.",
         ["Mise en relation avec l'avocat fiscaliste", "Lien avec l'expert-comptable",
          "Transmission d'un dossier prêt à l'emploi", "Suivi coordonné jusqu'à la clôture"]),
    ]
    blocks = "".join(f"""<div class="tl-item tl-item--wide reveal">
      <span class="tl-n">{i:02d}</span>
      <div>
        <span class="label" style="margin-bottom:12px">{t}</span>
        <h2 class="tl-titre">{s}</h2>
        <p class="mt-s">{x}</p>
        <div class="mt">{checklist(pts)}</div>
      </div>
    </div>""" for i, (t, s, x, pts) in enumerate(detail, 1))

    body = f"""{page_head("Notre méthode", "Une démarche structurée en quatre étapes",
      "Une méthode lisible pour comprendre les enjeux, construire un dossier exploitable et savoir "
      "à chaque instant où en est la procédure.",
      ["Analyser", "Identifier", "Préparer", "Coordonner"])}

{crumb([("Accueil", "index.html"), ("Notre méthode", None)], "")}

<section class="section">
  <div class="container">
    <div class="timeline">{blocks}</div>
  </div>
</section>

{cta("")}
"""
    return layout("methode.html", seo_titre("Notre méthode en quatre étapes"),
                  "Analyser la situation, identifier les enjeux, préparer un dossier exploitable et "
                  "coordonner les professionnels compétents : la méthode du cabinet, étape par étape.",
                  body, "", breadcrumb_schema([("Accueil", ""), ("Notre méthode", "methode.html")]))


def page_procedure():
    items = "".join(f"""<div class="tl-item reveal">
      <span class="tl-n">{i:02d}</span>
      <div>
        <h2 class="tl-titre">{titre}</h2>
        <p class="mt-s">{texte}</p>
        <div class="callout{' callout--alert' if ton == 'alert' else ''}">
          <b>{'Attention' if ton == 'alert' else 'À savoir'}</b>{note}
        </div>
      </div>
      <div class="tl-delay">
        <div class="tl-delay__label">{label}</div>
        <div class="tl-delay__value">{valeur}</div>
        <div class="tl-delay__from">{source}</div>
      </div>
    </div>""" for i, (titre, texte, label, valeur, source, ton, note) in enumerate(PROCEDURE, 1))

    faq = [
        ("Que se passe-t-il si je ne réponds pas dans les 30 jours ?",
         "L'absence de réponse dans le délai vaut acceptation tacite des rectifications proposées. "
         "Les sommes deviennent exigibles et la contestation devient nettement plus difficile."),
        ("Puis-je demander un délai supplémentaire ?",
         "Oui. Une prolongation de trente jours peut être demandée pour répondre à une proposition "
         "de rectification. La demande doit être formulée dans le délai initial."),
        ("Comment suspendre les mesures de recouvrement ?",
         "Par une demande de sursis de paiement fondée sur l'article L. 277 du Livre des procédures "
         "fiscales, présentée avec la réclamation. Elle suspend le recouvrement des sommes "
         "contestées, l'administration pouvant demander des garanties."),
        ("Le recours hiérarchique est-il obligatoire ?",
         "Non, il est facultatif. C'est une voie amiable qui permet souvent de trouver une solution "
         "sans saisir le tribunal, sans faire perdre le bénéfice des autres recours."),
    ]

    body = f"""{page_head("Comprendre la procédure", "La procédure fiscale, étape par étape",
      "De la proposition de rectification jusqu'à la décision du tribunal administratif : chaque "
      "étape a un délai. Le dépasser, c'est perdre le droit de contester.",
      ["30 jours pour répondre", "6 mois de réponse", "2 mois pour saisir le juge"])}

{crumb([("Accueil", "index.html"), ("La procédure fiscale", None)], "")}

<section class="section section--tight">
  <div class="container container--narrow">
    <div class="callout callout--alert reveal">
      <b>Repère pédagogique</b>
      Les délais indiqués sont ceux applicables dans les cas les plus courants. Ils varient selon
      la nature du contrôle, la procédure engagée et votre situation. Cette page ne remplace pas
      l'analyse de votre dossier.
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="timeline">{items}</div>
  </div>
</section>

<section class="section section--ivory">
  <div class="container container--narrow">
    <div class="section-head reveal">
      <span class="label label--rule">Questions fréquentes</span>
      <h2>Les délais et les recours</h2>
    </div>
    {faq_block(faq)}
  </div>
</section>

{cta("", "Vous avez reçu un courrier de l'administration ?",
     "Le premier réflexe utile est de vérifier la date de réception et le délai de réponse. "
     "Appelez-nous, nous le regardons ensemble.")}
"""
    return layout("procedure-fiscale.html",
                  seo_titre("Procédure fiscale : étapes et délais"),
                  "Proposition de rectification, réclamation contentieuse, recours hiérarchique, "
                  "tribunal administratif : les huit étapes et le délai applicable à chacune.",
                  body, "", faq_schema(faq) + breadcrumb_schema(
                      [("Accueil", ""), ("La procédure fiscale", "procedure-fiscale.html")])
                  + article_schema(
                      "La procédure fiscale, étape par étape",
                      "Les huit étapes de la procédure fiscale, de la proposition de "
                      "rectification à la décision du tribunal administratif, et le délai "
                      "applicable à chacune.",
                      "procedure-fiscale.html"))


def page_ressources():
    root = "../"
    lignes = []
    for n, r in enumerate(RESSOURCES, 1):
        if r.get("publie") and r.get("lien"):
            lignes.append(f"""<a class="index__row reveal" href="{r['lien']}">
        <span class="index__n">{n:02d}</span>
        <h2 class="index__titre">{r['titre']}</h2>
        <span class="index__desc">{r['resume']}</span>
        <span class="index__go">{icon('arrow', w=1.2)}</span>
      </a>""")
        else:
            lignes.append(f"""<div class="index__row index__row--soon">
        <span class="index__n">{n:02d}</span>
        <h2 class="index__titre">{r['titre']}</h2>
        <span class="index__desc">{r['resume']}</span>
        <span class="index__soon">À venir</span>
      </div>""")

    body = f"""{page_head("Ressources", "Comprendre avant de subir",
      "Des repères clairs sur les procédures fiscales et sociales, écrits pour des dirigeants qui "
      "n'ont ni le temps ni l'envie de lire le Livre des procédures fiscales.")}

{crumb([("Accueil", "index.html"), ("Ressources", None)], root)}

<section class="section">
  <div class="container">
    <div class="index">{"".join(lignes)}</div>
  </div>
</section>

{cta(root)}
"""
    return layout("ressources/index.html", seo_titre("Ressources : contrôles et procédures"),
                  "Guides et fiches pratiques sur le contrôle fiscal, le contrôle URSSAF, les délais "
                  "de procédure, le sursis de paiement et les difficultés d'entreprise.", body, root)


def carte_cabinet():
    """Rendez-vous au cabinet : proposé seulement si une adresse est renseignée."""
    if not a_adresse():
        return ""
    return f"""<div class="note">
            {icon('pin', 'note__icon')}
            <h3>Au cabinet</h3>
            <p>{adresse_html()}<br>{SITE['horaires']}</p>
          </div>"""


def page_contact():
    body = f"""{page_head("Contact", "Prenons le temps d'analyser votre situation",
      "Un premier échange pour comprendre votre besoin et identifier l'accompagnement adapté. "
      "Par téléphone, en visioconférence ou au cabinet.")}

{crumb([("Accueil", "index.html"), ("Contact", None)], "")}

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="gap:clamp(36px,6vw,90px);align-items:start">
      <div class="reveal">
        <span class="label label--rule">Nous joindre</span>
        <h2>{"Trois façons d'échanger" if a_adresse() else "Deux façons d'échanger"}</h2>
        <div class="stack mt">
          <div class="note">
            {icon('mail', 'note__icon')}
            <h3>Par email</h3>
            <p>Le plus simple pour exposer une situation et joindre le contexte utile.
               Réponse sous 24 heures ouvrées.</p>
            <p class="mt-s">{lien_email("arrow")}</p>
          </div>
          <div class="note">
            {icon('video', 'note__icon')}
            <h3>En visioconférence</h3>
            <p>Pratique pour passer en revue des documents ensemble, où que vous soyez.</p>
          </div>
          {carte_cabinet()}
        </div>
      </div>
      <div class="panel reveal reveal-d2">
        <span class="panel__label">Formulaire de contact</span>
        <h2>Décrivez votre situation</h2>
        <p class="panel__sub">Nous vous répondons sous 24 heures ouvrées. Si votre échéance est
          proche, réservez directement un créneau.</p>
        {form("", False, "contact")}
      </div>
    </div>
  </div>
</section>

{cta_rdv_seul("Vous préférez fixer un créneau&nbsp;?",
     "Choisissez directement une disponibilité dans l'agenda du cabinet. "
     "Quinze minutes, sans engagement.")}
"""
    return layout("contact.html", seo_titre("Contacter le cabinet"),
                  "Écrivez-nous ou réservez un premier échange de 15 minutes, par téléphone, "
                  "en visioconférence ou au cabinet. Sans engagement, réponse sous 24 heures.",
                  body, "", breadcrumb_schema([("Accueil", ""), ("Contact", "contact.html")]))


def page_rdv():
    formats = [
        ("phone", "Par téléphone", "Nous vous appelons au numéro indiqué lors de la réservation."),
        ("video", "En visioconférence", "Pour examiner ensemble des documents pendant l'échange."),
    ]
    if a_adresse():
        formats.append(("pin", "Au cabinet",
                        "Sur rendez-vous, pour les dossiers qui méritent un examen approfondi."))
    cartes = "".join(f"""<div class="note reveal">
        {icon(ic, 'note__icon')}<h2 class="index__titre">{titre}</h2><p>{texte}</p>
      </div>""" for ic, titre, texte in formats)

    body = f"""{page_head("Rendez-vous", "15 minutes offertes pour faire le point",
      "Choisissez un créneau dans l'agenda du cabinet. Sans engagement, et sans échange de mails "
      "pour trouver une date.",
      ["15 minutes", "Sans engagement", "Confidentiel"])}

{crumb([("Accueil", "index.html"), ("Rendez-vous", None)], "")}

<section class="section section--tight">
  <div class="container" style="max-width:940px">
    {calendly_embed()}
  </div>
</section>

<section class="section section--ivory section--tight">
  <div class="container">
    <div class="section-head reveal" style="margin-bottom:clamp(26px,3vw,40px)">
      <span class="label label--rule">Le format de l'échange</span>
      <h2>Vous choisissez au moment de réserver</h2>
    </div>
    <div class="grid grid--3">{cartes}</div>

    <div class="callout mt" style="max-width:70ch">
      <b>Avant le premier échange</b>
      N'envoyez aucun document ni aucune information sensible. Les pièces d'un dossier se
      transmettent ensuite, par un moyen sécurisé convenu ensemble.
    </div>
  </div>
</section>

{cta_rdv_seul("Vous préférez exposer votre situation par écrit&nbsp;?",
     "Décrivez votre demande par le formulaire de contact. Réponse sous 24 heures ouvrées.",
     ("contact.html", "Formulaire de contact"))}
"""
    return layout("rendez-vous.html", seo_titre("Prendre rendez-vous, 15 minutes offertes"),
                  "Choisissez un créneau dans l'agenda du cabinet : premier échange de 15 minutes, "
                  "par téléphone, en visioconférence ou au cabinet. Sans engagement.",
                  body, "", breadcrumb_schema([("Accueil", ""), ("Rendez-vous", "rendez-vous.html")]))


def page_prose(path, titre, h1, label, description, contenu):
    body = f"""{page_head(label, h1, "")}
{crumb([("Accueil", "index.html"), (h1, None)], "")}
<section class="section">
  <div class="container"><div class="prose">{contenu}</div></div>
</section>

{cta("", "Une question sur votre situation ?",
     "Un premier échange de quinze minutes, sans engagement, pour comprendre votre besoin "
     "et identifier l'accompagnement adapté.")}
"""
    return layout(path, titre, description, body, "")


def page_mentions():
    contenu = f"""
<h2>Éditeur du site</h2>
<p>{SITE['nom']} — {SITE['forme']}<br>
Siège social : {adresse_html(", ") or "à compléter"}<br>
SIREN : {SITE['siren']}<br>
Téléphone : <a href="tel:{SITE['telephone_lien']}">{SITE['telephone']}</a><br>
Courriel : <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
<p><em>Directeur de la publication, numéro de TVA intracommunautaire, capital social et assurance
de responsabilité civile professionnelle : à compléter avant mise en ligne.</em></p>

<h2>Hébergement</h2>
<p>Le site est hébergé par GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107,
États-Unis — <a href="https://github.com" rel="noopener">github.com</a>.</p>

<h2>Nature de l'activité</h2>
<p>{SITE['nom']} exerce une activité de conseil, d'assistance et de prestations de services en
matière fiscale, sociale, administrative, financière et de gestion. Le cabinet n'exerce pas la
profession d'avocat et n'assure aucune représentation devant les juridictions. Il intervient dans
les limites légalement autorisées et coordonne, lorsque la situation l'exige, les professionnels
compétents : avocat fiscaliste, expert-comptable, notaire ou mandataire.</p>

<h2>Propriété intellectuelle</h2>
<p>L'ensemble des contenus présents sur ce site — textes, illustrations, éléments graphiques,
structure — est protégé par le droit de la propriété intellectuelle. Toute reproduction ou
représentation, totale ou partielle, sans autorisation écrite préalable est interdite.</p>

<h2>Informations publiées</h2>
<p>Les informations diffusées sur ce site ont une vocation générale et pédagogique. Elles ne
constituent pas une consultation personnalisée et ne sauraient se substituer à l'analyse d'une
situation particulière. Les délais et procédures mentionnés correspondent aux cas les plus
courants et peuvent varier selon la nature du dossier.</p>

<h2>Responsabilité</h2>
<p>{SITE['nom']} met tout en œuvre pour assurer l'exactitude des informations publiées mais ne
peut garantir leur exhaustivité ni leur actualité permanente.</p>

<h2>Droit applicable</h2>
<p>Le présent site est soumis au droit français.</p>
"""
    return page_prose("mentions-legales.html", f"Mentions légales — {SITE['nom']}",
                      "Mentions légales", "Informations légales",
                      f"Mentions légales du site {SITE['nom']} : éditeur, hébergement, propriété "
                      "intellectuelle et responsabilité.", contenu)


def page_confidentialite():
    contenu = f"""
<p class="lede">Cette page décrit la manière dont {SITE['nom']} traite les données personnelles
collectées sur ce site, conformément au Règlement général sur la protection des données et à la
loi Informatique et Libertés.</p>

<h2>Responsable du traitement</h2>
<p>{SITE['nom']}{", " + adresse_html(", ") if a_adresse() else ""} —
<a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>

<h2>Données collectées</h2>
<p>Les formulaires de contact et de demande de rendez-vous collectent uniquement les données
nécessaires au traitement de votre demande : nom et prénom, numéro de téléphone, adresse email,
motif de la demande et, le cas échéant, la description que vous rédigez librement.</p>
<p><strong>Ne communiquez aucun document ni aucune information sensible via ces formulaires.</strong>
Les pièces d'un dossier se transmettent lors d'un échange direct, par un moyen sécurisé convenu
ensemble.</p>

<h2>Finalité et base légale</h2>
<div class="table-wrap">
<table>
  <thead><tr><th>Traitement</th><th>Finalité</th><th>Base légale</th><th>Conservation</th></tr></thead>
  <tbody>
    <tr><td>Formulaire de contact</td><td>Répondre à votre demande</td><td>Consentement</td><td>3 ans après le dernier contact</td></tr>
    <tr><td>Demande de rendez-vous</td><td>Organiser le premier échange</td><td>Mesures précontractuelles</td><td>3 ans après le dernier contact</td></tr>
    <tr><td>Relation client</td><td>Exécution de la mission</td><td>Contrat</td><td>Durée légale applicable</td></tr>
  </tbody>
</table>
</div>

<h2>Destinataires</h2>
<p>Vos données sont destinées au seul cabinet {SITE['nom']}. Elles ne sont ni vendues, ni louées,
ni transmises à des tiers à des fins commerciales. Les prestataires techniques intervenant pour
l'hébergement du site ou l'acheminement des messages agissent en qualité de sous-traitants.</p>

<h2>Vos droits</h2>
<p>Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition
et de portabilité sur vos données. Pour les exercer, écrivez à
<a href="mailto:{SITE['email']}">{SITE['email']}</a>. Vous pouvez également introduire une
réclamation auprès de la CNIL — <a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>.</p>

<h2>Cookies et service de réservation</h2>
<p>Ce site ne dépose aucun cookie de mesure d'audience ni de publicité, et n'utilise aucun
traceur publicitaire.</p>
<p>La prise de rendez-vous en ligne repose sur un service externe. Son module est
<strong>chargé en même temps que la page « Rendez-vous »</strong> : dès son ouverture, ce
prestataire reçoit votre adresse IP et peut déposer les cookies nécessaires à son
fonctionnement. Les autres pages du site n'appellent aucun script tiers. Si vous préférez ne
pas y recourir, le téléphone, le courriel et le formulaire de contact restent à votre
disposition.</p>
<p>Lorsque vous choisissez d'afficher le calendrier, les données que vous saisissez pour
réserver (nom, adresse email, téléphone, motif) sont traitées par ce prestataire agissant en
qualité de sous-traitant au sens de l'article 28 du RGPD, aux seules fins d'organiser le
rendez-vous.</p>

<h2>Sécurité</h2>
<p>Le site est servi exclusivement en HTTPS et applique une politique de sécurité du contenu
restrictive : seules les ressources strictement nécessaires peuvent être chargées.</p>
<p>Les échanges liés à un dossier se font par des canaux convenus avec vous et adaptés à la
sensibilité des documents concernés. <strong>Ne transmettez jamais de pièces comptables, de
courriers de l'administration ou de données bancaires via les formulaires de ce site.</strong></p>
<p>Pour signaler une faille de sécurité, écrivez à
<a href="mailto:{SITE['email']}">{SITE['email']}</a> — voir également le fichier
<a href="/.well-known/security.txt">security.txt</a>.</p>
"""
    return page_prose("confidentialite.html", f"Politique de confidentialité — {SITE['nom']}",
                      "Politique de confidentialité", "Données personnelles",
                      f"Politique de confidentialité de {SITE['nom']} : données collectées, "
                      "finalités, durées de conservation et exercice de vos droits.", contenu)


def page_plan():
    exp = "".join(f'<li><a href="expertises/{e["slug"]}.html">{e["titre"]}</a></li>' for e in EXPERTISES)
    contenu = f"""
<h2>Pages principales</h2>
<ul>
  <li><a href="index.html">Accueil</a></li>
  <li><a href="cabinet.html">Le cabinet</a></li>
  <li><a href="methode.html">Notre méthode</a></li>
  <li><a href="procedure-fiscale.html">La procédure fiscale étape par étape</a></li>
  <li><a href="ressources/index.html">Ressources</a></li>
  <li><a href="contact.html">Contact</a></li>
  <li><a href="rendez-vous.html">Prendre rendez-vous</a></li>
</ul>
<h2>Expertises</h2>
<ul><li><a href="expertises/index.html">Toutes nos expertises</a></li>{exp}</ul>
<h2>Informations légales</h2>
<ul>
  <li><a href="mentions-legales.html">Mentions légales</a></li>
  <li><a href="confidentialite.html">Politique de confidentialité</a></li>
</ul>
"""
    return page_prose("plan-du-site.html", seo_titre("Plan du site : toutes les pages"), "Plan du site",
                      "Navigation",
                      "Toutes les pages du site CCF Conseil : expertises, méthode, procédure "
                      "fiscale, ressources, contact et informations légales.", contenu)


def page_404():
    body = f"""{page_head("Erreur 404", "Cette page n'existe pas",
      "Le lien est peut-être erroné, ou la page a été déplacée. Rien n'est perdu : "
      "voici les chemins les plus utiles.")}

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="gap:clamp(36px,6vw,90px);align-items:start">
      <div class="reveal">
        <span class="label label--rule">Où aller</span>
        <h2>Reprendre votre navigation</h2>
        <div class="mt">
          {index_rows([
            ("/expertises/index.html", "Nos expertises", "Les sept pôles d'accompagnement du cabinet."),
            ("/procedure-fiscale.html", "La procédure fiscale", "Les huit étapes et leurs délais."),
            ("/plan-du-site.html", "Plan du site", "Toutes les pages en un coup d'œil."),
          ], niveau=3)}
        </div>
      </div>
      <div class="panel reveal reveal-d2">
        <span class="panel__label">Vous cherchiez à nous joindre&nbsp;?</span>
        <h2>Nous sommes joignables directement</h2>
        <p class="panel__sub">Réservez un créneau, ou écrivez-nous directement.</p>
        <p class="mt-s"><a class="btn btn--primary btn--block" href="/rendez-vous.html">
          {icon('calendar')} Réserver 15 minutes</a></p>
        <p class="panel__alt">{lien_email()}</p>
      </div>
    </div>
  </div>
</section>

{cta("")}
"""
    return layout("404.html", f"Page introuvable — {SITE['nom']}",
                  "La page demandée n'existe pas. Retrouvez les expertises, la procédure fiscale "
                  "et les coordonnées du cabinet.", body, "")


# ---------------------------------------------------------------------------
# Fichiers techniques
# ---------------------------------------------------------------------------
def favicon():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
  <rect width="48" height="48" fill="#0B1B30"/>
  <path d="M24 7.5 39 13v13.5C39 35 32.4 40.6 24 42.6 15.6 40.6 9 35 9 26.5V13z" fill="none" stroke="#C9A961" stroke-width="1.8"/>
  <path d="M24 16v16M18 32h12" stroke="#F3F1EB" stroke-width="1.8" stroke-linecap="round"/>
</svg>
"""


def security_txt():
    """Point de contact pour un signalement de faille (RFC 9116)."""
    from datetime import timedelta
    expire = (date.today() + timedelta(days=365)).isoformat()
    return (f"Contact: mailto:{SITE['email']}\n"
            f"Expires: {expire}T00:00:00.000Z\n"
            "Preferred-Languages: fr, en\n"
            f"Canonical: {SITE['domaine']}/.well-known/security.txt\n")


def sitemap(pages):
    today = date.today().isoformat()
    urls = []
    for p in pages:
        if p == "404.html":
            continue
        loc = SITE["domaine"] + "/" + ("" if p == "index.html" else p)
        prio = "1.0" if p == "index.html" else (
            "0.9" if p.startswith("expertises/") or p == "procedure-fiscale.html" else "0.7")
        freq = "weekly" if p in ("index.html", "ressources/index.html") else "monthly"
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>"
                    f"\n    <changefreq>{freq}</changefreq>"
                    f"\n    <priority>{prio}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def main():
    print("Construction du site CCF Conseil\n")
    produced = []

    def emit(path, html):
        write(path, html)
        produced.append(path)

    emit("index.html", page_accueil())
    emit("cabinet.html", page_cabinet())
    emit("methode.html", page_methode())
    emit("procedure-fiscale.html", page_procedure())
    emit("expertises/index.html", page_expertises_index())
    for e in EXPERTISES:
        emit(f"expertises/{e['slug']}.html", page_expertise(e))
    emit("ressources/index.html", page_ressources())
    emit("contact.html", page_contact())
    emit("rendez-vous.html", page_rdv())
    emit("mentions-legales.html", page_mentions())
    emit("confidentialite.html", page_confidentialite())
    emit("plan-du-site.html", page_plan())
    emit("404.html", page_404())

    write("assets/img/favicon.svg", favicon())
    write(".well-known/security.txt", security_txt())
    write("sitemap.xml", sitemap(produced))
    write("robots.txt",
          f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {SITE['domaine']}/sitemap.xml\n")
    write(".nojekyll", "")
    print(f"\n{len(produced)} pages générées.")


if __name__ == "__main__":
    main()
