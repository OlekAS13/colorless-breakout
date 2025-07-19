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
firstScreenCleared = False
infiniteLives = False
pointsVisible = 1
settingsTextVisible = True
totalBarHits = 0

# statystyki
points = 0
lostBalls = 1

# ustawienia
settingsOpen = False
ballRotationMode = "Dynamic"
leftWallGlitch = "On"

# elementy gry
paddle = pygame.Rect(960, 1014, 45, 17) # rect paddle
ball = pygame.Rect(960, 540, 13, 10) # rect ball
wallTop = pygame.Rect(573, 0, 775, 35) # rect wallTop
wall = pygame.image.load("wall.png").convert_alpha() # image wallLeft i wallRight
bar = pygame.Rect(585, 1014, 750, 17) # rect bar
wallBottom = pygame.Rect(0, 1070, 1920, 10)
wallLeft2 = pygame.Rect(558, 0, 15, 1080) # dodatkowa czarna lewa sciana za widoczna lewa sciana aby wystepowal Wall Glitch
shortPaddle = pygame.Rect(982, 1014, 25, 17) # rect shortPaddle
endBar = pygame.Rect(585, 1014, 750, 17) # rect endBar (bar na ekran koncowy)


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
atari = pygame.font.Font("atari.otf", 60) # czcionka atari
freesansbold = pygame.font.Font("freesansbold.ttf", 30) # czcionka freesansbold


# ---STARTOWE---
# startowa ball
startBall = pygame.Rect(960, 540, 13, 10)
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
    
    ball = pygame.Rect(random.randint(621, 1300), 540, 13, 10) # rect ball
    
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
def generateRedBricks():
    global redBricks, redBrick

    redBricks = [] # czerwone cegly

    for row in range(rows): # 2 rzedy wiec 2 iteracje
        for column in range(columns): # 15 kolumn wiec 15 iteracji
            x = redBrickPosX + column * (brickWidth + gapX) # bazowa pozycja cegly i dodawanie do niej numeru kolumny razy dlugosc cegly i odstep awiec jak pierwsza kolumna to bedzie bazowa pozycja, jak druga kolumna to bazowa + 2 razy cegla + odstep wiec bedzie  w drugiej kolumnie i tak dalej.
            y = redBrickPosY + row * (brickHeight + gapY) # jesli pierwszy rzad to y pozostaje bez zmian, jesli drugi rzad to y sie zwiekszy wysokosc cegly i odstep wiec bedzie w drugim rzedzie

            redBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect czerwonej cegly w oparciu o wyzej stworzone zmienne
            redBricks.append(redBrick)

            pygame.draw.rect(screen, "white", redBrick) # rysowanie czerwonej cegly
    
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

            pygame.draw.rect(screen, "white", orangeBrick) # rysowanie pomaranczowej cegly
    
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

            pygame.draw.rect(screen, "white", greenBrick) # rysowanie zielonej cegly
    
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

            pygame.draw.rect(screen, "white", yellowBrick) # rysowanie zoltej cegly

    return yellowBricks

# piłka wyleciała
def ballOut():
    global isBallOut, isPaddleShort, lostBalls
    
    isBallOut = True
    isPaddleShort = False
    
    if infiniteLives == False:
        lostBalls +=1
        
        ball.update(960, 540, 13, 10)
    

    
def changeSpeed(newSpeed):
    global ballSpeed, ballVelX, ballVelY, ballAngle, ballAngleRad
    
    ballSpeed = newSpeed
    
    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed
    
def sign(x):
    return (x > 0) - (x < 0)

def resetGame():
    global gameStarted, gameEnded, drawPaddle, clickStartVisible, freePlayVisible
    global points, lostBalls, isBallOut, paddle, shortPaddle, totalBallHits, speedMode
    global ballSpeed, ballVelX, ballVelY, ballAngle, ballAngleRad
    global firstScreenCleared, isPaddleShort, canBreakBricks

    gameStarted = 0
    gameEnded = 0
    drawPaddle = 0
    clickStartVisible = 1
    freePlayVisible = 0
    points = 0
    lostBalls = 1
    isBallOut = True
    firstScreenCleared = False
    isPaddleShort = False
    totalBallHits = 0
    canBreakBricks = False
    speedMode = "paddle"
    ballSpeed = 4

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

    newListsOfBricks()



    
pygame.time.set_timer(TOGGLE_CLICKSTART, 2000) # 1 sekundowy timer dla "CLICK START"

# tworzenie cegiel i zalaczanie kazdej do listy
def newListsOfBricks():
    global redBricks, orangeBricks, greenBricks, yellowBricks
    
    redBricks = generateRedBricks()
    orangeBricks = generateOrangeBricks()
    greenBricks = generateGreenBricks()
    yellowBricks = generateYellowBricks()

newListsOfBricks()


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
            
            elif pressedKeys[pygame.K_i]:
                infiniteLives = True
        
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



    # ---RYSOWANIE EKRANU---
    screen.fill("black")


    # rysowanie cegiel
    for redBrick in redBricks:    
        pygame.draw.rect(screen, "white", redBrick) # rysowanie czerwonej cegly

    for orangeBrick in orangeBricks:
        pygame.draw.rect(screen, "white", orangeBrick) # rysowanie pomaranczowej cegly

    for greenBrick in greenBricks:
        pygame.draw.rect(screen, "white", greenBrick) # rysowanie zielonej cegly

    for yellowBrick in yellowBricks:
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
        openSettingsText1 = freesansbold.render("Ball rotation: {}".format(ballRotationMode), True, "white")
        openSettignsText2 = freesansbold.render("B to toggle", True, "white")
        openSettingsText3 = freesansbold.render("Left wall glitch: {}".format(leftWallGlitch), True, "white")
        openSettingsText4 = freesansbold.render("L to toggle", True, "white")
        openSettingsText5 = freesansbold.render("I for infinite lives", True, "white")
        
        screen.blit(openSettingsText1, [100, 910])
        screen.blit(openSettignsText2, [100, 940])
        screen.blit(openSettingsText3, [100, 970])
        screen.blit(openSettingsText4, [100, 1000])
        screen.blit(openSettingsText5, [100, 1030])
        
        
    # ---WYSWIETLANIE STATYSTYK---

    
    # tekst gracza staky
    playerText = atari.render("I", True, "white")
    
    
    # miejsce setne punktow
    pointsHundered = atari.render("{}".format(points // 100), True, "white")

    """if points // 100 == 0:
        pointsHundered = atari.render("O", True, [204, 204, 204])
    
    elif points // 100 == 1:
        pointsHundered = atari.render("I", True, [204, 204, 204])
    
    elif points // 100 >= 2:
        pointsHundered = atari.render("{}".format(points // 100), True, [204, 204, 204])"""

    
    # miejsce dziesiate punktow
    pointsTen = atari.render("{}".format((points // 10) % 10), True, "white")

    """if (points // 10) % 10 == 0:
        pointsTen = atari.render("O", True, [204, 204, 204])
        
    elif (points // 10) % 10 == 1:
        pointsTen = atari.render("I", True, [204, 204, 204])
    
    elif (points // 10) % 10 >= 2:
        pointsTen = atari.render("{}".format((points // 10) % 10), True, [204, 204, 204])"""
    
    # miejsce jednosci punktow
    pointsOne = atari.render("{}".format(points % 10), True, "white")

    """if points % 10 == 0:
        pointsOne = atari.render("O", True, [204, 204, 204])
    
    elif points % 10 == 1:
        pointsOne = atari.render("I", True, [204, 204, 204])
        
    elif points % 10 >= 2:
        pointsOne = atari.render("{}".format(points % 10), True, [204, 204, 204])"""
        
    
    # tekst ilosci straconych pilek
    lostBallsText = atari.render("{}".format(lostBalls), True, "white")

    """if lostBalls == 0:
        lostBallsText = atari.render("O", True, [204, 204, 204])
        
    elif lostBalls == 1:
        lostBallsText = atari.render("I", True, [204, 204, 204])
        
    elif lostBalls >= 2:
        lostBallsText = atari.render("{}".format(lostBalls), True, [204, 204, 204])"""
    
    # punkty drugiego gracza stale
    secPointsHundered = atari.render("0", True, "white")
    secPointsTen = atari.render("0", True, "white")
    secPointsOne = atari.render("0", True, "white")
    
    
    screen.blit(playerText, [590, 24])
    
    if pointsVisible == 1 and gameEnded == 0:
        screen.blit(pointsHundered, [650, 85])
        screen.blit(pointsTen, [710, 85])
        screen.blit(pointsOne, [770, 85])
    screen.blit(lostBallsText, [985, 24])
    screen.blit(secPointsHundered, [1045, 85])
    screen.blit(secPointsTen, [1105, 85])
    screen.blit(secPointsOne, [1165, 85])

    if gameStarted == 0:
        screen.blit(pointsHundered, [650, 85])
        screen.blit(pointsTen, [710, 85])
        screen.blit(pointsOne, [770, 85])
    
    if gameEnded == 1:
        screen.blit(pointsHundered, [650, 85])
        screen.blit(pointsTen, [710, 85])
        screen.blit(pointsOne, [770, 85])


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
        

    


    # ---BALL---
    # ruch ball
    if gameStarted == 1 and isBallOut == False:
        ball = ball.move(ballVelX, ballVelY)

    # odbicie ball od wallTop
    if ball.colliderect(wallTop):
        ballVelY *= -1
        canBreakBricks = True
        isPaddleShort = True

    # odbicie ball od sciany prawej
    if ball.colliderect(wallRight):
        ballVelX *= -1
        
        if gameEnded == 0:
            wallSound.stop()
            wallSound.play()
        
    # odbicie ball od sciany lewej
    if leftWallGlitch == "On":
        if ball.colliderect(wallLeft2):
            ballVelX *= -1

            if gameEnded == 0:
                wallGlitchSound.stop()
                wallGlitchSound.play()
    
    elif leftWallGlitch == "Off":
        if ball.colliderect(wallLeft):
            ballVelX *= -1
            
            if gameEnded == 0:
                wallSound.stop()
                wallSound.play()
    
    # odbijanie ball od cegiel
    if canBreakBricks == True:
        allBrickRows = [
            (redBricks, 7, redBrickSound),
            (orangeBricks, 5, orangeBrickSound),
            (greenBricks, 3, greenBrickSound),
            (yellowBricks, 1, yellowBrickSound)
        ]

        for brickList, pointValue, sound in allBrickRows:
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
                        points += pointValue

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
    
    """# odpalanie dzwieku przy kolizji z wallLeft
    if ball.colliderect(wallLeft) and gameEnded == 0:
        wallSound.stop()
        wallSound.play()
        
        
        #pygame.time.set_timer(SOUND_DELAY_WALL, 5, loops = 1)"""
        
    
    
    """if canBreakBricks == True:
        # odbicie ball od czerwonej cegly
        for idx, redBrick in enumerate(redBricks):
                prevBallVelX = ballVelX
                prevBallVelY = ballVelY
                
                if ball.colliderect(redBrick):
                    if speedMode == "bat": # zmiana predkosci tylko w wypadku gdy ta jeszcze nie zostala zmieniona
                        changeSpeed(8)
                    
                    if sign(ballVelX) != sign(prevBallVelX): # ewentualne zamienienie znaku gdy cos niepoprawnie sie odbije (to jest bug i tylko tak udalo mi sie go wyeliminowac)
                        ballVelX *= -1
                    
                    if sign(ballVelY) == sign(prevBallVelY): # taka sama zamiana z ballVelY (trzeba to robic poniewaz ballSpeed sie zmienia, to oznacza ze obliczane sa nove ballVel wiec trzeba je tak zamieniac
                        ballVelY *= -1
                    
                    if gameEnded == 0:
                        del redBricks[idx]
                        
                        points += 7

                    canBreakBricks = False
                    speedMode = "brick"

                    if gameEnded == 0:
                        redBrickSound.stop()
                        redBrickSound.play()

                        orangeBrickSound.stop()
                        greenBrickSound.stop()
                        yellowBrickSound.stop()
                    
                    break
        
        # odbicie ball od pomaranczowej cegly
        for idx, orangeBrick in enumerate(orangeBricks):
                prevBallVelX = ballVelX
                prevBallVelY = ballVelY
                
                
                if ball.colliderect(orangeBrick):
                    if speedMode == "bat": # zmiana predkosci tylko w wypadku gdy ta jeszcze nie zostala zmieniona
                        changeSpeed(8)
                        
                    if sign(ballVelX) != sign(prevBallVelX): # ewentualne zamienienie znaku gdy cos niepoprawnie sie odbije (to jest bug i tylko tak udalo mi sie go wyeliminowac)
                        ballVelX *= -1
                        
                    if sign(ballVelY) == sign(prevBallVelY): # taka sama zamiana z ballVelY (trzeba to robic poniewaz ballSpeed sie zmienia, to oznacza ze obliczane sa nove ballVel wiec trzeba je tak zamieniac
                        ballVelY *= -1

                    if gameEnded == 0:
                        del orangeBricks[idx]
                        
                        points += 5
                        
                    canBreakBricks = False
                    speedMode = "brick"

                    if gameEnded == 0:
                        orangeBrickSound.stop()
                        orangeBrickSound.play()

                        redBrickSound.stop()
                        greenBrickSound.stop()
                        yellowBrickSound.stop()

                    break

        # odbicie ball od zielonej cegly
        for idx, greenBrick in enumerate(greenBricks):
                if ball.colliderect(greenBrick):
                    ballVelY *= -1
                    
                    if gameEnded == 0:
                        del greenBricks[idx]

                        points += 3
                        
                    canBreakBricks = False

                    if gameEnded == 0:
                        greenBrickSound.stop()
                        greenBrickSound.play()

                        redBrickSound.stop()
                        orangeBrickSound.stop()
                        yellowBrickSound.stop()

                    break
        
        # odbicie ball od zoltej cegly
        for idx, yellowBrick in enumerate(yellowBricks):
                if ball.colliderect(yellowBrick):
                    ballVelY *= -1
                    
                    if gameEnded == 0:
                        del yellowBricks[idx]
                    
                        points += 1
                        
                    canBreakBricks = False

                    if gameEnded == 0:
                        yellowBrickSound.stop()
                        yellowBrickSound.play()

                        redBrickSound.stop()
                        orangeBrickSound.stop()
                        greenBrickSound.stop()

                    break"""
    
    # odbicie ball od endBar (ekran koncowy)
    if ball.colliderect(endBar) and gameEnded == 1:
        totalBarHits += 1
        if totalBarHits >= 4:
            ballVelX *= -1
            
        ballVelY *= -1
        
        canBreakBricks = True
    
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
        startBall = startBall.move(startBallVelX, startBallVelY)

        # odbicie startowej ball od yellow bricks (reszty nie trzeba bo nigdy ich nie zbije)
        for idx, yellowBrick in enumerate(yellowBricks):
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
        
        if not redBricks and not orangeBricks and not greenBricks and not yellowBricks and firstScreenCleared == False:
            newListsOfBricks()
            firstScreenCleared = True

        totalBallHits += 1

        if totalBallHits == 3 and speedMode == "paddle": # zmiana predkosci w zaleznosci od odbic o paddle. Predkosc zmienia sie przy kolejnym odbiciu dlatego totalBallHits jest o 1 mniejsze
            ballSpeed = 5

        elif totalBallHits == 11 and speedMode == "paddle":
            ballSpeed = 6

        if gameEnded == 0:
            paddleSound.stop()
            paddleSound.play()

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
        if not redBricks and not orangeBricks and not greenBricks and not yellowBricks and firstScreenCleared == False:
            newListsOfBricks()
            firstScreenCleared = True
            
    
    # przegrana
    if lostBalls == 6 and gameEnded == 0:
        gameEnded = 1
        clickStartVisible = 1
        freePlayVisible = 0
        settingsTextVisible = True
        
        pygame.time.set_timer(THROW_BALL_EVENT, random.randint(1000, 3000), loops = 1)
    
            
    # ekran koncowy
    if ball.colliderect(yellowBrick) or ball.colliderect(greenBrick) or ball.colliderect(orangeBrick) or ball.colliderect(redBrick) and gameStarted == 1:
        if not redBricks and not orangeBricks and not greenBricks and not yellowBricks and firstScreenCleared == True:
            drawPaddle = 0
            gameEnded = 1
            clickStartVisible = 1
            freePlayVisible = 0
            settingsTextVisible = True
    
    if gameEnded == 1:
        pointsVisible = 1
        
    
    
    
    
    # wlaczanie albo wylaczanie debugu
    if debug == 1:
        text = freesansbold.render("T: {}; S: {}; A: {}".format(totalBallHits, ballSpeed, ballAngle), True, "white")
        text2 = freesansbold.render("O: {}; X: {}; Y: {}".format(checkOffset(), round(ballVelX, 2), round(ballVelY, 2)), True, "white")
        text3 = freesansbold.render("BALL OUT: {}".format(isBallOut), True, "white")
        text4 = freesansbold.render("SPEED MODE: {}".format(speedMode), True, "white")
        text5 = freesansbold.render("LOST BALLS: {}".format(lostBalls), True, "white")
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
        text5 = freesansbold.render("LOST BALLS: {}".format(lostBalls), True, "black")
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
