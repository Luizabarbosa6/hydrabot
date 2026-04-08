import requests
import os
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
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

        params = {
            "key": os.getenv("GEMINI_API_KEY")
        }

        risk = classify_risk(weather_data)

        prompt = f"""
Você é o HydraRec, um sistema inteligente de monitoramento de chuvas que atua em parceria com a Defesa Civil do Recife.

Seu papel é analisar dados meteorológicos e orientar a população durante situações de chuva, alagamento e risco.

Você deve agir como um especialista em clima e gestão de riscos urbanos, com foco na cidade do Recife, considerando sua vulnerabilidade a alagamentos e deslizamentos.

Regras obrigatórias:
- NÃO use markdown
- NÃO use formatação com asteriscos, hashtags ou listas
- Escreva em linguagem simples e direta
- Seja objetivo e claro
- Fale como um sistema oficial de alerta
- Evite termos técnicos difíceis
- Sempre traga orientação prática para a população

Contexto importante:
- Recife possui áreas de risco com drenagem limitada
- Chuvas acumuladas aumentam o risco de alagamentos
- A população precisa de instruções claras e rápidas

Dados atuais:
Temperatura: {weather_data['temp']} °C
Chuva atual: {weather_data['rain']} mm
Umidade: {weather_data['humidity']} %
Chuva acumulada nas últimas horas: {weather_data['total_rain']} mm
Pico de intensidade da chuva: {weather_data['max_rain']} mm/h
Classificação de risco: {risk}

Sua tarefa:
Explique a situação atual de forma clara e objetiva para a população do Recife.
Informe o nível de risco e o que as pessoas devem fazer agora.

Formato da resposta:
- Comece informando o nível de risco
- Explique brevemente a situação
- Dê instruções práticas

Exemplo de tom esperado:
"Risco médio de alagamento em Recife. A chuva acumulada nas últimas horas aumenta a possibilidade de pontos de alagamento. Evite áreas baixas e fique atento a novos alertas da Defesa Civil."
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

        response = requests.post(url, params=params, json=body)
        data = response.json()

        # 🔍 DEBUG (pode remover depois)
        if "error" in data:
            return {
                "risk": "ERRO",
                "analysis": f"Erro da API: {data['error']}"
            }

        # ✅ resposta correta
        if "candidates" in data:
            return {
                "risk": risk,
                "analysis": data["candidates"][0]["content"]["parts"][0]["text"]
            }

        # ⚠️ fallback
        return {
            "risk": risk,
            "analysis": "Não foi possível gerar análise no momento."
        }

    except Exception as e:
        return {
            "risk": "ERRO",
            "analysis": f"Erro ao analisar dados: {str(e)}"
        }