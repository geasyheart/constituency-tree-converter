# -*- coding: utf8 -*-
#
# copied from test_label_tree.py
import uuid
from typing import List, Dict

from constituency_labeling import label_tree_to_nltk
from constituency_labeling.label_tree import LabelTree
from nltk import tree
from constituency_labeling import transform

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


def extend_to_nltk(s: List[Dict]):
    extend_nodes = []
    for index, desc in enumerate(s):
        if len(desc['cut_words']) == 1 and desc['label']:
            # 进行扩充
            new_parent = str(uuid.uuid4())
            desc_rel = {
                'label': desc['label'],
                'cut_words': [],
                'id': new_parent,
                'parent': desc['parent']
            }
            desc['parent'] = new_parent
            extend_nodes.append((index, desc_rel))
    for i, d in extend_nodes:
        s.insert(i, d)
    return s


if __name__ == '__main__':
    ltree = LabelTree()
    new_sample = extend_to_nltk(sample)
    ltree.generate_tree(new_sample)
    ltree.pretty_tree(filename='t1.gv')
    nltk_tree = label_tree_to_nltk(ltree)

    nltk_tree_top = tree.Tree('TOP', [nltk_tree])
    nltk_tree_top.pretty_print()

    # 1. 转成序列结构
    to_sequence = transform.Tree.factorize(transform.Tree.binarize(nltk_tree_top)[0])
    print(to_sequence)
    # 2. 转回来
    t2 = transform.Tree.totree([('据中央时报报道', 'rph'),
                                ('华为', 'org'), ('说', 'v'),
                                ('虽然', 't'), ('今年', 'n'), ('举步维艰', 'c'),
                                ('但是', 't'), ('未来', 't'), ('一片光明', 'n')], 'TOP')
    nltk_tree_top2 = transform.Tree.build(
        t2,
        to_sequence
    )
    nltk_tree_top2.pretty_print()

    assert nltk_tree_top2 == nltk_tree_top
