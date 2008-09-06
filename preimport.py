import sys

def preimport(graph):
    for key, value in graph.items():
        __import__(key)
        for module in value:
            __import__(module)

