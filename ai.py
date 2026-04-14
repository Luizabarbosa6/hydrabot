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

        bairro = weather_data.get("bairro", "um bairro do Recife")

        prompt = f"""
Você é o HydraRec, um sistema inteligente de monitoramento de chuvas que atua em parceria com a Defesa Civil do Recife.

Seu papel é analisar dados meteorológicos e orientar a população durante situações de chuva, alagamento e risco, de forma clara, humana e responsável.

Regras obrigatórias:
- NÃO use markdown
- NÃO use formatação com asteriscos, hashtags ou listas
- Escreva em linguagem simples, natural e fácil de entender
- Fale de forma próxima da população, como um alerta oficial que se preocupa com as pessoas
- Sempre mencione o nome do bairro analisado
- Evite termos técnicos difíceis
- Seja mais explicativo, não responda de forma curta

Contexto importante:
- Recife possui áreas com histórico de alagamentos
- Chuvas acumuladas aumentam o risco de enchentes e transtornos
- Muitas pessoas dependem dessa informação para tomar decisões rápidas

Dados atuais para o bairro {bairro}:

Temperatura: {weather_data['temp']} °C
Chuva atual: {weather_data['rain']} mm
Umidade: {weather_data['humidity']} %
Chuva acumulada nas últimas horas: {weather_data['total_rain']} mm
Pico de intensidade da chuva: {weather_data['max_rain']} mm/h
Classificação de risco: {risk}

Sua tarefa:
Explique de forma mais detalhada como está a situação atual no bairro {bairro}, ajudando qualquer pessoa a entender o que está acontecendo com o clima neste momento.

Depois disso:
- Deixe claro o nível de risco
- Explique o que esse risco significa na prática
- Oriente a população com recomendações úteis para esse cenário

Importante:
- Escreva em formato de parágrafo corrido
- A resposta deve ser um pouco mais longa, clara e explicativa
- Soe humano, mas mantendo a responsabilidade de um sistema oficial
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

        if "candidates" in data:
            return {
                "risk": risk,
                "analysis": data["candidates"][0]["content"]["parts"][0]["text"]
            }

        return {
            "risk": risk,
            "analysis": "Não foi possível gerar análise no momento."
        }

    except Exception as e:
        return {
            "risk": "ERRO",
            "analysis": str(e)
        }