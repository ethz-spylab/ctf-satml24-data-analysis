"""
TODO load the HuggingFace dataset instead of this
"""
#%%
import json
from tqdm import tqdm
from pathlib import Path
from utils import PATH

PREFIX_LENGTH = 20

def count_unique_prefixes(filename, prefix_length=PREFIX_LENGTH, is_jsonl=False, only_successful=False):
    """
    Count unique prefixes of the specified length in the first message of each chat in the given file.
    
    Args:
    filename (str): Path to the JSON file containing chat data.
    prefix_length (int): Length of the prefix to consider in each first message.
    
    Returns:
    int: Number of unique prefixes.
    """
    unique_prefixes = set()
    with open(filename, 'r') as file:
        if is_jsonl:
            chats = []
            for line in tqdm(file):
                chats.append(json.loads(line))
        else:
            chats = json.load(file)

    total = 0
    for chat in tqdm(chats):
        if chat['history'] and chat['history'][0]['content'] is not None:
            if only_successful:
                if not chat['was_successful_secret_extraction']:
                    continue
                prefix = chat['history'][0]['content'][:prefix_length]
                unique_prefixes.add(prefix)
            else:
                prefix = chat['history'][0]['content'][:prefix_length]
                unique_prefixes.add(prefix)
            total += 1
    
    return {'total': total,
            'unique': len(unique_prefixes)}

#%%
def count_unique_attacker_defender_pairs(filename, is_jsonl=False, only_successful=False, only_unsuccessful=False):
    with open(filename, 'r') as file:
        if is_jsonl:
            chats = []
            for line in tqdm(file):
                chats.append(json.loads(line))
        else:
            chats = json.load(file)
    
    chats = [chat for chat in chats if chat['history'] and chat['history'][0]['content'] is not None]

    assert not (only_successful and only_unsuccessful)
    if only_successful:
        chats = [chat for chat in chats if chat['was_successful_secret_extraction']]
    elif only_unsuccessful:
        chats = [chat for chat in chats if not chat['was_successful_secret_extraction']]
    
    attacker_defender_pairs = set()
    attackers = set()
    defenders = set()
    for chat in tqdm(chats):
        attacker = chat['user']['$id']['$oid']
        defense = chat['defense']['team'] + "," + chat['model']
        attackers.add(attacker)
        defenders.add(defense)
        attacker_defender_pairs.add((attacker, defense))
    
    return {'total': len(chats),
            'unique': len(attacker_defender_pairs),
            'unsuccessful': len(chats) - len(attacker_defender_pairs),
            'attackers': len(attackers),
            'defenders': len(defenders)}


def count_unique_attacker_defender_teams(filename, is_jsonl=False, only_successful=False, only_unsuccessful=False):
    with open(filename, 'r') as file:
        if is_jsonl:
            chats = []
            for line in tqdm(file):
                chats.append(json.loads(line))
        else:
            chats = json.load(file)
    
    chats = [chat for chat in chats if chat['history'] and chat['history'][0]['content'] is not None]

    assert not (only_successful and only_unsuccessful)
    if only_successful:
        chats = [chat for chat in chats if chat['was_successful_secret_extraction']]
    elif only_unsuccessful:
        chats = [chat for chat in chats if not chat['was_successful_secret_extraction']]
    
    attacker_defender_pairs = set()
    attackers = set()
    defenders = set()
    for chat in tqdm(chats):
        attacker = chat['user']['team']
        defense = chat['defense']['team'] + "," + chat['model']
        attackers.add(attacker)
        defenders.add(defense)
        attacker_defender_pairs.add((attacker, defense))
    
    return {'total': len(chats),
            'unique': len(attacker_defender_pairs),
            'unsuccessful': len(chats) - len(attacker_defender_pairs),
            'attackers': len(attackers),
            'defenders': len(defenders)}

# Path to the dataset
dataset_path = PATH

test_filename = f"{dataset_path}/chat.120.json"
main_filename = f"{dataset_path}/chat.json"
#%%
# Run the attacker-defender function on the test file first
test_data = count_unique_attacker_defender_pairs(test_filename)
print(f"Number of unique attacker-defender pairs in test file: {test_data['unique']} out of {test_data['total']}")
print(f"Unique attackers: {test_data['attackers']}, unique defenders: {test_data['defenders']}")

test_data = count_unique_attacker_defender_pairs(test_filename, only_successful=True)
print(f"Number of unique successful attacker-defender pairs in test file: {test_data['unique']} out of {test_data['total']}")
print(f"Unique attackers: {test_data['attackers']}, unique defenders: {test_data['defenders']}")



#%%
# Now run the attacker-defender function on the main file
main_data = count_unique_attacker_defender_pairs(main_filename, is_jsonl=True)
print(f"Number of unique attacker-defender pairs in main file: {main_data['unique']} out of {main_data['total']}")
print(f"Unique attackers: {main_data['attackers']}, unique defenders: {main_data['defenders']}")

main_data = count_unique_attacker_defender_pairs(main_filename, is_jsonl=True, only_successful=True)
print(f"Number of unique successful attacker-defender pairs in main file: {main_data['unique']} out of {main_data['total']}")
print(f"Unique attackers: {main_data['attackers']}, unique defenders: {main_data['defenders']}")

main_data = count_unique_attacker_defender_pairs(main_filename, is_jsonl=True, only_unsuccessful=True)
print(f"Number of unique unsuccessful attacker-defender pairs in main file: {main_data['unique']} out of {main_data['total']}")
print(f"Unique attackers: {main_data['attackers']}, unique defenders: {main_data['defenders']}")

#%%
# The same for teams
test_data = count_unique_attacker_defender_teams(test_filename)
print(f"Number of unique attacker-defender team pairs in test file: {test_data['unique']} out of {test_data['total']}")
print(f"Unique attackers: {test_data['attackers']}, unique defenders: {test_data['defenders']}")

test_data = count_unique_attacker_defender_teams(test_filename, only_successful=True)
print(f"Number of unique successful attacker-defender team pairs in test file: {test_data['unique']} out of {test_data['total']}")
print(f"Unique attackers: {test_data['attackers']}, unique defenders: {test_data['defenders']}")

#%%
# Now run the teams sattacker-defender function on the main file
main_data = count_unique_attacker_defender_teams(main_filename, is_jsonl=True)
print(f"Number of unique attacker-defender team pairs in main file: {main_data['unique']} out of {main_data['total']}")
print(f"Unique attackers: {main_data['attackers']}, unique defenders: {main_data['defenders']}")

main_data = count_unique_attacker_defender_teams(main_filename, is_jsonl=True, only_successful=True)
print(f"Number of unique successful attacker-defender team pairs in main file: {main_data['unique']} out of {main_data['total']}")
print(f"Unique attackers: {main_data['attackers']}, unique defenders: {main_data['defenders']}")

main_data = count_unique_attacker_defender_teams(main_filename, is_jsonl=True, only_unsuccessful=True)
print(f"Number of unique successful attacker-defender team pairs in main file: {main_data['unique']} out of {main_data['total']}")
print(f"Unique attackers: {main_data['attackers']}, unique defenders: {main_data['defenders']}")

#%%
# Run the function on the test file first
# Test file
test_data = count_unique_prefixes(test_filename, prefix_length=PREFIX_LENGTH)
print(f"Number of unique {PREFIX_LENGTH if PREFIX_LENGTH < 25000 else 'infinity'}-character prefixes in test file: {test_data['unique']} out of {test_data['total']}")

#%%
# Optionally, uncomment the following lines to run on the main file
# Main file
main_data = count_unique_prefixes(main_filename, prefix_length=PREFIX_LENGTH, is_jsonl=True)
print(f"Number of unique {PREFIX_LENGTH if PREFIX_LENGTH < 25000 else 'infinity'}-character prefixes in main file: {main_data['unique']} out of {main_data['total']}")

#%%
# Now only successful chats, test
test_data = count_unique_prefixes(test_filename, prefix_length=PREFIX_LENGTH, only_successful=True)
print(f"Number of successful unique {PREFIX_LENGTH if PREFIX_LENGTH < 25000 else 'infinity'}-character prefixes in test file: {test_data['unique']} out of {test_data['total']}")

#%%
# Now only successful chats, main
main_data = count_unique_prefixes(main_filename, prefix_length=PREFIX_LENGTH, is_jsonl=True, only_successful=True)
print(f"Number of successful unique {PREFIX_LENGTH if PREFIX_LENGTH < 25000 else 'infinity'}-character prefixes in main file: {main_data['unique']} out of {main_data['total']}")
# %%
