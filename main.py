from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# obtaining file path from .env file
pgn_path = os.getenv("PGN_PATH")

from preprocessing_data import load_pgn_games, save_games_to_json
# Create output directory if it doesn't exist
output_dir = "Parsed Data"
os.makedirs(output_dir, exist_ok=True)  # Creates folder if it doesn't exist
output_json_path = os.path.join(output_dir, "parsed_games.json")
games = load_pgn_games(pgn_path, max_games=100)  # You can adjust max_games
save_games_to_json(games, output_json_path)
print(f"✅ Parsed {len(games)} games and saved to {output_json_path}")