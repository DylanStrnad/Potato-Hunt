import threading
import pygame
import socket
import sys
import math
import random
import time

playerX = 300
playerY = 500
speed = 1

conn = -1
address = -1

ending = False

clock = pygame.time.Clock()

def collision(one, two):
    cX = one.x + one.w / 2 >= two.x - two.w / 2 and two.x + two.w / 2 >= one.x - one.w / 2
    cY = one.y + one.h / 2 >= two.y - two.h / 2 and two.y + two.h / 2 >= one.y - one.h / 2
    return (cX and cY)

def GameThread():
    global conn
    global address
    global ending
    global clock

    if conn != -1 and address != -1:
        pygame.init()

        screen = pygame.display.set_mode((640,640))

        #assign image
        potato_img = pygame.image.load("potato.png").convert_alpha()
        player_img = pygame.image.load("basket.png").convert_alpha()
        #create rect for image

        #player start position
        player = pygame.Rect(0, 0, 25, 25)
        playerColor = (0,255,0)

        #scale image
        potato_img = pygame.transform.scale(potato_img, (potato_img.get_width() * 0.05, potato_img.get_height() * 0.05))

        player_img = pygame.transform.scale(player_img, (potato_img.get_width() * 1, potato_img.get_height() * 1))

        score = 0

        font = pygame.font.Font(None, size = 30)

        # position of falling item
        imageX = random.randint(-35, 545)
        imageY = 0
        
        bg = pygame.image.load("potatosBG.jpg")
        bg = pygame.transform.scale(bg, (bg.get_width() * 0.2, bg.get_height()* 0.15))

        running = True
        while running == True and ending == False:
            global speed

            #background
            screen.fill((255,255,255))
            screen.blit(bg,(0,0))

            #put image on screen
            screen.blit(potato_img, (imageX, imageY))

            screen.blit(player_img, (playerX, playerY))

            #put player on screen
            player.center = (playerX, playerY)
            #pygame.draw.rect(screen, playerColor, player)

            #displays score
            displayScore = font.render("Score: " + str(score), True, (0,255,0))
            screen.blit(displayScore, (300,100))

            #hitbox of potato
            hitbox = pygame.Rect(imageX + 35, imageY - 19, potato_img.get_width() - 70, potato_img.get_height() - 45)
            #shows the hitbox on screen
            #visiblePotatoHitbox =pygame.Rect(imageX + 35, imageY + 19, potato_img.get_width() - 70, potato_img.get_height() - 45)
            #pygame.draw.rect(screen, playerColor, visiblePotatoHitbox)

            #hitbox of player
            playerHitbox = pygame.Rect(playerX + 20, playerY + 15, player_img.get_width() * .68, player_img.get_height() * .72)
            #shows the hitbox on screen
            #visiblePlayerHitbox =pygame.Rect(playerX + 20, playerY + 15, player_img.get_width() * .68, player_img.get_height() * .72)
            #pygame.draw.rect(screen, playerColor, visiblePlayerHitbox)

            # falling potato speed incr
            imageY += 1 * speed

            #collision
            if collision(playerHitbox, hitbox):
                print("Collision detected!")
                imageY += 1000
                if(imageY >= 1000):
                    #make location of potato
                    imageY = 0
                    imageX = random.randint(potato_img.get_width(), 640 - potato_img.get_width())

                    score += 1
                    speed += 0.25

            #item goes off screen
            if(imageY >= 800):
                    #make location of potato
                    # imageY = 0
                    # imageX = random.randint(1, 630)

                    running = False
                    continue


            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        ending = True
                        break

            pygame.display.flip()
            if ending == False: clock.tick(60)

        while ending == False:
            screen.fill((255, 255, 255))

            gameOverDisplay = font.render("GAME OVER", True, (0, 0, 0))
            screen.blit(gameOverDisplay, (260, 295))
            displayScore = font.render("Final Score: " + str(score), True, (0,0,0))
            screen.blit(displayScore, (260, 320))
            quitButtonText = font.render("Press q to Quit", True, (0, 0, 0))
            screen.blit(quitButtonText, (260, 345))

            pygame.event.get()
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        ending = True
                        break

        pygame.quit()


t1 = threading.Thread(target=GameThread, args=[])

def ServerThread():
    global playerY
    global playerX

    global conn
    global address
    global t1

    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.22.18.96", 80))
    host = s.getsockname()[0]
    s.close()
    print(host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))    
    if conn != -1 and address != -1:
        t1.start()
    while True:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        if(data == 'w'):
            playerY -= 10 * speed
        if(data == 's'):
            playerY += 10 * speed
        if(data == 'a'):
            playerX -= 10 * speed
        if(data == 'd'):
            playerX += 10 * speed
        if(data == 'q'):
            break
    print("Server disabled")
    conn.close()  # close the connection

t2 = threading.Thread(target=ServerThread, args=[])
t2.start()
