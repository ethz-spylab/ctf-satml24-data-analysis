#%%
import json
from pathlib import Path

from ids import VALID, DQED, id_to_team
PATH = Path("/data/projects/satml-llm-ctf-analysis/ctf-satml24")


# Step 1: Read defense_submissions.json and build a mapping from submission id to defense id
submissions = {}
submission_to_defense = {}
with open(PATH / 'defense_submission.json', 'r') as submissions_file:
    for line in submissions_file:
        submission = json.loads(line)
        submission_id = submission["_id"]["$oid"]
        submissions[submission_id] = submission
        defense_id = submission["defense"]["$id"]["$oid"]
        model = submission["model"]
        submission_to_defense[submission_id] = defense_id

# Step 2: Read defenses.json and build a mapping from defense id to defense data
defense_id_to_data = {}
with open(PATH / 'defense.json', 'r') as defenses_file:
    for line in defenses_file:
        defense = json.loads(line)
        defense_id = defense["_id"]["$oid"]
        # Extract only the relevant defense data
        defense_data = {
            "defense_id": defense_id,
            "defense_prompt": defense["defense_prompt"],
            "output_filters": defense["output_filters"],
        }
        defense_id_to_data[defense_id] = defense_data

# Step 3: Create filtered_defense.json
with open(PATH / 'filtered_defense.json', 'w') as filtered_file:
    # Initialize an empty dictionary to hold the final mapping
    final_mapping = {}
    for submission_id, defense_id in submission_to_defense.items():
        # Use the mappings to fetch the corresponding defense data
        if defense_id in defense_id_to_data:
            final_mapping[submission_id] = defense_id_to_data[defense_id]
    
    # Write the final mapping to the file as a list of JSONs, each on a new line
    for submission_id, defense_data in final_mapping.items():
        filtered_file.write(json.dumps({
            "submission_id": submission_id,
            "defense_data": defense_data,
            "model": submissions[submission_id]["model"],
            }) + '\n')
    
print("filtered_defense.json has been created.")

#%%
# Step 4: take defenses which were used in the attack phase and connect with teams
print(len(VALID), len(DQED))

with open(PATH / 'valid_ids.json', 'w') as valid_ids_file:
    valid_ids_file.write(json.dumps(VALID) + '\n')
with open(PATH / 'dqed_ids.json', 'w') as invalid_ids_file:
    invalid_ids_file.write(json.dumps(DQED) + '\n')

assert all(id in id_to_team for id in VALID) and len(id_to_team) == len(VALID)

# write teams
with open(PATH / 'teams.json', 'w') as teams_file:
    for id, team in id_to_team.items():
        teams_file.write(json.dumps({
            "submission_id": id,
            "team": team
        }) + '\n')

#%%
# Step 5: save those defenses which were used in the attack phase
with open(PATH / 'valid_defense.json', 'w') as valid_submissions_file:
    for submission_id, defense_data in final_mapping.items():
        if submission_id in VALID:
            valid_submissions_file.write(json.dumps({
                "submission_id": submission_id,
                "team": id_to_team[submission_id],
                "model": submissions[submission_id]["model"],
                "defense_data": defense_data,
            }) + '\n')
                

# %%
