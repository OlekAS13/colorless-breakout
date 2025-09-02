import pygame
import random
import math

pygame.init()

THROW_BALL_EVENT = pygame.USEREVENT + 1
TOGGLE_CLICKSTART = pygame.USEREVENT + 2
BALL_OUT = pygame.USEREVENT + 3
TOGGLE_POINTS = pygame.USEREVENT + 4
#SOUND_DELAY_WALL = pygame.USEREVENT + 5

screen = pygame.display.set_mode((1920, 1080), vsync = 1)
clock = pygame.time.Clock()
running = True

pygame.mouse.set_visible(0)
pygame.display.set_caption("Breakout")
pygame.display.toggle_fullscreen()

gameStarted = 0
gameEnded = 0
drawPaddle = 0
debug = 0
clickStartVisible = 1
freePlayVisible = 0
space = 0
firstScreenClearedP1 = False
firstScreenClearedP2 = False
infiniteLives = False
pointsVisible = 1
settingsTextVisible = True
totalBarHits = 0
ballsAmount = 6
playerMode = "One-player"
flashPointsP1 = 0
flashPointsP2 = 0

# statystyki
pointsP1 = 0
pointsP2 = 0
lostBallsP1 = 1
lostBallsP2 = 1

# ustawienia
settingsOpen = False
ballRotationMode = "Dynamic"
leftWallGlitch = "On"

# elementy gry
paddle = pygame.Rect(960, 1014, 45, 17) # rect paddle
ball = pygame.Rect(960, 540, 12, 9) # rect ball
wallTop = pygame.Rect(573, 0, 775, 35) # rect wallTop
wall = pygame.image.load("wall.png").convert_alpha() # image wallLeft i wallRight
bar = pygame.Rect(585, 1014, 750, 17) # rect bar
wallBottom = pygame.Rect(0, 1070, 1920, 10)
wallLeft2 = pygame.Rect(558, 0, 15, 1080) # dodatkowa czarna lewa sciana za widoczna lewa sciana aby wystepowal Wall Glitch
shortPaddle = pygame.Rect(982, 1014, 25, 17) # rect shortPaddle
endBar = pygame.Rect(585, 1014, 750, 17) # rect endBar (bar na ekran koncowy)


# ogolne info do cegiel
brickWidth = 45
brickHeight = 13
gapX = 5
gapY = 6
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
speedMode = "paddle"
ballSpeed = 4

# zmienne paddle
totalBallHits = 0
isPaddleShort = False

# cechy ball
canBreakBricks = False
isBallOut = True

whichAngle = random.randint(0, 1) # losowanie kata pilki

if whichAngle == 0:
    ballAngle = -135

elif whichAngle == 1:
    ballAngle = -45

#ballAngle = random.randint(-135, -45)

ballAngleRad = math.radians(ballAngle)

ballVelX = math.cos(ballAngleRad) * ballSpeed
ballVelY = -math.sin(ballAngleRad) * ballSpeed

# ---CZCIONKI---
atari = pygame.font.Font("atari.otf", 70) # czcionka atari
freesansbold = pygame.font.Font("freesansbold.ttf", 30) # czcionka freesansbold


# ---STARTOWE---
# startowa ball
startBall = pygame.Rect(960, 540, 12, 9)
startBallSpeed = 7

startBallVelX = math.cos(ballAngleRad) * startBallSpeed
startBallVelY = -math.sin(ballAngleRad) * startBallSpeed


# ---DZWIEKI---
paddleSound = pygame.mixer.Sound("paddle.wav") # dzwiek paddle
wallSound = pygame.mixer.Sound("wall.mp3") # dzwiek wall
yellowBrickSound = pygame.mixer.Sound("brick.mp3") # dzwiek yellowBrick
greenBrickSound = pygame.mixer.Sound("brick+.wav") # dzwiek greenBrick
orangeBrickSound = pygame.mixer.Sound("brick++.wav") # dzwiek orangeBrick
redBrickSound = pygame.mixer.Sound("brick+++.wav") # dzwiek redBrick
wallGlitchSound = pygame.mixer.Sound("wallGlitch.wav") # dzwiek lewej sciany z glitchem


# roznica pomiedzy srodkiem paddle a srodkiem ball
def checkOffset():
    offset = ball.centerx - paddle.centerx
    
    return offset

def dynamicBallRotationAngle():
    maxOffset = paddle.width / 2 # max offset czyli polowa dlugosci paddle

    offset = checkOffset()
    offset = min(offset, maxOffset) # najmniejsza wartosc z offset i maxOffset

    normalizedOffset = offset / maxOffset # teraz offset jest liczba z przedzialu [-1, 1]

    ballAngle = 90 - normalizedOffset * 45 # ustawianie kata w przedziale [45, 135] w zaleznosci od offset. Im blizej srodka tym normalizedOffset blizszy zeru wiec kat bedzie bardziej pionowy bo mniej sie odejmie od 90

    return ballAngle



# funkcja startujaca gre
def startGame():
    global gameStarted, settingsTextVisible

    gameStarted = 1
    settingsTextVisible = False
    
    pygame.time.set_timer(TOGGLE_POINTS, 125)




# wyrzucenie pilki
def throwBall():
    global ballSpeed, ballAngle, ballAngleRad, ballVelX, ballVelY, ball, isBallOut, totalBallHits, speedMode, whichAngle, totalBarHits

    isBallOut = False
    
    ball = pygame.Rect(random.randint(621, 1300), 540, 12, 9) # rect ball
    
    speedMode = "paddle"
    ballSpeed = 4
    totalBallHits = 0
    totalBarHits = 0
    
    whichAngle = random.randint(0, 1) # losowanie kata

    if whichAngle == 0:
        ballAngle = -135

    elif whichAngle == 1:
        ballAngle = -45
    
    #ballAngle = random.randint(-135, -45)

    ballAngleRad = math.radians(ballAngle)

    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed
        


# generacja czerwonych cegiel
def generateRedBricksP1():
    global redBricksP1, redBrick

    redBricksP1 = [] # czerwone cegly

    for row in range(rows): # 2 rzedy wiec 2 iteracje
        for column in range(columns): # 15 kolumn wiec 15 iteracji
            x = redBrickPosX + column * (brickWidth + gapX) # bazowa pozycja cegly i dodawanie do niej numeru kolumny razy dlugosc cegly i odstep awiec jak pierwsza kolumna to bedzie bazowa pozycja, jak druga kolumna to bazowa + 2 razy cegla + odstep wiec bedzie  w drugiej kolumnie i tak dalej.
            y = redBrickPosY + row * (brickHeight + gapY) # jesli pierwszy rzad to y pozostaje bez zmian, jesli drugi rzad to y sie zwiekszy wysokosc cegly i odstep wiec bedzie w drugim rzedzie

            redBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect czerwonej cegly w oparciu o wyzej stworzone zmienne
            redBricksP1.append(redBrick)

            pygame.draw.rect(screen, "white", redBrick) # rysowanie czerwonej cegly
    
    return redBricksP1


# generacja pomaranczowych cegiel
def generateOrangeBricksP1():
    global orangeBricksP1, orangeBrick

    orangeBricksP1 = [] # pomaranczowe cegly

    for row in range(rows):
        for column in range(columns):
            x = orangeBrickPosX + column * (brickWidth + gapX)
            y = orangeBrickPosY + row * (brickHeight + gapY)

            orangeBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect pomaranczowsej cegly
            orangeBricksP1.append(orangeBrick)

            pygame.draw.rect(screen, "white", orangeBrick) # rysowanie pomaranczowej cegly
    
    return orangeBricksP1


# generacja zielonych cegiel
def generateGreenBricksP1():
    global greenBricksP1, greenBrick

    greenBricksP1 = [] # zielone cegly

    for row in range(rows):
        for column in range(columns):
            x = greenBrickPosX + column * (brickWidth + gapX)
            y = greenBrickPosY + row * (brickHeight + gapY)

            greenBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect zielonej cegly
            greenBricksP1.append(greenBrick)

            pygame.draw.rect(screen, "white", greenBrick) # rysowanie zielonej cegly
    
    return greenBricksP1


# generacja zoltych cegiel
def generateYellowBricksP1():
    global yellowBricksP1, yellowBrick

    yellowBricksP1 = [] # zolte cegly

    for row in range(rows):
        for column in range(columns):
            x = yellowBrickPosX + column * (brickWidth + gapX)
            y = yellowBrickPosY + row * (brickHeight + gapY)

            yellowBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect zoltej cegly
            yellowBricksP1.append(yellowBrick)

            pygame.draw.rect(screen, "white", yellowBrick) # rysowanie zoltej cegly

    return yellowBricksP1

# ---GRACZ 2---
# generacja czerwonych cegiel
def generateRedBricksP2():
    global redBricksP2, redBrick

    redBricksP2 = [] # czerwone cegly

    for row in range(rows): # 2 rzedy wiec 2 iteracje
        for column in range(columns): # 15 kolumn wiec 15 iteracji
            x = redBrickPosX + column * (brickWidth + gapX) # bazowa pozycja cegly i dodawanie do niej numeru kolumny razy dlugosc cegly i odstep awiec jak pierwsza kolumna to bedzie bazowa pozycja, jak druga kolumna to bazowa + 2 razy cegla + odstep wiec bedzie  w drugiej kolumnie i tak dalej.
            y = redBrickPosY + row * (brickHeight + gapY) # jesli pierwszy rzad to y pozostaje bez zmian, jesli drugi rzad to y sie zwiekszy wysokosc cegly i odstep wiec bedzie w drugim rzedzie

            redBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect czerwonej cegly w oparciu o wyzej stworzone zmienne
            redBricksP2.append(redBrick)

            pygame.draw.rect(screen, "white", redBrick) # rysowanie czerwonej cegly
    
    return redBricksP2


# generacja pomaranczowych cegiel
def generateOrangeBricksP2():
    global orangeBricksP2, orangeBrick

    orangeBricksP2 = [] # pomaranczowe cegly

    for row in range(rows):
        for column in range(columns):
            x = orangeBrickPosX + column * (brickWidth + gapX)
            y = orangeBrickPosY + row * (brickHeight + gapY)

            orangeBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect pomaranczowsej cegly
            orangeBricksP2.append(orangeBrick)

            pygame.draw.rect(screen, "white", orangeBrick) # rysowanie pomaranczowej cegly
    
    return orangeBricksP2


# generacja zielonych cegiel
def generateGreenBricksP2():
    global greenBricksP2, greenBrick

    greenBricksP2 = [] # zielone cegly

    for row in range(rows):
        for column in range(columns):
            x = greenBrickPosX + column * (brickWidth + gapX)
            y = greenBrickPosY + row * (brickHeight + gapY)

            greenBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect zielonej cegly
            greenBricksP2.append(greenBrick)

            pygame.draw.rect(screen, "white", greenBrick) # rysowanie zielonej cegly
    
    return greenBricksP2


# generacja zoltych cegiel
def generateYellowBricksP2():
    global yellowBricksP2, yellowBrick

    yellowBricksP2 = [] # zolte cegly

    for row in range(rows):
        for column in range(columns):
            x = yellowBrickPosX + column * (brickWidth + gapX)
            y = yellowBrickPosY + row * (brickHeight + gapY)

            yellowBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect zoltej cegly
            yellowBricksP2.append(yellowBrick)

            pygame.draw.rect(screen, "white", yellowBrick) # rysowanie zoltej cegly

    return yellowBricksP2

# piłka wyleciała
def ballOut():
    global isBallOut, isPaddleShort, lostBallsP1, whichPlayer, lostBallsP2
    
    isBallOut = True
    isPaddleShort = False
    
    if infiniteLives == False:
        if whichPlayer == 1:
            lostBallsP1 += 1
        
        elif whichPlayer == 2:
            lostBallsP2 += 1
    
    if playerMode == "Two-player":
        if whichPlayer == 1 and not(firstScreenClearedP1 == True and not redBricksP1 and not orangeBricksP1 and not greenBricksP1 and not yellowBricksP1):
            whichPlayer = 2
        
        elif whichPlayer == 2 and not(firstScreenClearedP2 == True and not redBricksP2 and not orangeBricksP2 and not greenBricksP2 and not yellowBricksP2):
            whichPlayer = 1
        
    ball.update(960, 540, 13, 10)
    

    
def changeSpeed(newSpeed):
    global ballSpeed, ballVelX, ballVelY, ballAngle, ballAngleRad
    
    ballSpeed = newSpeed
    
    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed
    
def sign(x):
    return (x > 0) - (x < 0)

def resetGame():
    global gameStarted, gameEnded, drawPaddle, clickStartVisible, freePlayVisible, flashPointsP1, flashPointsP2
    global pointsP1, pointsP2, lostBallsP1, lostBallsP2, isBallOut, paddle, shortPaddle, totalBallHits, speedMode
    global ballSpeed, ballVelX, ballVelY, ballAngle, ballAngleRad
    global firstScreenClearedP1, firstScreenClearedP2, isPaddleShort, canBreakBricks, whichPlayer

    gameStarted = 0
    gameEnded = 0
    drawPaddle = 0
    clickStartVisible = 1
    freePlayVisible = 0
    pointsP1 = 0
    pointsP2 = 0
    lostBallsP1 = 1
    lostBallsP2 = 1
    isBallOut = True
    firstScreenClearedP1 = False
    firstScreenClearedP2 = False
    isPaddleShort = False
    totalBallHits = 0
    canBreakBricks = False
    speedMode = "paddle"
    ballSpeed = 4
    flashPointsP1 = 0
    flashPointsP2 = 0
    whichPlayer = 1

    # reset ball angle i prędkość
    whichAngle = random.randint(0, 1)
    if whichAngle == 0:
        ballAngle = -135
    else:
        ballAngle = -45

    ballAngleRad = math.radians(ballAngle)
    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed

    # reset pozycji paddle
    paddle.centerx = 960
    shortPaddle.centerx = 960

    # reset startBall
    startBall.update(960, 540, 13, 10)

    newListsOfBricksP1()
    newListsOfBricksP2()



    
pygame.time.set_timer(TOGGLE_CLICKSTART, 2000) # 1 sekundowy timer dla "CLICK START"

# tworzenie cegiel i zalaczanie kazdej do listy
def newListsOfBricksP1():
    global redBricksP1, orangeBricksP1, greenBricksP1, yellowBricksP1
    
    redBricksP1 = generateRedBricksP1()
    orangeBricksP1 = generateOrangeBricksP1()
    greenBricksP1 = generateGreenBricksP1()
    yellowBricksP1 = generateYellowBricksP1()

def newListsOfBricksP2():
    global redBricksP2, orangeBricksP2, greenBricksP2, yellowBricksP2
    
    redBricksP2 = generateRedBricksP2()
    orangeBricksP2 = generateOrangeBricksP2()
    greenBricksP2 = generateGreenBricksP2()
    yellowBricksP2 = generateYellowBricksP2()

newListsOfBricksP1()
newListsOfBricksP2()


while running:
    dt = clock.get_time() / 1000.0 # delta time w sekundach
    pressedKeys = pygame.key.get_pressed()

    if playerMode == "One-player":
        whichPlayer = 1

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
            
            elif pressedKeys[pygame.K_i]:
                infiniteLives = True

            elif pressedKeys[pygame.K_a] and ballsAmount == 6:
                ballsAmount = 4
            
            elif pressedKeys[pygame.K_a] and ballsAmount == 4:
                ballsAmount = 6

            elif pressedKeys[pygame.K_p] and playerMode == "One-player":
                playerMode = "Two-player"
            
            elif pressedKeys[pygame.K_p] and playerMode == "Two-player":
                playerMode = "One-player"
        
        if pressedKeys[pygame.K_g] or event.type == pygame.MOUSEBUTTONDOWN and isBallOut == True and gameStarted == 1: # serwowanie ball
            pygame.time.set_timer(THROW_BALL_EVENT, random.randint(1000, 3000), loops = 1)
        

        if event.type == pygame.MOUSEBUTTONDOWN and (gameStarted == 0 or gameEnded == 1):
            resetGame()
            bar.update(10000, 10000, 0, 0)
            startBall.update(10000, 10000, 0, 0)
            drawPaddle = 1
            clickStartVisible = 0
            freePlayVisible = 0

            startGame() # start gry

        if event.type == THROW_BALL_EVENT: # timer osiagnal 1 sekunde wiec pilka jest serwowana
            throwBall()
        
        if event.type == TOGGLE_CLICKSTART and settingsTextVisible == True:
            clickStartVisible = not clickStartVisible
            freePlayVisible = not freePlayVisible
        
        if event.type == TOGGLE_POINTS and gameStarted == 1:
            pointsVisible = not pointsVisible

        """if event.type == SOUND_DELAY_WALL:
            pygame.mixer.Sound.play(wallSound)"""


    # ruch paddle
    mouse_x, _ = pygame.mouse.get_pos()
    paddle.centerx = mouse_x
    shortPaddle.centerx = mouse_x

    # ograniczenie do scian
    paddle.left = max(paddle.left, 558)
    paddle.right = min(paddle.right, 1333)
    shortPaddle.left = max(shortPaddle.left, 570)
    shortPaddle.right = min(shortPaddle.right, 1333)



    # ---RYSOWANIE EKRANU---
    screen.fill("black")


    # rysowanie cegiel
    if whichPlayer == 1:
        for redBrick in redBricksP1:    
            pygame.draw.rect(screen, "white", redBrick) # rysowanie czerwonej cegly

        for orangeBrick in orangeBricksP1:
            pygame.draw.rect(screen, "white", orangeBrick) # rysowanie pomaranczowej cegly

        for greenBrick in greenBricksP1:
            pygame.draw.rect(screen, "white", greenBrick) # rysowanie zielonej cegly

        for yellowBrick in yellowBricksP1:
            pygame.draw.rect(screen, "white", yellowBrick) # rysowanie zoltej cegly
    
    elif whichPlayer == 2:
        for redBrick in redBricksP2:    
            pygame.draw.rect(screen, "white", redBrick) # rysowanie czerwonej cegly

        for orangeBrick in orangeBricksP2:
            pygame.draw.rect(screen, "white", orangeBrick) # rysowanie pomaranczowej cegly

        for greenBrick in greenBricksP2:
            pygame.draw.rect(screen, "white", greenBrick) # rysowanie zielonej cegly

        for yellowBrick in yellowBricksP2:
            pygame.draw.rect(screen, "white", yellowBrick) # rysowanie zoltej cegly

    



    # miganie tekstu "CLICK START" i "FREE PLAY"
    if clickStartVisible == 1 and (gameStarted == 0 or gameEnded == 1):
        clickStartText = freesansbold.render("CLICK START", True, "white")

        screen.blit(clickStartText, [1600, 1000])
    
    if freePlayVisible == 1 and (gameStarted == 0 or gameEnded == 1):
        freePlayText = freesansbold.render("FREE PLAY", True, "white")

        screen.blit(freePlayText, [1615, 1000])
    
    # tekst ustawien
    if settingsTextVisible == True and settingsOpen == False:
        settingsText = freesansbold.render("SETTINGS", True, "white")
        
        screen.blit(settingsText, [120, 1000])
    
    # tekst otwartych ustawien
    if settingsTextVisible == True and settingsOpen == True:
        openSettingsText1 = freesansbold.render("Balls amount: {}".format(ballsAmount - 1), True, "white")
        openSettingsText2 = freesansbold.render("A to toggle", True, "white")
        openSettingsText3 = freesansbold.render("Mode: {}".format(playerMode), True, "white")
        openSettingsText4 = freesansbold.render("P to toggle", True, "white")
        openSettingsText5 = freesansbold.render("Ball rotation: {}".format(ballRotationMode), True, "white")
        openSettignsText6 = freesansbold.render("B to toggle", True, "white")
        openSettingsText7 = freesansbold.render("Left wall glitch: {}".format(leftWallGlitch), True, "white")
        openSettingsText8 = freesansbold.render("L to toggle", True, "white")
        openSettingsText9 = freesansbold.render("I for infinite lives", True, "white")
        
        screen.blit(openSettingsText1, [100, 850])
        screen.blit(openSettingsText2, [100, 880])
        screen.blit(openSettingsText3, [100, 790])
        screen.blit(openSettingsText4, [100, 820])
        screen.blit(openSettingsText5, [100, 910])
        screen.blit(openSettignsText6, [100, 940])
        screen.blit(openSettingsText7, [100, 970])
        screen.blit(openSettingsText8, [100, 1000])
        screen.blit(openSettingsText9, [100, 1030])
        
        
    # ---WYSWIETLANIE STATYSTYK---

    
    # tekst gracza
    playerText = atari.render("{}".format(whichPlayer), True, "white")

    
    # miejsce setne punktow
    pointsHundered = atari.render("{}".format(pointsP1 // 100), True, "white")
    
    # miejsce dziesiate punktow
    pointsTen = atari.render("{}".format((pointsP1 // 10) % 10), True, "white")
    
    # miejsce jednosci punktow
    pointsOne = atari.render("{}".format(pointsP1 % 10), True, "white")
        
    # tekst ilosci straconych pilek
    if whichPlayer == 1:
        lostBallsText = atari.render("{}".format(lostBallsP1), True, "white")
    
    elif whichPlayer == 2:
        lostBallsText = atari.render("{}".format(lostBallsP2), True, "white")
    
    # punkty drugiego gracza
    secPointsHundered = atari.render("{}".format(pointsP2 // 100), True, "white")
    secPointsTen = atari.render("{}".format((pointsP2 // 10) % 10), True, "white")
    secPointsOne = atari.render("{}".format(pointsP2 % 10), True, "white")
    
    
    screen.blit(playerText, [567, 20])

    if gameStarted == 1:
        if flashPointsP1 == 1:
            if pointsVisible == 1:
                screen.blit(pointsHundered, [610, 85])
                screen.blit(pointsTen, [660, 85])
                screen.blit(pointsOne, [710, 85])
        
        elif flashPointsP1 == 0:
            screen.blit(pointsHundered, [610, 85])
            screen.blit(pointsTen, [660, 85])
            screen.blit(pointsOne, [710, 85])
        
        if flashPointsP2 == 1:
            if pointsVisible == 1:
                screen.blit(secPointsHundered, [1010, 85])
                screen.blit(secPointsTen, [1060, 85])
                screen.blit(secPointsOne, [1110, 85])
        
        elif flashPointsP2 == 0:
            screen.blit(secPointsHundered, [1010, 85])
            screen.blit(secPointsTen, [1060, 85])
            screen.blit(secPointsOne, [1110, 85])
    
    if gameEnded == 1 or gameStarted == 0:
        screen.blit(pointsHundered, [610, 85])
        screen.blit(pointsTen, [660, 85])
        screen.blit(pointsOne, [710, 85])
        screen.blit(secPointsHundered, [1010, 85])
        screen.blit(secPointsTen, [1060, 85])
        screen.blit(secPointsOne, [1110, 85])

    screen.blit(lostBallsText, [960, 20])

    # rysowanie startowej ball
    # startBall biala
    pygame.draw.rect(screen, "white", startBall)

    


    # rysowanie ball
    if gameStarted == 1 and isBallOut == False:
        # ball biala
        pygame.draw.rect(screen, "white", ball)




    pygame.draw.rect(screen, "white", wallTop) # rysowanie wallTop
    wallLeft = screen.blit(wall, [573, 0]) # rysowanie wall lewa
    wallRight = screen.blit(wall, [1333, 0]) # rysowanie wall prawa
    pygame.draw.rect(screen, "black", wallBottom) # rysowanie wallBottom
    pygame.draw.rect(screen, "black", wallLeft2) # rysowanie dodatkowej lewej sciany

    if gameStarted == 0:
        pygame.draw.rect(screen, "white", bar) # rysowanie bar
    
    if gameEnded == 1: # rysowanie bar na ekreanie koncowym
        pygame.draw.rect(screen, "white", endBar) # rysowanie bar

    if drawPaddle == 1 and isPaddleShort == False and gameEnded == 0:
        pygame.draw.rect(screen, "white", paddle) # rysowanie paddle
    
    elif drawPaddle == 1 and isPaddleShort == True and gameEnded == 0: # rysowanie shortPaddle
        pygame.draw.rect(screen, "white", shortPaddle)
        
    # paddle hider
    pygame.draw.rect(screen, "black", (540, 1014, 33, 17))

    


    # ---BALL---
    # ruch ball
    if gameStarted == 1 and isBallOut == False:
        ball = ball.move(ballVelX * dt * 200, ballVelY * dt * 200)

    # odbicie ball od wallTop
    if ball.colliderect(wallTop):
        ballVelY *= -1
        canBreakBricks = True
        isPaddleShort = True

        # anti-clip
        if ball.top < wallTop.bottom:
            ball.top = wallTop.bottom

    # odbicie ball od sciany prawej
    if ball.colliderect(wallRight):
        ballVelX *= -1
        
        if gameEnded == 0:
            wallSound.stop()
            wallSound.play()

        # anti-clip
        if ball.right > wallRight.left:
            ball.right = wallRight.left
        
    # odbicie ball od sciany lewej
    if leftWallGlitch == "On":
        if ball.colliderect(wallLeft2):
            ballVelX *= -1

            if gameEnded == 0:
                wallGlitchSound.stop()
                wallGlitchSound.play()
        
            # anti-clip
            if ball.left < wallLeft2.right:
                ball.left = wallLeft2.right
    
    elif leftWallGlitch == "Off":
        if ball.colliderect(wallLeft):
            ballVelX *= -1
            
            if gameEnded == 0:
                wallSound.stop()
                wallSound.play()
            
            # anti-clip
            if ball.left < wallLeft.right:
                ball.left = wallLeft.right
    
    # odbijanie ball od cegiel
    if canBreakBricks == True:
        if whichPlayer == 1:
            allBrickRowsP1 = [
                (redBricksP1, 7, redBrickSound),
                (orangeBricksP1, 5, orangeBrickSound),
                (greenBricksP1, 3, greenBrickSound),
                (yellowBricksP1, 1, yellowBrickSound)
            ]

            for brickList, pointValue, sound in allBrickRowsP1:
                for idx, brick in enumerate(brickList):
                    prevBallVelX = ballVelX
                    prevBallVelY = ballVelY

                    if ball.colliderect(brick):
                        if pointValue >= 5 and speedMode == "paddle":
                            changeSpeed(8)

                        if sign(ballVelX) != sign(prevBallVelX):
                            ballVelX *= -1

                        if sign(ballVelY) == sign(prevBallVelY):
                            ballVelY *= -1

                        if gameEnded == 0:
                            del brickList[idx]
                            pointsP1 += pointValue

                        canBreakBricks = False
                        if pointValue >= 5:
                            speedMode = "brick"

                        if gameStarted == 1 and gameEnded == 0:
                            sound.stop()

                            redBrickSound.stop()
                            orangeBrickSound.stop()
                            greenBrickSound.stop()
                            yellowBrickSound.stop()

                            sound.play()
                        break
                if not canBreakBricks:
                    break
        
        # ---GRACZ 2---
        if whichPlayer == 2:
            allBrickRowsP2 = [
                (redBricksP2, 7, redBrickSound),
                (orangeBricksP2, 5, orangeBrickSound),
                (greenBricksP2, 3, greenBrickSound),
                (yellowBricksP2, 1, yellowBrickSound)
            ]

            for brickList, pointValue, sound in allBrickRowsP2:
                for idx, brick in enumerate(brickList):
                    prevBallVelX = ballVelX
                    prevBallVelY = ballVelY

                    if ball.colliderect(brick):
                        if pointValue >= 5 and speedMode == "paddle":
                            changeSpeed(8)

                        if sign(ballVelX) != sign(prevBallVelX):
                            ballVelX *= -1

                        if sign(ballVelY) == sign(prevBallVelY):
                            ballVelY *= -1

                        if gameEnded == 0:
                            del brickList[idx]
                            pointsP2 += pointValue

                        canBreakBricks = False
                        if pointValue >= 5:
                            speedMode = "brick"

                        if gameStarted == 1 and gameEnded == 0:
                            sound.stop()

                            redBrickSound.stop()
                            orangeBrickSound.stop()
                            greenBrickSound.stop()
                            yellowBrickSound.stop()

                            sound.play()
                        break
                if not canBreakBricks:
                    break
    
    # odbicie ball od endBar (ekran koncowy)
    if ball.colliderect(endBar) and gameEnded == 1:
        totalBarHits += 1
        if totalBarHits >= 4:
            ballVelX *= -1
            
        ballVelY *= -1
        
        canBreakBricks = True

        # anti-clip
        if ball.bottom > endBar.top:
            ball.bottom = endBar.top
    
    # ball wypada
    if ball.colliderect(wallBottom):
        ballOut()



    # ---STARTBALL---
    # odbicie startowej ball od bar
    if gameStarted == 0:
        if startBall.colliderect(bar):
            totalBarHits += 1

            if totalBarHits >= 4:
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
        startBall = startBall.move(startBallVelX * dt * 200, startBallVelY * dt * 200)

        # odbicie startowej ball od yellow bricks (reszty nie trzeba bo nigdy ich nie zbije)
        for idx, yellowBrick in enumerate(yellowBricksP1):
            if startBall.colliderect(yellowBrick):
                startBallVelY *= -1
                
 




    # odbicie ball od paddle STATIC
    if ball.colliderect(paddle) and ballRotationMode == "Static":
        ballVelX = math.cos(ballAngleRad) * ballSpeed
        ballVelY = -math.sin(ballAngleRad) * ballSpeed

        if checkOffset() > 0 and ballVelX < 0 and ballVelY > 0: # ball leci z prawej w dol, uderza paddle od prawej strony
            ballVelX *= -1
            ballVelY *= -1
        
        elif checkOffset() < 0 and ballVelX < 0 and ballVelY > 0: # ball leci z prawej w dol, udeza paddle od lewej strony
            ballVelY *= -1

        elif checkOffset() < 0 and ballVelX > 0 and ballVelY > 0: # ball leci z lewej w dol, udeza paddle od lewej strony
            ballVelX *= -1
            ballVelY *= -1

        elif checkOffset() > 0 and ballVelX > 0 and ballVelY > 0: # ball leci z lewej w dol, udeza paddle od prawej strony
            ballVelY *= -1
        
        canBreakBricks = True
        
        # generacja drugiego ekranu cegiel
        if whichPlayer == 1:
            if not redBricksP1 and not orangeBricksP1 and not greenBricksP1 and not yellowBricksP1 and firstScreenClearedP1 == False:
                newListsOfBricksP1()
                firstScreenClearedP1 = True
        
        # ---GRACZ 2---
        if whichPlayer == 2:
            if not redBricksP2 and not orangeBricksP2 and not greenBricksP2 and not yellowBricksP2 and firstScreenClearedP2 == False:
                newListsOfBricksP2()
                firstScreenClearedP2 = True

        totalBallHits += 1

        if totalBallHits == 3 and speedMode == "paddle": # zmiana predkosci w zaleznosci od odbic o paddle. Predkosc zmienia sie przy kolejnym odbiciu dlatego totalBallHits jest o 1 mniejsze
            ballSpeed = 5

        elif totalBallHits == 11 and speedMode == "paddle":
            ballSpeed = 6

        if gameEnded == 0:
            paddleSound.stop()
            paddleSound.play()

        """# anti-clip
        if ball.bottom > paddle.top:
            ball.bottom = paddle.top"""

    # odbicie ball od paddle DYNAMIC
    if ball.colliderect(paddle) and ballRotationMode == "Dynamic":
        ballAngle = dynamicBallRotationAngle()
        ballAngleRad = math.radians(ballAngle)

        ballVelX = math.cos(ballAngleRad) * ballSpeed
        ballVelY = -math.sin(ballAngleRad) * ballSpeed

        totalBallHits += 1
        
        if totalBallHits == 3 and speedMode == "paddle": # zmiana predkosci w zaleznosci od odbic o paddle. Predkosc zmienia sie przy kolejnym odbiciu dlatego totalBallHits jest o 1 mniejsze
            ballSpeed = 5

        elif totalBallHits == 11 and speedMode == "paddle":
            ballSpeed = 6

        canBreakBricks = True

        if gameEnded == 0:
            paddleSound.stop()
            paddleSound.play()

        
        # generacja drugiego ekranu cegiel
        if whichPlayer == 1:
            if not redBricksP1 and not orangeBricksP1 and not greenBricksP1 and not yellowBricksP1 and firstScreenClearedP1 == False:
                newListsOfBricksP1()
                firstScreenClearedP1 = True
        
        # ---GRACZ 2---
        if whichPlayer == 2:
            if not redBricksP2 and not orangeBricksP2 and not greenBricksP2 and not yellowBricksP2 and firstScreenClearedP2 == False:
                newListsOfBricksP2()
                firstScreenClearedP2 = True
            
        """# anti-clip
        if ball.bottom > paddle.top:
            ball.bottom = paddle.top"""
            
    
    # przegrana
    if playerMode == "One-player":
        if lostBallsP1 == ballsAmount and gameEnded == 0:
            gameEnded = 1
            clickStartVisible = 1
            freePlayVisible = 0
            settingsTextVisible = True
            
            pygame.time.set_timer(THROW_BALL_EVENT, random.randint(1000, 3000), loops = 1)
    
    elif playerMode == "Two-player":
        if lostBallsP1 == ballsAmount and lostBallsP2 == ballsAmount and gameEnded == 0:
            gameEnded = 1
            clickStartVisible = 1
            freePlayVisible = 0
            settingsTextVisible = True
            
            pygame.time.set_timer(THROW_BALL_EVENT, random.randint(1000, 3000), loops = 1)
            
    # ekran koncowy
    if ball.colliderect(yellowBrick) or ball.colliderect(greenBrick) or ball.colliderect(orangeBrick) or ball.colliderect(redBrick) and gameStarted == 1:
        if playerMode == "One-player":
            if whichPlayer == 1:
                if not redBricksP1 and not orangeBricksP1 and not greenBricksP1 and not yellowBricksP1 and firstScreenClearedP1 == True:
                    drawPaddle = 0
                    gameEnded = 1
                    clickStartVisible = 1
                    freePlayVisible = 0
                    settingsTextVisible = True
                
        elif playerMode == "Two-player":
            if whichPlayer == 1:
                if not redBricksP1 and not orangeBricksP1 and not greenBricksP1 and not yellowBricksP1 and firstScreenClearedP1 == True: # koniec gry
                    if not redBricksP2 and not orangeBricksP2 and not greenBricksP2 and not yellowBricksP2 and firstScreenClearedP2 == True:
                        drawPaddle = 0
                        gameEnded = 1
                        clickStartVisible = 1
                        freePlayVisible = 0
                        settingsTextVisible = True
                    
                    else: # zamiana gracza
                        whichPlayer = 2
                        isBallOut = True
                        isPaddleShort = False
                        
                        ball.update(960, 540, 13, 10)
            
            if whichPlayer == 2:
                if not redBricksP2 and not orangeBricksP2 and not greenBricksP2 and not yellowBricksP2 and firstScreenClearedP2 == True: # koniec gry
                    if not redBricksP1 and not orangeBricksP1 and not greenBricksP1 and not yellowBricksP1 and firstScreenClearedP1 == True:
                        drawPaddle = 0
                        gameEnded = 1
                        clickStartVisible = 1
                        freePlayVisible = 0
                        settingsTextVisible = True
                    
                    else: # zamiana gracza
                        whichPlayer = 1
                        isBallOut = True
                        isPaddleShort = False

                        ball.update(960, 540, 13, 10)
    
    if gameEnded == 1 or gameStarted == 0:
        pointsVisible = 1
    
    if gameStarted == 1:
        if whichPlayer == 1:
            flashPointsP1 = 1
            flashPointsP2 = 0

        elif whichPlayer == 2:
            flashPointsP2 = 1
            flashPointsP1 = 0
    
    else:
        flashPointsP1 = 0
        flashPointsP2 = 0
        
    
    
    
    
    # wlaczanie albo wylaczanie debugu
    if debug == 1:
        text = freesansbold.render("T: {}; S: {}; A: {}".format(totalBallHits, ballSpeed, ballAngle), True, "white")
        text2 = freesansbold.render("O: {}; X: {}; Y: {}".format(checkOffset(), round(ballVelX, 2), round(ballVelY, 2)), True, "white")
        text3 = freesansbold.render("BALL OUT: {}".format(isBallOut), True, "white")
        text4 = freesansbold.render("SPEED MODE: {}".format(speedMode), True, "white")
        text5 = freesansbold.render("LOST BALLS 1, 2: {}, {}".format(lostBallsP1, lostBallsP2), True, "white")
        text6 = freesansbold.render("FPS: {}".format(round(pygame.time.Clock.get_fps(clock), 2)), True, "white")

        screen.blit(text, [0, 0])
        screen.blit(text2, [0, 25])
        screen.blit(text3, [0, 50])
        screen.blit(text4, [0, 75])
        screen.blit(text5, [0, 100])
        screen.blit(text6, [0, 125])
        
    elif debug == 0:
        text = freesansbold.render("T: {}; S: {}; A: {}".format(totalBallHits, ballSpeed, ballAngle), True, "black")
        text2 = freesansbold.render("O: {}; X: {}; Y: {}".format(checkOffset(), round(ballVelX, 2), round(ballVelY, 2)), True, "black")
        text3 = freesansbold.render("BALL OUT: {}".format(isBallOut), True, "black")
        text4 = freesansbold.render("SPEED MODE: {}".format(speedMode), True, "black")
        text5 = freesansbold.render("LOST BALLS 1, 2: {}, {}".format(lostBallsP1, lostBallsP2), True, "black")
        text6 = freesansbold.render("FPS: {}".format(round(pygame.time.Clock.get_fps(clock), 2)), True, "black")

        screen.blit(text, [0, 0])
        screen.blit(text2, [0, 25])
        screen.blit(text3, [0, 50])
        screen.blit(text4, [0, 75])
        screen.blit(text5, [0, 100])
        screen.blit(text6, [0, 125])
    
    """print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("O: ", checkOffset())
    print("A: ", ballAngle)
    print("X: ", ballVelX)
    print("Y: ", ballVelY)
    print("TBH: ", totalBallHits)"""
        

    pygame.display.flip()

    clock.tick(240)
