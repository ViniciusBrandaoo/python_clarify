import turtle  # Importa a biblioteca gráfica Turtle para desenhar o jogo
import random  # Importa a biblioteca Random para gerar posições aleatórias para a fruta
import time  # Importa a biblioteca Time para controlar a velocidade e o tempo do jogo

# Configuração da janela do jogo
tela = turtle.Screen()  # Cria a tela do jogo
tela.title("Jogo da Cobrinha - Nokia3310")  # Define o título da janela
tela.bgcolor("black")  # Define a cor de fundo da tela como preta
tela.setup(width=600, height=600)  # Define a largura e altura da janela (600x600 pixels)
tela.tracer(0)  # Desativa as animações automáticas da tela para o jogo rodar mais fluido

# Inicialização das variáveis de controle do jogo
pontos = 0  # Cria a variável para armazenar a pontuação inicial do jogador
tempo_inicial = time.time()  # Registra o momento exato em que o jogo começou
segmentos_corpo = []  # Lista vazia que vai guardar os pedaços do corpo da cobra

# Configuração da Cabeça da Cobrinha
cobra = turtle.Turtle()  # Cria o objeto da cabeça da cobrinha
cobra.speed(0)  # Define a velocidade de animação do objeto como a mais rápida (imediata)
cobra.shape("square")  # Define o formato da cabeça como um quadrado
cobra.color("violet")  # Define a cor da cabeça como violeta
cobra.penup()  # Levanta a caneta para que a cobrinha não desenhe uma linha por onde passar
cobra.goto(0, 0)  # Posiciona a cobrinha no centro da tela (coordenadas 0,0)
cobra.direcao = "parado"  # Define a direção inicial da cobrinha como parada

# Configuração da Fruta
fruta = turtle.Turtle()  # Cria o objeto da fruta
fruta.speed(0)  # Define a velocidade de animação do objeto como a mais rápida
fruta.shape("circle")  # Define o formato da fruta como um círculo
fruta.color("green")  # Define a cor da fruta como verde
fruta.penup()  # Levanta a caneta para a fruta não desenhar linhas na tela
fruta.goto(0, 100)  # Posiciona a fruta em uma posição inicial na tela

# Configuração do Texto do Placar (Pontuação e Tempo no topo)
placar = turtle.Turtle()  # Cria um objeto turtle invisível apenas para escrever texto
placar.speed(0)  # Define a velocidade de renderização como imediata
placar.color("white")  # Define a cor do texto como branca
placar.penup()  # Levanta a caneta para não riscar a tela ao se mover
placar.hideturtle()  # Esconde a seta do objeto, deixando apenas o texto visível
placar.goto(0, 260)  # Posiciona o placar centralizado na parte superior da tela
placar.write(
    "Pontos: 0  |  Tempo: 0s", align="center", font=("Courier", 16, "bold")
)


# Funções para mudar a direção da cobrinha (evitam que ela volte para trás direto)
def ir_para_cima():
    """Muda a direção para cima, se não estiver indo para baixo."""
    if cobra.direcao != "baixo":
        cobra.direcao = "cima"


def ir_para_baixo():
    """Muda a direção para baixo, se não estiver indo para cima."""
    if cobra.direcao != "cima":
        cobra.direcao = "baixo"


def ir_para_direita():
    """Muda a direção para a direita, se não estiver indo para a esquerda."""
    if cobra.direcao != "esquerda":
        cobra.direcao = "direita"


def ir_para_esquerda():
    """Muda a direção para a esquerda, se não estiver indo para a direita."""
    if cobra.direcao != "direita":
        cobra.direcao = "esquerda"


# Configuração dos controles do teclado
tela.listen()  # Diz para a tela ficar "ouvindo" os comandos do teclado
tela.onkeypress(ir_para_cima, "Up")  # Associa a seta para CIMA à função ir_para_cima
tela.onkeypress(ir_para_baixo, "Down")  # Associa a seta para BAIXO à função ir_para_baixo
tela.onkeypress(ir_para_esquerda, "Left")  # Associa a seta para ESQUERDA à função ir_para_esquerda
tela.onkeypress(ir_para_direita, "Right")  # Associa a seta para DIREITA à função ir_para_direita


# Função para movimentar a cabeça da cobrinha com base na direção atual
def mover():
    if cobra.direcao == "cima":
        y = cobra.ycor()  # Pega a coordenada Y atual da cobrinha
        cobra.sety(y + 20)  # Move a cobrinha 20 pixels para cima

    if cobra.direcao == "baixo":
        y = cobra.ycor()  # Pega a coordenada Y atual da cobrinha
        cobra.sety(y - 20)  # Move a cobrinha 20 pixels para baixo

    if cobra.direcao == "esquerda":
        x = cobra.xcor()  # Pega a coordenada X atual da cobrinha
        cobra.setx(x - 20)  # Move a cobrinha 20 pixels para a esquerda

    if cobra.direcao == "direita":
        x = cobra.xcor()  # Pega a coordenada X atual da cobrinha
        cobra.setx(x + 20)  # Move a cobrinha 20 pixels para a direita


# Loop principal do jogo (O coração do aplicativo)
while True:
    tela.update()  # Atualiza a tela manualmente (necessário porque o tracer está em 0)

    # Verifica colisão com as bordas da tela (Game Over)
    if (
        cobra.xcor() > 290
        or cobra.xcor() < -290
        or cobra.ycor() > 290
        or cobra.ycor() < -290
    ):
        tela.title(f"GAME OVER! Pontuação Final: {pontos}")  # Exibe a pontuação final no título da janela
        time.sleep(1)  # Pausa o jogo por 1 segundo para o jogador notar a derrota
        break  # Sai do loop principal e encerra o jogo

    # Verifica a colisão da cobrinha com a fruta (distância menor que 20 pixels)
    if cobra.distance(fruta) < 20:
        x = random.randint(-270, 270)  # Gera uma coordenada X aleatória segura dentro da tela
        y = random.randint(-270, 250)  # Gera uma coordenada Y aleatória (evitando o placar)
        fruta.goto(x, y)  # Move a fruta para a nova posição aleatória
        pontos += 10  # Aumenta a pontuação do jogador em 10 pontos

        # Criação de um novo pedaço para o corpo da cobra crescer
        novo_segmento = turtle.Turtle()  # Cria um novo objeto turtle para o corpo
        novo_segmento.speed(0)  # Define a velocidade de animação imediata
        novo_segmento.shape("square")  # Define o formato como quadrado (igual à cabeça)
        novo_segmento.color("orchid")  # Define uma cor levemente diferente para o corpo
        novo_segmento.penup()  # Levanta a caneta do novo pedaço
        segmentos_corpo.append(novo_segmento)  # Adiciona esse pedaço na lista de segmentos

    # Movimentação do corpo da cobra (em ordem reversa, do último pedaço até o primeiro)
    # Cada pedaço vai para a posição onde o pedaço da frente dele estava
    for indice in range(len(segmentos_corpo) - 1, 0, -1):
        x = segmentos_corpo[indice - 1].xcor()  # Pega o X do pedaço da frente
        y = segmentos_corpo[indice - 1].ycor()  # Pega o Y do pedaço da frente
        segmentos_corpo[indice].goto(x, y)  # Move o pedaço atual para lá

    # Move o primeiríssimo pedaço do corpo para onde a cabeça está atualmente
    if len(segmentos_corpo) > 0:
        x = cobra.xcor()  # Pega o X da cabeça
        y = cobra.ycor()  # Pega o Y da cabeça
        segmentos_corpo[0].goto(x, y)  # Move o primeiro pedaço do corpo para o lugar da cabeça

    mover()  # Chama a função que faz a cabeça da cobra andar um passo para frente

    # Verifica se a cabeça colidiu com o próprio corpo (Game Over)
    for segmento in segmentos_corpo:
        if segmento.distance(cobra) < 20:  # Se a cabeça estiver em cima de qualquer pedaço do corpo
            tela.title(f"GAME OVER! Você bateu em si mesmo. Pontos: {pontos}")
            time.sleep(1)  # Aguarda 1 segundo
            break  # Interrompe o loop se bateu em si mesma (a checagem do while vai fechar no próximo ciclo)

    # Atualiza o tempo decorrido e o texto do placar no topo da tela
    tempo_decorrido = int(time.time() - tempo_inicial)  # Calcula quantos segundos se passaram desde o início
    placar.clear()  # Limpa o texto anterior do placar para não sobrepor
    placar.write(
        f"Pontos: {pontos}  |  Tempo: {tempo_decorrido}s",
        align="center",
        font=("Courier", 16, "bold"),
    )  # Escreve o placar atualizado

    time.sleep(0.1)  # Pausa o código por 0.1 segundos para controlar a velocidade geral do jogo