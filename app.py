from fastapi import FastAPI
from weather import get_weather
from ai import analyze_weather

app = FastAPI()

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