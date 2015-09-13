# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

count = 7
high = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global count
    global high
    print 'New game. Guess the number between 0 -', high 
    secret_number = random.randrange(0, high)
    count_turns(count)
    print
   
    

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global count
    global high
    global secret_number
    count = 7
    high = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global count
    global high
    global secret_number
    count = 10
    high = 1000
    new_game()
    
def input_guess(guess):
    global count
    print 'Guess was', guess
    if float(guess) < secret_number:
        count_turns(count_down)
        print 'Higher!'
        print
    elif float(guess) > secret_number:
        count_turns(count_down)
        print 'Lower!'
        print
        
    elif float(guess) == secret_number:
        print 'Correct!'
        print
        new_game()
        
    if count_down < 0 and float(guess) != secret_number:
            print 'You ran out of guesses. The answer was', secret_number
            print
            new_game()
   
   
def count_turns(num):
    global count
    global count_down
    count_down = num
    print 'Number of remaining guesses is', count_down
    count_down -= 1

    
# create frame
frame = simplegui.create_frame('Testing', 200, 200)


# register event handlers for control elements and start frame
frame.add_input('Guess', input_guess, 50)
frame.add_button('range100', range100, 100)
frame.add_button('range1000', range1000, 100)


# call new_game 
new_game()
