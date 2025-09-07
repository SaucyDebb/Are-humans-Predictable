from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# obtaining file path from .env file
pgn_path = os.getenv("PGN_PATH")

# # Begin preprocessing PGN files
# from preprocessing_pgn import parse_single_pgn, filter_games, cap_by_eco, pgn_batch_to_parquet
# print("Starting PGN preprocessing...")
# # Step 1: Convert PGN to Parquet
# parquet_path = "Parquet/games.parquet"
# raw_df = pgn_batch_to_parquet(pgn_path, parquet_path)
# # print top 10 rows
# print(f"✅ Converted PGN to Parquet: {parquet_path}, total: {len(raw_df)}")

# # Step 2: Filter games based on criteria
# filtered_path = "Parquet/games_filtered.parquet"
# filtered_df = filter_games(parquet_path, filtered_path)
# print(f"✅ Filtered games: {filtered_path}, remaining: {len(filtered_df)}")

# # Step 3: Cap number of games per ECO code to ensure diversity
# capped_path = "Parquet/games_capped.parquet"
# capped_df = cap_by_eco(filtered_path, capped_path)
# print(f"✅ Capped by ECO: {capped_path}, remaining: {len(capped_df)}")

# Using filtered dataset, no duplicates. 
# Source: https://database.nikonoel.fr/ Lichess Elite Database
#
# # Step 4: Remove duplicate games based on fingerprint
# ## Useful when parsing multiple PGN files that might contain overlapping games
# deduped_path = "Parquet/games_deduped.parquet"
# deduped_df = dedup(capped_path, deduped_path)
# print(f"✅ Deduplicated games: {deduped_path}, remaining: {len(deduped_df)}")
# print("All preprocessing steps completed successfully.")

# Next step: Extract positions from the processed PGN file
from extract_fen import extract_fen
df_positions = extract_fen(
    pgn_folder=pgn_path,           # folder containing all your PGNs
    parquet_out="Parquet/games_fen.parquet",
    log_interval=1000,  # log progress every N games
    limit_games=200000  # optional: cap total games processed
)