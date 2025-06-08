import pygame
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BOARD_WIDTH = 9
BOARD_HEIGHT = 10
CELL_SIZE = 60
BOARD_MARGIN_X = (SCREEN_WIDTH - (BOARD_WIDTH - 1) * CELL_SIZE) // 2
BOARD_MARGIN_Y = (SCREEN_HEIGHT - (BOARD_HEIGHT - 1) * CELL_SIZE) // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (165, 42, 42)
LIGHT_BROWN = (222, 184, 135)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chinese Chess (Xiangqi)')

# Piece values for AI evaluation
PIECE_VALUES = {
    'r_general': 1000,
    'r_advisor': 20,
    'r_elephant': 20,
    'r_horse': 40,
    'r_chariot': 90,
    'r_cannon': 45,
    'r_soldier': 10,
    'b_general': 1000,
    'b_advisor': 20,
    'b_elephant': 20,
    'b_horse': 40,
    'b_chariot': 90,
    'b_cannon': 45,
    'b_soldier': 10
}

class Piece:
    def __init__(self, piece_type, color, x, y):
        self.piece_type = piece_type
        self.color = color  # 'r' for red, 'b' for black
        self.x = x
        self.y = y
        self.selected = False
        self.id = f"{color}_{piece_type}"
    
    def draw(self, surface):
        # Calculate position
        pos_x = BOARD_MARGIN_X + self.x * CELL_SIZE
        pos_y = BOARD_MARGIN_Y + self.y * CELL_SIZE        
        # Draw piece circle
        circle_color = RED if self.color == 'r' else BLACK
        pygame.draw.circle(surface, circle_color, (pos_x, pos_y), CELL_SIZE // 2 - 5)
        pygame.draw.circle(surface, WHITE, (pos_x, pos_y), CELL_SIZE // 2 - 8)
        
        # Draw piece text
        font = pygame.font.SysFont('Arial', 20, bold=True)
        text_color = RED if self.color == 'r' else BLACK
        
        # Map piece type to display text
        piece_text = {
            'general': 'G',
            'advisor': 'A',
            'elephant': 'E',
            'horse': 'H',
            'chariot': 'R',
            'cannon': 'C',
            'soldier': 'S'
        }
        
        text = font.render(piece_text[self.piece_type], True, text_color)
        text_rect = text.get_rect(center=(pos_x, pos_y))
        surface.blit(text, text_rect)
        
        # Highlight if selected
        if self.selected:
            pygame.draw.circle(surface, YELLOW, (pos_x, pos_y), CELL_SIZE // 2, 2)

class Board:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.pieces = []
        self.selected_piece = None
        self.player_color = 'r'  # Default player is red
        self.current_turn = 'r'  # Red goes first
        
        # Initialize pieces
        self.initialize_pieces()
    
    def initialize_pieces(self):
        # Red pieces (bottom)
        # Chariot (Rook)
        self.pieces.append(Piece('chariot', 'r', 0, 9))
        self.pieces.append(Piece('chariot', 'r', 8, 9))
        
        # Horse (Knight)
        self.pieces.append(Piece('horse', 'r', 1, 9))
        self.pieces.append(Piece('horse', 'r', 7, 9))
        
        # Elephant
        self.pieces.append(Piece('elephant', 'r', 2, 9))
        self.pieces.append(Piece('elephant', 'r', 6, 9))
        
        # Advisor
        self.pieces.append(Piece('advisor', 'r', 3, 9))
        self.pieces.append(Piece('advisor', 'r', 5, 9))
        
        # General (King)
        self.pieces.append(Piece('general', 'r', 4, 9))
        
        # Cannon
        self.pieces.append(Piece('cannon', 'r', 1, 7))
        self.pieces.append(Piece('cannon', 'r', 7, 7))
        
        # Soldier (Pawn)
        for i in range(5):
            self.pieces.append(Piece('soldier', 'r', i*2, 6))
        
        # Black pieces (top)
        # Chariot (Rook)
        self.pieces.append(Piece('chariot', 'b', 0, 0))
        self.pieces.append(Piece('chariot', 'b', 8, 0))
        
        # Horse (Knight)
        self.pieces.append(Piece('horse', 'b', 1, 0))
        self.pieces.append(Piece('horse', 'b', 7, 0))
        
        # Elephant
        self.pieces.append(Piece('elephant', 'b', 2, 0))
        self.pieces.append(Piece('elephant', 'b', 6, 0))
        
        # Advisor
        self.pieces.append(Piece('advisor', 'b', 3, 0))
        self.pieces.append(Piece('advisor', 'b', 5, 0))
        
        # General (King)
        self.pieces.append(Piece('general', 'b', 4, 0))
        
        # Cannon
        self.pieces.append(Piece('cannon', 'b', 1, 2))
        self.pieces.append(Piece('cannon', 'b', 7, 2))
        
        # Soldier (Pawn)
        for i in range(5):
            self.pieces.append(Piece('soldier', 'b', i*2, 3))
    
    def draw(self, surface):
        # Draw board background
        pygame.draw.rect(        
        surface,
        LIGHT_BROWN,

            (
                BOARD_MARGIN_X,
                BOARD_MARGIN_Y,
                (BOARD_WIDTH - 1) * CELL_SIZE,
                (BOARD_HEIGHT - 1) * CELL_SIZE,
            ),
        )
        for i in range(BOARD_WIDTH):
            pygame.draw.line(surface, BLACK, 
                            (BOARD_MARGIN_X + i * CELL_SIZE, BOARD_MARGIN_Y),
                            (
                                BOARD_MARGIN_X + i * CELL_SIZE,
                                BOARD_MARGIN_Y + (BOARD_HEIGHT - 1) * CELL_SIZE,
                            ))

        for i in range(BOARD_HEIGHT):
            pygame.draw.line(surface, BLACK,
                            (BOARD_MARGIN_X, BOARD_MARGIN_Y + i * CELL_SIZE),
                            (
                                BOARD_MARGIN_X + (BOARD_WIDTH - 1) * CELL_SIZE,
                                 BOARD_MARGIN_Y + i * CELL_SIZE,
                            ))
        
        # Draw palace diagonals
        # Top palace
        pygame.draw.line(surface, BLACK, 
                        (BOARD_MARGIN_X + 3 * CELL_SIZE, BOARD_MARGIN_Y),
                        (BOARD_MARGIN_X + 5 * CELL_SIZE, BOARD_MARGIN_Y + 2 * CELL_SIZE))
        pygame.draw.line(surface, BLACK, 
                        (BOARD_MARGIN_X + 5 * CELL_SIZE, BOARD_MARGIN_Y),
                        (BOARD_MARGIN_X + 3 * CELL_SIZE, BOARD_MARGIN_Y + 2 * CELL_SIZE))
        
        # Bottom palace
        pygame.draw.line(surface, BLACK, 
                        (BOARD_MARGIN_X + 3 * CELL_SIZE, BOARD_MARGIN_Y + 7 * CELL_SIZE),
                        (BOARD_MARGIN_X + 5 * CELL_SIZE, BOARD_MARGIN_Y + 9 * CELL_SIZE))
        pygame.draw.line(surface, BLACK, 
                        (BOARD_MARGIN_X + 5 * CELL_SIZE, BOARD_MARGIN_Y + 7 * CELL_SIZE),
                        (BOARD_MARGIN_X + 3 * CELL_SIZE, BOARD_MARGIN_Y + 9 * CELL_SIZE))
        
        # Draw river text
        font = pygame.font.SysFont('Arial', 30)
        text = font.render("River", True, BLUE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, BOARD_MARGIN_Y + 4.5 * CELL_SIZE))
        surface.blit(text, text_rect)
        
        # Draw pieces
        for piece in self.pieces:
            piece.draw(surface)
        
        # Draw legal moves for selected piece
        if self.selected_piece:
            legal_moves = self.get_legal_moves(self.selected_piece)
            for move in legal_moves:
                x, y = move
                pos_x = BOARD_MARGIN_X + x * CELL_SIZE
                pos_y = BOARD_MARGIN_Y + y * CELL_SIZE
                
                # Check if there's a piece at this position
                target_piece = self.get_piece_at(x, y)
                if target_piece:
                    # Highlight capture move
                    pygame.draw.circle(surface, RED, (pos_x, pos_y), CELL_SIZE // 4, 2)
                else:
                    # Highlight empty move
                    pygame.draw.circle(surface, GREEN, (pos_x, pos_y), CELL_SIZE // 4, 2)
        
        # Draw turn indicator
        turn_text = "Red's Turn" if self.current_turn == 'r' else "Black's Turn"
        turn_color = RED if self.current_turn == 'r' else BLACK
        font = pygame.font.SysFont('Arial', 24)
        text = font.render(turn_text, True, turn_color)
        surface.blit(text, (20, 20))
    
    def get_piece_at(self, x, y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None
    
    def is_in_check(self, color):
        # Find the general
        general = None
        for piece in self.pieces:
            if piece.piece_type == 'general' and piece.color == color:
                general = piece
                break
        
        if not general:
            return False
        
        # Check if any opponent piece can capture the general
        opponent_color = 'b' if color == 'r' else 'r'
        for piece in self.pieces:
            if piece.color == opponent_color:
                legal_moves = self.get_legal_moves(piece, check_check=False)
                if (general.x, general.y) in legal_moves:
                    return True
        
        # Check for "flying general" rule
        opponent_general = None
        for piece in self.pieces:
            if piece.piece_type == 'general' and piece.color != color:
                opponent_general = piece
                break
        
        if opponent_general and general.x == opponent_general.x:
            # Check if there are any pieces between the two generals
            min_y = min(general.y, opponent_general.y)
            max_y = max(general.y, opponent_general.y)
            has_piece_between = False
            
            for y in range(min_y + 1, max_y):
                if self.get_piece_at(general.x, y):
                    has_piece_between = True
                    break
            
            if not has_piece_between:
                return True
        
        return False
    
    def would_be_in_check(self, piece, new_x, new_y):
        # Save original position
        orig_x, orig_y = piece.x, piece.y
        
        # Save target piece if any
        target_piece = self.get_piece_at(new_x, new_y)
        if target_piece:
            self.pieces.remove(target_piece)
        
        # Move piece temporarily
        piece.x, piece.y = new_x, new_y
        
        # Check if the move would result in check
        in_check = self.is_in_check(piece.color)
        
        # Restore original position
        piece.x, piece.y = orig_x, orig_y
        
        # Restore target piece if any
        if target_piece:
            self.pieces.append(target_piece)
        
        return in_check
    
    def get_legal_moves(self, piece, check_check=True):
        legal_moves = []
        
        if piece.piece_type == 'general':
            legal_moves = self.get_general_moves(piece)
        elif piece.piece_type == 'advisor':
            legal_moves = self.get_advisor_moves(piece)
        elif piece.piece_type == 'elephant':
            legal_moves = self.get_elephant_moves(piece)
        elif piece.piece_type == 'horse':
            legal_moves = self.get_horse_moves(piece)
        elif piece.piece_type == 'chariot':
            legal_moves = self.get_chariot_moves(piece)
        elif piece.piece_type == 'cannon':
            legal_moves = self.get_cannon_moves(piece)
        elif piece.piece_type == 'soldier':
            legal_moves = self.get_soldier_moves(piece)
        
        # Filter out moves that would result in check
        if check_check:
            legal_moves = [(x, y) for x, y in legal_moves if not self.would_be_in_check(piece, x, y)]
        
        return legal_moves
    
    def get_general_moves(self, piece):
        moves = []
        # Define palace boundaries
        min_x, max_x = 3, 5
        if piece.color == 'b':
            min_y, max_y = 0, 2
        else:
            min_y, max_y = 7, 9
        
        # Check all adjacent positions (horizontal and vertical)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = piece.x + dx, piece.y + dy
            
            # Check if within palace
            if min_x <= new_x <= max_x and min_y <= new_y <= max_y:
                target_piece = self.get_piece_at(new_x, new_y)
                if not target_piece or target_piece.color != piece.color:
                    moves.append((new_x, new_y))
        # Flying general capture
        opponent_color = 'b' if piece.color == 'r' else 'r'
        opponent_general = None
        for p in self.pieces:
            if p.piece_type == 'general' and p.color == opponent_color:
                opponent_general = p
                break

        if opponent_general and piece.x == opponent_general.x:
            min_y_between = min(piece.y, opponent_general.y) + 1
            max_y_between = max(piece.y, opponent_general.y)
            has_piece_between = any(
                self.get_piece_at(piece.x, y)
                for y in range(min_y_between, max_y_between)
            )
            if not has_piece_between:
                moves.append((opponent_general.x, opponent_general.y))
        
        return moves
    
    def get_advisor_moves(self, piece):
        moves = []
        # Define palace boundaries
        min_x, max_x = 3, 5
        if piece.color == 'b':
            min_y, max_y = 0, 2
        else:
            min_y, max_y = 7, 9
        
        # Check all diagonal positions
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            new_x, new_y = piece.x + dx, piece.y + dy
            
            # Check if within palace
            if min_x <= new_x <= max_x and min_y <= new_y <= max_y:
                target_piece = self.get_piece_at(new_x, new_y)
                if not target_piece or target_piece.color != piece.color:
                    moves.append((new_x, new_y))
        
        return moves
    
    def get_elephant_moves(self, piece):
        moves = []
        # Elephants can't cross the river
        max_y = 4 if piece.color == 'r' else 9
        min_y = 0 if piece.color == 'b' else 5
        
        # Check all diagonal positions at distance 2
        for dx, dy in [(2, 2), (2, -2), (-2, 2), (-2, -2)]:
            new_x, new_y = piece.x + dx, piece.y + dy
            
            # Check if within board and on correct side of river
            if 0 <= new_x <= 8 and min_y <= new_y <= max_y:
                # Check if the elephant's eye is blocked
                eye_x, eye_y = piece.x + dx//2, piece.y + dy//2
                if not self.get_piece_at(eye_x, eye_y):
                    target_piece = self.get_piece_at(new_x, new_y)
                    if not target_piece or target_piece.color != piece.color:
                        moves.append((new_x, new_y))
        
        return moves
    
    def get_horse_moves(self, piece):
        moves = []
        
        # Horse moves in L shape: one step orthogonally then one step diagonally
        for dx1, dy1 in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            # Check if the horse's leg is blocked
            leg_x, leg_y = piece.x + dx1, piece.y + dy1
            if 0 <= leg_x <= 8 and 0 <= leg_y <= 9 and not self.get_piece_at(leg_x, leg_y):
                # Check the two diagonal moves from the leg position
                for dx2, dy2 in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    # Ensure it's an L shape (not a diagonal move)
                    if dx1 * dx2 + dy1 * dy2 == 0:
                        new_x, new_y = leg_x + dx2, leg_y + dy2
                        if 0 <= new_x <= 8 and 0 <= new_y <= 9:
                            target_piece = self.get_piece_at(new_x, new_y)
                            if not target_piece or target_piece.color != piece.color:
                                moves.append((new_x, new_y))
        
        return moves
    
    def get_chariot_moves(self, piece):
        moves = []
        
        # Check in all four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            for i in range(1, 10):  # Maximum board dimension
                new_x, new_y = piece.x + dx * i, piece.y + dy * i
                
                # Check if within board
                if not (0 <= new_x <= 8 and 0 <= new_y <= 9):
                    break
                
                target_piece = self.get_piece_at(new_x, new_y)
                if not target_piece:
                    moves.append((new_x, new_y))
                else:
                    if target_piece.color != piece.color:
                        moves.append((new_x, new_y))
                    break  # Can't move further in this direction
        
        return moves
    
    def get_cannon_moves(self, piece):
        moves = []
        
        # Check in all four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            has_platform = False
            
            for i in range(1, 10):  # Maximum board dimension
                new_x, new_y = piece.x + dx * i, piece.y + dy * i
                
                # Check if within board
                if not (0 <= new_x <= 8 and 0 <= new_y <= 9):
                    break
                
                target_piece = self.get_piece_at(new_x, new_y)
                
                if not has_platform:
                    if not target_piece:
                        moves.append((new_x, new_y))
                    else:
                        has_platform = True  # Found a platform to jump over
                else:
                    if target_piece:
                        if target_piece.color != piece.color:
                            moves.append((new_x, new_y))
                        break  # Can't move further in this direction
        
        return moves
    
    def get_soldier_moves(self, piece):
        moves = []
        
        # Determine forward direction based on color
        forward = -1 if piece.color == 'r' else 1
        
        # Forward move
        new_y = piece.y + forward
        if 0 <= new_y <= 9:
            target_piece = self.get_piece_at(piece.x, new_y)
            if not target_piece or target_piece.color != piece.color:
                moves.append((piece.x, new_y))

        # Check if soldier has crossed the river
        crossed_river = (
            (piece.color == 'r' and piece.y < 5)
            or (piece.color == 'b' and piece.y > 4)
        )

        if crossed_river:
            # Horizontal moves
            for dx in [-1, 1]:
                new_x = piece.x + dx
                if 0 <= new_x <= 8:
                    target_piece = self.get_piece_at(new_x, piece.y)
                    if not target_piece or target_piece.color != piece.color:
                        moves.append((new_x, piece.y))

        return moves

    def select_piece(self, x, y):
        piece = self.get_piece_at(x, y)

        # Deselect current piece if any
        if self.selected_piece:
            current = self.selected_piece
            current.selected = False
            self.selected_piece = None

            # If clicking on a different piece of the same color, select it
            if piece and piece.color == self.current_turn:
                self.selected_piece = piece
                piece.selected = True
            # If clicking on a legal move position, move the piece
            elif current.color == self.current_turn:
                legal_moves = self.get_legal_moves(current)
                if (x, y) in legal_moves:
                    self.move_piece(current, x, y)
                    return True  # Move was made
        # Select a new piece if it's the current player's turn
        elif piece and piece.color == self.current_turn:
            self.selected_piece = piece
            piece.selected = True

        return False  # No move was made

    def move_piece(self, piece, x, y):
        # Check if there's a piece at the target position
        target_piece = self.get_piece_at(x, y)
        if target_piece:
            self.pieces.remove(target_piece)

        # Move the piece
        piece.x, piece.y = x, y

        # Switch turns
        self.current_turn = 'b' if self.current_turn == 'r' else 'r'
    
    def is_game_over(self):
        # Check if any player's general is captured
        red_general_exists = False
        black_general_exists = False
        
        for piece in self.pieces:
            if piece.piece_type == 'general':
                if piece.color == 'r':
                    red_general_exists = True
                else:
                    black_general_exists = True
        
        if not red_general_exists:
            return 'b'  # Black wins
        if not black_general_exists:
            return 'r'  # Red wins
        
        # Game continues if both generals exist
        return None
    
    def evaluate_board(self):
        # Simple evaluation function for AI
        score = 0
        
        # Material value
        for piece in self.pieces:
            value = PIECE_VALUES[f"{piece.color}_{piece.piece_type}"]
            if piece.color == 'b':
                score -= value
            else:
                score += value
        
        # Mobility (number of legal moves)
        red_mobility = 0
        black_mobility = 0
        
        for piece in self.pieces:
            legal_moves = self.get_legal_moves(piece)
            if piece.color == 'r':
                red_mobility += len(legal_moves)
            else:
                black_mobility += len(legal_moves)
        
        score += (red_mobility - black_mobility) * 0.1
        
        # Check status
        if self.is_in_check('b'):
            score += 50
        if self.is_in_check('r'):
            score -= 50
        
        return score
    
    def ai_make_move(self):
        if self.current_turn != self.player_color:
            best_score = float('-inf') if self.current_turn == 'r' else float('inf')
            best_move = None
            
            # Get all possible moves for AI
            possible_moves = []
            for piece in self.pieces:
                if piece.color == self.current_turn:
                    legal_moves = self.get_legal_moves(piece)
                    for move in legal_moves:
                        possible_moves.append((piece, move[0], move[1]))
            
            # If AI has no legal moves, switch turns back to player
            if not possible_moves:
                # Switch turns to player
                self.current_turn = 'b' if self.current_turn == 'r' else 'r'
                return True
            
            # Randomize move order to add variety
            random.shuffle(possible_moves)
            
            for move in possible_moves:
                piece, new_x, new_y = move
                
                # Save original position
                orig_x, orig_y = piece.x, piece.y
                
                # Save target piece if any
                target_piece = self.get_piece_at(new_x, new_y)
                if target_piece:
                    self.pieces.remove(target_piece)
                
                # Make the move
                piece.x, piece.y = new_x, new_y
                
                # Switch turns temporarily
                self.current_turn = 'b' if self.current_turn == 'r' else 'r'
                
                # Evaluate the board
                score = self.evaluate_board()
                
                # Restore turns
                self.current_turn = 'b' if self.current_turn == 'r' else 'r'
                
                # Restore original position
                piece.x, piece.y = orig_x, orig_y
                
                # Restore target piece if any
                if target_piece:
                    self.pieces.append(target_piece)
                
                # Update best move
                if self.current_turn == 'r':
                    if score > best_score:
                        best_score = score
                        best_move = move
                else:
                    if score < best_score:
                        best_score = score
                        best_move = move
            
            # Make the best move
            if best_move:
                piece, new_x, new_y = best_move
                self.move_piece(piece, new_x, new_y)
                return True
            else:
                # If no best move found (shouldn't happen if possible_moves is not empty)
                # Switch turns to player as fallback
                self.current_turn = 'b' if self.current_turn == 'r' else 'r'
                return True
        
        return False

class Game:
    def __init__(self):
        self.board = Board()
        self.game_over = False
        self.winner = None
        self.show_menu = True
    
    def handle_event(self, event):
        if self.show_menu:
            if event.type == MOUSEBUTTONDOWN:
                # Check if player clicked on red or black option
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Red button area
                if 300 <= mouse_x <= 500 and 300 <= mouse_y <= 350:
                    self.board.player_color = 'r'
                    self.show_menu = False
                
                # Black button area
                elif 300 <= mouse_x <= 500 and 400 <= mouse_y <= 450:
                    self.board.player_color = 'b'
                    self.board.current_turn = 'r'  # Red always goes first
                    self.show_menu = False
                    # AI makes first move if player is black
                    self.board.ai_make_move()
        else:
            if event.type == MOUSEBUTTONDOWN and not self.game_over:
                # Get board coordinates from mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                board_x = (mouse_x - BOARD_MARGIN_X) // CELL_SIZE
                board_y = (mouse_y - BOARD_MARGIN_Y) // CELL_SIZE
                
                # Check if click is within board
                if 0 <= board_x < BOARD_WIDTH and 0 <= board_y < BOARD_HEIGHT:
                    # Handle piece selection and movement
                    move_made = self.board.select_piece(board_x, board_y)
                    
                    # Check if game is over after player's move
                    result = self.board.is_game_over()
                    if result:
                        self.game_over = True
                        self.winner = result
                    
                    # AI makes a move if it's its turn
                    elif move_made and not self.game_over:
                        self.board.ai_make_move()
                        
                        # Check if game is over after AI's move
                        result = self.board.is_game_over()
                        if result:
                            self.game_over = True
                            self.winner = result
            
            elif event.type == KEYDOWN:
                if event.key == K_r:  # Reset game
                    self.board.reset()
                    self.game_over = False
                    self.winner = None
                    self.show_menu = True
    
    def draw(self, surface):
        surface.fill(WHITE)
        
        if self.show_menu:
            self.draw_menu(surface)
        else:
            self.board.draw(surface)
            
            if self.game_over:
                self.draw_game_over(surface)
    
    def draw_menu(self, surface):
        # Draw title
        font = pygame.font.SysFont('Arial', 48)
        title = font.render('Chinese Chess (Xiangqi)', True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title, title_rect)
        
        # Draw instructions
        font = pygame.font.SysFont('Arial', 24)
        instr = font.render('Choose your side:', True, BLACK)
        instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, 250))
        surface.blit(instr, instr_rect)
        
        # Draw red button
        pygame.draw.rect(surface, RED, (300, 300, 200, 50))
        red_text = font.render('Red (First)', True, WHITE)
        red_rect = red_text.get_rect(center=(400, 325))
        surface.blit(red_text, red_rect)
        
        # Draw black button
        pygame.draw.rect(surface, BLACK, (300, 400, 200, 50))
        black_text = font.render('Black (Second)', True, WHITE)
        black_rect = black_text.get_rect(center=(400, 425))
        surface.blit(black_text, black_rect)
    
    def draw_game_over(self, surface):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        surface.blit(overlay, (0, 0))
        
        # Draw game over message
        font = pygame.font.SysFont('Arial', 48)
        if self.winner == 'r':
            text = font.render('Red Wins!', True, RED)
        elif self.winner == 'b':
            text = font.render('Black Wins!', True, BLACK)
        else:
            text = font.render('Draw!', True, BLUE)
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        surface.blit(text, text_rect)
        
        # Draw restart instruction
        font = pygame.font.SysFont('Arial', 24)
        restart = font.render('Press R to restart', True, BLACK)
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        surface.blit(restart, restart_rect)

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            game.handle_event(event)
        
        game.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
