import pygame
import random

pygame.init()

# Defina as dimensões da tela e a velocidade da pista
largura = 713
altura = 525
velocidade_pista = 5
velocidade_entidades = 2  # Velocidade dos objetivos e obstáculos
pontuacao = 0

# Inicialize a tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo de Carro")

# Carregue as imagens do carro, da pista e dos objetivos pares
carro1 = pygame.image.load("carro1.png")
pista = pygame.image.load("floresta6.png")
objetivo_par1 = pygame.transform.scale(pygame.image.load('N2.png'), (30, 30))
objetivo_par2 = pygame.transform.scale(pygame.image.load('N4.png'), (30, 30))
objetivo_par3 = pygame.transform.scale(pygame.image.load('N6.png'), (30, 30))
objetivo_par4 = pygame.transform.scale(pygame.image.load('N8.png'), (30, 30))

# Carregue as imagens dos obstáculos ímpares
obstaculo_impar1 = pygame.transform.scale(pygame.image.load('N1.png'), (30, 30))
obstaculo_impar2 = pygame.transform.scale(pygame.image.load('N3.png'), (30, 30))
obstaculo_impar3 = pygame.transform.scale(pygame.image.load('N5.png'), (30, 30))
obstaculo_impar4 = pygame.transform.scale(pygame.image.load('N7.png'), (30, 30))
obstaculo_impar5 = pygame.transform.scale(pygame.image.load('N9.png'), (30, 30))

# Obtenha as dimensões do carro
carro1_rect = carro1.get_rect()

# Posicione o carro no centro da tela horizontalmente
x = largura // 2 - carro1_rect.width // 2
y = altura - carro1_rect.height - 20  # Posicione o carro na parte inferior

# Inicialize o relógio
relogio = pygame.time.Clock()

# Inicialize a posição da pista
posicao_pista = 0

# Inicialize todas as entidades (objetivos e obstáculos) em uma lista
entidades = []

# Adicione os objetivos pares à lista
entidades.extend([
    {'image': objetivo_par1, 'rect': pygame.Rect(0, 0, 30, 30), 'valor': 2},
    {'image': objetivo_par2, 'rect': pygame.Rect(0, 0, 30, 30), 'valor': 4},
    {'image': objetivo_par3, 'rect': pygame.Rect(0, 0, 30, 30), 'valor': 6},
    {'image': objetivo_par4, 'rect': pygame.Rect(0, 0, 30, 30), 'valor': 8}
])

# Adicione os obstáculos ímpares à lista
entidades.extend([
    {'image': obstaculo_impar1, 'rect': pygame.Rect(0, 0, 30, 30)},
    {'image': obstaculo_impar2, 'rect': pygame.Rect(0, 0, 30, 30)},
    {'image': obstaculo_impar3, 'rect': pygame.Rect(0, 0, 30, 30)},
    {'image': obstaculo_impar4, 'rect': pygame.Rect(0, 0, 30, 30)},
    {'image': obstaculo_impar5, 'rect': pygame.Rect(0, 0, 30, 30)}
])

# Embaralhe a ordem das entidades
random.shuffle(entidades)

# Variáveis para armazenar as posições dos objetivos atingidos
posicoes_objetivos_atingidos = set()

# Modo pontuação (o jogador só marca pontos com números pares)
modo_pontuacao = True

# Tempo máximo de jogo
tempo_maximo_jogo = float('inf')  # Infinito

# Função para inicializar as posições iniciais das entidades
def inicializar_entidades_com_menos_obstaculos():
    y_offset = -400
    for entidade in entidades:
        entidade['rect'].x = random.randint(270, 420)
        entidade['rect'].y = y_offset
        y_offset -= random.randint(200, 400)  # Ajuste aqui para diminuir a aparição dos obstáculos

# Função para verificar a colisão com os obstáculos
def colisao_obstaculo():
    for entidade in entidades[len(entidades)//2:]:
        if entidade['rect'].colliderect(carro1_rect):
            return True
    return False

# game over
def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'(Game Over!)'
    texto_formatado = fonte.render(mensagem, True, cor)
    tela.blit(texto_formatado, (largura // 2 - 150, altura // 2 - 50))
    pygame.display.update()
    pygame.time.delay(2000)

# Inicialize as posições iniciais das entidades
inicializar_entidades_com_menos_obstaculos()

# Loop principal do jogo
tela_aberta = True
while tela_aberta:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tela_aberta = False

    comandos = pygame.key.get_pressed()
    if comandos[pygame.K_RIGHT] and x <= 420:
        x += velocidade_pista
    if comandos[pygame.K_LEFT] and x >= 270:
        x -= velocidade_pista

    # Atualize o retângulo do carro com a posição mais recente
    carro1_rect.x = x
    carro1_rect.y = y

    # Desloque a pista para baixo para criar a ilusão de movimento vertical
    posicao_pista += velocidade_pista
    if posicao_pista > altura:
        posicao_pista = 0

    # Atualize as posições das entidades (objetivos e obstáculos)
    for entidade in entidades:
        entidade['rect'].y += velocidade_pista  # Mova as entidades com a pista
        if entidade['rect'].y > altura:
            entidade['rect'].y = -30
            entidade['rect'].x = random.randint(270, 420)  # Reposicione a entidade acima da tela

    # Verifique se o jogador colidiu com os obstáculos ímpares
    if modo_pontuacao and colisao_obstaculo():
        exibe_mensagem("Game Over! Você colidiu com um obstáculo ímpar!", 40, (255, 0, 0))
        modo_pontuacao = False
        tempo_maximo_jogo = pygame.time.get_ticks() + 2000
        # Ajuste para inicializar as entidades acima da tela
        for entidade in entidades:
            entidade['rect'].y = -30
            entidade['rect'].x = random.randint(270, 420)
        posicoes_objetivos_atingidos.clear()
        pygame.time.delay(2000)

    # Verifique se o jogador encostou em qualquer objetivo par
    for i, entidade in enumerate(entidades[:len(entidades) // 2]):
        if modo_pontuacao and entidade['rect'].colliderect(carro1_rect) and i not in posicoes_objetivos_atingidos:
            posicoes_objetivos_atingidos.add(i)
            pontuacao += 1  # Acumula 1 ponto por qualquer objetivo par atingido

    # Verifique se o jogador colidiu com um número ímpar
    for entidade in entidades[len(entidades) // 2:]:
        if modo_pontuacao and entidade['rect'].colliderect(carro1_rect):
            exibe_mensagem("Game Over! Você colidiu com um obstáculo ímpar!", 40, (255, 0, 0))
            modo_pontuacao = False
            tempo_maximo_jogo = pygame.time.get_ticks() + 2000
            # Ajuste para inicializar as entidades acima da tela
            for entidade in entidades:
                entidade['rect'].y = -30
                entidade['rect'].x = random.randint(270, 420)
            posicoes_objetivos_atingidos.clear()
            pygame.time.delay(2000)

    # Verifique o tempo de jogo e reinicie se o tempo máximo foi atingido
    if pygame.time.get_ticks() > tempo_maximo_jogo:
        modo_pontuacao = True
        tempo_maximo_jogo = float('inf')
        inicializar_entidades_com_menos_obstaculos()

    # Desenhe a pista continuamente, deslocando-a
    tela.blit(pista, (0, posicao_pista))
    tela.blit(pista, (0, posicao_pista - altura))
    tela.blit(carro1, (x, y))

    # Desenha todas as entidades
    for entidade in entidades:
        tela.blit(entidade['image'], (entidade['rect'].x, entidade['rect'].y))

    # Exiba a pontuação na tela
    fonte_pontuacao = pygame.font.SysFont('comicsansms', 30, True, False)
    texto_pontuacao = fonte_pontuacao.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
    tela.blit(texto_pontuacao, (10, 10))

    pygame.display.update()
    relogio.tick(30)
