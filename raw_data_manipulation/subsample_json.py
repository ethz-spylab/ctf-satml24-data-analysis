import json
import click
import os
from tqdm import tqdm
import random



@click.command()
@click.option('--input_file', '-i', help='Input JSONL file to subsample')
@click.option('--output_file', '-o', default=None, help='Output JSONL file to write the subsampled data')
@click.option('--sample_size', '-s', default=100, help='Size of the subsample')
@click.option('--criterion', '-c', default='random', help='Criterion to use for subsampling')
@click.option('--dump_json', is_flag=True, help='Dump a JSONL, not a JSON file')
def subsample_json(input_file : str, output_file : str, sample_size : int, criterion : str, dump_json : bool):
    # Read the input JSONL file
    data = []
    with open(input_file, 'r') as f:
        for i, line in enumerate(tqdm(f)):
            data.append(json.loads(line))

    print(f"Data is of length {len(data)}")

    # Subsample the data
    match criterion:
        case 'random':
            random.seed(42)
            random.shuffle(data)
            subsampled_data = data[:sample_size]
        case 'first':
            subsampled_data = data[:sample_size]
        case field:
            # check that this field exists in the data
            if field not in data[0]:
                raise ValueError(f"Unknown field: {field}")
            # get the first n examples with this field set to True
            subsampled_data = [x for x in data if x[field] is True]
            random.seed(42)
            random.shuffle(subsampled_data)
            subsampled_data = subsampled_data[:sample_size]

    print(f"Subsampled data is of length {len(subsampled_data)}")

    # If no output file is provided, default to e.g. filename.50.json
    if output_file is None:
        match criterion:
            case 'random':
                output_file = f"{os.path.splitext(input_file)[0]}.{sample_size}.json"
            case field:
                output_file = f"{os.path.splitext(input_file)[0]}.{field}.{sample_size}.json"


    if dump_json:
        # Write the subsampled data to the output JSON file
        with open(output_file, 'w') as f:
            json.dump(subsampled_data, f)
    else:
        # Write the subsampled data to the output JSONL file
        with open(output_file, 'w') as f:
            for line in subsampled_data:
                f.write(json.dumps(line) + '\n')

if __name__ == "__main__":
    subsample_json()

# Example usage: python subsample_json.py --input_file chat.json --sample_size 100
