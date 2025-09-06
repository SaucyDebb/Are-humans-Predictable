import chess.pgn
import pandas as pd

def pgn_to_parquet(pgn_path, parquet_out, limit=None):
    rows = []
    with open(pgn_path, 'r', encoding='utf-8') as pgn_file:
        i, game = 0, chess.pgn.read_game(pgn_file)
        while game:
            rows.append({
                "source_path": pgn_path,
                "event": game.headers.get("Event", ""),
                "site": game.headers.get("Site", ""),
                "date": game.headers.get("Date", ""),
                "round": game.headers.get("Round", ""),
                "white": game.headers.get("White", ""),
                "black": game.headers.get("Black", ""),
                "whiteelo": int(game.headers.get("WhiteElo", "0") or 0),
                "blackelo": int(game.headers.get("BlackElo", "0") or 0),
                "result": game.headers.get("Result", "*"),
                "timecontrol": game.headers.get("TimeControl", ""),
                "termination": game.headers.get("Termination", ""),
                "eco": game.headers.get("ECO", ""),
                "variant": game.headers.get("Variant", "Standard"),
                "plycount": int(game.headers.get("PlyCount", "0") or 0)
            })
            i += 1
            if limit and i >= limit:
                break
            game = chess.pgn.read_game(pgn_file)

    df = pd.DataFrame(rows)
    # Save to Parquet. Parquet file type is better for maintaining large datasets.
    df.to_parquet(parquet_out, index=False)
    return df

import re

def parse_tc(tc):
    # e.g., "600+5" -> base=600, inc=5
    m = re.match(r"(\d+)\+?(\d+)?", tc or "")
    if not m: return 0, 0
    base, inc = int(m.group(1)), int(m.group(2) or 0)
    return base, inc

def filter_games(parquet_path, parquet_out, min_elo=2200, min_base_sec=600, min_ply=20):
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
    df = (df.sort_values(["eco", "date"])
            .groupby("eco", group_keys=False) # Important to keep group keys for filtering
            .head(cap_per_eco)) # Keep only top N per group. basically croping each group to cap_per_eco
    df.to_parquet(parquet_out, index=False)
    return df

# Generate fingerprint to identify duplicates
def fingerprint(row):
    return f"{row['white']}|{row['black']}|{row['date']}|{row['round']}|{row['site']}|{row['result']}"

# Remove duplicate games based on fingerprint
def dedup(parquet_in, parquet_out):
    df = pd.read_parquet(parquet_in)
    df["fp"] = df.apply(fingerprint, axis=1)
    df = df.drop_duplicates(subset=["fp"])
    df.to_parquet(parquet_out, index=False)
    return df


