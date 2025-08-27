from dotenv import load_dotenv
import os

load_dotenv()
pgn_path = os.getenv("PGN_PATH")

from model_training import extract_board_move_pairs
data = extract_board_move_pairs(pgn_path)
print(data[:5])  # Print first 5 board-move pairs for verification