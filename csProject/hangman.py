#HANGMAN GAME
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
num_guesses=6
happ=["_","_",'_','_','_','_']
game_1,play,head,body,left_arm,right_arm,left_leg,right_leg,word=False,False,False,False,False,False,False,False,False
secret,game=True,True
start= True
win_image = simplegui.load_image("http://www.newyorker.com/wp-content/uploads/2016/01/Duca-Donald-Trumps-Path-to-Victory-290x149-1453933086.jpg")
lose_image = simplegui.load_image("http://static.tvtropes.org/pmwiki/pub/images/hanging2_3655.jpg")
start_first = True
loss = False
win = False

loss_sound = simplegui.load_sound("D:\Pygame\csProject\hangman_loss.ogg")
win_sound = simplegui.load_sound("D:\Pygame\csProject\hangman_win.ogg")

def draw(canvas):
    global num_guesses
    canvas.draw_text("*H-A-N-G-M-A-N*",(50,50),40,"Red")
    if start:
        canvas.draw_text(" CHOOSE AN OPTION ",(40,120),30,"Red")
        canvas.draw_polygon([(30,170),(190,170),(190,230),(30,230)],6,"Red")
        canvas.draw_polygon([(30,250),(190,250),(190,310),(30,310)],6,"Red")
        canvas.draw_polygon([(30,330),(190,330),(190,390),(30,390)],6,"Red")
        canvas.draw_polygon([(210,170),(370,170),(370,230),(210,230)],6,"Red")
        canvas.draw_polygon([(210,250),(370,250),(370,310),(210,310)],6,"Red")
        canvas.draw_polygon([(210,330),(370,330),(370,390),(210,390)],6,"Red")
        canvas.draw_text("ANIMALS",(40,210),30,"Red")
        canvas.draw_text("VOCAB",(40,290),30,"Red")
        canvas.draw_text("SOCIAL",(40,370),30,"Red")
        canvas.draw_text("MATHS",(220,210),30,"Red")
        canvas.draw_text("SCIENCE",(220,290),30,"Red")
        canvas.draw_text("RANDOM",(220,370),30,"Red")
    if not start:
            text=happ[0]+" "+happ[1]+" "+happ[2]+" "+happ[3]+" "+happ[4]+" "+happ[5]
            if start_first:
                canvas.draw_polyline([(175,275),(175,100),(275,100),(275,125)],7,"Blue")
                canvas.draw_line((100,275),(300,275),7,"Blue")
             
            if game:
                canvas.draw_text("Number of Guesses Remaining : ",(25,400),25,"Red")
                canvas.draw_text(str(num_guesses),(375,400),25,"Red")
            if not game:
                canvas.draw_text("CLICK ON NEW GAME",(30,400),30,"Yellow")
                canvas.draw_text("TO PLAY AGAIN!",(70,440),30,"Yellow")
            if secret:
                canvas.draw_text("Word: "+text,(25,350),40,"Green")
            if head:
                canvas.draw_circle((275,140),15,10,"Red")
            if body:
                canvas.draw_line((275,155),(275,225),10,"Red")
            if left_arm:
                canvas.draw_line((275,200),(225,160),10,"Red")
            if right_arm:
                canvas.draw_line((275,200),(315,160),10,"Red")
            if left_leg:
                canvas.draw_line((275,223),(225,265),10,"Red")
            if right_leg:
                canvas.draw_line((275,223),(315,265),10,"Red")
            if word:
                canvas.draw_text("Answer : "+secret_word,(5,350),40,"Aqua")
            if play:
                canvas.draw_text("THANK YOU FOR PLAYING!",(20,90),30,"Orange")
            if game_1:
                canvas.draw_text("CONGRATS,YOU WON!",(10,90),35,"White")
                
            if win:
                canvas.draw_image(win_image,(290/2,149/2),(290,149),(150,200),(300,200))
                win_sound.play()
            if loss:
                loss_sound.play()
                canvas.draw_image(lose_image,(350/2,359/2),(350,359),(80,200),(150,150))
                
def guess(text):
    global stop,secret,word,a,bad,happ,num_guesses,head,body,left_arm,right_arm,left_leg,right_leg,game,play
    a=0
    global loss,win
    text=text.upper()
    if num_guesses!=0:
        for i in range(len(secret_word)):
            if (secret_word[i]==text):
                happ[i]=secret_word[i]
                a=1
            if happ[0]+happ[1]+happ[2]+happ[3]+happ[4]+happ[5]==secret_word:
                stop=True
                win = True
                game= False
                time()
            
        if a==0:           
                num_guesses=num_guesses-1
                if num_guesses==5:
                    head =True
                elif num_guesses==4:
                    body=True
                elif num_guesses==3:
                    left_arm=True
                elif num_guesses==2:
                    right_arm=True
                elif num_guesses==1:
                    left_leg=True
                elif num_guesses==0:
                    right_leg,word,play=True,True,True
                    secret=False
                    loss = True
    else:pass
def timer_handler():
    global game_1,stop,start_first
    if stop:
        game_1= not game_1
        start_first = False
    else: game_1=False
def time():
    global timer
    timer.start()
def init_new_game(n):
        global secret_word,stop,happ,secret,head,body,left_arm,right_arm,left_leg,right_leg,word,play,num_guesses,z,game_1,a,game
        global start,start_first,loss,win
        win = False
        loss= False
        start_first = True
        start = False
        head,body,left_arm,right_arm,left_leg,right_leg,word,play,game_1=False,False,False,False,False,False,False,False,False
        z=random.randrange(len(n))
        secret_word=n[z]
        stop=False
        head,body,left_arm,right_arm,left_leg,right_leg,word,play,game_1=False,False,False,False,False,False,False,False,False
        num_guesses=6
        happ= ["_","_",'_','_','_','_']
                

def click(pos):
        global n
        if start:
                if pos[0]>30 and pos[0]<190:
                        if pos[1]>170 and pos[1]<230:
                                n=["BEAVER","DONKEY","MONKEY","RODENT","SAMBAR","TURTLE","WALRUS","WEASEL","BATMAN","KITTEN"]
                                init_new_game(n)                                
                        elif pos[1]>250 and pos[1]<310:
                                n=["DEPLOY","INTERN","MELODY","OCCUPY","JOGGLE","BOLERO","CALLOW","UPCAST","CUDDLE"]
                                init_new_game(n)
                        elif pos[1]>330 and pos[1]<390:
                                n=["BATTLE","BUREAU","GLOBAL","EXPORT","BARTER","SENATE","BELIEF","RIGHTS","ROADIE","CENSUS","MARKET","VALUES","COUNTY","DEMAND","DESERT","ETHICS","FEUDAL","POLICY"]
                                init_new_game(n)                                
                        
                elif pos[0]>210 and pos[0]<370:
                        if pos[1]>170 and pos[1]<230:
                                n=["COSINE","BINARY","DEGREE","EUCLID","DOMAIN","FACTOR","GOOGOL","OBTUSE","RADIUS","MATRIX","SECANT","VOLUME","SUBSET","SPHERE","SQUARE"]
                                init_new_game(n)
                        elif pos[1]>250 and pos[1]<310:
                                n=["CONVEX","ACETIC","SCALAR","VECTOR","GALAXY","COMETS","MATTER","MOTION","PLANET","ORGANS","SYSTEM","TISSUE","ALKALI","CARBON","ENERGY","FUSION","ZOMBIE"]
                                init_new_game(n)
                        elif pos[1]>330 and pos[1]<390:
                                n=["ARMOUR","AHIMSA","ABROAD","ANNEXE","ACCENT","BAKERY","BANDIT","DELETE","FOODIE","GADGET","HORROR","PSYCHO"]
                                init_new_game(n)
                                

def new_game():
    global secret_word,n,stop,happ,secret,head,body,left_arm,right_arm,left_leg,right_leg,word,play,num_guesses,z,game_1,a,game
    global start,start_first,loss,win,timer
    timer.stop()
    loss= False
    win = False
    start_first = False
    start = True
    happ= ["_","_",'_','_','_','_']
    secret,game=True,True
    head,body,left_arm,right_arm,left_leg,right_leg,word,play,game_1=False,False,False,False,False,False,False,False,False
    num_guesses=6
def quit_game():
    global timer
    frame.stop()
    timer.stop()
    
frame= simplegui.create_frame("Hangman Game",400,450)
b=frame.add_button("New Game",new_game,100)             
q=frame.add_button("Quit",quit_game,100)
timer=simplegui.create_timer(200,timer_handler)
inp = frame.add_input("Enter your guess: ",guess,100)        
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
frame.start()
