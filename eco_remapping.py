import os
import json

def save_ECO_to_json(games_data, output_path):
    # Save the extracted games data to a JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(games_data, f, indent=2)

