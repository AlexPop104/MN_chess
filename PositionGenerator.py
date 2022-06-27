import pygame as p
import re
import copy


import ChessEngine as ce


WIDTH =  1024   
HEIGHT = 1024
DIMENSION =8

# print("Width=")
# DIMENSION_WIDTH=int(input())


# print("Height=")
# DIMENSION_HEIGHT=int(input())

DIMENSION_WIDTH=8
DIMENSION_HEIGHT=8

DIMENSION_WIDTH=8
DIMENSION_HEIGHT=8

# 

SQ_SIZE=HEIGHT//DIMENSION

SQ_SIZE_HEIGHT = HEIGHT//DIMENSION_HEIGHT
SQ_SIZE_WIDTH = HEIGHT//DIMENSION_WIDTH


MAX_FPS=15
IMAGES={}

def loadImages():
    pieces=["wp","wR","wN","wB","wK","wQ","bp","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("/home/alex-pop/Desktop/Chess_games/MN_chess/images/"+piece+".png"),(SQ_SIZE_HEIGHT,SQ_SIZE_WIDTH))

def main():
    p.init()

    print("file_name=")
    file_name=str(input())

    gs=ce.GameState(nr_rows=1,nr_columns=1)

    with open(file_name+".txt", 'r') as f:
        nr= f.readline()
        extracted_nr=re.findall('[0-9]+',nr)
        [DIMENSION_HEIGHT,DIMENSION_WIDTH]=list(map(int, extracted_nr))
        
        gs=copy.deepcopy(ce.GameState(nr_rows=DIMENSION_HEIGHT,nr_columns=DIMENSION_WIDTH))
        

        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        
        for i in range(DIMENSION_HEIGHT):
            words=lines[i]
            split_words=words.split()
            for j in range(DIMENSION_WIDTH):
                gs.board[i][j]=split_words[j]

            

        


    screen =p.display.set_mode([WIDTH,HEIGHT])
    clock=p.time.Clock()
    screen.fill(p.Color("white"))

    
    

    #gs=ce.GameState(nr_rows=DIMENSION_HEIGHT,nr_columns=DIMENSION_WIDTH)
    #print(gs.board)

    drawBoard(screen,gs)
    loadImages()
    p.display.flip()
    
                    




  

    
    validMoves=gs.getValidMoves()
    moveMade=False

    
    running=True
    sqSelected={}
    playerClicks=[]
    while running:
        for e in p.event.get():
            mouse_buttons = p.mouse.get_pressed()
            if e.type==p.QUIT:
                running =False
            #elif e.type==p.MOUSEBUTTONDOWN:
            elif mouse_buttons[0]:
                location = p.mouse.get_pos()
                col= location[0]//SQ_SIZE_HEIGHT
                row= location[1]//SQ_SIZE_WIDTH
                if gs.board[row][col]=="--":
                    gs.board[row][col]="wp"
                elif gs.board[row][col]!="R" and gs.board[row][col][0]!="b":
                        if gs.board[row][col][1]=="p":
                            gs.board[row][col]="wN"
                        elif gs.board[row][col][1]=="N":
                            gs.board[row][col]="wB"
                        elif gs.board[row][col][1]=="B":
                            gs.board[row][col]="wR"
                        elif gs.board[row][col][1]=="R":
                            gs.board[row][col]="wQ"
                        elif gs.board[row][col][1]=="Q":
                            gs.board[row][col]="wK"
                        elif gs.board[row][col][1]=="K":
                            gs.board[row][col]="--"
            #elif e.type==p.MOUSEBUTTONDOWN and e.button == 3:
            elif mouse_buttons[2]:
                    location = p.mouse.get_pos()
                    col= location[0]//SQ_SIZE_HEIGHT
                    row= location[1]//SQ_SIZE_WIDTH
                    if gs.board[row][col]=="--":
                        gs.board[row][col]="bp"
                    elif gs.board[row][col]!="R" and gs.board[row][col][0]!="w":
                            if gs.board[row][col][1]=="p":
                                gs.board[row][col]="bN"
                            elif gs.board[row][col][1]=="N":
                                gs.board[row][col]="bB"
                            elif gs.board[row][col][1]=="B":
                                gs.board[row][col]="bR"
                            elif gs.board[row][col][1]=="R":
                                gs.board[row][col]="bQ"
                            elif gs.board[row][col][1]=="Q":
                                gs.board[row][col]="bK"
                            elif gs.board[row][col][1]=="K":
                                gs.board[row][col]="--"
                

            elif e.type== p.KEYDOWN:
                if e.key==p.K_s:
                    print("file_name=")
                    file_name=str(input())

                    

                    with open("board_"+file_name+".txt", 'w') as f:
                        f.write(str(DIMENSION_HEIGHT)+" ")
                        f.write(str(DIMENSION_WIDTH))
                        f.write('\n')
                        for r in range(0,DIMENSION_HEIGHT):
                            for c in range(0,DIMENSION_WIDTH):
                                f.write(gs.board[r][c]+" ")
                            f.write('\n')
                    
                          
                    
                   

                

        for i in range(DIMENSION_WIDTH):
            if(gs.board[0][i]=='wp'):
                gs.board[0][i]='wQ'
                loadImages()
            if(gs.board[DIMENSION_HEIGHT-1][i]=='bp'):
                gs.board[DIMENSION_HEIGHT-1][i]='bQ'
                loadImages()


        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs):
    drawBoard(screen,gs)
    drawPieces(screen,gs.board)

def drawBoard(screen,gs):
    colors=[p.Color("white"),p.Color("gray")]
    #colors=[p.Color("red"),p.Color("black")]
    for r in range(DIMENSION_HEIGHT):
        for c in range(DIMENSION_WIDTH):
            if gs.board[r][c]!="R":
                color= colors[((r+c)%2)]
            else:
                color=p.Color("red")
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE_HEIGHT,r*SQ_SIZE_WIDTH,SQ_SIZE_HEIGHT,SQ_SIZE_WIDTH))

def drawPieces(screen,board):
    for r in range(DIMENSION_HEIGHT):
        for c in range(DIMENSION_WIDTH):
            piece=board[r][c]
            if piece != "--" and piece != "R":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE_HEIGHT,r*SQ_SIZE_WIDTH,SQ_SIZE_HEIGHT,SQ_SIZE_WIDTH))

if __name__=="__main__":
    main()