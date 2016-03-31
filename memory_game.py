# for use in codeskulptor 
# implementation of card game - Memory

import simplegui
import random

canvas_width = 800
canvas_height = 100
exposed = []
counter = 0
state = 0
check_match = []

numbers = []


# helper function to initialize globals
def new_game():
    global exposed2, counter, numbers, check_match, state, exposed, numbers
    get_numbers()
    exposed_cards()
    counter = 0 
    state = 0
    check_match = []
    print exposed
    
def get_numbers():   
    global numbers
    for n in range(0,9):
        numbers+=str(n)
    numbers += numbers
    random.shuffle(numbers)   
    return numbers
       
def exposed_cards():
    global exposed, numbers
    exposed = []
    for nun in numbers:
        exposed.append(False) 
    return exposed    
    
def change_state():    
    global state, counter
    if state == 0:
        state = 1
    elif state == 1:
        state = 2
        counter +=1
        label.set_text('Turns = '+ str(counter))
    else:
        state = 1     


     
# define event handlers
def mouseclick(pos):
    global state, check_match, counter, exposed
    mouse_pos = list(pos)
    print 'state = ', state
    
    if state == 2:
        if numbers[check_match[0]] != numbers[check_match[1]]:
            exposed[check_match[0]] = False
            exposed[check_match[1]] = False
        check_match = []    
            
    
    for c in range(0,18):
        if mouse_pos[0] > c* canvas_width//18 and mouse_pos[0] < (c+1)* canvas_width//18:
            if exposed[c] == False:
                exposed[c] = True
                check_match.append(c)
                change_state()
                print 'check_match', check_match
            else:
                pass
                
            
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global numbers, exposed
    w = -0.7
    for c in range(0,18):
        w+=1
        if exposed[c] == True:
            canvas.draw_text(numbers[c], [w * canvas_width // 18, canvas_height // 1.5], 40, "white")
        else:
            canvas.draw_polygon([[c * canvas_width//18, 0],[c * canvas_width//18, canvas_height], [(c+1)*canvas_width//18, canvas_height], [(c+1)*canvas_width//18, 0]], 1, 'Red', 'Green')
            
        
        



# create frame and add a button and labels
frame = simplegui.create_frame("Memory", canvas_width, canvas_height)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")



# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


