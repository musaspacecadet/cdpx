"""
Defines the intermediate Python object model (dataclasses) representing
the structure parsed from the CDP JSON specification.
"""

import typing
from dataclasses import dataclass, field
from enum import Enum, auto

# --- Enums ---

class CdpType(Enum):
    """Enumerates the fundamental types of CDP type definitions."""
    STRING = auto()
    NUMBER = auto()
    INTEGER = auto()
    BOOLEAN = auto()
    OBJECT = auto()
    ARRAY = auto()
    ANY = auto()
    # Special case for string types with an explicit enum list
    STRING_ENUM = auto()


# --- Core Building Blocks ---

@dataclass(frozen=True)
class ItemDetails:
    """Details about the type of items within an array."""
    # Represents the type, can be a primitive ('string', 'integer')
    # or a reference ('Domain.TypeId').
    type_ref: str


@dataclass(frozen=True)
class FieldDefinition:
    """
    Represents a field within an object, a parameter, or a return value.
    Using frozen=True makes these effectively immutable after creation.
    """
    name: str
    description: typing.Optional[str]
    is_optional: bool
    is_experimental: bool
    is_deprecated: bool
    # Represents the type, can be primitive ('string', 'integer')
    # or a reference ('Domain.TypeId'). None if it's an array type.
    type_ref: typing.Optional[str]
    # Details about array items, only present if this field is an array.
    items: typing.Optional[ItemDetails] = None
    # Enum values if defined inline *on the parameter/property itself* (less common)
    enum_values: typing.Optional[typing.List[str]] = None

    # You could add a 'python_name: str = field(init=False)' here
    # and calculate it in __post_init__ using a utility if desired,
    # but keeping the model pure to the spec first is also valid.


# --- Top-Level Definitions ---

@dataclass(frozen=True)
class TypeDefinition:
    """Represents a named type defined within a domain."""
    domain_name: str  # Keep track of which domain it belongs to
    id: str           # The unique ID of the type within the domain (e.g., 'Frame')
    description: typing.Optional[str]
    type: CdpType     # The fundamental type (object, string, array, etc.)
    is_experimental: bool
    is_deprecated: bool
    # For type == ARRAY
    items: typing.Optional[ItemDetails] = None
    # For type == OBJECT
    properties: typing.List[FieldDefinition] = field(default_factory=list)
    # For type == STRING_ENUM (or STRING with enum values)
    enum_values: typing.Optional[typing.List[str]] = None


@dataclass(frozen=True)
class CommandDefinition:
    """Represents a command defined within a domain."""
    domain_name: str
    name: str
    description: typing.Optional[str]
    is_experimental: bool
    is_deprecated: bool
    parameters: typing.List[FieldDefinition] = field(default_factory=list)
    returns: typing.List[FieldDefinition] = field(default_factory=list)
    redirect: typing.Optional[str] = None # Target domain if this command redirects


@dataclass(frozen=True)
class EventDefinition:
    """Represents an event defined within a domain."""
    domain_name: str
    name: str
    description: typing.Optional[str]
    is_experimental: bool
    is_deprecated: bool
    parameters: typing.List[FieldDefinition] = field(default_factory=list)


# --- Domain and Protocol Aggregation ---

@dataclass(frozen=True)
class DomainDefinition:
    """Represents a complete domain parsed from the specification."""
    name: str
    description: typing.Optional[str]
    is_experimental: bool
    is_deprecated: bool
    dependencies: typing.List[str] = field(default_factory=list)
    # Using dicts for quick lookup by name/id
    types: typing.Dict[str, TypeDefinition] = field(default_factory=dict)
    commands: typing.Dict[str, CommandDefinition] = field(default_factory=dict)
    events: typing.Dict[str, EventDefinition] = field(default_factory=dict)


@dataclass(frozen=True)
class ProtocolDefinition:
    """Represents the entire parsed CDP protocol."""
    version_major: str
    version_minor: str
    domains: typing.Dict[str, DomainDefinition] = field(default_factory=dict)