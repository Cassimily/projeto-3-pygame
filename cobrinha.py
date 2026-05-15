
import pygame
import random
import sys

pygame.init()

# ---------------- CONFIGURAÇÕES ----------------
LARGURA = 800
ALTURA = 600
TAMANHO_BLOCO = 20
FPS = 10

# ---------------- CORES ----------------
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE_CLARO = (170, 255, 170)
VERDE_GRID = (140, 220, 140)
AZUL = (0, 100, 255)
VERMELHO = (255, 0, 0)
CINZA = (180, 180, 180)

# Cobra rainbow
CORES_COBRA = [
    (255, 0, 0),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (128, 0, 128)
]

# ---------------- FONTES ----------------
fonte_titulo = pygame.font.SysFont("Arial", 50, bold=True)
fonte_menu = pygame.font.SysFont("Arial", 30)
fonte_pontos = pygame.font.SysFont("Arial", 35)

# ---------------- TELA ----------------
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake Premium")

relogio = pygame.time.Clock()

# ---------------- FUNÇÕES ----------------

def desenhar_grade():

    for x in range(0, LARGURA, TAMANHO_BLOCO):
        pygame.draw.line(tela, VERDE_GRID, (x, 0), (x, ALTURA))

    for y in range(0, ALTURA, TAMANHO_BLOCO):
        pygame.draw.line(tela, VERDE_GRID, (0, y), (LARGURA, y))

def desenhar_texto(texto, fonte, cor, x, y):

    render = fonte.render(texto, True, cor)
    tela.blit(render, (x, y))

def gerar_comidas(cobra, quantidade):

    comidas = []

    while len(comidas) < quantidade:

        x = random.randrange(0, LARGURA - TAMANHO_BLOCO, TAMANHO_BLOCO)
        y = random.randrange(60, ALTURA - TAMANHO_BLOCO, TAMANHO_BLOCO)

        if [x, y] not in cobra and [x, y] not in comidas:
            comidas.append([x, y])

    return comidas

def tela_inicial():

    while True:

        tela.fill(VERDE_CLARO)

        desenhar_texto(
        "BEM-VINDO AO JOGO DA COBRINHA",
            fonte_titulo,
            PRETO,
            60,
            120
        )

        desenhar_texto(
            "Escolha quantas comidas quer no jogo👇:",
            fonte_menu,
            PRETO,
            180,
            250
        )

        desenhar_texto("1 - Uma comida", fonte_menu, PRETO, 280, 330)
        desenhar_texto("2 - Cinco comidas", fonte_menu, PRETO, 280, 380)
        desenhar_texto("3 - Dez comidas", fonte_menu, PRETO, 280, 430)

        pygame.display.update()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_1:
                    return 1

                elif evento.key == pygame.K_2:
                    return 5

                elif evento.key == pygame.K_3:
                    return 10

def tela_game_over(pontos):

    while True:

        tela.fill(PRETO)

        desenhar_texto(
            "GAME OVER",
            fonte_titulo,
            VERMELHO,
            250,
            180
        )

        desenhar_texto(
            f"PONTOS: {pontos}",
            fonte_menu,
            BRANCO,
            320,
            280
        )

        desenhar_texto(
            "R - Jogar novamente",
            fonte_menu,
            BRANCO,
            250,
            380
        )

        desenhar_texto(
            "ESC - Fechar jogo",
            fonte_menu,
            BRANCO,
            250,
            440
        )

        pygame.display.update()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_r:
                    main()

                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():

    quantidade_comidas = tela_inicial()

    cobra = [[LARGURA // 2, ALTURA // 2]]

    direcao = (0, 0)

    comidas = gerar_comidas(cobra, quantidade_comidas)

    pontos = 0

    while True:

        # ---------------- EVENTOS ----------------
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_UP and direcao != (0, TAMANHO_BLOCO):
                    direcao = (0, -TAMANHO_BLOCO)

                elif evento.key == pygame.K_DOWN and direcao != (0, -TAMANHO_BLOCO):
                    direcao = (0, TAMANHO_BLOCO)

                elif evento.key == pygame.K_LEFT and direcao != (TAMANHO_BLOCO, 0):
                    direcao = (-TAMANHO_BLOCO, 0)

                elif evento.key == pygame.K_RIGHT and direcao != (-TAMANHO_BLOCO, 0):
                    direcao = (TAMANHO_BLOCO, 0)

        # ---------------- MOVIMENTO ----------------
        if direcao != (0, 0):

            nova_cabeca = [
                cobra[0][0] + direcao[0],
                cobra[0][1] + direcao[1]
            ]

            # Colisão
            if (
                nova_cabeca[0] < 0 or
                nova_cabeca[0] >= LARGURA or
                nova_cabeca[1] < 60 or
                nova_cabeca[1] >= ALTURA or
                nova_cabeca in cobra
            ):
                tela_game_over(pontos)

            cobra.insert(0, nova_cabeca)

            comeu = False

            for comida in comidas:

                if nova_cabeca == comida:

                    comidas.remove(comida)

                    comidas.extend(gerar_comidas(cobra, 1))

                    pontos += 1

                    comeu = True

                    break

            if not comeu:
                cobra.pop()

        # ---------------- DESENHO ----------------
        tela.fill(VERDE_CLARO)

        desenhar_grade()

        # Barra cinza superior
        pygame.draw.rect(
            tela,
            CINZA,
            (0, 0, LARGURA, 60)
        )

        # Comidas
        for comida in comidas:

            pygame.draw.circle(
                tela,
                AZUL,
                (
                    comida[0] + TAMANHO_BLOCO // 2,
                    comida[1] + TAMANHO_BLOCO // 2
                ),
                TAMANHO_BLOCO // 2
            )

        # Cobra colorida
        for i, segmento in enumerate(cobra):

            cor = CORES_COBRA[i % len(CORES_COBRA)]

            pygame.draw.rect(
                tela,
                cor,
                (
                    segmento[0],
                    segmento[1],
                    TAMANHO_BLOCO,
                    TAMANHO_BLOCO
                )
            )

        # Pontuação
        desenhar_texto(
            f"PONTOS: {pontos}",
            fonte_pontos,
            PRETO,
            20,
            10
        )

        pygame.display.update()

        relogio.tick(FPS)

# ---------------- INICIAR ----------------
main()
