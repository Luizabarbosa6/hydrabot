import requests

# 🔎 Busca coordenadas a partir do nome do bairro
def get_coordinates(bairro):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"{bairro}, Recife, Pernambuco, Brasil",
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "HydraRecApp"  # obrigatório no Nominatim
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if not data:
            return None

        return {
            "lat": float(data[0]["lat"]),
            "lon": float(data[0]["lon"]),
            "display_name": data[0]["display_name"]
        }

    except Exception as e:
        print(f"Erro ao buscar coordenadas: {e}")
        return None


# 🌧️ Busca dados climáticos com base no bairro
def get_weather(bairro):
    location = get_coordinates(bairro)

    if not location:
        return {
            "error": "Bairro não encontrado"
        }

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": location["lat"],
        "longitude": location["lon"],
        "current": "temperature_2m,relative_humidity_2m,precipitation",
        "hourly": "precipitation",
        "forecast_days": 2
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        current = data.get("current", {})
        hourly = data.get("hourly", {}).get("precipitation", [])

        # pega próximas 12 horas
        next_hours = hourly[:12] if hourly else []

        total_rain = sum(next_hours) if next_hours else 0
        max_rain = max(next_hours) if next_hours else 0

        return {
            "bairro": bairro,
            "lat": location["lat"],
            "lon": location["lon"],
            "temp": current.get("temperature_2m", 0),
            "rain": current.get("precipitation", 0),
            "humidity": current.get("relative_humidity_2m", 0),
            "hourly_rain": next_hours,
            "total_rain": total_rain,
            "max_rain": max_rain
        }

    except Exception as e:
        print(f"Erro ao buscar clima: {e}")
        return {
            "error": "Erro ao buscar dados meteorológicos"
        }