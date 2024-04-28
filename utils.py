import json
from pathlib import Path
#PATH = Path("/data/projects/satml-llm-ctf-analysis/ctf-satml24")
PATH : Path = Path(".")

# Load valid_defense.json
with open(PATH / 'valid_defense.json', 'r') as valid_defense_file:
    valid_defense = [json.loads(line) for line in valid_defense_file]

#%%
short_model = {
    "openai/gpt-3.5-turbo-1106": "gpt35",
    "meta/llama-2-70b-chat": "llama"
}

# Create a dictionary to lookup defense
defense_lookup = {(defense["model"], defense["defense_data"]["defense_id"]): (defense["team"], defense["submission_id"]) for defense in valid_defense}
