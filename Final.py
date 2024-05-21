import pygame as p
import Chess as ChessEngine

width = height = 512
dimension = 8
sq_size = height // dimension
max_fps = 15
images = {}

def loadImages():
    pieces = ["wB", "bR"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("assets/" + piece + ".png"), (sq_size, sq_size))

def main():
    p.init()
    gs = ChessEngine.GameState()
    rookPos= (int(input("Ingresa la fila inicial de la Torre:"))-1, int(input("Ingresa la columna inicial de la Torre:"))-1)
    bishopPos= (int(input("Ingresa la fila inicial del Alfíl:"))-1, int(input("Ingresa la columna inicial del Alfíl:"))-1)
    gs.setPieces(rookPos, bishopPos)
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    GameOver = False
    loadImages()
    running = True
    sqSelected = ()
    playerCLicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not GameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//sq_size
                    row = location[1]//sq_size
                    if sqSelected == (row,col):
                        sqSelected = ()
                        playerCLicks = []
                    else:
                        sqSelected = (row,col)
                        playerCLicks.append(sqSelected)
                    if len(playerCLicks) == 2:
                        move = ChessEngine.Move(playerCLicks[0],playerCLicks[1], gs.board)
                        print(move.getChessNotation())
                        if move in validMoves:
                            moveMade = True
                            animate = True
                            gs.makeMove(move)
                            sqSelected = ()
                            playerCLicks = []
                        else:
                            playerCLicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerCLicks = []
                    moveMade = False
                    animate = False
                    GameOver = False
        if moveMade:
            if animate:
                animatedMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            w, b = gs.checkPieces()
            if w < 1 or b < 1:
                GameOver = True

        drawGameState(screen, gs, validMoves, sqSelected)

        if GameOver:
            w, b = gs.checkPieces()
            if w < 1:
                drawText(screen, "Gana la Torre")
            elif b < 1:  
                drawText(screen, "Gana el Alfíl")
        
        clock.tick(max_fps)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c*sq_size, r*sq_size))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sq_size, move.endRow*sq_size))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def animatedMove(move, screen, board, clock):
    global colors
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 4
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*sq_size, move.endRow*sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            screen.blit(images[move.pieceCaptured], endSquare)
        screen.blit(images[move.pieceMoved], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color("Gray"))
    textLocation = p.Rect(0,0,width, height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()