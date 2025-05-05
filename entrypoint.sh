#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Aucun AppID fourni. Lancement de l'interface web sur le port 8080..."
  echo "Accédez à http://localhost:8080 dans votre navigateur."
  echo "Pour lancer un serveur de jeu directement :"
  echo "  docker run -it -p 27015:27015/udp easy-steam-server 740"
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
echo "Pour voir la liste complète des jeux compatibles, lancez sans AppID :"
echo "  docker run -it -p 8080:8080 easy-steam-server"

tail -f /dev/null
