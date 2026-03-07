"""Module for validating json file against (nested) schema"""

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from script.args_parser import parse_args_dict


def load_validators_in_folder(target_schema):
    """Loads (nested) schema into a registry"""
    folder = Path(target_schema).resolve().parent
    resources = []
    main_content = None

    for file_path in folder.glob("*.schema.json"):
        content = json.loads(file_path.read_text(encoding="utf-8"))
        resource = Resource.from_contents(content)
        resources.append((resource.id(), resource))
        if file_path.name == target_schema:
            main_content = content

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
    else:
        error_list = []
        for error in errors:
            error_path = " -> ".join([str(p) for p in error.path])
            error_list.append(f"❌ Error at [{error_path}]: {error.message}")

        with open("errors.txt", encoding="utf-8") as f:
            f.writelines(error_list)


if __name__ == "__main__":
    main()
