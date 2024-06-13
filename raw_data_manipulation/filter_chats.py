#%%
import json
from tqdm import tqdm
from utils import PATH

def filter_empty_chats(filename, output_filename, is_jsonl=False):
    """
    Remove all entries of the chat file that have an empty chat history.
    
    Args:
    filename (str): Path to the JSON file containing chat data.
    output_filename (str): Path to the output JSON file to save filtered data.
    is_jsonl (bool): Whether the input file is in JSONL format.
    
    Returns:
    int: Number of entries removed.
    """
    with open(filename, 'r') as file:
        if is_jsonl:
            chats = []
            for line in tqdm(file):
                chats.append(json.loads(line))
        else:
            chats = json.load(file)
    
    initial_count = len(chats)
    filtered_chats = [chat for chat in chats if chat['history'] and len(chat['history']) > 0]
    removed_count = initial_count - len(filtered_chats)
    
    with open(output_filename, 'w') as outfile:
        if is_jsonl:
            for chat in tqdm(filtered_chats):
                outfile.write(json.dumps(chat) + '\n')
        else:
            json.dump(filtered_chats, outfile, indent=4)
    
    return removed_count

# Path to the dataset
dataset_path = PATH

#%%
test_filename = f"{dataset_path}/chat.120.json"
main_filename = f"{dataset_path}/chat.json"
output_test_filename = f"{dataset_path}/filtered_chat.120.json"
output_main_filename = f"{dataset_path}/filtered_chat.json"

# Run the filter function on the test file first
removed_count_test = filter_empty_chats(test_filename, output_test_filename)
print(f"Number of entries removed from test file: {removed_count_test}")

#%%
# Now run the filter function on the main file
removed_count_main = filter_empty_chats(main_filename, output_main_filename, is_jsonl=True)
print(f"Number of entries removed from main file: {removed_count_main}")



# %%
