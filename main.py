import pygame, sys, time
from Button import Button
from pyvidplayer import Video
import spritesheet
import random

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
#create game window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Menu")

sprite_sheet_image = pygame.image.load('redHoodChar.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

sprite_sheet_zombie = pygame.image.load('walkingZombie.png').convert_alpha()
sprite_sheet_zombie = spritesheet.SpriteSheet(sprite_sheet_zombie)

sprite_sheet_roll = pygame.image.load('rollingZombie.png').convert_alpha()
sprite_sheet_roll = spritesheet.SpriteSheet(sprite_sheet_roll)


BG = pygame.image.load("assets/backgroundd.png")
BLACK = (0, 0, 0)

animation_list = []
animation_steps = [25, 9, 17, 5, 64, 7]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 38
animation_cooldown2 = 140

frame_char = 0
step_counter = 0

walking_zombie = []
rolling_zombie = []
frame_zombie = 0
frame_roll = 0




for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
       temp_img_list.append(sprite_sheet.get_image(step_counter,  112, 133, 3, BLACK))
       step_counter += 1
    animation_list.append(temp_img_list)

step_counter = 0

for animation in range(8):
    walking_zombie.append(sprite_sheet_zombie.get_image(step_counter,  31.75, 32, 4, BLACK))
    step_counter += 1

step_counter = 0

for animation in range(22):
    temp_img_list = []
    for _ in range(animation):
       temp_img_list.append(sprite_sheet_roll.get_image(step_counter,  32, 28.5, 3, BLACK))
       step_counter += 1
    rolling_zombie.append(temp_img_list)

# COLORS!!! :))
VanDyke = (59, 50, 44)
Feldgrau = (78, 97, 81)
SeaGreen = (94, 140, 97)
Ivory = (254, 255, 234)
Beaver = (169, 124, 115)



def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/foont.ttf", size)

jump_cooldown = 0
def play():
    global action, frame_zombie, jump_cooldown
    last_update = 0
    last_update2 = 0
    frame_char = 0
    frame_zombie = 0
    isJump = False
    isLose = False
    jumpFrames = 40

    # define game variables


    ground_image = pygame.image.load("ground1.png").convert_alpha()
    ground_image = pygame.transform.scale(ground_image, (253 * 1, 87 * 1))
    ground_width = ground_image.get_width()
    ground_height = ground_image.get_height()

    bg_images = []
    for i in range(1, 4):
        bg_image = pygame.image.load(f"bg{i}.png").convert_alpha()
        orig_width = bg_image.get_width()
        orig_height = bg_image.get_height()
        bg_image = pygame.transform.scale(bg_image, (orig_width * 4, orig_height * 4))
        bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()

    scroll = orig_width * 20

    def draw_bg():
        for x in range(10):
            speed = 1
            for i in bg_images:
                screen.blit(i, ((x * bg_width) - scroll * speed, 0))
                speed += 0.2

    def draw_ground():
        for x in range(80):
            screen.blit(ground_image, ((x * ground_width) - scroll * 2.5, WINDOW_HEIGHT - ground_height))


    # maze_pic = pygame.image.load("maze2.jpg")
    # maze_pic = pygame.transform.scale(maze_pic, (1030 * 1.5, 561 * 1.5))

    PLAY_MOUSE_POS = pygame.mouse.get_pos()

    # SCREEN.fill("black")
    # pygame.display.set_caption("maze screen")
    FPS = 60

    # Player properties
    player_size = 50
    player_x = WINDOW_WIDTH // 2 - player_size // 2
    player_y = WINDOW_HEIGHT // 2 - player_size // 2 +8
    player_speed = 3

    zombie_x = -1 * random.randint(100,WINDOW_WIDTH*2)
    zombie_y = 518

    # Initialize game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("have fun - Ore Zohar :)")
    clock = pygame.time.Clock()

    # Game loop
    run = True
    while run:

        # draw world
        draw_bg()
        draw_ground()

        if scroll > 0:
            scroll -= 2
        else:
            scroll = orig_width * 20

        keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT] and scroll > 0:
        #     scroll -= 5
        # elif keys[pygame.K_LEFT]:
        #     scroll = orig_width * 20
        # if keys[pygame.K_RIGHT] and scroll < 3000:
        #     scroll += 5

        if keys[pygame.K_SPACE]:
            isJump = True

        if isJump:
            action = 2
            if (jumpFrames>20):
                player_y-=10
            else:
                player_y+=10
            jumpFrames -= 1
            if (jumpFrames<=0):
                jumpFrames = 40
                isJump = False
                action = 0


        # print ([zombie_x, zombie_y, player_x, player_y])

        if (zombie_x>=700 and zombie_x<=720) and player_y>=300:
            isLose = True
            lost()

        # if keys[pygame.K_LEFT] and player_x > 0:
        #     player_x -= player_speed
        # if keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - player_size:
        #     player_x += player_speed
        # if keys[pygame.K_UP] and player_y > 0:
        #     action = 2
        # if keys[pygame.K_DOWN] and player_y < WINDOW_HEIGHT - player_size:
        #     action = 3

        # SCREEN.blit(maze_pic, (-200, -50))
        # print([player_x, ' ', player_y])

        current_time = pygame.time.get_ticks()
        if ((current_time - last_update) >= animation_cooldown):
            frame_char += 1
            last_update = current_time
        if frame_char >= len(animation_list[action]):
            frame_char = 1
        SCREEN.blit(animation_list[action][frame_char], (player_x, player_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and action > 0:
                    action -= 1
                    frame_char = 0
                if event.key == pygame.K_2 and action < (len(animation_list) - 1):
                    action += 1
                    frame_char = 0

        if ((current_time - last_update2) >= animation_cooldown2):
            frame_zombie += 1
            last_update2 = current_time
            if frame_zombie >= len(walking_zombie):
                frame_zombie = 1
        SCREEN.blit(walking_zombie[frame_zombie], (zombie_x, zombie_y))
        zombie_x=zombie_x+7

        if (zombie_x>WINDOW_WIDTH):
            zombie_x = -1 * random.randint(100,WINDOW_WIDTH*2)




        pygame.display.update()
        # Cap the frame_char rate
        clock.tick(FPS)


def options():

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def lost():

    while True:
        LOST_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        LOST_TEXT = get_font(45).render("you lost... womp womp", True, "Black")
        LOST_RECT = LOST_TEXT.get_rect(center=(640, 220))
        SCREEN.blit(LOST_TEXT, LOST_RECT)

        LOST_BACK = Button(image=None, pos=(640, 400),
                              text_input="try again?", font=get_font(75), base_color="Black", hovering_color=Feldgrau)
        LOST_MENU = Button(image=None, pos=(640, 530),
                           text_input="return to menu", font=get_font(75), base_color="Black", hovering_color=Feldgrau)

        LOST_BACK.changeColor(LOST_MOUSE_POS)
        LOST_BACK.update(SCREEN)
        LOST_MENU.changeColor(LOST_MOUSE_POS)
        LOST_MENU.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOST_BACK.checkForInput(LOST_MOUSE_POS):
                    play()
                if LOST_MENU.checkForInput(LOST_MOUSE_POS):
                    main_menu()

        pygame.display.update()





def intro():
    vid = Video("finalVidForGame.mov")
    vid.set_size((1280, 720))
    while True:
        vid.draw(SCREEN, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                main_menu()

def pilot():
    pilotvid = Video("pilotMsg.mov")
    pilotvid.set_size((1280, 720))
    while True:
        pilotvid.draw(SCREEN, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pilotvid.close()
                main_menu()



def main_menu():
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play()

    while True:

        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("welcome....HAAHAHAHA", True, Ivory)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="careful..", font=get_font(75), base_color=Ivory, hovering_color=Beaver)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="How to escape? ;)", font=get_font(75), base_color=Ivory, hovering_color=Beaver)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="im scared", font=get_font(75), base_color=Ivory, hovering_color=Beaver)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pilot()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


intro()