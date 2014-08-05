# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
playerHand = None
dealerHand = None
deck = None
playerMessage = None
dealerMessage = None
stand = False
bustedOrBlackjack = False

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
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        return self.cards

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        aceFound = False
        for card in self.cards:
            value = value + VALUES.get(card.get_rank())
            if card.get_rank() == 'A':
                aceFound = True
        if aceFound == True:
            if value + 10 <= 21:
                return value+10
            else:
                return value	
        else:
            return value
   
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw( canvas, pos)
            pos[0] = pos[0] + CARD_SIZE[0]*3/2  
            
    def drawDealerHand(self, canvas, pos):
        for card in self.cards:
            if self.cards.index(card) == 0:
                card.draw_back(canvas, pos)
            else:
                card.draw(canvas, pos)
            pos[0] = pos[0] + CARD_SIZE[0]*3/2  
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.numbers = range(52)                        

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.numbers)
        print self.numbers

    def deal_card(self):
        x = self.numbers[0]
        self.numbers.remove(x)        
        suit = x/13
        rank = x%13        
        card = Card(self.getSuitFromNumber(suit), self.getRankFromNumber(rank))
        return card
    
    def __str__(self):
        return str(self.numbers)
    
    def getRankFromNumber(self, number):
        if number+1 == 1:
            return "A"
        if number+1 >=2 and number+1 <= 9:
            return str(number+1)
        if number+1 == 10:
            return "T"
        if number+1 == 11:
            return "J"
        if number+1 == 12:
            return "Q"
        if number+1 == 13:
            return "K"
       
    def getSuitFromNumber(self, number):
        if number == 0:
            return "C"
        if number == 1:
            return "S"
        if number == 2:
            return "H"
        if number == 3:
            return "D"

#define event handlers for buttons
def deal():
    global outcome, in_play, playerHand, dealerHand, deck, playerMessage, dealerMessage, stand, bustedOrBlackjack, score

    playerMessage = None
    dealerMessage = None
    stand = False
    bustedOrBlackjack = False
    if in_play == True:
        score -= 1
    # your code goes here
    deck = Deck()
    deck.shuffle()    
    card1 = deck.deal_card()
    card2 = deck.deal_card()
    card3 = deck.deal_card()
    card4 = deck.deal_card()
    
    print card1, card2, card3, card4
    playerHand = Hand()
    dealerHand = Hand()
    playerHand.add_card(card1)
    dealerHand.add_card(card2)
    playerHand.add_card(card3)
    dealerHand.add_card(card4)
    in_play = True
    value = playerHand.get_value()
    if value == 21:
        dealerMessage = "Blackjack!"
        playerMessage = None
        in_play = False
        bustedOrBlackjack = True
        score += 1  
    else:
        playerMessage = "Hit Or Stand?"

def hit():
    global in_play, playerHand, dealerHand, deck, playerMessage, bustedOrBlackjack, score, dealerMessage
    if in_play == True:
        card = deck.deal_card()
        playerHand.add_card(card)
        value = playerHand.get_value()
        print "value :" + str(value)
        if value == 21:
            dealerMessage = "Blackjack!"
            playerMessage = None
            in_play = False
            bustedOrBlackjack = True
            score += 1
        if value > 21:
            dealerMessage = "Player Busted"
            playerMessage = "New Deal?"
            in_play = False         
            bustedOrBlackjack = True
            score -= 1
       
def stand():
    global in_play, playerHand, dealerHand, deck, dealerMessage, stand, score, playerMessage, bustedOrBlackjack
    
    stand = True
    if bustedOrBlackjack == False:
        playerMessage = None
    while in_play == True:
        card = deck.deal_card()
        dealerHand.add_card(card)
        x = dealerHand.get_value()
        if x>=17:
            in_play = False
    
    if bustedOrBlackjack == False:
        x = dealerHand.get_value()
        y = playerHand.get_value()
        if x>21:
            dealerMessage = "Player wins"
            playerMessage = "New Deal?"
            score +=1
            print "player wins"
        elif x>y:
            dealerMessage = "Dealer wins"
            playerMessage = "New Deal?"
            score -= 1
            print "dealer wins"
        else:
            dealerMessage = "Player wins"
            playerMessage = "New Deal?"
            score += 1
            print "player wins"           

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global playerHand, dealerHand, playerMessage, dealerMessage, stand, bustedOrBlackjack, score
    #card = Card("S", "A")
    #card.draw(canvas, [100, 400])
    canvas.draw_text("Blackjack", (90, 75), 50, 'Blue')
    playerHand.draw(canvas, [100, 400])
    if stand == False or bustedOrBlackjack == True:
        dealerHand.drawDealerHand(canvas, [100, 200])	  
    else:
        dealerHand.draw(canvas, [100, 200])
    
    canvas.draw_text("Dealer", (100, 170), 35, 'Red')
    canvas.draw_text("Player", (100, 370), 35, 'Red')
    if dealerMessage != None:
       canvas.draw_text(dealerMessage, (275, 170), 35, 'Red')
    if playerMessage != None:
       canvas.draw_text(playerMessage, (275, 370), 35, 'Red')

    canvas.draw_text("Score : " + str(score), (400, 75), 40, 'Black')

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


# remember to review the gradic rubric