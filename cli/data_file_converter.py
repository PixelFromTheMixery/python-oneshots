"""Converts files"""

import csv
import json

import yaml

from script.args_parser import parse_args_dict

ENCODING = "utf-8"
INPUT_MAP = {
    "csv": "csv_pull",
    "json": "json_pull",
    "yaml": "yaml_pull",
}
OUTPUT_LIST = ["json", "yaml"]


# Pulls
def csv_pull(f):
    """Uses CSV header as mappings for list of Dictionaries"""
    csv_data = []

    reader = csv.reader(f, delimiter=",")
    for _, line in enumerate(reader):
        csv_data.append(line)

    dict_keys = csv_data[0]

    data = []
    for line in range(1, len(csv_data)):
        data_dict = {}
        for item in range(len(csv_data[line])):
            if csv_data[line][item] == "":
                data_dict[dict_keys[item]] = None
            elif csv_data[line][item].isdigit():
                data_dict[dict_keys[item]] = int(csv_data[line][item])
            else:
                data_dict[dict_keys[item]] = csv_data[line][item]
        data.append(data_dict)

    return data


def json_pull(f):
    """Basic JSON pull"""
    return json.load(f)


def yaml_pull(f):
    """Basic YAML pull"""
    return yaml.safe_load(f)


# Converter
def converter(data, output_type):
    """Central converter script for exports"""
    if output_type == "json":
        return json.dumps(data)
    if output_type == "yaml":
        return yaml.dump(data)


def main():
    """File converter"""
    args = parse_args_dict(
        {
            "name": "Data file converter",
            "info": """
YAML > JSON:
Direct mapping
CSV > YAML:
Takes top row of csv and creates a YAML file with a scalar of mappings
""",
            "args": [
                {"style": "basic", "name": "input_file"},
                {"style": "basic", "name": "output_file"},
            ],
        }
    )
    input_type = args.input_file.split(".")[-1]
    output_type = args.output_file.split(".")[-1]

    handler_name = INPUT_MAP.get(input_type)

    if not handler_name:
        print("❌ Source extension not supported: " + input_type)
        print("Following types supported:")
        for key in INPUT_MAP:
            print("- " + key)
        exit(1)

    if output_type not in OUTPUT_LIST:
        print("❌ Target extension not supported: " + input_type)
        print("Following types supported:")
        for key in OUTPUT_LIST:
            print("- " + key)
        exit(1)

    print(f"✅ Compatible combination found: {input_type} > {output_type}")

    data = None
    with open(args.input_file, "r", encoding=ENCODING) as f:
        handler = globals()[handler_name]
        data = handler(f)

    converted = converter(data, output_type)

    with open(args.output_file, "w", encoding=ENCODING) as f:
        f.write(converted)


if __name__ == "__main__":
    main()
