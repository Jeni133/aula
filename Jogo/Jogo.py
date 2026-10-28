import pygame
import random
import sys

pygame.init()

# Configurações da Janela
LARGURA = 1295
ALTURA = 750
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Batalha Pokémon - Interface Alinhada")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_CLARO = (220, 220, 220)
CINZA_ESCURO = (50, 50, 50)
VERDE = (46, 204, 113)   # Você (Player)
AZUL = (52, 152, 219)    # Inimigo
VERMELHO = (231, 76, 60)

# Fontes
fonte_interface = pygame.font.Font(None, 32)
fonte_status = pygame.font.Font(None, 28)
fonte_aviso = pygame.font.Font(None, 24)

# Nomes dos Combatentes
nome_player = "VERDE"
nome_inimigo = "AZUL"

# Atributos dos "Pokémons"
player_hp = 100
inimigo_hp = 100

# Lista de Ataques (Nome, Dano)
ataques = [
    {"nome": "1. Investida", "dano": 15, "limite": 15, "efeito": "bonus"},
    {"nome": "2. Folha Navalha", "dano": 25, "limite": 10, "efeito": "critico"},
    {"nome": "3. Ataque Rápido", "dano": 10, "limite": 25, "efeito": "esquiva"},
    {"nome": "4. Auto-Cura", "dano": -20, "limite": 15, "efeito": "cura"}
]

ataques_inimigo = [
    {"nome": "Pulso Dragão", "dano": 15, "limite": 15, "efeito": "bonus"},
    {"nome": "Jato d'Água", "dano": 25, "limite": 10, "efeito": "normal"},
    {"nome": "Mordida", "dano": 20, "limite": 25, "efeito": "critico"},
    {"nome": "Água-Sagrada", "dano": -15, "limite": 15, "efeito": "cura"}
]

for habilidade in ataques + ataques_inimigo:
    habilidade["usos"] = habilidade["limite"]

# Variáveis de Controle
turno_player = True
texto_painel = f"O que o {nome_player} vai fazer?"
jogo_acabou = False
esquiva_player = False

def resetar_batalha():
    global player_hp, inimigo_hp, turno_player, texto_painel, jogo_acabou, esquiva_player
    player_hp = 100
    inimigo_hp = 100
    turno_player = True
    texto_painel = f"O que o {nome_player} vai fazer?"
    jogo_acabou = False
    esquiva_player = False
    for habilidade in ataques + ataques_inimigo:
        habilidade["usos"] = habilidade["limite"]

relogio = pygame.time.Clock()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
        if evento.type == pygame.KEYDOWN:
            if jogo_acabou and evento.key == pygame.K_r:
                resetar_batalha()
            
            elif turno_player and not jogo_acabou:
                ataque_escolhido = None
                if evento.key == pygame.K_1: ataque_escolhido = ataques[0]
                elif evento.key == pygame.K_2: ataque_escolhido = ataques[1]
                elif evento.key == pygame.K_3: ataque_escolhido = ataques[2]
                elif evento.key == pygame.K_4: ataque_escolhido = ataques[3]
                    
                if ataque_escolhido:
                    if ataque_escolhido["usos"] <= 0:
                        texto_painel = f"{ataque_escolhido['nome'][3:]} acabou! Escolha outra habilidade."
                    else:
                        ataque_escolhido["usos"] -= 1
                        if ataque_escolhido["efeito"] == "cura":
                            cura = min(100 - player_hp, -ataque_escolhido["dano"])
                            player_hp += cura
                            texto_painel = f"{nome_player} usou Auto-Cura e recuperou {cura} HP!"
                        else:
                            dano = ataque_escolhido["dano"]
                            if ataque_escolhido["efeito"] == "bonus" and random.random() < 0.25:
                                dano += 10
                                texto_painel = f"Ataque especial! {ataque_escolhido['nome'][3:]} causou {dano} de dano!"
                            elif ataque_escolhido["efeito"] == "critico" and random.random() < 0.30:
                                dano *= 2
                                texto_painel = f"Acerto crítico! {ataque_escolhido['nome'][3:]} causou {dano} de dano!"
                            else:
                                texto_painel = f"{nome_player} usou {ataque_escolhido['nome'][3:]}! Causou {dano} de dano."
                            inimigo_hp -= dano
                            if ataque_escolhido["efeito"] == "esquiva":
                                esquiva_player = True
                                texto_painel += " Você poderá esquivar de parte do próximo golpe!"

                        if inimigo_hp <= 0:
                            inimigo_hp = 0
                            texto_painel = f"O {nome_inimigo} desmaiou! Vitória!"
                            jogo_acabou = True
                        elif not any(habilidade["usos"] > 0 for habilidade in ataques):
                            texto_painel = "Você ficou sem usos de habilidades. Derrota!"
                            jogo_acabou = True
                        else:
                            turno_player = False

    # Lógica do Turno do Inimigo
    if not turno_player and not jogo_acabou:
        pygame.time.wait(1)
        cura_disponivel = next(
            (ataque for ataque in ataques_inimigo
             if ataque["efeito"] == "cura" and ataque["usos"] > 0),
            None
        )
        if inimigo_hp <= 50 and cura_disponivel:
            ataque_inimigo = cura_disponivel
            ataque_inimigo["usos"] -= 1
            cura = min(100 - inimigo_hp, min(50, 20 + (50 - inimigo_hp)))
            inimigo_hp += cura
            texto_painel = f"O {nome_inimigo} usou Água-Sagrada e recuperou {cura} HP!"
        else:
            ataque_inimigo = max(
                (ataque for ataque in ataques_inimigo
                 if ataque["dano"] > 0 and ataque["usos"] > 0),
                key=lambda ataque: ataque["dano"],
                default=None
            )
            if ataque_inimigo:
                ataque_inimigo["usos"] -= 1
                dano = ataque_inimigo["dano"]
                if ataque_inimigo["efeito"] == "bonus" and random.random() < 0.25:
                    dano += 10
                elif ataque_inimigo["efeito"] == "critico" and random.random() < 0.30:
                    dano *= 2
                if esquiva_player:
                    dano = max(1, dano // 2)
                    esquiva_player = False
                    texto_painel = f"Você se esquivou parcialmente! {nome_inimigo} causou {dano} de dano."
                else:
                    texto_painel = f"O {nome_inimigo} usou {ataque_inimigo['nome']}! Causou {dano} de dano."
                player_hp -= dano
            else:
                texto_painel = f"O {nome_inimigo} ficou sem habilidades e perdeu o turno!"
        
        if player_hp <= 0:
            player_hp = 0
            texto_painel = f"Seu {nome_player} desmaiou... Você perdeu!"
            jogo_acabou = True
        
        turno_player = True

    # --- DESENHO NA TELA ---
    tela.fill(PRETO)  # Fundo Preto

    # 1. Desenhar os Combatentes (Quadrados)
    if player_hp > 0:
        pygame.draw.rect(tela, VERDE, (150, 270, 120, 120)) # Player à esquerda
    if inimigo_hp > 0:
        pygame.draw.rect(tela, AZUL, (800, 80, 120, 120))   # Inimigo à direita

    # 2. STATUS DO PLAYER (Alinhado à direita do quadrado verde)
    # Posição base do bloco de texto do Player: X=300, Y=290
    txt_nome_pl = fonte_interface.render(f"{nome_player}", True, BRANCO)
    tela.blit(txt_nome_pl, (300, 290))
    
    # Barra de vida logo abaixo do nome
    pygame.draw.rect(tela, CINZA_CLARO, (300, 320, 180, 12))
    pygame.draw.rect(tela, VERDE if player_hp > 30 else VERMELHO, (300, 320, int(180 * (player_hp / 100)), 12))
    
    # Texto de HP numérico abaixo da barra
    txt_hp_pl = fonte_status.render(f"HP: {player_hp}/100", True, BRANCO)
    tela.blit(txt_hp_pl, (300, 340))


    # 3. STATUS DO INIMIGO (Alinhado à esquerda do quadrado azulexit
    if inimigo_hp > 0:
        # Posição base do bloco de texto do Inimigo: X=320, Y=100
        txt_nome_in = fonte_interface.render(f"{nome_inimigo}", True, BRANCO)
        tela.blit(txt_nome_in, (600 , 100))
        
        # Barra de vida logo abaixo do nome
        pygame.draw.rect(tela, CINZA_CLARO, (600, 130, 180, 12))
        pygame.draw.rect(tela, AZUL if inimigo_hp > 30 else VERMELHO, (600, 130, int(180 * (inimigo_hp / 100)), 12))
        
        # Texto de HP numérico abaixo da barra
        txt_hp_in = fonte_status.render(f"HP: {inimigo_hp}/100", True, BRANCO)
        tela.blit(txt_hp_in, (600, 150))


    # 4. Painel de Batalha Inferior (Menu de Comandos)
    pygame.draw.rect(tela, CINZA_ESCURO, (0, 470, LARGURA, 130))
    pygame.draw.rect(tela, BRANCO, (5, 475, LARGURA - 10, 120), 3)

    # Texto de narração
    render_texto_painel = fonte_interface.render(texto_painel, True, BRANCO)
    tela.blit(render_texto_painel, (30, 520))

    # Exibe os ataques ou mensagem de reinício
    if not jogo_acabou:
        if turno_player:
            textos_ataques = [
                fonte_aviso.render(
                    f"{habilidade['nome']} ({habilidade['usos']}/{habilidade['limite']})",
                    True,
                    CINZA_CLARO if habilidade["usos"] > 0 else VERMELHO
                )
                for habilidade in ataques
            ]
            
            tela.blit(textos_ataques[0], (500, 500))
            tela.blit(textos_ataques[1], (850, 500))
            tela.blit(textos_ataques[2], (500, 540))
            tela.blit(textos_ataques[3], (850, 540))
    else:
        txt_reiniciar = fonte_aviso.render("[ Pressione R para recomeçar ]", True, (255, 215, 0))
        tela.blit(txt_reiniciar, (510, 525))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()
