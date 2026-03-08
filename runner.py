import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None          # X or O
difficulty = None    # 'easy', 'medium', 'hard'
board = ttt.initial_state()
ai_turn = False
ai_move = None       # store the AI's chosen move

while True:

    # Handle events first
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # ----- Player selection -----
            if user is None:
                playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
                playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
                if playXButton.collidepoint(x, y):
                    user = ttt.X
                elif playOButton.collidepoint(x, y):
                    user = ttt.O

            # ----- Difficulty selection -----
            elif difficulty is None:
                easyButton = pygame.Rect((width / 8), (height / 2) - 40, width / 4, 50)
                mediumButton = pygame.Rect(3 * (width / 8), (height / 2) - 40, width / 4, 50)
                hardButton = pygame.Rect(5 * (width / 8), (height / 2) - 40, width / 4, 50)
                if easyButton.collidepoint(x, y):
                    difficulty = 'easy'
                elif mediumButton.collidepoint(x, y):
                    difficulty = 'medium'
                elif hardButton.collidepoint(x, y):
                    difficulty = 'hard'

            # ----- Game board (user move) -----
            elif user is not None and difficulty is not None and not ttt.terminal(board) and ttt.player(board) == user:
                # Check tile clicks
                tile_size = 80
                tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
                for i in range(3):
                    for j in range(3):
                        rect = pygame.Rect(
                            tile_origin[0] + j * tile_size,
                            tile_origin[1] + i * tile_size,
                            tile_size, tile_size
                        )
                        if rect.collidepoint(x, y) and board[i][j] == ttt.EMPTY:
                            board = ttt.result(board, (i, j))
                            # After user move, reset AI turn flag so AI can think again
                            ai_turn = False
                            ai_move = None

            # ----- Play Again button -----
            if ttt.terminal(board):
                againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
                if againButton.collidepoint(x, y):
                    user = None
                    difficulty = None
                    board = ttt.initial_state()
                    ai_turn = False
                    ai_move = None

    # Drawing section
    screen.fill(black)

    # Player selection screen
    if user is None:
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

    # Difficulty selection screen
    elif difficulty is None:
        title = largeFont.render("Choose Difficulty", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        easyButton = pygame.Rect((width / 8), (height / 2) - 40, width / 4, 50)
        easy = mediumFont.render("Easy", True, black)
        easyRect = easy.get_rect()
        easyRect.center = easyButton.center
        pygame.draw.rect(screen, white, easyButton)
        screen.blit(easy, easyRect)

        mediumButton = pygame.Rect(3 * (width / 8), (height / 2) - 40, width / 4, 50)
        med = mediumFont.render("Medium", True, black)
        medRect = med.get_rect()
        medRect.center = mediumButton.center
        pygame.draw.rect(screen, white, mediumButton)
        screen.blit(med, medRect)

        hardButton = pygame.Rect(5 * (width / 8), (height / 2) - 40, width / 4, 50)
        hard = mediumFont.render("Hard", True, black)
        hardRect = hard.get_rect()
        hardRect.center = hardButton.center
        pygame.draw.rect(screen, white, hardButton)
        screen.blit(hard, hardRect)

    # Game board screen
    else:
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size), height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # ----- AI move calculation (only once per turn) -----
        if user != player and not game_over and ai_move is None:
            ai_move = ttt.get_ai_move(board, difficulty)

        # Title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = "Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Your Turn ({user})"
        else:
            # Display the stored AI move
            if ai_move is not None:
                title = f"AI thinking... Best move: {ai_move}"
            else:
                title = "AI thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # AI move execution
        if user != player and not game_over:
            if ai_turn:
                time.sleep(1)
                # Use the stored ai_move (should not be None here)
                if ai_move is not None:
                    board = ttt.result(board, ai_move)
                ai_turn = False
                ai_move = None   # Clear for next AI turn
            else:
                ai_turn = True

        # Play Again button
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)

    pygame.display.flip()