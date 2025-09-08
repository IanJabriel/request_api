import pytest
import steam_api
import json

def test_minutos_para_horas():
    assert steam_api.minutos_para_horas(0) == 0
    assert steam_api.minutos_para_horas(59) == 1
    assert steam_api.minutos_para_horas(60) == 1
    assert steam_api.minutos_para_horas(61) == 2

def test_jogos_steam(requests_mock):
    fake_response = {
        "response": {
            "game_count": 2,
            "games": [
                {"appid": 10, "name": "Counter-Strike", "playtime_forever": 120, "img_icon_url": "url1"},
                {"appid": 20, "name": "Team Fortress Classic", "playtime_forever": 300, "img_icon_url": "url2"}
            ]
        }
    }

    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    requests_mock.get(url, json=fake_response)

    steam = steam_api.Steam("fake_id", "fake_key")
    steam.jogos_steam(url)

    # Verifica se o arquivo foi criado corretamente
    with open("JsonSteam.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 2
        assert data[0]["name"] == "Team Fortress Classic"  # mais tempo de jogo
        assert data[1]["name"] == "Counter-Strike"

def test_jogos_recentes(requests_mock):
    fake_response = {
        "response": {
            "total_count": 1,
            "games": [
                {"appid": 730, "name": "CS:GO", "playtime_2weeks": 300, "playtime_forever": 15000}
            ]
        }
    }

    url = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/"
    requests_mock.get(url, json=fake_response)

    steam = steam_api.Steam("fake_id", "fake_key")
    steam.jogos_recentes(url)

    with open("JogosRecentes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["nome"] == "CS:GO"
        assert data[0]["horas_totais"] == steam_api.minutos_para_horas(15000)

def test_chave_api_invalida(requests_mock):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    requests_mock.get(url, status_code=403, text="Forbidden")

    steam = steam_api.Steam("fake_id", "chave_errada")

    # como o método só imprime o erro, não levanta exceção
    steam.jogos_steam(url)
