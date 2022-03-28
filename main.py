import pygame 
import random
import math
from pygame import mixer
pygame.init()

# creating the screen
screen=pygame.display.set_mode((800,400))
background=pygame.image.load('bg.png').convert()

# player information
player=pygame.image.load('spaceship.png').convert_alpha()
playerx=40
playery=180
player_change=00

# enemy information
enemy=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
number_of_enemies=5

for i in range(number_of_enemies):
    enemy.append(pygame.image.load('enemy.png').convert_alpha())
    enemyx.append(random.randint(100,720))
    enemyy.append(random.randint(0,360))
    enemyy_change.append(0.5)
    enemyx_change.append(20)

# bullet information
bullet=pygame.image.load('bullet.png').convert_alpha()
bulletx=30
bullety=180
bullet_changex=1
bullet_state="ready"

total_score=0
font_type = pygame.font.Font('freesansbold.ttf', 32)

textx = 10
testy = 10

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bullet,(x,y))

# function to check colliosion
def iscollision(bulletx,bullety,enemyx,enemyy):
    dis=math.sqrt(math.pow((bulletx-enemyx),2)+(math.pow((bullety-enemyy),2)))
    if dis<40:
        return True
    return False

def show_score(x,y):
    score = font_type.render("Score : " + str(total_score), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_show():
    over_font=pygame.font.Font('freesansbold.ttf', 64)
    over = over_font.render("GAME OVER", True, (255,215,0))
    screen.blit(over,(215,180))

def developer_name():
    name_font=pygame.font.Font('freesansbold.ttf', 16)
    name = name_font.render("MADE BY AKSHAT BANSAL", True, (200,200,0))
    screen.blit(name,(550,10))

mixer.music.load('music.wav')
mixer.music.play(-1)

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        # giving keyboard control to player(UP and DOWN arrow key)
        if(event.type==pygame.KEYDOWN):
            if(event.key==pygame.K_UP):
                player_change-=0.35    
            if(event.key==pygame.K_DOWN):
                player_change+=0.35
        if(event.type==pygame.KEYUP):
            if(event.key==pygame.K_UP or event.key==pygame.K_DOWN):
                player_change=0
        
        # giving keyboard control to bullet(fire on pressing space bar)
        if(event.type==pygame.KEYDOWN):
            if(event.key==pygame.K_SPACE and bullet_state=="ready"):
                bullety=playery
                fire_bullet(bulletx,bullety)
                bullet_sound=mixer.Sound('firing.wav')
                bullet_sound.play()
    
    # setting boundary condition for player
    if(playery<0):
        playery=0
    elif(playery>350):
        playery=350
    playery+=player_change

    screen.blit(background,(0,0))
     
    developer_name()

    # setting boundary condition for enemy and check for collision
    for i in range(number_of_enemies):
        
        if enemyx[i]<80:
            for i in range(number_of_enemies):
                enemyx[i]=-200
            game_over_show()
            break
        if(enemyy[i]<0):
            enemyy_change[i]=0.5
            enemyx[i]-=enemyx_change[i]
        elif(enemyy[i]>365):
            enemyy_change[i]= -0.5
            enemyx[i]-=enemyx_change[i]
        enemyy[i]+=enemyy_change[i]
        condition=iscollision(bulletx,bullety,enemyx[i],enemyy[i])
        if condition is True:
            bullety=190
            bulletx=30
            bullet_state="ready"
            enemyx[i]=random.randint(100,720)
            enemyy[i]=random.randint(0,360)
            total_score+=1
            collision_sound=mixer.Sound('explosion.wav')
            collision_sound.play()
        screen.blit(enemy[i],(enemyx[i],enemyy[i]))

    # resetting bullet
    if(bulletx>800):
        bulletx=playerx
        bullet_state="ready"

    # giving movement to bullet
    if(bullet_state=="fire"):
        fire_bullet(bulletx,bullety+10)
        bulletx+=bullet_changex
    
    show_score(textx, testy)

    screen.blit(player,(playerx,playery))
    pygame.display.update()