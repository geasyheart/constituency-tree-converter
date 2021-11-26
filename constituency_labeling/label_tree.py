# -*- coding: utf8 -*-
#
from typing import List, Optional, Dict, Iterable

from constituency_labeling.exception import DuplicateIdException


class Node(object):
    def __init__(self, id: str, cut_words: List, label: str, extra: Optional[Dict]):
        """

        :param id:  unique id
        :param cut_words: [(word1, pos1), (word2, pos2)]
        :param label:
        :param extra:
        """
        self.id = id
        self.cut_words = cut_words
        self.label = label
        self.extract = extra or {}

        self.parent: Optional[Node] = None
        self.children: List[Node] = []

    def __repr__(self):
        return f'{self.label}: {self.cut_words}'

    def set_parent(self, node: 'Node'):
        self.parent = node

    def add_child(self, node: 'Node'):
        self.children.append(node)


class LabelTree(object):
    def __init__(self):
        self.id_node_map: Dict[str, Node] = {}
        self.root: Optional[Node] = None

    def generate_tree(self, nodes: List[Dict]):
        if len(set([node_desc['id'] for node_desc in nodes])) != len(nodes):
            raise DuplicateIdException
        # 1. generate node
        for node_desc in nodes:
            id = node_desc['id']
            self.id_node_map.setdefault(
                id,
                Node(
                    id=id, cut_words=node_desc['cut_words'], label=node_desc['label'],
                    extra=node_desc
                )
            )
        # 2. relation
        for node_desc in nodes:
            id = node_desc['id']
            parent = node_desc['parent']
            node = self.id_node_map[id]
            if parent is None: continue
            parent = self.id_node_map[parent]
            node.set_parent(parent)
            parent.add_child(node)

        # 3. get root
        root = [_ for _ in self.id_node_map.values() if not _.parent][0]
        self.root = root
        # TODO: 4. digraph. but now pass.
        return root

    def bfs(self, nodes: List[Node]):
        if nodes:
            yield nodes

        level_nodes = []
        for node in nodes:
            if node.children:
                level_nodes.extend(node.children)
        if level_nodes:
            yield from self.bfs(nodes=level_nodes)

    def dfs(self, node: Optional[Node] = None) -> Iterable[Node]:
        if node:
            yield node
        for child in node.children:
            yield from self.dfs(node=child)

    def pretty_tree(self, use_algo='dfs', filename="", format="svg"):
        from graphviz import Digraph
        filename = filename or "tmp.gv"
        if use_algo == 'dfs':
            g = Digraph(format=format)
            for node in self.dfs(node=self.root):
                g.node(name=str(node.id), label=str(node))
            for node in self.dfs(node=self.root):
                if node.parent:
                    g.edge(str(node.parent.id), str(node.id))

        else:
            g = Digraph()
            for nodes in self.bfs(nodes=[self.root]):
                for node in nodes:
                    g.node(name=str(node.id), label=str(node))
                    if node.parent:
                        g.edge(str(node.parent.id), str(node.id))
        g.view(filename=filename, directory='./examples')

    @property
    def leaves(self):
        for node in self.dfs(node=self.root):
            if not node.children:
                yield node
