import chess.pgn
import os
import json

def load_pgn_games(pgn_path, max_games=None):
    games_data = []
    with open(pgn_path, 'r', encoding='utf-8') as pgn_file:
        game_count = 0
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            if max_games and game_count >= max_games:
                break
                
            # Extract relevant information from the game
            game_info = {
                "GameIndex": game_count,
                "White": game.headers.get("White", "Unknown"),
                "Black": game.headers.get("Black", "Unknown"),
                "WhiteElo": game.headers.get("WhiteElo", None),
                "BlackElo": game.headers.get("BlackElo", None),
                "Result": game.headers.get("Result", "Unknown"),
                "Opening": game.headers.get("Opening", "Unknown"),
                # ECO Code is used to classify chess openings. Refer to repo wiki for more details.
                "ECO": game.headers.get("ECO", None),
                "Moves": []
            }

            board = game.board()
            for move in game.mainline_moves():
                # Convert move to SAN (Standard Algebraic Notation) for better readability e.g., e4, Nf3
                san = board.san(move)
                game_info["Moves"].append(san)
                board.push(move)

            games_data.append(game_info)
            game_count += 1

    return games_data

def save_games_to_json(games_data, output_path):
    # Save the extracted games data to a JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(games_data, f, indent=2)