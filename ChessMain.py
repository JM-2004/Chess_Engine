# Responsible for handling user input and diplay current gameState object


import pygame as p
import ChessEngine

WIDTH = 496
HEIGHT = 496
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
    loadImages()
    running=True
    sqSelected = () # tuple: (row, col) of the square selected by the user
    playerClicks = []  # Keep track of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
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
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

# Top left square is always light
def drawBoard(screen):
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


if __name__ == "__main__":
    main()