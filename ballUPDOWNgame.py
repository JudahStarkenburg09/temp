import pygame           
import sys
import time
import tkinter as tk
import random
import os
pygame.init()

currentDir = os.getcwd()
newDir = os.path.join(currentDir, 'data')
os.chdir(newDir)

white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0 , 0)  
black = pygame.Color(0,0,0)
pink = pygame.Color(255, 0, 85)
yellow = pygame.Color(255,255,0)
fps = 60
clock=pygame.time.Clock()

width = 800 
height = 700

obsSpeeds = [7, 12]
obstacleColor = (255, 255, 254)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Judah is weird")

jump_strength = 20
speed = 10  #speed of the ball
score = 0
cx = 400
cy = 200
vy = speed 
bR = 15 #ball radius
font = pygame.font.Font(None, 30)
collisions = False
xs = 0
y = 0
fondo = pygame.image.load("space.jpg").convert()
fondo = pygame.transform.scale(fondo, [800,700])

obsTime = 75  # Time in milliseconds to spawn obstacles
currentTick = 0
obstacles = []
ballSpeed = 8


def lose():
    def leave():
        exit()
    failRoot = tk.Tk()
    failRoot.title("You failed!")
    failRoot.geometry('250x50')
    label = tk.Label(failRoot, text="You Died!")
    label.place(x=10,y=0)
    button = tk.Button(failRoot, text="Exit", command=leave)
    button.place(x=50,y=20)

    failRoot.mainloop()


while True:
    screen.fill(black)
    screen.blit(fondo,[0,0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        cy += -(jump_strength)





    relative = xs % fondo.get_rect().width
    screen.blit(fondo, (relative - fondo.get_rect().width, y))
    if relative < width:
        screen.blit(fondo,(relative,0))
    xs -= 5
    cy += vy
    circle = pygame.draw.circle(screen, yellow, [cx, cy], bR)


    if (cy < 0 - bR):
        lose()



    #Detect if you leave the bottom
    if cy >= (height+bR):
        lose()

    currentTick += 1
    if currentTick >= obsTime:
        print(obsTime)
        score += 1
        obsSpeeds[0] += .2
        obsSpeeds[1] += .2
        if obsTime > 10: 
            obsTime -= 1

        # Create a new obstacle
        yObs = random.randrange(0, 680) #1
        speed = random.randrange(int(obsSpeeds[0]), int(obsSpeeds[1])) #2
        obstacles.append([width + 10, yObs, speed])

        currentTick = 0

    # Update and draw obstacles
    new_obstacles = []
    for obstacle in obstacles:
        xObs, yObs, speed = obstacle
        xObs -= speed  # Move the obstacle horizontally

        # Check for collision with the ball
        if pygame.Rect(cx - bR, cy - bR, 2 * bR, 2 * bR).colliderect(pygame.Rect(xObs, yObs, 20, 20)):
            # Handle collision here (e.g., end the game)
            print("Collision detected!")
            lose()

        # Check if the obstacle is off the screen
        if xObs + 20 > 0:
            pygame.draw.rect(screen, obstacleColor, pygame.Rect(xObs, yObs, 30, 30))
            new_obstacles.append([xObs, yObs, speed])
            

    obstacles = new_obstacles






    score_text = font.render(f"Score: {score}",True,(255,0,0))
    screen.blit(score_text,(20,20)) 

    time.sleep(0.01)
    pygame.display.flip()
    pygame.display.update()