#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Aucun AppID fourni. Lancement de l'interface web sur le port 8080..."
  exec python3 /app.py
fi

APPID="$1"
INSTALL_DIR="/home/steam/game"

echo "Installation du serveur pour l'AppID $APPID..."

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

/opt/steamcmd/steamcmd.sh +login anonymous +force_install_dir "$INSTALL_DIR" +app_update "$APPID" validate +quit

echo "Serveur installé dans $INSTALL_DIR"
echo "Pour lancer le serveur, consultez la documentation du jeu."

tail -f /dev/null
