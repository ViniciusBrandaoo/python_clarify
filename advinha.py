from random import randint
import time

print("=" * 50)
print("🎯      JOGO DA ADIVINHAÇÃO SUPREMO      🎯")
print("=" * 50)

# Configurações
TEMPO_LIMITE = 30  # segundos
numero_secreto = randint(0, 100)
chances = 10
tentativas = []

inicio = time.time()

print(f"\n⏳ Você tem {TEMPO_LIMITE} segundos para descobrir o número!")
print("🎲 O número secreto está entre 0 e 100.")
print(f"❤️ Chances disponíveis: {chances}\n")

while chances > 0:

    tempo_decorrido = int(time.time() - inicio)
    tempo_restante = TEMPO_LIMITE - tempo_decorrido

    if tempo_restante <= 0:
        print("\n⏰ TEMPO ESGOTADO!")
        print(f"💀 Você perdeu! O número era {numero_secreto}.")
        break

    print("-" * 50)
    print(f"⏳ Tempo restante: {tempo_restante}s")
    print(f"❤️ Chances restantes: {chances}")

    chute = input("👉 Digite seu chute: ")

    if not chute.isnumeric():
        print("❌ Digite apenas números!")
        continue

    chute = int(chute)
    tentativas.append(chute)
    chances -= 1

    distancia = abs(numero_secreto - chute)

    if chute == numero_secreto:

        tempo_total = round(time.time() - inicio, 2)

        print("\n" + "=" * 50)
        print("🎉 PARABÉNS! VOCÊ VENCEU!")
        print("=" * 50)

        print(f"🎯 Número secreto: {numero_secreto}")
        print(f"⏱️ Tempo gasto: {tempo_total} segundos")
        print(f"📊 Tentativas realizadas: {len(tentativas)}")
        print(f"❤️ Chances restantes: {chances}")

        # Ranking
        if chances >= 8:
            titulo = "🏆 LENDA DOS NÚMEROS"
        elif chances >= 5:
            titulo = "🥇 MESTRE DA ADIVINHAÇÃO"
        elif chances >= 2:
            titulo = "🥈 ESPECIALISTA"
        else:
            titulo = "🥉 SOBREVIVENTE"

        print(f"\nSeu título: {titulo}")

        # Pontuação
        pontuacao = (chances * 100) + max(0, tempo_restante * 5)

        print(f"⭐ Pontuação final: {pontuacao}")

        print("\n📜 Histórico de tentativas:")
        print(tentativas)

        break

    else:

        if chute > numero_secreto:
            print("⬇️ O número secreto é MENOR.")
        else:
            print("⬆️ O número secreto é MAIOR.")

        # Sistema quente/frio
        if distancia <= 3:
            print("🔥 FERVENDO! Você está muito perto!")
        elif distancia <= 10:
            print("🌡️ QUENTE!")
        elif distancia <= 20:
            print("❄️ FRIO!")
        else:
            print("🧊 MUITO FRIO!")

        # Informação estratégica
        menor = min(tentativas)
        maior = max(tentativas)

        print(f"📌 Menor chute: {menor}")
        print(f"📌 Maior chute: {maior}")

        # Evento especial aleatório
        evento = randint(1, 20)

        if evento == 1:
            chances += 1
            print("🎁 Evento Especial: Você ganhou 1 chance extra!")

        elif evento == 2:
            if numero_secreto % 2 == 0:
                print("🔍 Dica Bônus: O número é PAR.")
            else:
                print("🔍 Dica Bônus: O número é ÍMPAR.")

        print()

else:
    print("\n💀 Suas chances acabaram!")
    print(f"🎯 O número era {numero_secreto}")

print("\n" + "=" * 50)
print("📈 RELATÓRIO FINAL")
print("=" * 50)

if tentativas:
    print(f"🎲 Número secreto: {numero_secreto}")
    print(f"📊 Total de tentativas: {len(tentativas)}")
    print(f"📉 Menor chute: {min(tentativas)}")
    print(f"📈 Maior chute: {max(tentativas)}")
    print(f"📝 Histórico: {tentativas}")

print("\nObrigado por jogar!")
print("=" * 50)
