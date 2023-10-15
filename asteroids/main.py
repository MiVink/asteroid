from typing import Any
from pygame import *
from random import *


w, h = 700, 500
window = display.set_mode((w, h))

display.set_caption("Call Of Duty:Modern Warfare(Mode:Survival)")

clock = time.Clock()
game = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, pImage, pX, pY, sizeX, sizeY, pSpeed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = pX
        self.rect.y = pY

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-9, self.rect.top, 20, 40, -15)
        bullets.add(bullet)

bullets = sprite.Group()

mixer.init()
mixer.music.load("cod_st.mp3")
mixer_music.play()    

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global hearts
        if self.rect.y > h:
            try:
                hearts.pop(0)
            except:
                pass
            #hearts.pop(Len(hearts)-1)
            self.rect.x = randint(0, w-80)
            self.rect.y = 0
            lost += 1

background = transform.scale(image.load("fon.jfif"), (w, h))

ship = Player("price.png", 10, h-100, 65, 95, 4)

asteroids = sprite.Group()
for i in range(6):
    randic = randint(1,2)
    if randic == 1:
        pic = "ussian2.png"
    if randic == 2:
        pic = "ussian2.png"
    asteroid = Enemy(pic, randint(10, w-50), -40, 50, 50, randint(1, 3))
    asteroids.add(asteroid)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

ship_reload = mixer.Sound("reload.mp3")
ship_reload.set_volume(0.15)
ship_fire = mixer.Sound("avtomat2.mp3")
ship_fire.set_volume(0.15)
score = 0
font.init()
mainfont = font.Font(None , 40)

re_time = False
num_fire = 0
from time import time as timer

lives = 10
hearts = []
hX = 300
for i in range(lives):
    heart = GameSprite("minecraft.png", hX, 10, 40, 38, 0)
    hearts.append(heart)
    hX += 40

restart = GameSprite("restart.png", 225, 200, 200, 100, 0)

def gameloop():
    global game, finish, score, re_time, num_fire, lost, hearts
    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire <= 50 and re_time == False:
                        ship.fire()
                        ship_fire.play()
                        num_fire += 1
                    if num_fire >= 50 and re_time == False:
                        re_start = timer()
                        re_time = True
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if restart.rect.collidepoint(x,y):
                    for a in asteroids:
                        a.rect.y = -100
                        a.rect.x = randint(0, w-100)
                    finish, lost, score = 0, 0, 0
                    lives = 10
                    hearts = []
                    hX = 300
                    for i in range(lives):
                        heart = GameSprite("minecraft.png", hX, 10, 40, 38, 0)
                        hearts.append(heart)
                        hX += 40

        if not finish:
            window.blit(background, (0,0))
            score_text = mainfont.render("Killed:" + str(score), True, (0,255,0))
            lost_text = mainfont.render("Missed:" + str(lost), True, (0,255,0))
            window.blit(score_text, (5, 10))
            window.blit(lost_text, (5, 50))       
            ship.update()
            ship.draw()

            bullets.draw(window)
            bullets.update()

            asteroids.draw(window)
            asteroids.update()

            collides = sprite.groupcollide(bullets, asteroids, True, True)
            for c in collides:
                score += 1
                randic = randint(1,2)
                if randic == 1:
                    pic = "ussian2.png"
                if randic == 2:
                    pic = "ussian2.png"
                asteroid = Enemy(pic, randint(10, w-50), -40, 50, 50, uniform(1, 2.5))
                asteroids.add(asteroid)

            if re_time == True:
                reload_end = timer()
                ship_reload.play
                if reload_end - re_start < 2:
                    reload = mainfont.render("RELOAD!", True, (0, 205, 0))
                    window.blit(reload, (250, 230))
                else:
                    num_fire = 0
                    re_time = False

            if sprite.spritecollide(ship, asteroids, False):
                restart.draw()
                lose = mainfont.render("YOU LOSE", True, (205, 0, 0))
                window.blit(lose, (250, 250))
                finish = True

            for heart in hearts:
                heart.draw()

            if len(hearts) <= 0:
                restart.draw()
                lose = mainfont.render("YOU LOSE", True, (205, 0, 0))
                window.blit(lose, (250, 250))
                finish = True
        
        display.update()
        clock.tick(60)

gameloop()