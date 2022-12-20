from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='constituency-tree-converter',
    version='1.0.11',
    packages=['con_tree_converter', ],
    url='https://github.com/geasyheart/constituency-tree-converter',
    license='MIT',
    author='yuzhang',
    author_email='geasyheart@163.com',
    description='constituency tree converter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=[
        'nltk==3.6.5'
    ],
    extras_require={
        'full': [
            'graphviz>=0.18.2'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
