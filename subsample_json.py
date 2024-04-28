import json
import click
import os
from tqdm import tqdm
import random

@click.command()
@click.option('--input_file', '-i', help='Input JSON file to subsample')
@click.option('--output_file', '-o', default=None, help='Output JSON file to write the subsampled data')
@click.option('--sample_size', '-s', default=100, help='Size of the subsample')
def subsample_json(input_file, output_file, sample_size):
    # Read the input JSONL file
    data = []
    with open(input_file, 'r') as f:
        for i, line in enumerate(tqdm(f)):
            data.append(json.loads(line))

    print(f"Data is of length {len(data)}")

    # Subsample the data
    random.seed(42)
    random.shuffle(data)
    subsampled_data = data[:sample_size]

    print(f"Subsampled data is of length {len(subsampled_data)}")

    # If no output file is provided, default to e.g. filename.50.json
    if output_file is None:
        output_file = f"{os.path.splitext(input_file)[0]}.{sample_size}.json"

    # Write the subsampled data to the output JSON file
    with open(output_file, 'w') as f:
        json.dump(subsampled_data, f)

if __name__ == "__main__":
    subsample_json()

# Example usage: python subsample_json.py --input_file chat.json --sample_size 100
