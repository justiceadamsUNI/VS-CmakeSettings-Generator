from dataclasses import dataclass
from enum import Enum, auto


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
    """Data container for representing a Cmake Variable within the JSON file."""
    name: str
    generator: str
    configurationType: str
    inheritEnvironments: str  #ToDo: Convert to an enum after finding microsoft API doc
    buildRoot: str
    installRoot: str
    cmakeCommandArgs: str
    buildCommandArgs: str
    ctestCommandArgs: str
    type: CmakeVarType


#ToDo: 1.) Create an interface to parse user input to the data classes with error checking (multiple buildconfigs)
#ToDo: 2.) Parse data classes to JSON
#ToDo: 3.) Write json to CMAKEList folder
#ToDo: 3.) Notify the user that they can acheive the same resulst with a constructed Cmake command (in terms of build systems)