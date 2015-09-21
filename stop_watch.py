# template for "Stopwatch: The Game"
import simplegui

# define global variables
interval = 100
count = 0
stop_count = 0
win_count = 0
score = str(win_count) + '/' + str(stop_count)
tens = 0.0
run = True


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global tens
    a = (t // 10) // 60
    
    secs = str((t // 10))   
    b = (int(secs)%60)//10

    #s = str((t // 10))   
    c = (int(secs[-1])%60)%10
    
    d = t%10
    tens = d
    return str(a)+':' + str(b) + str(c) + '.' + str(d)

    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def stop():
    global run
    global stop_count
    global win_count
    timer.stop()
    if run == True:
        stop_count +=1
        if tens == 0:
            win_count +=1
        run = False
    
def start():
    global run
    timer.start()
    run = True
    
def reset():
    global count
    global stop_count
    global win_count
    timer.stop()
    count = 0
    stop_count = 0
    win_count = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count +=1
            


# define draw handler
def draw(canvas):
    global count
    canvas.draw_text(str(format(count)), [250, 250], 36, "White")
    canvas.draw_text(str(stop_count) + '/' + str(win_count), [400, 50], 26, "White")
    
    

    
# create frame
frame = simplegui.create_frame("Home", 500, 500)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)
frame.add_button('Start', start, 100)
frame.add_button('Stop', stop, 100)
frame.add_button('Reset', reset, 100)

# start frame
frame.start()
#timer.start()


