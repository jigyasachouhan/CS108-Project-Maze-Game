import pygame
import sys
from sys import exit
from random import randint
from maze_generator import *
from collectibles import *
import time
from Scores import *
from aliens import *

# size of the player image on the screen
size = (TILE*1/3, TILE*7/12)

# images for when player moves right
right = []
right.append(pygame.transform.scale(pygame.image.load("images/right2.png"), size))
right.append(pygame.transform.scale(pygame.image.load("images/right1.png"), size))
right.append(pygame.transform.scale(pygame.image.load("images/right3.png"), size))
right.append(pygame.transform.scale(pygame.image.load("images/right1.png"), size))
jright=0

# images for when player moves left
left = []
left.append(pygame.transform.scale(pygame.image.load("images/left1.png"), size))
left.append(pygame.transform.scale(pygame.image.load("images/left2.png"), size))
left.append(pygame.transform.scale(pygame.image.load("images/left3.png"), size))
left.append(pygame.transform.scale(pygame.image.load("images/left2.png"), size))
jleft=0

# images for when player moves up
up = []
up.append(pygame.transform.scale(pygame.image.load("images/up1.png"), size))
up.append(pygame.transform.scale(pygame.image.load("images/up2.png"), size))
up.append(pygame.transform.scale(pygame.image.load("images/up3.png"), size))
up.append(pygame.transform.scale(pygame.image.load("images/up2.png"), size))
jup = 0

# images for when player moves down
down = []
down.append(pygame.transform.scale(pygame.image.load("images/standing.png"), size))
down.append(pygame.transform.scale(pygame.image.load("images/down1.png"), size))
down.append(pygame.transform.scale(pygame.image.load("images/standing.png"), size))
down.append(pygame.transform.scale(pygame.image.load("images/down2.png"), size))
jdown = 0

# alien visibility array
alien_visibility = []
for i in range(20):
    alien_visibility.append(True)
for i in range(40):
    alien_visibility.append(False)

# function to encode the end point of the maze
def winningpos(endpt):
    if endpt == 0:
        winx = RES[0]/2 + TILE/2
        winy = RES[1]/2 - TILE/2
    elif endpt == 1:
        winx = RES[0]/2 + TILE/2 - WIDTH
        winy = RES[1]/2 + TILE/2
    elif endpt == 2:
        winx = RES[0]/2 - TILE/2 - WIDTH
        winy = RES[1]/2 + TILE/2 - HEIGHT
    elif endpt == 3:
        winx = RES[0]/2 - TILE/2
        winy = RES[1]/2 - TILE/2 - HEIGHT
    return (winx, winy)

# declarations of the initial surfaces and pygame window
FPS = 60  # FPS = frame per second
t0 = 90   # default time given, at easy level, 90 seconds
pygame.init()

#  Font definitions
helvetica = pygame.font.Font('pixeboy-font/Pixeboy-z8XGD.ttf', 45)
helvetica_medium = pygame.font.Font('helvetica-255/Helvetica-Bold.ttf', 30)
helveticasmall = pygame.font.Font('helvetica-255/Helvetica-Bold.ttf', 20)
helveticasmaller = pygame.font.Font('helvetica-255/Helvetica-Bold.ttf', 15)

# background surfaces and display window
bg_surface = pygame.image.load("images/extendedstarrysky.jpeg")
bg_surface = pygame.transform.scale(bg_surface, (WIDTH+RES[0], HEIGHT+RES[1]))
background_surf = pygame.Surface((WIDTH+RES[0], HEIGHT+RES[1]))
game_surface = pygame.Surface((WIDTH, HEIGHT))
surface = pygame.display.set_mode((RES[0] , RES[1]+100))
pygame.display.set_caption("The Labyrinth")   #caption of the window
clock = pygame.time.Clock()
rocket = pygame.image.load('images/rocket.png').convert_alpha()

# initializations of game variables
game_active = False
main_menu = True
game_over = False
levels = False
levelchosen = 0
highscorespage = False
won = False
score = 0
tscorecapture = -2  # to display the score added message
ttimecapture = -2  # to display the time added message
kill_allowed = True  #  to check if multiple lives are not lost at once
life_lost = False   # to show a broken heart when a life is lost

# other required images 
spacebg = pygame.image.load('images/Spacebg.jpeg').convert_alpha()
spacebg = pygame.transform.scale(spacebg, (WIDTH, HEIGHT))
standing = pygame.image.load('images/standing.png')
player_img = standing
player_rect = player_img.get_rect()
player_rect.center = RES[0] // 2, RES[1] // 2
life = pygame.image.load('images/heart.png').convert_alpha()
life = pygame.transform.scale(life, (TILE/2, TILE/2))
brokenheart = pygame.image.load('images/brokenheart.png').convert_alpha()
brokenheart = pygame.transform.scale(brokenheart, (TILE*2/5, TILE*2/5))

# background music provided or not
if len(sys.argv)>1:
    if sys.argv[1][-3:]=="mp3":
        bg_music = pygame.mixer.Sound(sys.argv[1])
    else:
        print("Invalid music file provided")
        exit()

else:
    bg_music = pygame.mixer.Sound('Sound/pacmanmusic.mp3')

# play background music
# bg_music.play(loops = -1)

while True:
    
    #event handling loop
    for event in pygame.event.get():
        # quit when the window is closed
        if event.type == pygame.QUIT:
            exit()

        if game_active:
            # end the game session if the time runs out
            if event.type == game_timer:
                game_active = False
                game_over = True
                levels = False
                main_menu = False
                add_score(score)

            # timer for the pointer to the end point when map is collected to disappear
            if mymap.collected:
                if event.type == text_timer:
                    mymap.point = False

            # timer for no life to be lost for one second after a life is lost
            if event.type == nokill_timer:
                kill_allowed = True

            # timer for the broken heart to disappear after one second
            if event.type == life_lost_timer:
                life_lost = False

            if event.type == pygame.KEYDOWN:
                # whichever direction key is pressed, start animation of the player moving in that direction
                if event.key == pygame.K_RIGHT:
                    jright = 0
                if event.key == pygame.K_LEFT:
                    jleft = 0
                if event.key == pygame.K_UP:
                    jup = 0
                if event.key == pygame.K_DOWN:
                    jdown = 0
                    
        elif main_menu:
            # Play button generating a new random maze and other objects inside it
            if event.type == pygame.MOUSEBUTTONDOWN and abs(pygame.mouse.get_pos()[0] - 300) <= 70 and abs(pygame.mouse.get_pos()[1] - 335) <= 15 :
                endpt = randint(0,3)
                maploc = randint(0,3)
                mymap = map(endpt, maploc, False, 2-levelchosen)
                maze, path, found = generate_maze(endpt)
                save_path(path, found)
                num_time_boost = 6 - 2*levelchosen  #number of time boosters dependent on the level chosen
                collected_time_boost = 0
                tbs = []
                num_score_boost = 6 - 2*levelchosen  #number of score boosters dependent on the level chosen
                collected_score_boost = 0
                sbs = []
                # generating random locations for time and score boosters
                for j in range(num_time_boost):
                    tbs.append(timebooster(randint(0,cols-1), randint(0,rows-1)))
                for j in range(num_score_boost):
                    sbs.append(scorebooster(randint(0,cols-1), randint(0,rows-1)))
                # creating an array of aliens to be placed in the maze
                num_aliens = 2 + 2*levelchosen
                j_visibility = 0
                aliens = []
                nokill_timer = pygame.USEREVENT + 3
                life_lost_timer = pygame.USEREVENT + 4
                kill_allowed = True
                life_lost = False
                while len(aliens) < num_aliens:
                    xalien = randint(0,cols-1)
                    yalien = randint(0,rows-1)
                    if xalien == (cols-1)/2 and yalien == (rows-1)/2:
                        continue
                    aliens.append(Alien(randint(0,cols-1), randint(0,rows-1)))
                lives = 6 - 2*levelchosen
                # initial maze location such that the player is at the center of the screen
                maze_locx = (RES[0]-WIDTH)/2
                maze_locy = (RES[1]-HEIGHT)/2
                won = False
                game_active = True
                main_menu = False
                score = 0
                start_time=time.time()
                game_timer = pygame.USEREVENT + 1
                pygame.time.set_timer(game_timer,t0*1000)

            # Levels button to direct to the page to select the level
            if event.type == pygame.MOUSEBUTTONDOWN and abs(pygame.mouse.get_pos()[0] - 300) <= 70 and abs(pygame.mouse.get_pos()[1] - 370) <= 15 :
                levels = True
                main_menu = False

            # Highscores button to direct to the page to display the highscores
            if event.type == pygame.MOUSEBUTTONDOWN and abs(pygame.mouse.get_pos()[0] - 300) <= 70 and abs(pygame.mouse.get_pos()[1] - 410) <= 15 :
                highscorespage = True
                main_menu = False

            # Exit button to quit the game
            if event.type == pygame.MOUSEBUTTONDOWN and abs(pygame.mouse.get_pos()[0] - 300) <= 70 and abs(pygame.mouse.get_pos()[1] - 450) <= 17 :
                exit()

        elif levels:
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                if y<=250:
                    # easy level
                    if x>0 and x<=200:
                        levelchosen = 0
                        t0 = 90

                    # medium level
                    elif x>200 and x<=400:
                        levelchosen = 1
                        t0 = 60

                    # hard level
                    else:
                        levelchosen = 2
                        t0 = 45

                # back to main menu
                if abs(x-300)<=100 and abs(y-450)<20:
                    main_menu = True
                    levels = False           
            
        elif game_over:
            # if the game just ended was won
            if won:
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    # Replay button reinitializing the game
                    if abs(pygame.mouse.get_pos()[0] - 300) <= 75 and abs(pygame.mouse.get_pos()[1] - 402.5) <= 15  :
                        endpt = randint(0,3)
                        maploc = randint(0,3)
                        mymap = map(endpt, maploc, False, 2-levelchosen)
                        maze, path, found = generate_maze(endpt)
                        save_path(path, found)
                        num_time_boost = 6 - 2*levelchosen
                        collected_time_boost = 0
                        tbs = []
                        num_score_boost = 2 + 2*levelchosen
                        collected_score_boost = 0
                        sbs = []
                        for j in range(num_time_boost):
                            tbs.append(timebooster(randint(0,cols-1), randint(0,rows-1)))
                        for j in range(num_score_boost):
                            sbs.append(scorebooster(randint(0,cols-1), randint(0,rows-1)))
                        # creating an array of aliens to be placed in the maze
                        num_aliens = 2 + 2*levelchosen
                        aliens = []
                        kill_allowed = True
                        life_lost = False
                        nokill_timer = pygame.USEREVENT + 3
                        life_lost_timer = pygame.USEREVENT + 4
                        j_visibility = 0
                        while len(aliens) < num_aliens:
                            xalien = randint(0,cols-1)
                            yalien = randint(0,rows-1)
                            if xalien == (cols-1)/2 and yalien == (rows-1)/2:
                                continue
                            aliens.append(Alien(randint(0,cols-1), randint(0,rows-1)))
                        lives = 6 - 2*levelchosen
                        maze_locx = (RES[0]-WIDTH)/2
                        maze_locy = (RES[1]-HEIGHT)/2
                        won = False
                        game_active = True
                        main_menu = False
                        score = 0
                        start_time=time.time()
                        game_timer = pygame.USEREVENT + 1
                        pygame.time.set_timer(game_timer,t0*1000)

                    # Main menu button to go back to the main menu
                    if abs(pygame.mouse.get_pos()[0] - 300) <= 75 and abs(pygame.mouse.get_pos()[1] - 444) <= 15  :
                        main_menu = True
                        levels = False
                        highscorespage = False
                        game_over = False

            else:
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    # Replay button reinitializing the game
                    if abs(pygame.mouse.get_pos()[0] - 300) <= 112.5 and abs(pygame.mouse.get_pos()[1] - 407.5) <= 22.5  :
                        endpt = randint(0,3)
                        maploc = randint(0,3)
                        mymap = map(endpt, maploc, False, 2-levelchosen)
                        maze, path, found = generate_maze(endpt)
                        save_path(path, found)
                        num_time_boost = 6 - 2*levelchosen
                        collected_time_boost = 0
                        tbs = []
                        num_score_boost = 2 + 2*levelchosen
                        collected_score_boost = 0
                        sbs = []
                        for j in range(num_time_boost):
                            tbs.append(timebooster(randint(0,cols-1), randint(0,rows-1)))
                        for j in range(num_score_boost):
                            sbs.append(scorebooster(randint(0,cols-1), randint(0,rows-1)))
                        # creating an array of aliens to be placed in the maze
                        num_aliens = 2 + 2*levelchosen
                        aliens = []
                        kill_allowed = True
                        life_lost = False
                        nokill_timer = pygame.USEREVENT + 3
                        life_lost_timer = pygame.USEREVENT + 4
                        j_visibility = 0
                        while len(aliens) < num_aliens:
                            xalien = randint(0,cols-1)
                            yalien = randint(0,rows-1)
                            if xalien == (cols-1)/2 and yalien == (rows-1)/2:
                                continue
                            aliens.append(Alien(randint(0,cols-1), randint(0,rows-1)))
                        lives = 6 - 2*levelchosen
                        maze_locx = (RES[0]-WIDTH)/2
                        maze_locy = (RES[1]-HEIGHT)/2
                        won = False
                        game_active = True
                        main_menu = False
                        score = 0
                        start_time=time.time()
                        game_timer = pygame.USEREVENT + 1
                        pygame.time.set_timer(game_timer,t0*1000)

                    # Main menu button to go back to the main menu
                    if abs(pygame.mouse.get_pos()[0] - 300) <= 112.5 and abs(pygame.mouse.get_pos()[1] - 456) <= 22.5  :
                        main_menu = True
                        levels = False
                        highscorespage = False
                        game_over = False

        elif highscorespage:
            # Main menu button to go back to the main menu
            if event.type == pygame.MOUSEBUTTONDOWN and abs(pygame.mouse.get_pos()[0] - 300) <= 60 and abs(pygame.mouse.get_pos()[1] - 485) <= 25 :
                main_menu = True
                highscorespage = False

    if game_active:
        
        # movement of the player
        keys_pressed = pygame.key.get_pressed()
        bounce_back=8
        movement=8

        # up key pressed makes the maze move down
        if keys_pressed[pygame.K_UP]:
            # the player img should keep rotating between the up images
            player_img = up[round(jup)]
            player_rect = player_img.get_rect()
            player_rect.center = RES[0] // 2, RES[1] // 2
            jup = jup + 0.3
            if jup>3:
                jup = 0
            maze_locy += movement
            temp = [cell.get_rects(locx=maze_locx, locy=maze_locy) for cell in maze]
            walls_collide_list = []
            for x in temp:
                for y in x:
                    walls_collide_list.append(y)

            # if the player collides with a wall, the maze moves back to the original location ie no movement allowed
            if player_rect.collidelist(walls_collide_list)!=(-1):
                maze_locy -= bounce_back
        
        # down key pressed makes the maze move up
        elif keys_pressed[pygame.K_DOWN]:
            # the player img should keep rotating between the down images
            player_img = down[round(jdown)]
            player_rect = player_img.get_rect()
            player_rect.center = RES[0] // 2, RES[1] // 2
            jdown = jdown + 0.3
            if jdown>3:
                jdown = 0
            maze_locy -= movement
            temp = [cell.get_rects(locx=maze_locx, locy=maze_locy) for cell in maze]
            walls_collide_list = []
            for x in temp:
                for y in x:
                    walls_collide_list.append(y)
            # if the player collides with a wall, the maze moves back to the original location ie no movement allowed
            if player_rect.collidelist(walls_collide_list)!=(-1):
                maze_locy += bounce_back
        
        # left key pressed makes the maze move right
        elif keys_pressed[pygame.K_LEFT]:
            # the player img should keep rotating between the left images
            player_img = left[round(jleft)]
            player_rect = player_img.get_rect()
            player_rect.center = RES[0] // 2, RES[1] // 2
            jleft = jleft + 0.3
            if jleft>3:
                jleft = 0
            maze_locx += movement
            temp = [cell.get_rects(locx=maze_locx, locy=maze_locy) for cell in maze]
            walls_collide_list = []
            for x in temp:
                for y in x:
                    walls_collide_list.append(y)
            
            # if the player collides with a wall, the maze moves back to the original location ie no movement allowed
            if player_rect.collidelist(walls_collide_list)!=(-1):
                maze_locx -= bounce_back
        
        # right key pressed makes the maze move left
        elif keys_pressed[pygame.K_RIGHT]:
            # the player img should keep rotating between the right images
            player_img = right[round(jright)]
            player_rect = player_img.get_rect()
            player_rect.center = RES[0] // 2, RES[1] // 2
            jright = jright+0.3
            if jright>3:
                jright = 0
            maze_locx -= movement
            temp = [cell.get_rects(locx=maze_locx, locy=maze_locy) for cell in maze]
            walls_collide_list = []
            for x in temp:
                for y in x:
                    walls_collide_list.append(y)
            
            # if the player collides with a wall, the maze moves back to the original location ie no movement allowed
            if player_rect.collidelist(walls_collide_list)!=(-1):
                maze_locx += bounce_back

        else:
            player_img = standing
            player_img = pygame.transform.rotozoom(player_img, 0, 0.1)
            player_rect = player_img.get_rect()
            player_rect.center = RES[0] // 2, RES[1] // 2

        winx, winy = winningpos(endpt)

        # if the player reaches the end point, the game is won
        if (abs(maze_locx - winx) <= TILE/4 and abs(maze_locy - winy) <= TILE/4):
            won = True
            game_active = False
            levels = False
            game_over = True
            add_score(score) # add the score to the highscores list

        # if the map is collected, the arrow towards the end point is shown
        if not mymap.collected and (abs(maze_locx - (RES[0]/2 - mymap.x))<=TILE/4 and abs(maze_locy - (RES[1]/2 - mymap.y))<=TILE/4):
            mymap.collected = True 
            collected_time_boost = + 1
            text_timer = pygame.USEREVENT + 2
            pygame.time.set_timer(text_timer, 1000)
            mymap.point = True
            i = 0  # counter for the animation of arrow

        # if the player collides with a time booster, the time is increased by 5 seconds
        j_for_timeboosters = num_time_boost - 1
        while j_for_timeboosters>=0:
            if (not tbs[j_for_timeboosters].collected) and (abs(maze_locx - (RES[0]/2 - tbs[j_for_timeboosters].x))<=TILE/4 and abs(maze_locy - (RES[1]/2 - tbs[j_for_timeboosters].y))<=TILE/4):
                tbs[j_for_timeboosters].collected = True
                pygame.time.set_timer(game_timer, int(((t0 - ((time.time())-(start_time)) + 5*collected_time_boost) + 5)*1000))
                collected_time_boost+=1
                tbs.pop(j_for_timeboosters)
                ttimecapture = time.time()
                index_time_added = 0
                break
            j_for_timeboosters -= 1
        
        # if the number of time boosters reduces less than they should be, new time boosters are generated
        if len(tbs)<num_time_boost:
            for k in range(num_time_boost-len(tbs)):
                tbs.append(timebooster(randint(0,cols-1),randint(0,rows-1)))

        # if the player collides with a score booster, the score is increased by 500
        j_for_scoreboosters = num_score_boost - 1
        while j_for_scoreboosters>=0:
            if (not sbs[j_for_scoreboosters].collected) and (abs(maze_locx - (RES[0]/2 - sbs[j_for_scoreboosters].x))<=TILE/4 and abs(maze_locy - (RES[1]/2 -sbs[j_for_scoreboosters].y))<=TILE/4):
                sbs[j_for_scoreboosters].collected = True
                collected_score_boost+=1
                sbs.pop(j_for_scoreboosters)
                tscorecapture = time.time()
                index_score_added = 0
                break
            j_for_scoreboosters -= 1
        
        # if the number of score boosters reduces less than they should be, new score boosters are generated
        if len(sbs)<num_score_boost:
            for k in range(num_score_boost-len(sbs)):
                sbs.append(scorebooster(randint(0,cols-1),randint(0,rows-1)))

        background_surf.blit(bg_surface, (0,0))  # background surface
        rocket = pygame.transform.scale(rocket, (TILE, TILE+50))    # rocket image resized to fit properly

        # rocket image placed at the end point of the maze
        if endpt == 0:
            x0 = -TILE/2
            y0 = TILE/2
            rocket_rect = rocket.get_rect(center = (x0+RES[0]/2, y0+RES[1]/2))
        elif endpt == 1:
            x0 = WIDTH - TILE/2
            y0 = -TILE/2
            rocket_rect = rocket.get_rect(center = (x0+RES[0]/2, y0+RES[1]/2-TILE//3))
        elif endpt == 2:
            x0 = WIDTH + TILE/2
            y0 = HEIGHT - TILE/2
            rocket_rect = rocket.get_rect(center = (x0+RES[0]/2, y0+RES[1]/2))
        elif endpt == 3:
            x0 = TILE/2
            y0 = HEIGHT + TILE/2
            rocket_rect = rocket.get_rect(center = (x0+RES[0]/2, y0+RES[1]/2+TILE//3))
        background_surf.blit(rocket, rocket_rect)
    
        # drawing the maze and a space themed background
        game_surface.blit(spacebg, (0,0))
        [cell.draw(game_surface) for cell in maze]

        # drawing the map
        if not mymap.collected:
            mymap.draw(game_surface)

        # drawing the time boosters and score boosters
        for j in range(len(tbs)):
            tbs[j].draw(game_surface)
        for j in range(len(sbs)):
            sbs[j].draw(game_surface)

        # drawing the aliens
        if alien_visibility[j_visibility]:
            for j in range(num_aliens):
                aliens[j].draw(game_surface)
            
            for j in range(num_aliens):
                if kill_allowed and abs(maze_locx - (RES[0]/2 - aliens[j].x))<=TILE/3 and abs(maze_locy - (RES[1]/2 - aliens[j].y))<=TILE/3:
                    lives -= 1
                    pygame.time.set_timer(nokill_timer, 1000)
                    pygame.time.set_timer(life_lost_timer, 1000)
                    kill_allowed = False
                    life_lost = True
                    break
        j_visibility = (j_visibility + 1)%60

        # placing the whole game screen on the background surface
        background_surf.blit(game_surface, (RES[0]/2,RES[1]/2))

        # placing the background with the maze on the display screen
        surface.blit(background_surf, (maze_locx-RES[0]/2, maze_locy-RES[1]/2))

        # show the arrow to the end point if the map is collected
        if mymap.point:
            arr = []
            for k in range(3):
                for j in range(5):
                    arr.append(1)
                for j in range(5):
                    arr.append(0.9)
                for j in range(5):
                    arr.append(0.8)
                for j in range(5):
                    arr.append(0.7)
                for j in range(5):
                    arr.append(0.8)
                for j in range(5):
                    arr.append(0.9)
            mymap.showdir(surface, arr[i])
            i = (i + 1)

        player_img = pygame.transform.scale(player_img, size)
        surface.blit(player_img, player_rect)  # player image placed on the display screen at the centre all the time
        scoreboard = pygame.Rect((0,600),(600,100))
        pygame.draw.rect(surface, 'black', scoreboard) # score board at the bottom of the screen

        # time left and score displayed on the scoreboard
        time_left = int(t0 - (int(time.time())-int(start_time)) + 5*collected_time_boost) 
        time_message = helvetica.render(f'Time left: {time_left}',False,'white')
        time_message_rect = time_message.get_rect(center = (150,650))
        score = int((t0 - ((time.time())-(start_time)) + 5*collected_time_boost) * 10) * 15  + 500*collected_score_boost
        score_msg = helvetica.render(f'Score: {score}', False, 'white')
        score_msg_rect = score_msg.get_rect(center = (450, 650))
        surface.blit(score_msg, score_msg_rect)
        surface.blit(time_message,time_message_rect)

        # if a score booster is collected, a message showing 500 points added is displayed
        if (time.time()-tscorecapture)<0.5:
            arr_score = []
            for k in range(50):
                arr_score.append(1-k*0.9/50)
            factor = arr_score[49-index_score_added]
            index_score_added += 1
            scorecapture = pygame.image.load('images/score_added.png')
            scorecapture = pygame.transform.rotozoom(scorecapture, 0, 0.4)
            scorecapture = pygame.transform.rotozoom(scorecapture, 0, factor)
            scorecapture_rect = scorecapture.get_rect(center = (450, 600))
            pygame.draw.rect(surface, 'white', scorecapture_rect)
            surface.blit(scorecapture, scorecapture_rect)

        # if a time booster is collected, a message showing 5 seconds added is displayed
        if (time.time()-ttimecapture)<0.5:
            arr_time = []
            for k in range(50):
                arr_time.append(1-k*0.9/50)
            factor = arr_time[49-index_time_added]
            index_time_added += 1
            timecapture = pygame.image.load('images/time_added.png')
            timecapture = pygame.transform.rotozoom(timecapture, 0, 0.4)
            timecapture = pygame.transform.rotozoom(timecapture, 0, factor)
            timecapture_rect = timecapture.get_rect(center = (150, 600))
            pygame.draw.rect(surface, 'white', timecapture_rect)
            surface.blit(timecapture, timecapture_rect)

        # lives displayed on the screen
        for j in range(lives):
            life_rect = life.get_rect(center = (RES[0]-(j+1)*TILE/2, TILE/2))
            surface.blit(life, life_rect)

        if life_lost:
            brokenheart_rect = brokenheart.get_rect(center = (RES[0]-(lives+1)*TILE/2, TILE/2))
            surface.blit(brokenheart, brokenheart_rect)

        # if lives become 0, the game is over
        if lives <= 0:
            game_active = False
            game_over = True
            won = False
            levels = False
            main_menu = False
            score = collected_score_boost * 500
            add_score(score)

    elif main_menu:
        # main menu page
        bg = pygame.image.load('images/MainMenu.png').convert_alpha()
        bg = pygame.transform.scale(bg,(RES[0], RES[1]+100))
        surface.blit(bg, (0,0))

    elif levels:
        # levels page
        levelspage = pygame.image.load('images/Levels.jpeg').convert_alpha()
        levelspage = pygame.transform.scale(levelspage, (RES[0], RES[1]+100))
        surface.blit(levelspage, (0,0))
        back = helvetica.render(f'Back to Menu',False,'black')
        back_rect = back.get_rect(center = (300,450))
        pygame.draw.rect(surface, 'white', back_rect)
        surface.blit(back,back_rect)

        # a white box is used to highlight the level chosen
        box = pygame.image.load('images/WhiteBox.png').convert_alpha()
        box = pygame.transform.scale(box,(300, 400))

        # encoding the levelchosen to highlight the box
        if levelchosen == 0:
            surface.blit(box, (-50,-10))
        elif levelchosen == 1:
            surface.blit(box, (150,-10))
        else:
            surface.blit(box, (350,-10))

    elif game_over:

        if won:
            # congratulations page
            congrats = pygame.image.load('images/Congrats.jpeg').convert_alpha()  #background image
            congrats = pygame.transform.scale(congrats, (RES[0], RES[1]+100))
            score_msg = helveticasmaller.render(f'SCORE: {score}', False, '#f8fdff')  # make score
            score_msg_rect = score_msg.get_rect(center = (300, 370))
            
            surface.blit(congrats, (0,0))
            bgrect = pygame.Rect(265, 355, 70, 25)
            pygame.draw.rect(surface, '#1c2534', bgrect)  
            surface.blit(score_msg, score_msg_rect)   #  show score on the screen

        else:
            lost = pygame.image.load('images/Skill Issue.jpeg').convert_alpha() # background image
            lost = pygame.transform.scale(lost, (RES[0], RES[1]+100))
            score_msg = helveticasmaller.render(f'SCORE: {score}', False, '#181818')  # make score
            score_msg_rect = score_msg.get_rect(center = (300, 360))
            
            surface.blit(lost, (0,0))
            bgrect = pygame.Rect(230, 345, 133, 25)
            pygame.draw.rect(surface, '#fcfcfc', bgrect)    
            surface.blit(score_msg, score_msg_rect)    # show score on the screen
    
    elif highscorespage:
        # highscores page
        hspg = pygame.image.load('images/highscorespage.png').convert_alpha()
        hspg = pygame.transform.scale(hspg, (RES[0], RES[1]+100))
        surface.blit(hspg, (0,0))
        blackbox = pygame.image.load('images/blackbox.png').convert_alpha()
        blackbox = pygame.transform.scale(blackbox, (150, 40))   # black box to highlight the scores
        scores = get_scores()
        l = len(scores)   # to handle cases when there are not enough scores
        if l >= 1:
            first = scores[0]
            first_score = helveticasmall.render(f'1. {first}', False, 'white')
            first_score_rect = first_score.get_rect(center = (300, 330))
            blackbox_rect = blackbox.get_rect(center = (300, 328))
            surface.blit(blackbox, blackbox_rect)
            surface.blit(first_score, first_score_rect)
        if l >= 2:
            second = scores[1]
            second_score = helveticasmall.render(f'2. {second}', False, 'white')
            second_score_rect = second_score.get_rect(center = (300, 360))
            blackbox_rect = blackbox_rect.move(0, 30)
            surface.blit(blackbox, blackbox_rect)
            surface.blit(second_score, second_score_rect)
        if l >= 3:
            third = scores[2]
            third_score = helveticasmall.render(f'3. {third}', False, 'white')
            third_score_rect = third_score.get_rect(center = (300, 390))
            blackbox_rect = blackbox_rect.move(0, 30)
            surface.blit(blackbox, blackbox_rect)
            surface.blit(third_score, third_score_rect)
        if l >= 4:
            fourth = scores[3]
            fourth_score = helveticasmall.render(f'4. {fourth}', False, 'white')
            fourth_score_rect = fourth_score.get_rect(center = (300, 420))
            blackbox_rect = blackbox_rect.move(0, 30)
            surface.blit(blackbox, blackbox_rect)
            surface.blit(fourth_score, fourth_score_rect)
        if l == 5:
            fifth = scores[4]
            fifth_score = helveticasmall.render(f'5. {fifth}', False, 'white')
            fifth_score_rect = fifth_score.get_rect(center = (300, 450))
            blackbox_rect = blackbox_rect.move(0, 30)
            surface.blit(blackbox, blackbox_rect)
            surface.blit(fifth_score, fifth_score_rect)
        
        # back to main menu button
        back = helvetica_medium.render(f'Main Menu',False,'black')
        back_rect = back.get_rect(center = (300,485))
        pygame.draw.rect(surface, 'white', back_rect)
        surface.blit(back,back_rect)
   
    pygame.display.flip()  # update the display
    clock.tick(FPS)   # FPS set to 60