#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCF Conseil — générateur de site statique.

Le site livré est du HTML pur : ce script sert uniquement à régénérer les
pages sans dupliquer l'en-tête, le pied de page et les métadonnées à la main.

    python3 build.py

Modifier le contenu : les dictionnaires SITE et PAGES ci-dessous.
"""

import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Configuration du cabinet — à compléter avec les informations réelles
# ---------------------------------------------------------------------------
SITE = {
    "nom": "CCF Conseil",
    "baseline": "Conseil · Fiscalité · Entreprises",
    "signature": "Accompagner · Analyser · Préparer · Coordonner",
    "domaine": "https://www.ccf-conseil.fr",
    "telephone": "01 23 45 67 89",          # À REMPLACER
    "telephone_lien": "+33123456789",       # À REMPLACER
    "email": "contact@ccf-conseil.fr",      # À REMPLACER
    "adresse": "Adresse à compléter",       # À REMPLACER
    "code_postal": "00000",                 # À REMPLACER
    "ville": "Ville à compléter",           # À REMPLACER
    "siren": "SIREN à compléter",           # À REMPLACER
    "forme": "Société à compléter",         # À REMPLACER
    "horaires": "Du lundi au vendredi, 9h – 18h",
    "booking": "#formulaire-rdv",           # Lien de réservation externe le cas échéant
}

ANNEE = date.today().year

# ---------------------------------------------------------------------------
# Icônes (SVG en ligne, 24×24, couleur héritée)
# ---------------------------------------------------------------------------
I = {
"doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/>',
"search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
"users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
"bank": '<path d="M3 21h18M4 10h16M5 10V21M19 10V21M9 10V21M15 10V21M12 2 3 7h18z"/>',
"brief": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/><path d="M2 13h20"/>',
"scale": '<path d="M12 3v18M7 21h10M12 6l-7 2 3 6a3.5 3.5 0 0 0 8 0l-4-8"/><path d="m12 6 7 2-3 6a3.5 3.5 0 0 1-8 0"/>',
"shield": '<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
"clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
"phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
"video": '<rect x="2" y="6" width="14" height="12" rx="2"/><path d="m16 11 6-3v8l-6-3z"/>',
"mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
"pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
"calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 11h18"/>',
"check": '<circle cx="12" cy="12" r="9"/><path d="m8.5 12.2 2.4 2.4 4.6-4.8"/>',
"arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
"alert": '<path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4M12 17.5v.01"/>',
"target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
"hand": '<path d="m11 14-3-3a2 2 0 0 1 3-3l5 5"/><path d="m3 11 4-4 6 6 3-3 5 5-6 6z"/>',
"file-check": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/>',
"menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
"close": '<path d="M6 6l12 12M18 6 6 18"/>',
"lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
}


def icon(name, cls="", size=24):
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" focusable="false">{I[name]}</svg>'
    )


# ---------------------------------------------------------------------------
# Expertises — source unique de vérité
# ---------------------------------------------------------------------------
EXPERTISES = [
    {
        "slug": "conseil-fiscal",
        "nav": "Conseil fiscal",
        "titre": "Conseil fiscal",
        "accroche": "Anticiper pour mieux décider",
        "icone": "doc",
        "resume": "Analyse de votre situation fiscale, identification des points de vigilance et préparation des dossiers.",
        "meta": "Conseil fiscal pour dirigeants et entreprises : analyse de votre situation, identification des risques, préparation et suivi des dossiers. Premier échange de 15 minutes offert.",
        "intro": "Une décision fiscale se prépare rarement dans l'urgence. Analyser la situation en amont, repérer les points sensibles et documenter les choix retenus évite la plupart des difficultés qui surgissent des années plus tard, au moment d'un contrôle.",
        "tags": ["Analyse", "Points de vigilance", "Préparation de dossier"],
        "etapes": [
            ("Analyser la situation", "Lecture de vos documents comptables et fiscaux, compréhension de l'activité et du contexte de l'entreprise."),
            ("Identifier les risques", "Repérage des points susceptibles d'être remis en cause et hiérarchisation selon leur importance."),
            ("Préparer les éléments", "Organisation des pièces justificatives et construction d'un dossier documenté et exploitable."),
            ("Coordonner si nécessaire", "Mobilisation de l'expert-comptable, de l'avocat fiscaliste ou du professionnel compétent selon le dossier."),
        ],
        "points": [
            "Analyse de la situation fiscale de l'entreprise et du dirigeant",
            "Identification des points de vigilance avant qu'ils ne deviennent des litiges",
            "Préparation et organisation des dossiers et des justificatifs",
            "Suivi administratif des échanges avec l'administration",
            "Coordination avec les professionnels compétents lorsque le dossier l'exige",
        ],
        "faq": [
            ("À quel moment faut-il consulter ?", "Le plus tôt possible. Avant une opération importante, avant une cession, avant un changement de structure. Une situation analysée en amont coûte toujours moins cher qu'un dossier repris après une notification."),
            ("Intervenez-vous auprès de l'administration ?", "Nous préparons les dossiers, organisons les pièces et assurons le suivi administratif des échanges. Lorsque la situation appelle une intervention juridique, nous coordonnons l'avocat fiscaliste compétent."),
        ],
    },
    {
        "slug": "controle-fiscal",
        "nav": "Contrôle fiscal",
        "titre": "Contrôle fiscal",
        "accroche": "Vous accompagner à chaque étape",
        "icone": "search",
        "resume": "Analyse des demandes de l'administration, organisation des pièces, préparation du dossier et suivi des échanges.",
        "meta": "Accompagnement en cas de contrôle fiscal : analyse des demandes, organisation des pièces, préparation de la réponse et suivi des délais. Premier échange de 15 minutes offert.",
        "intro": "Un avis de vérification n'est pas une sanction, c'est le début d'une procédure encadrée par des délais stricts. Ce qui fait la différence, c'est la qualité des pièces réunies et la rigueur des réponses apportées dans les temps.",
        "tags": ["Avis de vérification", "Délai de 30 jours", "Préparation de la réponse"],
        "etapes": [
            ("Demande de l'administration", "Lecture attentive de l'avis reçu, identification précise de ce qui est demandé et des exercices concernés."),
            ("Pièces & justificatifs", "Recensement, tri et organisation des documents à produire, en identifiant ce qui manque."),
            ("Préparation du dossier", "Construction d'une réponse argumentée, documentée et complète, point par point."),
            ("Suivi administratif", "Respect des délais, suivi des échanges et préparation des étapes suivantes."),
        ],
        "points": [
            "Analyse de l'avis de vérification et des demandes formulées",
            "Recensement et organisation des pièces justificatives",
            "Préparation des observations dans le délai imparti",
            "Suivi des échanges avec le service vérificateur",
            "Coordination d'un avocat fiscaliste en cas de contentieux",
        ],
        "faq": [
            ("Combien de temps ai-je pour répondre ?", "En principe 30 jours à compter de la réception de la proposition de rectification, avec une prolongation de 30 jours possible sur demande. L'absence de réponse dans ce délai vaut acceptation tacite des rectifications proposées."),
            ("Puis-je répondre moi-même ?", "Rien ne l'interdit. Mais une réponse doit être argumentée, documentée et complète : c'est elle qui fixe le cadre de toute la suite de la procédure. Une réponse improvisée est difficile à rattraper ensuite."),
        ],
    },
    {
        "slug": "controle-urssaf",
        "nav": "Contrôle URSSAF",
        "titre": "Contrôle URSSAF",
        "accroche": "Analyse · Préparation · Suivi",
        "icone": "users",
        "resume": "Étude des documents reçus, préparation des éléments demandés et analyse des observations.",
        "meta": "Accompagnement lors d'un contrôle URSSAF : étude des documents, préparation des éléments demandés, analyse des observations et suivi du redressement. Premier échange offert.",
        "intro": "Le contrôle URSSAF suit sa propre logique et ses propres délais. Les points examinés — frais professionnels, avantages en nature, statut des intervenants, DSN — appellent des justificatifs précis qu'il vaut mieux réunir avant la visite que pendant.",
        "tags": ["Avis de contrôle", "Lettre d'observations", "Mise en demeure"],
        "etapes": [
            ("Documents reçus", "Analyse de l'avis de contrôle et du périmètre annoncé par l'inspecteur."),
            ("Éléments demandés", "Préparation des pièces sociales et de paie attendues, dans la forme demandée."),
            ("Observations", "Étude de la lettre d'observations et préparation d'une réponse motivée."),
            ("Redressement", "Analyse du redressement notifié et préparation des suites, recours compris."),
        ],
        "points": [
            "Analyse de l'avis de contrôle et de son périmètre",
            "Préparation des éléments de paie et des justificatifs sociaux",
            "Réponse argumentée à la lettre d'observations",
            "Analyse de la mise en demeure et des suites possibles",
            "Suivi administratif jusqu'à la clôture du dossier",
        ],
        "faq": [
            ("Quels points sont le plus souvent contrôlés ?", "Les frais professionnels, les avantages en nature, le traitement des indemnités de rupture, le statut des intervenants extérieurs et la cohérence entre la paie et les déclarations sociales."),
            ("Quel délai pour répondre aux observations ?", "En général 30 jours à compter de la réception de la lettre d'observations. Ce délai est court : mieux vaut préparer les éléments pendant le contrôle plutôt qu'après."),
        ],
    },
    {
        "slug": "entreprises-en-difficulte",
        "nav": "Entreprises en difficulté",
        "titre": "Entreprises en difficulté",
        "accroche": "Intervenir avec méthode et anticipation",
        "icone": "shield",
        "resume": "Préparation administrative des dossiers de prévention, de sauvegarde et de redressement judiciaire.",
        "meta": "Accompagnement des entreprises en difficulté : prévention, sauvegarde, redressement judiciaire. Préparation administrative des dossiers et coordination des professionnels compétents.",
        "intro": "Les difficultés d'une entreprise se traitent d'autant mieux qu'elles sont prises tôt. Entre le moment où la trésorerie se tend et celui où la cessation de paiements est constatée, il existe une fenêtre pendant laquelle beaucoup de solutions restent ouvertes.",
        "tags": ["Prévention", "Sauvegarde", "Redressement judiciaire"],
        "etapes": [
            ("Prévention", "Analyse de la situation, préparation des éléments financiers et des demandes de délais."),
            ("Sauvegarde", "Constitution du dossier administratif et organisation des pièces à produire."),
            ("Redressement judiciaire", "Préparation des documents nécessaires et suivi administratif de la procédure."),
        ],
        "points": [
            "Analyse de la situation financière et de son évolution",
            "Préparation des demandes de délais de paiement",
            "Constitution des dossiers de prévention et de sauvegarde",
            "Préparation administrative des documents de procédure",
            "Coordination avec l'avocat et les mandataires, dans les limites légalement autorisées",
        ],
        "faq": [
            ("Est-il trop tard pour agir ?", "Rarement, mais chaque semaine compte. Plus la démarche est engagée tôt, plus les dispositifs de prévention restent accessibles et efficaces."),
            ("Puis-je obtenir un délai de paiement ?", "Une demande écrite et motivée, accompagnée de justificatifs et d'une proposition d'échéancier réaliste, a de bien meilleures chances d'aboutir qu'un simple appel téléphonique."),
        ],
    },
    {
        "slug": "creation-entreprise",
        "nav": "Création d'entreprise",
        "titre": "Création d'entreprise",
        "accroche": "Structurer le projet dès le départ",
        "icone": "brief",
        "resume": "Accompagnement dans les premières étapes du projet : constitution, organisation et préparation des éléments.",
        "meta": "Accompagnement à la création d'entreprise : constitution, organisation administrative, préparation des éléments du projet et coordination des professionnels compétents.",
        "intro": "Les choix faits au moment de la création se paient, dans un sens ou dans l'autre, pendant des années. Structurer le projet dès le départ coûte beaucoup moins cher que de le corriger une fois l'activité lancée.",
        "tags": ["Constitution", "Organisation", "Développement"],
        "etapes": [
            ("Création & constitution", "Analyse du projet et préparation des éléments nécessaires à la constitution."),
            ("Choix et préparation", "Étude des options envisageables et préparation des pièces correspondantes."),
            ("Organisation administrative", "Mise en place des obligations déclaratives et de l'organisation documentaire."),
            ("Coordination", "Mobilisation de l'expert-comptable, du notaire ou du professionnel compétent."),
        ],
        "points": [
            "Analyse du projet et de ses contraintes",
            "Préparation des éléments nécessaires à la constitution",
            "Organisation administrative et déclarative des premiers mois",
            "Accompagnement dans la reprise et la réorganisation d'une activité existante",
            "Coordination avec les professionnels compétents",
        ],
        "faq": [
            ("Vous occupez-vous des formalités ?", "Nous préparons et organisons les éléments du dossier et coordonnons les professionnels compétents pour les actes qui relèvent de leur intervention."),
            ("Intervenez-vous aussi pour une reprise ?", "Oui. La reprise et la réorganisation d'une activité existante font partie du périmètre d'accompagnement."),
        ],
    },
    {
        "slug": "social-paie-dsn",
        "nav": "Social · Paie · DSN",
        "titre": "Social, paie et DSN",
        "accroche": "Accompagnement administratif au quotidien",
        "icone": "users",
        "resume": "Gestion administrative de la paie, préparation et suivi des déclarations sociales et de la DSN.",
        "meta": "Accompagnement administratif en paie et déclarations sociales : préparation des éléments de paie, suivi des déclarations et de la DSN, organisation documentaire.",
        "intro": "La paie et les déclarations sociales ne tolèrent ni approximation ni retard. Une DSN mal préparée se rattrape, mais elle laisse des traces qui ressortent au premier contrôle URSSAF.",
        "tags": ["Paie", "Déclarations sociales", "DSN"],
        "etapes": [
            ("Paie", "Préparation et suivi des éléments nécessaires à la gestion de la paie."),
            ("Déclarations sociales", "Préparation et suivi des déclarations sociales périodiques."),
            ("DSN", "Accompagnement dans la préparation et le suivi des données de la déclaration sociale nominative."),
            ("Suivi administratif", "Organisation des documents et suivi des démarches dans la durée."),
        ],
        "points": [
            "Préparation des éléments variables de paie",
            "Suivi des déclarations sociales périodiques",
            "Accompagnement sur la préparation et le contrôle des DSN",
            "Organisation documentaire et archivage des pièces sociales",
            "Coordination avec l'expert-comptable ou le gestionnaire de paie",
        ],
        "faq": [
            ("Remplacez-vous un gestionnaire de paie ?", "Non. Nous intervenons sur la préparation, l'organisation et le suivi administratif, en lien avec les professionnels compétents lorsque nécessaire."),
            ("Que se passe-t-il en cas d'erreur de DSN ?", "Une anomalie se régularise, mais les écarts répétés entre la paie et les déclarations constituent l'un des premiers points examinés lors d'un contrôle URSSAF."),
        ],
    },
    {
        "slug": "procedures-et-recours",
        "nav": "Procédures & recours",
        "titre": "Procédures et recours",
        "accroche": "Du contrôle jusqu'au contentieux",
        "icone": "scale",
        "resume": "Analyse documentaire et préparation administrative des dossiers de réclamation et de recours.",
        "meta": "Procédures et recours fiscaux : réclamation contentieuse, recours hiérarchique, saisine du tribunal administratif. Préparation des dossiers et coordination d'un avocat fiscaliste.",
        "intro": "Un désaccord avec l'administration n'est pas une impasse. Réclamation, recours hiérarchique, tribunal administratif : chaque voie a ses conditions et surtout ses délais, dont le dépassement est irrattrapable.",
        "tags": ["Réclamation", "Recours hiérarchique", "Tribunal administratif"],
        "etapes": [
            ("Contrôle", "Analyse du dossier et des actes reçus depuis le début de la procédure."),
            ("Rectification", "Étude de la proposition de rectification et préparation des observations."),
            ("Réclamation", "Constitution du dossier de réclamation contentieuse dans les délais."),
            ("Recours", "Préparation du recours hiérarchique et coordination d'un avocat pour la voie juridictionnelle."),
        ],
        "points": [
            "Analyse documentaire complète du dossier",
            "Préparation de la réclamation contentieuse",
            "Préparation du recours hiérarchique",
            "Suivi des délais à chaque étape de la procédure",
            "Coordination d'un avocat fiscaliste pour le recours contentieux",
        ],
        "faq": [
            ("Quel est le délai pour contester ?", "Il varie selon l'acte reçu et l'étape de la procédure. C'est le premier point à vérifier : un délai dépassé ferme définitivement la voie de recours correspondante."),
            ("Faut-il obligatoirement un avocat ?", "Pour la phase administrative, non. Pour le recours contentieux devant le tribunal, l'assistance d'un avocat fiscaliste est vivement recommandée, et nous en assurons la coordination."),
        ],
    },
]

EXP_BY_SLUG = {e["slug"]: e for e in EXPERTISES}

# ---------------------------------------------------------------------------
# Étapes de la procédure fiscale — page pédagogique
# ---------------------------------------------------------------------------
PROCEDURE = [
    ("Réception de la proposition de rectification",
     "L'administration vous adresse par courrier recommandé une proposition de rectification, souvent appelée « 3924 ». Elle détaille les redressements envisagés, leur motif et leur montant.",
     "Délai", "30 jours", "à compter de la réception",
     "alert", "L'absence de réponse dans ce délai vaut acceptation tacite des rectifications proposées. Une prolongation de 30 jours peut être demandée."),
    ("Réponse du contribuable",
     "Vous répondez par écrit en présentant vos observations et en joignant toutes les pièces utiles. C'est l'étape qui fixe le cadre de toute la suite : la réponse doit être argumentée, documentée et complète.",
     "Délai", "30 jours", "prolongeable de 30 jours sur demande",
     "info", "Objectif : convaincre l'administration point par point et éviter tout redressement injustifié."),
    ("Réponse de l'administration",
     "Le service examine vos observations et vous notifie sa position par écrit et de manière motivée. Il peut abandonner, réduire ou maintenir tout ou partie des rectifications.",
     "Délai", "60 jours", "en principe, pour les PME",
     "info", "La réponse est notifiée par courrier motivé. Elle précise ce qui est abandonné et ce qui est maintenu."),
    ("Mise en recouvrement",
     "Les sommes maintenues sont mises en recouvrement. C'est à ce moment que les mesures de recouvrement peuvent être engagées si rien n'est fait.",
     "À savoir", "Sursis", "de paiement possible",
     "alert", "Une demande de sursis de paiement, fondée sur l'article L. 277 du Livre des procédures fiscales, suspend les mesures de recouvrement le temps de la contestation."),
    ("Réclamation contentieuse",
     "Vous adressez une réclamation écrite au service des impôts pour contester les impositions maintenues. C'est le passage obligé avant toute saisine du juge.",
     "Réponse", "6 mois", "délai de réponse de l'administration",
     "info", "L'administration doit répondre de manière explicite et motivée : acceptation, rejet total ou rejet partiel."),
    ("Recours hiérarchique",
     "Voie amiable et facultative : vous demandez le réexamen de votre situation par le supérieur hiérarchique de l'auteur de la décision, puis le cas échéant par l'interlocuteur départemental.",
     "Réponse", "Variable", "voie amiable, sans délai imposé",
     "info", "Cette étape permet souvent de trouver une solution sans aller devant le tribunal."),
    ("Recours contentieux",
     "Si le désaccord persiste, vous saisissez le tribunal administratif. La procédure est écrite et contradictoire, avec des échanges de mémoires et, le cas échéant, une audience.",
     "Délai", "2 mois", "après la décision de rejet, ou après 6 mois de silence",
     "alert", "Passé ce délai, la contestation n'est plus recevable. L'assistance d'un avocat fiscaliste est vivement recommandée à ce stade."),
    ("Décision du tribunal",
     "Le tribunal rend son jugement : il peut rejeter la demande, l'accueillir totalement ou partiellement. Un appel reste possible devant la cour administrative d'appel.",
     "Instruction", "8 à 18 mois", "durée moyenne constatée",
     "info", "Le délai d'appel devant la cour administrative d'appel est en principe de deux mois."),
]

# ---------------------------------------------------------------------------
# Gabarit
# ---------------------------------------------------------------------------
NAV_ITEMS = [
    ("cabinet.html", "Cabinet"),
    ("expertises/index.html", "Expertises"),
    ("methode.html", "Méthode"),
    ("procedure-fiscale.html", "Procédure"),
    ("ressources/index.html", "Ressources"),
    ("contact.html", "Contact"),
]


def rel(path, root):
    """Chemin relatif depuis la profondeur courante."""
    return root + path


def brand_mark():
    return (
        '<svg class="brand__mark" viewBox="0 0 48 48" fill="none" aria-hidden="true">'
        '<path d="M24 3 42 10v13c0 11.5-8.4 19.5-18 22C14.4 42.5 6 34.5 6 23V10z" '
        'fill="none" stroke="#C9A227" stroke-width="2"/>'
        '<path d="M24 12v20M16 32h16M24 16l-6 2 2.6 5.5a3.6 3.6 0 0 0 6.8 0L24 16z" '
        'stroke="#EDF2F8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
        '<path d="m24 16 6 2-2.6 5.5a3.6 3.6 0 0 1-6.8 0" '
        'stroke="#EDF2F8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
        '</svg>'
    )


def header(current, root):
    links = []
    for href, label in NAV_ITEMS:
        aria = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{rel(href, root)}"{aria}>{label}</a>')
    nav_links = "\n          ".join(links)

    return f"""<a class="skip-link" href="#contenu">Aller au contenu principal</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{rel('index.html', root)}" aria-label="{SITE['nom']}, retour à l'accueil">
      {brand_mark()}
      <span class="brand__text">
        <span class="brand__name">CCF<em>&nbsp;Conseil</em></span>
        <span class="brand__tag">{SITE['baseline']}</span>
      </span>
    </a>

    <nav class="nav" id="nav-principal" aria-label="Navigation principale">
      {nav_links}
      <span class="nav__cta">
        <a class="btn btn--gold" href="{rel('rendez-vous.html', root)}">{icon('calendar')} Prendre rendez-vous</a>
      </span>
    </nav>

    <div class="header-cta">
      <a class="header-phone" href="tel:{SITE['telephone_lien']}">{icon('phone')} {SITE['telephone']}</a>
      <a class="btn btn--gold" href="{rel('rendez-vous.html', root)}">{icon('calendar')} Rendez-vous</a>
      <button class="nav-toggle" type="button" aria-expanded="false"
              aria-controls="nav-principal" aria-label="Ouvrir le menu">
        <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">{I['menu']}</svg>
        <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">{I['close']}</svg>
      </button>
    </div>
  </div>
</header>"""


def footer(root):
    exp_links = "\n        ".join(
        f'<li><a href="{rel("expertises/" + e["slug"] + ".html", root)}">{e["nav"]}</a></li>'
        for e in EXPERTISES
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{rel('index.html', root)}">
          {brand_mark()}
          <span class="brand__text">
            <span class="brand__name">CCF<em>&nbsp;Conseil</em></span>
            <span class="brand__tag">{SITE['baseline']}</span>
          </span>
        </a>
        <p>{SITE['signature']}</p>
        <p>Conseil et assistance en matière fiscale, sociale, administrative, financière et de gestion.</p>
      </div>

      <div>
        <h4>Expertises</h4>
        <ul>
        {exp_links}
        </ul>
      </div>

      <div>
        <h4>Le cabinet</h4>
        <ul>
          <li><a href="{rel('cabinet.html', root)}">Notre approche</a></li>
          <li><a href="{rel('methode.html', root)}">Notre méthode</a></li>
          <li><a href="{rel('procedure-fiscale.html', root)}">La procédure fiscale</a></li>
          <li><a href="{rel('ressources/index.html', root)}">Ressources</a></li>
          <li><a href="{rel('contact.html', root)}">Contact</a></li>
        </ul>
      </div>

      <div>
        <h4>Nous joindre</h4>
        <ul>
          <li><a href="tel:{SITE['telephone_lien']}">{SITE['telephone']}</a></li>
          <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
          <li>{SITE['adresse']}<br>{SITE['code_postal']} {SITE['ville']}</li>
          <li>{SITE['horaires']}</li>
        </ul>
        <p style="margin-top:20px">
          <a class="btn btn--gold" href="{rel('rendez-vous.html', root)}">Prendre rendez-vous</a>
        </p>
      </div>
    </div>

    <p class="footer-disclaimer" style="margin-top:36px">
      CCF Conseil exerce une activité de conseil et d'assistance en matière fiscale, sociale,
      administrative, financière et de gestion. Le cabinet n'exerce pas la profession d'avocat
      et intervient dans les limites légalement autorisées, en coordination avec les
      professionnels compétents lorsque la situation l'exige. Les informations publiées sur ce
      site sont fournies à titre général et ne constituent pas une consultation personnalisée.
    </p>

    <div class="footer-legal">
      <span>© <span data-year>{ANNEE}</span> {SITE['nom']}. Tous droits réservés.</span>
      <span>
        <a href="{rel('mentions-legales.html', root)}">Mentions légales</a> ·
        <a href="{rel('confidentialite.html', root)}">Confidentialité</a> ·
        <a href="{rel('plan-du-site.html', root)}">Plan du site</a>
      </span>
    </div>
  </div>
</footer>

<div class="mobile-bar">
  <a class="mb-call" href="tel:{SITE['telephone_lien']}">{icon('phone')} Appeler</a>
  <a class="mb-book" href="{rel('rendez-vous.html', root)}">{icon('calendar')} Rendez-vous</a>
</div>"""


def cta_band(root, titre="Un premier échange de 15 minutes, sans engagement",
             texte="Présentez brièvement votre situation. Nous identifions ensemble la nature du besoin et les prochaines étapes."):
    return f"""<section class="cta-band">
  <div class="container">
    <div class="cta-band__inner">
      <div class="reveal">
        <p class="eyebrow">Prendre rendez-vous</p>
        <h2>{titre}</h2>
        <p>{texte}</p>
      </div>
      <div class="cta-band__actions reveal reveal-d1">
        <a class="btn btn--gold btn--lg" href="{rel('rendez-vous.html', root)}">{icon('calendar')} Réserver un créneau</a>
        <a class="btn btn--ghost-light btn--lg" href="tel:{SITE['telephone_lien']}">{icon('phone')} {SITE['telephone']}</a>
      </div>
    </div>
  </div>
</section>"""


def breadcrumb(items, root):
    lis = []
    for i, (label, href) in enumerate(items):
        last = i == len(items) - 1
        if last or href is None:
            lis.append(f'<li><span aria-current="page">{label}</span></li>')
        else:
            lis.append(f'<li><a href="{rel(href, root)}">{label}</a></li>')
    return f"""<nav class="breadcrumb" aria-label="Fil d'Ariane">
  <div class="container"><ol>{''.join(lis)}</ol></div>
</nav>"""


def layout(page_path, titre, description, body, root="", schema=""):
    canonical = SITE["domaine"] + "/" + page_path.replace("index.html", "")
    canonical = canonical.rstrip("/") + ("/" if page_path.endswith("index.html") else "")
    if page_path == "index.html":
        canonical = SITE["domaine"] + "/"

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0A1A2F">

<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{SITE['nom']}">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">

<link rel="icon" href="{rel('assets/img/favicon.svg', root)}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Manrope:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{rel('assets/css/style.css', root)}">
{schema}
</head>
<body>
{header(page_path, root)}
<main id="contenu">
{body}
</main>
{footer(root)}
<script src="{rel('assets/js/main.js', root)}" defer></script>
</body>
</html>
"""


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("  ✓", path)


# ---------------------------------------------------------------------------
# Données structurées
# ---------------------------------------------------------------------------
SCHEMA_ORG = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "{SITE['nom']}",
  "description": "Conseil et assistance en matière fiscale, sociale, administrative, financière et de gestion.",
  "url": "{SITE['domaine']}",
  "telephone": "{SITE['telephone_lien']}",
  "email": "{SITE['email']}",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{SITE['adresse']}",
    "postalCode": "{SITE['code_postal']}",
    "addressLocality": "{SITE['ville']}",
    "addressCountry": "FR"
  }},
  "areaServed": "FR",
  "priceRange": "€€",
  "knowsAbout": ["Conseil fiscal","Contrôle fiscal","Contrôle URSSAF","Entreprises en difficulté","Création d'entreprise","Paie et DSN","Procédures et recours"]
}}
</script>"""


def faq_schema(pairs):
    items = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (jsonstr(q), jsonstr(a)) for q, a in pairs
    )
    return f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}</script>'


def jsonstr(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"').replace("\n", " ") + '"'


# ---------------------------------------------------------------------------
# Blocs réutilisables
# ---------------------------------------------------------------------------
def form_rdv(root, compact=False, form_id="formulaire-rdv"):
    options = "\n            ".join(
        f'<option value="{e["slug"]}">{e["nav"]}</option>' for e in EXPERTISES
    )
    return f"""<form class="lead-form" data-form id="{form_id}" method="post" action="#" novalidate>
      <div class="hp-field" aria-hidden="true">
        <label for="{form_id}-site">Ne pas remplir</label>
        <input type="text" id="{form_id}-site" name="site" tabindex="-1" autocomplete="off">
      </div>

      <div class="field-row">
        <div class="field">
          <label for="{form_id}-nom">Nom et prénom</label>
          <input type="text" id="{form_id}-nom" name="nom" required autocomplete="name" placeholder="Marie Durand">
        </div>
        <div class="field">
          <label for="{form_id}-tel">Téléphone</label>
          <input type="tel" id="{form_id}-tel" name="telephone" required autocomplete="tel" placeholder="06 12 34 56 78">
        </div>
      </div>

      <div class="field">
        <label for="{form_id}-email">Adresse email</label>
        <input type="email" id="{form_id}-email" name="email" required autocomplete="email" placeholder="marie.durand@entreprise.fr">
      </div>

      <div class="field">
        <label for="{form_id}-motif">Motif de votre demande</label>
        <select id="{form_id}-motif" name="motif" required>
          <option value="">Sélectionnez un motif…</option>
          {options}
          <option value="autre">Autre demande</option>
        </select>
      </div>
      {'' if compact else f'''
      <div class="field">
        <label for="{form_id}-message">Votre situation en quelques lignes</label>
        <textarea id="{form_id}-message" name="message" placeholder="Décrivez brièvement votre situation et, le cas échéant, l'échéance à laquelle vous êtes confronté."></textarea>
      </div>'''}

      <div class="form-consent">
        <input type="checkbox" id="{form_id}-consent" name="consentement" required>
        <label for="{form_id}-consent">
          J'accepte que mes données soient utilisées pour être recontacté au sujet de ma demande.
          <a href="{rel('confidentialite.html', root)}">Politique de confidentialité</a>.
        </label>
      </div>

      <button class="btn btn--gold btn--block btn--lg" type="submit">
        {icon('calendar')} Réserver mon appel
      </button>
      <p class="form-note">Téléphone · 15 minutes · Sans engagement · Réponse sous 24&nbsp;h ouvrées</p>
    </form>"""


def etapes_block(etapes, navy=False):
    cards = []
    for i, (titre, texte) in enumerate(etapes, 1):
        cards.append(f"""<div class="step reveal reveal-d{min(i,4)}">
        <span class="step__n">{i:02d}</span>
        <h3>{titre}</h3>
        <p>{texte}</p>
      </div>""")
    return '<div class="steps">' + "\n      ".join(cards) + "</div>"


def checklist(points):
    lis = "\n        ".join(
        f'<li>{icon("check")}<span>{p}</span></li>' for p in points
    )
    return f'<ul class="checklist">\n        {lis}\n      </ul>'


def faq_block(pairs):
    details = "\n    ".join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
        for i, (q, a) in enumerate(pairs)
    )
    return f'<div class="faq">\n    {details}\n  </div>'


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_accueil():
    pillars = "\n      ".join(
        f"""<a class="pillar" href="expertises/{e['slug']}.html">
        {icon(e['icone'], 'pillar__icon')}
        <h3>{e['nav']}</h3>
        <p>{e['resume'].split('.')[0]}.</p>
      </a>""" for e in EXPERTISES[:5]
    )

    cards = "\n      ".join(
        f"""<a class="card reveal reveal-d{min(i,4)}" href="expertises/{e['slug']}.html">
        {icon(e['icone'], 'card__icon')}
        <h3>{e['titre']}</h3>
        <p>{e['resume']}</p>
        <span class="link-arrow">En savoir plus {icon('arrow')}</span>
      </a>""" for i, e in enumerate(EXPERTISES, 1)
    )

    methode = etapes_block([
        ("Analyser", "Comprendre votre situation, vos documents et le contexte de l'entreprise."),
        ("Identifier", "Repérer les enjeux, les risques et les priorités du dossier."),
        ("Préparer", "Organiser les éléments et construire un dossier exploitable."),
        ("Coordonner", "Mobiliser l'expert-comptable, l'avocat fiscaliste ou le professionnel compétent."),
    ])

    body = f"""<section class="hero">
  <div class="hero__bg"></div>
  <div class="container">
    <div class="hero__inner">
      <div>
        <p class="hero__kicker">{SITE['baseline']}</p>
        <h1>Il est temps<br>d'<span class="accent">agir</span>.</h1>
        <p class="hero__text">
          Face aux difficultés de votre entreprise, chaque étape mérite d'être préparée.
          Un accompagnement clair, structuré et personnalisé pour comprendre votre
          situation et avancer avec méthode.
        </p>
        <div class="hero__actions">
          <a class="btn btn--gold btn--lg" href="#formulaire-rdv">{icon('calendar')} 15 minutes offertes</a>
          <a class="btn btn--ghost-light btn--lg" href="expertises/index.html">Découvrir nos expertises</a>
        </div>
        <div class="hero__trust">
          <span>{icon('lock')} Confidentialité absolue</span>
          <span>{icon('clock')} Réponse sous 24 h ouvrées</span>
          <span>{icon('hand')} Sans engagement</span>
        </div>
      </div>

      <div class="lead-card">
        <span class="lead-card__badge">{icon('clock')} 15 minutes offertes</span>
        <h2>Un premier échange par téléphone</h2>
        <p class="lead-card__sub">
          Faites le point sur votre situation et identifiez les prochaines étapes.
        </p>
        {form_rdv("", compact=True)}
      </div>
    </div>
  </div>
  <div class="hero__rule"></div>
</section>

<section class="pillars">
  <div class="container">
    <div class="pillars__grid">
      {pillars}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Nos expertises</p>
      <h2>Sept pôles pour accompagner l'entreprise</h2>
      <p>
        Fiscalité, contrôles, création, paie, gestion, difficultés et recours.
        Chaque situation appelle une préparation différente.
      </p>
    </div>
    <div class="grid grid--3">
      {cards}
      <a class="card card--navy card--hover reveal reveal-d4" href="contact.html">
        {icon('hand', 'card__icon')}
        <h3>Votre situation n'entre dans aucune case ?</h3>
        <p>C'est fréquent. Décrivez-la nous en quelques lignes, nous vous dirons si nous sommes le bon interlocuteur.</p>
        <span class="link-arrow" style="color:var(--gold-300)">Nous écrire {icon('arrow')}</span>
      </a>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Notre méthode</p>
      <h2>Une démarche structurée en quatre étapes</h2>
      <p>
        Une méthode lisible pour comprendre les enjeux et construire un dossier
        qui tient devant l'administration.
      </p>
    </div>
    {methode}
    <p class="mt-lg"><a class="btn btn--ghost-light" href="methode.html">Voir la méthode en détail {icon('arrow')}</a></p>
  </div>
</section>

<section class="section section--paper2">
  <div class="container">
    <div class="grid grid--2" style="align-items:center">
      <div class="reveal">
        <p class="eyebrow">Comprendre la procédure</p>
        <h2>Chaque étape a un délai. Le dépasser vous coûte vos droits.</h2>
        <p class="lede mt-lg">
          De la proposition de rectification jusqu'au tribunal administratif, la procédure
          fiscale suit un calendrier strict. Nous l'avons détaillée étape par étape, avec
          les délais applicables à chacune.
        </p>
        <p class="mt-lg">
          <a class="btn btn--navy btn--lg" href="procedure-fiscale.html">
            Voir la procédure étape par étape {icon('arrow')}
          </a>
        </p>
      </div>
      <div class="stack reveal reveal-d2">
        <div class="card card--hover">
          <span class="card__num">30 jours</span>
          <h3>Pour répondre à une proposition de rectification</h3>
          <p>Passé ce délai, l'absence de réponse vaut acceptation tacite des redressements proposés.</p>
        </div>
        <div class="card card--hover">
          <span class="card__num">6 mois</span>
          <h3>Pour la réponse à une réclamation contentieuse</h3>
          <p>L'administration doit répondre de manière explicite et motivée.</p>
        </div>
        <div class="card card--hover">
          <span class="card__num">2 mois</span>
          <h3>Pour saisir le tribunal administratif</h3>
          <p>Après la décision de rejet, ou après six mois de silence de l'administration.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Le cabinet</p>
      <h2>Une approche globale et personnalisée</h2>
      <p>Conseil et assistance en matière fiscale, sociale, administrative, financière et de gestion.</p>
    </div>
    <div class="grid grid--3">
      <div class="card card--hover reveal">
        {icon('lock', 'card__icon')}
        <h3>Confidentialité</h3>
        <p>Vos documents et votre situation restent strictement confidentiels. C'est la condition d'un échange utile.</p>
      </div>
      <div class="card card--hover reveal reveal-d1">
        {icon('target', 'card__icon')}
        <h3>Anticipation</h3>
        <p>Prévenir les risques et sécuriser les décisions avant qu'une échéance ne les impose.</p>
      </div>
      <div class="card card--hover reveal reveal-d2">
        {icon('users', 'card__icon')}
        <h3>Coordination</h3>
        <p>Un réseau de professionnels mobilisés selon les besoins réels de votre dossier.</p>
      </div>
    </div>
  </div>
</section>

{cta_band("")}
"""
    return layout(
        "index.html",
        "CCF Conseil — Conseil fiscal, contrôles et accompagnement des entreprises",
        "Cabinet de conseil et d'assistance en matière fiscale, sociale et administrative. "
        "Contrôle fiscal, contrôle URSSAF, entreprises en difficulté, création, paie et DSN. "
        "Premier échange de 15 minutes offert.",
        body, "", SCHEMA_ORG,
    )


def page_expertise(e):
    root = "../"
    autres = [x for x in EXPERTISES if x["slug"] != e["slug"]][:3]
    autres_cards = "\n      ".join(
        f"""<a class="card reveal reveal-d{i}" href="{a['slug']}.html">
        {icon(a['icone'], 'card__icon')}
        <h3>{a['titre']}</h3>
        <p>{a['resume']}</p>
        <span class="link-arrow">En savoir plus {icon('arrow')}</span>
      </a>""" for i, a in enumerate(autres, 1)
    )
    tags = "".join(f'<span class="tag">{t}</span>' for t in e["tags"])

    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">Expertise</p>
      <h1>{e['titre']}</h1>
      <p>{e['accroche']} — {e['resume']}</p>
      <div class="page-hero__tags">{tags}</div>
    </div>
  </div>
</section>

{breadcrumb([("Accueil", "index.html"), ("Expertises", "expertises/index.html"), (e['titre'], None)], root)}

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="align-items:start;gap:clamp(28px,4vw,56px)">
      <div class="reveal">
        <p class="eyebrow">Le contexte</p>
        <h2>{e['accroche']}</h2>
        <p class="lede mt-lg">{e['intro']}</p>
        <hr class="divider">
        <h3 class="mb-lg">Ce que nous prenons en charge</h3>
        {checklist(e['points'])}
      </div>
      <div class="lead-card reveal reveal-d2">
        <span class="lead-card__badge">{icon('clock')} 15 minutes offertes</span>
        <h2>Parlons de votre dossier</h2>
        <p class="lead-card__sub">
          Un premier échange téléphonique pour comprendre votre situation
          et identifier l'accompagnement adapté.
        </p>
        {form_rdv(root, compact=True, form_id="rdv-" + e['slug'])}
      </div>
    </div>
  </div>
</section>

<section class="section section--paper2">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Déroulé</p>
      <h2>Comment nous procédons</h2>
    </div>
    {etapes_block(e['etapes'])}
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div class="section-head reveal">
      <p class="eyebrow">Questions fréquentes</p>
      <h2>Ce que l'on nous demande le plus souvent</h2>
    </div>
    {faq_block(e['faq'])}
  </div>
</section>

<section class="section section--paper2">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Autres expertises</p>
      <h2>Poursuivre votre lecture</h2>
    </div>
    <div class="grid grid--3">
      {autres_cards}
    </div>
  </div>
</section>

{cta_band(root)}
"""
    return layout(
        f"expertises/{e['slug']}.html",
        f"{e['titre']} — {SITE['nom']}",
        e["meta"],
        body, root, faq_schema(e["faq"]),
    )


def page_expertises_index():
    root = "../"
    cards = "\n      ".join(
        f"""<a class="card reveal reveal-d{min(i,4)}" href="{e['slug']}.html">
        {icon(e['icone'], 'card__icon')}
        <span class="card__num">{i:02d}</span>
        <h3>{e['titre']}</h3>
        <p>{e['resume']}</p>
        <span class="link-arrow">En savoir plus {icon('arrow')}</span>
      </a>""" for i, e in enumerate(EXPERTISES, 1)
    )
    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">Nos expertises</p>
      <h1>Sept pôles pour accompagner l'entreprise</h1>
      <p>
        Fiscalité, contrôles, création, paie, gestion, difficultés et recours.
        Chaque situation appelle une préparation différente et un calendrier propre.
      </p>
    </div>
  </div>
</section>

{breadcrumb([("Accueil", "index.html"), ("Expertises", None)], root)}

<section class="section">
  <div class="container">
    <div class="grid grid--3">
      {cards}
    </div>
  </div>
</section>

{cta_band(root)}
"""
    return layout(
        "expertises/index.html",
        f"Nos expertises — {SITE['nom']}",
        "Les sept pôles d'expertise de CCF Conseil : conseil fiscal, contrôle fiscal, contrôle URSSAF, "
        "entreprises en difficulté, création d'entreprise, social et paie, procédures et recours.",
        body, root,
    )


def page_cabinet():
    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">Le cabinet</p>
      <h1>Une approche globale et personnalisée</h1>
      <p>
        Conseil et assistance en matière fiscale, sociale, administrative, financière
        et de gestion, pour les dirigeants, les entreprises et les entrepreneurs.
      </p>
    </div>
  </div>
</section>

{breadcrumb([("Accueil", "index.html"), ("Le cabinet", None)], "")}

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="gap:clamp(28px,4vw,56px);align-items:start">
      <div class="reveal">
        <p class="eyebrow">Notre positionnement</p>
        <h2>Comprendre avant de décider</h2>
        <p class="lede mt-lg">
          La plupart des dossiers qui arrivent au cabinet ont un point commun : ils ont
          commencé par une lettre ouverte trop tard, ou par une décision prise sans en
          avoir mesuré les conséquences.
        </p>
        <p>
          Notre rôle est d'abord de comprendre la situation réelle de l'entreprise, puis
          d'identifier ce qui est en jeu, de préparer les éléments nécessaires et, lorsque
          le dossier l'exige, de mobiliser le professionnel compétent.
        </p>
        <p>
          Nous n'exerçons pas la profession d'avocat. Nous intervenons sur l'analyse, la
          préparation administrative des dossiers et la coordination, dans les limites
          légalement autorisées. C'est un périmètre clair, et c'est aussi ce qui nous permet
          de travailler efficacement aux côtés des avocats fiscalistes et des
          experts-comptables plutôt qu'en concurrence avec eux.
        </p>
      </div>
      <div class="stack reveal reveal-d2">
        <div class="card card--hover">
          {icon('lock', 'card__icon')}
          <h3>Confidentialité</h3>
          <p>
            Les situations que nous traitons touchent au plus sensible de la vie d'une
            entreprise. Vos documents et vos échanges restent strictement confidentiels.
          </p>
        </div>
        <div class="card card--hover">
          {icon('target', 'card__icon')}
          <h3>Anticipation</h3>
          <p>
            Prévenir les risques et sécuriser les décisions avant qu'une échéance ne les
            impose. Un dossier préparé se défend toujours mieux qu'un dossier subi.
          </p>
        </div>
        <div class="card card--hover">
          {icon('users', 'card__icon')}
          <h3>Coordination</h3>
          <p>
            Expert-comptable, avocat fiscaliste, mandataire : nous mobilisons le bon
            interlocuteur au bon moment, et nous assurons le lien entre eux.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Périmètre d'intervention</p>
      <h2>Ce que recouvre notre activité</h2>
      <p>Un champ d'intervention défini par notre objet social, appliqué sans ambiguïté.</p>
    </div>
    <div class="grid grid--2">
      <div class="reveal">
        {checklist([
          "Conseil, assistance et prestations de services en matière fiscale, sociale, administrative, financière et de gestion",
          "Assistance à la création, la constitution, la reprise, l'organisation et le développement des entreprises",
          "Gestion administrative de la paie, préparation et suivi des déclarations sociales et fiscales",
        ])}
      </div>
      <div class="reveal reveal-d2">
        {checklist([
          "Conseil et assistance dans le cadre des contrôles fiscaux, contrôles URSSAF et procédures administratives",
          "Conseil et assistance aux entreprises en difficulté : prévention, sauvegarde, redressement judiciaire, dans les limites légalement autorisées",
          "Analyse, préparation de dossiers et de documents, assistance administrative",
        ])}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container container--narrow">
    <div class="section-head reveal">
      <p class="eyebrow">Questions fréquentes</p>
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

{cta_band("")}
"""
    return layout(
        "cabinet.html",
        f"Le cabinet — {SITE['nom']}",
        "CCF Conseil : cabinet de conseil et d'assistance en matière fiscale, sociale et administrative. "
        "Confidentialité, anticipation, coordination des professionnels compétents.",
        body, "",
    )


def page_methode():
    detail = [
        ("Analyser",
         "Comprendre votre situation et vos documents",
         "Nous partons de ce qui existe : vos documents comptables et fiscaux, les courriers reçus, l'historique de l'entreprise. Cette lecture prend du temps et c'est normal : un dossier mal compris au départ se défend mal ensuite.",
         ["Lecture des documents comptables et fiscaux", "Analyse des courriers et actes reçus", "Compréhension de l'activité et du contexte", "Identification des pièces manquantes"]),
        ("Identifier",
         "Repérer les enjeux, les risques et les priorités",
         "Tous les points d'un dossier n'ont pas le même poids. Nous distinguons ce qui est solide de ce qui est fragile, ce qui est urgent de ce qui peut attendre, et ce qui relève de notre périmètre de ce qui appelle un autre professionnel.",
         ["Hiérarchisation des points de vigilance", "Identification des délais applicables", "Évaluation des suites possibles", "Définition de la stratégie de réponse"]),
        ("Préparer",
         "Organiser les éléments et construire le dossier",
         "Un dossier exploitable est un dossier où chaque affirmation est justifiée par une pièce. C'est la partie la plus longue du travail, et celle qui fait la différence devant l'administration.",
         ["Collecte et organisation des justificatifs", "Rédaction des observations argumentées", "Construction d'un dossier structuré", "Respect strict des délais"]),
        ("Coordonner",
         "Mobiliser le professionnel compétent",
         "Certaines étapes relèvent de l'avocat, du notaire ou de l'expert-comptable. Nous les mobilisons au bon moment, avec un dossier déjà préparé — ce qui réduit leur temps d'intervention, donc leur coût.",
         ["Mise en relation avec l'avocat fiscaliste", "Lien avec l'expert-comptable", "Transmission d'un dossier prêt à l'emploi", "Suivi coordonné jusqu'à la clôture"]),
    ]
    blocks = []
    for i, (titre, sous, texte, points) in enumerate(detail, 1):
        blocks.append(f"""<div class="tl-item reveal">
      <span class="tl-item__dot">{i:02d}</span>
      <div class="tl-item__body" style="grid-template-columns:1fr">
        <div>
          <p class="eyebrow" style="margin-bottom:8px">{titre}</p>
          <h3>{sous}</h3>
          <p>{texte}</p>
          <div class="mt-lg">{checklist(points)}</div>
        </div>
      </div>
    </div>""")

    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">Notre méthode</p>
      <h1>Une démarche structurée en quatre étapes</h1>
      <p>
        Une méthode lisible pour comprendre les enjeux, construire un dossier exploitable
        et savoir à chaque instant où en est la procédure.
      </p>
      <div class="page-hero__tags">
        <span class="tag">Analyser</span><span class="tag">Identifier</span>
        <span class="tag">Préparer</span><span class="tag">Coordonner</span>
      </div>
    </div>
  </div>
</section>

{breadcrumb([("Accueil", "index.html"), ("Notre méthode", None)], "")}

<section class="section">
  <div class="container">
    <div class="timeline">
      {''.join(blocks)}
    </div>
  </div>
</section>

{cta_band("")}
"""
    return layout(
        "methode.html",
        f"Notre méthode — {SITE['nom']}",
        "La méthode CCF Conseil en quatre étapes : analyser la situation, identifier les enjeux, "
        "préparer le dossier, coordonner les professionnels compétents.",
        body, "",
    )


def page_procedure():
    items = []
    for i, (titre, texte, label, valeur, source, ton, note) in enumerate(PROCEDURE, 1):
        cls = "callout callout--alert" if ton == "alert" else "callout"
        prefix = "Attention" if ton == "alert" else "À savoir"
        items.append(f"""<div class="tl-item reveal">
      <span class="tl-item__dot">{i:02d}</span>
      <div class="tl-item__body">
        <div>
          <h3>{titre}</h3>
          <p>{texte}</p>
          <div class="{cls}"><strong>{prefix} :</strong> {note}</div>
        </div>
        <div class="delay">
          <div class="delay__label">{label}</div>
          <div class="delay__value">{valeur}</div>
          <div class="delay__from">{source}</div>
        </div>
      </div>
    </div>""")

    faq = [
        ("Que se passe-t-il si je ne réponds pas dans les 30 jours ?",
         "L'absence de réponse dans le délai vaut acceptation tacite des rectifications proposées. Les sommes deviennent exigibles et la contestation devient nettement plus difficile."),
        ("Puis-je demander un délai supplémentaire ?",
         "Oui. Une prolongation de trente jours peut être demandée pour répondre à une proposition de rectification. La demande doit être formulée dans le délai initial."),
        ("Comment suspendre les mesures de recouvrement ?",
         "Par une demande de sursis de paiement fondée sur l'article L. 277 du Livre des procédures fiscales, présentée avec la réclamation. Elle suspend le recouvrement des sommes contestées, l'administration pouvant demander des garanties."),
        ("Le recours hiérarchique est-il obligatoire ?",
         "Non, il est facultatif. C'est une voie amiable qui permet souvent de trouver une solution sans saisir le tribunal, sans faire perdre le bénéfice des autres recours."),
    ]

    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">Comprendre la procédure</p>
      <h1>La procédure fiscale, étape par étape</h1>
      <p>
        De la proposition de rectification jusqu'à la décision du tribunal administratif :
        chaque étape a un délai. Le dépasser, c'est perdre le droit de contester.
      </p>
      <div class="page-hero__tags">
        <span class="tag">30 jours pour répondre</span>
        <span class="tag">6 mois de réponse</span>
        <span class="tag">2 mois pour saisir le juge</span>
      </div>
    </div>
  </div>
</section>

{breadcrumb([("Accueil", "index.html"), ("La procédure fiscale", None)], "")}

<section class="section section--tight">
  <div class="container container--narrow">
    <div class="callout callout--alert reveal">
      <strong>Les délais indiqués sont ceux applicables dans les cas les plus courants.</strong>
      Ils varient selon la nature du contrôle, la procédure engagée et votre situation.
      Cette page est un repère pédagogique : elle ne remplace pas l'analyse de votre dossier.
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="timeline">
      {''.join(items)}
    </div>
  </div>
</section>

<section class="section section--paper2">
  <div class="container container--narrow">
    <div class="section-head reveal">
      <p class="eyebrow">Questions fréquentes</p>
      <h2>Les délais et les recours</h2>
    </div>
    {faq_block(faq)}
  </div>
</section>

{cta_band("", "Vous avez reçu un courrier de l'administration ?",
  "Le premier réflexe utile est de vérifier la date de réception et le délai de réponse. Appelez-nous, nous le regardons ensemble.")}
"""
    return layout(
        "procedure-fiscale.html",
        f"La procédure fiscale étape par étape : délais et recours — {SITE['nom']}",
        "Proposition de rectification, réponse du contribuable, réclamation contentieuse, recours "
        "hiérarchique, tribunal administratif : toutes les étapes de la procédure fiscale et les "
        "délais à respecter, expliqués simplement.",
        body, "", faq_schema(faq),
    )


def page_ressources():
    root = "../"
    articles = [
        ("procedure-fiscale.html", "Guide", "La procédure fiscale étape par étape",
         "Les huit étapes de la procédure, de la proposition de rectification au tribunal administratif, avec le délai applicable à chacune.", True),
        (None, "Fiche pratique", "Contrôle fiscal : les cinq réflexes des premières 48 heures",
         "Vérifier la date de réception, identifier les exercices visés, rassembler les pièces, poser le calendrier, appeler un professionnel.", False),
        (None, "Fiche pratique", "Sursis de paiement : suspendre les saisies pendant la contestation",
         "Ce que permet l'article L. 277 du Livre des procédures fiscales, comment formuler la demande et quelles pièces y joindre.", False),
        (None, "Fiche pratique", "Contrôle URSSAF : les points les plus souvent redressés",
         "Frais professionnels, avantages en nature, indemnités de rupture, statut des intervenants extérieurs et cohérence des DSN.", False),
        (None, "Fiche pratique", "Difficultés de trésorerie : demander un délai de paiement",
         "Comment construire une demande motivée et proposer un échéancier réaliste qui a des chances d'être accepté.", False),
        (None, "Fiche pratique", "Créer son entreprise : les décisions qui coûtent cher plus tard",
         "Les choix structurants des premiers mois et leurs conséquences fiscales et sociales dans la durée.", False),
    ]
    cards = []
    for i, (href, cat, titre, texte, dispo) in enumerate(articles, 1):
        if dispo:
            cards.append(f"""<a class="card reveal reveal-d{min(i,4)}" href="{rel(href, root)}">
        <span class="card__num">{cat}</span>
        <h3>{titre}</h3>
        <p>{texte}</p>
        <span class="link-arrow">Lire le guide {icon('arrow')}</span>
      </a>""")
        else:
            cards.append(f"""<article class="card reveal reveal-d{min(i,4)}" style="opacity:.72">
        <span class="card__num">{cat}</span>
        <h3>{titre}</h3>
        <p>{texte}</p>
        <span class="link-arrow" style="color:var(--ink-3)">Bientôt disponible</span>
      </article>""")

    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">Ressources</p>
      <h1>Comprendre avant de subir</h1>
      <p>
        Des repères clairs sur les procédures fiscales et sociales, écrits pour des dirigeants
        qui n'ont ni le temps ni l'envie de lire le Livre des procédures fiscales.
      </p>
    </div>
  </div>
</section>

{breadcrumb([("Accueil", "index.html"), ("Ressources", None)], root)}

<section class="section">
  <div class="container">
    <div class="grid grid--3">
      {''.join(cards)}
    </div>
  </div>
</section>

{cta_band(root)}
"""
    return layout(
        "ressources/index.html",
        f"Ressources — {SITE['nom']}",
        "Guides et fiches pratiques sur le contrôle fiscal, le contrôle URSSAF, les délais de "
        "procédure, le sursis de paiement et les difficultés d'entreprise.",
        body, root,
    )


def page_contact():
    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">Contact</p>
      <h1>Prenons le temps d'analyser votre situation</h1>
      <p>
        Un premier échange pour comprendre votre besoin et identifier l'accompagnement adapté.
        Par téléphone, en visioconférence ou au cabinet.
      </p>
    </div>
  </div>
</section>

{breadcrumb([("Accueil", "index.html"), ("Contact", None)], "")}

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="gap:clamp(28px,4vw,56px);align-items:start">
      <div class="reveal">
        <p class="eyebrow">Nous joindre</p>
        <h2>Trois façons d'échanger</h2>
        <div class="grid mt-lg" style="gap:16px">
          <div class="card card--hover">
            {icon('phone', 'card__icon')}
            <h3>Par téléphone</h3>
            <p>Le plus direct, surtout en cas d'échéance proche.</p>
            <p><a class="link-arrow" href="tel:{SITE['telephone_lien']}">{SITE['telephone']} {icon('arrow')}</a></p>
          </div>
          <div class="card card--hover">
            {icon('video', 'card__icon')}
            <h3>En visioconférence</h3>
            <p>Pratique pour passer en revue des documents ensemble, où que vous soyez.</p>
          </div>
          <div class="card card--hover">
            {icon('pin', 'card__icon')}
            <h3>Au cabinet</h3>
            <p>{SITE['adresse']}<br>{SITE['code_postal']} {SITE['ville']}</p>
            <p>{SITE['horaires']}</p>
          </div>
        </div>
      </div>

      <div class="lead-card reveal reveal-d2">
        <span class="lead-card__badge">{icon('mail')} Formulaire de contact</span>
        <h2>Décrivez votre situation</h2>
        <p class="lead-card__sub">
          Nous vous répondons sous 24 heures ouvrées. Si la situation est urgente,
          privilégiez le téléphone.
        </p>
        {form_rdv("", compact=False, form_id="contact")}
      </div>
    </div>
  </div>
</section>

{cta_band("")}
"""
    return layout(
        "contact.html",
        f"Contact — {SITE['nom']}",
        "Contactez CCF Conseil par téléphone, en visioconférence ou au cabinet. "
        "Premier échange de 15 minutes offert, sans engagement.",
        body, "",
    )


def page_rdv():
    formats = [
        ("phone", "Par téléphone", "Le format le plus simple et le plus rapide. Nous vous appelons au numéro indiqué."),
        ("video", "En visioconférence", "Utile pour examiner ensemble des documents pendant l'échange."),
        ("pin", "Au cabinet", "Sur rendez-vous, pour les dossiers qui méritent un examen approfondi."),
    ]
    cards = "\n      ".join(
        f"""<div class="card card--hover reveal reveal-d{i}">
        {icon(ic, 'card__icon')}
        <h3>{t}</h3>
        <p>{d}</p>
      </div>""" for i, (ic, t, d) in enumerate(formats, 1)
    )

    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">Rendez-vous</p>
      <h1>15 minutes offertes pour faire le point</h1>
      <p>
        Un échange préalable, sans engagement, pour présenter brièvement votre situation
        et déterminer la nature de votre besoin.
      </p>
      <div class="page-hero__tags">
        <span class="tag">15 minutes</span><span class="tag">Sans engagement</span>
        <span class="tag">Confidentiel</span>
      </div>
    </div>
  </div>
</section>

{breadcrumb([("Accueil", "index.html"), ("Rendez-vous", None)], "")}

<section class="section">
  <div class="container">
    <div class="grid grid--2" style="gap:clamp(28px,4vw,56px);align-items:start">
      <div class="reveal">
        <p class="eyebrow">Comment ça se passe</p>
        <h2>Trois étapes, et c'est réglé</h2>
        <div class="mt-lg">{checklist([
          "Vous indiquez vos coordonnées et le motif de votre demande.",
          "Vous choisissez un créneau parmi les disponibilités réelles du cabinet.",
          "Vous recevez immédiatement une confirmation par email, avec le rendez-vous dans votre agenda.",
        ])}</div>

        <hr class="divider">

        <h3 class="mb-lg">Le format de l'échange</h3>
        <div class="grid" style="gap:16px">
          {cards}
        </div>

        <div class="callout mt-lg">
          <strong>Ce que nous vous dirons pendant ces quinze minutes :</strong>
          si votre situation relève de notre périmètre, quelles sont les échéances à
          surveiller en priorité, et quel professionnel mobiliser si ce n'est pas nous.
        </div>
      </div>

      <div class="lead-card reveal reveal-d2" id="reserver">
        <span class="lead-card__badge">{icon('calendar')} Réserver un créneau</span>
        <h2>Votre demande de rendez-vous</h2>
        <p class="lead-card__sub">
          Renseignez vos coordonnées, nous vous confirmons le créneau par email.
        </p>
        {form_rdv("", compact=False, form_id="rdv")}
      </div>
    </div>
  </div>
</section>

<!--
  ════════════════════════════════════════════════════════════════════════════
  INTÉGRATION DE L'AGENDA EN LIGNE
  ────────────────────────────────────────────────────────────────────────────
  Le formulaire ci-dessus est la version sans dépendance externe.
  Pour activer la réservation synchronisée avec l'agenda du cabinet, remplacer
  le bloc .lead-card par le widget du service de réservation retenu, en
  conservant la pré-sélection du motif via le paramètre ?motif=<slug>.
  Les slugs disponibles sont ceux des pages d'expertise.
  ════════════════════════════════════════════════════════════════════════════
-->
"""
    return layout(
        "rendez-vous.html",
        f"Prendre rendez-vous — 15 minutes offertes — {SITE['nom']}",
        "Réservez un premier échange de 15 minutes avec CCF Conseil, par téléphone, "
        "en visioconférence ou au cabinet. Sans engagement.",
        body, "",
    )


def page_prose(path, titre, h1, eyebrow, description, contenu):
    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
    </div>
  </div>
</section>

{breadcrumb([("Accueil", "index.html"), (h1, None)], "")}

<section class="section">
  <div class="container">
    <div class="prose">
      {contenu}
    </div>
  </div>
</section>
"""
    return layout(path, titre, description, body, "")


def page_mentions():
    contenu = f"""
<h2>Éditeur du site</h2>
<p>
  {SITE['nom']} — {SITE['forme']}<br>
  Siège social : {SITE['adresse']}, {SITE['code_postal']} {SITE['ville']}<br>
  SIREN : {SITE['siren']}<br>
  Téléphone : <a href="tel:{SITE['telephone_lien']}">{SITE['telephone']}</a><br>
  Courriel : <a href="mailto:{SITE['email']}">{SITE['email']}</a>
</p>
<p><em>Directeur de la publication, numéro de TVA intracommunautaire, capital social et
assurance de responsabilité civile professionnelle : à compléter avant mise en ligne.</em></p>

<h2>Hébergement</h2>
<p>
  Le site est hébergé par GitHub&nbsp;Inc., 88 Colin P. Kelly Jr. Street, San Francisco,
  CA 94107, États-Unis — <a href="https://github.com" rel="noopener">github.com</a>.
</p>

<h2>Nature de l'activité</h2>
<p>
  {SITE['nom']} exerce une activité de conseil, d'assistance et de prestations de services
  en matière fiscale, sociale, administrative, financière et de gestion. Le cabinet
  n'exerce pas la profession d'avocat et n'assure aucune représentation devant les
  juridictions. Il intervient dans les limites légalement autorisées et coordonne, lorsque
  la situation l'exige, les professionnels compétents — avocat fiscaliste, expert-comptable,
  notaire ou mandataire.
</p>

<h2>Propriété intellectuelle</h2>
<p>
  L'ensemble des contenus présents sur ce site — textes, illustrations, éléments graphiques,
  structure — est protégé par le droit de la propriété intellectuelle. Toute reproduction ou
  représentation, totale ou partielle, sans autorisation écrite préalable est interdite.
</p>

<h2>Informations publiées</h2>
<p>
  Les informations diffusées sur ce site ont une vocation générale et pédagogique. Elles ne
  constituent pas une consultation personnalisée et ne sauraient se substituer à l'analyse
  d'une situation particulière. Les délais et procédures mentionnés correspondent aux cas les
  plus courants et peuvent varier selon la nature du dossier.
</p>

<h2>Responsabilité</h2>
<p>
  {SITE['nom']} met tout en œuvre pour assurer l'exactitude des informations publiées mais ne
  peut garantir leur exhaustivité ni leur actualité permanente. La responsabilité de l'éditeur
  ne saurait être engagée en cas d'usage de ces informations sans analyse préalable de la
  situation concernée.
</p>

<h2>Liens</h2>
<p>
  Ce site peut contenir des liens vers des sites tiers. {SITE['nom']} n'exerce aucun contrôle
  sur leur contenu et décline toute responsabilité à leur égard.
</p>

<h2>Droit applicable</h2>
<p>Le présent site est soumis au droit français.</p>
"""
    return page_prose("mentions-legales.html", f"Mentions légales — {SITE['nom']}",
                      "Mentions légales", "Informations légales",
                      f"Mentions légales du site {SITE['nom']} : éditeur, hébergement, propriété intellectuelle et responsabilité.",
                      contenu)


def page_confidentialite():
    contenu = f"""
<p class="lede">
  Cette page décrit la manière dont {SITE['nom']} traite les données personnelles collectées
  sur ce site, conformément au Règlement général sur la protection des données (RGPD) et à
  la loi Informatique et Libertés.
</p>

<h2>Responsable du traitement</h2>
<p>
  {SITE['nom']}, {SITE['adresse']}, {SITE['code_postal']} {SITE['ville']} —
  <a href="mailto:{SITE['email']}">{SITE['email']}</a>.
</p>

<h2>Données collectées</h2>
<p>
  Les formulaires de contact et de demande de rendez-vous collectent uniquement les données
  nécessaires au traitement de votre demande : nom et prénom, numéro de téléphone, adresse
  email, motif de la demande et, le cas échéant, la description que vous rédigez librement.
</p>
<p>
  <strong>Ne communiquez aucun document ni aucune information sensible via ces formulaires.</strong>
  Les pièces d'un dossier se transmettent lors d'un échange direct, par un moyen sécurisé
  convenu ensemble.
</p>

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
<p>
  Vos données sont destinées au seul cabinet {SITE['nom']}. Elles ne sont ni vendues, ni louées,
  ni transmises à des tiers à des fins commerciales. Les prestataires techniques intervenant
  pour l'hébergement du site ou l'acheminement des messages agissent en qualité de
  sous-traitants, dans le cadre d'un contrat conforme à l'article 28 du RGPD.
</p>

<h2>Vos droits</h2>
<p>
  Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition
  et de portabilité sur vos données. Pour les exercer, écrivez à
  <a href="mailto:{SITE['email']}">{SITE['email']}</a>. Vous pouvez également introduire une
  réclamation auprès de la CNIL — <a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>.
</p>

<h2>Cookies</h2>
<p>
  Ce site ne dépose aucun cookie de mesure d'audience ni de publicité. Aucune bannière de
  consentement n'est donc nécessaire. Si un outil de réservation externe est intégré
  ultérieurement, cette page sera mise à jour et le consentement recueilli avant tout dépôt
  de cookie non essentiel.
</p>

<h2>Sécurité</h2>
<p>
  Le site est servi exclusivement en HTTPS. Les échanges liés à un dossier se font par des
  canaux convenus avec vous et adaptés à la sensibilité des documents concernés.
</p>
"""
    return page_prose("confidentialite.html", f"Politique de confidentialité — {SITE['nom']}",
                      "Politique de confidentialité", "Données personnelles",
                      f"Politique de confidentialité de {SITE['nom']} : données collectées, finalités, durées de conservation et exercice de vos droits.",
                      contenu)


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
<ul>
  <li><a href="expertises/index.html">Toutes nos expertises</a></li>
  {exp}
</ul>

<h2>Informations légales</h2>
<ul>
  <li><a href="mentions-legales.html">Mentions légales</a></li>
  <li><a href="confidentialite.html">Politique de confidentialité</a></li>
</ul>
"""
    return page_prose("plan-du-site.html", f"Plan du site — {SITE['nom']}",
                      "Plan du site", "Navigation",
                      f"Plan du site {SITE['nom']} : toutes les pages accessibles en un coup d'œil.",
                      contenu)


def page_404():
    body = f"""<section class="page-hero">
  <div class="container">
    <div class="page-hero__inner">
      <p class="eyebrow">Erreur 404</p>
      <h1>Cette page n'existe pas</h1>
      <p>
        Le lien est peut-être erroné ou la page a été déplacée.
        Voici les chemins les plus utiles.
      </p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid--3">
      <a class="card" href="/index.html">{icon('arrow','card__icon')}<h3>Retour à l'accueil</h3><p>La page principale du site.</p></a>
      <a class="card" href="/expertises/index.html">{icon('brief','card__icon')}<h3>Nos expertises</h3><p>Les sept pôles d'accompagnement.</p></a>
      <a class="card" href="/rendez-vous.html">{icon('calendar','card__icon')}<h3>Prendre rendez-vous</h3><p>15 minutes offertes, sans engagement.</p></a>
    </div>
  </div>
</section>
"""
    return layout("404.html", f"Page introuvable — {SITE['nom']}",
                  "La page demandée n'existe pas.", body, "")


# ---------------------------------------------------------------------------
# Fichiers techniques
# ---------------------------------------------------------------------------
def favicon():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
  <rect width="48" height="48" rx="8" fill="#0A1A2F"/>
  <path d="M24 7 39 12v11c0 9.6-7 16.3-15 18.4C16 39.3 9 32.6 9 23V12z" fill="none" stroke="#C9A227" stroke-width="2.2"/>
  <path d="M24 15v16M18 31h12" stroke="#EDF2F8" stroke-width="2" stroke-linecap="round"/>
</svg>
"""


def sitemap(pages):
    today = date.today().isoformat()
    urls = []
    for p in pages:
        if p in ("404.html",):
            continue
        loc = SITE["domaine"] + "/" + ("" if p == "index.html" else p)
        prio = "1.0" if p == "index.html" else ("0.9" if p.startswith("expertises/") or p == "procedure-fiscale.html" else "0.7")
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{prio}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domaine']}/sitemap.xml\n"


# ---------------------------------------------------------------------------
# Exécution
# ---------------------------------------------------------------------------
def main():
    print("Construction du site CCF Conseil…\n")
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
    write("sitemap.xml", sitemap(produced))
    write("robots.txt", robots())
    write(".nojekyll", "")

    print(f"\n{len(produced)} pages générées.")


if __name__ == "__main__":
    main()
