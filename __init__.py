#!/usr/bin/env pypy3

from . import nodes
from . import xpath


class Node(object):
    """docstring for Node"""
    def __init__(self, node, html_string, node_tree_whole):
        super(Node, self).__init__()
        self.node = node
        self.html_string = html_string
        self.node_tree_whole = node_tree_whole


    @classmethod
    def new(cls, html_string):
        """docstring for new"""
        node_list = nodes.node_tree(html_string)
        if len(node_list) == 1:
            return cls(node_list[0], html_string, node_list)
        else:
            l = []
            for i in node_list:
                l.append(cls(i, html_string, node_list))
            return l

    def pick(self, cmd_string, node_tree=None):
        """docstring for node"""
        if node_tree is None:
            node_tree = self.node
        if not isinstance(node_tree, list):
            node_tree = [node_tree]
        _node_tree = []
        for n in node_tree:
            if isinstance(n, Node):
                n = n.node
            _node_tree.append(n)
        _node_list = xpath.pickup(_node_tree, cmd_string)
        node_list = []
        for n in _node_list:
            node_list.append(Node(n, self.html_string, self.node_tree_whole))
        return node_list

    def text(self):
        """docstring for text"""
        if isinstance(self.node, list):
            raise
        return nodes.text(self.html_string, self.node)

    def attr(self, key):
        """docstring for attr"""
        if isinstance(self.node, list):
            raise
        return nodes.get_attr(self.node, key)



