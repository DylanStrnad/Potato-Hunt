import threading
import pygame
import socket
import sys
import math
import random

name = "test"
playerX = 300
playerY = 200




def collision(one, two):
    cX = one.x + one.w / 2 >= two.x - two.w / 2 and two.x + two.w / 2 >= one.x - one.w / 2
    cY = one.y + one.h / 2 >= two.y - two.h / 2 and two.y + two.h / 2 >= one.y - one.h / 2
    return (cX and cY)

def GameThread():

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

    clock = pygame.time.Clock()

    



    score = 0

    font = pygame.font.Font(None, size = 30)

    # position of falling item
    imageX = random.randint(1, 630)
    imageY = 0

    #incr speed of falling potato
    speed = 1

    running = True
    while running:

        #background color
        screen.fill((255,255,255))

        #put image on screen
        screen.blit(potato_img, (imageX, imageY))

        screen.blit(player_img, (playerX, playerY))

        #put player on screen
        player.center = (playerX, playerY)
        #pygame.draw.rect(screen, playerColor, player)

        #hitbox of potato
        hitbox = pygame.Rect(imageX + 35, imageY + 19, potato_img.get_width() - 70, potato_img.get_height() - 45)
        #shows the hitbox on screen
        #visiblePotatoHitbox =pygame.Rect(imageX + 35, imageY + 19, potato_img.get_width() - 70, potato_img.get_height() - 45)
        #pygame.draw.rect(screen, playerColor, visiblePotatoHitbox)

        #hitbox of player
        playerHitbox = pygame.Rect(playerX + 20, playerY + 15, player_img.get_width() * .68, player_img.get_height() * .72)
        #shows the hitbox on screen
        #visiblePlayerHitbox =pygame.Rect(playerX + 20, playerY + 15, player_img.get_width() * .68, player_img.get_height() * .72)
        #pygame.draw.rect(screen, playerColor, visiblePlayerHitbox)

        #displays score
        displayScore = font.render(str(score), True, (0,0,0))
        screen.blit(displayScore, (300,100))

        
        # falling potato speed incr
        imageY += 1 * speed

        #collision
        if collision(playerHitbox, hitbox):
            print("Collision detected!")
            imageY += 1000
            if(imageY >= 1000):
                #make location of potato
                imageY = 0
                imageX = random.randint(1, 630)

                score += 1
                speed += 0.25

        #item goes off screen
        if(imageY >= 800):
                #make location of potato
                imageY = 0
                imageX = random.randint(1, 630)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def ServerThread():
    global playerY
    global playerX
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
    while True:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        if(data == 'w'):
            playerY -= 10
        if(data == 's'):
            playerY += 10
        if(data == 'a'):
            playerX -= 10
        if(data == 'd'):
            playerX += 10
    conn.close()  # close the connection


t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t1.start()
t2.start()
