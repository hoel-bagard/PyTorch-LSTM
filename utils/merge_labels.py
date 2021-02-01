import argparse
import json
from pathlib import Path
import shutil
from typing import Dict


def main():
    parser = argparse.ArgumentParser("Script to merge multiple label files into one file")
    parser.add_argument("input_path", type=Path, help='Path to the folder with all the label files')
    parser.add_argument("--output_path", "--o", default='.', type=Path,
                        help='Path to the directory where the label file will be created')
    args = parser.parse_args()

    output_path: Path = args.output_path / "labels.json"
    assert not output_path.exists(), f"There is already a label file at {str(output_path)}"
    args.output_path.mkdir()

    files = args.input_path.glob("*.json")
    nb_files = len(files)

    class_dict: Dict = {
        'g': "glass",
        'h': "hair",
        'p': "plastic",
        's': "steel",
        'f': "fiber"
    }

    # Creates empty json
    aggregated_labels = {"entries": []}
    aggregated_entries = aggregated_labels["entries"]

    for file_index, file_name in enumerate(files):
        msg = f"Processing file {file_name},   ({file_index}/{nb_files})"
        print(msg + ' ' * (shutil.get_terminal_size(fallback=(156, 38)).columns - len(msg)), end="\r")

        with open(output_path) as json_file:
            json_data = json.load(json_file)
            entries = json_data["entries"]

        for entry in entries:
            file_path: str = entry["file_path"]
            file_path = file_path.split(sep='/')[1:]   # Removes the "data"
            sample_class = class_dict[file_path[0][0]]
            file_path = Path(sample_class, *file_path)
            entry["file_path"] = file_path
            aggregated_entries.append(entry)

    # Write everything to disk
    print(f"\nWriting labels to {output_path}")
    with open(output_path, 'w') as label_file:
        json.dump(aggregated_labels, label_file, indent=4)

    print("Finished labelling dataset")


if __name__ == "__main__":
    main()