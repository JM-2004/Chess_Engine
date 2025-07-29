# Find moves for AI

import random

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
DEPTH = 2

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
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceValue[square[1]]
            elif square[0] == 'b':
                score -= pieceValue[square[1]]
    return score

