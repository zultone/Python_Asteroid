from turtle import Turtle, Screen
import time
import random
import sys
screen = Screen()
screen.bgcolor("black")
screen.title("ASTEROIDS")
screen.bgpic("wallpaper.gif")



VELOCITY_X = 0
VELOCITY_Y = 0
BULLET_VELOCITY = 2
STEPS = .2
DELAY = .25
bulletList = []
bulletArray = {}
COUNT = 1
shapeList = ["circle","square","triangle"]
neg_pos_list = [-1,1]
asteroid_list = []
split_asteroid_list = []
fresh_split_asteroid_list = []

class Player():
    def __init__(self, score, lives, state):
        self.score = score
        self.lives = lives
        self.state = True
        self.restart = False
        self.game = True
        self.level = 1
        self.level_bonus = self.level * 10
        self.spawn_enemy_range = 1
        self.framerate = 1
        
class WriterTurtle(Turtle):
    def __init__(self,x,y):
        super().__init__(shape='square', visible=False)
        self.pu()
        self.color("white")
        self.style = ('Arial', 12, 'normal')
        self.goto(x,y)
        
        
class Spaceship(Turtle):
    def __init__(self, velocity_x,velocity_y):
        super().__init__(shape='triangle', visible=False)
        self.color("white","black")
        self.shapesize(2,3.8)
        self.pu()
        self.st()
        self.setheading(90)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.collision = True

    def move_spaceship(self):
        self.goto(self.xcor()+self.velocity_x,self.ycor()+self.velocity_y)

class Bullet(Turtle):
    def __init__(self,):
        super().__init__(shape='triangle', visible=False)
        self.color("white")
        self.shapesize(.3,1)
        self.pu()
        self.st()
        self.collision = True
        

class AsteroidObject(Turtle):
    def __init__(self):
        super().__init__(shape='square', visible=False)
        self.color("orange","black")
        self.pu()
        self.goto(random.randrange(-700,700),random.randrange(-375,375))
        self.shape(random.choice(shapeList))
        self.shapesize(random.uniform(1.0,4.0),random.uniform(1.0,4.0))
        self.shearfactor(random.uniform(.1,2.0))
        self.tilt_direction = random.choice(neg_pos_list)
        self.tilt_velocity = .1
        self.st()
        self.velocity_x = random.random()
        self.velocity_y = random.random()
        self.change_x = random.choice(neg_pos_list)
        self.change_y = random.choice(neg_pos_list)
        self.newVelocity_x = self.change_x*self.velocity_x
        self.newVelocity_y = self.change_y*self.velocity_y
        self.collision = True

    def move_asteroid(self):
        self.tilt(self.tilt_velocity * self.tilt_direction)
        self.goto(self.xcor()+self.newVelocity_x, self.ycor()+self.newVelocity_y)
        if self.xcor() > 800:
            self.ht()
            self.goto(-800, self.ycor())
            self.st()
        if self.xcor() < -800:
            self.ht()
            self.goto(800, self.ycor())
            self.st()
        if self.ycor() > 375:
            self.ht()
            self.goto(self.xcor(), -375)
            self.st()
        if self.ycor() < -375:
            self.ht()
            self.goto(self.xcor(), 375)
            self.st()
            
class SplitAsteroid(AsteroidObject):
    def __init__(self,velocity_x,velocity_y):
        super().__init__()
        self.color("orange","black")
        self.pu()
        self.shape(random.choice(shapeList))
        self.shapesize(1,2)
        self.shearfactor(1)
        self.tilt_direction = random.choice(neg_pos_list)
        self.tilt_velocity = .1
        self.st()
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.collision = True
        
    def move_asteroid(self):
        self.tilt(self.tilt_velocity * self.tilt_direction)
        self.goto(self.xcor()+self.velocity_x, self.ycor()+self.velocity_y)
        if self.xcor() > 800:
            self.ht()
            self.goto(-800, self.ycor())
            self.st()
        if self.xcor() < -800:
            self.ht()
            self.goto(800, self.ycor())
            self.st()
        if self.ycor() > 375:
            self.ht()
            self.goto(self.xcor(), -375)
            self.st()
        if self.ycor() < -375:
            self.ht()
            self.goto(self.xcor(), 375)
            self.st()            
            

def check_spaceship_collision():
    for asteroid in asteroid_list:
        if asteroid.collision:
            if spaceship.distance(asteroid.pos()) < 25:
                user.state = False
                user.lives -= 1
                for asteroids in asteroid_list:
                    time.sleep(.10)
                    asteroids.ht()
                for splits in split_asteroid_list:
                    time.sleep(.10)
                    splits.ht()
                    
                spaceship.ht()
                                                
                if user.lives < 0:
                    user.game = False
                if user.lives < 3:
                    life_3.ht()
                if user.lives < 2:
                    life_2.ht()
                if user.lives < 1:
                    life_1.ht()
                                
    for split in split_asteroid_list:
        if split.collision:
            if spaceship.distance(split.pos()) < 25:
                user.state = False
                user.lives -= 1
                for asteroids in asteroid_list:
                    time.sleep(.10)
                    asteroids.ht()
                for splits in split_asteroid_list:
                    time.sleep(.10)
                    splits.ht()
                    
                spaceship.ht()
                
                
                
                if user.lives <= 0:
                    user.game = False

                if user.lives < 3:
                    life_3.ht()
                if user.lives < 2:
                    life_2.ht()
                if user.lives < 1:
                    life_1.ht()
            

            
    
def check_bullet_collision():
    if len(bulletList) > 0:        
        for bullet in bulletList:
            if bullet.collision:
                if len(asteroid_list) > 0:
                    for asteroid in asteroid_list:
                        if bullet.distance(asteroid.pos()) < 25 and asteroid.collision == True:
                            user.score += 1
                            bullet.clear()
                            bullet.ht()
                            bullet.collision = False
                            bullet.goto(0,500)
                            if bullet in bulletList:
                                bulletList.remove(bullet)
                            fresh_split_asteroid_list.append(SplitAsteroid(asteroid.newVelocity_x,asteroid.newVelocity_y))
                        
                            fresh_split_asteroid_list.append(SplitAsteroid(asteroid.newVelocity_x*-1,asteroid.newVelocity_y))
                            split_asteroid_list.extend(fresh_split_asteroid_list)
                            # Make list specifically to loop through fresh split asteroids, then append them in a for loop
                            # To a new list, and remove them from fresh split asteroid list.
                            # Currently they are all looped through and all go to the position of the last turtle that was
                            # Collided with
                            
                            fresh_split_asteroid_list.clear()
                            asteroid.ht()
                            asteroid.clear()
                            asteroid.collision = False
                            asteroid.goto(0,500)
                            asteroid_list.remove(asteroid)
                            
                            
                if len(split_asteroid_list) > 0:       
                    for asteroids in split_asteroid_list:
                        if bullet.distance(asteroids.pos()) < 25:
                            user.score += 1
                            bullet.clear()
                            bullet.ht()
                            bullet.goto(0,500)
                            if bullet in bulletList:
                                bulletList.remove(bullet)
                            asteroids.ht()
                            asteroids.goto(0,500)
                            split_asteroid_list.remove(asteroids)
                           
                        
       
def move_bullets():
    if len(bulletList) > 0:
        for bullet_ in bulletList:
            bullet_.collision = True
            newVel = spaceship.velocity_x+spaceship.velocity_y
            
            if newVel < 0:
                newVel = newVel*(-1)
               
            bullet_.forward(BULLET_VELOCITY+newVel)
            if spaceship.distance(bullet_.pos()) > 500:
                bullet_.ht()
                if bullet_ in bulletList:
                    bulletList.remove(bullet_)
                
def move_asteroids():
    for asteroid in asteroid_list:
        asteroid.move_asteroid()
    for split_asteroid in split_asteroid_list:
        split_asteroid.move_asteroid()
            
def turn_r():
    spaceship.right(15)
def turn_l():
    spaceship.left(15)
def increase_x():
    spaceship.velocity_x += STEPS
def decrease_x():
    spaceship.velocity_x -= STEPS
def increase_y():
    spaceship.velocity_y += STEPS
def decrease_y():
    spaceship.velocity_y -= STEPS
def fire():
    global bulletList
    bulletList.append(Bullet())
    bulletList[-1].goto(spaceship.pos())
    bulletList[-1].setheading(spaceship.heading())
    bulletList[-1].collision = False
def quit_game():
    sys.exit("User terminated\n Thank you for playing!")


    
def next_level():
    if len(asteroid_list) == 0 and len(split_asteroid_list) == 0:
        user.spawn_enemy_range += 3
        user.level += 1
        user.score = user.score + user.level_bonus
        message_turtle.style = ('Arial', 20, 'normal')
        next_level_message = "Level: " + str(user.level) + "\nLevel bonus: " + str(user.level_bonus) + "\nSpawning " + str(user.spawn_enemy_range) + " enemies" 
        message_turtle.write(next_level_message, move = False, align='center', font = message_turtle.style)
        spaceship.ht()
        spaceship.goto(0,0)
        spaceship.setheading(90)
        spaceship.velocity_x = 0
        spaceship.velocity_y = 0
        level_keeper.clear()
        level_keeper.write("Level: " + str(user.level), move = False, align='center', font = score_keeper.style)
        time.sleep(3)
        message_turtle.clear()
        spaceship.st()
        for i in range(user.spawn_enemy_range):
            asteroid_list.append(AsteroidObject())
        


def restart_game_lives_left():
    if user.lives > 0:
        if asteroid_list:
            for a in asteroid_list:
                a.ht()
                a.goto(0,500)
        asteroid_list.clear()
        if bulletList:
            for a in bulletList:
                a.ht()
                a.goto(0,500)
        bulletList.clear()
        if split_asteroid_list:
            for a in split_asteroid_list:
                a.ht()
                a.goto(0,500)
        split_asteroid_list.clear()
        if fresh_split_asteroid_list:
            for a in fresh_split_asteroid_list:
                a.ht()
                a.goto(0,500)
        fresh_split_asteroid_list.clear()
        spaceship.goto(0,0)
        spaceship.setheading(90)
        spaceship.velocity_x = 0
        spaceship.velocity_y = 0
        message_turtle.style = ('Arial', 20, 'normal')
        restart_message = "Lives left: " + str(user.lives)
        message_turtle.write(restart_message, move = False, align='center', font = message_turtle.style)
        level_keeper.clear()
        level_keeper.write("Level: " + str(user.level), move = False, align='center', font = score_keeper.style)
        time.sleep(2)
        message_turtle.clear()
        spaceship.st()
        user.state = True
        
        for i in range(user.spawn_enemy_range):
            asteroid_list.append(AsteroidObject())
    

def restart_game_lost():
    if user.lives <= 0:
        if asteroid_list:
            for a in asteroid_list:
                a.ht()
                a.goto(0,500)
        asteroid_list.clear()
        if bulletList:
            for a in bulletList:
                a.ht()
                a.goto(0,500)
        bulletList.clear()
        if split_asteroid_list:
            for a in split_asteroid_list:
                a.ht()
                a.goto(0,500)
        split_asteroid_list.clear()
        if fresh_split_asteroid_list:
            for a in fresh_split_asteroid_list:
                a.ht()
                a.goto(0,500)
        fresh_split_asteroid_list.clear()
        spaceship.goto(0,0)
        spaceship.setheading(90)
        spaceship.velocity_x = 0
        spaceship.velocity_y = 0
        message_turtle.style = ('Arial', 20, 'normal')
        restart_message = "GAME LOST.... RESTARTING"
        message_turtle.write(restart_message, move = False, align='center', font = message_turtle.style)
        time.sleep(5)
        message_turtle.clear()
        user.state = True
        user.score = 0
        user.level = 1
        user.lives = 3
        level_keeper.clear()
        level_keeper.write("Level: " + str(user.level), move = False, align='center', font = score_keeper.style)
        life_1.st()
        life_2.st()
        life_3.st()
        spaceship.st()
        for i in range(user.spawn_enemy_range):
            asteroid_list.append(AsteroidObject())

    
    
user = Player(0,3,True)
screen.tracer(0)

spaceship = Spaceship(VELOCITY_X, VELOCITY_Y)
score_keeper = WriterTurtle(-500,-275)
level_keeper = WriterTurtle(-425,-275)
message_turtle = WriterTurtle(0,150)



life_1 = Spaceship(0,0)
life_1.collision = False
life_1.shapesize(1,1.9)
life_1.goto(-650,-275)
life_2 = Spaceship(0,0)
life_2.collision = False
life_2.shapesize(1,1.9)
life_2.goto(-625,-275)
life_3 = Spaceship(0,0)
life_3.collision = False
life_3.shapesize(1,1.9)
life_3.goto(-600,-275)

level_keeper.clear()
level_keeper.write("Level: " + str(user.level), move = False, align='center', font = score_keeper.style)

for i in range(user.spawn_enemy_range):
    asteroid_list.append(AsteroidObject())
    
while True:
    if user.state:
        spaceship.move_spaceship()
        move_bullets()
        check_bullet_collision()
        move_asteroids()
        check_spaceship_collision()
        next_level()
        score_keeper.clear()
        score_keeper.write("Score: " + str(user.score), move = False, align='center', font = score_keeper.style)
        if spaceship.xcor() > 800:
            spaceship.goto(-800, spaceship.ycor())
        if spaceship.xcor() < -800:
            spaceship.goto(800, spaceship.ycor())
        if spaceship.ycor() > 375:
            spaceship.goto(spaceship.xcor(), -375)                   
        if spaceship.ycor() < -375:
            spaceship.goto(spaceship.xcor(), 375)
    else:
        restart_game_lives_left()
        restart_game_lost()
        
    screen.onkey(quit_game, "Escape")
    screen.onkey(fire, "space")
    screen.onkey(turn_r, "w")
    screen.onkey(turn_l, "q")
    screen.onkey(increase_x, "Right")
    screen.onkey(decrease_x, "Left")
    screen.onkey(increase_y, "Up")
    screen.onkey(decrease_y, "Down")
    screen.listen()
    screen.update()

