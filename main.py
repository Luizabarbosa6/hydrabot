from weather import get_weather
from ai import analyze_weather

def main():
    bairro = "Boa Viagem"

    weather = get_weather(bairro)

    print("🌧️ Dados atuais:")
    print(weather)

    if "error" not in weather:
        analysis = analyze_weather(weather)

        print("\n🧠 Análise do risco:")
        print(analysis)
    else:
        print("Erro:", weather["error"])

if __name__ == "__main__":
    main()