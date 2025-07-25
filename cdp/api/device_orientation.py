# # DO NOT EDIT THIS FILE!
# #
# # This file is generated from the CDP specification using AST. If you need to make
# # changes, edit the generator and regenerate all of the modules.

from __future__ import annotations
"""API wrapper for the DeviceOrientation domain."""
import typing
from ..util import CDPClient
from .. import device_orientation as _device_orientation_module
None


class DeviceOrientationAPI:
    """Provides an API wrapper for the 'DeviceOrientation' domain commands.

**EXPERIMENTAL**"""

    def __init__(self, client: CDPClient) ->None:
        self.client: CDPClient = client

    def clear_device_orientation_override(self, _response_timeout: typing.
        Optional[float]=None) ->None:
        """Clears the overridden Device Orientation.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _device_orientation_module.clear_device_orientation_override()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_device_orientation_override(self, alpha: float, beta: float,
        gamma: float, _response_timeout: typing.Optional[float]=None) ->None:
        """Overrides the Device Orientation.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param alpha: Mock alpha

:param beta: Mock beta

:param gamma: Mock gamma

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _device_orientation_module.set_device_orientation_override(alpha
            =alpha, beta=beta, gamma=gamma)
        return self.client.send(gen, _response_timeout=_response_timeout)
