# # DO NOT EDIT THIS FILE!
# #
# # This file is generated from the CDP specification using AST. If you need to make
# # changes, edit the generator and regenerate all of the modules.

from __future__ import annotations
"""API wrapper for the DOMSnapshot domain."""
import typing
from ..util import CDPClient
from .. import dom_snapshot as _dom_snapshot_module
from deprecated.sphinx import deprecated
None


class DomSnapshotAPI:
    """Provides an API wrapper for the 'DOMSnapshot' domain commands.

**EXPERIMENTAL**

Domain Description:
This domain facilitates obtaining document snapshots with DOM, layout, and style information."""

    def __init__(self, client: CDPClient) ->None:
        self.client: CDPClient = client

    def capture_snapshot(self, computed_styles: typing.List[str],
        include_paint_order: typing.Optional[bool]=None, include_dom_rects:
        typing.Optional[bool]=None, include_blended_background_colors:
        typing.Optional[bool]=None, include_text_color_opacities: typing.
        Optional[bool]=None, _response_timeout: typing.Optional[float]=None
        ) ->typing.Tuple[typing.List[_dom_snapshot_module.DocumentSnapshot],
        typing.List[str]]:
        """Returns a document snapshot, including the full DOM tree of the root node (including iframes,
template contents, and imported documents) in a flattened array, as well as layout and
white-listed computed style information for the nodes. Shadow DOM in the returned DOM tree is
flattened.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param computed_styles: Whitelist of computed styles to return.

:param include_paint_order: *(Optional)* Whether to include layout object paint orders into the snapshot.

:param include_dom_rects: *(Optional)* Whether to include DOM rectangles (offsetRects, clientRects, scrollRects) into the snapshot

:param include_blended_background_colors: **(EXPERIMENTAL)** *(Optional)* Whether to include blended background colors in the snapshot (default: false). Blended background color is achieved by blending background colors of all elements that overlap with the current element.

:param include_text_color_opacities: **(EXPERIMENTAL)** *(Optional)* Whether to include text color opacity in the snapshot (default: false). An element might have the opacity property set that affects the text color of the element. The final text color opacity is computed based on the opacity of all overlapping elements.

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **documents** - The nodes in the DOM tree. The DOMNode at index 0 corresponds to the root document.
    2. **strings** - Shared string table that all string properties refer to with indexes."""
        gen = _dom_snapshot_module.capture_snapshot(computed_styles=
            computed_styles, include_paint_order=include_paint_order,
            include_dom_rects=include_dom_rects,
            include_blended_background_colors=
            include_blended_background_colors, include_text_color_opacities
            =include_text_color_opacities)
        return self.client.send(gen, _response_timeout=_response_timeout)

    def disable(self, _response_timeout: typing.Optional[float]=None) ->None:
        """Disables DOM snapshot agent for the given page.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_snapshot_module.disable()
        return self.client.send(gen, _response_timeout=_response_timeout)

    def enable(self, _response_timeout: typing.Optional[float]=None) ->None:
        """Enables DOM snapshot agent for the given page.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.


:param ...:

:param _response_timeout: Optional timeout in seconds for the command."""
        gen = _dom_snapshot_module.enable()
        return self.client.send(gen, _response_timeout=_response_timeout)

    @deprecated(version='1.3')
    def get_snapshot(self, computed_style_whitelist: typing.List[str],
        include_event_listeners: typing.Optional[bool]=None,
        include_paint_order: typing.Optional[bool]=None,
        include_user_agent_shadow_tree: typing.Optional[bool]=None,
        _response_timeout: typing.Optional[float]=None) ->typing.Tuple[
        typing.List[_dom_snapshot_module.DOMNode], typing.List[
        _dom_snapshot_module.LayoutTreeNode], typing.List[
        _dom_snapshot_module.ComputedStyle]]:
        """Returns a document snapshot, including the full DOM tree of the root node (including iframes,
template contents, and imported documents) in a flattened array, as well as layout and
white-listed computed style information for the nodes. Shadow DOM in the returned DOM tree is
flattened.

NOTE: This is a blocking wrapper method that executes the underlying generator command using the client.

.. deprecated:: 1.3


:param ...:

:param computed_style_whitelist: Whitelist of computed styles to return.

:param include_event_listeners: *(Optional)* Whether or not to retrieve details of DOM listeners (default false).

:param include_paint_order: *(Optional)* Whether to determine and include the paint order index of LayoutTreeNodes (default false).

:param include_user_agent_shadow_tree: *(Optional)* Whether to include UA shadow tree in the snapshot (default false).

:param _response_timeout: Optional timeout in seconds for the command.


:returns: A tuple with the following items:

    1. **domNodes** - The nodes in the DOM tree. The DOMNode at index 0 corresponds to the root document.
    2. **layoutTreeNodes** - The nodes in the layout tree.
    3. **computedStyles** - Whitelisted ComputedStyle properties for each node in the layout tree."""
        gen = _dom_snapshot_module.get_snapshot(computed_style_whitelist=
            computed_style_whitelist, include_event_listeners=
            include_event_listeners, include_paint_order=
            include_paint_order, include_user_agent_shadow_tree=
            include_user_agent_shadow_tree)
        return self.client.send(gen, _response_timeout=_response_timeout)
