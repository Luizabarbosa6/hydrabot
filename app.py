from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from weather import get_weather
from ai import analyze_weather, classify_risk

app = FastAPI()

# 🔓 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "HydraRec API funcionando"}


@app.get("/alerta")
def alerta(bairro: str = Query(..., description="Nome do bairro do Recife")):
    try:
        # 🌧️ buscar clima
        weather = get_weather(bairro)

        if "error" in weather:
            return {
                "weather": None,
                "analysis": {
                    "risk": "ERRO",
                    "analysis": weather["error"]
                }
            }

        # 🧠 classificação básica (backup)
        risk = classify_risk(weather)

        # 🤖 SEMPRE chama a IA
        analysis = analyze_weather(weather)

        # 🔥 fallback se IA falhar
        if not analysis or analysis.get("risk") == "ERRO":
            return {
                "weather": weather,
                "analysis": {
                    "risk": risk,
                    "analysis": f"O bairro {bairro} apresenta risco {risk.lower()} de alagamento no momento. As condições climáticas indicam atenção, principalmente em áreas com histórico de acúmulo de água. Recomenda-se evitar locais propensos a alagamentos e acompanhar novas atualizações."
                }
            }

        return {
            "weather": weather,
            "analysis": analysis
        }

    except Exception as e:
        return {
            "weather": None,
            "analysis": {
                "risk": "ERRO",
                "analysis": "Sistema temporariamente indisponível. Tente novamente."
            }
        }