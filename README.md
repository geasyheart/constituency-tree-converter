# Constituency Tree Labeling Tool

> The purpose of this package is to solve the `constituency tree labeling` problem.

Look from the dataset labeled by NLTK,it is a bit counter-intuitive and it is very troublesome to label.

Then this package provides a `LabelTree`, you can use this class to generate dataset, for example, `convert example1` and `convert example2`, and then use the `label_tree_to_nltk` method to convert them into data conforming to the NLTK label format. 
Then this package provides a `LabelTree`, you can use this class to generate dataset, for example, `convert example1` and `convert example2`, and then use the `label_tree_to_nltk` method to convert them into data conforming to the NLTK label format. 

## examples

### example1

> NLTK example 1
```
     TOP      
      |        
    IP-HLN    
  ____|_____   
 IP   IP    IP
 |    |     |  
 VP   VP    VP
 |    |     |  
 VA   VA    VA
 |    |     |  
 清新   清新    清新
```

> convert example 1

![11.gv.pdf](./constituency_labeling/tests/examples/11.gv.svg)

### example2
> NLTK example 2
```
                      TOP                 
                       |                   
                     IP-HLN               
                 ______|________________   
              IP-TPC              |     | 
     ___________|______           |     |  
    |                  VP         |     | 
    |            ______|_____     |     |  
    |         PP-DIR         |    |     | 
    |       ____|______      |    |     |  
NP-PN-SBJ  |           NP    VP NP-SBJ  VP
    |      |           |     |    |     |  
    NR     P           NN    VV   NN    VV
    |      |           |     |    |     |  
    广西     对           外     开放   成绩    斐然
```
> convert example 2
![22.gv.pdf](./constituency_labeling/tests/examples/22.gv.svg)

> More example you can see [test](./constituency_labeling/tests/test_convert.py).

# 成分分析树标注工具

> 这个包的目的在于标注成分分析树。

从nltk标注出来的数据集来看，有点反直觉，标注起来很麻烦。
那么此包提供一个`LabelTree`，您可以通过这个类来生成例如`convert example1`以及`convert example2`，然后通过`label_tree_to_nltk`方法将其转换成符合nltk标注格式的数据出来。