# # DO NOT EDIT THIS FILE!
# #
# # This file is generated from the CDP specification using AST. If you need to make
# # changes, edit the generator and regenerate all of the modules.

from __future__ import annotations
"""API wrapper for the Accessibility domain."""
import typing
from ..util import CDPClient
from .. import accessibility as _accessibility_module
from .. import dom
from .. import page
from .. import runtime
None


class AccessibilityAPI:
    """Provides an API wrapper for the 'Accessibility' domain commands.

**EXPERIMENTAL**"""

    def __init__(self, client: CDPClient) ->None:
        self.client: CDPClient = client

    def disable(self, _response_timeout: typing.Optional[float]=None) ->None:
        """Disables the accessibility domain.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _accessibility_module.disable()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def enable(self, _response_timeout: typing.Optional[float]=None) ->None:
        """Enables the accessibility domain which causes ``AXNodeId``s to remain consistent between method calls.
This turns on accessibility for the page, which can impact performance until accessibility is disabled.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _accessibility_module.enable()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def get_ax_node_and_ancestors(self, node_id: typing.Optional[dom.NodeId
        ]=None, backend_node_id: typing.Optional[dom.BackendNodeId]=None,
        object_id: typing.Optional[runtime.RemoteObjectId]=None,
        _response_timeout: typing.Optional[float]=None) ->typing.List[
        _accessibility_module.AXNode]:
        """Fetches a node and all ancestors up to and including the root.
Requires ``enable()`` to have been called previously.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param node_id: *(Optional)* Identifier of the node to get.

:param backend_node_id: *(Optional)* Identifier of the backend node to get.

:param object_id: *(Optional)* JavaScript object id of the node wrapper to get.

:param _response_timeout: Optional timeout in seconds for the command.


:returns:"""
        gen = _accessibility_module.get_ax_node_and_ancestors(node_id=
            node_id, backend_node_id=backend_node_id, object_id=object_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def get_child_ax_nodes(self, id_: _accessibility_module.AXNodeId,
        frame_id: typing.Optional[page.FrameId]=None, _response_timeout:
        typing.Optional[float]=None) ->typing.List[_accessibility_module.AXNode
        ]:
        """Fetches a particular accessibility node by AXNodeId.
Requires ``enable()`` to have been called previously.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param id_:

:param frame_id: *(Optional)* The frame in whose document the node resides. If omitted, the root frame is used.

:param _response_timeout: Optional timeout in seconds for the command.


:returns:"""
        gen = _accessibility_module.get_child_ax_nodes(id_=id_, frame_id=
            frame_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def get_full_ax_tree(self, depth: typing.Optional[int]=None, frame_id:
        typing.Optional[page.FrameId]=None, _response_timeout: typing.
        Optional[float]=None) ->typing.List[_accessibility_module.AXNode]:
        """Fetches the entire accessibility tree for the root Document

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param depth: *(Optional)* The maximum depth at which descendants of the root node should be retrieved. If omitted, the full tree is returned.

:param frame_id: *(Optional)* The frame for whose document the AX tree should be retrieved. If omitted, the root frame is used.

:param _response_timeout: Optional timeout in seconds for the command.


:returns:"""
        gen = _accessibility_module.get_full_ax_tree(depth=depth, frame_id=
            frame_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def get_partial_ax_tree(self, node_id: typing.Optional[dom.NodeId]=None,
        backend_node_id: typing.Optional[dom.BackendNodeId]=None, object_id:
        typing.Optional[runtime.RemoteObjectId]=None, fetch_relatives:
        typing.Optional[bool]=None, _response_timeout: typing.Optional[
        float]=None) ->typing.List[_accessibility_module.AXNode]:
        """Fetches the accessibility node and partial accessibility tree for this DOM node, if it exists.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param node_id: *(Optional)* Identifier of the node to get the partial accessibility tree for.

:param backend_node_id: *(Optional)* Identifier of the backend node to get the partial accessibility tree for.

:param object_id: *(Optional)* JavaScript object id of the node wrapper to get the partial accessibility tree for.

:param fetch_relatives: *(Optional)* Whether to fetch this node's ancestors, siblings and children. Defaults to true.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: The ``Accessibility.AXNode`` for this DOM node, if it exists, plus its ancestors, siblings and children, if requested."""
        gen = _accessibility_module.get_partial_ax_tree(node_id=node_id,
            backend_node_id=backend_node_id, object_id=object_id,
            fetch_relatives=fetch_relatives)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def get_root_ax_node(self, frame_id: typing.Optional[page.FrameId]=None,
        _response_timeout: typing.Optional[float]=None
        ) ->_accessibility_module.AXNode:
        """Fetches the root node.
Requires ``enable()`` to have been called previously.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param frame_id: *(Optional)* The frame in whose document the node resides. If omitted, the root frame is used.

:param _response_timeout: Optional timeout in seconds for the command.


:returns:"""
        gen = _accessibility_module.get_root_ax_node(frame_id=frame_id)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def query_ax_tree(self, node_id: typing.Optional[dom.NodeId]=None,
        backend_node_id: typing.Optional[dom.BackendNodeId]=None, object_id:
        typing.Optional[runtime.RemoteObjectId]=None, accessible_name:
        typing.Optional[str]=None, role: typing.Optional[str]=None,
        _response_timeout: typing.Optional[float]=None) ->typing.List[
        _accessibility_module.AXNode]:
        """Query a DOM node's accessibility subtree for accessible name and role.
This command computes the name and role for all nodes in the subtree, including those that are
ignored for accessibility, and returns those that match the specified name and role. If no DOM
node is specified, or the DOM node does not exist, the command returns an error. If neither
``accessibleName`` or ``role`` is specified, it returns all the accessibility nodes in the subtree.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

**EXPERIMENTAL**


:param ...:

:param node_id: *(Optional)* Identifier of the node for the root to query.

:param backend_node_id: *(Optional)* Identifier of the backend node for the root to query.

:param object_id: *(Optional)* JavaScript object id of the node wrapper for the root to query.

:param accessible_name: *(Optional)* Find nodes with this computed name.

:param role: *(Optional)* Find nodes with this computed role.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A list of ``Accessibility.AXNode`` matching the specified attributes, including nodes that are ignored for accessibility."""
        gen = _accessibility_module.query_ax_tree(node_id=node_id,
            backend_node_id=backend_node_id, object_id=object_id,
            accessible_name=accessible_name, role=role)
        return self.client.send(gen, _response_timeout=_response_timeout)
