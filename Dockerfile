FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y wget ca-certificates lib32gcc-s1 curl python3-pip && \
    useradd -m steam

# Installer SteamCMD
RUN mkdir -p /opt/steamcmd && \
    cd /opt/steamcmd && \
    wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz && \
    tar -xzf steamcmd_linux.tar.gz && \
    rm steamcmd_linux.tar.gz

# Installer steamctl et Flask
RUN pip3 install steamctl flask

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY app.py /app.py

USER steam
WORKDIR /home/steam

ENTRYPOINT ["/entrypoint.sh"]
