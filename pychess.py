import chess

board = chess.Board()
print(board)  # ASCII representation of the board
# print(list(board.legal_moves))  # All legal moves from current position

# Mini Interpreter for chess moves
def interpret_legal_moves(board):
    # Map piece notation to full names
    # sample of move 'g1h3' => Knight from g1 to h3
    name_map = {
        'N': 'Knight',
        'B': 'Bishop',
        'R': 'Rook',
        'Q': 'Queen',
        'K': 'King',
        'P': 'Pawn'
    }
    # Convert legal moves to human-readable format
    readable_moves = []
    for move in board.legal_moves:
        # move being the available move
        # Get the piece Name (e.g., 'N' for Knight)
        piece = board.piece_at(move.from_square)
        if piece:
            # Determine piece color
            color = 'White' if piece.color == chess.WHITE else 'Black'
            # Get full piece name
            piece_name = name_map[piece.symbol().upper()]
            # (e.g., 'g1h3' from g1
            from_sq = chess.square_name(move.from_square)
            # (e.g., 'g1h3' to h3)
            to_sq = chess.square_name(move.to_square)
            # Add promotion info if applicable (e.g., 'e7e8Q' promoting to Queen)
            if move.promotion:
                promoted_piece = name_map[chess.PIECE_SYMBOLS[move.promotion].upper()]
                description = f"{color} {piece_name} from {from_sq} to {to_sq}, promoting to {promoted_piece}"
            else:
                description = f"{color} {piece_name} from {from_sq} to {to_sq}"
            readable_moves.append(description)
    return readable_moves

print(interpret_legal_moves(board))
