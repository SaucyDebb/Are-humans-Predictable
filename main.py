from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env file
load_dotenv()
# obtaining file path from .env file
pgn_path = os.getenv("PGN_PATH")

# Begin preprocessing PGN files
# from preprocessing_pgn import filter_games, cap_by_eco, pgn_to_parquet
# print("Starting PGN preprocessing...")
# # Step 1: Convert PGN to Parquet
# parquet_path = "Parquet Files/games.parquet"
# raw_df = pgn_to_parquet(
#     pgn_folder=pgn_path,           # folder containing all your PGNs
#     parquet_out=parquet_path,
#     log_interval=50000,  # log progress every N games
#     limit_games=3818709  # max number of games in the dataset, included to estime time remaining
#     # limit_games=100  # optional: cap total games processed
# )

# print(f"✅ Step 1: Converted PGN to Parquet: {parquet_path}, total: {len(raw_df)}")

# # Step 2: Filter games based on criteria
# filtered_path = "Parquet Files/games_filtered.parquet"
# filtered_df = filter_games(parquet_path, filtered_path)
# print(f"✅ Step 2: Filtered games: {filtered_path}, remaining: {len(filtered_df)}")

# # Step 3: Cap number of games per ECO code to ensure diversity
# capped_path = "Parquet Files/games_capped.parquet"
# capped_df = cap_by_eco(filtered_path, capped_path)
# print(f"✅ Step 3: Capped by ECO: {capped_path}, remaining: {len(capped_df)}")

# Using filtered dataset, no duplicates. 
# Source: https://database.nikonoel.fr/ Lichess Elite Database
#
# # Step 4: Remove duplicate games based on fingerprint
# ## Useful when parsing multiple PGN files that might contain overlapping games
# deduped_path = "Parquet Files/games_deduped.parquet"
# deduped_df = dedup(capped_path, deduped_path)
# print(f"✅ Step 4: Deduplicated games: {deduped_path}, remaining: {len(deduped_df)}")
# print("All preprocessing steps completed successfully.")

# Next step: Extract positions from the processed PGN file
# from extract_fen import extract_fen
# print("Starting FEN extraction...")
# extracted_fen = extract_fen(
#     parquet_in=capped_path,           # folder containing all your PGNs
#     parquet_folder="FEN MOVES",
#     log_interval=60000,  # log progress every N games
#     # limit_games=2717093  # maximum games in the capped dataset/final dataset
#     limit_games=500000  # optional: cap total games processed
# )
# print(f"✅ FEN extraction completed, total file extracted: {extracted_fen}")

# Quick sanity check on extracted positions
print("Performing sanity check on extracted positions...\n")
df = pd.read_parquet("FEN MOVES/fen_moves_500k.parquet")
print(df["ply"].describe())
print(df["eco"].value_counts().head(20))
