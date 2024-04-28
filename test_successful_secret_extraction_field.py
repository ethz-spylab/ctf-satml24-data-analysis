import json
from tqdm import tqdm
from utils import PATH

# Define the path to the updated chat file
updated_chat_path = PATH /"chat_updated.json"

# Function to read a sample of entries and verify the new field
def test_successful_secret_extraction():
    # Counter for the number of entries tested
    tested_entries = 0
    # Counter for the number of entries with the correct new field
    correct_entries = 0

    successful_secret_extraction_entries = {'all': 0, 'evaluation': 0, 'recon': 0}
    eval_chats = 0

    # Open the updated chat file and read a sample of entries
    with open(updated_chat_path, 'r') as updated_chats_file:
        for i, line in tqdm(enumerate(updated_chats_file)):
            chat = json.loads(line)
            # Check if the 'was_successful_secret_extraction' field exists and is a boolean
            if 'was_successful_secret_extraction' in chat and isinstance(chat['was_successful_secret_extraction'], bool):
                correct_entries += 1
                if chat['is_evaluation']:
                    eval_chats += 1
                if chat['was_successful_secret_extraction']:
                    successful_secret_extraction_entries['all'] += 1
                    if chat['is_evaluation']:
                        successful_secret_extraction_entries['evaluation'] += 1
                    else:
                        successful_secret_extraction_entries['recon'] += 1

            tested_entries += 1

    # Print the test results
    print(f"Tested {tested_entries} entries.")
    print(f"{correct_entries} entries have the 'was_successful_secret_extraction' field.")
    print(f"{eval_chats} of these chats have 'is_evaluation' set to True.")
    print("Successful secret extraction entries:")
    for key, value in successful_secret_extraction_entries.items():
        print(f"{key}: {value}")


# Run the test function
if __name__ == "__main__":
    test_successful_secret_extraction()
