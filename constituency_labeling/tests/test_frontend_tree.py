# -*- coding: utf8 -*-
#
from constituency_labeling.frontend_tree import FrontendTree
# 不一样的树格式
sample = {
    "data": {
        "words": "他指出要深入贯彻……论述，提高……站位，落实……责任",
        "label": "简单句",
        "child": [
            {
                "words": "他",
                "label": "主",
                "child": [],
            },
            {
                "words": "指出",
                "label": "谓",
                "child": [],
            },
            {
                "words": "要深入贯彻……论述，提高……站位，落实……责任",
                "label": "宾",
                "child": [
                    {
                        "words": "深入贯彻……论述",
                        "label": "并行1",
                        "child": [
                            {
                                "words": "他",
                                "label": "主",
                                "child": []
                            },
                            {
                                "words": "深入贯彻",
                                "label": "谓",
                                "child": []
                            },
                            {
                                "words": "……论述",
                                "label": "宾",
                                "child": []
                            }
                        ]
                    },
                    {
                        "words": "提高……站位",
                        "label": "并行2",
                        "child": [

                            {
                                "words": "提高",
                                "label": "谓",
                                "child": []
                            },
                            {
                                "words": "……站位",
                                "label": "宾",
                                "child": []
                            }
                        ]
                    },
                    {
                        "words": "落实……责任",
                        "label": "并行3",
                        "child": [

                            {
                                "words": "落实",
                                "label": "谓",
                                "child": []
                            },
                            {
                                "words": "……责任",
                                "label": "宾",
                                "child": []
                            }
                        ]
                    }
                ]
            }
        ]
    }
}

if __name__ == '__main__':
    tree = FrontendTree()
    tree.generate_tree(sample['data'])

    tree.pretty_tree(filename='f1')
