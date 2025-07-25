"""Custom exceptions for the CDP parsing process."""

class CdpParsingError(Exception):
    """Base exception for errors during CDP JSON parsing."""
    pass

class FileFormatError(CdpParsingError):
    """Error related to the JSON file format or structure."""
    pass

class DefinitionError(CdpParsingError):
    """Error related to a specific definition within the protocol (type, command, etc.)."""
    pass