import sys
from py2depgraph import mymf

def preimport(graph):
    for key, value in graph.items():
        __import__(key)
        __import__(value)

def gengraph(root):
    path = sys.path[:]
    path.append('.')
    debug = 0
    exclude = []
    mf = mymf(path, debug, exclude)
    mf.run_script(root)
    return mf._depgraph
