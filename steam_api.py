import requests, json, os

class Steam():
    def __init__(self,id_steam,key_steam):
        self.id_steam = id_steam
        self.key_steam = key_steam

    def jogos_steam(self,url_api:str):

        url = url_api
        params = {
            "key": self.key_steam, 
            "steamid": self.id_steam, 
            "include_appinfo": 1, 
            "format": "json"
        }

        response = requests.get(url, params=params)

        print(f"Status code 'jogos_steam': {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            game_list = data.get("response",{}).get("games",[])
            game_list_sorted = sorted(game_list,key=lambda g: g.get("playtime_forever",0), reverse=True)

            games_filtred = [
                {
                    "appid": g["appid"],
                    "name": g["name"],
                    "playtime_hours": round(minutos_para_horas(g.get("playtime_forever", 0)),1),
                    "img_icon_url": g["img_icon_url"]
                }
                for g in game_list_sorted
            ]
        
            with open("JsonSteam.json", "w", encoding="utf-8") as arq:
                json.dump(games_filtred, arq, indent=4, ensure_ascii=False)
        else:
            print("Erro na requisição:", response.text)


    def jogos_recentes(self, url_api):

        url = url_api
        params = {
            "key": self.key_steam,
            "steamid": self.id_steam,
            "format": "json",
            "count": 50  # quantos jogos recentes você quer pegar
        }

        response = requests.get(url, params=params)

        print(f"Status code 'jogos_recentes': {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            games = data.get("response", {}).get("games", [])

            games_sorted = sorted(games, key=lambda g: g.get("playtime_2weeks", 0), reverse=True)

            # Filtra campos desejados e converte minutos em horas
            recent_games_filtered = [
                {
                    "appid": g["appid"],
                    "nome": g.get("name", ""),
                    "horas_totais": minutos_para_horas(g.get("playtime_forever", 0))
                }
                for g in games_sorted
            ]

            with open("JogosRecentes.json", "w", encoding="utf-8") as arq:
                json.dump(recent_games_filtered, arq, indent=4, ensure_ascii=False)

        else:
            print("Erro na requisição:", response.status_code, response.text)

def minutos_para_horas(minutos:int ) -> int:
    import math
    return math.ceil(minutos / 60)

def main():
    id_steam = os.getenv("id_steam")    
    key_steam = os.getenv("api_key")

    print("EXECUTANDO AS APIS DA STEAM: ")

    steam = Steam(id_steam,key_steam)
    steam.jogos_steam("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/")
    steam.jogos_recentes("https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/")

main()