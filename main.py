import pygame,sys
import time,random
import math
import numpy as np
pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_width = 800
display_height = 600

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Snake AI")

icon= pygame.Surface([10, 10])
icon.fill(red)
pygame.display.set_icon(icon)

img= pygame.Surface([10, 10])
img.fill(green)
appleimg= pygame.Surface([10, 10])
appleimg.fill(red)
clock = pygame.time.Clock()

AppleThickness=10
block_size = 10
FPS = 10

# direction="right"

smallfont = pygame.font.SysFont("arial",15)
medfont = pygame.font.SysFont("arial",50)
largefont = pygame.font.SysFont("arial",80)



def game_intro():
    global FPS
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    intro=False
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_f:

                    FPS= 3000
                    print(FPS)
                if event.key == pygame.K_s:

                    FPS= 7
                    print(FPS)
        gameDisplay.fill(white)

        message_to_screen("SmartSnake ",green,-100,"large")
        message_to_screen("",black,-30)
        message_to_screen("",black,10)
        message_to_screen("",black,50)
        message_to_screen("Press C to play, SPACE to pause or Q to quit",black,180)
        pygame.display.update()
        clock.tick(15)

def pause():

    paused=True

    message_to_screen("Paused",black,-100,size="large")
    message_to_screen("Press C to continue or Q to quit",black,25)
    message_to_screen("Controls:up-fastest|down - slowest|left - slower|right - fastter| m - manual/random apple placment| I - information", black, 50)

    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    paused=False
                elif event.key==pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)

def score(score,lead_x,lead_y,applePosX,applePosY,showInfo):

    text=smallfont.render("Score: "+str(score),True,black)
    gameDisplay.blit(text,[0,0])

    if showInfo is True:
        text2 = smallfont.render("X: " + str(lead_x), True, black)
        gameDisplay.blit(text2, [0, 25])

        text3 = smallfont.render("Y: " + str(lead_y), True, black)
        gameDisplay.blit(text3, [0, 50])

        text4 = smallfont.render("apple x: " + str(applePosX), True, black)
        gameDisplay.blit(text4, [0, 75])

        text5 = smallfont.render("apple Y: " + str(applePosY), True, black)
        gameDisplay.blit(text5, [0, 100])

        distanceToApple = math.hypot(applePosX - lead_x, applePosY - lead_y)

        text6 = smallfont.render("Distance to apple: " + str(distanceToApple), True, black)
        gameDisplay.blit(text6, [0, 125])


        obsX = False
        obsY = False

        if (applePosX == lead_x):
            obsX = True
        else:
            obsX = False

        if(applePosY == lead_y):
            obsY = True
        else:
            obsY = False

        text7 = smallfont.render("Food on X: " + str(obsX), True, black)
        gameDisplay.blit(text7, [0, 150])
        text8 = smallfont.render("Food on Y: " + str(obsY), True, black)
        gameDisplay.blit(text8, [0, 175])


def randAppleGen(snakeX,snakeY):
    notOnX = False
    notOnY = False


    randApplex = round(random.randrange(10,display_width-AppleThickness))# padaryti kad gautu  lygini skaiciu
    rAx = randApplex
    rAx = rAx - rAx%10
    randAppley = round(random.randrange(10,display_height-AppleThickness))#/10.0)*10.0
    rAy = randAppley
    rAy = rAy - rAy%10
    applePos =[randApplex,randAppley]

    # if apple on same x or y position move apple by 10 on then axis
    for pos in snakeX:
        if pos == rAx:
            if rAx < display_width:
                rAx+=100
            else:
                rAx-=100

    for poz in snakeY:
        if poz == rAy:
            if rAy < display_height:
                rAy+=100
            else:
                rAy-=100

    if rAy >= 600:
        rAy-=100
    if rAy <= 0:
        rAy+=100

    if rAx >= 800:
        rAx-=100
    if rAx <= 0:
        rAx+=100
    return rAx,rAy


def snake(block_size,snakeList):

    if direction=="right":
        head=pygame.transform.rotate(img,270)
    if direction=="left":
        head=pygame.transform.rotate(img,90)
    if direction=="up":
        head=img
    if direction=="down":
        head=pygame.transform.rotate(img,180)

    gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, (XnY[0],XnY[1],block_size,block_size))

def text_objects(text,color,size):

    if size=="small":
        textSurface=smallfont.render(text,True,color)
    elif size=="medium":
        textSurface=medfont.render(text,True,color)
    elif size=="large":
        textSurface=largefont.render(text,True,color)
    return textSurface,textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size="small"):

    textSurf,textRect=text_objects(msg,color,size)
    textRect.center=(display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf,textRect)


def gameLoop():
    start = True
    randomAppleGen=True
    showInfo = False

    appleonleft = 0
    appleonright = 0
    movesToApple=[]
    movesToAppleAvg=[]
    avg =[]
    obsX = False
    obsY = False
    global direction
    global FPS
    direction = "up"
    """
        decision which direction should first take left or right
    """
    appleonleftCount = 0
    appleonrightCount = 0
    with open("applePositionList.txt", "r") as mfile:
        for line in mfile:
            appleonleftCount, appleonrightCount = line.split(',')





    running = True
    gameOver= False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0


    snakeList=[]
    snakeLength =1
    snakeX = []
    snakeY = []
    if randomAppleGen is True:
        randApplex,randAppley=randAppleGen(snakeX,snakeY)

    while running:


        if gameOver==True:
            message_to_screen("Game over",red,-50,size="large")
            message_to_screen("Press C to play again or Q to quit",black,50,size="medium")
            pygame.display.update()

        while gameOver is True:
            # gameDisplay.fill(white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver=False
                    running=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        running=False
                        gameOver=False
                    if event.key==pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and randomAppleGen is False:
                mx, my = pygame.mouse.get_pos()
                mx = mx - mx % 10
                my = my - my % 10
                print(mx, my)
                randAppley = my
                randApplex = mx

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                   if showInfo is False:
                       showInfo = True
                   else:
                       showInfo = False

                if event.key == pygame.K_SPACE:
                    pause()
                if event.key == pygame.K_DOWN:
                    FPS = 5

                if event.key == pygame.K_UP:
                    FPS = 10000

                if event.key == pygame.K_RIGHT:
                    FPS += 30

                if event.key == pygame.K_LEFT:
                    if FPS-30 >= 0:
                        FPS -= 30
                if event.key == pygame.K_m:
                    if randomAppleGen is True:
                        randomAppleGen = False
                        print('Manual apple placment ON')
                        randApplex = -10
                        randAppley = -10

                    elif randomAppleGen is False:
                        randomAppleGen = True
                        randApplex, randAppley = randAppleGen(snakeX, snakeY)
                        print('Manual apple placment OFF')


            if event.type == pygame.QUIT:
                running = False
        """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:

                   # direction="left"
                    lead_x_change = -block_size
                    lead_y_change = 0

                elif event.key == pygame.K_RIGHT:

                    #direction="right"
                    lead_x_change = block_size
                    lead_y_change = 0

                elif event.key == pygame.K_UP:

                    #direction="up"
                    lead_y_change = -block_size
                    lead_x_change = 0

                elif event.key == pygame.K_DOWN:

                   # direction="down"
                    lead_y_change = block_size
                    lead_x_change = 0
                

        with open("applePositionList.txt", "r") as filestream:
            with open("answers.txt", "w") as filestreamtwo:
                for line in filestream:
                    currentline = line.split("-")
                    avg1 = currentline
                    avg = [sum(x) for x in zip(*avg1)]
                    filestreamtwo.write(str(currentline))
                    """
        # Simple snake AI
        with open("applePositionList.txt", "r") as mfile:
            for line in mfile:
                appleonleftCount, appleonrightCount = line.split(',')
        snake1 = [lead_x, lead_y - 10]
        snake2 = [lead_x - 10, lead_y]
        snake3 = [lead_x, lead_y + 10]
        snake4 = [lead_x + 10, lead_y]

        obsUp = False
        obsDown = False
        obsRight = False
        obsLeft = False

        wallUp = False
        wallDown = False
        wallLeft = False
        wallRight = False
        appleonleftCount = int(appleonleftCount)
        appleonrightCount = int(appleonrightCount)

        if appleonleftCount > appleonrightCount and start is True:
            direction = "left"
            print(appleonleftCount , " " , appleonrightCount, " left")
            start = False
        elif appleonrightCount > appleonleftCount and start is True:
            direction = "right"
            print(appleonleftCount , " " , appleonrightCount , " right")
            start = False
        elif appleonrightCount == appleonleftCount and start is True:
            direction = 'up'
            start = False
            print(appleonleftCount, " ", appleonrightCount, " up")


        for i in snakeList:
           # print(snake1,' and ',i)
            if i == snake1:
                obsUp = True
            if i == snake2:
                obsLeft = True
            if i == snake3:
                obsDown = True
            if i == snake4:
                obsRight = True
        if lead_y == 10:
            obsUp = True
            wallUp = True
        if lead_y == 590:
            obsDown = True
            wallDown = True
        if lead_x == 10:
            obsLeft = True
            wallLeft = True
        if lead_x == 790:
            obsRight = True
            wallRight = True

       # print(direction,'up:', obsUp,'down:', obsDown,'right:', obsRight,'left:', obsLeft)

        if obsRight is True and direction == 'right':
            direction='up'
        elif obsLeft is True and direction == 'left':
            if obsUp is False:
                direction = 'up'
            else:
                direction = 'down'


        if obsUp is True:
            if obsLeft is True :
                direction = 'right'
            elif obsRight is True:
                direction = 'left'
               # print('go left')
            else:
                direction='down'
               # print('go right')
        elif obsDown is True:
            if obsRight is True:
                direction = 'up'
               # print('go up')
            else:
                direction = 'right'
               # print('go up2')

        if obsDown is True and obsUp is True:
            if obsLeft is True:
                direction = 'right'
            else:
                direction = 'left'
        elif obsRight is True and obsLeft is True:
            if obsUp is False:
                direction = 'up'
            else:
                direction = 'down'



        if randApplex == lead_x:
            obsX = True
        else:
            obsX = False

        if randAppley == lead_y:
           obsY = True
        else:
           obsY = False
        """
        if lead_x == 790 and obsUp is False:
            direction = 'up'
        if lead_y == 10 and obsLeft is False:
            direction = 'left'

        if lead_x == 10 and obsDown is False:
            direction = 'down'
        if lead_y == 590 and obsRight is False :
            direction = 'right'

        if lead_x == 10 and lead_y == 10 and direction == "up":
            direction = 'right'
        if lead_x == 790 and lead_y == 10 and direction == "right":
            direction = 'down'
        if lead_x == 790 and lead_y == 590 :
            direction = 'up'
        """

        if obsX is True and lead_y > randAppley:
            if obsUp is False:
                direction = 'up'
        elif obsX is True and lead_y != randAppley:
            if obsDown is False:
                direction = 'down'
        elif obsY is True and lead_x > randApplex:
            if obsLeft is False:
                direction = 'left'
        elif obsY is True and lead_x != randApplex:
            if obsRight is False:
                direction = 'right'


        # --Movement logic--
        if direction == 'left':
            lead_x_change = -block_size
            lead_y_change = 0
            movesToApple.append('left')
        elif direction == 'right':
            lead_x_change = block_size
            lead_y_change = 0
            movesToApple.append('right')
        elif direction == 'up':
            lead_y_change = -block_size
            lead_x_change = 0
            movesToApple.append('up')
        elif direction == 'down':
            lead_y_change = block_size
            lead_x_change = 0
            movesToApple.append('down')


        #---------------------------

        if lead_x >= display_width or lead_x<0 or lead_y<0 or lead_y >= display_height:
            gameOver = True
            print('avg', avg)
            print('snake hit the wall',direction,obsUp,obsDown,obsRight,obsLeft)
            print('average distance moved', np.mean(movesToAppleAvg))
            print('apples on the left: ', appleonleft, '  apples on the right:', appleonright)
            currentline1 = 0
            currentline2 = 0

            with open("applePositionList.txt", "r") as myfile:
                for line in myfile:
                    currentline1, currentline2 = line.split(',')
                currentline1 = int(currentline1)
                currentline2 = int(currentline2)
                currentline1 += int(appleonleft)
                currentline2 += int(appleonright)
                myfile.close()

            with open("applePositionList.txt", 'w') as file:
                file.write(str(currentline1))
                file.write(',')
                file.write(str(currentline2))
                file.close()

        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(white)

        gameDisplay.blit(appleimg,(randApplex,randAppley))



        snakeHead=[]
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)

        snakeX.append(lead_x)
        snakeY.append(lead_y)

        snakeList.append(snakeHead)


        if len(snakeList) > snakeLength:
            del snakeList[0]
            del snakeX[0]
            del snakeY[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment==snakeHead:
                gameOver=True
                print('avg',avg)
                print('snake hit it self: ',direction,' ',obsUp,obsDown,obsRight,obsLeft)
                print('average distance moved', np.mean(movesToAppleAvg))
                print('apples on the left: ',appleonleft,'  apples on the right:',appleonright)
                currentline1=0
                currentline2=0

                with open("applePositionList.txt", "r") as myfile:
                    for line in myfile:
                        currentline1,currentline2 = line.split(',')
                    currentline1 = int(currentline1)
                    currentline2 = int(currentline2)
                    currentline1+=int(appleonleft)
                    currentline2+=int(appleonright)
                    myfile.close()

                with open("applePositionList.txt",'w') as file:
                    file.write(str(currentline1))
                    file.write(',')
                    file.write(str(currentline2))
                    file.close()


        snake(block_size,snakeList)


        score(snakeLength-1,lead_x,lead_y,randApplex,randAppley,showInfo)


        pygame.display.update()

        """
        if lead_x >= randApplex and lead_x <= randApplex + AppleThickness or lead_x+block_size >= randApplex and lead_x+block_size <= randApplex+AppleThickness:
            if lead_y > randAppley and lead_y < randAppley+AppleThickness:
                randApplex,randAppley=randAppleGen()
                snakeLength+=1
            elif lead_y+block_size > randAppley and lead_y+block_size<randAppley+AppleThickness:
                randApplex,randAppley=randAppleGen()
                snakeLength+=1
                """
        if lead_x >= randApplex and lead_x <= randApplex + AppleThickness or lead_x + block_size >= randApplex and lead_x + block_size <= randApplex + AppleThickness:
            if lead_y == randAppley and lead_x == randApplex :

                if randApplex <= display_width / 2:
                    appleonleft += 1
                else:
                    appleonright += 1
                if randomAppleGen is True:
                    randApplex, randAppley = randAppleGen(snakeX,snakeY)
                else:
                    randApplex = -10
                    randAppley = -10
                snakeLength += 1
               # print(len(movesToApple))
                movesToAppleAvg.append(len(movesToApple))
                movesToApple=[]



        clock.tick(FPS)

    pygame.quit()
    quit()


game_intro()
gameLoop()
