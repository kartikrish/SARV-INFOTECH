import math
import random

class TicTacToe:
    def __init__(self):
        # The board is represented as a list of 9 elements, indexed 0-8.
        # ' ' for empty, 'X' for AI, 'O' for Human.
        self.board = [' '] * 9
        self.human_player = 'O'
        self.ai_player = 'X'

    def print_board(self):
        """Prints the current state of the board in a 3x3 grid format."""
        print('\n-------------')
        print(f'| {self.board[0]} | {self.board[1]} | {self.board[2]} |')
        print('-------------')
        print(f'| {self.board[3]} | {self.board[4]} | {self.board[5]} |')
        print('-------------')
        print(f'| {self.board[6]} | {self.board[7]} | {self.board[8]} |')
        print('-------------')

    def available_moves(self):
        """Returns a list of indices for all empty spots."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        """Checks if the board has any empty squares left."""
        return ' ' in self.board

    def make_move(self, square, player):
        """Places a player's marker on the board if the spot is empty."""
        if self.board[square] == ' ':
            self.board[square] = player
            return True
        return False

    def check_win(self, board, player):
        """Checks if the specified player has won on the given board state."""
        # Define winning combinations (indices)
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]

        for combo in win_combinations:
            if all(board[i] == player for i in combo):
                return True
        return False

# --- Minimax Algorithm ---

def minimax(board, player, game_instance):
    """
    The Minimax algorithm function.
    It returns a tuple: (score, best_move_index).
    """
    ai = game_instance.ai_player
    human = game_instance.human_player

    # 1. Check for terminal states (win/loss/tie)
    if game_instance.check_win(board, ai):
        return (1, None)  # AI wins (Max player)
    if game_instance.check_win(board, human):
        return (-1, None) # Human wins (Min player)
    if not game_instance.empty_squares():
        return (0, None)  # Tie

    # 2. Initialize best_move and best_score
    if player == ai:
        # AI is Max player, wants to maximize score
        best_score = -math.inf
        best_move = None
    else:
        # Human is Min player, wants to minimize score (AI's score)
        best_score = math.inf
        best_move = None

    # 3. Iterate through available moves
    for move in game_instance.available_moves():
        # a. Make the move
        board[move] = player

        # b. Recurse (call minimax for the next player)
        # Note: We pass the 'score' from the tuple, ignoring the 'move'
        if player == ai:
            # Next move is Human's (Minimizer)
            score, _ = minimax(board, human, game_instance)
        else:
            # Next move is AI's (Maximizer)
            score, _ = minimax(board, ai, game_instance)

        # c. Undo the move (backtrack)
        board[move] = ' '
        
        # d. Update best score and move
        if player == ai:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    # 4. Return the result
    return (best_score, best_move)

# --- Game Loop ---

def play_game():
    """Main function to run the human vs. AI game."""
    game = TicTacToe()
    current_player = game.human_player # Human goes first (can be changed)
    
    # Randomly choose who goes first
    if random.choice([True, False]):
        current_player = game.ai_player
        print(f"The AI ({game.ai_player}) goes first.")
    else:
        print(f"The Human ({game.human_player}) goes first.")
        
    print("Welcome to Tic-Tac-Toe! The board positions are 0-8, from top-left to bottom-right.")
    
    # The game continues as long as there are empty squares and no one has won
    while game.empty_squares() and not game.check_win(game.board, game.human_player) and not game.check_win(game.board, game.ai_player):
        game.print_board()

        if current_player == game.human_player:
            # Human Player's Turn
            while True:
                try:
                    move = int(input(f"Enter your move (0-8): "))
                    if 0 <= move <= 8 and game.make_move(move, game.human_player):
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            current_player = game.ai_player # Switch turn

        else:
            # AI Player's Turn (The Minimax agent)
            print(f"AI ({game.ai_player}) is thinking...")
            
            # The Minimax algorithm calculates the best move
            score, ai_move = minimax(game.board, game.ai_player, game)
            
            if ai_move is not None:
                game.make_move(ai_move, game.ai_player)
                print(f"AI chooses move {ai_move}")
            else:
                 # Should only happen on the first move if Minimax is called on an empty board
                game.make_move(random.choice(game.available_moves()), game.ai_player)

            current_player = game.human_player # Switch turn

    # Game Over
    game.print_board()
    if game.check_win(game.board, game.ai_player):
        print("Game Over! The AI wins! You cannot defeat me!")
    elif game.check_win(game.board, game.human_player):
        print("Game Over! You won... (This should only happen if there's a bug!)")
    else:
        print("Game Over! It's a draw!")
        
if __name__ == '__main__':
    play_game()