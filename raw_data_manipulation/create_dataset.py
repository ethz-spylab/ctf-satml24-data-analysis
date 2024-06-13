#%%
from huggingface_hub import HfFolder, Repository

# Define your dataset repository name and local folder
repo_name = "llm-ctf-satml24"  # Choose a name for your dataset
local_folder = "/data/projects/satml-llm-ctf-analysis/ctf-satml24"

# Make sure you're logged in
token = HfFolder.get_token()

#%%
# Create a new repository on the Hub (set `private=True` for a private dataset)
repo = Repository(local_folder, use_auth_token=token, repo_type="dataset")
# Copy your dataset files into `local_folder` before pushing

# Push to the Hub
repo.push_to_hub()

# %%
