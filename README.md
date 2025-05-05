# Easy Host Server (SteamCMD + Docker)

Ce projet permet d’héberger facilement un serveur de jeu Steam compatible Docker/Ubuntu, sans login requis.

## Fonctionnalités

- Interface web moderne avec grille de jaquettes cliquables pour générer la commande Docker adaptée à chaque jeu.
- Liste complète et dynamique des jeux Steam disposant d’un serveur dédié Linux, avec un visuel animé.
- Affichage en temps réel du **statut des serveurs Valve et Faceit** pour la France, la Belgique et la Suisse (bandeau en haut de la page jeux).
- Installation automatique du serveur de jeu via SteamCMD sans compte Steam.
- Prise en charge des ports nécessaires pour chaque jeu.
- **Suivi des logs serveur** via la page `/logs` (affichage stylé, lecture du fichier `server.log`).
- Pages d’erreur **404** et **503** avec un thème gaming moderne.
- Documentation claire et interface utilisateur intuitive.

## Utilisation rapide

1. **Construisez l’image Docker** :
   ```sh
   docker build -t easy-steam-server .
   ```

2. **Lancez l’interface web** :
   ```sh
   docker run -it -p 8080:8080 easy-steam-server
   ```

3. **Ouvrez votre navigateur sur** [http://localhost:8080](http://localhost:8080)

   - **Accueil** : Choisissez un jeu en cliquant sur sa jaquette pour générer la commande Docker adaptée (avec les bons ports).
   - **Liste complète** : Cliquez sur "Liste complète des jeux compatibles" pour voir tous les jeux Steam supportant un serveur Linux/Docker, avec un visuel animé et le statut des serveurs Valve/Faceit.
   - **Logs** : Accédez à [http://localhost:8080/logs](http://localhost:8080/logs) pour consulter les derniers logs du serveur (fichier `server.log`).
   - **Pages d’erreur** : Les erreurs 404 et 503 affichent des pages gaming stylées.

4. **Lancez un serveur de jeu directement** (exemple pour CS:GO : 740) :
   ```sh
   docker run -it -p 27015:27015/udp easy-steam-server 740
   ```

5. **Les fichiers du serveur seront installés dans** `/home/steam/game` **dans le conteneur.**

6. **Consultez la documentation du jeu pour lancer le serveur** (chaque jeu a sa propre commande de lancement).

## Exemples de commandes

- **Lancer l'interface web (liste des jeux, génération de commandes) :**
  ```sh
  docker run -it -p 8080:8080 easy-steam-server
  ```
  Accédez à [http://localhost:8080](http://localhost:8080)

- **Lancer un serveur CS:GO (AppID 740) avec le port UDP ouvert :**
  ```sh
  docker run -it -p 27015:27015/udp easy-steam-server 740
  ```

## Dépannage

- **Problème de droits Docker :**  
  Si vous voyez une erreur "permission denied", ajoutez votre utilisateur au groupe docker :
  ```sh
  sudo usermod -aG docker $USER
  # Déconnectez-vous puis reconnectez-vous
  ```

- **Ports non accessibles :**  
  Vérifiez que les ports nécessaires sont bien ouverts sur votre VPS/pare-feu.

## Liste dynamique des jeux compatibles

- Rendez-vous sur [http://localhost:8080/games](http://localhost:8080/games) pour voir la liste complète des jeux Steam disposant d’un serveur dédié Linux, idéale pour Docker, avec un visuel moderne et des animations.
- Le statut des serveurs Valve et Faceit pour la France, la Belgique et la Suisse est affiché en haut de la page.

## Suivi des logs serveur

- Consultez [http://localhost:8080/logs](http://localhost:8080/logs) pour voir les derniers logs du serveur (lecture du fichier `server.log`).

## Pages d’erreur personnalisées

- Les erreurs 404 et 503 affichent des pages gaming stylées pour une meilleure expérience utilisateur.

## Ressources

- [steamctl](https://github.com/ValvePython/steamctl)
- [SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD)
- [Liste officielle des serveurs dédiés Steam](https://developer.valvesoftware.com/wiki/Dedicated_Servers_List)

---

Pour une interface web locale, ouvrez `index.html`.
