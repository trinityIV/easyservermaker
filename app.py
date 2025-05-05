from flask import Flask, render_template, render_template_string, request, jsonify, send_from_directory, abort
import requests
from bs4 import BeautifulSoup
import socket
import json
import os
import urllib.request

def load_games():
    local_json_path = os.path.join(os.path.dirname(__file__), "game", "games_linux.json")
    try:
        with open(local_json_path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("games", [])
    except Exception:
        return []

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

@app.route("/", methods=["GET"])
def index():
    games = load_games()
    ip = get_ip()
    return render_template("index.html", games=games, ip=ip)

@app.route("/games")
def games():
    # Charge la liste depuis le fichier local
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        local_json_path = os.path.join(base_dir, "game", "games_linux.json")
        with open(local_json_path, encoding="utf-8") as f:
            data = json.load(f)
        games = data.get("games", [])
        # Passe les variables dans un seul dict context pour éviter le conflit d'arguments
        context = dict(games=games, source=data.get("source", ""), last_update=data.get("last_update", ""))
        return render_template_string(GAMES_HTML, **context)
    except Exception as e:
        # Log l'erreur pour debug
        print("Erreur chargement /games :", e)
        return "<h2>Erreur de chargement de la liste des jeux.<br>Détail : {}</h2>".format(e), 500

# Nouvelle route pour la page de configuration détaillée d'un jeu
@app.route("/game/<appid>")
def game_detail(appid):
    # Charge la liste depuis le fichier local
    local_json_path = os.path.join(os.path.dirname(__file__), "game", "games_linux.json")
    try:
        with open(local_json_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {"games": []}
    games = data.get("games", [])
    game = next((g for g in games if g.get("appid") == appid), None)
    if not game:
        return "<h2>Jeu non trouvé</h2>", 404
    # Génère la commande Docker par défaut
    ports = game.get("ports", "")
    port_args = " ".join([f"-p {p.strip()}" for p in ports.split(",")]) if ports else ""
    docker_cmd = f"docker run -it {port_args} easy-steam-server {appid}"
    return render_template_string(GAME_DETAIL_HTML, game=game, docker_cmd=docker_cmd)

# Nouveau template pour la page de configuration d'un jeu
GAME_DETAIL_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Configurer {{game.name}} - Easy Host Server</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <style>
      body {
        margin: 0;
        min-height: 100vh;
        background: linear-gradient(120deg, #232526 0%, #414345 100%);
        font-family: 'Segoe UI', Arial, sans-serif;
        color: #fff;
        overflow-x: hidden;
      }
      .blur-bg {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: url('https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1500&q=80') center/cover no-repeat;
        filter: blur(16px) brightness(0.5);
        z-index: 0;
      }
      .container {
        position: relative;
        z-index: 2;
        max-width: 700px;
        margin: 60px auto 30px auto;
        background: rgba(30,40,60,0.85);
        border-radius: 24px;
        box-shadow: 0 8px 40px #00c6ff33;
        padding: 40px 32px;
        backdrop-filter: blur(6px);
        animation: fadeInUp 1.2s cubic-bezier(.23,1.01,.32,1) both;
      }
      @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(60px);}
        to { opacity: 1; transform: translateY(0);}
      }
      h1 {
        font-size: 2.2em;
        margin-bottom: 0.2em;
        letter-spacing: 1px;
        text-shadow: 0 2px 16px #00c6ff77;
        animation: pulse 2s infinite;
      }
      .game-info {
        margin-bottom: 1.5em;
        font-size: 1.1em;
      }
      .docker-cmd {
        background: linear-gradient(90deg, #232526 60%, #00c6ff33 100%);
        border-radius: 10px;
        padding: 18px 12px;
        font-family: 'Fira Mono', 'Consolas', monospace;
        font-size: 1.1em;
        color: #00ffea;
        margin-bottom: 1.2em;
        box-shadow: 0 2px 16px #00c6ff22;
        user-select: all;
        animation: fadeIn 1.5s;
      }
      @keyframes fadeIn {
        from { opacity: 0;}
        to { opacity: 1;}
      }
      .explain {
        margin-bottom: 1.5em;
        background: rgba(0,198,255,0.09);
        border-left: 4px solid #00c6ff;
        padding: 16px 18px;
        border-radius: 8px;
        font-size: 1.07em;
        box-shadow: 0 2px 8px #00c6ff11;
        animation: fadeIn 2s;
      }
      .btn {
        display: inline-block;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: #fff;
        padding: 12px 28px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1em;
        text-decoration: none;
        box-shadow: 0 2px 12px #00c6ff55;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-top: 18px;
      }
      .btn:hover {
        transform: scale(1.06) rotate(-1deg);
        box-shadow: 0 6px 24px #00c6ff99;
      }
      .ports {
        color: #00ffea;
        font-weight: bold;
      }
      .ubuntu {
        margin-top: 2em;
        background: rgba(255,255,255,0.04);
        border-radius: 10px;
        padding: 18px 16px;
        font-size: 1em;
        box-shadow: 0 2px 8px #00c6ff22;
        animation: fadeIn 2.5s;
      }
      .ubuntu pre {
        background: #181c22;
        color: #00ffea;
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 1em;
        margin: 0.5em 0 0 0;
        overflow-x: auto;
      }
      @keyframes pulse {
        0% { text-shadow: 0 0 8px #00c6ff88; }
        50% { text-shadow: 0 0 24px #00c6ff; }
        100% { text-shadow: 0 0 8px #00c6ff88; }
      }
    </style>
</head>
<body>
<div class="blur-bg"></div>
<div class="container animate__animated animate__fadeInUp">
    <h1>{{game.name}}</h1>
    <div class="game-info">
        <b>AppID :</b> {{game.appid}}<br>
        <b>Ports recommandés :</b> <span class="ports">{{game.ports}}</span><br>
        <b>OS :</b> {{game.os}}
    </div>
    <div class="explain">
        <b>Commandez votre serveur Docker :</b><br>
        Copiez la commande ci-dessous et exécutez-la sur votre machine Docker/Ubuntu.<br>
        <span style="color:#ffb300">Assurez-vous d’avoir Docker installé et les ports ouverts sur votre pare-feu !</span>
    </div>
    <div class="docker-cmd" onclick="navigator.clipboard.writeText(this.innerText);this.style.background='#00c6ff44';this.innerText='Copié !';setTimeout(()=>{this.innerText='{{docker_cmd}}';this.style.background='';},1200);">
        {{docker_cmd}}
    </div>
    <a href="/games" class="btn">⬅ Retour à la liste des jeux</a>
    <div class="ubuntu">
        <b>Installer Docker sur Ubuntu :</b>
        <pre>
sudo apt update
sudo apt install docker.io -y
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# Déconnectez-vous puis reconnectez-vous pour appliquer les droits
        </pre>
        <b>Lancer le serveur pour {{game.name}} :</b>
        <pre>
{{docker_cmd}}
        </pre>
        <span style="color:#aaa">Pour personnaliser les variables d’environnement, consultez la <a href="https://hub.docker.com/r/cm2network/steamcmd" style="color:#00c6ff">doc Docker SteamCMD</a>.</span>
    </div>
</div>
</body>
</html>
"""

@app.route("/games/list")
def games_list():
    local_json_path = os.path.join(os.path.dirname(__file__), "game", "games_linux.json")
    try:
        with open(local_json_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {"games": [], "source": local_json_path, "last_update": "Erreur de chargement"}
    return jsonify(data)

@app.route("/logs")
def logs():
    log_path = os.path.join(os.path.dirname(__file__), "server.log")
    if not os.path.exists(log_path):
        logs = "Aucun log trouvé."
    else:
        with open(log_path, encoding="utf-8", errors="ignore") as f:
            logs = f.read()[-10000:]  # Limite à 10k derniers caractères
    return render_template("logs.html", logs=logs)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(503)
def service_unavailable(e):
    return render_template("503.html"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
