import chess
import pandas as pd
import time
import numpy as np


def extract_fen(parquet_in, parquet_folder, log_interval=10000, limit_games=None, random_seed=42):
    """
    Extracts FEN + move pairs from filtered Parquet containing moves_uci.
    Saves position-level data to a new Parquet file.
    """
    df_games = pd.read_parquet(parquet_in)
    df_sampled = df_games.sample(n=limit_games, random_state=random_seed).reset_index(drop=True)
    if limit_games:
        df_sampled = df_sampled.head(limit_games)

    positions = []
    start_time = time.time()
    game_count = 0
    pos_count = 0
    file_count = 1

    for idx, row in df_sampled.iterrows():
        moves = row["moves_uci"]
        moves = list(moves) if isinstance(moves, np.ndarray) else moves
        if not isinstance(moves, (list, np.ndarray)) or len(moves) == 0:
            continue    

        board = chess.Board()
        for ply, move_uci in enumerate(moves):
            try:
                move = chess.Move.from_uci(move_uci)
                if move not in board.legal_moves:
                    break  # skip illegal move
                positions.append({
                    "game_id": row["game_id"],
                    "fen": board.fen(),
                    "move_uci": move_uci,
                    "ply": ply,
                    "result": row["result"],
                    "whiteelo": row["whiteelo"],
                    "blackelo": row["blackelo"],
                    "eco": row["eco"]
                })
                pos_count += 1
                board.push(move)
            except Exception as e:
                print(f"⚠️ Error processing move {move_uci} in game {row['game_id']}: {e}")
                break  # skip malformed move

        game_count += 1
        if game_count % log_interval == 0:
            elapsed = time.time() - start_time
            games_per_sec = game_count / elapsed
            remaining_games = len(df_sampled) - game_count
            current_time = time.time()
            eta_time = remaining_games / games_per_sec
            eta_str = (
                f"ETA: {eta_time / 60:.1f} min"
                if games_per_sec > 0 else "ETA: unknown"
            )
            end_timestamp = time.time() + eta_time
            # converting to local time
            local_struct = time.localtime(end_timestamp)
            end_time = time.strftime("%Y-%m-%d %H:%M:%S", local_struct)
            end_time_str = (
                f"End time: {end_time} "
                if games_per_sec > 0 else "End time: unknown"
            )
            print(
                f"[{elapsed/60:.1f} min] "
                f"Total: {game_count:,} games ({pos_count:,} positions) | "
                f"{eta_str} | ",
                f"{end_time_str}",
                flush=True
            )

        # Save intermediate results to avoid memory issues. If memory error occurs, reduce the number len(positions) >= 100_000..etc
        if len(positions) >= 500_000 or (game_count == limit_games and len(positions) > 0):
            parquet_out = f"{parquet_folder}/fen_moves_{file_count}.parquet"
            pd.DataFrame(positions).to_parquet(parquet_out, index=False)
            positions.clear()
            file_count += 1
            print(f"💾 Saved intermediate positions to {parquet_out}")

    elapsed = time.time() - start_time
    print(f"🎯 Done: {game_count:,} games, {pos_count:,} positions in {elapsed/60:.1f} min total.\n")
    print(len(positions))
    return file_count - 1