import pygame, time, random
from pygame.locals import *

class Game(): #Track scores, settings, players etc
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1314,753))
        pygame.display.set_caption('Snake?')
        self.colours = {
            'white' :   (255, 255, 255),
            'offwhite': (250, 250, 250),
            'black' :   (  0,   0,   0),
            'blue'  :   (  0,   0, 205),
            'red'   :   (255,   0,   0),
            'random':   (  0,   0,   0)
        }
        self.moves = {
            'l' : Position(-51,  0),
            'r' : Position( 51,  0),
            'u' : Position(  0,-51),
            'd' : Position(  0, 51)
        }
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.colours['offwhite'])
        self.one = None #player 1
        self.two = None #player 2
        self.game_type = 0
        self.snake_speed = 100 #Speed of game
        self.snake_speed_label = self.snake_speed
        self.food_move = 60
        self.score_top = 0
        self.score_bonus_time = 10
        self.score_bonus_points = 30
        self.pause = False #track if game is paused
        #bonus score reduces by 1 every second (must remember to stop reduction when paused)

    def manage_game(self):
        option = 0

        while option > -1:
            if option == 0: #Main Menu
                self.game_type = option = self.main_menu()
            elif option == 11: #Player 1 died
                self.game_type = option = self.game_over('p1')
            elif option == 12: #Player 2 dies
                self.game_type = option = self.game_over('p2')
            elif option == 13: #Draw
                self.game_type = option = self.game_over('d')
            else:
                option = self.play()
        
    def game_over(self,result):
        print("In game over - " + str(self.game_type))
        game_over = True
        pygame.mouse.set_visible(True)

        font_large = self.make_font('m')
        font_title = self.make_font('l')

        while game_over:
            #print("In game over - " + str(self.game_type))
            pygame.event.pump()
            self.screen.fill(self.colours['black'])

            button_main_menu = self.make_button(550,450,200,50,'Main Menu',font_large,self.colours['white'],self.colours['black'])
            button_replay = self.make_button(550,550,200,50,'Play Again',font_large,self.colours['white'],self.colours['black'])

            if self.game_type == 1 or self.game_type == 4: #1 Player Game or AI Test
                self.make_label(310,150,'Game Over',font_title,self.colours['white'])
                self.make_label(550,325,'Your score was: ' + str(self.one.score_current),font_large,self.colours['white'])
            else: #2 Player Game
                if result == 'p1':
                    message = 'Player 2 Wins'
                elif result == 'p2':
                    message = 'Player 1 Wins'
                else:
                    message = '    Draw!'
                self.make_label(270,150,message,font_title,self.colours['white'])
                self.make_label(370,325,'Player 1 score was: ' + str(self.one.score_current),font_large,self.colours['white'])
                self.make_label(720,325,'Player 2 score was: ' + str(self.two.score_current),font_large,self.colours['white'])

            pygame.display.update()

            if self.check_click(button_main_menu):
                game_over = False
                return 0
            if self.check_click(button_replay):
                game_over = False
                return self.game_type


    def main_menu(self):
        pygame.mouse.set_visible(True)
        #Randomise colour in the menu - whenever menu is called there is a new random colour
        self.colours['random'] = (random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))

        game_type = 0
        pygame.mouse.set_visible(True)

        font_large = self.make_font('m')
        font_small = self.make_font('s')
        font_title = self.make_font('l')

        while game_type == 0:
            pygame.event.pump()

            self.screen.fill(self.colours['black'])

            button_single = self.make_button(50,50,200,50,'Single Player',font_large,self.colours['white'],self.colours['black'])
            button_two = self.make_button(50,150,200,50,'Player VS Player',font_large,self.colours['white'],self.colours['black'])
            button_ai = self.make_button(50,250,200,50,'Player VS AI',font_large,self.colours['white'],self.colours['black'])
            button_ai_test = self.make_button(50,550,200,50,'Test AI',font_large,self.colours['white'],self.colours['black'])
            button_quit = self.make_button(50,350,200,50,'Quit Game',font_large,self.colours['white'],self.colours['black'])

            button_speed_up = self.make_button(300,50,75,50,'Speed +',font_small,self.colours['white'],self.colours['black'])
            self.make_button(312,111,50,28,str(self.snake_speed_label)+'%',font_small,self.colours['white'],self.colours['black'])
            button_speed_down = self.make_button(300,150,75,50,'Speed -',font_small,self.colours['white'],self.colours['black'])

            button_delay_up = self.make_button(300,250,75,50,'Time +',font_small,self.colours['white'],self.colours['black'])
            self.make_button(322,311,30,28,str(self.food_move),font_small,self.colours['white'],self.colours['black'])
            button_delay_down = self.make_button(300,350,75,50,'Time -',font_small,self.colours['white'],self.colours['black'])

            self.make_label(787,553,'Snake',font_title,self.colours['white'])
            self.make_label(800,700,'Highest SP score during this session: ' + str(self.score_top),font_large,self.colours['white'])

            if self.check_click(button_single):
                game_type = 1
                #print('Game Type 1')
            elif self.check_click(button_two):
                game_type = 2
                #print('Game Type 2')
            elif self.check_click(button_ai):
                game_type = 3
                #print('Game Type 3')
            elif self.check_click(button_quit):
                game_type = -1 #quit
            elif self.check_click(button_speed_up):
                self.increase_speed()
                #print('Increase speed')
            elif self.check_click(button_speed_down):
                self.decrease_speed()
                #print('Decrease speed')
            elif self.check_click(button_delay_up):
                self.increase_time()
               # print('Increase time bonus')
            elif self.check_click(button_delay_down):
                self.decrease_time()
                #print('Decrease time bonus')
            elif self.check_click(button_ai_test):
                game_type = 4
                #print('Game Type 4 - Test AI')

            pygame.display.update()

        return game_type

    def make_font(self,size = 's'):
        if size == 'l':
            return pygame.font.SysFont("bitstreamverasans", 150)
        elif size == 'm':
            return pygame.font.SysFont("bitstreamverasans", 20)
        else:
            return pygame.font.SysFont("bitstreamverasans", 15)

    def increase_speed(self):
        if self.snake_speed < 200:
            self.snake_speed -= 1
            self.snake_speed_label += 1
            if self.score_bonus_points >= 30:
                self.score_bonus_points += 2
            if self.score_bonus_points < 30:
                self.score_bonus_points += 1
            time.sleep(0.1)

    def decrease_speed(self):
        if self.snake_speed > 0:
            self.snake_speed += 1
            self.snake_speed_label -= 1
            if self.score_bonus_points <= 30:
                self.score_bonus_points -= 1
            if self.score_bonus_points > 30:
                self.score_bonus_points -= 2
            time.sleep(0.1)

    def increase_time(self):
        if self.food_move < 999:
            self.food_move += 1
            time.sleep(0.1)

    def decrease_time(self):
        if self.food_move > -1:
            self.food_move -= 1
            time.sleep(0.1)

    def make_button(self,x,y,h,w,text,font,colour_button,colour_text):
        button = pygame.draw.rect(self.screen, colour_button, (x, y, h, w))
        self.make_label(x+5,y+5,text,font,colour_text)
        return button

    def make_label(self,x,y,text,font,colour):
        label = font.render(text,1,colour)
        self.screen.blit(label, (x,y))

    def check_click(self, button):
        if button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def play(self):
        if self.game_type == -1:
            self.quit()

        game_over = '' #'' if not over, 'p1' is p1 dies, 'p2' if p2 dies, 'd' if draw
        keep_playing = True
        game_time = int(time.perf_counter())
        pygame.mouse.set_visible(False)

        if self.game_type == 1: #if one player game then random colour
            self.one = Human(self.screen,self.moves,1,'h',self.colours['random'])
        elif self.game_type == 4: #test ai on its own
            self.one = AI(self.screen,self.moves,1,'a',self.colours['random'])
        else: #more than 1 player so colour must be blue
            self.one = Human(self.screen,self.moves,1,'h',self.colours['blue'])

        if self.game_type == 2:
            self.two = Human(self.screen,self.moves,2,'h',self.colours['red'])
        
        elif self.game_type == 3:
            self.two = AI(self.screen,self.moves,2,'a',self.colours['red'])

        food = Food(self.screen, self.colours['random'])
        self.score_bonus_time = self.food_move

        counters = {} #dictionary of counters to track per time span
        #item:[start,reset,decrement per second,current value of counter,take action]
        counters['food'] = [self.food_move,0,1,0,True]

        while keep_playing: #game loop
            game_time, second_passed = self.count_second(game_time)
            food_eaten = False

            #Display actions
            self.screen.blit(self.background, (0, 0))
            self.print_border()
            food.draw_food()

            if second_passed:
                self.change_bonus() #update the bonus points counter

            #Players actions
            players = [] #generate list for printing game info
            players.append([self.one.player,self.one.score_current])
            self.one.draw_snake()

            if self.game_type == 2 or self.game_type == 3: #if 2 snakes
                players.append([self.two.player,self.two.score_current])

                self.two.draw_snake()
                if self.two.blocks[0].rect.colliderect(self.one.blocks[0]):
                    game_over = 'draw'
                    
                snakes = {'p1':self.one.blocks, 'p2':self.two.blocks}
                if len(self.two.blocks)>=len(self.one.blocks):
                    current_longest='p2'
                    shortest = 'p1'

                elif len(self.two.blocks)<len(self.one.blocks):
                    current_longest='p1'
                    shortest = 'p2'

                for d in range(len(snakes[current_longest])-1,-1,-1):
                    if snakes[current_longest][d].rect.colliderect(snakes[shortest][0]) and d!= 0:
                        game_over = current_longest
                    if snakes[shortest][0].rect.colliderect(snakes[current_longest][d]) and d!= 0:
                        game_over = shortest

                if self.two.check_eat_food(food,self.score_bonus_points):
                    food_eaten = True
                    self.two.grow_snake()

            if self.one.check_eat_food(food,self.score_bonus_points):
                food_eaten = True
                self.one.grow_snake()

            self.print_game_info(players)

            #User Controls
            events = self.manage_events()

            for event in events:
                if event == 'p': #Pause game
                    event = self.pause_game()
                if event == 'q' or event == 'm': #Stop playing game
                    keep_playing = False
                    break

                if self.validate_move(event):
                    #print('Move Key')
                    player,move = self.process_key(event)
                    if player == 1:
                        #print('MOVE: Player 1 Move: ' + move)
                        self.one.set_direction(move)
                    if self.game_type > 1 and player == 2:
                        if self.two.type == 'h': #Human player 2
                            #print('Player 2 Move: ' + move)
                            self.two.set_direction(move)
                        else: #AI player 2
                            self.two.set_direction(food) #pass food to AI
                    """
                    if game_type == 1 and player == 2:
                        print('Cannot make that move')
                    """
                
            #Food actions
            if self.score_bonus_time == 0:
                if self.game_type == 1:
                    game_over = 'p1'
                elif self.game_type==4:
                    game_over='p1'
                else:
                    if self.one.score_current > self.two.score_current:
                        game_over = 'p2'
                    elif self.one.score_current < self.two.score_current:
                        game_over = 'p1'
            if food_eaten: #Check if food has been eaten by a player
                food.move_food()
                food.draw_food()
                
            #if not food_eaten:

            if self.one.type == 'a': #AI player
                self.one.set_direction(food, None)
            #Move player(s)
            self.one.move_snake()
            if self.game_type == 3: #2 player AI game
                self.two.set_direction(food,self.one.blocks)
                #self.two.move_snake()
            
            if self.one.check_collision_screen_boundaries():
                #Game Over - self.one at edge of screen
                game_over = 'p1'
                print('Game Over - Collide with boundaries')
            if self.one.check_collision_with_self():
                #Game over - p1 hit itself
                game_over = 'p1'
                print('Game Over - Collide with self')
            if self.game_type == 2 or self.game_type == 3: #2 player game
                self.two.move_snake()
                if self.two.check_collision_screen_boundaries():
                    #Game Over - p2 at edge of screen
                    game_over = 'p2'
                if self.two.check_collision_with_self():
                    game_over = 'p2'

            pygame.display.update()
            self.clock.tick(self.fps)
            pygame.time.delay(self.snake_speed)

            if not game_over == '': #Game is over so end game loop
                keep_playing = False

        if not game_over == '':
            if game_over == 'p1': #p1 died
                print('Play Game - P1 Died')
                if self.game_type == 2 or self.game_type == 3:
                    if self.score_top < self.two.score_current:
                        self.score_top = self.two.score_current
                else:
                    if self.score_top < self.one.score_current:
                        self.score_top = self.one.score_current
                return 11
            elif game_over == 'p2': #p2 died
                print('Play Game - P2 Died')
                if self.score_top < self.one.score_current:
                    self.score_top = self.one.score_current
                return 12
            elif game_over=='draw': #draw
                print('Play Game - Draw')
                if self.one.score_current > self.two.score_current:
                    if self.score_top < self.one.score_current:
                        self.score_top = self.one.score_current
                else:
                    if self.score_top < self.two.score_current:
                        self.score_top = self.two.score_current
                return 13
        else:
            return 0 #Tell manage_game() to load main menu

    def validate_move(self,key):
        if key in ['1l','1r','1u','1d','2l','2r','2u','2d']:
            return True
        return False

    def process_key(self,key):
        player = int(key[0:1])
        move = key[1:]

        return player, move

    def count_second(self,game_time):
        if int(time.perf_counter()) == game_time:
            game_time += 1
            return game_time, True #returns time and flag that says time has changed
        return game_time, False #returns time and flag that says time hasn't changed

    def change_bonus(self):
        if self.score_bonus_time > 0:
            self.score_bonus_time -= 1 #subtract 1 from bonus score

    def manage_events(self):
        """
        Possible outputs: q - quit, p - pause, m - main menu, 1l - player 1 left, 1r - p1 right, 1u - p1 up,
        1d - p1 down, 2l - player 2 - left, 2r - p2 right, 2u - p2 up, 2d - p2 down
        """
        pressed_keys = []
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pressed_keys.append('q')

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pressed_keys.append('q')

                if event.key == K_p:
                    pressed_keys.append('p')
        
                if event.key == K_m:
                    pressed_keys.append('m')

            if pressed_keys: return pressed_keys

        keys = pygame.key.get_pressed()
                
        if keys[pygame.K_d]:
            pressed_keys.append('1r')
        
        if keys[pygame.K_a]:
            pressed_keys.append('1l')
        
        if keys[pygame.K_s]:
            pressed_keys.append('1d')

        if keys[pygame.K_w]:
            pressed_keys.append('1u')
        
        if keys[pygame.K_RIGHT]:
            pressed_keys.append('2r')

        if keys[pygame.K_LEFT]:
            pressed_keys.append('2l')
        
        if keys[pygame.K_DOWN]:
            pressed_keys.append('2d')

        if keys[pygame.K_UP]:
            pressed_keys.append('2u')
        
        return pressed_keys

    def pause_game(self):
        self.pause = True
        pause_font = self.make_font('m')
        self.make_label(450,350,'Game Paused - Press P to resume the game',pause_font,self.colours['red'])
        pygame.display.update()
        pygame.mouse.set_visible(True)
        while self.pause: #Pause game
            pygame.mouse.set_visible(True)
            events = self.manage_events()
            if 'p' in events: #If pressed p then unpause
                self.pause = False
            print('Pause Game')
        pygame.mouse.set_visible(True)

    def quit(self):
        print('Quit')
        pygame.quit()

    def print_border(self):
        pygame.draw.line(self.screen, self.colours['black'], (0, 9), (1360, 9), 20)
        pygame.draw.line(self.screen, self.colours['black'], (0, 742), (1360, 742), 20)
        pygame.draw.line(self.screen, self.colours['black'], (9, 0), (9, 770), 20)
        pygame.draw.line(self.screen, self.colours['black'], (1303, 0), (1303, 760), 20)

    def print_game_info(self,players): #player is a list of players - player number + score e.g. [[1,4],[2,6]]
        font_small = self.make_font('s')
        x = 150
        for p in players:
            self.make_label(x, 1, 'Player ' + str(p[0]) + ' Score: ' + str(p[1]), font_small, self.colours['white'])
            x += 150
        self.make_label(610, 1, 'Time Left: ' + str(self.score_bonus_time), font_small, self.colours['white'])
        self.make_label(1050, 1, 'Press P to pause', font_small, self.colours['white'])
        self.make_label(1050, 735, 'Press M for the menu', font_small, self.colours['white'])

class Position:
    def __init__(self, x=20, y=20):
        self.x = x
        self.y = y

class Snake():
    def __init__(self,screen,moves,player,type,colour):
        self.blocks = []
        self.player = player #1 vs 2
        self.type = type #Human vs AI
        self.score_current = 0 #store the current score
        self.score_old = 0 #store the player's previous score
        self.direction = ''
        self.old_direction = ''
        self.colour = colour
        self.screen = screen
        self.moves = moves
        self.grown = False
        self.setup_snake()

    def setup_snake(self):
        if self.player == 1:
            self.blocks.append(Block(122,20,True))
            self.blocks.append(Block(71,20,False))
            self.blocks.append(Block(20,20,False))
            self.direction = 'r' #Start moving right
        else:            
            self.blocks.append(Block(1091,683,True))
            self.blocks.append(Block(1142,683,False))
            self.blocks.append(Block(1193,683,False))
            self.direction = 'l' #Start moving left

    def grow_snake(self):
        last_position = self.blocks[len(self.blocks)-1].old
        self.blocks.append(Block(last_position.x,last_position.y,False))
        #self.blocks[len(self.blocks)-1].draw_block(self.screen, self.colour, 50, 50)
        self.grown = True

    def draw_snake(self):
        for segment in self.blocks:
            segment.draw_block(self.screen, self.colour, 50, 50)

    def set_direction(self,move):
        if move in self.moves:
            #Make sure snake doesn't move back on itself
            if (self.direction != 'l' and move == 'r') or \
                (self.direction != 'r' and move == 'l') or \
                (self.direction != 'u' and move == 'd') or \
                (self.direction != 'd' and move == 'u'):
                self.old_direction = self.direction
                self.direction = move
                print("MOVE: Player " + str(self.player) + " - Direction Made: " + self.direction)

    def check_eat_food(self,food,score_modifier):
        if self.blocks[0].check_overlap(food.block):
            #print('FOOD EATEN: Snake head has collided with food')
            self.score_current += score_modifier
            return True
        return False

    def update_head_position(self):
        modifier = Position(self.moves[self.direction].x,self.moves[self.direction].y)
        #print('    MOVE HEAD: Direction X ' + str(modifier.x) + ' Y ' + str(modifier.y))
        modifier.x += self.blocks[0].current.x
        modifier.y += self.blocks[0].current.y
        #print('    MOVE HEAD: Old X ' + str(self.blocks[0].current.x) + ' Y ' + str(self.blocks[0].current.y))
        #print('    MOVE HEAD: New X ' + str(modifier.x) + ' Y ' + str(modifier.y))
        self.blocks[0] = self.update_position(self.blocks[0],modifier)

    def update_position(self,block,new_position):
        #print('    MOVE BLOCK: Old Before Change X ' + str(block.old.x) + ' Y ' + str(block.old.y))
        block.old.x = block.current.x
        block.old.y = block.current.y
        #print('    MOVE BLOCK: Old After Change X ' + str(block.old.x) + ' Y ' + str(block.old.y))
        block.current.x = new_position.x
        block.current.y = new_position.y
        #print('    MOVE BLOCK: New After Change X ' + str(block.current.x) + ' Y ' + str(block.current.y))
        return block

    def move_snake(self):
        #change head position
        self.update_head_position()

        #change segment positions
        self.change_segment_positions()

    def check_collision_with_self(self):
        for i in range(1,len(self.blocks)):
            #print('Block ' + str(i))
            if (self.grown and i == len(self.blocks)-1): #if just added new block then don't check (rect not exist yet)
                self.grown = False #reset grown flag
            else:
                if self.blocks[0].check_overlap(self.blocks[i]):
                    print("Collided with self")
                    return True
        return False

    def check_collision_screen_boundaries(self):
        if self.blocks[0].current.x < 0 or self.blocks[0].current.x > 1275 or \
            self.blocks[0].current.y < 0 or self.blocks[0].current.y > 714:
            print('Collided with edge')
            return True
        return False

    def change_segment_positions(self):
        for i in range(1,len(self.blocks)):
            #print('Block ' + str(i))
            self.blocks[i] = self.update_position(self.blocks[i],self.blocks[i-1].old)

class Human(Snake):
    def __init__(self,screen,moves,player,type,colour):
        Snake.__init__(self,screen,moves,player,type,colour)

class AI(Snake):
    def __init__(self,screen,moves,player,type,colour):
        Snake.__init__(self,screen,moves,player,type,colour)

    def set_direction(self,food,other_snake):
        path = self.generate_path(food,other_snake)
        if len(path) > 0:
            self.old_direction = self.direction
            self.direction = path[0][1]

    #Find distance to the snake
    def find_distance_to_food(self,food,position):
        difference = Position(0,0)
        difference.x = food.block.current.x - position.x #negative - go left; positive - go right
        difference.y = food.block.current.y - position.y #negative - go up; positive - go down            

        return difference

    #Decide the next direction to move
    #Direction scoring
    def decide_next_direction(self, difference):
        directions = [
            ['d',0],
            ['u',0],
            ['l',0],
            ['r',0]
        ]

        if difference.x > 0:
            directions[3][1] += 1 #r
        elif difference.x < 0:
            directions[2][1] += 1 #l

        if difference.y > 0:
            directions[0][1] += 1 #d
        elif difference.y < 0:
            directions[1][1] += 1 #u

        pos_x = abs(difference.x) #convert all numbers to positive
        pos_y = abs(difference.y) #convert all numbers to positive

        if pos_x > pos_y:
            if difference.x < 0:
                directions[2][1] += 2 #l
            else:
                directions[3][1] += 2 #r
        elif pos_x < pos_y:
            if difference.y > 0:
                directions[0][1] += 2 #d
            else:
                directions[1][1] += 2 #u

        directions = sorted(directions, key=lambda x: x[1], reverse=True)

        return directions


    #Generate a path from snake head to food
    def check_against_snake(self,next_x,next_y):
        print("\n    Check Against Snake")
        counter = 0
        for segment in self.blocks:
            print("            Segment " + str(counter) + " X:", self.coord_to_index(segment.current.x), "Segment Y:", self.coord_to_index(segment.current.y),"Next X", self.coord_to_index(next_x),"Next Y", self.coord_to_index(next_y))
            if (segment.current.x==next_x and segment.current.y== next_y):
                print('   Same location as segment/element ' + str(counter))

                return False
            counter+=1

        return True


    #Generate a path from snake head to food
    def check_against_enemy(self,next_x,next_y,other_snake):
        print("\n    Check Against enemy")
        counter = 0
        for segment in other_snake:
            print("            Segment " + str(counter) + " X:", self.coord_to_index(segment.current.x), "Segment Y:", self.coord_to_index(segment.current.y),"Next X", self.coord_to_index(next_x),"Next Y", self.coord_to_index(next_y))
            if (segment.current.x==next_x and segment.current.y== next_y):
                print('   Same location as segment/element ' + str(counter))

                return False
            counter+=1

        return True
    def check_against_path(self, path, new_pos):
        for pos in path:
            if pos[0].x == new_pos.x and pos[0].y == new_pos.y:
                return False #collision detected so return False (Fail)
        return True #no collision so return True

    def check_edge(self, pos):
        if (pos.x < 0 or pos.x >= 1275 or \
                     pos.y < 0 or pos.y > 714):
            return False
        return True

    def check_direction(self, new, old):
        if old == 'l' and new == 'r':
            print('    CHK Direction - FAIL - NEW DIR r')
            return False
        elif old == 'r' and new == 'l':
            print('    CHK Direction - FAIL - NEW DIR l')
            return False
        elif old == 'u' and new == 'd':
            print('    CHK Direction - FAIL - NEW DIR d')
            return False
        elif old == 'd' and new == 'u':
            print('    CHK Direction - FAIL - NEW DIR u')
            return False
        print('    CHK Direction - PASS - NEW DIR ' + new)

        return True

    def coord_to_index(self,coord):
        index = 0
        index = (coord-20)/51
        return str(index) + " (" + str(coord) + ")"

    def generate_path(self, food, other_snake):
        #Needs to check against the other snake
        path = []
        directions = []
        current_position = Position(self.blocks[0].current.x,self.blocks[0].current.y)
        current_direction = self.direction
        old_direction = None

        counter = 1

        print("\nFOOD X - ", self.coord_to_index(food.block.current.x), " Y - ", self.coord_to_index(food.block.current.y) + '\n')

        force_end = False #used to force loop to end if needed
        while not self.check_path(current_position.x, current_position.y, food.block.rect) and not force_end:
            print('Path Move No. ' + str(counter))
            distance = self.find_distance_to_food(food,current_position) # get distance
            directions = self.decide_next_direction(distance)

            dir_counter = 0
            chosen_direction = False
            while dir_counter < 4 and not chosen_direction:
                test_direction = directions[dir_counter][0]
                print('CHECK DIRECTION ' + test_direction)
                chosen_direction = True
                modifier = None
                test_pos = None
                modifier = Position(self.moves[test_direction].x, self.moves[test_direction].y)
                test_pos = Position(current_position.x+modifier.x, current_position.y+modifier.y)

                if not self.check_direction(test_direction, old_direction): #check not going back
                    chosen_direction = False
                    print('    Failed Check Direction')

                if not self.check_against_snake(test_pos.x, test_pos.y): #Test new position against entire snake
                    chosen_direction = False
                    print('    Failed Check Against Snake')

                if not self.check_against_path(path,test_pos): #Test new position against existing path so far
                    chosen_direction = False
                    print('    Failed Check Against Path')

                if not self.check_edge(test_pos): #Test new position against screen boundaries
                    chosen_direction = False
                    print('    Failed Check Boundaries')
                
                if other_snake and not self.check_against_enemy(test_pos.x, test_pos.y,other_snake): #Test new position against screen boundaries
                    chosen_direction = False
                    print('    Failed Check enemy')

                if chosen_direction: #Valid direction
                    old_direction = current_direction
                    current_direction = test_direction
                    current_position.x += modifier.x
                    current_position.y += modifier.y
                    path.append([Position(current_position.x, current_position.y), current_direction])

                dir_counter += 1

            if not chosen_direction: #could not find a suitable pddddddath so use existing path
                modifier = Position(self.moves[current_direction].x, self.moves[current_direction].y)
                current_position.x += modifier.x
                current_position.y += modifier.y
                if not self.check_edge(Position(current_position.x, current_position.y)): #Test new position against screen boundaries
                    force_end = True
                    print('    Failed Check Boundaries')
                else: #if in boundaries then add to path
                    path.append([Position(current_position.x, current_position.y), current_direction])

            elif len(path) > 5:
                force_end = True

            print('\n    PATH:')
            for pos in path:
                print("         x-", self.coord_to_index(pos[0].x), "y-", self.coord_to_index(pos[0].y),"dir-",pos[1])
            print()

            counter += 1
        return path

    def check_path(self, x, y, rect):
            if (x > rect.left or x == rect.left) and (x < rect.right or x == rect.right) and (
                    y > rect.top or y == rect.top) and (y < rect.bottom or y == rect.bottom):  # improved
                print("AI FOUND FOOD")
                return True    

class Block():
    block_counter = 0

    def __init__(self, x, y, head = False):
        self.id = Block.block_counter  # added an id to each snake block
        Block.block_counter += 1  # add 1 to the block class counter
        self.current = Position(x, y)
        self.old = Position()
        self.is_head = head #True/False
        self.rect = None     

    def draw_block(self, screen, colour, w, h):
        # print(self.id) #draws the id each time the block is drawn
        self.rect = pygame.draw.rect(screen, colour, (self.current.x, self.current.y, w, h))

    def check_overlap(self, item):
        if hasattr(item, 'rect') and item.rect == None: #Create rect if does not exist
            item.rect = Rect(item.current.x, item.current.y, 50, 50)

        if self.rect.colliderect(item.rect):
            return True
        return False
        """
        for a, b in [(self.rect, item.rect)]:
            if ((self.check_points(a.left, a.top, b)) or
                    (self.check_points(a.left, a.bottom, b)) or
                    (self.check_points(a.right, a.top, b)) or
                    (self.check_points(a.right, a.bottom, b))):
                return True
        """

    def check_points(self, x, y, rect):
        if (x > rect.left or x == rect.left) and (x < rect.right or x == rect.right) and (
                y > rect.top or y == rect.top) and (y < rect.bottom or y == rect.bottom):  # improved
            return True

class Food():
    def __init__(self, screen, colour):
        self.score_modifier = 30
        self.screen = screen
        self.colour = colour
        x,y = self.random_position()
        self.block = Block(x, y)

    def draw_food(self):
        #print('FOOD X: ' + str(self.block.current.x) + '  Y: ' + str(self.block.current.y))
        self.block.draw_block(self.screen, self.colour, 50, 50)

    def eaten(self):
        self.move_food()
        return self.score_modifier

    def move_food(self):
        x, y = self.random_position()
        self.block.current.x = x
        self.block.current.y = y

    def random_position(self):
        x = random.randrange(20, 1275, 51)
        y = random.randrange(20, 714, 51)
        return x, y

if __name__ == "__main__":
    game = Game()
    game.manage_game()
    game.quit()
    
    
    # in check other, finds the direction but never moves to that place