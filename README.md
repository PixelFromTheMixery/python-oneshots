# One-shot scripts I had a use for
Mini scripts I've used as exercises and tools for my games. I hope they help you too.

## 🍪 List of treats
### CLI Tools
[`csv_to_yaml.py`](#csv_to_yamlpy) - Uses CSV header as keys for a list of YAML mappings

### Script Tools
[`args_parse.py`](#args_parserpy) - Returns a namespace object to use based on supplied dictionary

[`validate_json.py`](#validate_jsonpy) - Validates json file against (nested) schema

# CLI Tools
## [`csv_to_yaml.py`](./cli/csv_to_yaml.py)
Uses CSV header as keys for a list of YAML mappings
- Best used in same directory
- Initially used for exporting Notion database export to YAML
- Supports basic data types only
  - Contained array turned into `,` seperated string as a workaround

### Requires
- module: yaml
- sibling: args_parser.py

### Parameters
| Parameter | Type | Defaults |
|---|---|---|
| input_file | string | None |
| output_file | string | None |

### Potential expansion
- Decoupling from my other tool
- I am likely to make a YAML to JSON converter as Godot prefers JSON
- Support for more types

[Back to top](#-list-of-treats)

## [`validate_json.py`](./cli/validate_json.py)
Validates json file against (nested) schema
- Reads JSON at path
- Takes parent folder of target schema
  - Add all schema in folder into registry
  - Target schema is main content
- Outputs errors as local errors.txt file with location and issue

### Requires
- module: jsonschema
- sibling: args_parser.py


### Parameters
| Parameter | Type | Defaults |
|---|---|---|
| json | string | None |
| schema | string | None |

### Potential expansion
None yet

[Back to top](#-list-of-treats)

# Script Tools
## [`args_parser.py`](./code/args_parser.py)
Returns a namespace object to use based on supplied dictionary
- Has verbosity stored true by default 
- Accepts name, description, and epilogue (default to "Good luck")
- Accepts argument types
  - Positonal (name)
  - Optional (flag)
  - Switch (store_true)

### Requires
- module: pydantic

### Paramters
| Parameter | Type | Defaults |
|---|---|---|
| parse_dict | Dictionary | None |

### Potential expansion 
- Decoupling from my other tool
- Pydantic can be an option rather than a requirement but I do love being pedantic

[Back to top](#-list-of-treats)

# Template
## `Template`
Description, likely docstring

### Requires
Modules, etc

### Parameters
| Parameter | Type | Defaults |
|---|---|---|
|  |  |  |

### Potential expansion
- Issues
- Intentions
- Pipedreams

[Back to top](#-list-of-treats)
