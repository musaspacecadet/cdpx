"""
Parses CDP JSON specification data into the intermediate object model
defined in models.py.
"""

import json
import typing
from pathlib import Path
import logging

from .models import (
    ProtocolDefinition, DomainDefinition, TypeDefinition, CommandDefinition,
    EventDefinition, FieldDefinition, ItemDetails, CdpType
)
from .exceptions import CdpParsingError, FileFormatError, DefinitionError
from .utils import check_key # Optional utility


logger = logging.getLogger(__name__)

# --- Private Parsing Helpers ---

def _parse_item_details(item_data: dict, context: str) -> ItemDetails:
    """Parses the 'items' block for arrays."""
    if not isinstance(item_data, dict):
        raise DefinitionError(f"Expected 'items' to be an object in {context}, got {type(item_data)}")

    type_ref = item_data.get('$ref')
    if not type_ref:
        type_ref = item_data.get('type')
    if not type_ref:
        raise DefinitionError(f"Missing '$ref' or 'type' in items definition for {context}")

    # Could add more validation here if needed (e.g., ensure only one is present)
    return ItemDetails(type_ref=type_ref)


def _parse_field_list(field_data_list: list, context: str) -> typing.List[FieldDefinition]:
    """Parses a list of fields (parameters, returns, properties)."""
    fields = []
    if not isinstance(field_data_list, list):
         raise DefinitionError(f"Expected list for fields in {context}, got {type(field_data_list)}")

    for i, field_data in enumerate(field_data_list):
         field_context = f"{context} field {i} ('{field_data.get('name', 'unknown')}')"
         try:
             fields.append(_parse_field_definition(field_data, field_context))
         except (KeyError, DefinitionError) as e:
             logger.warning(f"Skipping invalid field definition in {field_context}: {e}")
             # Or re-raise if strictness is required: raise DefinitionError(f"Invalid field in {field_context}") from e
         except Exception as e:
             logger.error(f"Unexpected error parsing {field_context}: {e}", exc_info=True)
             raise DefinitionError(f"Unexpected error parsing {field_context}") from e # Or skip

    return fields


def _parse_field_definition(field_data: dict, context: str) -> FieldDefinition:
    """Parses a single field (property, parameter, return value)."""
    if not isinstance(field_data, dict):
        raise DefinitionError(f"Expected field definition to be an object in {context}, got {type(field_data)}")

    check_key(field_data, 'name', context) # Ensure name exists

    name = field_data['name']
    field_type = field_data.get('type')
    type_ref = field_data.get('$ref')
    items_data = field_data.get('items')
    items_details = None

    if items_data:
        if field_type and field_type != 'array':
            logger.warning(f"'items' present but type is '{field_type}' (expected 'array') in {context}")
        items_details = _parse_item_details(items_data, f"items block of {context}")
        type_ref = None # Field type is determined by items
    elif type_ref:
        if field_type:
             logger.debug(f"Both '$ref' ('{type_ref}') and 'type' ('{field_type}') found in {context}, using '$ref'.")
        # type_ref already set
    elif field_type:
        type_ref = field_type # Use primitive type name as reference
    else:
        # Sometimes 'any' type has neither $ref nor type explicitly
        if field_data.get('description', '').lower().strip() == 'any':
             type_ref = 'any'
             logger.debug(f"Assuming 'any' type based on description for {context}")
        else:
             raise DefinitionError(f"Field must have '$ref', 'type', or 'items' in {context}")


    return FieldDefinition(
        name=name,
        description=field_data.get('description'),
        is_optional=field_data.get('optional', False),
        is_experimental=field_data.get('experimental', False),
        is_deprecated=field_data.get('deprecated', False),
        type_ref=type_ref,
        items=items_details,
        enum_values=field_data.get('enum') # Enum on field itself
    )


def _parse_type_definition(type_data: dict, domain_name: str) -> TypeDefinition:
    """Parses a single type definition from the 'types' list."""
    context = f"type '{type_data.get('id', 'unknown')}' in domain '{domain_name}'"
    if not isinstance(type_data, dict):
        raise DefinitionError(f"Expected type definition to be an object for {context}, got {type(type_data)}")

    check_key(type_data, 'id', context)
    check_key(type_data, 'type', context)

    type_id = type_data['id']
    cdp_type_str = type_data['type']
    items_data = type_data.get('items')
    properties_data = type_data.get('properties', [])
    enum_data = type_data.get('enum')

    type: CdpType
    items_details: typing.Optional[ItemDetails] = None
    properties: typing.List[FieldDefinition] = []

    if cdp_type_str == 'object':
        type = CdpType.OBJECT
        properties = _parse_field_list(properties_data, f"properties of {context}")
    elif cdp_type_str == 'array':
        type = CdpType.ARRAY
        if not items_data:
            raise DefinitionError(f"Type is 'array' but 'items' is missing in {context}")
        items_details = _parse_item_details(items_data, f"items block of {context}")
    elif cdp_type_str == 'string':
        type = CdpType.STRING_ENUM if enum_data else CdpType.STRING
    elif cdp_type_str == 'integer':
        type = CdpType.INTEGER
    elif cdp_type_str == 'number':
        type = CdpType.NUMBER
    elif cdp_type_str == 'boolean':
        type = CdpType.BOOLEAN
    elif cdp_type_str == 'any':
        type = CdpType.ANY
    else:
        raise DefinitionError(f"Unknown CDP type string '{cdp_type_str}' in {context}")

    # Sanity checks
    if type != CdpType.OBJECT and properties_data:
        logger.warning(f"'properties' found but type is '{cdp_type_str}' in {context}")
    if type != CdpType.ARRAY and items_data:
        logger.warning(f"'items' found but type is '{cdp_type_str}' in {context}")
    if type not in (CdpType.STRING, CdpType.STRING_ENUM) and enum_data:
        logger.warning(f"'enum' found but type is '{cdp_type_str}' in {context}")

    return TypeDefinition(
        domain_name=domain_name,
        id=type_id,
        description=type_data.get('description'),
        type=type,
        is_experimental=type_data.get('experimental', False),
        is_deprecated=type_data.get('deprecated', False),
        items=items_details,
        properties=properties,
        enum_values=enum_data,
    )


def _parse_command_definition(command_data: dict, domain_name: str) -> CommandDefinition:
    """Parses a single command definition."""
    context = f"command '{command_data.get('name', 'unknown')}' in domain '{domain_name}'"
    if not isinstance(command_data, dict):
        raise DefinitionError(f"Expected command definition to be an object for {context}, got {type(command_data)}")

    check_key(command_data, 'name', context)
    name = command_data['name']

    parameters = _parse_field_list(command_data.get('parameters', []), f"parameters of {context}")
    returns = _parse_field_list(command_data.get('returns', []), f"returns of {context}")

    return CommandDefinition(
        domain_name=domain_name,
        name=name,
        description=command_data.get('description'),
        is_experimental=command_data.get('experimental', False),
        is_deprecated=command_data.get('deprecated', False),
        parameters=parameters,
        returns=returns,
        redirect=command_data.get('redirect'),
    )


def _parse_event_definition(event_data: dict, domain_name: str) -> EventDefinition:
    """Parses a single event definition."""
    context = f"event '{event_data.get('name', 'unknown')}' in domain '{domain_name}'"
    if not isinstance(event_data, dict):
         raise DefinitionError(f"Expected event definition to be an object for {context}, got {type(event_data)}")

    check_key(event_data, 'name', context)
    name = event_data['name']

    parameters = _parse_field_list(event_data.get('parameters', []), f"parameters of {context}")

    return EventDefinition(
        domain_name=domain_name,
        name=name,
        description=event_data.get('description'),
        is_experimental=event_data.get('experimental', False),
        is_deprecated=event_data.get('deprecated', False),
        parameters=parameters,
    )


def _parse_domain_definition(domain_data: dict) -> DomainDefinition:
    """Parses a single domain from the 'domains' list."""
    context = f"domain '{domain_data.get('domain', 'unknown')}'"
    if not isinstance(domain_data, dict):
        raise DefinitionError(f"Expected domain definition to be an object, got {type(domain_data)}")

    check_key(domain_data, 'domain', context)
    domain_name = domain_data['domain']
    context = f"domain '{domain_name}'" # Update context with actual name

    types: typing.Dict[str, TypeDefinition] = {}
    commands: typing.Dict[str, CommandDefinition] = {}
    events: typing.Dict[str, EventDefinition] = {}

    for type_data in domain_data.get('types', []):
        try:
            type_def = _parse_type_definition(type_data, domain_name)
            if type_def.id in types:
                 logger.warning(f"Duplicate type ID '{type_def.id}' found in {context}. Overwriting.")
            types[type_def.id] = type_def
        except DefinitionError as e:
            logger.warning(f"Skipping invalid type definition in {context}: {e}")
        except Exception as e:
             type_id = type_data.get('id', 'unknown')
             logger.error(f"Unexpected error parsing type '{type_id}' in {context}: {e}", exc_info=True)
             # Decide whether to skip or raise

    for command_data in domain_data.get('commands', []):
        try:
            command_def = _parse_command_definition(command_data, domain_name)
            if command_def.name in commands:
                 logger.warning(f"Duplicate command name '{command_def.name}' found in {context}. Overwriting.")
            commands[command_def.name] = command_def
        except DefinitionError as e:
            logger.warning(f"Skipping invalid command definition in {context}: {e}")
        except Exception as e:
            cmd_name = command_data.get('name', 'unknown')
            logger.error(f"Unexpected error parsing command '{cmd_name}' in {context}: {e}", exc_info=True)


    for event_data in domain_data.get('events', []):
        try:
            event_def = _parse_event_definition(event_data, domain_name)
            if event_def.name in events:
                 logger.warning(f"Duplicate event name '{event_def.name}' found in {context}. Overwriting.")
            events[event_def.name] = event_def
        except DefinitionError as e:
            logger.warning(f"Skipping invalid event definition in {context}: {e}")
        except Exception as e:
            evt_name = event_data.get('name', 'unknown')
            logger.error(f"Unexpected error parsing event '{evt_name}' in {context}: {e}", exc_info=True)


    return DomainDefinition(
        name=domain_name,
        description=domain_data.get('description'),
        is_experimental=domain_data.get('experimental', False),
        is_deprecated=domain_data.get('deprecated', False),
        dependencies=domain_data.get('dependencies', []),
        types=types,
        commands=commands,
        events=events,
    )


# --- Public Parsing Function ---

def parse_protocol_files(*json_paths: Path) -> ProtocolDefinition:
    """
    Parses one or more CDP JSON protocol files into a single ProtocolDefinition.

    Args:
        *json_paths: Path objects pointing to the JSON specification files.

    Returns:
        A ProtocolDefinition object representing the combined protocol.

    Raises:
        FileNotFoundError: If any json_path does not exist.
        FileFormatError: If JSON decoding fails or top-level keys are missing.
        CdpParsingError: For errors during definition parsing (potentially logged warnings).
    """
    all_domains: typing.Dict[str, DomainDefinition] = {}
    protocol_version_major = "unknown"
    protocol_version_minor = "unknown"
    first_file = True

    for json_path in json_paths:
        logger.info(f"Processing protocol file: {json_path}")
        if not json_path.is_file():
            raise FileNotFoundError(f"Protocol file not found: {json_path}")

        try:
            with json_path.open('r', encoding='utf-8') as f:
                schema = json.load(f)
        except json.JSONDecodeError as e:
            raise FileFormatError(f"Invalid JSON in file {json_path}: {e}") from e
        except Exception as e:
            raise CdpParsingError(f"Error reading file {json_path}: {e}") from e

        if not isinstance(schema, dict):
             raise FileFormatError(f"Expected JSON root to be an object in {json_path}, got {type(schema)}")

        # Version - Take from the first file, warn if subsequent files differ
        version_info = schema.get('version', {})
        if not isinstance(version_info, dict):
             logger.warning(f"Invalid 'version' format in {json_path}, expected object.")
             major, minor = "unknown", "unknown"
        else:
             major = version_info.get('major', 'unknown')
             minor = version_info.get('minor', 'unknown')

        if first_file:
            protocol_version_major = major
            protocol_version_minor = minor
            first_file = False
            logger.info(f"Using protocol version {major}.{minor} from {json_path}")
        elif (major != protocol_version_major or minor != protocol_version_minor):
             logger.warning(
                 f"Protocol version mismatch in {json_path} ({major}.{minor}) "
                 f"does not match initial version ({protocol_version_major}.{protocol_version_minor}). "
                 f"Keeping initial version."
             )

        # Domains
        domains_list = schema.get('domains')
        if not isinstance(domains_list, list):
            raise FileFormatError(f"Missing or invalid 'domains' list in {json_path}")

        for domain_data in domains_list:
            try:
                domain_def = _parse_domain_definition(domain_data)
                if domain_def.name in all_domains:
                    # This can happen if domains are split across files (e.g., browser vs js)
                    # We might need a strategy to merge them later if required.
                    # For now, let's assume the last one wins or log a warning.
                    logger.warning(f"Domain '{domain_def.name}' redefined in {json_path}. Overwriting.")
                all_domains[domain_def.name] = domain_def
            except (DefinitionError, KeyError) as e:
                 domain_name = domain_data.get('domain', 'unknown') if isinstance(domain_data, dict) else 'unknown'
                 logger.error(f"Failed to parse domain '{domain_name}' from {json_path}: {e}. Skipping domain.")
                 # Continue parsing other domains
            except Exception as e:
                 domain_name = domain_data.get('domain', 'unknown') if isinstance(domain_data, dict) else 'unknown'
                 logger.error(f"Unexpected error parsing domain '{domain_name}' from {json_path}: {e}. Skipping domain.", exc_info=True)


    logger.info(f"Finished processing. Found {len(all_domains)} unique domains.")
    return ProtocolDefinition(
        version_major=protocol_version_major,
        version_minor=protocol_version_minor,
        domains=all_domains
    )