import math
import os
import random
import sys

import pygame

pygame.init()

# ─────────────────────────── Configurações ───────────────────────────
LARGURA, ALTURA, FPS = 800, 400, 60
CHAO_Y = ALTURA - 50
TAM_DINO = 85
TAM_PLANTA = 40

VEL_INICIAL, VEL_MAXIMA = 7, 15
GRAVIDADE, FORCA_PULO = 1.2, -21
ARQUIVO_RECORDE = "recorde.txt"

BRANCO, CINZA, PRETO = (255, 255, 255), (83, 83, 83), (0, 0, 0)
VERMELHO, AMARELO, VERDE = (200, 30, 30), (255, 215, 0), (50, 205, 50)
AZUL_VIDRO = (173, 216, 230)
CORES_FUNDO = [BRANCO, (255, 182, 193), AZUL_VIDRO, (144, 238, 144),
               (230, 230, 250), (255, 218, 185), (255, 255, 150)]

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dino de Juliete: A Fuga do Gin e da Patroa")
relogio = pygame.time.Clock()

# Fontes criadas uma única vez (antes eram recriadas a cada frame)
FONTE_PLACAR = pygame.font.SysFont("Arial", 22, bold=True)
FONTE_TITULO = pygame.font.SysFont("Impact", 55)
FONTE_TEXTO = pygame.font.SysFont("Arial", 18, bold=True)


# ─────────────────────────── Recursos ───────────────────────────
def remover_fundo_branco(img, limite=220):
    """Apaga só o branco conectado às bordas (preserva olhos e detalhes internos)."""
    w, h = img.get_size()
    pilha = ([(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] +
             [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
    visitados = set()
    while pilha:
        x, y = pilha.pop()
        if (x, y) in visitados or not (0 <= x < w and 0 <= y < h):
            continue
        visitados.add((x, y))
        r, g, b, a = img.get_at((x, y))
        if a == 0 or (r > limite and g > limite and b > limite):
            img.set_at((x, y), (0, 0, 0, 0))
            pilha.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))


def carregar(caminho, tamanho, cor_reserva):
    """Carrega a imagem; se não existir, devolve um retângulo colorido."""
    if not isinstance(tamanho, tuple):
        tamanho = (tamanho, tamanho)
    if os.path.exists(caminho):
        img = pygame.image.load(caminho).convert_alpha()
        img = pygame.transform.smoothscale(img, tamanho)  # reduz antes de limpar (mais rápido)
        remover_fundo_branco(img)
        return img
    surf = pygame.Surface(tamanho, pygame.SRCALPHA)
    surf.fill(cor_reserva)
    return surf


DINO_IMG = carregar("assets/dino.png", TAM_DINO, CINZA)
PATROA_IMG = carregar("assets/dino_f.png", TAM_DINO, VERMELHO)
PLANTA_IMG = carregar("assets/planta.png", TAM_PLANTA, VERDE)
GIN_ORIGINAL = carregar("assets/cacto.png", (50, 85), (34, 139, 34))

NUVEM = pygame.Surface((60, 25), pygame.SRCALPHA)
pygame.draw.ellipse(NUVEM, (230, 230, 230), (0, 5, 40, 20))
pygame.draw.ellipse(NUVEM, (230, 230, 230), (20, 0, 40, 20))

SOMBRA_MORTE = pygame.Surface((LARGURA, ALTURA))
SOMBRA_MORTE.fill(PRETO)
SOMBRA_MORTE.set_alpha(200)

_cache_gin = {}


def gin_redimensionado(w, h):
    if (w, h) not in _cache_gin:
        _cache_gin[(w, h)] = pygame.transform.smoothscale(GIN_ORIGINAL, (w, h))
    return _cache_gin[(w, h)]


def ler_recorde():
    try:
        with open(ARQUIVO_RECORDE) as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0


def salvar_recorde(valor):
    try:
        with open(ARQUIVO_RECORDE, "w") as f:
            f.write(str(valor))
    except OSError:
        pass


def texto_centralizado(fonte, texto, cor, y):
    surf = fonte.render(texto, True, cor)
    tela.blit(surf, (LARGURA // 2 - surf.get_width() // 2, y))


# ─────────────────────────── Jogo ───────────────────────────
class Jogo:
    def __init__(self):
        self.recorde = ler_recorde()
        self.reset()

    def reset(self):
        self.tempo = 0
        self.pontos = 0
        self.vel = VEL_INICIAL
        self.game_over = False
        self.pausado = False
        self.cor_idx = 0
        self.ultimo_marco_cor = 0

        # Dino
        self.dino_x = 220
        self.dino_y = CHAO_Y - TAM_DINO
        self.dino_vy = 0
        self.pulando = False

        # Patroa
        self.patroa_x = 40
        self.patroa_y = CHAO_Y - TAM_DINO
        self.patroa_y_anim = self.patroa_y

        # Gin
        self.novo_gin()
        self.cacos = []

        # Planta
        self.planta_x = LARGURA + 300
        self.planta_y = random.randint(120, 180)
        self.planta_ativa = True

        # Cenário
        self.nuvens = [{'x': random.randint(0, LARGURA), 'y': random.randint(20, 120),
                        'v': random.uniform(0.5, 1.2)} for _ in range(4)]
        self.tiros = []

    def novo_gin(self):
        self.gin_x = LARGURA
        self.gin_w = random.randint(45, 55)
        self.gin_h = random.randint(80, 95)
        self.quebrada = False

    # ── Eventos ──
    def tratar_eventos(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_SPACE, pygame.K_UP) and not self.pulando \
                        and not self.game_over and not self.pausado:
                    self.dino_vy, self.pulando = FORCA_PULO, True
                elif ev.key == pygame.K_p and not self.game_over:
                    self.pausado = not self.pausado
                elif ev.key == pygame.K_r and self.game_over:
                    self.reset()
                elif ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # Pulo variável: soltar cedo corta a subida
            if ev.type == pygame.KEYUP and ev.key in (pygame.K_SPACE, pygame.K_UP):
                if self.pulando and self.dino_vy < -8:
                    self.dino_vy = -8

    # ── Atualização ──
    def atualizar(self):
        self.tempo += 1
        self.atualizar_ceu()
        self.atualizar_planta()
        self.atualizar_dino()
        self.atualizar_gin()
        self.checar_colisoes()

    def atualizar_ceu(self):
        if random.randint(1, 45) == 1 and len(self.tiros) < 3:
            da_esquerda = random.choice((True, False))
            self.tiros.append({
                'x': -40 if da_esquerda else LARGURA + 40,
                'y': random.randint(10, 100),
                'vx': random.randint(12, 18) if da_esquerda else random.randint(-18, -12)})
        for t in self.tiros[:]:
            t['x'] += t['vx']
            t['y'] += 1.5
            if t['x'] < -100 or t['x'] > LARGURA + 100:
                self.tiros.remove(t)

        for n in self.nuvens:
            n['x'] -= n['v']
            if n['x'] < -60:
                n['x'], n['y'] = LARGURA, random.randint(20, 120)

    def atualizar_planta(self):
        self.planta_x -= self.vel
        if self.planta_x < -TAM_PLANTA:
            self.planta_x = LARGURA + random.randint(400, 800)
            self.planta_y = random.randint(130, 200)
            self.planta_ativa = True

    def atualizar_dino(self):
        if self.pulando:
            self.dino_y += self.dino_vy
            self.dino_vy += GRAVIDADE
            if self.dino_y >= CHAO_Y - TAM_DINO:
                self.dino_y, self.pulando = CHAO_Y - TAM_DINO, False
        self.patroa_y_anim = self.patroa_y + math.sin(self.tempo * 0.4) * 4

    def atualizar_gin(self):
        if not self.quebrada:
            self.gin_x -= self.vel
            if self.gin_x <= self.patroa_x + 55:  # a patroa "pega" o gin
                self.quebrada = True
                self.cacos = [{'x': self.gin_x + 20, 'y': CHAO_Y - 20,
                               'vx': random.randint(-5, 2), 'vy': random.randint(-7, -2)}
                              for _ in range(12)]
                self.pontos += 1
                self.vel = min(VEL_INICIAL + self.pontos // 5, VEL_MAXIMA)
        else:
            for c in self.cacos:
                c['x'] += c['vx']
                c['y'] += c['vy']
                c['vy'] += 0.4
            if all(c['y'] > ALTURA for c in self.cacos):
                self.cacos = []
                self.novo_gin()

    def checar_colisoes(self):
        dino = pygame.Rect(self.dino_x + 15, self.dino_y + 10, 55, 60)

        if self.planta_ativa and dino.colliderect(
                (self.planta_x, self.planta_y, TAM_PLANTA, TAM_PLANTA)):
            self.planta_ativa = False
            self.cor_idx = (self.cor_idx + 1) % len(CORES_FUNDO)

        # A cada 10 pontos o fundo também muda
        marco = self.pontos // 10
        if marco > self.ultimo_marco_cor:
            self.ultimo_marco_cor = marco
            self.cor_idx = (self.cor_idx + 1) % len(CORES_FUNDO)

        if not self.quebrada and dino.colliderect(
                (self.gin_x + 5, CHAO_Y - self.gin_h, self.gin_w - 10, self.gin_h)):
            self.game_over = True
            if self.pontos > self.recorde:
                self.recorde = self.pontos
                salvar_recorde(self.recorde)

    # ── Desenho ──
    def desenhar(self):
        tela.fill(CORES_FUNDO[self.cor_idx])
        for n in self.nuvens:
            tela.blit(NUVEM, (n['x'], n['y']))
        for t in self.tiros:
            pygame.draw.line(tela, AMARELO, (t['x'], t['y']),
                             (t['x'] - t['vx'], t['y'] - 1.5), 3)

        if self.planta_ativa and not self.game_over:
            tela.blit(PLANTA_IMG, (self.planta_x, self.planta_y))

        pygame.draw.line(tela, CINZA, (0, CHAO_Y), (LARGURA, CHAO_Y), 2)
        tela.blit(PATROA_IMG, (self.patroa_x,
                               self.patroa_y if self.game_over else self.patroa_y_anim))
        tela.blit(DINO_IMG, (self.dino_x, self.dino_y))

        if not self.quebrada:
            tela.blit(gin_redimensionado(self.gin_w, self.gin_h),
                      (self.gin_x, CHAO_Y - self.gin_h))
        else:
            for c in self.cacos:
                pygame.draw.rect(tela, AZUL_VIDRO, (c['x'], c['y'], 5, 5))

        tela.blit(FONTE_PLACAR.render(f"PONTOS: {self.pontos:04d}", True, CINZA),
                  (LARGURA - 175, 15))
        tela.blit(FONTE_TEXTO.render(f"RECORDE: {self.recorde:04d}", True, CINZA),
                  (LARGURA - 175, 45))

        if self.pausado:
            tela.blit(SOMBRA_MORTE, (0, 0))
            texto_centralizado(FONTE_TITULO, "PAUSADO", BRANCO, ALTURA // 2 - 40)
            texto_centralizado(FONTE_TEXTO, "Pressione P para continuar", BRANCO, ALTURA // 2 + 30)

        if self.game_over:
            tela.blit(SOMBRA_MORTE, (0, 0))
            texto_centralizado(FONTE_TITULO, "SE FUDEU", VERMELHO, ALTURA // 2 - 55)
            texto_centralizado(FONTE_TEXTO, f"Pontos: {self.pontos}   Recorde: {self.recorde}",
                               AMARELO, ALTURA // 2 + 10)
            texto_centralizado(FONTE_TEXTO, "Pressione R para tentar novamente",
                               BRANCO, ALTURA // 2 + 40)

    # ── Loop principal ──
    def executar(self):
        while True:
            self.tratar_eventos()
            if not self.game_over and not self.pausado:
                self.atualizar()
            self.desenhar()
            pygame.display.flip()
            relogio.tick(FPS)


if __name__ == "__main__":
    Jogo().executar() 
