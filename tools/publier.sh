#!/usr/bin/env bash
#
# Crée le dépôt GitHub et pousse le site — CCF Conseil
#
#   bash tools/publier.sh
#
# Le dépôt est créé en PRIVÉ : content/cabinet.json contiendra le SIREN et
# l'adresse de la cliente. À passer en public plus tard si vous le souhaitez.

set -euo pipefail

DEPOT="${1:-ccfconseil-web}"
BRANCHE="main"

bleu()  { printf '\033[1;34m%s\033[0m\n' "$1"; }
vert()  { printf '\033[32m%s\033[0m\n' "$1"; }
rouge() { printf '\033[31m%s\033[0m\n' "$1"; }

cd "$(dirname "$0")/.."

# --- Le dossier est-il bien un dépôt git ? ----------------------------------
if [ ! -d .git ]; then
  bleu "Aucun dépôt git ici — initialisation."
  git init -q
  git add -A
  git commit -q -m "Site vitrine CCF Conseil"
fi

git branch -M "$BRANCHE"

# --- Reste-t-il des modifications non enregistrées ? ------------------------
if [ -n "$(git status --porcelain)" ]; then
  bleu "Modifications en attente — enregistrement."
  git add -A
  git commit -q -m "Mise à jour du site"
fi

vert "$(git rev-list --count HEAD) commits prêts sur la branche $BRANCHE."

# --- Le dépôt distant existe-t-il déjà ? ------------------------------------
if git remote get-url origin >/dev/null 2>&1; then
  bleu "Dépôt distant déjà configuré : $(git remote get-url origin)"
  git push -u origin "$BRANCHE"
  vert "Poussé."
  exit 0
fi

# --- Création du dépôt ------------------------------------------------------
if command -v gh >/dev/null 2>&1; then
  if ! gh auth status >/dev/null 2>&1; then
    rouge "GitHub CLI installé mais pas connecté."
    echo "  Lancez d'abord :  gh auth login"
    exit 1
  fi
  bleu "Création du dépôt privé « $DEPOT » et envoi…"
  gh repo create "$DEPOT" --private --source=. --remote=origin --push
  vert "Terminé."
  echo
  echo "  Dépôt : $(gh repo view --json url -q .url 2>/dev/null || echo "$DEPOT")"
else
  rouge "GitHub CLI (gh) n'est pas installé."
  echo
  echo "  Option 1 — l'installer :"
  echo "      brew install gh && gh auth login"
  echo "      puis relancer ce script."
  echo
  echo "  Option 2 — à la main :"
  echo "      1. Créer un dépôt PRIVÉ nommé « $DEPOT » sur github.com/new"
  echo "         (sans README, sans .gitignore : le dossier en contient déjà)"
  echo "      2. Puis ici :"
  echo "         git remote add origin git@github.com:VOTRE-PSEUDO/$DEPOT.git"
  echo "         git push -u origin $BRANCHE"
  exit 1
fi

echo
bleu "Après le push, trois choses :"
echo "  · Settings → Pages → branche $BRANCHE, dossier / (root)"
echo "  · Remplacer UTILISATEUR/$DEPOT dans admin/config.yml"
echo "  · Renseigner content/cabinet.json (la ville en priorité), puis npm run build"
