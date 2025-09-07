import chess
import pandas as pd
import time

def extract_fen(parquet_in, parquet_out, log_interval=10000, limit_games=None):
    """
    Extracts FEN + move pairs from filtered Parquet containing moves_uci.
    Saves position-level data to a new Parquet file.
    """
    df_games = pd.read_parquet(parquet_in)
    if limit_games:
        df_games = df_games.head(limit_games)

    positions = []
    start_time = time.time()
    game_count = 0
    pos_count = 0

    for idx, row in df_games.iterrows():
        moves = row["moves_uci"]
        if not isinstance(moves, list) or len(moves) == 0:
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
                break  # skip malformed move

        game_count += 1
        if game_count % log_interval == 0:
            elapsed = time.time() - start_time
            games_per_sec = game_count / elapsed
            remaining_games = len(df_games) - game_count
            eta_str = (
                f"ETA: {remaining_games / games_per_sec / 60:.1f} min"
                if games_per_sec > 0 else "ETA: unknown"
            )
            print(
                f"[{elapsed/60:.1f} min] "
                f"Total: {game_count:,} games ({pos_count:,} positions) | "
                f"{eta_str}",
                flush=True
            )

    df_positions = pd.DataFrame(positions)
    df_positions.to_parquet(parquet_out, index=False)
    elapsed = time.time() - start_time
    print(f"\n🎯 Done: {game_count:,} games, {pos_count:,} positions in {elapsed/60:.1f} min total.")
    return df_positions