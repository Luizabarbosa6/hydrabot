from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from weather import get_weather
from ai import analyze_weather, classify_risk

app = FastAPI()

# 🔓 CORS (liberado para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois pode restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "HydraRec API funcionando"}

@app.get("/alerta")
def alerta():
    try:
        # 🌧️ pegar clima
        weather = get_weather()

        if not weather:
            return {
                "weather": None,
                "analysis": {
                    "risk": "ERRO",
                    "analysis": "Erro ao obter dados meteorológicos."
                }
            }

        # 🧠 risco básico (sem IA)
        risk = classify_risk(weather)

        # ⚡ evita gastar API à toa
        if risk == "BAIXO":
            return {
                "weather": weather,
                "analysis": {
                    "risk": "BAIXO",
                    "analysis": "Risco baixo de alagamento no momento. Situação estável."
                }
            }

        # 🤖 chama IA só quando necessário
        analysis = analyze_weather(weather)

        # 🔥 fallback se IA falhar
        if analysis.get("risk") == "ERRO":
            return {
                "weather": weather,
                "analysis": {
                    "risk": risk,
                    "analysis": f"Risco {risk.lower()} de alagamento no Recife. Fique atento às condições climáticas."
                }
            }

        return {
            "weather": weather,
            "analysis": analysis
        }

    except Exception as e:
        # 💣 nunca deixa quebrar (resolve CORS falso)
        return {
            "weather": None,
            "analysis": {
                "risk": "ERRO",
                "analysis": "Sistema temporariamente indisponível. Tente novamente."
            }
        }