# implementation of card game - Memory

import simplegui
import random

num_list = []
exposed = []
state = 0
first_pick = 0
second_pick = 0
moves = 0

# helper function to initialize globals
def init():
    global num_list, exposed, moves
    moves = 0
    num_list = [i%8 for i in range(16)]
    random.shuffle(num_list)
    exposed = [False for i in range(16)]
    pass


# define event handlers
def mouseclick(pos):
    global state, first_pick, second_pick, moves
    this_pick = int(pos[0] / 50)
    if state == 0:
        first_pick = this_pick
        exposed[first_pick] = True
        state = 1
        moves += 1
    elif state == 1:
        if not exposed[this_pick]:
            second_pick = int(pos[0] / 50)
            exposed[second_pick] = True
            state = 2
            moves += 1
    elif state == 2:
        if not exposed[this_pick]:
            if num_list[first_pick] == num_list[second_pick]:
                pass
            else:
                exposed[first_pick] = False
                exposed[second_pick] = False
            first_pick = this_pick
            exposed[first_pick] = True
            state = 1
            moves += 1
    l.set_text("Moves = " + str(moves))
    pass


# cards are logically 50x100 pixels in size
def draw(canvas):
    offset = 50
    hor_pos = -25
    for i in range(len(num_list)):
        hor_pos += offset
        canvas.draw_text(str(num_list[i]), [hor_pos, 50], 20, "White")
    exposed_pos = -50
    for i in exposed:
        exposed_pos += offset
        if not i:
            canvas.draw_polygon([(exposed_pos, 0), (exposed_pos + 50, 0), (exposed_pos + 50, 100), (exposed_pos + 0, 100)], 12, "Green", "White")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
l=frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()

# Always remember to review the grading rubric