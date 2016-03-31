# Blackjack
# for use in codeskulptor

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")


CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
question = 'Hit or Stand?'
score = 0
newplayer_hand = []
dealer_hand = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
      
    def draw_back(self, canvas, pos):
        if in_play == True:
            canvas.draw_image(card_back, [36, 48], [72, 96], [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], [72, 96])
                              
         
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        hand_list = 'Hand contains'
        for i in range(len(self.cards)):
            hand_list += ' '
            hand_list += str(self.cards[i])
        return hand_list
                       
    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        h_list = ''
        for c in self.cards:
            hand_value += VALUES[str(c)[1]]
        for i in range(len(self.cards)):
            h_list += ' '
            h_list += str(self.cards[i])
        if not 'A' in h_list:
            return hand_value
        else:
            if hand_value +10 <= 21:
                return hand_value+10
            else:
                return hand_value
   
    def draw(self, canvas, pos):      
        for i in range(len(self.cards)):
            self.cards[i].draw(canvas, [pos[0] + ((CARD_SIZE[0] + 10) * i), pos[1]])                      
                         

class Deck:
    def __init__(self):
        #create a Deck object
        self.deck_list = []
        for suit in SUITS:
            for rank in RANKS:
                item = Card(suit, rank)
                self.deck_list.append(item)
                        

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_list)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck_list.pop()
     
    
    def __str__(self):
        # return a string representing the deck
        deck_str = 'Deck contains'
        for i in range(len(self.deck_list)):
            deck_str += ' '
            deck_str += str(self.deck_list[i])
        return deck_str


#event handlers for buttons
def deal():
    global outcome, in_play, my_deck, newplayer_hand, dealer_hand, score
    # your code goes here
    if in_play == True:
        output = 'Player lost the round'
        score -=1
    my_deck = Deck()
    my_deck.shuffle()
    newplayer_hand = Hand()
    dealer_hand = Hand()
    print my_deck
    for i in range(2):
        newplayer_hand.add_card(my_deck.deal_card())
        dealer_hand.add_card(my_deck.deal_card())
    print 'player hand: ', newplayer_hand
    print 'dealer hand: ', dealer_hand
    print 'Dealer', dealer_hand.get_value()
    print 'Player', newplayer_hand.get_value()
    outcome = ''
    in_play = True

def hit():
    global in_play, outcome, score
    # if the hand is in play, hit the player
    if in_play == True:
        newplayer_hand.add_card(my_deck.deal_card())
        print newplayer_hand
        print newplayer_hand.get_value()
        if newplayer_hand.get_value() > 21:
            outcome = 'You are BUST!'
            in_play = False
            score -= 1
            print outcome
    
       
def stand():
    global in_play, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == False:
        outcome = "Sorry you can't stand you are BUST"
        print outcome
    else:
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(my_deck.deal_card())
            print 'dealer hand is ', dealer_hand
            print 'dealer hand value: ', dealer_hand.get_value()
        if dealer_hand.get_value() > 21:
            outcome = 'You win'
            score += 1
            print outcome

        else:
            if dealer_hand.get_value()> newplayer_hand.get_value():
                outcome = 'The dealer won'
                print outcome
                score -= 1
            elif newplayer_hand.get_value() > dealer_hand.get_value():
                outcome = 'You won! Congratulations!'
                print outcome
                score += 1
            else:
                outcome = 'It was a tie, the dealer won'
                print outcome
                score -= 1
        in_play = False
        print 'in plau is now false'
    
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global dealer_hand, newplayer_hand, outcome, score
    dealer_hand.draw(canvas, [10, 200])
    newplayer_hand.draw(canvas, [10, 400])
    card = Card("H", "4")
    card.draw_back(canvas, [10, 200])
    canvas.draw_text('Blackjack', (90, 110), 40, 'White')
    canvas.draw_text('Score ' + str(score), (400, 110), 30, 'Black')
    canvas.draw_text('Dealer', (20, 180), 30, 'Black')
    canvas.draw_text('Player', (20, 380), 30, 'Black')
    canvas.draw_text(outcome, (200, 180), 30, 'Black')
    if in_play == True:
        question = 'Hit or Stand?'
    else:
        question = 'Deal again?'
    canvas.draw_text(question, (200, 380), 30, 'Black')
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

