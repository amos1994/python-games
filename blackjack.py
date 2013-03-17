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
player_hand = None
dealer_hand = None
deck = None
message = ''

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

# define hand class
class Hand:
    def __init__(self, cards):
        self.cards = cards
        pass	# replace with your code

    def __str__(self):
        string = ''
        for i in self.cards:
            string += ' ' + str(i)
        return string

    def add_card(self, card):
        self.cards.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        value = 0
        for c in self.cards:
            value += VALUES[c.rank]
        for c in self.cards:
            if c.rank == "A" and value + 10 <= 21:
                value += 10
        return value

    def busted(self):
        if self.get_value() > 21:
            return True
        else:
            return False

    def draw(self, canvas, p):
        for c in self.cards:
            p[0] += CARD_SIZE[0]
            c.draw(canvas, p)


# define deck class
class Deck:
    def __init__(self):
        self.cards = [Card(s, r) for s in SUITS for r in RANKS]
        #print 'initial card pack'
        #for c in self.cards:
            #print c,

    # add cards back to deck and shuffle
    def shuffle(self):
        #print '\nshuffled cards'
        self.cards = [Card(s, r) for s in SUITS for r in RANKS]
        random.shuffle(self.cards)
        #for c in self.cards:
            #print c,

    def deal_card(self):
        return self.cards.pop()


#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, message, score

    if in_play:
        score -= 1

    message = ''
    # your code goes here
    deck = Deck()
    deck.shuffle()
    player_hand = Hand([deck.deal_card(), deck.deal_card()])
    dealer_hand = Hand([deck.deal_card(), deck.deal_card()])
    #print '\n\nplayer ', player_hand, player_hand.get_value()
    #print 'dealer ', dealer_hand, dealer_hand.get_value(), '\n'
    message = "Hit or Stand?"

    in_play = True

def hit():
    global message, in_play, score
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        #print 'player ', player_hand, ' ', player_hand.get_value()
        if player_hand.busted():
            message = "You have busted"
            score -= 1
            in_play = False
    # if busted, assign an message to outcome, update in_play and score

def stand():
    global dealer_hand, deck, in_play, score, message

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            #print 'dealer ', dealer_hand, ' ', dealer_hand.get_value()

    # assign a message to outcome, update in_play and score
        in_play = False

        if dealer_hand.busted():
            score += 1
            message = "Dealer bust. You win. \nNew deal?"
        elif dealer_hand.get_value() >= player_hand.get_value():
            score -= 1
            message = "You lose \nNew deal?"
        else:
            score += 1
            message = "You win \nNew deal?"




# draw handler
def draw(canvas):
    global message
    # test to make sure that card.draw works, replace with your code below

    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])

    player_hand.draw(canvas, [50, 400])
    dealer_hand.draw(canvas, [50, 200])

    canvas.draw_text(message, [50, 80], 20, "White")

    canvas.draw_text('Score ' + str(score), [500, 50], 20, "White")

    canvas.draw_text('Player', [50, 350], 20, "White")

    canvas.draw_text('Dealer', [50, 150], 20, "White")

    canvas.draw_text('Black Jack', [50, 50], 30, "Blue")

    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [52 + CARD_BACK_SIZE[0] + CARD_BACK_CENTER[0], 201 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()


# remember to review the gradic rubric