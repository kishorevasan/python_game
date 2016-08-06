"""THE GAME OF PONG"""
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

#GLOBAL VARIABLES
width=600
height=300
ball_pos=[int(width/2),int(height/2)]
radius=3
vel=[random.randrange(-1,2,2),random.randrange(-1,2)]
score_1=0
score_2=0
Pad_Top_Left_y=0
Pad_Bottom_Left_y=50
Pad_Top_Right_y=0
Pad_Bottom_Right_y=50
Pad_Right=[Pad_Top_Right_y,Pad_Bottom_Right_y]
Pad_Height=0
Pad_Height_1=0
Pad_Left=[Pad_Top_Left_y,Pad_Bottom_Left_y]
LEFT,RIGHT=False,False
start = True
controls = False
w_key = simplegui.load_image("https://www.wpclipart.com/computer/keyboard_keys/letters/computer_key_W.png")
s_key = simplegui.load_image("https://www.wpclipart.com/computer/keyboard_keys/letters/computer_key_S.png")
up_key = simplegui.load_image("https://www.wpclipart.com/computer/keyboard_keys/arrow_keys/computer_key_Arrow_Up.png")
down_key = simplegui.load_image("https://www.wpclipart.com/computer/keyboard_keys/arrow_keys/computer_key_Arrow_Down.png")
multi_arrow_image=simplegui.load_image("https://cdn2.iconfinder.com/data/icons/crystalproject/crystal_project_256x256/apps/restart-1.png")

pong_sound = simplegui.load_sound("D:\Pygame\csProject\pong_music.ogg")
pong_sound.set_volume(.5)
pong_sound.play()

pong_image = simplegui.load_image("http://www.slashgear.com/wp-content/uploads/2015/07/PONG.jpg")
pong_restart = simplegui.load_sound("D:\Pygame\csProject\pong_restart.ogg")

#HANDLER(S)
def draw(canvas):
    global vel,score_1,LEFT,RIGHT,score_2,Pad_Height,Pad_Right,Pad_Left,Pad_Height_1
    if start:
        canvas.draw_image(pong_image,(1280/2,714/2),(1280,714),(300,150),(600,300))
        canvas.draw_polygon([(40,240),(140,240),(140,280),(20,280)],5,"Black")
        canvas.draw_polygon([(460,240),(555,240),(595,280),(460,280)],5,"Black")
        canvas.draw_text("PLAY",(50,270),30,"Red")
        canvas.draw_text("CONTROLS",(465,270),20,"Red")
    if controls:
        canvas.draw_polygon([(50,40),(560,40),(560,280),(50,280)],10,"Red")
        canvas.draw_text("CONTROLS",(180,100),40,"White")
        canvas.draw_image(w_key,(559/2,527/2),(559,527),(90,140),(50,50))
        canvas.draw_image(s_key,(559/2,527/2),(559,527),(90,230),(50,50))
        canvas.draw_image(up_key,(559/2,527/2),(559,527),(350,140),(50,50))
        canvas.draw_image(down_key,(559/2,527/2),(559,527),(350,230),(50,50))
        canvas.draw_image(multi_arrow_image,(256/2,256/2),(256,256),(20,270),(40,40))
        canvas.draw_line((120,140),(140,140),8,"Blue")
        canvas.draw_line((120,230),(140,230),8,"Blue")
        canvas.draw_line((390,140),(410,140),8,"Blue")
        canvas.draw_line((390,230),(410,230),8,"Blue")
        canvas.draw_text("Left Paddle",(150,150),20,"Red")
        canvas.draw_text("UP",(150,170),20,"Red")
        canvas.draw_text("Left Paddle",(150,230),20,"Red")
        canvas.draw_text("DOWN",(150,250),20,"Red")
        canvas.draw_text("Right Paddle",(430,150),20,"Red")
        canvas.draw_text("UP",(430,170),20,"Red")
        canvas.draw_text("Right Paddle",(430,230),20,"Red")
        canvas.draw_text("DOWN",(430,250),20,"Red")
        
    if not start and not controls:
        ball_pos[0]+=vel[0]
        ball_pos[1]+=vel[1]
    
        #MAKING BALL BOUND TO X AXIS
        if ball_pos[0]+radius >= 584:	
            ball_pos[0] = 2*584 - ball_pos[0]-2*radius
            vel[0] *= -1
            if ball_pos[1]<=Pad_Right[1] and ball_pos[1]>=Pad_Right[0]:
                if ball_pos[1]<(int((Pad_Right[1]-Pad_Right[0])/2)) and ball_pos[1]>=Pad_Right[0]:
                    vel[1]+=1
                else:
                    vel[1]-=1
                vel[0]-=1
            else: 
                score_1+=1
                LEFT=True
                new_game()
        elif ball_pos[0]-radius <= 15:	
            ball_pos[0] = 2*15 - ball_pos[0]+2*radius
            vel[0] *= -1
            if ball_pos[1]>=Pad_Left[0] and ball_pos[1]<=Pad_Left[1]:
                if ball_pos[1]>=Pad_Left[0] and ball_pos[1]<int((Pad_Left[1]-Pad_Left[0])/2):
                    vel[1]-=1
                else: 
                    vel[1]+=1
                vel[0]+=1
            else: 
                score_2+=1 
                RIGHT=True
                new_game()
        #MAKING BALL BOUND TO Y AXIS
        if ball_pos[1]+radius >= 299:	
            ball_pos[1] = 2*299 - ball_pos[1]-2*radius
            vel[1] *= -1
        elif ball_pos[1]-radius <= 0:	
            ball_pos[1] = -ball_pos[1]+2*radius
            vel[1] *= -1
        
        Pad_Right[0]+=Pad_Height  
        Pad_Right[1]+=Pad_Height
        #MAKING RIGHT PAD BOUND TO LAYOUT
        if Pad_Right[0]<=0:
            Pad_Height=0
        elif Pad_Right[1]>=299:
            Pad_Height=0
        
        Pad_Left[0]+=Pad_Height_1
        Pad_Left[1]+=Pad_Height_1
        #MAKING LEFT PAD BOUND TO LAYOUT
        if Pad_Left[0]<=0:
            Pad_Height_1=0
        elif Pad_Left[1]>=299:
            Pad_Height_1=0
        
        #DRAW FUNCTIONS
        canvas.draw_line([width/2,0],[width/2,height],3,'Blue')
        canvas.draw_circle(ball_pos,radius,10,'Blue')
        canvas.draw_line([15,0],[15,299],3,'Red')
        canvas.draw_line([584,0],[584,299],3,'Red')
        canvas.draw_polygon([(585,Pad_Right[0]),(601,Pad_Right[0]),(601,Pad_Right[1]),(585,Pad_Right[1])],4,"Yellow","Blue")
        canvas.draw_polygon([(0,Pad_Left[0]),(14,Pad_Left[0]),(14,Pad_Left[1]),(0,Pad_Left[1])],4,"Yellow","Blue")
        canvas.draw_text(str(score_1),(250,50),50,"White")
        canvas.draw_text(str(score_2),(325,50),50,"White")
        canvas.draw_circle((width/2,height/2),20,4,"Blue")

def key_handler(key):
    global Pad_Height_1,Pad_Height
    if key==simplegui.KEY_MAP['down']:
        Pad_Height+=3   
    elif key==simplegui.KEY_MAP['up']:
        Pad_Height-=3
    if key==simplegui.KEY_MAP['w']:
        Pad_Height_1-=3
    elif key==simplegui.KEY_MAP['s']:
        Pad_Height_1+=3

def new_game():
    global vel,ball_pos,LEFT,RIGHT,Pad_Left,Pad_Height_1,Pad_Height,Pad_Right,Pad_Bottom_Right_y,Pad_Top_Right_y,Pad_Top_Left_y,Pad_Bottom_Left_y
    vel=[random.randrange(1,2),random.randrange(-1,2)]
    ball_pos=[int(width/2),int(height/2)]
    if RIGHT:
        pass
    else:
        vel[0]=-vel[0]
        LEFT=False
    RIGHT,LEFT=False,False    

def Button_handler():
    global pong_restart,vel,LEFT,RIGHT,ball_pos,score_1,score_2,Pad_Left,Pad_Height_1,Pad_Height,Pad_Right,Pad_Bottom_Right_y,Pad_Top_Right_y,Pad_Top_Left_y,Pad_Bottom_Left_y
    pong_restart.play()
    vel=[random.randrange(-1,2,2),random.randrange(-1,2)]
    score_1=0
    score_2=0
    Pad_Top_Left_y=0
    Pad_Bottom_Left_y=50
    Pad_Top_Right_y=0
    Pad_Bottom_Right_y=50
    Pad_Right=[Pad_Top_Right_y,Pad_Bottom_Right_y]
    Pad_Height=0
    Pad_Height_1=0
    Pad_Left=[Pad_Top_Left_y,Pad_Bottom_Right_y]
    ball_pos=[int(width/2),int(height/2)]
    LEFT,RIGHT=False,False

def key_handler_1(key):
    global Pad_Height,Pad_Height_1
    Pad_Height= 0
    Pad_Height_1=0

def click(pos):
    global start,controls
    if start:
        if pos[1]>240 and pos[1]<280:
            if pos[0]>40 and pos[0]<140:
                start = False
            elif pos[0]>460 and pos[0]<555:
                controls = True
                start = False
    if controls:
        if pos[0]>5 and pos[0]<35:
            if pos[1]>255 and pos[1]<285:
                controls = False
                start = True

def quit_game():
    frame.stop()
    pong_sound.pause()
    
#INITIALIZIATION FUNCTIONS   
frame= simplegui.create_frame("PONG",width,height)
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_handler)
frame.add_button("Restart",Button_handler,100)
frame.add_button("Quit",quit_game,100)
frame.set_keyup_handler(key_handler_1)
frame.set_mouseclick_handler(click)
frame.start()
