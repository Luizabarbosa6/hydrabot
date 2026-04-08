from weather import get_weather
from ai import analyze_weather

def main():
    weather = get_weather()
    
    print("🌧️ Dados atuais:")
    print(weather)

    analysis = analyze_weather(weather)

    print("\n🧠 Análise do risco:")
    print(analysis)

if __name__ == "__main__":
    main()