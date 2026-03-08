"""Module for validating json file against (nested) schema"""

import json
import os
from pathlib import Path


from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from script.args_parser import parse_args_dict


def load_validators_in_folder(target_schema):
    """Loads (nested) schema into a registry"""
    target_path = Path(target_schema).resolve()
    folder = target_path.parent
    resources = []
    main_content = None

    for file_path in folder.glob("*.schema.json"):
        current_file = file_path.resolve()

        content = json.loads(current_file.read_text(encoding="utf-8"))
        resource = Resource.from_contents(content)
        print(f"Indexed: {resource.id()}")
        resources.append((resource.id(), resource))
        if current_file == target_path:
            main_content = content

    if main_content is None:
        raise FileNotFoundError(f"Could not identify the main schema at {target_path}")

    registry = Registry().with_resources(resources)

    return Draft202012Validator(main_content, registry=registry)


def main():
    """
    Args
    Loads both files
    Validates and collects errors
    Prints errors
    """
    args = parse_args_dict(
        {
            "name": "Json Validator",
            "info": "Validates JSON against schema",
            "args": [
                {"style": "basic", "name": "json"},
                {"style": "basic", "name": "schema"},
            ],
        }
    )
    with open(args.json, encoding="utf-8") as d:
        data = json.load(d)

    validator = load_validators_in_folder(args.schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

    if not errors:
        print(f"✅ {args.json} is clean!")
        if os.path.exists("errors.txt"):
            os.remove("errors.txt")
    else:
        error_list = []
        for error in errors:
            error_path = " -> ".join([str(p) for p in error.path])
            error_list.append(f"❌ Error at [{error_path}]: {error.message}")

        with open("errors.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(error_list))


if __name__ == "__main__":
    main()
