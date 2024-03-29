#%%
import json
from tqdm import tqdm

from utils import PATH, valid_defense, defense_lookup, short_model

print(defense_lookup)

#%%
# Load chats.json
with open(PATH / 'chat.json', 'r') as chats_file:
    chats = [json.loads(line) for line in chats_file]


#%%
# Create a dictionary of defenses wrt (team, model) id
defenses = {(defense["team"], short_model[defense["model"]]): defense for defense in valid_defense}
attacks = {(defense["team"], short_model[defense["model"]]): [] for defense in valid_defense}

# Construct attacks dict from chats
for chat in chats:
    chat_defense_id = chat["defense"]["$id"]["$oid"]
    chat_model = chat["model"]
    chat_team, submission_id = defense_lookup[(chat_model, chat_defense_id)]

    if chat["is_attack"]:
        try:
            attacks[(chat_team, short_model[chat_model])].append(chat)
        except KeyError:
            print(f"Defense {chat_defense_id} not found in defenses")


#%%
print(len(defenses))
print(len(attacks[(chat_team, short_model[chat_model])]))
#%%
# Count the number of attacks for each defense
attack_counts = {(team, model): len(attacks[(team, model)]) for (team, model) in attacks}

# Print the number of attacks for each defense
for (team, model), count in attack_counts.items():
    print(f"{team}, {model}: {count} attacks")


# %%
# Count how many attacks are how many messages
# in the sense that "history" has two entries

import pandas as pd

# Create a DataFrame to store the message counts
buckets = [[2], [4], [6], [8,10,12,14], list(range(16, 1000, 2)), [0]]
bucket_names = ["2", "4", "6", "8-14", "more", "empty"]
msg_counts = pd.DataFrame(0, index=defenses.keys(), columns=bucket_names)


# Fill the DataFrame with the message counts
for (team, model), attack_list in tqdm(attacks.items()):
    for attack in attack_list:
        msgs = attack["history"]
        for i, bucket in enumerate(buckets):
            if len(msgs) in bucket:
                msg_counts.loc[(team, model), bucket_names[i]] += 1
                break
        else:
            print(f"{team}, {model}: {len(msgs)} messages")

# Print the DataFrame
print(msg_counts)

# %%
# Save the message counts DataFrame to a file
msg_counts.to_csv(PATH / 'message_counts.csv')


# %%
