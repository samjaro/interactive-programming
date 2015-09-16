# Rock-paper-scissors-lizard-Spock template

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# input will come from buttons 
# all output for the game will be printed in the console


import simplegui
import random

player_score = 0
comp_score = 0
count = 0

# helper function to start and restart the game

def new_game():
    global comp_score
    global player_score
    global count
    comp_score = 0
    player_score = 0
    count = 0
    print
    print 'choose between: rock, paper, scissors, lizard or Spock'
    print

def name_to_number(name):
    """
    Returns the number associated with the inputed name
    """
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        return "Name doesn't match"
        

def number_to_name(number):
    # delete the following pass statement and fill in your code below
    """
    Takes a number between 1 - 4 and converts it into a name
    """
    if number == 0:
        return 'Rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        return 'That number is incorrect'
    
def best_of_3(comp_score, player_score):
    if comp_score > player_score:
        print
        print 'Sorry the computer beat you!'
    else:    
        print
        print 'Congratulations! you won best out of 3!'
        
    

# define event handlers for control panel


def guess_rock():
    return input_guess('rock')

def guess_paper():
    return input_guess('paper')

def guess_scissors():
    return input_guess('scissors')

def guess_lizard():
    return input_guess('lizard')

def guess_spock():
    return input_guess('Spock')
    
def input_guess(player_choice):
    global comp_score
    global player_score
    global count
    count += 1
    print
    print 'Game', count
    print
    print 'Player chooses: ', player_choice
    player_number = name_to_number(player_choice)
    player_number = 0
    comp_number = random.randrange(5)
    comp_choice = number_to_name(comp_number)
    print 'Computer chooses: ', comp_choice
    difference = (player_number - comp_number) %5
# use if/elif/else to determine winner, print winner message
    if difference ==2 or difference ==1:
        print 'Player wins!'
        player_score += 1
    elif difference ==3 or difference ==4:
        print 'Computer wins!'
        comp_score += 1
    elif difference ==0:
        print 'player and computer tie!'
        print    
    if count == 3:
        best_of_3(comp_score, player_score)
        comp_score = 0
        player_score = 0
        count = 0
        
   
  
    
    
        
# create frame
frame = simplegui.create_frame('Testing', 300, 200)


# register event handlers for control elements and start frame

frame.add_button('rock', guess_rock, 100)
frame.add_button('paper', guess_paper, 100)
frame.add_button('lizard', guess_lizard, 100)
frame.add_button('scissors', guess_scissors, 100)
frame.add_button('spock', guess_spock, 100)
frame.add_button('new game', new_game, 100)


# call new_game 
new_game()

