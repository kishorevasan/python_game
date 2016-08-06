"""3 IN ONE GAME FILE"""
print "WELCOME TO THE WORLD OF GAMES"
while True:
    a = int(raw_input("Choose any game:\n1) Pong\n2) Hangman\n3) RiceRocks\n"))
    if a ==1:
        import pong
    elif a ==2:
        import hangman
    elif a ==3:
        import riceRocks
    n = raw_input("Want to play another game? Y/N\n")
    if n == "Y":
        continue
    else: break
print "Thank you for Playing! :D"

