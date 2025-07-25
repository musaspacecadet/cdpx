# # DO NOT EDIT THIS FILE!
# #
# # This file is generated from the CDP specification using AST. If you need to make
# # changes, edit the generator and regenerate all of the modules.

from __future__ import annotations
"""API wrapper for the Profiler domain."""
import typing
from ..util import CDPClient
from .. import profiler as _profiler_module
None


class ProfilerAPI:
    """Provides an API wrapper for the 'Profiler' domain commands."""

    def __init__(self, client: CDPClient) ->None:
        self.client: CDPClient = client

    def disable(self, _response_timeout: typing.Optional[float]=None) ->None:
        """NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _profiler_module.disable()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def enable(self, _response_timeout: typing.Optional[float]=None) ->None:
        """NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _profiler_module.enable()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def get_best_effort_coverage(self, _response_timeout: typing.Optional[
        float]=None) ->typing.List[_profiler_module.ScriptCoverage]:
        """Collect coverage data for the current isolate. The coverage data may be incomplete due to
garbage collection.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command.


:returns: Coverage data for the current isolate."""
        gen = _profiler_module.get_best_effort_coverage()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_sampling_interval(self, interval: int, _response_timeout:
        typing.Optional[float]=None) ->None:
        """Changes CPU profiler sampling interval. Must be called before CPU profiles recording started.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param interval: New sampling interval in microseconds.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _profiler_module.set_sampling_interval(interval=interval)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def start(self, _response_timeout: typing.Optional[float]=None) ->None:
        """NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _profiler_module.start()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def start_precise_coverage(self, call_count: typing.Optional[bool]=None,
        detailed: typing.Optional[bool]=None, allow_triggered_updates:
        typing.Optional[bool]=None, _response_timeout: typing.Optional[
        float]=None) ->float:
        """Enable precise code coverage. Coverage data for JavaScript executed before enabling precise code
coverage may be incomplete. Enabling prevents running optimized code and resets execution
counters.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param call_count: *(Optional)* Collect accurate call counts beyond simple 'covered' or 'not covered'.

:param detailed: *(Optional)* Collect block-based coverage.

:param allow_triggered_updates: *(Optional)* Allow the backend to send updates on its own initiative

:param _response_timeout: Optional timeout in seconds for the command.


:returns: Monotonically increasing time (in seconds) when the coverage update was taken in the backend."""
        gen = _profiler_module.start_precise_coverage(call_count=call_count,
            detailed=detailed, allow_triggered_updates=allow_triggered_updates)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def stop(self, _response_timeout: typing.Optional[float]=None
        ) ->_profiler_module.Profile:
        """NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command.


:returns: Recorded profile."""
        gen = _profiler_module.stop()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def stop_precise_coverage(self, _response_timeout: typing.Optional[
        float]=None) ->None:
        """Disable precise code coverage. Disabling releases unnecessary execution count records and allows
executing optimized code.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _profiler_module.stop_precise_coverage()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def take_precise_coverage(self, _response_timeout: typing.Optional[
        float]=None) ->typing.Tuple[typing.List[_profiler_module.
        ScriptCoverage], float]:
        """Collect coverage data for the current isolate, and resets execution counters. Precise code
coverage needs to have started.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **result** - Coverage data for the current isolate.
    2. **timestamp** - Monotonically increasing time (in seconds) when the coverage update was taken in the backend."""
        gen = _profiler_module.take_precise_coverage()
        return self.client.send(gen, _response_timeout=_response_timeout)
