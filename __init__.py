#!/usr/bin/env pypy3

import node
import xpath


class HTML(object):
    """docstring for NodeTree"""
    def __init__(self, html_string):
        super(HTML, self).__init__()
        self.html_string = html_string
        self.node_tree = node.node_tree(html_string)

    def node(self, cmd_string):
        """docstring for node"""
        return xpath.pickup(self.node_tree, cmd_string)

    def text(self, node):
        """docstring for text"""
        return node.text(self.html_string, node)

    def attr(self, node, key):
        """docstring for attr"""
        return node.get_attr(node, key)

