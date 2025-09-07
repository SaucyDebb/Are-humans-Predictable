import os
import pandas as pd
import chess.pgn

def parse_single_pgn(pgn_path, limit=None):
    rows = []
    invalid_game = 0
    with open(pgn_path, 'r', encoding='utf-8') as pgn_file:
        i, game = 0, chess.pgn.read_game(pgn_file)
        while game:
            if not game.headers or len(list(game.mainline_moves())) == 0:
                invalid_game += 1
                game = chess.pgn.read_game(pgn_file)
                continue

            rows.append({
                "source_path": os.path.basename(pgn_path),
                "event": game.headers.get("Event", ""),
                "white": game.headers.get("White", ""),
                "black": game.headers.get("Black", ""),
                "whiteelo": int(game.headers.get("WhiteElo", "0") or 0),
                "blackelo": int(game.headers.get("BlackElo", "0") or 0),
                "result": game.headers.get("Result", "*"),
                "timecontrol": game.headers.get("TimeControl", ""),
                "termination": game.headers.get("Termination", ""),
                "eco": game.headers.get("ECO", ""),
                "variant": game.headers.get("Variant", "Standard"),
                "plycount": game.end().ply()
            })
            i += 1
            if limit and i >= limit:
                break
            game = chess.pgn.read_game(pgn_file)

    return rows, invalid_game

def pgn_batch_to_parquet(pgn_folder, parquet_out, limit_per_file=None):
    all_rows = []
    total_invalid = 0
    for filename in os.listdir(pgn_folder):
        if filename.endswith(".pgn"):
            pgn_path = os.path.join(pgn_folder, filename)
            print(f"📂 Parsing {filename}")
            rows, invalid = parse_single_pgn(pgn_path, limit=limit_per_file)
            all_rows.extend(rows)
            total_invalid += invalid

    df = pd.DataFrame(all_rows)
    df.to_parquet(parquet_out, index=False)
    print(f"✅ Saved {len(df)} games to {parquet_out}")
    if total_invalid > 0:
        print(f"⚠️ Skipped {total_invalid} invalid or empty games.")
    return df

import re

def parse_tc(tc):
    # e.g., "600+5" -> base=600, inc=5
    m = re.match(r"(\d+)\+?(\d+)?", tc or "")
    if not m: return 0, 0
    base, inc = int(m.group(1)), int(m.group(2) or 0)
    return base, inc

def filter_games(parquet_path, parquet_out, min_elo=2200, min_base_sec=180, min_ply=20):
    df = pd.read_parquet(parquet_path)
    avg_elo = (df.whiteelo + df.blackelo) / 2
    base_inc = df.timecontrol.apply(parse_tc)
    df["base_sec"] = [b for b, _ in base_inc]
    df["variant_norm"] = df.variant.fillna("Standard").str.lower()
    df["termination_norm"] = df.termination.fillna("").str.lower()  

    keep = (
        (avg_elo >= min_elo) &
        (df.variant_norm == "standard") &
        (df.base_sec >= min_base_sec) &
        (df.plycount >= min_ply) &
        (~df.termination_norm.str.contains("time forfeit|abandoned|cheat|rules infraction"))
    )
    out = df[keep].copy()
    out.to_parquet(parquet_out, index=False)
    return out

# Cap number of games per ECO code to ensure diversity
def cap_by_eco(parquet_path, parquet_out, cap_per_eco=50000):
    df = pd.read_parquet(parquet_path)
    df["eco"] = df.eco.fillna("A00")
    df = (df.sort_values(["eco"])
            .groupby("eco", group_keys=False) # Important to keep group keys for filtering
            .head(cap_per_eco)) # Keep only top N per group. basically croping each group to cap_per_eco
    df.to_parquet(parquet_out, index=False)
    return df

# Using filtered dataset, no duplicates. 
# Source: https://database.nikonoel.fr/ Lichess Elite Database
#
# # Generate fingerprint to identify duplicates
# def fingerprint(row):
#     return f"{row['white']}|{row['black']}|{row['date']}|{row['round']}|{row['result']}"

# # Remove duplicate games based on fingerprint
# def dedup(parquet_in, parquet_out):
#     df = pd.read_parquet(parquet_in)
#     df["fp"] = df.apply(fingerprint, axis=1)
#     df = df.drop_duplicates(subset=["fp"])
#     df.to_parquet(parquet_out, index=False)
#     return df

