import pygame
import random
import math
from pygame import mixer
import time


# initialize pygame
pygame.init()

# create the game window
win = pygame.display.set_mode((700,550))
pygame.display.set_caption("Star War")

# background image
bg = pygame.image.load("pics//bg.jpg")

# Background sound
mixer.music.load('bgSound.mp3')
mixer.music.play(-1) 

# Player
PlayerX = 0
PlayerY = 450
width = 60
height = 60
FPS = 60
speed = 10

ship = pygame.image.load('pics//ship.png')

# Enemy 
enemyImg = []
EnemyX = []
EnemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 6
enemySpeed = 5
enemyWidth = 30

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load('pics//enemy.png'))
    EnemyX.append(random.randint(0,250)) 
    EnemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)
 

# Bullet
bulletImg = pygame.image.load('pics//bullet.png')
bulletX = 0
bulletY = 450
bulletX_change = 0
bulletY_change = 10 
bullet_state = "ready"

# Score 
scoreNo = 0 
font = pygame.font.Font('freesansbold.ttf',32)
# create x & y corrdinate of text which we want to appear
textX = 10
textY = 10

# Game Over 
GameOver_font = pygame.font.Font('freesansbold.ttf',70)
GameOverTextX = 250
GameOverTextY = 200

def showScore(x,y):
    score = font.render("Score : " +str(scoreNo), True, (255,255,255))
    win.blit(score,(x,y))

def player(x, y):
    # Player image set
    win.blit(ship,(PlayerX,PlayerY))  

def enemy(x,y,i):
    # Enemy image set 
    win.blit(enemyImg[i],(x,y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bulletImg,(x+16,y)) 
    
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def gameOver(x,y):
    GameOver_font = font.render("GAME OVER", True, (0,255,0))
    win.blit(GameOver_font, (x,y))
    
clock = pygame.time.Clock()

run = True
while run:

    # background set 
    win.blit(bg,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False

    # Game logic goes here
    keys = pygame.key.get_pressed()

    # PlayerX Moves Left and its boudaries
    if keys[pygame.K_LEFT] and PlayerX > speed:
        PlayerX -= speed  
    
    # PlayerX Moves Right and its boudaries
    if keys[pygame.K_RIGHT] and PlayerX < 690 - width - speed:
        PlayerX += speed
    
    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bulletSound = mixer.Sound('bulletFire.wav')
            bulletSound.play()
            bulletX = PlayerX 
            fire_bullet(bulletX,bulletY)

    # Enemy Movement
    for i in range(numOfEnemies):

        # GameOver if enemy fall this cordinate
        if EnemyY[i] > 400:
            for j in range(numOfEnemies): 
                EnemyX[j] = 2000
                gameOver(GameOverTextX,GameOverTextY)
                
                pygame.display.flip()
                time.sleep(5) 
                run = False           
                break

        EnemyX[i] += enemyX_change[i]
        if EnemyX[i] <= 0:
            enemyX_change[i] = 5
            EnemyY[i] += enemyY_change [i]
        elif EnemyX[i] >= 690 - enemySpeed - width:
            enemyX_change[i] = -5
            EnemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(EnemyX[i],EnemyY[i],bulletX,bulletY)
        if collision:
            hitSound = mixer.Sound('hit.wav')
            hitSound.play()
            bulletY = 480
            bullet_state = "ready"
            scoreNo += 1
            # print(score)
            EnemyX[i] = random.randint(0,250) 
            EnemyY[i] = random.randint(0,150)  


        # Enemy fun call
        enemy(EnemyX[i],EnemyY[i],i)


    # bullet movement
    if bulletY <= 0:
        bulletY  = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    # Player fun call
    player(PlayerX,PlayerY)
    
    # score fun call
    showScore(textX,textY)

    # Update the display
    pygame.display.flip()
  
    # cap the frame rate
    clock.tick(FPS)

# quit the game
pygame.quit()
