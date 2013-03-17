# template for "Stopwatch: The Game"
import simplegui

# define global variables
tenths_of_seconds = 0

# define helper function format that converts integer
# counting tenths of seconds into formatted string A:BC.D
def format(t):
    D = t % 10
    C = int(t / 10) % 10
    B = (int(t / 100)) % 6
    A = int(t / 600)
    return str(A) + ':' + str(B) + str(C) + '.' + str(D)
# define event handlers for buttons; "Start", "Stop", "Reset"

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tenths_of_seconds
    tenths_of_seconds += 1
    formatted_time = format(tenths_of_seconds)
    print formatted_time

timer = simplegui.create_timer(100, timer_handler)

# create frame
frame = simplegui.create_frame("Game", 300, 200)

# register event handlers
def draw_handler(canvas):
    canvas.draw_text(format(tenths_of_seconds), (100, 100), 12, "White")

def start_handler():
    timer.start()

def stop_handler():
    timer.stop()

frame.set_draw_handler(draw_handler)
frame.add_button("Start", start_handler)
frame.add_button("Stop", stop_handler)

# start timer and frame
frame.start()
#timer.start()

# remember to review the grading rubric