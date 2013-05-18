"""
The MIT License (MIT)

Copyright (c) 2013 Oscar Utbult

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
""" 

try:
    import math
    import time
    import pygame
    from pygame.locals import *

except ImportError:
    print "PyRay could not import necessary modules"
    raise ImportError

keys=[False]*324

# A map over the world
worldMap =  [
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 3, 0, 0, 2],
            [2, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 3, 1, 0, 0, 2, 0, 0, 0, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 2, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 1, 2, 0, 1],
            [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 2],
            [2, 3, 1, 0, 0, 2, 0, 0, 2, 1, 3, 2, 0, 2, 0, 0, 3, 0, 3, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 2, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 3, 0, 1, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1],
            [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]]

# Closes the program 
def close(): 
    pygame.display.quit()
    pygame.quit()

def main():
    pygame.init()

    # Head Up Display information (HUD)
    font = pygame.font.SysFont("Verdana",20)
    HUD = font.render("F1 / F2 - Screenshot JPEG/BMP   F5/F6 - Shadows on/off   F7/F8 - HUD Show/Hide", True, (0,0,0))

    # Creates window 
    WIDTH = 1000
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PyRay - Python Raycasting Engine (v0.03)")

    showShadow = True
    showHUD = True    
    
    # Defines starting position and direction
    positionX = 3.0
    positionY = 7.0

    directionX = 1.0
    directionY = 0.0

    planeX = 0.0
    planeY = 0.5

    # Movement constants   
    ROTATIONSPEED = 0.02
    MOVESPEED = 0.03

    # Trigeometric tuples + variables for index
    TGM = (math.cos(ROTATIONSPEED), math.sin(ROTATIONSPEED))
    ITGM = (math.cos(-ROTATIONSPEED), math.sin(-ROTATIONSPEED))
    COS, SIN = (0,1)
    
    while True:
        # Catches user input
        # Sets keys[key] to True or False
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    close()
                    return
                keys[event.key] = True
            elif event.type == KEYUP:
                keys[event.key] = False

        # Checks with keys are pressed by the user
        # Uses if so that more than one button at a time can be pressed.  
        if keys[K_ESCAPE]:
            close()

        if keys[K_LEFT]:
            oldDirectionX = directionX
            directionX = directionX * ITGM[COS] - directionY * ITGM[SIN]
            directionY = oldDirectionX * ITGM[SIN] + directionY * ITGM[COS]
            oldPlaneX = planeX
            planeX = planeX * ITGM[COS] - planeY * ITGM[SIN]
            planeY = oldPlaneX * ITGM[SIN] + planeY * ITGM[COS]

        if keys[K_RIGHT]:
            oldDirectionX = directionX
            directionX = directionX * TGM[COS] - directionY * TGM[SIN]
            directionY = oldDirectionX * TGM[SIN] + directionY * TGM[COS]
            oldPlaneX = planeX
            planeX = planeX * TGM[COS] - planeY * TGM[SIN]
            planeY = oldPlaneX * TGM[SIN] + planeY * TGM[COS]    

        if keys[K_UP]:
            if not worldMap[int(positionX + directionX * MOVESPEED)][int(positionY)]:
                positionX += directionX * MOVESPEED
            if not worldMap[int(positionX)][int(positionY + directionY * MOVESPEED)]:
                positionY += directionY * MOVESPEED
                
        if keys[K_DOWN]:
            if not worldMap[int(positionX - directionX * MOVESPEED)][int(positionY)]:
                positionX -= directionX * MOVESPEED
            if not worldMap[int(positionX)][int(positionY - directionY * MOVESPEED)]:
                positionY -= directionY * MOVESPEED

        if keys[K_F1]:
            try:
                pygame.image.save(screen,('PyRay' + time.strftime('%Y%m%d%H%M%S')+ '.jpeg'))
            except:
                print "Couldn't save jpeg screenshot"
                
        if keys[K_F2]:
            try:
                pygame.image.save(screen,('PyRay' + time.strftime('%Y%m%d%H%M%S')+ '.bmp'))
            except:
                print "Couldn't save bmp screenshot"

        # showShadows - On / Off
        if keys[K_F5]:
            showShadow = True
        if keys[K_F6]:
            showShadow = False

        # showHUD - Show / Hide
        if keys[K_F7]:
            showHUD = True
        if keys[K_F8]:
            showHUD = False
            
        # Draws roof and floor
        screen.fill((25,25,25))
        pygame.draw.rect(screen, (50,50,50), (0, HEIGHT/2, WIDTH, HEIGHT/2)) 
                
        # Starts drawing level from 0 to < WIDTH 
        column = 0        
        while column < WIDTH:
            cameraX = 2.0 * column / WIDTH - 1.0
            rayPositionX = positionX
            rayPositionY = positionY
            rayDirectionX = directionX + planeX * cameraX
            rayDirectionY = directionY + planeY * cameraX + .000000000000001 # avoiding ZDE 

            # In what square is the ray?
            mapX = int(rayPositionX)
            mapY = int(rayPositionY)

            # Delta distance calculation
            # Delta = square ( raydir * raydir) / (raydir * raydir)
            deltaDistanceX = math.sqrt(1.0 + (rayDirectionY * rayDirectionY) / (rayDirectionX * rayDirectionX))
            deltaDistanceY = math.sqrt(1.0 + (rayDirectionX * rayDirectionX) / (rayDirectionY * rayDirectionY))

            # We need sideDistanceX and Y for distance calculation. Checks quadrant
            if (rayDirectionX < 0):
                stepX = -1
                sideDistanceX = (rayPositionX - mapX) * deltaDistanceX

            else:
                stepX = 1
                sideDistanceX = (mapX + 1.0 - rayPositionX) * deltaDistanceX

            if (rayDirectionY < 0):
                stepY = -1
                sideDistanceY = (rayPositionY - mapY) * deltaDistanceY

            else:
                stepY = 1
                sideDistanceY = (mapY + 1.0 - rayPositionY) * deltaDistanceY

            # Finding distance to a wall
            hit = 0
            while  (hit == 0):
                if (sideDistanceX < sideDistanceY):
                    sideDistanceX += deltaDistanceX
                    mapX += stepX
                    side = 0
                    
                else:
                    sideDistanceY += deltaDistanceY
                    mapY += stepY
                    side = 1
                    
                if (worldMap[mapX][mapY] > 0):
                    hit = 1

            # Correction against fish eye effect
            if (side == 0):
                perpWallDistance = abs((mapX - rayPositionX + ( 1.0 - stepX ) / 2.0) / rayDirectionX)
            else:
                perpWallDistance = abs((mapY - rayPositionY + ( 1.0 - stepY ) / 2.0) / rayDirectionY)

            # Calculating HEIGHT of the line to draw
            lineHEIGHT = abs(int(HEIGHT / (perpWallDistance+.0000001)))
            drawStart = -lineHEIGHT / 2.0 + HEIGHT / 2.0

            # if drawStat < 0 it would draw outside the screen
            if (drawStart < 0):
                drawStart = 0

            drawEnd = lineHEIGHT / 2.0 + HEIGHT / 2.0

            if (drawEnd >= HEIGHT):
                drawEnd = HEIGHT - 1

            # Wall colors 0 to 3
            wallcolors = [ [], [150,0,0], [0,150,0], [0,0,150] ]
            color = wallcolors[ worldMap[mapX][mapY] ]                                  

            # If side == 1 then ton the color down. Gives a "showShadow" an the wall.
            # Draws showShadow if showShadow is True
            if showShadow:
                if side == 1:
                    for i,v in enumerate(color):
                        color[i] = int(v / 1.2)                    

            # Drawing the graphics                           
            pygame.draw.line(screen, color, (column,drawStart), (column, drawEnd), 2)
            column += 2

        # Drawing HUD if showHUD is True
        if showHUD:
            pygame.draw.rect(screen, (100,100,200), (0, HEIGHT-40, WIDTH, 40))
            screen.blit(HUD, (20,HEIGHT-30))

        # Updating display
        pygame.event.pump()
        pygame.display.flip()           
       
main()