import requests
from bs4 import BeautifulSoup
import json

url = "https://developer.valvesoftware.com/wiki/Dedicated_Servers_List"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table", {"class": "wikitable"})
games = []
if table:
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) >= 3:
            name = cols[0].get_text(strip=True)
            appid = cols[1].get_text(strip=True)
            os = cols[2].get_text(strip=True)
            if "Linux" in os:
                games.append({"name": name, "appid": appid, "os": os})

with open("games.json", "w", encoding="utf-8") as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

print(f"{len(games)} jeux compatibles Linux exportés dans games.json")
