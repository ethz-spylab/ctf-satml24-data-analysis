#%%
import json


from pathlib import Path

PATH = Path("/data/projects/satml-llm-ctf-analysis/dumps")


# Step 1: Read defense_submissions.json and build a mapping from submission id to defense id
submission_to_defense = {}
with open(PATH / 'defense_submission.json', 'r') as submissions_file:
    for line in submissions_file:
        submission = json.loads(line)
        submission_id = submission["_id"]["$oid"]
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
            "defense_prompt": defense["defense_prompt"],
            "output_filters": defense["output_filters"],
            "model": model
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
            "defense_data": defense_data
            }) + '\n')
    

print("filtered_defense.json has been created.")

# %%
