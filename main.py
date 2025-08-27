from dotenv import load_dotenv
import os

load_dotenv()
pgn_path = os.getenv("PGN_PATH")
print(f"PGN_PATH: {pgn_path}")
