# -*- coding: utf8 -*-
#
from typing import List, Tuple, Dict

import nltk.tree

from constituency_labeling.exception import LeaveNodeLengthError
from constituency_labeling.label_tree import LabelTree, Node


def label_tree_to_nltk(label_tree: LabelTree) -> nltk.tree.Tree:
    n1_n2_map: Dict[int, nltk.Tree] = {}
    # 1. 叶子节点
    for node in label_tree.dfs(node=label_tree.root):
        if not node.children:
            lens = len(node.cut_words)
            # 这里为叶子节点
            if lens == 1:
                word, pos = node.cut_words[0]
            # 这里为叶子节点的label
            # 对于单个词进行标注label，需要额外增加一个Node
            elif lens == 0:
                word, pos = '', node.label
            else:
                raise LeaveNodeLengthError
            n1_n2_map[id(node)] = nltk.Tree(pos, [word])

    # 2. 非叶子节点
    reverse_nodes = [nodes for nodes in label_tree.bfs(nodes=[label_tree.root])][::-1]
    for nodes in reverse_nodes:
        for node in nodes:
            if node.children:
                t = nltk.Tree(node.label, [n1_n2_map[id(_)] for _ in node.children])
                n1_n2_map[id(node)] = t
    return n1_n2_map[id(label_tree.root)]


def nltk_tree_to_label(tree: nltk.tree.Tree) -> LabelTree:
    tree = nltk.tree.ParentedTree.convert(tree)

    # 因为t1是unhashable
    t1_t2_map: List[Tuple[nltk.tree.Tree, Node]] = []
    # 先创建叶子节点
    for _id, t in enumerate(tree.subtrees()):
        if t.height() == 2:
            node = Node(
                id=f'node-{_id}',
                cut_words=t.pos(),
                label=t.label(),
                extra={}
            )
            t1_t2_map.append((t, node))

    dt = LabelTree()

    is_leave_node = lambda x: any([id(x) == id(t1) for t1, t2 in t1_t2_map])
    for _id, t in enumerate(tree.subtrees()):
        # t.pretty_print()
        if len(t.pos()) == 1:
            # 那么就表示要么是叶子节点要么是只有一个的了
            if not is_leave_node(t):
                node = Node(
                    id=f'node-{_id}',
                    cut_words=t.pos(),
                    label=t.label(),
                    extra={}
                )

                t1_t2_map.append((t, node))
            else:
                node = [t2 for t1, t2 in t1_t2_map if id(t1) == id(t)][0]
        else:
            node = Node(
                id=f'node-{_id}',
                cut_words=t.pos(),
                label=t.label(),
                extra={}
            )
            t1_t2_map.append((t, node))
        if t.parent() is None:
            dt.root = node
        else:
            parent_node = [t2 for t1, t2 in t1_t2_map if id(t1) == id(t.parent())][0]
            node.set_parent(parent_node)
            parent_node.add_child(node)
    return dt
