# implementation of Spaceship - program template for RiceRocks
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random
# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
rock_group= set([])
missile_group=set([])
explosion_group= set([])
max_rocks=10
main=True
controls,help_1,credits=False,False,False
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius
    def get_lifespan(self):
        return self.lifespan
    def get_animated(self):
        return self.animated

# debris images    
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")
# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")
''' Extra images'''
back_image=simplegui.load_image("https://cdn2.iconfinder.com/data/icons/crystalproject/crystal_project_256x256/apps/restart-1.png")
up_arrow_image= simplegui.load_image("http://www.wpclipart.com/computer/keyboard_keys/arrow_keys/computer_key_Arrow_Up.png")
right_arrow_image= simplegui.load_image("http://www.wpclipart.com/computer/keyboard_keys/arrow_keys/computer_key_Arrow_Right.png")
left_arrow_image= simplegui.load_image("http://www.wpclipart.com/computer/keyboard_keys/arrow_keys/computer_key_Arrow_Left.png")
#559x527 pixels
multi_arrow_image=simplegui.load_image("http://cdn.mysitemyway.com/etc-mysitemyway/icons/legacy-previews/icons-256/glossy-black-icons-arrows/008061-glossy-black-icon-arrows-two-directions-left-right1.png")
#256x256 pixels
spacebar_image= simplegui.load_image("http://www.learnmyway.com/sites/default/files/courses/justyourtype/images/key_space_bar_small.png")
#323x108 pixels

# helper functions to handle position between objects
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]
def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# helper functions to handle collisions
def process_sprite_group(canvas, sprite_group):
    global missile_group, explosion_group
    working_sprite_group = set(sprite_group)
    for item in working_sprite_group:        
        if item.update() == True:            
            sprite_group.remove(item)
        item.draw(canvas)
def group_group_collide(group_1,group_2):
    global score,explosion_group
    helper_group_1= set(group_1)
    helper_group_2= set(group_2)
    for item in helper_group_1:
        for element in helper_group_2:
            if item.collide(element):
                group_1.remove(item)
                group_2.remove(element)
                explosion_group.add(Sprite(item.pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
                score+=1    
def group_object_collide(group,other_object):
    global explosion_group
    helper_group= set(group)
    for item in helper_group:
        if item.collide(other_object):
            group.remove(item)
            explosion_group.add(Sprite(item.pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))  
            return True  
    

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
        self.vel[0] *= .99
        self.vel[1] *= .99
    def reset(self):
        self.vel = [0, 0]
        self.pos = [WIDTH / 2, HEIGHT / 2]
        self.angle = 0        
        self.angle_vel = 0
        self.thrust = False        
        self.update()
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    def increment_angle_vel(self):
        self.angle_vel += .05
    def decrement_angle_vel(self):
        self.angle_vel -= .05
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    def draw(self, canvas):
        if self.animated == True:
            global time
            x_coord = (self.age % 24 * self.image_size[0]) + self.image_center[0] ##24 frames
            image_center = [x_coord, self.image_center[1]] 
            time += 1            
        else:
            image_center = self.image_center
        canvas.draw_image(self.image, image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
    def position(self):
        return self.pos
    def radius(self):
        return self.radius
    def collide(self,other_object):
        other_object_pos= other_object.pos
        other_object_radius= other_object.radius
        distance= dist(self.pos,other_object_pos)
        if distance<=(self.radius+other_object_radius):
            return True
        else: return False            
    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        #Increment age of missile
        self.age+=1
        if str(self.lifespan) != "inf" and self.age > missile_info.lifespan:
            return True
        else: return False
  
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started,score,lives,controls,help_1,credits,main
    if controls and pos[0]>70 and pos[0]<90 and pos[1]>510 and pos[1]<590:
        controls= False
        main=True
    if help_1 and pos[0]>70 and pos[0]<90 and pos[1]>510 and pos[1]<590:
        help_1= False
        main=True
    if credits and pos[0]>70 and pos[0]<90 and pos[1]>510 and pos[1]<590:
        credits= False
        main=True
    score,lives=0,3
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started)and (not credits) and (not help_1) and (not controls) and inwidth and inheight:
        started = True
    if (not started) and pos[0]>100 and pos[0]<280 and pos[1]>510 and pos[1]<550:
        controls=True
        main=False
    if (not started) and pos[0]>370 and pos[0]<460 and pos[1]>510 and pos[1]<550:
                help_1=True
                main=False
    if (not started) and pos[0]>550 and pos[0]<693 and pos[1]>510 and pos[1]<550:
                credits=True
                main=False
        
#Draw handler
def draw(canvas):
    global time, started, lives
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives"+ " : "+ str(lives), [50, 50], 22, "White")
    canvas.draw_text("Score" + " : "+str(score), [680, 50], 22, "White")
    
    
    process_sprite_group(canvas,rock_group)
    process_sprite_group(canvas,missile_group)
    process_sprite_group(canvas,explosion_group)
    group_group_collide(rock_group,missile_group)
    my_ship.draw(canvas)
    my_ship.update()
    
    
    
    if group_object_collide(rock_group,my_ship):
        lives-=1
    if lives==0:
        started=False
        soundtrack.rewind()
    # draw splash screen if not started
    if not started:
        if main==True:
            canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
            canvas.draw_polygon([(100,510),(280,510),(280,550),(100,550)],12,"Black","Red")
            canvas.draw_text("CONTROLS",(110,540),30,"White")
            canvas.draw_polygon([(370,510),(460,510),(460,550),(370,550)],12,"Black","Red")
            
            canvas.draw_text("HELP",(380,540),30,"White")
            canvas.draw_polygon([(550,510),(693,510),(693,550),(550,550)],12,"Black","Red")
            canvas.draw_text("CREDITS",(560,540),30,"White")
        else:
            if controls:
                canvas.draw_polygon([(100,100),(675,100),(675,500),(100,500)],12,"Black","Red")
                canvas.draw_text("CONTROLS",(300,150),40,"White")
                canvas.draw_image(back_image,(256/2,256/2),(256,256),(80,550),(40,40))
                canvas.draw_image(up_arrow_image,(559/2,527/2),(559,527),(150,220),(60,55))
                canvas.draw_image(left_arrow_image,(559/2,527/2),(559,527),(150,300),(60,55))
                canvas.draw_image(right_arrow_image,(559/2,527/2),(559,527),(150,370),(60,55))
                canvas.draw_image(spacebar_image,(323/2,108/2),(323,108),(170,450),(120,55))
                canvas.draw_image(multi_arrow_image,(256/2,256/2),(256,256),(275,225),(200,100))
                canvas.draw_image(multi_arrow_image,(256/2,256/2),(256,256),(275,300),(200,100))
                canvas.draw_image(multi_arrow_image,(256/2,256/2),(256,256),(275,375),(200,100))
                canvas.draw_image(multi_arrow_image,(256/2,256/2),(256,256),(305,450),(200,100))
                canvas.draw_text("THRUST",(345,240),40,"Navy")
                canvas.draw_text("ROTATE LEFT",(345,315),40,"Navy")
                canvas.draw_text("ROTATE RIGHT",(345,390),40,"Navy")
                canvas.draw_text("SHOOT MISSILE",(375,465),40,"Navy")
                
            if help_1:
                canvas.draw_polygon([(175,100),(650,100),(650,500),(175,500)],12,"Black","Red")
                canvas.draw_text("HELP",(350,150),40,"White")
                canvas.draw_image(back_image,(256/2,256/2),(256,256),(80,550),(40,40))
                canvas.draw_text("Protect your Spaceship from",(200,200),35,"Black")
                canvas.draw_text("the raging Asteroids.",(200,240),35,"Black")
                canvas.draw_text("Your Spaceship will wrap",(200,280),35,"Black")
                canvas.draw_text("around the play area.",(200,320),35,"Black")
                canvas.draw_text("You get one point for Shooting",(200,360),35,"Black")
                canvas.draw_text("down one Asteroid.",(200,400),35,"Black")
                canvas.draw_text("The level of difficulty increases",(200,440),35,"Black")
                canvas.draw_text("as your Score increases.",(200,480),35,"Black")
                
            if credits:
                canvas.draw_polygon([(175,100),(700,100),(700,500),(175,500)],12,"Black","Red")
                canvas.draw_text("CREDITS",(350,150),40,"White")
                canvas.draw_image(back_image,(256/2,256/2),(256,256),(80,550),(40,40))
                canvas.draw_text("This game was made by Kishore",(200,200),35,"Black")
                canvas.draw_text("Vasan during the course of",(200,240),35,"Black")
                canvas.draw_text("Introduction to Python in Coursera",(200,280),35,"Black")
                canvas.draw_text("by Rice University.",(200,320),35,"Black")
                canvas.draw_text("The Art Assets have been created",(200,360),35,"Black")
                canvas.draw_text("by Kim Lathrop.",(200,400),35,"Black")
                canvas.draw_text("The credits for Simplegui goes",(200,440),35,"Black")
                canvas.draw_text("to Scott Rixner.",(200,480),35,"Black")

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group,max_rocks
    if started:
        if len(rock_group)<max_rocks:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
            rock_avel = random.random() * .2 - .1
            if score >= 10:
                rock_vel[0] *= 15
                rock_vel[1] *= 15
            elif score >= 30:
                rock_vel[0] *= 30
                rock_vel[1] *= 30
            rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))
        soundtrack.play()
    else:
        rock_group= set([])
        my_ship.reset()

def quit_game():
    global timer
    frame.stop()
    timer.stop()
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.add_button("Quit",quit_game,100)

timer = simplegui.create_timer(1000, rock_spawner)

# get things rolling
timer.start()
frame.start()
