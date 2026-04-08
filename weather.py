import requests

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": -8.0476,
        "longitude": -34.8770,
        "current": "temperature_2m,relative_humidity_2m,precipitation",
        "hourly": "precipitation",
        "forecast_days": 2
    }

    response = requests.get(url, params=params)
    data = response.json()

    current = data["current"]
    hourly = data["hourly"]["precipitation"]

    # pega próximas 12 horas
    next_hours = hourly[:12]

    total_rain = sum(next_hours)
    max_rain = max(next_hours)

    return {
        "temp": current["temperature_2m"],
        "rain": current["precipitation"],
        "humidity": current["relative_humidity_2m"],
        "hourly_rain": next_hours,
        "total_rain": total_rain,
        "max_rain": max_rain
    }