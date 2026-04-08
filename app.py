from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from weather import get_weather
from ai import analyze_weather

app = FastAPI()

# 🔓 CONFIGURAÇÃO DE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # libera tudo (ideal pra teste)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "HydraRec API funcionando"}

@app.get("/alerta")
def alerta():
    weather = get_weather()
    analysis = analyze_weather(weather)

    return {
        "weather": weather,
        "analysis": analysis
    }