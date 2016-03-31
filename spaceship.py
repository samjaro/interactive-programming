# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

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

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35, 10)
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
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.shooting = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        

        
    def draw(self,canvas):
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()
        else:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[0]],self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()

    def update(self):
        self.vel[0]*=0.98
        self.vel[1]*=0.98
        self.pos[0] += self.vel[0]
        self.pos[0]%=WIDTH
        self.pos[1] += self.vel[1]
        self.pos[1]%=HEIGHT
        self.angle += self.angle_vel
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * 0.2
            self.vel[1] += forward[1] * 0.2
            
        
    def turn_left(self):
        if self.angle_vel == 0:
            self.angle_vel =-0.1
        else:
            self.angle_vel = 0
    
    def turn_right(self):
        if self.angle_vel == 0:
            self.angle_vel =0.1
        else:
            self.angle_vel = 0        
        
    def thrust_on(self):
        if self.thrust == False:
            self.thrust = True
        else:
            self.thrust = False
            
    def shoot(self):
        global a_missile
        if self.shooting == False:
            self.shooting = True
            forward = angle_to_vector(self.angle)
            start_pos = self.pos[0]+self.radius*forward[0], self.pos[1]+self.radius*forward[1]
            start_vel = self.vel[0]+forward[0]*3,self.vel[1]+forward[1]*3
            a_missile = Sprite(start_pos,start_vel, 0, 0, missile_image, missile_info, missile_sound)
        else:
            self.shooting = False
    
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
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[0]%=WIDTH
        self.pos[1] += self.vel[1]
        self.pos[1]%=HEIGHT
        self.angle += self.angle_vel   
        
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw user interface
    canvas.draw_text('Lives:', (60, 70), 30, 'White')
    canvas.draw_text(str(lives), (90, 100), 30, 'White')
    canvas.draw_text('Score:', (WIDTH-120, 70), 30, 'White')
    canvas.draw_text(str(score), (WIDTH-90, 100), 30, 'White')

    
    
inputs = {'left':'turn_left', 'right':'turn_right', 'up': 'thrust', 'space':'shoot'}
    
def key(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn_left()
    if key == simplegui.KEY_MAP["right"]:
        my_ship.turn_right()   
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_on()
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    
         
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    a_rock = Sprite([random.random()*WIDTH,random.random()*HEIGHT],[random.choice([-1,-0.5, -0.2,-0.1, 0.1, 0.2, 0.5, 1]),random.choice([-2,-1.5, -1,-0.5,0.5, 1, 1.5,2])], 2, random.choice([-0.1, 0.1]) ,asteroid_image, asteroid_info)
    print 'angle', a_rock.angle
    print 'angle_vel', a_rock.angle_vel
    #(self, pos, vel, ang, ang_vel, image, info, sound = None):
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key)
frame.set_keyup_handler(key)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()