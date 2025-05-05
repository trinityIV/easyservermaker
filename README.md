# Easy Host Server (SteamCMD + Docker)

Ce projet permet d’héberger facilement un serveur de jeu Steam compatible Docker/Ubuntu, sans login requis.

## Fonctionnalités

- Interface web moderne pour choisir un jeu et générer la commande Docker adaptée.
- Liste complète et dynamique des jeux Steam disposant d’un serveur dédié Linux, avec un visuel animé.
- Installation automatique du serveur de jeu via SteamCMD sans compte Steam.
- Prise en charge des ports nécessaires pour chaque jeu.
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

   - Choisissez un jeu dans la liste pour générer la commande Docker adaptée (avec les bons ports).
   - Ou cliquez sur "Liste complète des jeux compatibles" pour voir tous les jeux Steam supportant un serveur Linux/Docker, avec un visuel animé.

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

## Ressources

- [steamctl](https://github.com/ValvePython/steamctl)
- [SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD)
- [Liste officielle des serveurs dédiés Steam](https://developer.valvesoftware.com/wiki/Dedicated_Servers_List)

---

Pour une interface web locale, ouvrez `index.html`.
