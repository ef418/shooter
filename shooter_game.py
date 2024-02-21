#Создай собственный Шутер!

from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')

game = True
FPS = 60
win_w = 900
win_h = 600
delay_shot = 15
finish = False
sprite_size = 100
comets_time = 80


font.init()

main_win = display.set_mode((win_w,win_h))
display.set_caption('Шутер')
clock = time.Clock()
background = transform.scale(image.load('galaxy.jpg'),(win_w,win_h))




class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        main_win.blit(self.image,(self.rect.x,self.rect.y))



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    delay_b = 0
    hp = 3
    reset_bullets = 5
    recharge_time = 180
    def update(self):
        self.delay_b += 1

        keys = key.get_pressed()

        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x < win_w - 80:
            self.rect.x += self.speed

        if self.reset_bullets > 0:
            if keys[K_SPACE]:
                if self.delay_b >= delay_shot:
                    self.delay_b = 0
                    bullets.add(Bullet('bullet.png',self.rect.centerx-6,self.rect.y,10,15,25))
                    self.reset_bullets -= 1
        else:
            self.recharge_time -= 1
            main_win.blit(reload_bulets,(385,555))
            if self.recharge_time <= 0:
                self.reset_bullets = 5
                self.recharge_time = 180
    def reset_game(self):
        self.hp = 3
        self.reset_bullets = 5
        self.recharge_time = 180
        self.delay_b = 0
        self.rect.x = 400

class Enemy(GameSprite):
    def update(self):
        if self.rect.y < win_h:
            self.rect.y += self.speed
        else:
            self.rect.y = -sprite_size
            self.rect.x = randint(0, win_w - sprite_size)
            self.speed = randint(2,6)
            lost.change()

class Score():
    def __init__(self,text,color,size,x,y,check = 0):
        self.text = text
        self.color = color
        self.font_ = font.Font(None,size)
        self.check = check
        self.x = x
        self.y = y
        

    def change(self,step = 1):
            self.check += step

    def reset(self):
        self.image = self.font_.render(self.text + str(self.check),1,self.color)
        main_win.blit(self.image,(self.x,self.y))
    


class Comeets(GameSprite):
    def update(self):
        if self.rect.y < win_h:
            self.rect.y += self.speed
        else:
            self.kill()


font.init()
font1 = font.SysFont('Arial',400)
WIN = font1.render('WIN!',True,(255,215,0))

font2 = font.SysFont('Arial',150)
LOSE = font2.render('GAME OVER',True,(255,0,0))

font3 = font.SysFont('Arial',100)
reset = font3.render('заново: R',True,(255,255,255))

font4 = font.SysFont('Arial',35)
reload_bulets = font4.render('перезарядка',True,(184,254,34))


player = Player('rocket.png',400,win_h - sprite_size,5,sprite_size,sprite_size)


monsters = sprite.Group()
for i in range(1,6):
    enemy = Enemy('ufo.png', randint(1,win_w - sprite_size), -sprite_size, randint(2,6),sprite_size,sprite_size)
    monsters.add(enemy)

comets_group = sprite.Group()

bullets = sprite.Group()

lost = Score('Пропущено: ',(150,150,150),36,0,0)
frag = Score('счёт: ',(150,150,150),36,0,36)
count_live = Score('',(184,254,34),36,870,0,3)


while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_r and finish:
                finish = False
                for bullet in bullets:
                    bullet.kill()
#тут перезапуск
                for monster in monsters:
                    monster.kill()
                for comet in comets_group:
                    comet.kill()
                lost.check = 0
                frag.check = 0
                player.reset_game()
                count_live.check = 3

                for i in range(1,6):
                    enemy = Enemy('ufo.png', randint(1,win_w - sprite_size), -sprite_size, randint(2,4),sprite_size,sprite_size)
                    monsters.add(enemy)

    




    if not finish:
        main_win.blit(background,(0,0))
        player.reset()
        player.update()
        monsters.draw(main_win)
        monsters.update()
        bullets.draw(main_win)
        bullets.update()
        lost.reset()
        comets_group.draw(main_win)
        comets_group.update()
        frag.reset()
        comets_time -= 1
        


        if comets_time <= 0:
            comet = Comeets('asteroid.png',randint(0,win_w - sprite_size),-sprite_size,randint(4,7),sprite_size,sprite_size)
            comet.update()
            comets_group.add(comet)
            comets_time = randint(60,180)
        

        sprite_list = sprite.spritecollide(player,monsters,True)
        group_list = sprite.groupcollide(monsters,bullets,True,True)
        comets_list = sprite.spritecollide(player,comets_group,True)
        sprite.groupcollide(bullets,comets_group,True,False)

        if sprite_list or comets_list:
            count_live.change(-1)
        count_live.reset()


        if frag.check >= 8:
            finish = True
            main_win.blit(WIN,(130,50))
            main_win.blit(reset,(280,300))
        


        if count_live.check <= 0 or lost.check >= 10:
            finish = True
            main_win.blit(LOSE,(130,200))
            main_win.blit(reset,(280,300))

        for monster in group_list:
            frag.check += 1
            enemy = Enemy('ufo.png', randint(1,win_w - sprite_size), -sprite_size, randint(2,4),sprite_size,sprite_size)
            monsters.add(enemy)



    display.update()
    clock.tick(FPS)
