# Responsible for handling user input and diplay current gameState object


import pygame as p
import ChessEngine

WIDTH = 512
HEIGHT = 512
DIMENSION = 8 # 8x8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}

# Initialize global dictionary of Images. It will load only once hence saving memory
def loadImages():
    pieces=['wP','bP','wK','bK','wQ','bQ','wB','bB','wN','bN','wR','bR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess_pieces/"+piece+".png"), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    moveMade = False
    animate = False
    validMoves = gs.getValidMoves()
    loadImages()
    running=True
    sqSelected = () # tuple: (row, col) of the square selected by the user
    playerClicks = []  # Keep track of player clicks
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    row = location[1] // SQUARE_SIZE
                    col = location[0] // SQUARE_SIZE
                    if sqSelected == (row, col): # User clicked the same square again
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # append both 1st and 2nd clicks
                    if len(playerClicks) == 2:
                        move=ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # Undo the last move
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r: # Reset the game
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        if(moveMade):
            if animate:
                animateMove(gs.movesLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        if gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # Highlight only if the selected square has a piece of the current player
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # Set transparency
            s.fill(p.Color("#baca44"))
            screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
            s.fill(p.Color("#769656"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

# Top left square is always light
def drawBoard(screen):
    global colors
    colors = [p.Color("#F0D9B5"), p.Color("#B58863")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def animateMove(move, screen, board, clock):
    global colors
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move. startCol
    frames = 2
    frameCount = (abs(dR) + abs(dC)) * frames
    for frame in range(frameCount + 1):
        r,c = ((move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece from the end square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare =p.Rect(move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - textObject.get_width() // 2, HEIGHT // 2 - textObject.get_height() // 2)

    # Create semi-transparent background surface
    bg_surface = p.Surface((textObject.get_width() + 20, textObject.get_height() + 10))
    bg_surface.set_alpha(180)  # Transparency (0=fully transparent, 255=solid)
    bg_surface.fill((240, 240, 240))  # Light gray background

    screen.blit(bg_surface, (textLocation.x - 10, textLocation.y - 5))
    screen.blit(textObject, textLocation)
    p.display.flip()

if __name__ == "__main__":
    main()