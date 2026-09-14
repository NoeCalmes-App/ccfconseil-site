#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCF Conseil — chargement du contenu.

Tout le texte du site vit dans le dossier `content/`, en JSON :

    content/cabinet.json      coordonnées et réglages du cabinet
    content/expertises.json   les sept pôles
    content/procedure.json    les étapes de la procédure fiscale
    content/ressources.json   les fiches pratiques

C'est la base de contenu du site. Elle se modifie de trois façons :

  1. depuis l'interface d'administration (`/admin`), sans toucher au code ;
  2. en éditant les fichiers JSON à la main ;
  3. par un script, si un jour il faut importer des données en masse.

Le site reste entièrement statique : le JSON est lu au moment de la génération,
jamais par le navigateur du visiteur. Aucune base à héberger, à sauvegarder ou
à sécuriser — et l'historique des modifications, c'est celui de git.
"""

import json
import os

DOSSIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")


def charger(nom):
    chemin = os.path.join(DOSSIER, nom)
    if not os.path.exists(chemin):
        raise SystemExit(
            f"\n  Fichier de contenu introuvable : content/{nom}\n"
            f"  Le site ne peut pas être généré sans lui.\n"
        )
    try:
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise SystemExit(
            f"\n  content/{nom} n'est pas un JSON valide.\n"
            f"  {e}\n"
            f"  Une virgule en trop ou un guillemet oublié, le plus souvent.\n"
        )


# ---------------------------------------------------------------------------
# Cabinet
# ---------------------------------------------------------------------------
CABINET = charger("cabinet.json")

# ---------------------------------------------------------------------------
# Expertises
# Les gabarits attendent des tuples pour les étapes et les questions :
# on convertit ici, une seule fois, pour que build.py reste inchangé.
# ---------------------------------------------------------------------------
EXPERTISES = []
for _e in charger("expertises.json"):
    _e = dict(_e)
    _e["etapes"] = [(s["titre"], s["texte"]) for s in _e.get("etapes", [])]
    _e["faq"] = [(q["question"], q["reponse"]) for q in _e.get("faq", [])]
    EXPERTISES.append(_e)

# ---------------------------------------------------------------------------
# Procédure fiscale
# ---------------------------------------------------------------------------
PROCEDURE = [
    (p["titre"], p["texte"], p["label"], p["valeur"], p["source"], p["ton"], p["note"])
    for p in charger("procedure.json")
]

# ---------------------------------------------------------------------------
# Ressources
# ---------------------------------------------------------------------------
RESSOURCES = charger("ressources.json")
