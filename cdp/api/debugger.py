# # DO NOT EDIT THIS FILE!
# #
# # This file is generated from the CDP specification using AST. If you need to make
# # changes, edit the generator and regenerate all of the modules.

from __future__ import annotations
"""API wrapper for the Debugger domain."""
import typing
from ..util import CDPClient
from .. import debugger as _debugger_module
from .. import runtime
from deprecated.sphinx import deprecated
None


class DebuggerAPI:
    """Provides an API wrapper for the 'Debugger' domain commands.

Domain Description:
Debugger domain exposes JavaScript debugging capabilities. It allows setting and removing
breakpoints, stepping through execution, exploring stack traces, etc."""

    def __init__(self, client: CDPClient) ->None:
        self.client: CDPClient = client

    def continue_to_location(self, location: _debugger_module.Location,
        target_call_frames: typing.Optional[str]=None, _response_timeout:
        typing.Optional[float]=None) ->None:
        """Continues execution until specific location is reached.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param location: Location to continue to.

:param target_call_frames: *(Optional)*

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.continue_to_location(location=location,
            target_call_frames=target_call_frames)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def disable(self, _response_timeout: typing.Optional[float]=None) ->None:
        """Disables debugger for given page.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.disable()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def disassemble_wasm_module(self, script_id: runtime.ScriptId,
        _response_timeout: typing.Optional[float]=None) ->typing.Tuple[
        typing.Optional[str], int, typing.List[int], _debugger_module.
        WasmDisassemblyChunk]:
        """NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param script_id: Id of the script to disassemble

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **streamId** - *(Optional)* For large modules, return a stream from which additional chunks of disassembly can be read successively.
    2. **totalNumberOfLines** - The total number of lines in the disassembly text.
    3. **functionBodyOffsets** - The offsets of all function bodies, in the format [start1, end1, start2, end2, ...] where all ends are exclusive.
    4. **chunk** - The first chunk of disassembly."""
        gen = _debugger_module.disassemble_wasm_module(script_id=script_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def enable(self, max_scripts_cache_size: typing.Optional[float]=None,
        _response_timeout: typing.Optional[float]=None
        ) ->runtime.UniqueDebuggerId:
        """Enables debugger for the given page. Clients should not assume that the debugging has been
enabled until the result for this command is received.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param max_scripts_cache_size: **(EXPERIMENTAL)** *(Optional)* The maximum size in bytes of collected scripts (not referenced by other heap objects) the debugger can hold. Puts no limit if parameter is omitted.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: Unique identifier of the debugger."""
        gen = _debugger_module.enable(max_scripts_cache_size=
            max_scripts_cache_size)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def evaluate_on_call_frame(self, call_frame_id: _debugger_module.
        CallFrameId, expression: str, object_group: typing.Optional[str]=
        None, include_command_line_api: typing.Optional[bool]=None, silent:
        typing.Optional[bool]=None, return_by_value: typing.Optional[bool]=
        None, generate_preview: typing.Optional[bool]=None,
        throw_on_side_effect: typing.Optional[bool]=None, timeout: typing.
        Optional[runtime.TimeDelta]=None, _response_timeout: typing.
        Optional[float]=None) ->typing.Tuple[runtime.RemoteObject, typing.
        Optional[runtime.ExceptionDetails]]:
        """Evaluates expression on a given call frame.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param call_frame_id: Call frame identifier to evaluate on.

:param expression: Expression to evaluate.

:param object_group: *(Optional)* String object group name to put result into (allows rapid releasing resulting object handles using ``releaseObjectGroup``).

:param include_command_line_api: *(Optional)* Specifies whether command line API should be available to the evaluated expression, defaults to false.

:param silent: *(Optional)* In silent mode exceptions thrown during evaluation are not reported and do not pause execution. Overrides ``setPauseOnException`` state.

:param return_by_value: *(Optional)* Whether the result is expected to be a JSON object that should be sent by value.

:param generate_preview: **(EXPERIMENTAL)** *(Optional)* Whether preview should be generated for the result.

:param throw_on_side_effect: *(Optional)* Whether to throw an exception if side effect cannot be ruled out during evaluation.

:param timeout: **(EXPERIMENTAL)** *(Optional)* Terminate execution after timing out (number of milliseconds).

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **result** - Object wrapper for the evaluation result.
    2. **exceptionDetails** - *(Optional)* Exception details."""
        gen = _debugger_module.evaluate_on_call_frame(call_frame_id=
            call_frame_id, expression=expression, object_group=object_group,
            include_command_line_api=include_command_line_api, silent=
            silent, return_by_value=return_by_value, generate_preview=
            generate_preview, throw_on_side_effect=throw_on_side_effect,
            timeout=timeout)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def get_possible_breakpoints(self, start: _debugger_module.Location,
        end: typing.Optional[_debugger_module.Location]=None,
        restrict_to_function: typing.Optional[bool]=None, _response_timeout:
        typing.Optional[float]=None) ->typing.List[_debugger_module.
        BreakLocation]:
        """Returns possible locations for breakpoint. scriptId in start and end range locations should be
the same.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param start: Start of range to search possible breakpoint locations in.

:param end: *(Optional)* End of range to search possible breakpoint locations in (excluding). When not specified, end of scripts is used as end of range.

:param restrict_to_function: *(Optional)* Only consider locations which are in the same (non-nested) function as start.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: List of the possible breakpoint locations."""
        gen = _debugger_module.get_possible_breakpoints(start=start, end=
            end, restrict_to_function=restrict_to_function)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def get_script_source(self, script_id: runtime.ScriptId,
        _response_timeout: typing.Optional[float]=None) ->typing.Tuple[str,
        typing.Optional[str]]:
        """Returns source for the script with given id.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param script_id: Id of the script to get source for.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **scriptSource** - Script source (empty in case of Wasm bytecode).
    2. **bytecode** - *(Optional)* Wasm bytecode. (Encoded as a base64 string when passed over JSON)"""
        gen = _debugger_module.get_script_source(script_id=script_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def get_stack_trace(self, stack_trace_id: runtime.StackTraceId,
        _response_timeout: typing.Optional[float]=None) ->runtime.StackTrace:
        """Returns stack trace with given ``stackTraceId``.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param stack_trace_id:

:param _response_timeout: Optional timeout in seconds for the command.


:returns:"""
        gen = _debugger_module.get_stack_trace(stack_trace_id=stack_trace_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    @deprecated(version='1.3')
    def get_wasm_bytecode(self, script_id: runtime.ScriptId,
        _response_timeout: typing.Optional[float]=None) ->str:
        """This command is deprecated. Use getScriptSource instead.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

.. deprecated:: 1.3


:param ...:

:param script_id: Id of the Wasm script to get source for.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: Script source. (Encoded as a base64 string when passed over JSON)"""
        gen = _debugger_module.get_wasm_bytecode(script_id=script_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def next_wasm_disassembly_chunk(self, stream_id: str, _response_timeout:
        typing.Optional[float]=None) ->_debugger_module.WasmDisassemblyChunk:
        """Disassemble the next chunk of lines for the module corresponding to the
stream. If disassembly is complete, this API will invalidate the streamId
and return an empty chunk. Any subsequent calls for the now invalid stream
will return errors.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param stream_id:

:param _response_timeout: Optional timeout in seconds for the command.


:returns: The next chunk of disassembly."""
        gen = _debugger_module.next_wasm_disassembly_chunk(stream_id=stream_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def pause(self, _response_timeout: typing.Optional[float]=None) ->None:
        """Stops on the next JavaScript statement.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.pause()
        return self.client.send(gen, _response_timeout=_response_timeout)

    @deprecated(version='1.3')
    def pause_on_async_call(self, parent_stack_trace_id: runtime.
        StackTraceId, _response_timeout: typing.Optional[float]=None) ->None:
        """NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

.. deprecated:: 1.3

**EXPERIMENTAL**


:param ...:

:param parent_stack_trace_id: Debugger will pause when async call with given stack trace is started.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.pause_on_async_call(parent_stack_trace_id=
            parent_stack_trace_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def remove_breakpoint(self, breakpoint_id: _debugger_module.
        BreakpointId, _response_timeout: typing.Optional[float]=None) ->None:
        """Removes JavaScript breakpoint.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param breakpoint_id:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.remove_breakpoint(breakpoint_id=breakpoint_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def restart_frame(self, call_frame_id: _debugger_module.CallFrameId,
        mode: typing.Optional[str]=None, _response_timeout: typing.Optional
        [float]=None) ->typing.Tuple[typing.List[_debugger_module.CallFrame
        ], typing.Optional[runtime.StackTrace], typing.Optional[runtime.
        StackTraceId]]:
        """Restarts particular call frame from the beginning. The old, deprecated
behavior of ``restartFrame`` is to stay paused and allow further CDP commands
after a restart was scheduled. This can cause problems with restarting, so
we now continue execution immediatly after it has been scheduled until we
reach the beginning of the restarted frame.

To stay back-wards compatible, ``restartFrame`` now expects a ``mode``
parameter to be present. If the ``mode`` parameter is missing, ``restartFrame``
errors out.

The various return values are deprecated and ``callFrames`` is always empty.
Use the call frames from the ``Debugger#paused`` events instead, that fires
once V8 pauses at the beginning of the restarted function.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param call_frame_id: Call frame identifier to evaluate on.

:param mode: **(EXPERIMENTAL)** *(Optional)* The ``mode`` parameter must be present and set to 'StepInto', otherwise ``restartFrame`` will error out.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **callFrames** - New stack trace.
    2. **asyncStackTrace** - *(Optional)* Async stack trace, if any.
    3. **asyncStackTraceId** - *(Optional)* Async stack trace, if any."""
        gen = _debugger_module.restart_frame(call_frame_id=call_frame_id,
            mode=mode)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def resume(self, terminate_on_resume: typing.Optional[bool]=None,
        _response_timeout: typing.Optional[float]=None) ->None:
        """Resumes JavaScript execution.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param terminate_on_resume: *(Optional)* Set to true to terminate execution upon resuming execution. In contrast to Runtime.terminateExecution, this will allows to execute further JavaScript (i.e. via evaluation) until execution of the paused code is actually resumed, at which point termination is triggered. If execution is currently not paused, this parameter has no effect.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.resume(terminate_on_resume=terminate_on_resume)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def search_in_content(self, script_id: runtime.ScriptId, query: str,
        case_sensitive: typing.Optional[bool]=None, is_regex: typing.
        Optional[bool]=None, _response_timeout: typing.Optional[float]=None
        ) ->typing.List[_debugger_module.SearchMatch]:
        """Searches for given string in script content.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param script_id: Id of the script to search in.

:param query: String to search for.

:param case_sensitive: *(Optional)* If true, search is case sensitive.

:param is_regex: *(Optional)* If true, treats string parameter as regex.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: List of search matches."""
        gen = _debugger_module.search_in_content(script_id=script_id, query
            =query, case_sensitive=case_sensitive, is_regex=is_regex)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_async_call_stack_depth(self, max_depth: int, _response_timeout:
        typing.Optional[float]=None) ->None:
        """Enables or disables async call stacks tracking.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param max_depth: Maximum depth of async call stacks. Setting to ``0`` will effectively disable collecting async call stacks (default).

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.set_async_call_stack_depth(max_depth=max_depth)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_blackbox_execution_contexts(self, unique_ids: typing.List[str],
        _response_timeout: typing.Optional[float]=None) ->None:
        """Replace previous blackbox execution contexts with passed ones. Forces backend to skip
stepping/pausing in scripts in these execution contexts. VM will try to leave blackboxed script by
performing 'step in' several times, finally resorting to 'step out' if unsuccessful.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param unique_ids: Array of execution context unique ids for the debugger to ignore.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.set_blackbox_execution_contexts(unique_ids=
            unique_ids)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_blackbox_patterns(self, patterns: typing.List[str],
        skip_anonymous: typing.Optional[bool]=None, _response_timeout:
        typing.Optional[float]=None) ->None:
        """Replace previous blackbox patterns with passed ones. Forces backend to skip stepping/pausing in
scripts with url matching one of the patterns. VM will try to leave blackboxed script by
performing 'step in' several times, finally resorting to 'step out' if unsuccessful.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param patterns: Array of regexps that will be used to check script url for blackbox state.

:param skip_anonymous: *(Optional)* If true, also ignore scripts with no source url.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.set_blackbox_patterns(patterns=patterns,
            skip_anonymous=skip_anonymous)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_blackboxed_ranges(self, script_id: runtime.ScriptId, positions:
        typing.List[_debugger_module.ScriptPosition], _response_timeout:
        typing.Optional[float]=None) ->None:
        """Makes backend skip steps in the script in blackboxed ranges. VM will try leave blacklisted
scripts by performing 'step in' several times, finally resorting to 'step out' if unsuccessful.
Positions array contains positions where blackbox state is changed. First interval isn't
blackboxed. Array should be sorted.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param script_id: Id of the script.

:param positions:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.set_blackboxed_ranges(script_id=script_id,
            positions=positions)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_breakpoint(self, location: _debugger_module.Location, condition:
        typing.Optional[str]=None, _response_timeout: typing.Optional[float
        ]=None) ->typing.Tuple[_debugger_module.BreakpointId,
        _debugger_module.Location]:
        """Sets JavaScript breakpoint at a given location.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param location: Location to set breakpoint in.

:param condition: *(Optional)* Expression to use as a breakpoint condition. When specified, debugger will only stop on the breakpoint if this expression evaluates to true.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **breakpointId** - Id of the created breakpoint for further reference.
    2. **actualLocation** - Location this breakpoint resolved into."""
        gen = _debugger_module.set_breakpoint(location=location, condition=
            condition)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_breakpoint_by_url(self, line_number: int, url: typing.Optional[
        str]=None, url_regex: typing.Optional[str]=None, script_hash:
        typing.Optional[str]=None, column_number: typing.Optional[int]=None,
        condition: typing.Optional[str]=None, _response_timeout: typing.
        Optional[float]=None) ->typing.Tuple[_debugger_module.BreakpointId,
        typing.List[_debugger_module.Location]]:
        """Sets JavaScript breakpoint at given location specified either by URL or URL regex. Once this
command is issued, all existing parsed scripts will have breakpoints resolved and returned in
``locations`` property. Further matching script parsing will result in subsequent
``breakpointResolved`` events issued. This logical breakpoint will survive page reloads.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param line_number: Line number to set breakpoint at.

:param url: *(Optional)* URL of the resources to set breakpoint on.

:param url_regex: *(Optional)* Regex pattern for the URLs of the resources to set breakpoints on. Either ``url`` or ``urlRegex`` must be specified.

:param script_hash: *(Optional)* Script hash of the resources to set breakpoint on.

:param column_number: *(Optional)* Offset in the line to set breakpoint at.

:param condition: *(Optional)* Expression to use as a breakpoint condition. When specified, debugger will only stop on the breakpoint if this expression evaluates to true.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **breakpointId** - Id of the created breakpoint for further reference.
    2. **locations** - List of the locations this breakpoint resolved into upon addition."""
        gen = _debugger_module.set_breakpoint_by_url(line_number=
            line_number, url=url, url_regex=url_regex, script_hash=
            script_hash, column_number=column_number, condition=condition)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_breakpoint_on_function_call(self, object_id: runtime.
        RemoteObjectId, condition: typing.Optional[str]=None,
        _response_timeout: typing.Optional[float]=None
        ) ->_debugger_module.BreakpointId:
        """Sets JavaScript breakpoint before each call to the given function.
If another function was created from the same source as a given one,
calling it will also trigger the breakpoint.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param object_id: Function object id.

:param condition: *(Optional)* Expression to use as a breakpoint condition. When specified, debugger will stop on the breakpoint if this expression evaluates to true.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: Id of the created breakpoint for further reference."""
        gen = _debugger_module.set_breakpoint_on_function_call(object_id=
            object_id, condition=condition)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_breakpoints_active(self, active: bool, _response_timeout:
        typing.Optional[float]=None) ->None:
        """Activates / deactivates all breakpoints on the page.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param active: New value for breakpoints active state.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.set_breakpoints_active(active=active)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_instrumentation_breakpoint(self, instrumentation: str,
        _response_timeout: typing.Optional[float]=None
        ) ->_debugger_module.BreakpointId:
        """Sets instrumentation breakpoint.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param instrumentation: Instrumentation name.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: Id of the created breakpoint for further reference."""
        gen = _debugger_module.set_instrumentation_breakpoint(instrumentation
            =instrumentation)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_pause_on_exceptions(self, state: str, _response_timeout: typing
        .Optional[float]=None) ->None:
        """Defines pause on exceptions state. Can be set to stop on all exceptions, uncaught exceptions,
or caught exceptions, no exceptions. Initial pause on exceptions state is ``none``.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param state: Pause on exceptions mode.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.set_pause_on_exceptions(state=state)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_return_value(self, new_value: runtime.CallArgument,
        _response_timeout: typing.Optional[float]=None) ->None:
        """Changes return value in top frame. Available only at return break position.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param new_value: New return value.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.set_return_value(new_value=new_value)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_script_source(self, script_id: runtime.ScriptId, script_source:
        str, dry_run: typing.Optional[bool]=None, allow_top_frame_editing:
        typing.Optional[bool]=None, _response_timeout: typing.Optional[
        float]=None) ->typing.Tuple[typing.Optional[typing.List[
        _debugger_module.CallFrame]], typing.Optional[bool], typing.
        Optional[runtime.StackTrace], typing.Optional[runtime.StackTraceId],
        str, typing.Optional[runtime.ExceptionDetails]]:
        """Edits JavaScript source live.

In general, functions that are currently on the stack can not be edited with
a single exception: If the edited function is the top-most stack frame and
that is the only activation of that function on the stack. In this case
the live edit will be successful and a ``Debugger.restartFrame`` for the
top-most function is automatically triggered.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param script_id: Id of the script to edit.

:param script_source: New content of the script.

:param dry_run: *(Optional)* If true the change will not actually be applied. Dry run may be used to get result description without actually modifying the code.

:param allow_top_frame_editing: **(EXPERIMENTAL)** *(Optional)* If true, then ``scriptSource`` is allowed to change the function on top of the stack as long as the top-most stack frame is the only activation of that function.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **callFrames** - *(Optional)* New stack trace in case editing has happened while VM was stopped.
    2. **stackChanged** - *(Optional)* Whether current call stack  was modified after applying the changes.
    3. **asyncStackTrace** - *(Optional)* Async stack trace, if any.
    4. **asyncStackTraceId** - *(Optional)* Async stack trace, if any.
    5. **status** - Whether the operation was successful or not. Only ``Ok`` denotes a successful live edit while the other enum variants denote why the live edit failed.
    6. **exceptionDetails** - *(Optional)* Exception details if any. Only present when ``status`` is ``CompileError``."""
        gen = _debugger_module.set_script_source(script_id=script_id,
            script_source=script_source, dry_run=dry_run,
            allow_top_frame_editing=allow_top_frame_editing)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_skip_all_pauses(self, skip: bool, _response_timeout: typing.
        Optional[float]=None) ->None:
        """Makes page not interrupt on any pauses (breakpoint, exception, dom exception etc).

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param skip: New value for skip pauses state.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.set_skip_all_pauses(skip=skip)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def set_variable_value(self, scope_number: int, variable_name: str,
        new_value: runtime.CallArgument, call_frame_id: _debugger_module.
        CallFrameId, _response_timeout: typing.Optional[float]=None) ->None:
        """Changes value of variable in a callframe. Object-based scopes are not supported and must be
mutated manually.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param scope_number: 0-based number of scope as was listed in scope chain. Only 'local', 'closure' and 'catch' scope types are allowed. Other scopes could be manipulated manually.

:param variable_name: Variable name.

:param new_value: New variable value.

:param call_frame_id: Id of callframe that holds variable.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.set_variable_value(scope_number=scope_number,
            variable_name=variable_name, new_value=new_value, call_frame_id
            =call_frame_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def step_into(self, break_on_async_call: typing.Optional[bool]=None,
        skip_list: typing.Optional[typing.List[_debugger_module.
        LocationRange]]=None, _response_timeout: typing.Optional[float]=None
        ) ->None:
        """Steps into the function call.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param break_on_async_call: **(EXPERIMENTAL)** *(Optional)* Debugger will pause on the execution of the first async task which was scheduled before next pause.

:param skip_list: **(EXPERIMENTAL)** *(Optional)* The skipList specifies location ranges that should be skipped on step into.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.step_into(break_on_async_call=
            break_on_async_call, skip_list=skip_list)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def step_out(self, _response_timeout: typing.Optional[float]=None) ->None:
        """Steps out of the function call.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.step_out()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def step_over(self, skip_list: typing.Optional[typing.List[
        _debugger_module.LocationRange]]=None, _response_timeout: typing.
        Optional[float]=None) ->None:
        """Steps over the statement.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param skip_list: **(EXPERIMENTAL)** *(Optional)* The skipList specifies location ranges that should be skipped on step over.

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _debugger_module.step_over(skip_list=skip_list)
        return self.client.send(gen, _response_timeout=_response_timeout)
