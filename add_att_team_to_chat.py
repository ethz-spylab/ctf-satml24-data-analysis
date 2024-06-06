#%%
"""
The teams are in teams_all.json.
One line is
{{"_id":{"$oid":"659d035042b46e7ff17ee76f"},"name":"Ciber010010","is_active":true,"users":[{"$ref":"user","$id":{"$oid":"659a69b5d405b9f08da7b2f2"}}]}

1. Make a user -> team mapping
"""
#%%
import json
from tqdm import tqdm
from utils import PATH

def create_user_team_mapping(users_file, teams_file, output_file):
    """
    Create a user -> team mapping from the given users and teams files.
    
    Args:
    users_file (str): Path to the JSONL file containing user data.
    teams_file (str): Path to the JSONL file containing team data.
    output_file (str): Path to the output JSON file to save the user -> team mapping.
    
    Returns:
    dict: A dictionary mapping user IDs to team names.
    """
    user_team_mapping = {}

    # Read teams and create the mapping
    with open(teams_file, 'r') as teams_f:
        for line in tqdm(teams_f, desc="Processing teams"):
            team = json.loads(line)
            team_name = team['name']
            for user in team['users']:
                user_id = user['$id']['$oid']
                user_team_mapping[user_id] = team_name

    # Save the mapping to the output file
    with open(output_file, 'w') as output_f:
        json.dump(user_team_mapping, output_f, indent=4)

    return user_team_mapping

# Path to the dataset
dataset_path = PATH

#%%
# Define file paths
teams_file = f"{dataset_path}/team_all.json"
output_file = f"{dataset_path}/user_team_mapping.json"

# Create the user -> team mapping
user_team_mapping = create_user_team_mapping(None, teams_file, output_file)
print(f"User -> Team mapping created and saved to {output_file}")



#%%
"""
2. Add the team to the chat entries in the `user` field
"""
# %%
def add_team_to_chats(chats_file, user_team_mapping, output_file, is_jsonl=False):
    with open(chats_file, 'r') as chats_f:
        if is_jsonl:
            chats = []
            for line in tqdm(chats_f):
                chats.append(json.loads(line))
        else:
            chats = json.load(chats_f)
    
    for chat in tqdm(chats, desc="Processing chats"):
        user_id = chat['user']['$id']['$oid']
        if user_id in user_team_mapping:
            chat['user']['team'] = user_team_mapping[user_id]
        else:
            chat['user']['team'] = "Team unknown"

    # Save the updated chats back to the file
    with open(output_file, 'w') as chats_f:
        if is_jsonl:
            for chat in chats:
                chats_f.write(json.dumps(chat) + '\n')
        else:
            json.dump(chats, chats_f, indent=4)

#%%
# Path to the dataset
dataset_path = PATH

# Define file paths
test_file = f"{dataset_path}/chat.120.json"
main_file = f"{dataset_path}/chat.json"

# Run the add_team_to_chats function on the test file first
test_output_file = PATH/'added_chat.120.json'
add_team_to_chats(test_file, user_team_mapping, output_file=test_output_file)
print(f"Teams added to users in test file: {test_output_file}")

#%%
# Now run the add_team_to_chats function on the main file
main_output_file = PATH/'added_chat.json'
add_team_to_chats(main_file, user_team_mapping, output_file=main_output_file, is_jsonl=True)
print(f"Teams added to users in main file: {main_output_file}")



# %%
