import chess.pgn
import pandas as pd
import time
from pathlib import Path

def extract_fen(pgn_folder, parquet_out, log_interval=10000, limit_games=None):
    """
    Extracts FEN + move pairs from all PGN files in a folder and saves to Parquet.
    Shows per-file and total progress with ETA.
    """
    positions = []
    start_time = time.time()
    game_count = 0
    pos_count = 0

    # Get all .pgn files in the folder (sorted for consistency)
    pgn_files = sorted(Path(pgn_folder).glob("*.pgn"))
    total_files = len(pgn_files)

    if not pgn_files:
        print(f"⚠️ No PGN files found in {pgn_folder}")
        return None

    for file_idx, pgn_path in enumerate(pgn_files, start=1):
        file_game_count = 0
        print(f"\n📂 [{file_idx}/{total_files}] Processing file: {pgn_path.name}")

        with open(pgn_path, 'r', encoding='utf-8') as pgn_file:
            game = chess.pgn.read_game(pgn_file)
            while game:
                headers = game.headers
                whiteelo = int(headers.get("WhiteElo", "0") or 0)
                blackelo = int(headers.get("BlackElo", "0") or 0)
                result = headers.get("Result", "*")
                eco = headers.get("ECO", "")

                board = game.board()
                for ply, move in enumerate(game.mainline_moves()):
                    positions.append({
                        "fen": board.fen(),
                        "move_uci": move.uci(),
                        "ply": ply,
                        "result": result,
                        "whiteelo": whiteelo,
                        "blackelo": blackelo,
                        "eco": eco
                    })
                    pos_count += 1
                    board.push(move)

                game_count += 1
                file_game_count += 1

                # Progress log
                if game_count % log_interval == 0:
                    elapsed = time.time() - start_time
                    games_per_sec = game_count / elapsed
                    est_total_games = limit_games if limit_games else "?"
                    if isinstance(est_total_games, int):
                        remaining_games = est_total_games - game_count
                        eta_sec = remaining_games / games_per_sec if games_per_sec > 0 else 0
                        eta_str = f"ETA: {eta_sec/60:.1f} min"
                    else:
                        eta_str = "ETA: unknown"

                    print(
                        f"[{elapsed/60:.1f} min] "
                        f"Total: {game_count:,} games ({pos_count:,} positions) | "
                        f"Current file: {file_game_count:,} games | "
                        f"{eta_str}",
                        flush=True
                    )

                if limit_games and game_count >= limit_games:
                    break

                game = chess.pgn.read_game(pgn_file)

        print(f"✅ Finished file {pgn_path.name} — {file_game_count:,} games processed.")

        if limit_games and game_count >= limit_games:
            break

    # Save all positions to Parquet
    df = pd.DataFrame(positions)
    df.to_parquet(parquet_out, index=False)
    elapsed = time.time() - start_time
    print(f"\n🎯 Done: {game_count:,} games, {pos_count:,} positions in {elapsed/60:.1f} min total.")
    return df