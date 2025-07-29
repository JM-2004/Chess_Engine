# Find moves for AI

import random
import numpy as np

pieceValue = {
    'P': 1,  # Pawn
    'R': 5,  # Rook
    'N': 3,  # Knight
    'B': 3,  # Bishop
    'Q': 9,  # Queen
    'K': 0   # King (not used in scoring)
}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

knightScores = np.array([[1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1]])

bishopScores = np.array([[4,3,2,1,1,2,3,4],
                [3,4,3,2,2,3,4,3],
                [2,3,4,3,3,4,3,2],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [2,3,4,3,3,4,3,2],
                [3,4,3,2,2,3,4,3],
                [4,3,2,1,1,2,3,4]])

queenScores = np.array([[1,1,1,3,1,1,1,1],
               [1,2,3,3,3,1,1,1],
               [1,4,3,3,3,4,2,1],
               [1,2,3,3,3,2,2,1],
               [1,2,3,3,3,2,2,1],
               [1,4,3,3,3,4,2,1],
               [1,2,3,3,3,1,1,1],
               [1,1,1,3,1,1,1,1]])

rookScores = np.array([[4,3,4,4,4,4,3,4],
              [4,4,4,4,4,4,4,4],
              [1,1,2,3,3,2,1,1],
              [1,2,3,4,4,3,2,1],
              [1,2,3,4,4,3,2,1],
              [1,1,2,3,3,2,1,1],
              [4,4,4,4,4,4,4,4],
              [4,3,4,4,4,4,3,4]])

whitePawnScores = np.array([[8,8,8,8,8,8,8,8],
                   [8,8,8,8,8,8,8,8],
                   [5,6,6,7,7,6,6,5],
                   [2,3,3,5,5,3,3,2],
                   [1,2,3,4,4,3,2,1],
                   [1,1,2,3,3,2,1,1],
                   [1,1,1,0,0,1,1,1],
                   [0,0,0,0,0,0,0,0]])

blackPawnScores = np.array([[0,0,0,0,0,0,0,0],
                   [1,1,1,0,0,1,1,1],
                   [1,1,2,3,3,2,1,1],
                   [1,2,3,4,4,3,2,1],
                   [2,3,3,5,5,3,3,2],
                   [5,6,6,7,7,6,6,5],
                   [8,8,8,8,8,8,8,8],
                   [8,8,8,8,8,8,8,8]])

piecePositionScores = {'N': knightScores, 
                       'B': bishopScores, 
                       'Q': queenScores, 
                       'R': rookScores, 
                       'wP': whitePawnScores,
                       'bP': blackPawnScores}

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

# Helper method to make first recursive call
def findBestMove(gs, validMoves):
    global nextMove,counter
    counter = 0
    nextMove = None
    random.shuffle(validMoves)
    #findBestMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE,1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

def findBestMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove,counter
    counter += 1
    if depth == 0:
        return scoreMaterial(gs)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findBestMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findBestMoveMinMax(gs, nextMoves, depth -1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove,counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreMaterial(gs)
    
    # Move ordering
    validMoves.sort(key=scoreMove, reverse=True)
    
    #move order - Implement later
    maxScore = -CHECKMATE
    for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
    return maxScore

# positive score is good for white and negative for black
def scoreMaterial(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE #Black wins
        else:
            return CHECKMATE # White wins
    if gs.staleMate:
        return STALEMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                if square[1]!='K':
                    if square[1] == 'P':
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                if square[0] == 'w':
                    score += pieceValue[square[1]] + piecePositionScore*0.1
                elif square[0] == 'b':
                    score -= pieceValue[square[1]] + piecePositionScore*0.1
    return score


def scoreMove(move):
    captureScore = 0
    if move.pieceCaptured != "--":
        captureScore += 10 * pieceValue[move.pieceCaptured[1]] - pieceValue[move.pieceMoved[1]]
    promotionBonus = 9 if move.pawnPromotion else 0
    castleBonus = 2 if move.isCastleMove else 0
    return captureScore + promotionBonus + castleBonus

