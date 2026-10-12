import pygame
import sys
import random
import math
import os

# Força o Python a usar a pasta onde o main.py está guardado como pasta principal
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0] if __name__ == '__main__' else __file__)))

# Inicializa o Pygame e o sistema de som
pygame.init()
pygame.mixer.init()

# 1. Configurações da Janela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Defensores da Terra")
relogio = pygame.time.Clock()

# 2. Definição de Cores (RGB)
PRETO   = (10, 10, 20)
BRANCO  = (255, 255, 255)
CINZA   = (120, 120, 130)
VERMELHO= (255, 50, 50)
VERDE   = (50, 255, 50)
AZUL_C  = (0, 255, 255)
ROXO    = (150, 50, 255)
AMARELO = (255, 215, 0)

# 3. Variáveis do Jogo
nave_x, nave_y = 400, 450
nave_vel = 6
nave_largura, nave_altura = 50, 40

# --- CONFIGURAÇÃO DA IMAGEM DA NAVE ---
# Carrega a imagem PNG da pasta
imagem_nave_original = pygame.image.load("nave.png").convert_alpha()

# Redimensiona a imagem para encaixar perfeitamente no tamanho da tela
imagem_nave = pygame.transform.scale(imagem_nave_original, (nave_largura, nave_altura))

# Configuração de Vidas iniciais 
vida_nave_max = 5
vida_nave = 5
vida_terra_max = 10     
vida_terra = 5       

pontuacao = 0
circulos_azuis_coletados = 5
game_over = False
som_game_over = False
jogo_pausado = False  

# VARIÁVEIS DO TIMER DO JOGO
tempo_acumulado = 0  # Guarda os segundos jogados antes de pausar
momento_retomada = pygame.time.get_ticks()  # Monitora quando o jogo despausa

# Efeito do Especial (Tiro em Área)
pulso_ativo = False
pulso_raio = 0
pulso_duracao = 0

# Listas de objetos
asteroides = []
coracoes = []
itens_azuis = []
coracoes_verdes = [] 
estrelas = [{"x": random.randint(0, LARGURA), "y": random.randint(0, ALTURA), "vel": random.uniform(0.5, 2)} for _ in range(50)]

# Dificuldade progressiva e Temporizadores de Spawn
tempo_inicial = pygame.time.get_ticks()
frequencia_asteroide = 1500  
ultimo_asteroide = 0

ultimo_coracao = 0
freq_coracao = 14000 

ultimo_item_azul = 0
freq_azul = 18000    

ultimo_coracao_verde = 0
freq_verde = 16000   

velocidade_base_asteroide = 2.8

# 4 CONFIGURAÇÃO DOS SONS
som_powerup = pygame.mixer.Sound("power_ups.wav") # Power Up azul
som_coracao = pygame.mixer.Sound("coracoes.wav") # Corações (Vermelho e Verde)
som_especial = pygame.mixer.Sound("poder_especial.wav") # Poder especial
som_asteroide = pygame.mixer.Sound("asteroide.wav") # Dano no asteróide
som_danos = pygame.mixer.Sound("danos.mpeg") # Poder especial
som_gameover = pygame.mixer.Sound("game_over.mpeg") # Game Over

som_gameover.set_volume(0.7)
som_danos.set_volume(0.25)
som_asteroide.set_volume(0.2)
som_powerup.set_volume(0.8)
som_coracao.set_volume(0.55)
som_especial.set_volume(0.85)

# Música de Fundo:
def tocar_nota(frequencia, duracao_ms):
    sample_rate = 22050
    num_samples = int(sample_rate * (duracao_ms / 1000.0))
    buffer = bytearray()
    for i in range(num_samples):
        t = i / sample_rate
        val = 127 if math.sin(2 * math.pi * frequencia * t) > 0 else -128
        buffer.append(val & 255)
    try:
        sound = pygame.mixer.Sound(buffer=buffer)
        sound.set_volume(0.05)
        sound.play()
    except:
        pass

# Notas musicais para o loop de fundo (MANTENHA ISSO)
notas_musicais = [110, 116, 123, 116]
indice_nota = 0
ultima_nota_tempo = 0
tempo_entre_notas = 800

# Loop Principal
while True:
    relogio.tick(60)
    agora = pygame.time.get_ticks()
    
    # CÁLCULO DO TIMER DINÂMICO (Congela na pausa ou game over)
    if not game_over and not jogo_pausado:
        segundos_jogados = tempo_acumulado + int((agora - momento_retomada) / 1000)
    
    # Ajusta a dificuldade dinamicamente baseada APENAS nos segundos reais jogados (congela na pausa)
    multiplicador_dificuldade = 1.0 + (segundos_jogados * 0.0175)
    tempo_entre_notas = max(200, 800 - int(segundos_jogados * 4)) 
    intervalo_asteroides = max(400, frequencia_asteroide - int(segundos_jogados * 8))
    
    # Controle da Música 
    if not game_over and not jogo_pausado and agora - ultima_nota_tempo > tempo_entre_notas:
        tocar_nota(notas_musicais[indice_nota] * (1 + int(segundos_jogados*0.0175)), 150)
        indice_nota = (indice_nota + 1) % len(notas_musicais)
        ultima_nota_tempo = agora

    # --- 1. CAPTURA DE EVENTOS (TECLADO) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.KEYDOWN:
            # Alterna estado de pausa
            if evento.key == pygame.K_p and not game_over:
                jogo_pausado = not jogo_pausado
                if jogo_pausado:
                    # Quando pausa, guarda o tempo acumulado até aqui
                    tempo_acumulado = segundos_jogados
                else:
                    # Quando despausa, reinicia a contagem a partir de agora
                    momento_retomada = pygame.time.get_ticks()

            if game_over and evento.key == pygame.K_r: # Reiniciar
                pygame.mixer.music.stop()  # Para a música de derrota
                nave_x, nave_y = 400, 450
                vida_nave = 5 
                vida_terra = 5
                pontuacao = 0
                circulos_azuis_coletados = 5
                asteroides.clear()
                coracoes.clear()
                itens_azuis.clear()
                coracoes_verdes.clear()
                pulso_ativo = False
                jogo_pausado = False
                som_game_over = False
                tempo_acumulado = 0
                momento_retomada = pygame.time.get_ticks()
                tempo_inicial = pygame.time.get_ticks()
                game_over = False
                
            elif not game_over and not jogo_pausado and evento.key == pygame.K_SPACE and circulos_azuis_coletados > 0:
                pulso_ativo = True
                pulso_raio = 25
                pulso_duracao = 30
                circulos_azuis_coletados -= 1  
                som_especial.play()  # Toca o som do poder especial

                
                for asteroide in asteroides[:]:
                    if asteroide["y"] > ALTURA // 2: 
                        asteroides.remove(asteroide)
                        pontuacao += 5  

    # TUDO ABAIXO SÓ ANDA SE O JOGO NÃO ESTIVER PAUSADO
    if not game_over and not jogo_pausado:
        # --- 2. MOVIMENTAÇÃO (WASD) ---
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a] and nave_x > 0:
            nave_x -= nave_vel
        if teclas[pygame.K_d] and nave_x < LARGURA - nave_largura:
            nave_x += nave_vel
        if teclas[pygame.K_w] and nave_y > 100:
            nave_y -= nave_vel
        if teclas[pygame.K_s] and nave_y < ALTURA - nave_altura - 20:
            nave_y += nave_vel

        # Animação do pulso de tiro
        if pulso_ativo:
            pulso_raio += 80
            pulso_duracao -= 1
            if pulso_duracao <= 0:
                pulso_ativo = False

        # --- 3. CRIAÇÃO DE INIMIGOS E ITENS ---
        if agora - ultimo_asteroide > intervalo_asteroides:
            asteroides.append({
                "x": random.randint(20, LARGURA - 40),
                "y": -40,
                "raio": random.randint(15, 30),
                "vel": velocidade_base_asteroide * multiplicador_dificuldade
            })
            ultimo_asteroide = agora
            
        if agora - ultimo_coracao > freq_coracao:
            coracoes.append({
                "x": random.randint(50, LARGURA - 50),
                "y": random.randint(150, ALTURA - 150),
                "expira": agora + 6000 
            })
            ultimo_coracao = agora

        if agora - ultimo_item_azul > freq_azul:
            itens_azuis.append({
                "x": random.randint(50, LARGURA - 50),
                "y": random.randint(150, ALTURA - 150),
                "expira": agora + 6000
            })
            ultimo_item_azul = agora

        if agora - ultimo_coracao_verde > freq_verde:
            coracoes_verdes.append({
                "x": random.randint(50, LARGURA - 50),
                "y": random.randint(150, ALTURA - 150),
                "expira": agora + 6000
            })
            ultimo_coracao_verde = agora

        # --- 4. ATUALIZAÇÃO DE POSIÇÕES E COLISÕES ---
        for estrela in estrelas:
            estrela["y"] += estrela["vel"]
            if estrela["y"] > ALTURA:
                estrela["y"] = 0
                estrela["x"] = random.randint(0, LARGURA)

        escudo_rect = pygame.Rect(nave_x - 10, nave_y - 12, nave_largura + 20, 10)
        nave_rect = pygame.Rect(nave_x, nave_y, nave_largura, nave_altura)

        for asteroide in asteroides[:]:
            asteroide["y"] += asteroide["vel"]
            ast_rect = pygame.Rect(asteroide["x"] - asteroide["raio"], asteroide["y"] - asteroide["raio"], asteroide["raio"]*2, asteroide["raio"]*2)
            
            if escudo_rect.colliderect(ast_rect):
                som_asteroide.play()
                asteroides.remove(asteroide)
                pontuacao += 10
                continue
                
            if nave_rect.colliderect(ast_rect):
                som_danos.play()
                vida_nave -= 1
                asteroides.remove(asteroide)
                if vida_nave <= 0:
                    som_gameover.play()
                    game_over = True
                continue

            if asteroide["y"] - asteroide["raio"] > ALTURA:
                som_danos.play()
                vida_terra -= 1
                asteroides.remove(asteroide)
                if vida_terra <= 0:
                    som_gameover.play()
                    game_over = True
                continue

        for coracao in coracoes[:]:
            if agora > coracao["expira"]:
                coracoes.remove(coracao)
                continue
            coracao_rect = pygame.Rect(coracao["x"] - 12, coracao["y"] - 12, 24, 24)
            if nave_rect.colliderect(coracao_rect) or escudo_rect.colliderect(coracao_rect):
                som_coracao.play()  # Toca o som do coração

                if vida_nave < vida_nave_max:
                    vida_nave += 1
                coracoes.remove(coracao)

        for item in itens_azuis[:]:
            if agora > item["expira"]:
                itens_azuis.remove(item)
                continue
            item_rect = pygame.Rect(item["x"] - 12, item["y"] - 12, 24, 24)
            if nave_rect.colliderect(item_rect) or escudo_rect.colliderect(item_rect):
                som_powerup.play()  # Toca o som do item azul
    
                if circulos_azuis_coletados < 10:
                    circulos_azuis_coletados += 1
                itens_azuis.remove(item)

        for cv in coracoes_verdes[:]:
            if agora > cv["expira"]:
                coracoes_verdes.remove(cv)
                continue
            cv_rect = pygame.Rect(cv["x"] - 12, cv["y"] - 12, 24, 24)
            if nave_rect.colliderect(cv_rect) or escudo_rect.colliderect(cv_rect):
                som_coracao.play()  # Toca o som do coração para a Terra também

                if vida_terra < vida_terra_max:
                    vida_terra += 1
                coracoes_verdes.remove(cv)

    # --- 5. RENDERIZAÇÃO DA TELA (DESENHOS) ---
    tela.fill(PRETO)

    for estrela in estrelas:
        pygame.draw.circle(tela, BRANCO, (int(estrela["x"]), int(estrela["y"])), 1)

    if pulso_ativo:
        pygame.draw.circle(tela, ROXO, (LARGURA // 2, ALTURA), pulso_raio, width=6) # Linha do poder especial


    if not game_over:
        # Desenha os Corações Vermelhos e a Nave
        for coracao in coracoes:
            cx, cy = coracao["x"], coracao["y"]
            pygame.draw.circle(tela, VERMELHO, (cx - 6, cy - 4), 7)
            pygame.draw.circle(tela, VERMELHO, (cx + 6, cy - 4), 7)
            pygame.draw.polygon(tela, VERMELHO, [(cx - 13, cy - 2), (cx + 13, cy - 2), (cx, cy + 12)])

        # Desenha os Corações Verdes (Terra)
        for cv in coracoes_verdes:
            cx, cy = cv["x"], cv["y"]
            pygame.draw.circle(tela, VERDE, (cx - 6, cy - 4), 7)
            pygame.draw.circle(tela, VERDE, (cx + 6, cy - 4), 7)
            pygame.draw.polygon(tela, VERDE, [(cx - 13, cy - 2), (cx + 13, cy - 2), (cx, cy + 12)])

        # Desenha os Círculos Azuis
        for item in itens_azuis:
            pygame.draw.circle(tela, AZUL_C, (item["x"], item["y"]), 12)
            pygame.draw.circle(tela, BRANCO, (item["x"], item["y"]), 6)

        for asteroide in asteroides:
            pygame.draw.circle(tela, CINZA, (int(asteroide["x"]), int(asteroide["y"])), asteroide["raio"])

        pygame.draw.rect(tela, AZUL_C, escudo_rect, border_top_left_radius=5, border_top_right_radius=5)
        tela.blit(imagem_nave, (nave_x, nave_y))

        # INTERFACE SUPERIOR ALINHADA
        fonte = pygame.font.SysFont("Arial", 20, bold=True)
        
        texto_pontos = fonte.render(f"PONTOS: {pontuacao}", True, BRANCO)
        texto_azuis = fonte.render(f"CARGAS ESPECIAIS: {circulos_azuis_coletados}/10", True, AZUL_C)
        texto_vel = fonte.render(f"DIFICULDADE: x{multiplicador_dificuldade:.1f}", True, VERDE)
        
        # DESENHA O TIMER CENTRALIZADO NO TOPO
        texto_timer = fonte.render(f"TEMPO: {segundos_jogados}s", True, AMARELO)
        
        tela.blit(texto_pontos, (20, 15))
        tela.blit(texto_azuis, (20, 40))
        tela.blit(texto_vel, (20, 65))
        tela.blit(texto_timer, (LARGURA // 2 - texto_timer.get_width() // 2, 15)) # Centralizado
        
                # 1. Alinhamento da Vida da Nave (Texto em X=460, corações começam em X=550)
        texto_vnave = fonte.render("NAVE:", True, BRANCO)
        tela.blit(texto_vnave, (460, 18))
        for i in range(vida_nave_max):
            cor = VERMELHO if i < vida_nave else (40, 40, 45)
            cx, cy = 550 + (i * 20), 28
            pygame.draw.circle(tela, cor, (cx - 4, cy - 3), 5)
            pygame.draw.circle(tela, cor, (cx + 4, cy - 3), 5)
            pygame.draw.polygon(tela, cor, [(cx - 9, cy - 1), (cx + 9, cy - 1), (cx, cy + 8)])

        # 2. Alinhamento da Vida da Terra (Texto em X=460, corações começam em X=550 - Suporta até 10)
        texto_vterra = fonte.render("TERRA:", True, VERDE)
        tela.blit(texto_vterra, (460, 48))
        for i in range(vida_terra_max):
            cor = VERDE if i < vida_terra else (40, 40, 45)
            cx, cy = 550 + (i * 20), 58  # Ajustado para andar de 20 em 20 pixels e caber os 10 corações
            pygame.draw.circle(tela, cor, (cx - 4, cy - 3), 5)
            pygame.draw.circle(tela, cor, (cx + 4, cy - 3), 5)
            pygame.draw.polygon(tela, cor, [(cx - 9, cy - 1), (cx + 9, cy - 1), (cx, cy + 8)])

    else:
        # TELA DE GAME OVER (MOSTRA O TIMER E MENSAGEM ESPECIAL)
        fonte_g = pygame.font.SysFont("Arial", 45, bold=True)
        fonte_p = pygame.font.SysFont("Arial", 25)
        fonte_m = pygame.font.SysFont("Arial", 22, bold=True) # Fonte para o parabéns
        fonte_t = pygame.font.SysFont("Arial", 20, italic=True) # Fonte para a dica de tentar novamente

        motivo = "GAME OVER" if vida_terra <= 0 else "NAVE ABATIDA"
        txt_gameover = fonte_g.render(motivo, True, VERMELHO)
        
        txt_PontosFinais = fonte_p.render(f"Pontos: {pontuacao}   |   Tempo Sobrevivido: {segundos_jogados}s", True, BRANCO)
        txt_reiniciar = fonte_p.render("Pressione 'R' para tentar novamente", True, VERDE)
        
        tela.blit(txt_gameover, (LARGURA//2 - txt_gameover.get_width()//2, ALTURA//2 - 100))

        if motivo == "NAVE ABATIDA":
            fonte_dica = pygame.font.SysFont("Arial", 20, italic=True)
            txt_dica = fonte_dica.render("Dica: Proteja a sua nave dos impactos laterais!", True, AZUL_C)
            tela.blit(txt_dica, (LARGURA//2 - txt_dica.get_width()//2, ALTURA//2 - 40))

        # Desenha os textos padrões de fim de jogo
        tela.blit(txt_gameover, (LARGURA//2 - txt_gameover.get_width()//2, ALTURA//2 - 100))
        tela.blit(txt_PontosFinais, (LARGURA//2 - txt_PontosFinais.get_width()//2, ALTURA//2 + 30))
        tela.blit(txt_reiniciar, (LARGURA//2 - txt_reiniciar.get_width()//2, ALTURA//2 + 70))

        # CONDIÇÃO DOS 60 SEGUNDOS: Se o jogador resistir por 60s ou mais, exibe a mensagem
                # CONDIÇÃO DO TIMER DA VITÓRIA (Ordem corrigida do maior para o menor)
        if segundos_jogados >= 120:
            txt_parabens = fonte_m.render("PARABÉNS! VOCÊ SOBREVIVEU MAIS DE 2 MINUTOS!", True, AMARELO)
            tela.blit(txt_parabens, (LARGURA//2 - txt_parabens.get_width()//2, ALTURA//2 - 20))
            
        elif segundos_jogados >= 60:
            txt_parabens = fonte_m.render("PARABÉNS! VOCÊ SOBREVIVEU MAIS DE 1 MINUTO!", True, AMARELO)
            tela.blit(txt_parabens, (LARGURA//2 - txt_parabens.get_width()//2, ALTURA//2 - 20))
            
        else:
            # Caso não tenha criado a fonte_t ainda, use fonte_p para não dar erro
            txt_tente = fonte_p.render("TENTE RESISTIR POR 60 SEGUNDOS OU MAIS!", True, AMARELO)
            tela.blit(txt_tente, (LARGURA//2 - txt_tente.get_width()//2, ALTURA//2 - 20))

    # TELA DE PAUSA (MOSTRA O TIMER TAMBÉM)
    if jogo_pausado and not game_over:
        fonte_p = pygame.font.SysFont("Arial", 50, bold=True)
        txt_pausa = fonte_p.render("JOGO PAUSADO", True, AZUL_C)
        fonte_ajuda = pygame.font.SysFont("Arial", 20)
        txt_ajuda = fonte_ajuda.render(f"Tempo atual: {segundos_jogados}s  |  Pressione 'P' para continuar", True, BRANCO)
        
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        tela.blit(overlay, (0, 0))
        
        tela.blit(txt_pausa, (LARGURA//2 - txt_pausa.get_width()//2, ALTURA//2 - 40))
        tela.blit(txt_ajuda, (LARGURA//2 - txt_ajuda.get_width()//2, ALTURA//2 + 20))

    pygame.display.flip()