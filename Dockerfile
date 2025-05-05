FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LOG_PATH=/app/server.log

RUN apt-get update && \
    apt-get install -y wget ca-certificates lib32gcc-s1 curl python3-pip && \
    useradd -m steam && \
    rm -rf /var/lib/apt/lists/*

# Installer SteamCMD
RUN mkdir -p /opt/steamcmd && \
    cd /opt/steamcmd && \
    wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz && \
    tar -xzf steamcmd_linux.tar.gz && \
    rm steamcmd_linux.tar.gz

# Crée le dossier de l'app
WORKDIR /app

# Copie tout le code et les fichiers nécessaires dans /app
COPY . /app

# Installer les dépendances Python
RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh

USER steam
WORKDIR /home/steam

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
