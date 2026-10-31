import pygame, sys, random, os, math
pygame.init()

# Tela e Configurações Básicas
LARGURA, ALTURA = 800, 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dino de Juliete: A Fuga do Gin e da Patroa")
relogio = pygame.time.Clock()

# Cores e Lista de Cores Psicodélicas para o Fundo
BRANCO, CINZA, PRETO, VERMELHO, AMARELO = (255,255,255), (83,83,83), (0,0,0), (200,30,30), (255,215,0)
VERDE = (50, 205, 50)
CORES_FUNDO = [BRANCO, (255,182,193), (173,216,230), (144,238,144), (230,230,250), (255,218,185), (255,255,150)]

# --- FUNÇÃO AVANÇADA: LIMPA O CONTORNO E REMOVE REBARBAS PIXELADAS ANTES DE RENDERIZAR ---
def carregar(caminho, dim, cor):
    if os.path.exists(caminho):
        # Carrega a imagem aceitando transparência por canal Alpha nativo
        img = pygame.image.load(caminho).convert_alpha()
        
        # Cria uma nova superfície limpa e varre os pixels para remover o ruído branco/cinza do contorno
        largura_original, altura_original = img.get_size()
        for x in range(largura_original):
            for y in range(altura_original):
                r, g, b, a = img.get_at((x, y))
                # Se o pixel for branco puro ou muito próximo de branco (pontinhos cinzas/rebarbas)
                if r > 220 and g > 220 and b > 220:
                    img.set_at((x, y), (0, 0, 0, 0)) # Transforma em 100% invisível
                    
        return pygame.transform.scale(img, (dim, dim) if isinstance(dim, int) else dim)
    
    surf = pygame.Surface(dim if isinstance(dim, tuple) else (dim, dim), pygame.SRCALPHA)
    surf.fill(cor if len(cor) == 4 else cor + (255,)); return surf

# --- VARIÁVEIS DE CONFIGURAÇÃO DO ITEM ---
TAMANHO_PLANTA = 40

# Inicializa os Elementos Visuais do Jogo com o novo filtro anti-rebarbas
DINO_IMG = carregar("assets/dino.png", 85, CINZA)
GIN_IMG = carregar("assets/cacto.png", (50, 85), (34,139,34))
DINOSSAURA_IMG = carregar("assets/dino_f.png", 85, VERMELHO)
PLANTA_IMG = carregar("assets/planta.png", (TAMANHO_PLANTA, TAMANHO_PLANTA), VERDE)

# Elemento nativo da Nuvem por código com suporte a Alpha transparente
NUVEM = pygame.Surface((60, 25), pygame.SRCALPHA)
pygame.draw.ellipse(NUVEM, (230,230,230,255), (0,5,40,20))
pygame.draw.ellipse(NUVEM, (230,230,230,255), (20,0,40,20))

PLANTA_FALLBACK = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(PLANTA_FALLBACK, (50,205,50,255), (20,20), 12)

def jogar():
    chao_y = ALTURA - 50
    dino_x, dino_y, dino_vel_y, gravidade, pulando = 220, chao_y - 85, 0, 1.2, False
    patroa_x, patroa_y, tempo = 40, chao_y - 85, 0
    gin_x, gin_h, gin_w, vel_jogo = LARGURA, 85, 50, 7
    planta_x, planta_y, planta_ativa = LARGURA + 300, random.randint(120, 180), True
    cor_idx, pontos, pts_ultimo, game_over, rodando = 0, 0, 0, False, True
    
    nuvens = [{'x': random.randint(0, LARGURA), 'y': random.randint(20, 120), 'v': random.uniform(0.5, 1.2)} for _ in range(4)]
    tiros, cacos, quebrada = [], [], False

    while rodando:
        tempo += 1
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE and not pulando and not game_over: dino_vel_y, pulando = -21, True
                if ev.key == pygame.K_r and game_over: jogar(); return

        if not game_over:
            # Efeito de Tiros no Céu
            if random.randint(1, 45) == 1 and len(tiros) < 3:
                dir_t = random.choice(["esq", "dir"])
                tiros.append({'x': -40 if dir_t == "esq" else LARGURA + 40, 'y': random.randint(10, 100), 'vx': random.randint(12, 18) if dir_t == "esq" else random.randint(-18, -12)})
            for t in tiros[:]:
                t['x'] += t['vx']; t['y'] += 1.5
                if t['x'] < -100 or t['x'] > LARGURA + 100: tiros.remove(t)

            # Nuvens e Planta
            for n in nuvens:
                n['x'] -= n['v']
                if n['x'] < -60: n['x'], n['y'] = LARGURA, random.randint(20, 120)
            
            planta_x -= vel_jogo
            if planta_x < -40: planta_x, planta_y, planta_ativa = LARGURA + random.randint(400, 800), random.randint(130, 200), True

            # Física do Pulo do Dino e Animação da Patroa
            if pulando:
                dino_y += dino_vel_y; dino_vel_y += gravidade
                if dino_y >= chao_y - 85: dino_y, pulando = chao_y - 85, False
            patroa_y_at = patroa_y + (math.sin(tempo * 0.4) * 4)

            # Movimentação do Gin ou Vidros Quebrados
            if not quebrada:
                gin_x -= vel_jogo
                if gin_x <= (patroa_x + 55):
                    quebrada = True
                    cacos = [{'x': gin_x + 20, 'y': chao_y - 20, 'vx': random.randint(-5, 2), 'vy': random.randint(-7, -2)} for _ in range(12)]
                if gin_x < -gin_w:
                    gin_x, gin_h, gin_w = LARGURA, random.randint(80, 95), random.randint(45, 55)
                    pontos += 1; vel_jogo += 1 if pontos % 5 == 0 else 0
            else:
                for c in cacos: c['x'] += c['vx']; c['y'] += c['vy']; c['vy'] += 0.4
                if len(cacos) > 0 and all(c['y'] > ALTURA for c in cacos):
                    gin_x, gin_h, gin_w, quebrada, cacos = LARGURA, random.randint(80, 95), random.randint(45, 55), False, []
                    pontos += 1; vel_jogo += 1 if pontos % 5 == 0 else 0

            # Sistema de Colisões (Dino, Planta e Gin)
            d_rect = pygame.Rect(dino_x + 15, dino_y + 10, 55, 60)
            if planta_ativa and d_rect.colliderect(pygame.Rect(planta_x, planta_y, 40, 40)):
                planta_ativa, cor_idx = False, (cor_idx + 1) % len(CORES_FUNDO)
            if pontos > 0 and pontos % 10 == 0 and pontos != pts_ultimo:
                cor_idx, pts_ultimo = (cor_idx + 1) % len(CORES_FUNDO), pontos
            if not quebrada and d_rect.colliderect(pygame.Rect(gin_x + 5, chao_y - gin_h, gin_w - 10, gin_h)):
                game_over = True

        # Renderização Final do Cenário e Personagens
        tela.fill(CORES_FUNDO[cor_idx])
        for n in nuvens: tela.blit(NUVEM, (n['x'], n['y']))
        for t in tiros: pygame.draw.line(tela, AMARELO, (t['x'], t['y']), (t['x'] - t['vx'], t['y'] - 1.5), 3)
        
        if planta_ativa and not game_over: 
            if os.path.exists("assets/planta.png"): tela.blit(PLANTA_IMG, (planta_x, planta_y))
            else: tela.blit(PLANTA_FALLBACK, (planta_x, planta_y))
        
        pygame.draw.line(tela, CINZA, (0, chao_y), (LARGURA, chao_y), 2)
        tela.blit(DINOSSAURA_IMG, (patroa_x, patroa_y_at if not game_over else patroa_y))
        tela.blit(DINO_IMG, (dino_x, dino_y))
        
        if not quebrada: tela.blit(pygame.transform.scale(GIN_IMG, (gin_w, gin_h)), (gin_x, chao_y - gin_h))
        else:
            for c in cacos: pygame.draw.rect(tela, (173, 216, 230), (c['x'], c['y'], 5, 5))

        # Placar e Tela de Morte (GTA Se Fudeu)
        tela.blit(pygame.font.SysFont("Arial", 22, bold=True).render(f"PONTOS: {pontos:04d}", True, CINZA), (LARGURA - 160, 15))
        if game_over:
            sm = pygame.Surface((LARGURA, ALTURA)); sm.fill(PRETO); sm.set_alpha(200); tela.blit(sm, (0,0))
            tela.blit(pygame.font.SysFont("Impact", 55).render("SE FUDEU", True, VERMELHO), (LARGURA // 2 - 110, ALTURA // 2 - 40))
            tela.blit(pygame.font.SysFont("Arial", 18, bold=True).render("Pressione R para tentar novamente", True, BRANCO), (LARGURA // 2 - 145, ALTURA // 2 + 30))

        pygame.display.flip(); relogio.tick(60)

jogar()
