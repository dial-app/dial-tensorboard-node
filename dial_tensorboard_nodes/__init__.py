# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""This package adds some nodes for using Tensorboard along the training nodes."""

from dial_core.node_editor import NodeRegistrySingleton
from dial_core.notebook import NodeCellsRegistrySingleton

from .tensorboard_node import TensorboardInstanceNode, TensorboardInstanceNodeFactory

def load_plugin():
    node_registry = NodeRegistrySingleton()

    # Register Node
    node_registry.register_node("Tensorboard Node", TensorboardInstanceNodeFactory)

def unload_plugin():
    node_registry = NodeRegistrySingleton()

    # Unregister Nodes
    node_registry.unregister_node("Tensorboard Node")

__all__ = [
    "load_plugin",
    "unload_plugin",
    "TensorboardInstanceNode",
    "TensorboardInstanceNodeFactory"
]
