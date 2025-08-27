import chess.pgn

def extract_board_move_pairs(pgn_path):
    data = []
    with open(pgn_path, 'r') as pgn_file:
        while True:
            # Read a single game from the PGN file
            game = chess.pgn.read_game(pgn_file)
            # Break if no more games are available
            if game is None:
                break
            # Initialize the board for the game
            board = game.board()
            # Iterate through all moves in the game
            for move in game.mainline_moves():
                # Record the board state (FEN) and the move (UCI)
                fen = board.fen()
                uci = move.uci()
                data.append((fen, uci))
                # Make the move on the board
                board.push(move)
            break  # Process only the first game for now
    return data

import chess

def extract_features(fen):
    # The current board state in FEN notation
    board = chess.Board(fen)
    # Example features: turn, material balance, number of legal moves, castling rights
    features = {
        'turn': int(board.turn),
        'white_material': sum([piece_value(p) for p in board.piece_map().values() if p.color == chess.WHITE]),
        'black_material': sum([piece_value(p) for p in board.piece_map().values() if p.color == chess.BLACK]),
        'legal_moves': len(list(board.legal_moves)),
        'castling_rights': int(board.has_castling_rights(chess.WHITE)) + int(board.has_castling_rights(chess.BLACK))
    }
    return features

def piece_value(piece):
    values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
    return values[piece.piece_type]
