import chess.pgn

def extract_board_move_pairs(pgn_path):
    data = []
    with open(pgn_path, 'r') as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            board = game.board()
            for move in game.mainline_moves():
                fen = board.fen()
                uci = move.uci()
                data.append((fen, uci))
                board.push(move)
    return data

