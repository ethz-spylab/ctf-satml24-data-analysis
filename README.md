# Dataset and Lessons Learned from the 2024 SaTML LLM Capture-the-Flag Competition

Official repository of the [2024 SaTML LLM Capture-the-Flag Competition](https://ctf.spylab.ai/) led by [Edoardo Debenedetti](https://edoardo.science), [Javier Rando](https://javirando.com) and [Daniel Paleka](https://danielpaleka.com).

**Competition report**: https://arxiv.org/abs/2406.07954

**Dataset**: https://huggingface.co/datasets/ethz-spylab/ctf-satml24

----

### Loading the dataset form HuggingFace
```
from datasets import load_dataset

defenses = load_dataset("ethz-spylab/ctf-satml24", "defense")["valid"]

teams = load_dataset("ethz-spylab/ctf-satml24", "teams")["defense_teams"]

chats = load_dataset("ethz-spylab/ctf-satml24", "interaction_chats")["attack"]
```

----

### Analyzing the data

We provide a script `chat_diversity.py` to perform some basic analysis on the dataset that we include in our official report. The folder `raw_data_manipulation` includes transformations we performed on the raw data we collected from the competition. Please, reach to us if you think you need the original raw data.