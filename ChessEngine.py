# Responsible for storing all information about current state of chess game and determining valid moves
import numpy as np

class GameState():
    def __init__(self):
        self.board=np.array([
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
            ])
        self.whiteToMove = True
        self.movesLog=[]
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movesLog.append(move)
        self.whiteToMove = not self.whiteToMove # switch turns
    
    def undoMove(self):
        if len(self.movesLog)!=0 :
            move = self.movesLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch turns back

    #All moves with check
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    # All moves without check
    def getAllPossibleMoves(self):
        moves=[]
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != "--":
                    if (piece[0] == 'w' and self.whiteToMove) or (piece[0] == 'b' and not self.whiteToMove):
                        if(piece[1] == 'P'):
                            self.getPawnMoves(r, c, moves)
                        elif(piece[1] == 'R'):
                            self.getRookMoves(r, c, moves)
                        elif(piece[1] == 'N'):
                            self.getKnightMoves(r, c, moves)
                        elif(piece[1] == 'B'):
                            self.getBishopMoves(r, c, moves)
                        elif(piece[1] == 'Q'):
                            self.getQueenMoves(r, c, moves)
                        elif(piece[1] == 'K'):
                            self.getKingMoves(r, c, moves)
        return moves 
                          
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # White pawns moves
            if r-1 >= 0 and self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1>=0 :
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1<=7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else: # Black pawns moves
            if r+1 <= 7 and self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))


    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0]*i
                end_col = c + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else: # Friendly piece encountered
                        break
                else: # Off the board
                    break
    def getKnightMoves(self, r, c, moves):
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),(1, -2), (1, 2), (2, -1), (2, 1)]
        ally_color = 'w' if self.whiteToMove else 'b'
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))
    def getBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0]*i
                end_col = c + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else: # Friendly piece encountered
                        break
                else: # Off the board
                    break
    def getQueenMoves(self, r, c, moves):   
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    def getKingMoves(self, r, c, moves):
        king_moves = [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1), (1, 0), (1, 1)]
        ally_color = 'w' if self.whiteToMove else 'b'
        for m in king_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

class Move():
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    #def getChessNotation(self): # Very basic chess notation. Can be improved later
    #    return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    #Overriding equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        piece = self.pieceMoved[1] if self.pieceMoved[1] != 'P' else ''
        capture = 'x' if self.pieceCaptured != "--" else ''
        
        # For pawns, include file on capture (e.g., exd5)
        if self.pieceMoved[1] == 'P' and capture:
            piece = self.colsToFiles[self.startCol]  # pawn file
        
        return piece + capture + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]