import copy

class GameState():
    def __init__(self,nr_rows,nr_columns):

        self.nr_rows=nr_rows
        self.nr_columns=nr_columns
        self.board=[]
        self.board_secundar=[]

        self.moveFunctions={'p':self.getPawnMoves,'R':self.getRookMoves,'B':self.getBishopMoves,'N':self.getKnightMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}

        for i in range(nr_columns):
            self.board_secundar.append("--")

        for j in range(nr_rows):
            self.board.append(copy.deepcopy(self.board_secundar))

        # self.board=[
        #     ["bR","bN","bB","bQ","bK","bB","bN","bR"],
        #     ["bp","bp","bp","bp","bp","bp","bp","bp"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["--","--","--","--","--","--","--","--"],
        #     ["wp","wp","wp","wp","wp","wp","wp","wp"],
        #     ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        # ]

        self.board[0][(nr_columns//2)]="bK"

        if(nr_columns>1):
            self.board[nr_rows-1][(nr_columns//2)]="wK"

            for i in range(nr_columns):
                self.board[1][i]="bp"

            for i in range(nr_columns):
                self.board[nr_rows-2][i]="wp"

            if(nr_rows>2):
                self.board[0][0]="bR"
                self.board[0][nr_columns-1]="bR"

                self.board[nr_rows-1][0]="wR"
                self.board[nr_rows-1][nr_columns-1]="wR"

                if(nr_rows>3):
                    self.board[0][nr_columns//2-1]="bQ"
                    self.board[nr_rows-1][nr_columns//2-1]="wQ"

                if(nr_rows>4):
                    self.board[0][nr_columns//2+1]="bB"
                    self.board[nr_rows-1][nr_columns//2+1]="wB"

                if(nr_rows>5):
                    
                    self.board[0][nr_columns//2-2]="bB"
                    self.board[nr_rows-1][nr_columns//2-2]="wB"

                if(nr_rows>6):
                    self.board[0][nr_columns//2+2]="bN"
                    self.board[nr_rows-1][nr_columns//2+2]="wN"

                if(nr_rows>7):
                    
                    self.board[0][nr_columns//2-3]="bN"
                    self.board[nr_rows-1][nr_columns//2-3]="wN"
                    
        self.whiteToMove=True
        self.moveLog=[]

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] ="--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove= not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move=self.moveLog.pop()
            self.board[move.startRow][move.startCol]= move.pieceMoved
            self.board[move.endRow][move.endCol]= move.pieceCaptured
            self.whiteToMove= not self.whiteToMove
            
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn=="w" and self.whiteToMove) or (turn=="b" and not self.whiteToMove):
                    piece=self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)

                   
        return moves

    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove:
            if self.board[r-1][c]== "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r ==self.nr_rows-2 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c),(r-2,c),self.board))
                if c-1>=0:
                    if self.board[r-1][c-1][0]=="b":
                        moves.append(Move((r,c),(r-1,c-1),self.board))
                if c+1 <= self.nr_columns-1:
                    if self.board[r-1][c+1][0]== "b":
                        moves.append(Move((r,c),(r-1,c+1),self.board))
        
        else:
            if self.board[r+1][c]=="--":
                moves.append(Move((r,c),(r+1,c),self.board))
            if r ==1 and self.board[r+2][c]=="--":
                moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0:
                if self.board[r+1][c-1][0]=="w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<=len(self.board[0])-1:
                if self.board[r+1][c+1][0]=="w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))


    def getRookMoves(self,r,c,moves):
        directions_horizontal = ((0,-1),(0,1))
        directions_vertical = ((-1,0),(1,0))

        enemyColor = "b" if self.whiteToMove  else "w"
        for d in directions_horizontal:
                for i in range(1,self.nr_columns):
                    endRow=r +d[0] *i
                    endCol=c+d[1] *i
                    if 0<=endRow<self.nr_rows and 0<=endCol<self.nr_columns:
                        endPiece=self.board[endRow][endCol]
                        if endPiece=="--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                    else:
                        break

        for d in directions_vertical:
                for i in range(1,self.nr_rows):
                    endRow=r +d[0] *i
                    endCol=c+d[1] *i
                    if 0<=endRow<self.nr_rows and 0<=endCol<self.nr_columns:
                        endPiece=self.board[endRow][endCol]
                        if endPiece=="--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                    else:
                        break

                



    def getBishopMoves(self,r,c,moves):
        pass

    def getKnightMoves(self,r,c,moves):
        knightMoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whiteToMove  else "b"
        for m in knightMoves:
            endRow=r+m[0]
            endCol=c+m[1]
            if 0<=endRow < self.nr_rows and 0<=endCol<self.nr_columns:
                endPiece =self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))


    def getQueenMoves(self,r,c,moves):
        pass
    
    def getKingMoves(self,r,c,moves):
        pass

class Move():

    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}

    rowsToRanks={v:k for k,v in ranksToRows.items()}

    filesToCols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}

    colsToFiles={v:k for k, v in filesToCols.items()}

    def __init__(self,startSq,endSq, board):
        self.startRow=startSq[0]
        self.startCol =startSq[1]
        self.endRow =endSq[0]
        self.endCol =endSq[1]
        self.pieceMoved= board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID=(self.startCol+1)*1000+(8-self.startRow)*100+(self.endCol+1)*10 +(8-self.endRow)
        print(self.moveID)

    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID==other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        #return self.colsToFiles[c]+ self.rowsToRanks[r]
        return (str(c+1)+str(8-r))