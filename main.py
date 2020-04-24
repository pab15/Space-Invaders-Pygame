import csv
import math
import random
import pygame
from pygame import mixer

class Player():
    def __init__(self, player_name, score):
        self.score = int(score)
        self.player_name = player_name

class Scoreboard(): 
    def __init__(self):
        self.player_list = []

    def addPlayer(self, player_name, score):
        self.player_list.append(Player(player_name, score))

    def sortList(self):
        self.player_list.sort(key=lambda player: player.score, reverse = True)

    def createFromCSV(self, file_name):
        file = open(file_name, "r")
        for line in file:
            try:
                line = line.split(',')
                self.addPlayer(line[0], line[1])
            except:
                pass

    def createCSV(self, file_name):
        file = open(file_name, "w")
        count = 0
        for player in self.player_list:
          if count >= 10:
            break
          else:
            file.write("{},{}\n".format(player.player_name, str(player.score)))
            count += 1
        file.close()

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

# Text Box
input_box = pygame.Rect(300, 250, 200, 40)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False

# ScoreBoard:
scores = Scoreboard()

# Sound
# mixer.music.load("background.wav")
# mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    rand_x = random.randint(0, 736)
    rand_y = random.randint(50, 150)
    for x in range(0, len(enemyX)):
        if rand_x < 25 + enemyX[x] and rand_y < 50 + enemyY[x]:
            rand_x += random.randint(50, 75)
    enemyX.append(rand_x)
    enemyY.append(rand_y)
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

double_points = False
triple_points = False
ended = False
# Score

score_value = 0

textX = 10
testY = 10

# Game Over
top_font = pygame.font.Font('freesansbold.ttf', 64)
second_font = pygame.font.Font('freesansbold.ttf', 48)
over_font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(x, y):
    if triple_points == True:
        score = font.render("Score : " + str(score_value) + " (x3)", True, (255, 255, 255))
        screen.blit(score, (x, y))
    elif double_points == True:
        score = font.render("Score : " + str(score_value) + " (x2)", True, (255, 255, 255))
        screen.blit(score, (x, y))
    else:
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    

def show_user_input(x, y):
    user_in = font.render("Enter Your Username and Press Enter to Begin:", True, (255, 255, 255))
    screen.blit(user_in, (x, y))


def game_over_text():
    scores.createFromCSV('scores.csv')
    if ended == False:
        scores.addPlayer(text, score_value)
    scores.sortList()
    top_players = scores.player_list
    first_text = top_font.render('1. ' + top_players[0].player_name + ': ' + str(top_players[0].score), True, (255, 255, 255))
    second_text = second_font.render('2. ' + top_players[1].player_name + ': ' + str(top_players[1].score), True, (255, 255, 255))
    third_text = over_font.render('3. ' + top_players[2].player_name + ': ' + str(top_players[2].score), True, (255, 255, 255))
    fourth_text = over_font.render('4. ' + top_players[3].player_name + ': ' + str(top_players[3].score), True, (255, 255, 255))
    fifth_text = over_font.render('5. ' + top_players[4].player_name + ': ' + str(top_players[4].score), True, (255, 255, 255))
    sixth_text = over_font.render('6. ' + top_players[5].player_name + ': ' + str(top_players[5].score), True, (255, 255, 255))
    seventh_text = over_font.render('7. ' + top_players[6].player_name + ': ' + str(top_players[6].score), True, (255, 255, 255))
    eighth_text = over_font.render('8. ' + top_players[7].player_name + ': ' + str(top_players[7].score), True, (255, 255, 255))
    ninth_text = over_font.render('9. ' + top_players[8].player_name + ': ' + str(top_players[8].score), True, (255, 255, 255))
    tenth_text = over_font.render('10. ' + top_players[9].player_name + ': ' + str(top_players[9].score), True, (255, 255, 255))
    screen.blit(first_text, (260, 25))
    screen.blit(second_text, (330, 100))
    screen.blit(third_text, (225, 160))
    screen.blit(fourth_text, (225, 210))
    screen.blit(fifth_text, (225, 260))
    screen.blit(sixth_text, (225, 310))
    screen.blit(seventh_text, (475, 160))
    screen.blit(eighth_text, (475, 210))
    screen.blit(ninth_text, (475, 260))
    screen.blit(tenth_text, (475, 310))
    scores.createCSV('scores.csv')
    scores.player_list.clear()


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    if score_value >= 10:
        bullet_state = "fire"
        screen.blit(bulletImg, (x - 5, y + 10))
        screen.blit(bulletImg, (x + 16, y + 10))
        screen.blit(bulletImg, (x + 40, y + 10))
    elif score_value >= 6:
        bullet_state = "fire"
        screen.blit(bulletImg, (x - 5, y + 10))
        screen.blit(bulletImg, (x + 40, y + 10))
    elif score_value >= 3:
        bullet_state = "fire"
        screen.blit(bulletImg, (x - 5, y + 10))
        screen.blit(bulletImg, (x + 40, y + 10))
    else:
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    screen.fill((30, 30, 30))
    screen.blit(background, (0, 0))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)
    show_user_input(25, 150)
    pygame.display.flip()
    clock.tick(30)

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # bulletSound = mixer.Sound("laser.wav")
                    # bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            ended = True
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # explosionSound = mixer.Sound("explosion.wav")
            # explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            if score_value >= 10:
                triple_points = True
                double_points = False
                score_value += 3
            elif score_value >= 5:
                double_points = True
                score_value += 2
            else:
                score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()