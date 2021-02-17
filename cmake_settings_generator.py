from dataclasses import dataclass, asdict
from enum import Enum, auto
from typing import List, TypeVar, Generic
import json


class NameableEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class CmakeVarType(NameableEnum):
    BOOL = auto()
    FILEPATH = auto()
    INTERNAL = auto()
    PATH = auto()
    STRING = auto()

    def _generate_next_value_(name, start, count, last_values):
        return name


@dataclass(frozen=True)
class CmakeVariable:
    """Data container for representing a Cmake Variable within the JSON file."""
    name: str
    value: str
    type: CmakeVarType


@dataclass(frozen=True)
class BuildConfig:
    """Data container for representing a CMAKE Build Configuration within the JSON file."""
    name: str
    generator: str
    configurationType: str
    inheritEnvironments: str  #ToDo: Convert to an enum after finding microsoft API doc
    installRoot: str
    cmakeCommandArgs: str
    buildCommandArgs: str
    ctestCommandArgs: str
    variables: List[CmakeVariable]
    buildRoot: str
    installRoot: str


# Generic type used for parsing in user input while maintaining type hints (Dynamic typing sucks)
T = TypeVar('T')


def get_user_input_for_value(message: str, return_type: Generic[T]) -> T:
    """Prompts a user for a given value and returns a typed version of the data according to the user provided
    generic"""
    #ToDo: Add a system for printing verbose output according to script arguments.
    return return_type(input(message))


def prompt_user_to_add_cmake_var() -> bool:
    """Prompt a user to determine weather or not to add cmake_vars to the build config and return a boolean."""
    add_cmake_var: str = get_user_input_for_value("Do you have any Cmake vars to add? (y/n): ", str).lower()
    while add_cmake_var not in ["y", "n"]:
        print("Invalid choice. Use (y) for yes. (n) for No.")
        add_cmake_var = get_user_input_for_value("Do you have any Cmake vars to add? (y/n): ", str).lower()

    # Return boolean value that represents weather the user wants to add a variable to the configuration
    return add_cmake_var == "y"


def get_cmake_vars_from_user() -> List[CmakeVariable]:
    """Get all cmake vars from a given user for a provided build configuration."""
    cmake_variables: List[CmakeVariable] = []
    while prompt_user_to_add_cmake_var():
        try:
            cmake_variables.append(CmakeVariable(
                get_user_input_for_value("Cmake Variable Name: ", str),
                get_user_input_for_value("Cmake Variable Value: ", str),
                get_user_input_for_value("Cmake Variable Type: ", CmakeVarType)
            ))
        except ValueError as e:
            print(f"Invalid CmakeVarType: {e}. Ignoring variable. Enter variable info again.")

    return cmake_variables


def build_config_from_user_input() -> BuildConfig:
    """Helper method to prompt the user and build data container object from input."""
    project_dir: str = get_user_input_for_value("Cmake Project Directory: ", str)
    name: str = get_user_input_for_value("Project Config Name: ", str)
    generator: str = get_user_input_for_value("Generator: ", str)
    configurationType: str = get_user_input_for_value("Configuration Type: ", str)
    inheritEnvironments: str = get_user_input_for_value("Inherit Environments: ", str)
    buildRoot: str = r"${projectDir}\\out\\build\\${name}"
    installRoot: str = r"${projectDir}\\out\\install\\${name}"
    cmakeCommandArgs: str = get_user_input_for_value("Cmake Command Args: ", str)
    buildCommandArgs: str = get_user_input_for_value("Build Command Args: ", str)
    ctestCommandArgs: str = get_user_input_for_value("Ctest Command Args: ", str)
    variables: List[CmakeVariable] = get_cmake_vars_from_user()

    # Build object and return it to function user
    return BuildConfig(name=name,
                       generator=generator,
                       configurationType=configurationType,
                       inheritEnvironments=inheritEnvironments,
                       buildRoot=buildRoot,
                       installRoot=installRoot,
                       cmakeCommandArgs=cmakeCommandArgs,
                       buildCommandArgs=buildCommandArgs,
                       ctestCommandArgs=ctestCommandArgs,
                       variables=variables)



# Main -------------------------
v = build_config_from_user_input()
print()
print(f"Generated Build Config ({v.name}):")
print(json.dumps(asdict(v), indent=2))

#ToDo: Parse data classes to JSON and write to the project_dir

#ToDo: Notify the user that they can acheive the same resulst with a constructed Cmake command (in terms of build systems)