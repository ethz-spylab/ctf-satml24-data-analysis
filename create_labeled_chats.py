import json                                                               
from pathlib import Path                                                  
                                                                            
PATH = Path("/data/projects/satml-llm-ctf-analysis/ctf-satml24")          
                                                                            
# Step 1: Read secret_guess.json and build a mapping from chat id to guess outcome                                                                     
chat_id_to_outcome = {}                                                   
with open(PATH / 'secret_guess.json', 'r') as guesses_file:               
    for line in guesses_file:                                             
        guess = json.loads(line)                                          
        chat_id = guess["chat"]["$id"]["$oid"]                            
        outcome = guess["success"]                                        
        chat_id_to_outcome[chat_id] = outcome                             
                                                                            
# Step 2: Read chat.json and label each chat based on the guess outcome   
labeled_chats = []                                                        
with open(PATH / 'chat.json', 'r') as chats_file:                         
    for line in chats_file:                                               
        chat = json.loads(line)                                           
        chat_id = chat["_id"]["$oid"]                                     
        if chat_id in chat_id_to_outcome:                                 
            chat["attack_success"] = chat_id_to_outcome[chat_id]          
            labeled_chats.append(chat)                                    
                                                                            
# Step 3: Save the labeled chats to a new file                            
with open(PATH / 'labeled_chats.json', 'w') as labeled_file:              
    for chat in labeled_chats:                                            
        labeled_file.write(json.dumps(chat) + '\n')                       
                                                                            
print(f"Labeled chats have been saved to {PATH / 'labeled_chats.json'}")  
                                                                              