import threading
import pygame
import socket
import sys
import math

name = "test"
playerX = 300
playerY = 200

# position of falling item
imageX = 0
imageY = 0

def GameThread():
    pygame.init()

    screen = pygame.display.set_mode((640,640))

    #assign image
    potato_img = pygame.image.load('potato2.png').convert_alpha()
    player_img = pygame.image.load("basket.png").convert_alpha()
    #create rect for image


    #player start position
    player = pygame.Rect(0, 0, 25, 25)
    playerColor = (0,255,0)

    #scale image
    potato_img = pygame.transform.scale(potato_img, (potato_img.get_width() * 0.05, potato_img.get_height() * 0.05))

    clock = pygame.time.Clock()

    



    score = 0

    font = pygame.font.Font(None, size = 30)

    running = True
    while running:
        #background color
        screen.fill((255,255,255))

        #put image on screen
        screen.blit(potato_img, (imageX, imageY))

        #put player on screen
        player.center = (posx, posy)
        pygame.draw.rect(screen, playerColor, player)

        #hitbox of potato
        #hitbox = pygame.Rect(x, 30, potato_img.get_width(), potato_img.get_height())

        #displays score
        text = font.render('score:', True, (0,0,0))
        screen.blit(text, (300,100))
        #imageX += 1

        #collision
        if player.colliderect(imgRect):
            print("Collision detected!")

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def ServerThread():
    global posy
    global posx
    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("192.168.1.188", 80))
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
            posy -= 10
        if(data == 's'):
            posy += 10
        if(data == 'a'):
            posx -= 10
        if(data == 'd'):
            posx += 10
    conn.close()  # close the connection


t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t1.start()
t2.start()