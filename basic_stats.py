#%%
import json
from pathlib import Path

PATH = Path("/data/projects/satml-llm-ctf-analysis/ctf-satml24")

# Load chats.json
with open(PATH / 'chat.json', 'r') as chats_file:
    chats = [json.loads(line) for line in chats_file]

# Load valid_defense.json
with open(PATH / 'valid_defense.json', 'r') as valid_defense_file:
    valid_defense = [json.loads(line) for line in valid_defense_file]

#%%
# Create a dictionary of defenses wrt defense id
defenses = {defense["defense_data"]["defense_id"]: defense for defense in valid_defense}
attacks = {defense["defense_data"]["defense_id"]: [] for defense in valid_defense}

# Construct attacks dict from chats
for chat in chats:
    chat_defense_id = chat["defense"]["$id"]["$oid"]
    if chat["is_attack"]:
        try:
            attacks[chat_defense_id].append(chat)
        except KeyError:
            print(f"Defense {chat_defense_id} not found in defenses")


#%%
# Count the number of attacks for each defense
attack_counts = {defense_id: len(attacks[defense_id]) for defense_id in attacks}

# Print the number of attacks for each defense
for defense_id, count in attack_counts.items():
    print(f"{defenses[defense_id]['team']}, {defenses[defense_id]['model']}: {count} attacks")


# %%
