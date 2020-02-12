import pygame
import random


#Fazli flappy bird V5
#Finally completed the game project. I've managed to create the starting page and ending page
#I wanted to add sound effect but can't seem to find any

# ---------------------------------------------------------------------- #





###INSTRUCTIONS
#PRESS THE SPACE BAR TO JUMP THE BIRD
#YOU MUST FLY THE BIRD IN BETWEEN THE PIPES
#IF THE BIRD HIT THE POLE OR THE GROUND, IT WILL DIE


# --------------------------------------------------------------------- #


#screen
DISPLAY = (600, 750)

#initialise pygame
pygame.init()
screen = pygame.display.set_mode(DISPLAY)

#caption
pygame.display.set_caption('Flappy Bird')


#font
font = pygame.font.Font(None, 100)
font2 = pygame.font.Font(None, 40)
font3 = pygame.font.Font(None, 80)

#colour
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
brown = (255, 179, 102)


#load image
bird_imgs_1 = [pygame.image.load('bird1.png'), pygame.image.load('bird2.png'), pygame.image.load('bird3.png')]
bird_imgs = []
for bird in bird_imgs_1:
    bird_imgs.append(pygame.transform.scale2x(bird))
    
    
pipe_img_1 = pygame.image.load('pipe.png')
pipe_img = pygame.transform.scale2x(pipe_img_1)

background = pygame.image.load('bg.png')
bg_img = pygame.transform.smoothscale(background, (600, 750))

base_img = pygame.image.load('base.png')



# -------------------------------------- #

class Bird:
    IMGS = bird_imgs
    #for looping bird wings flapping
    animation_time = 3

    #for rotating bird
    max_rotation = 25
    rotation_vel = 15

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = self.y       
        self.tilt = 0 #current angle of bird tilt
        self.tick_count = 0 #counter, acts like time // for calculatin displacement
        self.vel = 0 #vel of bird
        self.img_count = 0 #for animation of bird
        self.img = self.IMGS[0]  #for animation of bird
        

    def jump(self):
        self.vel = -10.5  #bird going up
        self.tick_count = 0
        self.height = self.y



    def move(self):
        self.tick_count += 1

        #displacement of bird i.e gravity
        #s = ut + 1/2at^2
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2
            
        #set max falling down speed
        if displacement >= 12:
            displacement = 12

        #make the jump be higher   
        if displacement < 0:
            pass
            #displacement -= 2

        #if bird hit the ground
        if self.y + self.img.get_height() >= 650:  #base.y
            displacement = 0   #bird stop
            
            
        self.y += displacement  #update current position of bird
            


        ### rotating/tilting the bird ###
        #if bird is jumping // tilt bird upwards
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt <= self.max_rotation:
                self.tilt = self.max_rotation  #tilt the bird upward immeadiately

        #if bird is falling
        else:
            if self.tilt > -90:  #if bird is not 90 deg
                self.tilt -= self.rotation_vel  #decrease angle until 90

                

    
    def show(self, screen):
        self.img_count += 1  #counter

        #looping through the pictures // bird flapping 

        #1  down
        if self.img_count < self.animation_time:
            self.img = self.IMGS[0]

        #2  rest
        elif self.img_count < self.animation_time * 2:
            self.img = self.IMGS[1]

        #3  up
        elif self.img_count < self.animation_time * 3:
            self.img = self.IMGS[2]

        #4  rest
        elif self.img_count < self.animation_time * 4:
            self.img = self.IMGS[1]

        #5  down
        elif self.img_count < self.animation_time * 4 + 1:
            self.img = self.IMGS[0]

            #reset counter // animation repeat
            self.img_count = 0


        #if bird is falling at 80 deg, stop flapping - rest 
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.animation_time * 2  #if bird jump when falling, continue animation from #2

        #tilt the bird about the centre
        tilt_bird = pygame.transform.rotate(self.img, self.tilt)
        new_rect = tilt_bird.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)  #bird tilting looks cleaner
        screen.blit(tilt_bird, new_rect.topleft)




# ---------------------------------------------- #

class Pipe:
    #dimension of pipe // 52 x 320
    
    vel = 8  #vel of pipe i.e how fast it moves across screen
    gap = 200 #gap between the pipes

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        #pipe images
        self.t_pipe = pygame.transform.flip(pipe_img, False, True)  #flip image vertically for top pipe
        self.b_pipe = pipe_img

        self.passed = False  #check if bird pass the pipe

        self.set_height()  #call function to set height of pipes (self.height)

    def set_height(self):
        self.height = random.randint(50, 400)  #height of pipe is random
        #y coordinate of images
        self.bottom = self.height + self.gap
        self.top = self.height - self.t_pipe.get_height()
        

    def move(self):
        self.x -= self.vel

    def show(self, screen):
        screen.blit(self.t_pipe, (self.x, self.top))
        screen.blit(self.b_pipe, (self.x, self.bottom))

    def collision(self, bird):
        if bird.x + bird.img.get_width() >= self.x and bird.x <= self.x + self.t_pipe.get_width():
            if bird.y <= self.bottom - self.gap or bird.y >= self.bottom:
                return True
                
            
            
             
    

# ----------------------------------------------------------- #


class Base:
    vel = 8  #same as pipe // need to be moving together
    img = base_img
    width = img.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        #there will be two pictures moving together back to back
        #when one of the picture is completely off the screen, it immeadiately joins back from behind
        #e.g leave the queue from the front and join it from behind
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
        
        
    def show(self, screen):
        screen.blit(self.img, (self.x1, self.y))
        screen.blit(self.img, (self.x2, self.y))

    def collision(self, bird):
        if bird.y + bird.img.get_height() >= self.y:
            return True


# ----------------------------------------------------------- #

score_his = []  #score history


# ------ main game ------#   

def draw_screen(screen, bird, pipes, base, score, instruction):
    screen.blit(bg_img, (0,0))  #display background

    for pipe in pipes:  #display pipe
        pipe.show(screen)
    
    bird.show(screen)  #display bird // dispaly after pipe so bird in front of pipe

    base.show(screen)  #display base

    #display text on screen
    text = font.render(str(score), True, white)
    screen.blit(text, (DISPLAY[0]//2 - text.get_width()//2, 75))

    text2 = font2.render(instruction, True, white)
    screen.blit(text2, (DISPLAY[0]//2 - text2.get_width()//2, 200))

    #display score
    if score == 'Game Over':

        text3 = font3.render('Score: ' + str(score_his[-1]), True, black)
        screen.blit(text3, (DISPLAY[0]//2 - text3.get_width()//2, 400))

        text4 = font3.render('Best: ' + str(max(score_his)), True, black)
        screen.blit(text4, (DISPLAY[0]//2 - text4.get_width()//2, 500))
                            
        
    pygame.display.update()  #update screen




def main():
    #current screen dimension // 600 x 750
    
    #initialise bird class
    #dimension of bird // 68 x 48
    bird = Bird(216, 375)
    #intialise pipe class // there will be multiple pipe so it is in a list
    pipes = [Pipe(600)]
    #initialise base class
    base = Base(650)
    

    clock = pygame.time.Clock()  #initilise clock
    counter = 0
    score = 0  #score of player // no of pipe brid pass
    instruction = ''
    game_start = False
    run = True
    done = False

    # ------ main while loop ----- # 
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_start = True
                    if run:  #if bird has colllided  with pole/hit floor, bird cannot jump
                        bird.jump()

                #restart game
                if event.key == pygame.K_r:
                    main()

        if not game_start:
            base.move()
            instruction = 'press [SPACE] to start'
        
        # ----------- GAME STARTED ----------- #                    

        if game_start:

            counter += 1

            instruction = ''

            
            bird.move()  #move the bird
            #print('y', bird.y)
            

            rem_pipe = []  #removed pipe will be in this list
            add_pipe = False
            

            #check if bird hit floor
            if base.collision(bird):
                #print('bird hit floor')
                run = False

                

            for pipe in pipes:

                #check if bird collide with pipe
                if pipe.collision(bird):
                    #print('COLLISION')
                    run = False
                    
                    
                #check if pipe is not in screen
                if pipe.x + pipe.t_pipe.get_width() < 0:   #if pipe is out of screen
                    rem_pipe.append(pipe)                  #remove pipe

                #check if bird pass the pipe
                if not pipe.passed and pipe.x + pipe.t_pipe.get_width() < bird.x:
                    pipe.passed = True
                    add_pipe = True  #can add another pipe

                #move pipe if bird never hit pole, else stop
                if run:
                    if counter >= 50:
                        pipe.move()

                    

            #move base if pipe is moving, else stop
            if run:
                base.move()  #move the base

        
                    
              

            #add pipe 
            if add_pipe == True:
                score += 1
                #print('score: ' + str(score))
                pipes.append(Pipe(600))

            #if pipe is removed, remove from pipes list
            for ele in rem_pipe:
                pipes.remove(ele)


            if not run:
                if type(score) == int:  #so that it only add the score and not 'Game Over'
                    score_his.append(score)
                #print('score history:', score_his)
                score = 'Game Over'
                instruction = 'press [R] to restart'
        
        
        #display images
        draw_screen(screen, bird, pipes, base, score, instruction)

        #FPS
        clock.tick(30)
        
    #out of game loop // quit
    pygame.display.quit()



if __name__ == '__main__':
    main()


