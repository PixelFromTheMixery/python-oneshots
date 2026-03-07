"""Utility module for processing cli parsers"""

import argparse
from typing import Optional

from pydantic import BaseModel


class Arguments(BaseModel):
    """Argument to add to parser. Currently very basic"""

    style: str
    name: Optional[str] = None
    flag: Optional[str] = None
    short_flag: Optional[str] = None
    boolean: Optional[bool] = None


class ParseObject(BaseModel):
    """Parser object to turn into real parser object"""

    name: str
    info: str
    epilog: Optional[str] = "Good luck"
    args: list[Arguments]


def parse_args_dict(parse_dict: dict):
    """returns a namespace object to use by consuming scripts"""
    parse_obj = ParseObject.model_validate(parse_dict)
    parser = argparse.ArgumentParser(
        prog=parse_obj.name,
        description=parse_obj.info,
        epilog=parse_obj.epilog,
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    for arg in parse_obj.args:
        if arg.style == "basic":
            parser.add_argument(arg.name)
        elif arg.style == "optional":
            parser.add_argument(
                arg.short_flag if arg.short_flag else arg.flag[0], arg.flag
            )
        elif arg.style == "boolean":
            parser.add_argument(arg.short_flag, arg.flag, action="store_true")

    return parser.parse_args()
