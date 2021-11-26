# -*- coding: utf8 -*-
#

from unittest import TestCase

import nltk

from constituency_labeling import nltk_tree_to_label, label_tree_to_nltk


class TestConvert(TestCase):
    def test_convert_1(self):
        line = '(TOP (IP-HLN (IP (VP (VA 清新))) (IP (VP (VA 清新))) (IP (VP (VA 清新)))))'
        ptree = nltk.tree.Tree.fromstring(line)
        ptree.pretty_print()
        dt = nltk_tree_to_label(ptree)
        dt.pretty_tree(filename='11.gv')
        ptree2 = label_tree_to_nltk(dt)
        ptree2.pretty_print()

    def test_convert_2(self):
        line = '(TOP (IP-HLN (IP-TPC (NP-PN-SBJ (NR 广西)) (VP (PP-DIR (P 对) (NP (NN 外))) (VP (VV 开放)))) (NP-SBJ (NN 成绩)) (VP (VV 斐然))))'
        ptree = nltk.tree.Tree.fromstring(line)
        ptree.pretty_print()
        dt = nltk_tree_to_label(ptree)
        dt.pretty_tree(filename='22.gv')
        ptree2 = label_tree_to_nltk(dt)
        ptree2.pretty_print()

    def test_batch_convert(self):
        path = '/home/yuzhang/PycharmProjects/con-parser/src/data/train.noempty.txt'
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                ptree = nltk.tree.Tree.fromstring(line)
                dt = nltk_tree_to_label(ptree)
                ptree2 = label_tree_to_nltk(dt)
                assert ptree == ptree2
