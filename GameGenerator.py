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
            if e.type==p.QUIT:
                running =False
            elif e.type==p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col= location[0]//SQ_SIZE_HEIGHT
                row= location[1]//SQ_SIZE_WIDTH
                if sqSelected == (row, col):
                    sqSelected=()
                    playerClicks=[]
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks)==2:
                    move= ce.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade=True
                    sqSelected=()
                    playerClicks=[]    

                    # gs.makeMove(move)

                

            elif e.type== p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

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