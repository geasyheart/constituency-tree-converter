# 成分分析树转换工具

## 介绍
这个包的目的在于将数据转换成符合constituency tree输入的格式，解决业界没有此类工具的问题（没发现～）。

从NLTK标注出来的数据集来看，有点反直觉，标注起来很麻烦。

故提供一个`LabelTree`类，您可以通过这个类转换成符合nltk标注格式的数据出来。

## install

```bash
pip install constituency-tree-converter
```

## 工作原理图

![converter functions](https://raw.githubusercontent.com/geasyheart/constituency-tree-converter/main/con_tree_converter/tests/examples/converter.png)

##  More Usage: 
更多请参考tests/。
1. [convert NLTK tree to LabelTree](./con_tree_converter/tests/test_convert.py)
2. [convert NLTK tree to sequence](./con_tree_converter/tests/test_transform.py)

## 历史
1. 项目更名啦，从`constituency-tree-labeling-tool`改成`constituency-tree-converter`，方便通过名字直观理解以及通过`工作原理图`快速理解。