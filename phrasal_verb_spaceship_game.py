# Mouseclick Handlers
# Phrasal verb game


import simplegui
import codeskulptor
import random


# Global Variables

canvas_width = 1100
canvas_height = 550
canvas_height2 = canvas_height-40 
grid = [["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""], ["", "", "", "", "", ""]]

#definitions 
unit_1 = {
    'show up': ["To attend a meeting or event", "Tom didn't ..... at the party on Saturday", "How many students will .....  to the lecture?"], 
    'run into':["To meet someone by accident", "I don't want to see Simon, I hope I don't ..... him at school", "I was working in the same building as Kate today, I'm surprised I didn't .....her"],
    'turn down':["To reject an invitation or reject someone", "Sorry, I have to ..... your invitation because I'm busy that night", "Why did Simon ..... my invitation to go to the cinema?"],
    'feel up to':["To feel capable of doing something", "I don't ..... going out, I've got a headache", "Will Fred .....walking after his operation?"],
    'sleep in':["To stay in bed later than normal", "I have a meeting at 8am tomorrow, I hope I don't ..... ", "Why are you late? Did you ..... ?"],
    'sit back':["To sit somewhere comfortably and relaxed", "....., relax and enjoy your flight","I like to ..... and read a good book"],
    'sit around':["To be lazy at home and do nothing", "The children always ..... and never help with the house work", "I'm going to do nothing on Sunday, just ..... the house"],
    'get together':["To meet friends socially", "We're going to ..... tonight, do you want to come?", "We always ..... on Friday evening to talking about what happened during the week"]
    }

unit_2 = {
    'do away with':["To kill someone", "The murderer ..... his victim", "He ..... his neighbour with a gun?"], 
    'get away with':["Not get caught for doing something wrong", "The bank robbers ..... with their crime ", "Do you think we will ..... cheating in the exam?"],
    'give yourself up':["Surrender to the police", "The police told the robbers: 'You should ..... because we know who you are", "If you ..... you could receive a shorter prison sentence"],
    'own up':["To confess", "I ....., it was me who ate the last piece of cake", "Will whoever broke the vase please .....?"],
    'put away':["To put somebody in prison", "He was ..... for 10 years", "She was found guilty of murder ..... and put away for life"],
    'see through':["Realise somebody is lying", "I can..... your lies","I got away with it because they didn't ..... my lies"],
    }

all_definitions = dict(unit_1.items() + unit_2.items())


personalised_pv = {}
grid_pos1 = 0
grid_pos2 = 0
won = False
game_over = False
answer = grid[0][0]
lives = 3
clue = ''
selected_answers = []
correct_answers = {}
templist = []
grid_pos = 0
used_clues = []
result = ''
fish_pos = [0,0]
fish_vel = [0, 0]
fish_swim = False
fish = True
mouse_pos = [0,0]
explosion = False
longest = 0
move = 128
middle = 64
congratulations = False
try_again = False
text_pos = canvas_width/3
text_vel = 0


# Helper Functions

#selects a phrasal verb from the first column
def start_game(definitions):
    global answer, grid_pos, clue, used_clue, phrasal_verbs
    phrasal_verbs = definitions
    fill_grid()
    grid_pos2 = 0
    num = random.randint(0,2)
    num2 = random.randint(0,2)
    answer = grid[num][grid_pos2]
    find_clue(answer)
    spawn_fish()
    print answer
 
#randomly fills the grid with words from the dictionary
def fill_grid():
    global templist, phrasal_verbs
    if templist == []:
        for k in phrasal_verbs:
            templist.append(k)
            
    print 'temp list is:', templist

    for i in range(0, len(grid[0])):    
        num = random.randint(0,len(templist)-1)
        grid[0][i] = templist[num]
                
        num2 = random.randint(0,len(templist)-1)
        grid[1][i] = templist[num2]
        
        num3 = random.randint(0,len(templist)-1)
        grid[2][i] = templist[num3]
        
        num4 = random.randint(0,len(templist)-1)
        grid[3][i] = templist[num4] 
        
        num5 = random.randint(0,len(templist)-1)
        grid[4][i] = templist[num5] 
    
def find_clue(answer):
    global used_clues, clue, phrasal_verbs
    num2 = random.randint(0,2)
    clue = phrasal_verbs[answer][num2] 
    if clue in used_clues:
        num2 = random.randint(0,2)
        clue = phrasal_verbs[answer][num2] 
    else:
        used_clues.append(clue)
 


def find_question():
    global grid_pos, answer, game_over, clue, selected, fish_swim 
    #selected = False
    num = random.randint(0,2)
    if check_winner() == False:        
        answer = grid[num][grid_pos]
        find_clue(answer)
    
    
def check_winner():
    global grid_pos, game_over, clue, fish_vel, fish_swim, congratulations
    if grid_pos == len(grid[0]):  #this number should be the length of the rows
        clue = "Congratulations you won!"
        congratulations = True
        fish_swim = True
        game_over = True    
    else:
        return False  
    
      
        
# Returns 'True' if a player has won, false otherwise
def check_win():
    global result, lives, try_again
    if grid[clickpos1][clickpos2] == answer:
        result = "Correct!"
        return True
    else:
        result = "Wrong answer " 
        try_again = True
            
def spawn_fish():
    global fish_swim, fish_pos, fish_vel 
    fish_pos = [50, canvas_height//2]        
    
def flounder():
    global fish_vel, fish_swim
    fish_vel[1] += 0.3
    if fish_vel[1] > 2:
        fish_vel[1] = -2
        
def set_direction():
    global longest, mouse_pos, fish_pos, fish_vel, fish_travel
    difference = 0
    speed = 2
    # calculating the difference between x and y on the vector(longest between x or y will be assigned: longest  / shortest * the difference
    biggest = max(fish_pos[1], mouse_pos[1])
    smallest = min(fish_pos[1], mouse_pos[1])
    if biggest == fish_pos[1]:
        print 'fish is lowest'
    else:
        print 'mouse is highest'
    y = biggest - smallest
    x = mouse_pos[0] - fish_pos[0] 
    longest = max(x, y)
    shortest = min(x, y)
    fish_travel = longest
    # This calculates the amount which the longest distance (x or y) is going to be multiplied by
    try:
        difference = longest / shortest
        print 'difference: ', difference
        print ''
    except ZeroDivisionError:
        fish_vel[0] = 0
        fish_vel[1] = 0
            
    if longest == y:
        print 'y is longest'
        print 'y is ', y
        print 'x is ', x
        if x < 25:
            fish_vel[1] = 2
            fish_vel[0] = 0
            print 'x was < that 25'
        elif biggest == mouse_pos[1]:
            print  'the fish is higher and im about to change its vel'
            fish_vel[1] = speed*difference
            fish_vel[0] = speed
        else:         
            fish_vel[1] = -speed*difference
            fish_vel[0] = speed

    
    elif longest == x:
        if y < 25:
            print 'y was < 25'
            fish_vel[1] = 0
            fish_vel[0] = 2
        elif biggest == mouse_pos[1]:
            print 'fish is higher and needs to go down'
            fish_vel[0] = speed*difference
            fish_vel[1] = speed
            fish_pos[1] = int(fish_pos[1])
            fish_pos[0] = int(fish_pos[0])
        else:
            print 'fish is lowest, needs to go up'
            fish_vel[0] = speed*difference
            fish_vel[1] = -speed
            fish_pos[1] = int(fish_pos[1])
            fish_pos[0] = int(fish_pos[0])
    print 'coordinates set'
    print 'fish_vel[1] ', fish_vel[1]
    print 'fish_vel[0] ', fish_vel[0]
    print ''
    
  
def check_position():
    global fish_pos, mouse_pos, fish_vel, fish_swim
    if fish_pos[0] > mouse_pos[0]-3 and fish_pos[0] < mouse_pos[0]+3:
        fish_vel[1] = 0
        fish_vel[0] = 0
        fish_swim = False
        print 'fish pos ', fish_pos
        print 'mouse pos ', mouse_pos
        print 'check_position says that position has been found'
        print ''
  
            
# Event Handlers   
def draw(canvas):
    # DRAWS THE BACKGROUND
    global guess, selected, grid_pos, block_pos, result, correct_answers, lives, fish_pos, fish_vel, middle, move, explosion, fish, congratulations, text_pos, text_vel, try_again
    canvas.draw_image(nebula, (400, 300), (800, 600), (canvas_width//2, (canvas_height)//2), (canvas_width, canvas_height))
     
    #draws the vertical lines
    if game_over == False:
        canvas.draw_line([0, 40], [canvas_width, 40], 1, "white")
        #canvas.draw_line([0, canvas_height2 // 4], [canvas_width, canvas_height2 // 4], 1, "red")
        #canvas.draw_line([0, canvas_height2 // 4 * 2], [canvas_width, canvas_height2 // 4 * 2], 1, "orange")
        #canvas.draw_line([0, canvas_height2 // 4 * 3], [canvas_width, canvas_height2 // 4 * 3], 1, "Black")
        #draws the horizontal lines
        canvas.draw_line([canvas_width // 6, 40], [canvas_width // 6, canvas_height], 1, "yellow")
        canvas.draw_line([canvas_width // 6 * 2, 40], [canvas_width // 6 * 2, canvas_height], 1, "green")
        canvas.draw_line([canvas_width // 6 * 3, 40], [canvas_width // 6 * 3, canvas_height], 1, "pink")
        canvas.draw_line([canvas_width // 6 * 4, 40], [canvas_width // 6 * 4, canvas_height], 1, "purple")
        canvas.draw_line([canvas_width // 6 * 5, 40], [canvas_width // 6 * 5, canvas_height], 1, "orange")
    canvas.draw_polygon([[0, 40],[canvas_width, 40], [canvas_width, 0], [0, 0]], 2, 'black', 'white')
    canvas.draw_polygon([[0, canvas_height],[canvas_width, canvas_height], [canvas_width, canvas_height-40], [0, canvas_height-40]], 2, 'black', 'white')
    
    #DRAWS MOVING BLOCK
    block_pos = {
        0:[[0, 40],[0, canvas_height-40], [canvas_width//6, canvas_height-40], [canvas_width//6, 40]],
        1:[[canvas_width//6, 40],[canvas_width//6, canvas_height-40], [canvas_width//6*2, canvas_height-40], [canvas_width//6*2, 40]],
        2:[[canvas_width//6*2, 40],[canvas_width//6*2, canvas_height-40], [canvas_width//6*3, canvas_height-40], [canvas_width//6*3, 40]],
        3:[[canvas_width//6*3, 40],[canvas_width//6*3, canvas_height-40], [canvas_width//6*4, canvas_height-40], [canvas_width//6*4, 40]],
        4:[[canvas_width//6*4, 40],[canvas_width//6*4, canvas_height-40], [canvas_width//6*5, canvas_height-40], [canvas_width//6*5, 40]],
        5:[[canvas_width//6*5, 40],[canvas_width//6*5, canvas_height-40], [canvas_width//6*6, canvas_height-40], [canvas_width//6*6, 40]],
        6:[[canvas_width//6*6, 40],[canvas_width//6*6, canvas_height-40], [canvas_width//6*7, canvas_height-40], [canvas_width//6*7, 40]]
    }
    coordinates = block_pos[grid_pos]
    if game_over == False:
        #canvas.draw_polygon(coordinates, 2, 'black', '#00BFFF')#block for fish game
        canvas.draw_polygon(coordinates, 2, 'black', 'black') #block for space game
        
    # draws clue on the screen
    canvas.draw_text(clue, [40, 30], 20, "black")
    
    # draws remaining turns left at bottom of canvas
    canvas.draw_text('Lives left: ' + str(lives), [canvas_width -150, canvas_height-15], 20, "#00BFFF")
    
    # draws if player has answered wrong or right
    canvas.draw_text(result, [40, canvas_height-10], 30, "black")
    
    # Adds text to grid using loops
    if game_over == False:
        for r in range(0,5):
            for c in range(0,6):
                canvas.draw_text(grid[r][c], [c * canvas_width // 6 + 30, r * canvas_height // 6 + 40+70], 23, "white")
                
    
    # CHANGES THE TEXT COLOUR OF COMPLETED QUESTIONS ON THE GRID
        for i in correct_answers:
            canvas.draw_text(grid[correct_answers[i]][i], [i * canvas_width // 6 + 30, correct_answers[i] * canvas_height // 6 + 40+70], 23, "#00BFFF")    
    
    # Draw 'try again' text if question is answered wrong
    if try_again == True and game_over != True:
        canvas.draw_text('Try again', [text_pos, canvas_height/2], 70, "#00BFFF")   
        text_pos += text_vel
        text_vel = 6
        if text_pos > canvas_width:
            try_again = False
            text_pos = canvas_width/3
  
    # draw fish
    if fish == True:
        if fish_swim == True:# and position_found == False:
            canvas.draw_image(ship, (135, 90/2), (90, 90), (fish_pos[0], fish_pos[1]), (90, 90))
            if game_over == False:
                check_position()       
            else:
                fish_vel[0] = 4
                fish_vel[1] = 0
        else:
            flounder()
            canvas.draw_image(ship, (90/2, 90/2), (90, 90), (fish_pos[0], fish_pos[1]), (90, 90))#ship with rockets
    else:       
        explosion = True  
           
    # update fish
    fish_pos[0] += fish_vel[0]
    fish_pos[1] += fish_vel[1] 
 
        
    # DRAW EXLOSION AND GAME OVER
    if explosion == True: 
        timer.start()
        print 'timer has started'
        canvas.draw_image(explode, (middle, 128/2), (move, 128), (fish_pos[0], fish_pos[1]), (move, 128))
        if middle > 3136:
            explosion = False
            timer.stop()
        canvas.draw_text('Game over!!', [canvas_width/3,canvas_height/2], 70, "#00BFFF")       
     
    # DRAW congratulations TEXT
    if congratulations == True:
        canvas.draw_text('Well done!!', [canvas_width/3,canvas_height/2], 70, "#00BFFF")
             
def click(pos):
    global won, game_over, clickpos1, clickpos2, selected, answer, clue, correct_answers, grid_pos, lives, fish_pos, mouse_pos, fish_swim, explosion, fish, game_over_text
    if not game_over:    
        # Checks to see if the click was on a grid line
        if pos[0] % (canvas_width // 6) != 0 and pos[1] % (canvas_height // 6) != 0:
            r = pos[1] // (canvas_height // 4)
            c = pos[0] // (canvas_width // 6)
            # Checks to see if a square is correct answer            
            clickpos1 = r
            clickpos2 = c
            if check_win() == True:
                correct_answers[c]= r
                grid_pos += 1
                mouse_pos = pos
                print 'mouse_pos', mouse_pos  
                print 'fish_pos', fish_pos
                set_direction()
                print 'on click fish vel[1] is: ', fish_vel[1]
                print 'on click fish vel[0] is: ', fish_vel[0]
                fish_swim = True 
                find_question()
           
            else:
                lives -= 1
                if lives <=0:
                    clue = "Game Over!!"
                    fish = False
                    game_over = True
                
                    
def tick():
    global middle, move, explosion
    middle += move    
    print 'middle = ', middle

          

def reset(definitions):
    global grid, clickpos2, game_over, lives, grid_pos, templist, correct_answers, fish_pos, fish_vel, fish_swim, mouse_pos, fish, congratulations, result
    templist = []
    game_over = False
    clickpos2 = 0
    lives = 3
    grid_pos = 0
    correct_answers = {}
    fish_pos = [0,0]
    fish_vel = [0, 0]
    fish_swim = False
    fish = True
    mouse_pos = [0,0]
    start_game(definitions)
    congratulations = False
    text = True
    result = ''

    
def restart():
    reset(all_definitions)    
    
def select_unit1():
    reset(unit_1)
    
def select_unit2():
    reset(unit_2)    

def select_pv(text_input):
    global templist, correct_answers1, correct_answers2
    templist = []
    for pv in definitions:
        if text_input in pv:
            templist.append(pv)
            correct_answers1 = {}
            fill_grid()
            start_game()

    print templist    
    
        
# Frame
frame = simplegui.create_frame("Flounder verbs", canvas_width, canvas_height) 

# Register Event Handlers
frame.set_draw_handler(draw)
frame.set_canvas_background('White')
frame.set_mouseclick_handler(click)

#images
ship = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png')
nebula = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png')
explode = simplegui.load_image('http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png')


inp = frame.add_input('Phrasal verbs including this word:', select_pv, 150)
frame.add_button("Reset", restart)
frame.add_button("Unit 1", select_unit1)
frame.add_button("Unit 2", select_unit2)

# Start
frame.start()
timer = simplegui.create_timer(50, tick)
start_game(all_definitions)

