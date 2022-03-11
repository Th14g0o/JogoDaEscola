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

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Superman Flight")
    
def jogo():

    posi_x_c = 40
    posi_y_c = 250
    posi_y = 290
    posi_y_sele = 290

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
    explosao = pygame.image.load('explo.png')

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

    class Superman(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.imagens_superm = []
            for i in range(2):          
                img = superho_sprites.subsurface((i * 546,0), (546, 216))
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
                self.rect.x = largura
            self.rect.x -= 10

    class Nave(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('NaveTemporaria2.png')
            self.image = pygame.transform.scale(self.image, (90, 80))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.y = randrange(0, 450, 100)
            self.rect.x = randrange(350, largura + 10)
            self.rect = self.image.get_rect()
            self.velo = randrange(15, 25)

        def update(self):
            if self.rect.x < -100:
                self.rect.y = randrange(0, 450, 100)
                self.rect.x = randrange(largura, largura + 300, 90)
                self.velo = randrange(15, 30)
            self.rect.x -= self.velo
            
        def reiniciar(self):
            self.mask = pygame.mask.from_surface(self.image)
            self.velo = randrange(15, 25)
            self.rect.y = randrange(0, 450, 100)
            self.rect.x = largura + 20
            
    todas_as_sprites = pygame.sprite.Group()
    

    for e in range(18):
        estrelinhas = Estrelas()
        todas_as_sprites.add(estrelinhas)

    superhomem = Superman()
    todas_as_sprites.add(superhomem)

    grupo_oponente = pygame.sprite.Group()

    navez = Nave()
    navez2 = Nave()
    todas_as_sprites.add(navez)
    grupo_oponente.add(navez)
    todas_as_sprites.add(navez2)
    grupo_oponente.add(navez2)


    cenario = pygame.image.load("Espaco_0.png").convert()
    cenario_na_tela = pygame.transform.scale(cenario, (largura, altura))

    funcionando = False

    rodando = True

    gameover = False

    explo = False

    score = 0

    relogio = pygame.time.Clock()

    
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

            colisao = pygame.sprite.spritecollide(superhomem, grupo_oponente, False, pygame.sprite.collide_mask)
            todas_as_sprites.draw(tela)

            tela.blit(superlife[vidas], (largura - 210, -20))

                        
            if colisao and explo == False:
                som_kabum.play()
                som_kabum.play()
                todas_as_sprites.add(navez)
                grupo_oponente.add(navez)
                navez.reiniciar()
                todas_as_sprites.add(navez2)
                grupo_oponente.add(navez2)
                navez2.reiniciar()
                todas_as_sprites.update()
                vidas += 1
            if vidas > 2:
                sleep(1)
                funcionando = False
                gameover = True
            
            else:
                todas_as_sprites.update()
                        

            score += 0.03
            texto(f"Placar: {int(score)}", branco, 40, 10, 0)
                        
                        
            pygame.display.flip()
            relogio.tick(30)
            

        theme.play()

        texto("Superman Flight", verm, 50, 0, 9)
        texto("Superman Flight", amare, 50, 3,9)

        selecao(branco, posi_y)
        pygame.draw.rect(tela, azul, [173, 300, 250, 40])
        texto("INICIAR", amare, 40, 240, 305)
        pygame.draw.rect(tela, azul, [173, 350, 250, 40])
        texto("SAIR", amare, 40, 260, 355)
                        
        pygame.display.flip()

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
                            
                        if posi_y_sele == 290:
                            theme.stop()
                            navez.reiniciar()
                            navez2.reiniciar()
                            superhomem.reiniciar()
                            todas_as_sprites.update()
                            score = 0
                            explo = False
                            vidas = 0
                            gameover = False
                            funcionando = True
                                
                                                        
                        if posi_y_sele == 340:
                            theme.stop()
                            navez.reiniciar()
                            navez2.reiniciar()
                            superhomem.reiniciar()
                            todas_as_sprites.update()
                            score = 0
                            vidas = 0
                            explo = False
                            gameover = False
                            funcionando = False
                            rodando = True                  
                                                
                        if posi_y_sele == 390:
                            rodando = False
                            funcionando = False
                            gameover = False
                                
                                            
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                gameover = False
                funcionando = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                orientasao = pygame.mouse.get_pos()
                                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    posi_y += (50)
                if posi_y >= 340:
                    posi_y = 340
                if event.key == pygame.K_UP:
                    posi_y -= (50)
                if posi_y <=  290:
                    posi_y = 290
                    
                if event.key == pygame.K_RETURN:
                    if posi_y == 290:
                        theme.stop()
                        navez.reiniciar()
                        todas_as_sprites.update()
                        score = 0
                        explo = False
                        funcionando = True
                                        
                    if posi_y == 340:
                        rodando = False
    
jogo()
pygame.quit()
