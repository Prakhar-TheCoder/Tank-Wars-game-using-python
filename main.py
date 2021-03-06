import pygame, sys

def gameLoop():
    global tank1X, tank1Y, tank2X, tank2Y, tank1_bullet_launch_avoider, tank2_bullet_launch_avoider, hack_mode
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if tank1_bullet_launch_avoider < 10:
                        tank1_bullet_coor_list.append([tank1X+140, tank1Y+tank1.get_height()/2-10])
                        tank1_bullet_launch_avoider = 50
                if event.key == pygame.K_m:
                    if hack_mode == "off":
                        if tank2_bullet_launch_avoider < 10:
                            tank2_bullet_coor_list.append([tank2X-140, tank2Y+tank2.get_height()/2-10])
                            tank2_bullet_launch_avoider = 50
                if event.key == pygame.K_k:
                    hack_mode = "on"

        if pygame.key.get_pressed()[pygame.K_w]:
            if tank1Y > 0:
                tank1Y -= 10
        if pygame.key.get_pressed()[pygame.K_s]:
            if tank1Y < 650-90:
                tank1Y += 10
        if pygame.key.get_pressed()[pygame.K_a]:
            if tank1X > 0:
                tank1X -= 10
        if pygame.key.get_pressed()[pygame.K_d]:
            if tank1X < 1300/2-150:
                tank1X += 10
        if hack_mode == "off":
            if pygame.key.get_pressed()[pygame.K_UP]:
                if tank2Y > 0:
                    tank2Y -= 10
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if tank2Y < 650-90:
                    tank2Y += 10
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if tank2X > 1300/2:
                    tank2X -= 10
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if tank2X < 1300-150:
                    tank2X += 10

        screen.fill((230, 184, 0))
        screen.blit(line, (100+25,-50))
        screen.blit(tank1, (tank1X,tank1Y))
        screen.blit(tank2, (tank2X,tank2Y))
        moveBullets()
        checkCollision()
        tank1_bullet_launch_avoider -= 2
        tank2_bullet_launch_avoider -= 2
        displayHealth(tank1_health, tank2_health)
        pygame.display.update()
        clock.tick(fps)

def moveBullets():
    for coor in tank1_bullet_coor_list:
        if coor[0] > 1300:
            pop_index = tank1_bullet_coor_list.index(coor)
            tank1_bullet_coor_list.pop(pop_index)
            break
        coor[0] += 30
        screen.blit(bullet, (coor[0], coor[1]))
    for coor in tank2_bullet_coor_list:
        if coor[0] < 0-bullet.get_width() :
            pop_index = tank2_bullet_coor_list.index(coor)
            tank2_bullet_coor_list.pop(pop_index)
        coor[0] -= 30
        screen.blit(bullet2, (coor[0], coor[1]))

def checkCollision():
    global tank2_health, tank1_health, winning_tank
    if tank2_health < 1:
        winning_tank = "Player 1(Left)"
        displayGameOverScreen(winning_tank)
    if tank1_health < 1:
        winning_tank = "Player 2(Right)"
        displayGameOverScreen(winning_tank)
    for i in range(len(tank1_bullet_coor_list)):
        bulletX = tank1_bullet_coor_list[i][0] + 115
        bulletY = tank1_bullet_coor_list[i][1]
        tankX = tank2X
        tankUY = tank2Y
        tankDY = tankUY + tank2.get_height()
        if bulletX > tankX and (bulletY > tankUY and bulletY < tankDY):
            tank1_bullet_coor_list.pop(i)
            tank2_health -= 1
            break
    for i in range(len(tank2_bullet_coor_list)):
        bulletX = tank2_bullet_coor_list[i][0]
        bulletY = tank2_bullet_coor_list[i][1]
        tankX = tank1X + tank1.get_width()
        tankUY = tank1Y
        tankDY = tankUY + tank1.get_height()
        if bulletX < tankX and (bulletY > tankUY and bulletY < tankDY):
            tank2_bullet_coor_list.pop(i)
            tank1_health -= 1
            break

def displayGameOverScreen(winner):
    global tank1_bullet_coor_list, tank2_bullet_coor_list, tank1_bullet_launch_avoider, tank2_bullet_launch_avoider, tank1X, tank2X, tank1Y, tank2Y, tank1_health, tank2_health
    winner_name_display = game_font_big.render(f"{winner} has won", True, (255,255,255))
    play_again_display = game_font.render("Press Space Bar to play again", True, (255,255,255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                tank1_bullet_coor_list = []
                tank2_bullet_coor_list = []
                tank1_bullet_launch_avoider = 30
                tank2_bullet_launch_avoider = 30
                tank1X = 10
                tank1Y = 650 / 2 - 20
                tank2X = 1100 + 40
                tank2Y = 650 / 2 - 20
                tank1_health = 5
                tank2_health = 5
                return

        screen.blit(winner_name_display, (1300/2-300, 650/2-50))
        screen.blit(play_again_display, (450, 650/2-50+150))
        pygame.display.update()
        clock.tick(fps)

def displayHealth(tank1_health, tank2_health):
    tank1_health_display = game_font.render("Health : "+str(tank1_health), True, (255,255,255))
    tank2_health_display = game_font.render("Health : "+str(tank2_health), True, (255,255,255))

    screen.blit(tank1_health_display, (0,0))
    screen.blit(tank2_health_display, (1100,0))


pygame.init()
screen = pygame.display.set_mode((1300, 650))
pygame.display.set_caption("Tank Wars")
clock = pygame.time.Clock()
fps = 30

tank1 = pygame.transform.rotate(pygame.image.load("images/tank1.png"), -90)
tank2 = pygame.transform.rotate(pygame.image.load("images/tank2.png"), 90)
bullet = pygame.image.load("images/bullet.png")
bullet2 = pygame.transform.rotate(pygame.image.load("images/bullet.png"), 180)
line = pygame.transform.rotozoom(pygame.image.load("images/line.png"), 90, 3)
pygame.font.init()
game_font_big = pygame.font.Font("OpenSans-Bold.ttf", 60)
game_font = pygame.font.Font("OpenSans-Bold.ttf", 40)

tank1X = 10
tank1Y = 650/2-20
tank2X = 1100+40
tank2Y = 650/2-20
tank1_bullet_launch_avoider = 0
tank2_bullet_launch_avoider = 0

tank1_bullet_coor_list = []
tank2_bullet_coor_list = []

tank1_health = 5
tank2_health = 5
winning_tank = ""
hack_mode = "off"

if __name__ == '__main__':
    gameLoop()