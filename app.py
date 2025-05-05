from flask import Flask, render_template_string, request, jsonify
import requests
from bs4 import BeautifulSoup
import socket
import json
import os

GAMES = [
    {"name": "CS:GO", "appid": "740", "ports": "27015:27015/udp"},
    {"name": "ARK: Survival Evolved", "appid": "376030", "ports": "7777:7777/udp,27015:27015/udp"},
    {"name": "Team Fortress 2", "appid": "232250", "ports": "27015:27015/udp"},
    {"name": "Rust", "appid": "258550", "ports": "28015:28015/udp"},
    {"name": "Unturned", "appid": "1110390", "ports": "27015:27015/udp"},
    # Ajoutez d'autres jeux ici
]

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Choisissez votre jeu Steam</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="hero">
    <h1>🎮 Easy Host Server</h1>
    <p>Sélectionnez un jeu pour générer la commande Docker adaptée.</p>
</div>
<section class="howto">
    <form method="post">
        <label for="game">Jeu :</label>
        <select name="game" id="game">
            {% for g in games %}
            <option value="{{g.appid}}|{{g.ports}}">{{g.name}}</option>
            {% endfor %}
        </select>
        <button type="submit" class="btn">Générer la commande</button>
    </form>
    {% if cmd %}
    <h2>Votre commande Docker :</h2>
    <pre>{{cmd}}</pre>
    <h3>IP du serveur : <span style="color:#00ffea">{{ip}}</span></h3>
    <p>Ports ouverts : <b>{{ports}}</b></p>
    {% endif %}
</section>
<footer>
    <p>Projet open-source. Fait avec ❤️ pour la communauté gaming.</p>
</footer>
</body>
</html>
"""

GAMES_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Liste des jeux compatibles Linux/Docker</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vanilla-tilt/1.7.2/vanilla-tilt.min.js"></script>
    <style>
      .games-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 30px;
        margin: 40px auto;
        max-width: 1200px;
        padding: 0 20px;
      }
      .game-card {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31,38,135,0.37);
        padding: 30px 20px;
        color: #fff;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
        position: relative;
        overflow: hidden;
      }
      .game-card:hover {
        transform: scale(1.05) rotate(-1deg);
        box-shadow: 0 16px 48px 0 #00c6ff55;
        z-index: 2;
      }
      .game-title {
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 0.5em;
        letter-spacing: 1px;
        text-shadow: 0 2px 8px #000a;
        animation: pulse 2s infinite;
      }
      .game-appid {
        font-size: 1em;
        color: #00ffea;
        margin-bottom: 0.3em;
      }
      .game-os {
        font-size: 0.95em;
        color: #aaa;
      }
      @keyframes pulse {
        0% { text-shadow: 0 0 8px #00c6ff88; }
        50% { text-shadow: 0 0 24px #00c6ff; }
        100% { text-shadow: 0 0 8px #00c6ff88; }
      }
    </style>
</head>
<body>
<div class="hero animate__animated animate__fadeInDown">
    <h1>🌟 Jeux compatibles Linux & Docker</h1>
    <p>Voici la liste complète des jeux Steam disposant d’un serveur dédié Linux, idéale pour Docker !</p>
    <a href="/" class="btn">Retour à l'accueil</a>
</div>
<div class="games-grid">
    {% for game in games %}
    <div class="game-card animate__animated animate__zoomIn" data-tilt data-tilt-max="8" data-tilt-speed="400">
        <div class="game-title">{{game.name}}</div>
        <div class="game-appid">AppID: {{game.appid}}</div>
        <div class="game-os">{{game.os}}</div>
    </div>
    {% endfor %}
</div>
<footer>
    <p>
      Liste extraite de <a href="{{source}}" style="color:#00c6ff">Valve Developer Wiki</a>
      <br>
      Dernière mise à jour : {{last_update}}
      <br>
      Effets par <a href="https://animate.style/" style="color:#00c6ff">Animate.css</a> & <a href="https://micku7zu.github.io/vanilla-tilt.js/" style="color:#00c6ff">Vanilla Tilt</a>.
    </p>
</footer>
<script>
  VanillaTilt.init(document.querySelectorAll(".game-card"));
</script>
</body>
</html>
"""

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    cmd = None
    ip = get_ip()
    ports = ""
    if request.method == "POST":
        val = request.form["game"]
        appid, ports = val.split("|")
        port_args = " ".join([f"-p {p.strip()}" for p in ports.split(",")])
        cmd = f"docker run -it {port_args} easy-steam-server {appid}"
    return render_template_string(HTML, games=GAMES, cmd=cmd, ip=ip, ports=ports)

@app.route("/games")
def games():
    # Charge la liste statique depuis Game/games_linux.json
    games_path = os.path.join(os.path.dirname(__file__), "Game", "games_linux.json")
    with open(games_path, encoding="utf-8") as f:
        data = json.load(f)
    games = data.get("games", [])
    source = data.get("source", "")
    last_update = data.get("last_update", "")
    return render_template_string(GAMES_HTML, games=games, source=source, last_update=last_update)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
