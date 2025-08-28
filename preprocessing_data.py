import chess.pgn
import os
import json

required_fields = ["White", "Black", "WhiteElo", "BlackElo", "Result", "Opening", "ECO", "TimeControl"]

def load_pgn_games(pgn_path, max_games=None, min_elo=1700):
    games_data = []
    with open(pgn_path, 'r', encoding='utf-8') as pgn_file:
        game_count = 0
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            # Filtering unkown or broken data
            for field in required_fields:
                value = game.headers.get(field)
                if value in [None, "Unknown", ""]:
                    continue # Skip this game
            
            # Limit the number of games processed
            if max_games and game_count >= max_games:
                break

            # Skip games with invalid Elo formats
            white_elo = game.headers.get("WhiteElo")
            black_elo = game.headers.get("BlackElo")
            try:
                white_elo = int(white_elo) if white_elo else 0
                black_elo = int(black_elo) if black_elo else 0
            except ValueError:
                continue

            # Skip games below threshold
            if white_elo < min_elo or black_elo < min_elo:
                continue  

            # Filtering out games with very short time controls (e.g., blitz or bullet)
            time_control = game.headers.get("TimeControl", "0")
            base_time = int(time_control.split('+')[0]) if '+' in time_control else 0
            if base_time < 60: # Minimum 1 minute base time
                continue

            # Extract relevant information from the game
            game_info = {
                "GameIndex": game_count,
                "White": game.headers.get("White"),
                "Black": game.headers.get("Black"),
                "WhiteElo": white_elo,
                "BlackElo": black_elo,
                "Result": game.headers.get("Result", "Unknown"),
                "Opening": game.headers.get("Opening", "Unknown"),
                # ECO Code is used to classify chess openings. Refer to repo wiki for more details.
                "ECO": game.headers.get("ECO", None),
                "TimeControl": time_control,
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