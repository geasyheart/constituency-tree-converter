# -*- coding: utf8 -*-
#
from typing import List, Dict, Optional, Iterable


class FrontendNode(object):
    def __init__(self, words: str, label: str = ''):
        """

        :param words:
        :param label: 成分
        """
        self.words = words
        self.label = label

        self.children: List['FrontendNode'] = []
        self.parent: 'FrontendNode' = None

        # check
        if not self.words.strip():
            raise ValueError('words cannot be null')

    def add_child(self, node: 'FrontendNode'):
        self.children.append(node)

    def set_parent(self, node: 'FrontendNode'):
        self.parent = node

    def __repr__(self):
        s = ''
        if self.label:
            s += f'{self.label}\n'
        s += self.words
        return s


class FrontendTree(object):
    def __init__(self):
        self.root: Optional[FrontendNode] = None

    def generate_tree(self, sample: Dict):

        self._generate(node_info=sample, parent=None)

    def _generate(self, node_info: Dict, parent):
        node = FrontendNode(
            words=node_info['words'],
            label=node_info['label'],
        )
        node.set_parent(node=parent)
        if parent is not None:
            parent.add_child(node=node)
        else:
            self.root = node

        for child in node_info['child']:
            self._generate(node_info=child, parent=node)

    def bfs(self, nodes: List[FrontendNode]):
        if nodes:
            yield nodes

        level_nodes = []
        for node in nodes:
            if node.children:
                level_nodes.extend(node.children)
        if level_nodes:
            yield from self.bfs(nodes=level_nodes)

    def dfs(self, node: Optional[FrontendNode] = None) -> Iterable[FrontendNode]:
        if node:
            yield node
        for child in node.children:
            yield from self.dfs(node=child)

    def pretty_tree(self, filename="", format="svg"):
        from graphviz import Digraph
        filename = filename or "tmp.gv"

        g = Digraph(format=format)
        for node in self.dfs(node=self.root):
            g.node(name=str(id(node)), label=str(node))

        for node in self.dfs(node=self.root):
            if node.parent:
                g.edge(str(id(node.parent)), str(id(node)))

        g.view(filename=filename, directory='./examples')
