# -*- coding: utf8 -*-
# 此文件来自yzhangcs/parser，在原代码基础上进行改动，目的在于提供NLTK Tree和序列结构转换，方便数据处理与模型输入等功能。
# https://github.com/yzhangcs/parser/blob/4f34852d6aeac53d819b3ece11b2a3aee4822d74/supar/utils/transform.py#L353
import nltk


class Tree(object):
    r"""
    The Tree object factorize a constituency tree into four fields,
    each associated with one or more :class:`~supar.utils.field.Field` objects.

    Attributes:
        WORD:
            Words in the sentence.
        POS:
            Part-of-speech tags, or underscores if not available.
        TREE:
            The raw constituency tree in :class:`nltk.tree.Tree` format.
        CHART:
            The factorized sequence of binarized tree traversed in pre-order.
    """

    root = ''
    fields = ['WORD', 'POS', 'TREE', 'CHART']

    def __init__(self, WORD=None, POS=None, TREE=None, CHART=None):
        super().__init__()

        self.WORD = WORD
        self.POS = POS
        self.TREE = TREE
        self.CHART = CHART

    @property
    def src(self):
        return self.WORD, self.POS, self.TREE

    @property
    def tgt(self):
        return self.CHART,

    @classmethod
    def totree(cls, tokens, root='', special_tokens={'(': '-LRB-', ')': '-RRB-'}):
        r"""
        Converts a list of tokens to a :class:`nltk.tree.Tree`.
        Missing fields are filled with underscores.

        Args:
            tokens (list[str] or list[tuple]):
                This can be either a list of words or word/pos pairs.
            root (str):
                The root label of the tree. Default: ''.
            special_tokens (dict):
                A dict for normalizing some special tokens to avoid tree construction crash.
                Default: {'(': '-LRB-', ')': '-RRB-'}.

        Returns:
            A :class:`nltk.tree.Tree` object.

        Examples:
            >>> print(Tree.totree(['She', 'enjoys', 'playing', 'tennis', '.'], 'TOP'))
            (TOP ( (_ She)) ( (_ enjoys)) ( (_ playing)) ( (_ tennis)) ( (_ .)))
        """

        if isinstance(tokens[0], str):
            tokens = [(token, '_') for token in tokens]
        mapped = []
        for i, (word, pos) in enumerate(tokens):
            if word in special_tokens:
                tokens[i] = (special_tokens[word], pos)
                mapped.append((i, word))
        tree = nltk.Tree.fromstring(f"({root} {' '.join([f'( ({pos} {word}))' for word, pos in tokens])})")
        for i, word in mapped:
            tree[i][0][0] = word
        return tree

    @classmethod
    def binarize(cls, tree):
        r"""
        Conducts binarization over the tree.

        First, the tree is transformed to satisfy `Chomsky Normal Form (CNF)`_.
        Here we call :meth:`~nltk.tree.Tree.chomsky_normal_form` to conduct left-binarization.
        Second, all unary productions in the tree are collapsed.

        Args:
            tree (nltk.tree.Tree):
                The tree to be binarized.

        Returns:
            The binarized tree.

        Examples:
            >>> tree = nltk.Tree.fromstring('''
                                            (TOP
                                              (S
                                                (NP (_ She))
                                                (VP (_ enjoys) (S (VP (_ playing) (NP (_ tennis)))))
                                                (_ .)))
                                            ''')
            >>> print(Tree.binarize(tree))
            (TOP
              (S
                (S|<>
                  (NP (_ She))
                  (VP
                    (VP|<> (_ enjoys))
                    (S::VP (VP|<> (_ playing)) (NP (_ tennis)))))
                (S|<> (_ .))))

        .. _Chomsky Normal Form (CNF):
            https://en.wikipedia.org/wiki/Chomsky_normal_form
        """

        tree = tree.copy(True)
        if len(tree) == 1 and not isinstance(tree[0][0], nltk.Tree):
            tree[0] = nltk.Tree(f"{tree.label()}|<>", [tree[0]])
        nodes = [tree]
        while nodes:
            node = nodes.pop()
            if isinstance(node, nltk.Tree):
                nodes.extend([child for child in node])
                if len(node) > 1:
                    for i, child in enumerate(node):
                        if not isinstance(child[0], nltk.Tree):
                            node[i] = nltk.Tree(f"{node.label()}|<>", [child])
        tree.chomsky_normal_form('left', 0, 0)
        tree.collapse_unary(joinChar='::')

        return tree

    @classmethod
    def factorize(cls, tree, delete_labels=None, equal_labels=None):
        r"""
        Factorizes the tree into a sequence.
        The tree is traversed in pre-order.

        Args:
            tree (nltk.tree.Tree):
                The tree to be factorized.
            delete_labels (set[str]):
                A set of labels to be ignored. This is used for evaluation.
                If it is a pre-terminal label, delete the word along with the brackets.
                If it is a non-terminal label, just delete the brackets (don't delete children).
                In `EVALB`_, the default set is:
                {'TOP', 'S1', '-NONE-', ',', ':', '``', "''", '.', '?', '!', ''}
                Default: ``None``.
            equal_labels (dict[str, str]):
                The key-val pairs in the dict are considered equivalent (non-directional). This is used for evaluation.
                The default dict defined in `EVALB`_ is: {'ADVP': 'PRT'}
                Default: ``None``.

        Returns:
            The sequence of the factorized tree.

        Examples:
            >>> tree = nltk.Tree.fromstring('''
                                            (TOP
                                              (S
                                                (NP (_ She))
                                                (VP (_ enjoys) (S (VP (_ playing) (NP (_ tennis)))))
                                                (_ .)))
                                            ''')
            >>> Tree.factorize(tree)
            [(0, 5, 'TOP'), (0, 5, 'S'), (0, 1, 'NP'), (1, 4, 'VP'), (2, 4, 'S'), (2, 4, 'VP'), (3, 4, 'NP')]
            >>> Tree.factorize(tree, delete_labels={'TOP', 'S1', '-NONE-', ',', ':', '``', "''", '.', '?', '!', ''})
            [(0, 5, 'S'), (0, 1, 'NP'), (1, 4, 'VP'), (2, 4, 'S'), (2, 4, 'VP'), (3, 4, 'NP')]

        .. _EVALB:
            https://nlp.cs.nyu.edu/evalb/
        """

        def track(tree, i):
            label = tree.label()
            if delete_labels is not None and label in delete_labels:
                label = None
            if equal_labels is not None:
                label = equal_labels.get(label, label)
            if len(tree) == 1 and not isinstance(tree[0], nltk.Tree):
                return (i+1 if label is not None else i), []
            j, spans = i, []
            for child in tree:
                j, s = track(child, j)
                spans += s
            if label is not None and j > i:
                spans = [(i, j, label)] + spans
            return j, spans
        return track(tree, 0)[1]

    @classmethod
    def build(cls, tree, sequence):
        r"""
        Builds a constituency tree from the sequence. The sequence is generated in pre-order.
        During building the tree, the sequence is de-binarized to the original format (i.e.,
        the suffixes ``|<>`` are ignored, the collapsed labels are recovered).

        Args:
            tree (nltk.tree.Tree):
                An empty tree that provides a base for building a result tree.
            sequence (list[tuple]):
                A list of tuples used for generating a tree.
                Each tuple consits of the indices of left/right boundaries and label of the constituent.

        Returns:
            A result constituency tree.

        Examples:
            >>> tree = Tree.totree(['She', 'enjoys', 'playing', 'tennis', '.'], 'TOP')
            >>> sequence = [(0, 5, 'S'), (0, 4, 'S|<>'), (0, 1, 'NP'), (1, 4, 'VP'), (1, 2, 'VP|<>'),
                            (2, 4, 'S::VP'), (2, 3, 'VP|<>'), (3, 4, 'NP'), (4, 5, 'S|<>')]
            >>> print(Tree.build(tree, sequence))
            (TOP
              (S
                (NP (_ She))
                (VP (_ enjoys) (S (VP (_ playing) (NP (_ tennis)))))
                (_ .)))
        """

        root = tree.label()
        leaves = [subtree for subtree in tree.subtrees()
                  if not isinstance(subtree[0], nltk.Tree)]

        def track(node):
            i, j, label = next(node)
            if j == i+1:
                children = [leaves[i]]
            else:
                children = track(node) + track(node)
            if label is None or label.endswith('|<>'):
                return children
            labels = label.split('::')
            tree = nltk.Tree(labels[-1], children)
            for label in reversed(labels[:-1]):
                tree = nltk.Tree(label, [tree])
            return [tree]
        return nltk.Tree(root, track(iter(sequence)))
