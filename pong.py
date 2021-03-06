# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]

score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel = [random.randrange(120.0/60.0, 240.0/60.0), random.randrange(-180.0/60.0, -60.0/60.0)]
    
    if direction == LEFT:
        ball_vel = [random.randrange(-240.0/60.0, -120.0/60.0), random.randrange(-180.0/60.0, -60.0/60.0)]
     
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)
    score1, score2 = 0, 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    #print ball_pos[0], ball_pos[1]
    
    # collide and reflect off of top of canvas
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # collide and reflect off of bottom of canvas
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
        
    # collide with left hand side gutter       
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] + BALL_RADIUS < paddle1_pos or ball_pos[1] - BALL_RADIUS > paddle1_pos + PAD_HEIGHT:
            spawn_ball(RIGHT)
            score2 += 1
        else:
            ball_vel[0] = - ball_vel[0] + 0.5#ball_vel[0]/100 *10
            ball_vel[1] = ball_vel[1] + 0.5#ball_vel[1]/100 *10
            print ball_vel[0]
            
            
    # collide with right hand side gutter or paddle   
    if ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
    #collide with gutter    
        if ball_pos[1] + BALL_RADIUS < paddle2_pos or ball_pos[1] - BALL_RADIUS > paddle2_pos + PAD_HEIGHT:
            spawn_ball(LEFT)    
            score1 += 1
    #collide with paddle        
        else:
            ball_vel[0] = - ball_vel[0] - 0.5
            ball_vel[1] = ball_vel[1] - 0.5
            print ball_vel[0]
        
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_vel[1] > 0 and paddle1_pos < HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel[1]
    elif paddle1_vel[1] < 0 and paddle1_pos >= 0:
        paddle1_pos += paddle1_vel[1]
        
    if paddle2_vel[1] > 0 and paddle2_pos < HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel[1]
    elif paddle2_vel[1] < 0 and paddle2_pos >= 0:
        paddle2_pos += paddle2_vel[1]    
        
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos],[HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH-HALF_PAD_WIDTH, paddle2_pos],[WIDTH-HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "White")
  
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 4, 50], 36, "White")
    canvas.draw_text(str(score2), [WIDTH - WIDTH / 4, 50], 36, "White")
    
  

   

        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = -5
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 5
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = -5
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 5
        
    #print ball_pos    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0    


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Re-start', new_game, 100) 


# start frame
new_game()
frame.start()
