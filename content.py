#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCF Conseil — contenu du site.

Tout le texte éditable est ici : expertises, étapes de la procédure fiscale.
Les gabarits et la mise en page sont dans build.py.
"""

# ---------------------------------------------------------------------------
# Expertises — source unique de vérité
# ---------------------------------------------------------------------------
EXPERTISES = [
    {
        "slug": "conseil-fiscal",
        "titre_seo": "Conseil fiscal pour entreprises",
        "nav": "Conseil fiscal",
        "titre": "Conseil fiscal",
        "accroche": "Anticiper pour mieux décider",
        "icone": "doc",
        "resume": "Analyse de votre situation fiscale, identification des points de vigilance et préparation des dossiers.",
        "meta": "Analyse de votre situation fiscale, identification des risques et préparation des dossiers. Premier échange de 15 minutes offert.",
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
        "titre_seo": "Contrôle fiscal : se faire accompagner",
        "nav": "Contrôle fiscal",
        "titre": "Contrôle fiscal",
        "accroche": "Vous accompagner à chaque étape",
        "icone": "search",
        "resume": "Analyse des demandes de l'administration, organisation des pièces, préparation du dossier et suivi des échanges.",
        "meta": "Avis de vérification, proposition de rectification : organisation des pièces et réponse dans les délais. 15 minutes offertes.",
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
        "titre_seo": "Contrôle URSSAF : préparer son dossier",
        "nav": "Contrôle URSSAF",
        "titre": "Contrôle URSSAF",
        "accroche": "Analyse · Préparation · Suivi",
        "icone": "users",
        "resume": "Étude des documents reçus, préparation des éléments demandés et analyse des observations.",
        "meta": "Étude des documents, préparation des éléments demandés et réponse à la lettre d'observations. Premier échange offert.",
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
        "titre_seo": "Entreprise en difficulté : agir à temps",
        "nav": "Entreprises en difficulté",
        "titre": "Entreprises en difficulté",
        "accroche": "Intervenir avec méthode et anticipation",
        "icone": "shield",
        "resume": "Préparation administrative des dossiers de prévention, de sauvegarde et de redressement judiciaire.",
        "meta": "Prévention, sauvegarde, redressement judiciaire : préparation administrative des dossiers et coordination des professionnels.",
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
        "titre_seo": "Création d'entreprise : être accompagné",
        "nav": "Création d'entreprise",
        "titre": "Création d'entreprise",
        "accroche": "Structurer le projet dès le départ",
        "icone": "brief",
        "resume": "Accompagnement dans les premières étapes du projet : constitution, organisation et préparation des éléments.",
        "meta": "Constitution, organisation administrative et préparation des éléments du projet, avec les professionnels compétents.",
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
        "titre_seo": "Paie, déclarations sociales et DSN",
        "nav": "Social · Paie · DSN",
        "titre": "Social, paie et DSN",
        "accroche": "Accompagnement administratif au quotidien",
        "icone": "users",
        "resume": "Gestion administrative de la paie, préparation et suivi des déclarations sociales et de la DSN.",
        "meta": "Préparation des éléments de paie, suivi des déclarations sociales et de la DSN, organisation documentaire du dossier social.",
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
        "titre_seo": "Réclamation et recours fiscal",
        "nav": "Procédures & recours",
        "titre": "Procédures et recours",
        "accroche": "Du contrôle jusqu'au contentieux",
        "icone": "scale",
        "resume": "Analyse documentaire et préparation administrative des dossiers de réclamation et de recours.",
        "meta": "Réclamation contentieuse, recours hiérarchique, tribunal administratif : préparation des dossiers et respect des délais.",
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

