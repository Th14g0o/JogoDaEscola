import pygame
from random import randrange
from time import sleep

pygame.init()

branco = (255, 255, 255)
verd = (0, 255, 0)
verm = (255, 0, 0)
azul = (0, 0, 255)
preto = (0, 0, 0)
amare = (255, 255, 0)

largura = 600
altura = 500

tela = pygame.display.set_mode((largura, altura), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Superman Flight")

def jogo():

    posi_x_c = 40
    posi_y_c = 250
    posi_y = 290
    posi_y_sele = 290
    posi_y_sele_tutor = 390

    som_kabum = pygame.mixer.Sound('kabum.mp3')
    som_kabum.set_volume(1)

    def texto(msg, cor, tam, x, y):
        estilo_da_fonte = pygame.font.SysFont(None, tam)
        mensagem = estilo_da_fonte.render(msg, True, cor)
        tela.blit(mensagem, (x, y))
        
    def selecao(cor, y):
        selecao = pygame.draw.rect(tela, cor, [163, y, 270, 60])

    theme = pygame.mixer.Sound('TrilhaSuperman.mp3')
    theme.set_volume(1)

    tela_inicio = pygame.image.load('TelaDeInicio.png').convert()
    menu_inicial = pygame.transform.scale(tela_inicio, (largura, altura))

    superho_sprites = pygame.image.load('SpriteSheetSuperman.png')

    superlife = []
    superman3 = pygame.image.load('BarraDeVida_3.png')
    super3 = pygame.transform.scale(superman3, (84*3, 84*2))
    superman2 = pygame.image.load('BarraDeVida_2.png')
    super2 = pygame.transform.scale(superman2, (84*3, 84*2))
    superman1 = pygame.image.load('BarraDeVida_1.png')
    super1 = pygame.transform.scale(superman1, (84*3, 84*2))
    superman0 = pygame.image.load('BarraDeVida_0.png')
    super0 = pygame.transform.scale(superman0, (84*3, 84*2))

    superlife.append(super3)
    superlife.append(super2)
    superlife.append(super1)
    superlife.append(super0)

    vidas = 0

    s = pygame.image.load('SupermanEmblema1SpriteRoll.png')

    ExploSprite = pygame.image.load('7ExploKryp115x115.png')
    
    class Explosion(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.imagens = []
            for i in range (0,7):
                    self.imagens.append(pygame.transform.scale(ExploSprite.subsurface((0+(115*i), 0), (115,115)), (96,96)))
            self.image = self.imagens[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y 
            self.mask = pygame.mask.from_surface(self.image)
            self.index_lista = 0
            
        def update(self):
            self.index_lista += 0.8
            if self.index_lista >= 7:
                self.index_lista = 0 
                pygame.sprite.Sprite.kill(self)
            self.image = self.imagens[int(self.index_lista)]

    class Vidaad(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.imagens_vida = []
            pt1 = s.subsurface((0, 0), (32, 32))
            s1 = pygame.transform.scale(pt1, (64, 64))
            pt2 = s.subsurface((32, 0), (32, 32))
            s2 = pygame.transform.scale(pt2, (64, 64))
            pt3 = s.subsurface((64, 0), (32, 32))
            s3 = pygame.transform.scale(pt3, (64, 64))
            pt4 = s.subsurface((96, 0), (32, 32))
            s4 = pygame.transform.scale(pt4, (64, 64))
            self.imagens_vida.append(s1)
            self.imagens_vida.append(s2)
            self.imagens_vida.append(s3)
            self.imagens_vida.append(s4)

            
            self.index_lista = 0
            self.image = self.imagens_vida[self.index_lista]
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.y = randrange(0, 400)
            self.rect.x = randrange(2000, 2001)

        def update(self):
            self.index_lista += 0.07    
            if self.index_lista > 3: 
                self.index_lista = 0
            self.image = self.imagens_vida[int(self.index_lista)]

            self.rect.x -= 5
            if self.rect.x <= -90:
                self.rect.x = randrange(2000, 2001)

        def reiniciar(self):
            self.rect.x = randrange(2000, 2001)
            self.rect.y = randrange(0, 400)

    class Superman(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.imagens_superm = []
            for i in range(2):          
                img = superho_sprites.subsurface((i * 546, 0), (546, 216))
                img2 = pygame.transform.scale(img, (64*2, 64))
                self.imagens_superm.append(img2)
            
            self.index_lista = 0
            self.image = self.imagens_superm[self.index_lista]
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.y = posi_y_c
            self.rect.x = posi_x_c

        def update(self):
                
            if self.index_lista > 1: 
                self.index_lista = 0
            self.index_lista += 0.2
            self.image = self.imagens_superm[int(self.index_lista)]

        def ChecandoSeColidiu(self, mask, x, y):
            return self.mask.overlap(mask, (x - self.rect.x, y - self.rect.y))
        def parabaixo(self):
            self.rect.y += 50
            if self.rect.y <= 0:
                self.rect.y = 0
            if self.rect.y >= altura - 64:
                self.rect.y = altura - 64

        def paracima(self):
            self.rect.y -= 50
            if self.rect.y <= 0:
                self.rect.y = 0
            if self.rect.y >= altura - 64:
                self.rect.y = altura - 64

        def reiniciar(self):
            self.rect.y = randrange(0, altura, 100)

    class Estrelas(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('Estrelas_0.png')
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect()
            self.rect.y = randrange(0, altura)
            self.rect.x = randrange(100, largura)

        def update(self):
            if self.rect.x < -100:
                self.rect.y = randrange(0, altura)
                self.rect.x = randrange(largura, largura+100)
            self.rect.x -= 10

    class Nave(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('NaveTemporaria2.png')
            self.image = pygame.transform.scale(self.image, (90, 80))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.y = randrange(0, 450, 100)
            self.rect.x = largura + 20
            self.velo = randrange(15, 20)

        def update(self):
            if self.rect.x < -100:
                self.reiniciar()
            self.rect.x -= self.velo
            
        def reiniciar(self):
            self.velo = randrange(15, 25)
            self.rect.y = randrange(0, 450, 100)
            self.rect.x = largura + 20
            
    todas_as_sprites = pygame.sprite.Group()
    superman = pygame.sprite.Group()
    grupo_oponente = pygame.sprite.Group()


    for e in range(20):
        estrelinhas = Estrelas()
        todas_as_sprites.add(estrelinhas)

    superhomem = Superman()
    todas_as_sprites.add(superhomem)
    superman.add(superhomem)
    

    for n in range(2):
        navez = Nave()
        todas_as_sprites.add(navez)
        grupo_oponente.add(navez)

    grupo_vida = pygame.sprite.Group()
    emblema_s = Vidaad()
    grupo_vida.add(emblema_s)

    cenario = pygame.image.load("Espaco_0.png").convert()
    cenario_na_tela = pygame.transform.scale(cenario, (largura, altura))

    funcionando = False

    rodando = True

    gameover = False

    tutor = False

    score = 0

    relogio = pygame.time.Clock()

    quant = 20
    
    while rodando:

        tela.blit(menu_inicial, (0, 0))
            
        while funcionando:

            tela.blit(cenario_na_tela, (0,0))
                                
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:   
                        superhomem.paracima()

                    if event.key == pygame.K_DOWN:   
                        superhomem.parabaixo()

            
                if event.type == pygame.QUIT:
                    funcionando = False
                    gameover = False
                    rodando = False


            mais_vida = pygame.sprite.spritecollide(superhomem, grupo_vida, False, pygame.sprite.collide_mask)
            
            
            

            

            if mais_vida:
                if vidas > 0:
                    vidas -= 1
                    emblema_s.reiniciar()
                    
            for i in grupo_oponente:
                if superhomem.ChecandoSeColidiu(i.mask, i.rect.x, i.rect.y):
                    som_kabum.play()
                    som_kabum.play()
                    todas_as_sprites.add(Explosion(i.rect.x, i.rect.y))
                    i.reiniciar()
                    vidas += 1
                
            if vidas > 2:
                sleep(0.5)
                funcionando = False
                gameover = True
            
            score += 0.03
            texto(f"Placar: {int(score)}", branco, 40, 10, 0)
            if score >= quant:
                quant += 20
                navez = Nave()
                todas_as_sprites.add(navez)
                grupo_oponente.add(navez)
            todas_as_sprites.draw(tela)
            todas_as_sprites.update()
            grupo_vida.draw(tela)
            grupo_vida.update()
            tela.blit(superlife[vidas], (largura - 210, -20))
            
            pygame.display.flip()
            relogio.tick(30)


        while gameover:
            theme.play()
            
            posi_y_sele == 290
                
            tela.fill(branco)
            
            texto(f"Placar: {int(score)}", amare, 50, 235, 100)
            texto(f"Placar: {int(score)}", verm, 50, 230, 100)
                        
            texto("VOCE PERDEU!!!", amare, 50, 175, 25)
            texto("VOCE PERDEU!!!", verm, 50, 170, 25)
            
            selecao(preto, posi_y_sele)
                                    
            pygame.draw.rect(tela, azul, [173, 300, 250, 40])
            texto("REINICIAR", amare, 40, 237, 305)
            pygame.draw.rect(tela, azul, [173, 350, 250, 40])
            texto("VOLTAR AO MENU", amare, 40, 175, 355)
            pygame.draw.rect(tela, azul, [173, 400, 250, 40])
            texto("SAIR", amare, 40, 260, 405)
                                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = False
                    funcionando = False
                    rodando = False
                                         
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        posi_y_sele += (50)
                        if posi_y_sele >= 390:
                            posi_y_sele = 390
                                                    
                    if event.key == pygame.K_UP:
                        posi_y_sele -= (50)
                        if posi_y_sele <=  290:
                            posi_y_sele = 290
                                                    
                    if event.key == pygame.K_RETURN:
                        todas_as_sprites.empty()
                        todas_as_sprites.update()
                        grupo_oponente.empty()
                        grupo_oponente.update()
                        for i in range(2):
                            navez = Nave()
                            todas_as_sprites.add(navez)
                            grupo_oponente.add(navez)
                        superhomem.reiniciar()
                        emblema_s.reiniciar()
                        todas_as_sprites.add(superhomem)
                        todas_as_sprites.add(emblema_s)
                        score = 0
                        vidas = 0
                        
                        if posi_y_sele == 290:
                            theme.stop()     
                            gameover = False
                            funcionando = True

                        if posi_y_sele == 340:
                            theme.stop()
                            gameover = False
                            funcionando = False
                            rodando = True                  
                                                
                        if posi_y_sele == 390:
                            rodando = False
                            funcionando = False
                            gameover = False

            pygame.display.flip()

        while tutor:

            tela.fill(branco)

            selecao(preto, posi_y_sele_tutor)
            pygame.draw.rect(tela, azul, [173, 400, 250, 40])
            texto("VOLTAR", amare, 40, 240, 405)

            texto("Seta para cima move o personagem para cima", preto, 30, 80, 100)
            texto("Seta para baixo move o personagem para baixo", preto, 30, 75, 150)
            texto("Se o Superman tocar em um dos drones perdera uma vida", preto, 30, 14, 200)
            texto("(Total 3)", preto, 30, 250, 230)
            texto("A velocidade dos drones varia, tome cuidado!", preto, 30, 75, 280)
            texto("O emblema do superman que aparece recupera uma vida", preto, 30, 15, 330)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tutor = False
                    rodando = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        tutor = False

            pygame.display.flip()

        theme.play()

        texto("Superman Flight", verm, 50, 0, 9)
        texto("Superman Flight", amare, 50, 3, 9)

        selecao(branco, posi_y)
        pygame.draw.rect(tela, azul, [173, 300, 250, 40])
        texto("INICIAR", amare, 40, 240, 305)
        pygame.draw.rect(tela, azul, [173, 350, 250, 40])
        texto("TUTORIAL", amare, 40, 234, 355)
        pygame.draw.rect(tela, azul, [173, 400, 250, 40])
        texto("SAIR", amare, 40, 260, 405)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                gameover = False
                funcionando = False
                                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    posi_y += (50)
                if posi_y >= 390:
                    posi_y = 390
                if event.key == pygame.K_UP:
                    posi_y -= (50)
                if posi_y <=  290:
                    posi_y = 290
                    
                if event.key == pygame.K_RETURN:
                    if posi_y == 290:
                        theme.stop()
                        funcionando = True
                                        
                    if posi_y == 340:
                        tutor = True

                    if posi_y == 390:
                        rodando = False
    
jogo()
pygame.quit()
