"""Converts csv file to yaml file"""

import csv

import yaml

from script.args_parser import parse_args_dict


def main():
    """Uses CSV header as mappings for list of YAML mappings"""
    args = parse_args_dict(
        {
            "name": "CSV to YAML converter",
            "info": "Takes top row of csv and creates a YAML file with a scalar of mappings",
            "args": [
                {"style": "basic", "name": "input_file"},
                {"style": "basic", "name": "output_file"},
            ],
        }
    )

    csv_data = []

    with open(args.input_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        for _, line in enumerate(reader):
            csv_data.append(line)

    dict_keys = csv_data[0]

    yaml_data = []
    for line in range(1, len(csv_data)):
        yaml_dict = {}
        for item in range(len(csv_data[line])):
            if csv_data[line][item] == "":
                yaml_dict[dict_keys[item]] = None
            elif csv_data[line][item].isdigit():
                yaml_dict[dict_keys[item]] = int(csv_data[line][item])
            else:
                yaml_dict[dict_keys[item]] = csv_data[line][item]
        yaml_data.append(yaml_dict)

    yaml_obj = yaml.dump(yaml_data)

    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(yaml_obj)


if __name__ == "__main__":
    main()
