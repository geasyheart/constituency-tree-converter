# -*- coding: utf8 -*-
#
from unittest import TestCase

from constituency_labeling.label_tree import LabelTree

# 1. 举个例子，另外其中标注标准、分词、词性等信息都是随意指定的。

# 2. 你可以自己增加TOP节点。
sample = [
    {
        'label': '陈述句',
        'cut_words': [('据中央时报报道', 'rph'),
                      ('华为', 'org'), ('说', 'v'),
                      ('虽然', 't'), ('今年', 'n'), ('举步维艰', 'c'),
                      ('但是', 't'), ('未来', 't'), ('一片光明', 'n')],
        'id': 'node-11',  # just unique
        'parent': None
    },
    {
        'label': '引导句',
        'cut_words': [('据中央时报报道', 'rph')],
        'id': 'node-123',
        'parent': 'node-11'

    },
    {
        "label": '主体',
        "cut_words": [('华为', 'org'), ('说', 'v')],
        "id": 'node-1',
        "parent": 'node-11'
    },
    {
        "label": '客体',
        "cut_words": [('虽然', 't'), ('今年', 'n'), ('举步维艰', 'c'), ('但是', 't'), ('未来', 't'), ('一片光明', 'n')],
        "id": 'node-2',
        "parent": 'node-11'
    },

    {
        'label': '转折句1',
        'cut_words': [('虽然', 't'), ('今年', 'n'), ('举步维艰', 'c')],
        'id': 'node-3',
        'parent': 'node-2',
    },
    {
        'label': '转折句2',
        'cut_words': [('但是', 't'), ('未来', 't'), ('一片光明', 'n')],
        'id': 'node-4',
        'parent': 'node-2',
    },
    {
        'label': '主语',
        'cut_words': [('华为', 'org')],
        'id': 'node-5',
        'parent': 'node-1'
    },
    {
        'label': '主动词',
        'cut_words': [('说', 'v')],
        'id': 'node-6',
        'parent': 'node-1'
    },
    {
        'label': '',
        'cut_words': [('虽然', 't')],
        'id': 'node-7',
        'parent': 'node-3'
    },
    {
        'label': '',
        'cut_words': [('今年', 'n')],
        'id': 'node-8',
        'parent': 'node-3'
    },
    {
        'label': '',
        'cut_words': [('举步维艰', 'c')],
        'id': 'node-9',
        'parent': 'node-3'
    },
    {
        'label': '',
        'cut_words': [('但是', 't')],
        'id': 'node-10',
        'parent': 'node-4'
    },
    {
        'label': '',
        'cut_words': [('未来', 't')],
        'id': 'node-111',
        'parent': 'node-4'
    },
    {
        'label': '',
        'cut_words': [('一片光明', 'n')],
        'id': 'node-122',
        'parent': 'node-4'
    },
]


class TestLabelTree(TestCase):
    def test_eq1(self):
        tree = LabelTree()
        tree.generate_tree(nodes=sample)

        tree2 = LabelTree()
        tree2.generate_tree(sample)

        self.assertEqual(tree, tree2)

    def test_eq2(self):
        tree = LabelTree()
        tree.generate_tree(nodes=sample)

        tree2 = LabelTree()
        tree2.generate_tree(sample)

        tree2.root.children = []
        # tree2.root.cut_words = []

        self.assertNotEqual(tree, tree2)

    def test_eq3(self):
        tree = LabelTree()
        tree.generate_tree(nodes=sample)

        tree2 = LabelTree()
        tree2.generate_tree(sample)

        tree2.root.cut_words = []

        self.assertNotEqual(tree, tree2)
