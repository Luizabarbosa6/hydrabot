import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()


def classify_risk(weather_data):
    total = weather_data["total_rain"]
    peak = weather_data["max_rain"]

    if peak > 30 or total > 100:
        return "ALTO"
    elif peak > 10 or total > 40:
        return "MÉDIO"
    else:
        return "BAIXO"


def analyze_weather(weather_data):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "risk": "ERRO",
            "analysis": "Chave da API não configurada."
        }

    params = {
        "key": api_key
    }

    risk = classify_risk(weather_data)

    prompt = f"""
Você é o HydraRec, um sistema inteligente de monitoramento de chuvas que atua em parceria com a Defesa Civil do Recife.

Seu papel é analisar dados meteorológicos e orientar a população durante situações de chuva, alagamento e risco.

Você deve agir como um especialista em clima e gestão de riscos urbanos, com foco na cidade do Recife.

Regras obrigatórias:
- NÃO use markdown
- NÃO use formatação com asteriscos, hashtags ou listas
- Escreva em linguagem simples e direta
- Seja objetivo e claro
- Fale como um sistema oficial de alerta

Dados atuais:
Temperatura: {weather_data['temp']} °C
Chuva atual: {weather_data['rain']} mm
Umidade: {weather_data['humidity']} %
Chuva acumulada: {weather_data['total_rain']} mm
Pico de chuva: {weather_data['max_rain']} mm/h
Classificação de risco: {risk}

Explique a situação e diga o que a população deve fazer.
"""

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # 🔁 retry automático
    tentativas = 3

    for tentativa in range(tentativas):
        try:
            response = requests.post(
                url,
                params=params,
                json=body,
                timeout=10  # evita travar
            )

            data = response.json()

            # 🚨 erro da API
            if "error" in data:
                erro_msg = str(data["error"])

                # retry se for 503 (sobrecarga)
                if "503" in erro_msg or "UNAVAILABLE" in erro_msg:
                    print(f"Tentativa {tentativa + 1} falhou (503)...")
                    time.sleep(2)
                    continue

                return {
                    "risk": "ERRO",
                    "analysis": f"Erro da API: {data['error']}"
                }

            # ✅ sucesso
            if "candidates" in data:
                return {
                    "risk": risk,
                    "analysis": data["candidates"][0]["content"]["parts"][0]["text"]
                }

        except requests.exceptions.Timeout:
            print(f"Timeout na tentativa {tentativa + 1}")
            time.sleep(2)

        except Exception as e:
            return {
                "risk": "ERRO",
                "analysis": f"Erro inesperado: {str(e)}"
            }

    # ⚠️ fallback final
    return {
        "risk": risk,
        "analysis": "Sistema temporariamente indisponível devido à alta demanda. Tente novamente em instantes."
    }