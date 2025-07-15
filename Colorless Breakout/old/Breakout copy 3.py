import pygame
import random
import math
import time

pygame.init()

THROW_BALL_EVENT = pygame.USEREVENT + 1
TOGGLE_CLICKSTART = pygame.USEREVENT + 2
BALL_OUT = pygame.USEREVENT + 3
CHANGE_SPEED_8 = pygame.USEREVENT + 4

screen = pygame.display.set_mode((1920, 1080), vsync = 1)
clock = pygame.time.Clock()
running = True

pygame.mouse.set_visible(0)
pygame.display.set_caption("Breakout")
pygame.display.toggle_fullscreen()

gameStarted = 0
drawBat = 0
debug = 0
clickStartVisible = 1
space = 0

# ustawienia
settingsOpen = False
ballRotationMode = "Dynamic"
leftWallGlitch = "On"

# elementy gry
bat = pygame.Rect(960, 1014, 45, 17) # rect bat
ball = pygame.Rect(960, 540, 13, 10) # rect ball
wallTop = pygame.Rect(588, 0, 745, 35) # rect wallTop
wall = pygame.image.load("wall.png").convert_alpha() # image wallLeft i wallRight
bar = pygame.Rect(585, 1014, 750, 17) # rect bar
wallBottom = pygame.Rect(0, 1070, 1920, 10)
wallLeft2 = pygame.Rect(558, 0, 15, 1080) # dodatkowa czarna lewa sciana za widoczna lewa sciana aby wystepowal Wall Glitch
shortBat = pygame.Rect(982, 1014, 25, 17) # rect shortBat


# ogolne info do cegiel
brickWidth = 45
brickHeight = 15
gapX = 5
gapY = 4
rows = 2
columns = 15

# czerwona cegla
redBrickPosX = 588
redBrickPosY = 169

# pomarańczowa cegla
orangeBrickPosX = 588
orangeBrickPosY = 207

# zielona cegla
greenBrickPosX = 588
greenBrickPosY = 245

# zolta cegla
yellowBrickPosX = 588
yellowBrickPosY = 283

# zmienne predkosci ball
speedMode = "bat"
ballSpeed = 4

# zmienne bat
totalBallHits = 0
smallBat = False

# cechy ball
canBreakBricks = False
isBallOut = True

ballAngle = random.randint(-135, -45)

ballAngleRad = math.radians(ballAngle)

ballVelX = math.cos(ballAngleRad) * ballSpeed
ballVelY = -math.sin(ballAngleRad) * ballSpeed




# ---STARTOWE---
# startowa ball
startBall = pygame.Rect(960, 540, 13, 10)
startBallSpeed = 7

startBallVelX = math.cos(ballAngleRad) * startBallSpeed
startBallVelY = -math.sin(ballAngleRad) * startBallSpeed




# roznica pomiedzy srodkiem bat a srodkiem ball
def checkOffset():
    offset = ball.centerx - bat.centerx
    
    return offset

def dynamicBallRotationAngle():
    maxOffset = bat.width / 2 # max offset czyli polowa dlugosci bat

    offset = checkOffset()
    offset = min(offset, maxOffset) # najmniejsza wartosc z offset i maxOffset

    normalizedOffset = offset / maxOffset # teraz offset jest liczba z przedzialu [-1, 1]

    ballAngle = 90 - normalizedOffset * 45 # ustawianie kata w przedziale [45, 135] w zaleznosci od offset. Im blizej srodka tym normalizedOffset blizszy zeru wiec kat bedzie bardziej pionowy bo mniej sie odejmie od 90

    return ballAngle



# funkcja startujaca gre
def startGame():
    global gameStarted

    gameStarted = 1




# wyrzucenie pilki
def throwBall():
    global ballSpeed, ballAngle, ballAngleRad, ballVelX, ballVelY, ball, isBallOut, totalBallHits, speedMode

    isBallOut = False
    
    ball = pygame.Rect(960, 540, 13, 10) # rect ball
    
    speedMode = "bat"
    ballSpeed = 4
    totalBallHits = 0
    

    ballAngle = random.randint(-135, -45)

    ballAngleRad = math.radians(ballAngle)

    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed
        


# generacja czerwonych cegiel
def generateRedBricks():
    global redBricks, redBrick

    redBricks = [] # czerwone cegly

    for row in range(rows): # 2 rzedy wiec 2 iteracje
        for column in range(columns): # 15 kolumn wiec 15 iteracji
            x = redBrickPosX + column * (brickWidth + gapX) # bazowa pozycja cegly i dodawanie do niej numeru kolumny razy dlugosc cegly i odstep awiec jak pierwsza kolumna to bedzie bazowa pozycja, jak druga kolumna to bazowa + 2 razy cegla + odstep wiec bedzie  w drugiej kolumnie i tak dalej.
            y = redBrickPosY + row * (brickHeight + gapY) # jesli pierwszy rzad to y pozostaje bez zmian, jesli drugi rzad to y sie zwiekszy wysokosc cegly i odstep wiec bedzie w drugim rzedzie

            redBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect czerwonej cegly w oparciu o wyzej stworzone zmienne
            redBricks.append(redBrick)

            pygame.draw.rect(screen, [178, 31, 0], redBrick) # rysowanie czerwonej cegly
    
    return redBricks


# generacja pomaranczowych cegiel
def generateOrangeBricks():
    global orangeBricks, orangeBrick

    orangeBricks = [] # pomaranczowe cegly

    for row in range(rows):
        for column in range(columns):
            x = orangeBrickPosX + column * (brickWidth + gapX)
            y = orangeBrickPosY + row * (brickHeight + gapY)

            orangeBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect pomaranczowsej cegly
            orangeBricks.append(orangeBrick)

            pygame.draw.rect(screen, [214, 136, 0], orangeBrick) # rysowanie pomaranczowej cegly
    
    return orangeBricks


# generacja zielonych cegiel
def generateGreenBricks():
    global greenBricks, greenBrick

    greenBricks = [] # zielone cegly

    for row in range(rows):
        for column in range(columns):
            x = greenBrickPosX + column * (brickWidth + gapX)
            y = greenBrickPosY + row * (brickHeight + gapY)

            greenBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect zielonej cegly
            greenBricks.append(greenBrick)

            pygame.draw.rect(screen, [0, 115, 42], greenBrick) # rysowanie zielonej cegly
    
    return greenBricks


# generacja zoltych cegiel
def generateYellowBricks():
    global yellowBricks, yellowBrick

    yellowBricks = [] # zolte cegly

    for row in range(rows):
        for column in range(columns):
            x = yellowBrickPosX + column * (brickWidth + gapX)
            y = yellowBrickPosY + row * (brickHeight + gapY)

            yellowBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect zoltej cegly
            yellowBricks.append(yellowBrick)

            pygame.draw.rect(screen, [207, 198, 23], yellowBrick) # rysowanie zoltej cegly

    return yellowBricks

# piłka wyleciała
def ballOut():
    global isBallOut
    
    isBallOut = True
    smallBat = False
    
    
def changeSpeed(newSpeed):
    global ballSpeed, ballVelX, ballVelY, ballAngle, ballAngleRad
    
    ballSpeed = newSpeed
    
    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed


    
pygame.time.set_timer(TOGGLE_CLICKSTART, 1000) # 1 sekundowy timer dla "CLICK START"


redBricks = generateRedBricks()
orangeBricks = generateOrangeBricks()
#greenBricks = generateGreenBricks()
#yellowBricks = generateYellowBricks()


while running:
    pressedKeys = pygame.key.get_pressed()

    # obsluga eventow
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if pressedKeys[pygame.K_LCTRL]: # wychodzenie z gry
            running = False
        
        if pressedKeys[pygame.K_d]: # przelaczanie debugu
            if debug == 0:
                debug = 1

            elif debug == 1:
                debug = 0
        
        if pressedKeys[pygame.K_s]: # otwieranie ustawien
            settingsOpen = True
        
        if settingsOpen == True:
            if pressedKeys[pygame.K_ESCAPE]: # zamykanie ustawien
                settingsOpen = False
            
            if pressedKeys[pygame.K_b] and ballRotationMode == "Dynamic": # przelaczenie ballRotationMode na Static
                ballRotationMode = "Static"
            
            elif pressedKeys[pygame.K_b] and ballRotationMode == "Static": # przelaczenie ballRotationMode na Dynamic
                ballRotationMode = "Dynamic"
            
            elif pressedKeys[pygame.K_l] and leftWallGlitch == "On": # wylaczenie Left Wall Glitch
                leftWallGlitch = "Off"
            
            elif pressedKeys[pygame.K_l] and leftWallGlitch == "Off": # wlaczenie Left Wall Glitch
                leftWallGlitch = "On"
        
        if pressedKeys[pygame.K_g] and isBallOut == True and gameStarted == 1: # serwowanie ball
            pygame.time.set_timer(THROW_BALL_EVENT, 1000, loops = 1)
        

        if event.type == pygame.MOUSEBUTTONDOWN and gameStarted == 0: # nacisniecie myszy spowoduje start
            bar.update(10000, 10000, 0, 0)
            startBall.update(10000, 10000, 0, 0)
            drawBat = 1
            clickStartVisible == 0

            startGame() # start gry

        if event.type == THROW_BALL_EVENT: # timer osiagnal 1 sekunde wiec pilka jest serwowana
            throwBall()
        
        if event.type == TOGGLE_CLICKSTART:
            clickStartVisible = not clickStartVisible
            
        if event.type == CHANGE_SPEED_8:
            changeSpeed(7)


    # ruch bat
    mouse_x, _ = pygame.mouse.get_pos()
    bat.centerx = mouse_x
    shortBat.centerx = mouse_x



    # ---RYSOWANIE EKRANU---
    screen.fill("black")


    # rysowanie cegiel
    for redBrick in redBricks:    
        pygame.draw.rect(screen, [178, 31, 0], redBrick) # rysowanie czerwonej cegly

    for orangeBrick in orangeBricks:
        pygame.draw.rect(screen, [214, 136, 0], orangeBrick) # rysowanie pomaranczowej cegly

    """for greenBrick in greenBricks:
        pygame.draw.rect(screen, [0, 115, 42], greenBrick) # rysowanie zielonej cegly

    for yellowBrick in yellowBricks:
        pygame.draw.rect(screen, [207, 198, 23], yellowBrick) # rysowanie zoltej cegly"""

    



    # miganie tekstu "CLICK START"
    if clickStartVisible == 1 and gameStarted == 0:
        freesansbold = pygame.font.Font("freesansbold.ttf", 30)
        clickStartText = freesansbold.render("CLICK START", True, "white")

        screen.blit(clickStartText, [1600, 1000])
    
    # tekst ustawien
    if gameStarted == 0 and settingsOpen == False:
        settingsText = freesansbold.render("SETTINGS", True, "white")
        
        screen.blit(settingsText, [120, 1000])
    
    # tekst otwartych ustawien
    if gameStarted == 0 and settingsOpen == True:
        openSettingsText1 = freesansbold.render("Ball rotation: {}".format(ballRotationMode), True, "white")
        openSettignsText2 = freesansbold.render("B to toggle", True, "white")
        openSettingsText3 = freesansbold.render("Left wall glitch: {}".format(leftWallGlitch), True, "white")
        openSettingsText4 = freesansbold.render("L to toggle", True, "white")
        
        screen.blit(openSettingsText1, [100, 940])
        screen.blit(openSettignsText2, [100, 970])
        screen.blit(openSettingsText3, [100, 1000])
        screen.blit(openSettingsText4, [100, 1030])



    # rysowanie startowej ball
    if startBall.bottom >= 1005 and startBall.bottom < 1039: # startBall niebieska
        pygame.draw.rect(screen, [0, 95, 160], startBall) 

    elif startBall.top <= 319 and startBall.top > 281: # startBall zolta
        pygame.draw.rect(screen, [207, 198, 23], startBall)
    
    elif startBall.top <= 281 and startBall.top > 243: # startBall zielona
        pygame.draw.rect(screen, [0, 115, 42], startBall)

    elif startBall.top <= 243 and startBall.top > 205: # startBall pomaranczowa
        pygame.draw.rect(screen, [214, 136, 0], startBall)

    elif startBall.top <= 205 and startBall.top > 167: # startBall czerwona
        pygame.draw.rect(screen, [178, 31, 0], startBall)
    
    else: # startBall biala
        pygame.draw.rect(screen, "white", startBall)

    


    # rysowanie ball
    if gameStarted == 1 and isBallOut == False:
        if ball.bottom >= 1005 and ball.bottom < 1039: # ball niebieska
            pygame.draw.rect(screen, [0, 95, 160], ball) 

        elif ball.top <= 319 and ball.top > 281: # ball zolta
            pygame.draw.rect(screen, [207, 198, 23], ball)
        
        elif ball.top <= 281 and ball.top > 243: # ball zielona
            pygame.draw.rect(screen, [0, 115, 42], ball)

        elif ball.top <= 243 and ball.top > 205: # ball pomaranczowa
            pygame.draw.rect(screen, [214, 136, 0], ball)

        elif ball.top <= 205 and ball.top > 167: # ball czerwona
            pygame.draw.rect(screen, [178, 31, 0], ball)
        
        else: # ball biala
            pygame.draw.rect(screen, "white", ball)




    pygame.draw.rect(screen, [204, 204, 204], wallTop) # rysowanie wallTop
    wallLeft = screen.blit(wall, [573, 0]) # rysowanie wall lewa
    wallRight = screen.blit(wall, [1333, 0]) # rysowanie wall prawa
    pygame.draw.rect(screen, "black", wallBottom) # rysowanie wallBottom
    pygame.draw.rect(screen, "black", wallLeft2) # rysowanie dodatkowej lewej sciany

    if gameStarted == 0:
        pygame.draw.rect(screen, [0, 95, 155], bar) # rysowanie bar

    if drawBat == 1 and smallBat == False:
        pygame.draw.rect(screen, [0, 95, 155], bat) # rysowanie bat
    
    elif drawBat == 1 and smallBat == True: # rysowanie shortBat
        pygame.draw.rect(screen, [0, 95 , 155], shortBat)
        

    


    # ---BALL---
    # ruch ball
    if gameStarted == 1 and isBallOut == False:
        ball = ball.move(ballVelX, ballVelY)

    # odbicie ball od wallTop
    if ball.colliderect(wallTop):
        ballVelY *= -1
        canBreakBricks = True
        smallBat = True

    # odbicie ball od sciany prawej
    if ball.colliderect(wallRight):
        ballVelX *= -1
        
    # odbicie ball od sciany lewej
    if leftWallGlitch == "On":
        if ball.colliderect(wallLeft2):
            ballVelX *= -1
    
    elif leftWallGlitch == "Off":
        if ball.colliderect(wallLeft):
            ballVelX *= -1
    
    if canBreakBricks == True:
        # odbicie ball od czerwonej cegly
        for idx, redBrick in enumerate(redBricks):
                if ball.colliderect(redBrick):
                    if speedMode == "bat" and canBreakBricks == True: # zmienianie ballSpeed na max
                        pygame.time.set_timer(CHANGE_SPEED_8, 10, loops = 1)
                        canBreakBricks = False
                    
                    ballVelY *= -1
                    
                    del redBricks[idx]

                    canBreakBricks = False

                    speedMode = "brick"
                    break
        
        # odbicie ball od pomaranczowej cegly
        for idx, orangeBrick in enumerate(orangeBricks):
                if ball.colliderect(orangeBrick):
                    ballVelY *= -1


                    if speedMode == "bat" and canBreakBricks == True: # zmienianie ballSpeed na max
                        changeSpeed(7)
                        canBreakBricks = False
                    
                    
                    del orangeBricks[idx]
                    
                    canBreakBricks = False
                    
                    speedMode = "brick"
                    

        # odbicie ball od zielonej cegly
        """for idx, greenBrick in enumerate(greenBricks):
                if ball.colliderect(greenBrick):
                    ballVelY *= -1
                    del greenBricks[idx]

                    canBreakBricks = False
                    break
        
        # odbicie ball od zoltej cegly
        for idx, yellowBrick in enumerate(yellowBricks):
                if ball.colliderect(yellowBrick):
                    ballVelY *= -1
                    del yellowBricks[idx]

                    canBreakBricks = False
                    break"""
    
    # ball wypada
    if ball.colliderect(wallBottom):
        ballOut()



    # ---STARTBALL---
    # odbicie startowej ball od bar
    if gameStarted == 0:
        if startBall.colliderect(bar):
            startBallVelX *= -1
            startBallVelY *= -1

        # odbicie startowej ball od wallTop
        if startBall.colliderect(wallTop):
            startBallVelY *= -1

        # odbicie startowej ball od sciany prawej
        if startBall.colliderect(wallRight):
            startBallVelX *= -1
            
        # odbicie startowej ball od sciany lewej
        if leftWallGlitch == "On":
            if startBall.colliderect(wallLeft2):
                startBallVelX *= -1
        
        elif leftWallGlitch == "Off":
            if startBall.colliderect(wallLeft):
                startBallVelX *= -1

        # ruch startowej ball
        startBall = startBall.move(startBallVelX, startBallVelY)

        # odbicie startowej ball od yellow bricks (reszty nie trzeba bo nigdy ich nie zbije)
        """for idx, yellowBrick in enumerate(yellowBricks):
            if startBall.colliderect(yellowBrick):
                startBallVelY *= -1"""
                
 




    # odbicie ball od bat STATIC
    if ball.colliderect(bat) and ballRotationMode == "Static":
        if checkOffset() > 0 and ballVelX < 0 and ballVelY > 0: # ball leci z prawej w dol, uderza bat od prawej strony
            ballVelX *= -1
            ballVelY *= -1
        
        elif checkOffset() < 0 and ballVelX < 0 and ballVelY > 0: # ball leci z prawej w dol, udeza bat od lewej strony
            ballVelY *= -1

        elif checkOffset() < 0 and ballVelX > 0 and ballVelY > 0: # ball leci z lewej w dol, udeza bat od lewej strony
            ballVelX *= -1
            ballVelY *= -1

        elif checkOffset() > 0 and ballVelX > 0 and ballVelY > 0: # ball leci z lewej w dol, udeza bat od prawej strony
            ballVelY *= -1
        
        canBreakBricks = True
        totalBallHits += 1


        
    # odbicie ball od bat DYNAMIC
    if ball.colliderect(bat) and ballRotationMode == "Dynamic":
        ballAngle = dynamicBallRotationAngle()
        ballAngleRad = math.radians(ballAngle)

        ballVelX = math.cos(ballAngleRad) * ballSpeed
        ballVelY = -math.sin(ballAngleRad) * ballSpeed

        totalBallHits += 1
        
        if totalBallHits == 4 and speedMode == "bat": # zmiana predkosci w zaleznosci od odbic o bat.
            changeSpeed(5)

        elif totalBallHits == 12 and speedMode == "bat":
            changeSpeed(6)

        canBreakBricks = True
    
    
    # wlaczanie albo wylaczanie debugu
    if debug == 1:
        atari = pygame.font.Font("atari.ttf", 20)
        text = atari.render("T: {}; S: {}; A: {}".format(totalBallHits, ballSpeed, ballAngle), True, "white")
        text2 = atari.render("O: {}; X: {}; Y: {}".format(checkOffset(), int(ballVelX), int(ballVelY)), True, "white")
        text3 = atari.render("BALL OUT: {}".format(isBallOut), True, "white")
        text4 = atari.render("SPEED MODE: {}".format(speedMode), True, "white")

        screen.blit(text, [0, 0])
        screen.blit(text2, [0, 25])
        screen.blit(text3, [0, 50])
        screen.blit(text4, [0, 75])
        
    elif debug == 0:
        atari = pygame.font.Font("atari.ttf", 20)
        text = atari.render("T: {}; S: {}; A: {}".format(totalBallHits, ballSpeed, ballAngle), True, "black")
        text2 = atari.render("O: {}; X: {}; Y: {}".format(checkOffset(), int(ballVelX), int(ballVelY)), True, "black")
        text3 = atari.render("BALL OUT: {}".format(isBallOut), True, "black")
        text4 = atari.render("SPEED MODE: {}".format(speedMode), True, "black")

        screen.blit(text, [0, 0])
        screen.blit(text2, [0, 25])
        screen.blit(text3, [0, 50])
        screen.blit(text4, [0, 75])
    
    """print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("O: ", checkOffset())
    print("A: ", ballAngle)
    print("X: ", ballVelX)
    print("Y: ", ballVelY)
    print("TBH: ", totalBallHits)"""
        

    pygame.display.flip()

    clock.tick(240)
