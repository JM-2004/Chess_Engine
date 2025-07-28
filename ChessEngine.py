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
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins =[]
        self.checks = []
        self.enPassantPossible = ()
        self.currentCastlingRights = CastleRights(True, True, True, True) # White King Side, White Queen Side, Black King Side, Black Queen Side
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wKS, self.currentCastlingRights.wQS,
                                             self.currentCastlingRights.bKS, self.currentCastlingRights.bQS)]

    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movesLog.append(move)
        self.whiteToMove = not self.whiteToMove # switch turns
        # Update king's position
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        # If pawn moves twice, next move can be en passant
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.endRow + move.startRow)//2, move.endCol)
        else:
            self.enPassantPossible = ()
        # If en passant is captured, remove the pawn
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"
        # If pawn promotes, replace it with the promoted piece
        if move.pawnPromotion:
            promotedPiece = input("Enter the piece to promote to (Q, R, B, N): ")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece
        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # Kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--"
            else: # Queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"
        # Update castling rights
        self.updateCastlingRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wKS, self.currentCastlingRights.wQS,
                                             self.currentCastlingRights.bKS, self.currentCastlingRights.bQS))



    def undoMove(self):
        if len(self.movesLog)!=0 :
            move = self.movesLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch turns back
            # Update king's position
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            # Undo en passant
            if move.enPassant:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)
            # Undo 2 sqaure pawn advance should allow en passant again
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()
            # Undo castling rights
            self.castleRightsLog.pop()
            self.currentCastlingRights = self.castleRightsLog[-1]
            ##############################################################################
            # Undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: # Kingside castle
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else: # Queenside castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

    def updateCastlingRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wKS = False
            self.currentCastlingRights.wQS = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bKS = False
            self.currentCastlingRights.bQS = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7 and move.startCol == 0:
                self.currentCastlingRights.wQS = False
            elif move.startRow == 7 and move.startCol == 7:
                self.currentCastlingRights.wKS = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0 and move.startCol == 0:
                self.currentCastlingRights.bQS = False
            elif move.startRow == 0 and move.startCol == 7:
                self.currentCastlingRights.bKS = False

    #All moves with check
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
            self.getCastleMoves(kingRow, kingCol, moves, 'w')
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
            self.getCastleMoves(kingRow, kingCol, moves, 'b')
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: # Double check
                self.getKingMoves(kingRow, kingCol, moves)
        else: # Not in check
            moves = self.getAllPossibleMoves()
        if len(moves) == 0: # Checkmate or Stalemate
            if self.isInCheck():
                self.checkMate = True
                print("Checkmate")
            else:
                self.staleMate = True
                print("Stalemate")
        else: # For undo moves
            self.checkMate = False
            self.staleMate = False
        return moves
    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for j in range(len(directions)):
            d = directions[j]
            possiblePins = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePins == ():
                            possiblePins = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possible checks
                        # Orthogonally away from king and piece is Rook
                        # Diagonally away from king and piece is Bishop
                        # 1 square away from king and piece is pawn
                        # Any direction and piece is King
                        if(0<=j<=3 and type=='R') or (4<=j<=7 and type=='B') or \
                            (i==1 and type=='P' and((enemyColor=='w' and 6<=j<=7) or \
                            (enemyColor=='b' and 4<=j<=5))) or (type=='Q') or \
                            (i==1 and type=='K'):
                                if possiblePins == ():
                                    inCheck = True
                                    checks.append((endRow, endCol, d[0], d[1]))
                                    break
                                else:
                                    pins.append(possiblePins)
                                    break
                        else:
                            break
                else:
                    break
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
    def isInCheck(self):
        if self.whiteToMove:
            return self.isSquareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.isSquareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])      
    def isSquareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # Switch to opponent's turn
        opponentMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # Switch back to current player's turn
        for move in opponentMoves:
            if move.endRow == r and move.endCol == c: # Square is under attack
                return True
        return False
    
    def squareUnderAttack(self, r, c, ally_color):
        enemy_color = 'w' if ally_color == 'b' else 'b'
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        break
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1]
                        # 5 possible checks
                        # Orthogonally away from king and piece is Rook
                        # Diagonally away from king and piece is Bishop
                        # 1 square away from king and piece is pawn
                        # Any direction and piece is King
                        if(0<=j<=3 and type=='R') or (4<=j<=7 and type=='B') or \
                            (i==1 and type=='P' and((enemy_color=='w' and 6<=j<=7) or \
                            (enemy_color=='b' and 4<=j<=5))) or (type=='Q') or \
                            (i==1 and type=='K'):
                            return True
                        else:
                            break
                else:
                    break
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemy_color and endPiece[1] == 'N':
                    return True
        return False

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
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
        pawnPromotion = False

        if self.board[r + moveAmount][c] == "--":
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:
                    pawnPromotion = True
                moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion=pawnPromotion))
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--":
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))
        if c - 1 >= 0:
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c-1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, enPassant=True))

        if c + 1 <= 7:
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c+1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, enPassant=True))

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if (self.board[r][c][1]!= 'Q'): # Cant remove queen from pin on rook moves, only remove for bishop moves
                    self.pins.remove(self.pins[i])
                break
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0]*i
                end_col = c + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
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
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),(1, -2), (1, 2), (2, -1), (2, 1)]
        ally_color = 'w' if self.whiteToMove else 'b'
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piecePinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--" or end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemy_color = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0]*i
                end_col = c + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
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
        rowMoves = (-1,-1,-1,0,0,1,1,1)
        colMoves = (-1,0,1,-1,1,-1,0,1)
        ally_color = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            end_row = r + rowMoves[i]
            end_col = c + colMoves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0]!=ally_color:
                    if ally_color == 'w':
                        self.whiteKingLocation = (end_row, end_col)
                    else:
                        self.blackKingLocation = (end_row, end_col)
                    inChecks, pins, checks = self.checkForPinsAndChecks()
                    if not inChecks:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    if ally_color == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        self.getCastleMoves(r, c, moves, ally_color)

    def getCastleMoves(self, r, c, moves, ally_color):
        inCheck = self.squareUnderAttack(r, c, ally_color)
        if inCheck:
            return
        if (self.whiteToMove and self.currentCastlingRights.wKS) or (not self.whiteToMove and self.currentCastlingRights.bKS):
            self.getKingsideCastleMoves(r, c, moves, ally_color)
        if (self.whiteToMove and self.currentCastlingRights.wQS) or (not self.whiteToMove and self.currentCastlingRights.bQS):
            self.getQueensideCastleMoves(r, c, moves, ally_color)
        
    def getKingsideCastleMoves(self, r, c, moves, ally_color):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c+1, ally_color) and not self.squareUnderAttack(r, c+2, ally_color):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves, ally_color):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r, c-1, ally_color) and not self.squareUnderAttack(r, c-2, ally_color):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

class CastleRights():
    def __init__(self, wKS, wQS, bKS, bQS):
        self.wKS = wKS  # White King Side
        self.wQS = wQS  # White Queen Side
        self.bKS = bKS  # Black King Side
        self.bQS = bQS  # Black Queen Side

class Move():
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board, enPassant=False, pawnPromotion=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.enPassant = enPassant
        self.pawnPromotion = pawnPromotion
        if enPassant:
            self.pieceCaptured = "bP" if self.pieceMoved == "wP" else "wP"
        self.isCastleMove = isCastleMove
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