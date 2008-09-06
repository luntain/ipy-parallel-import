from unittest import TestCase, TestLoader, TextTestRunner
from preimport import preimport
from testdata.importgraph import import_graph
import sys


class preimport_test(TestCase):

    def test_empty_graph(self):
        preimport({})
        # should not blow up

    def test_one_edge_graph(self):
        nodes = reduce(set.union, import_graph.values(), set(import_graph.keys()))
        for earthling in nodes:
            assert earthling not in sys.modules
        preimport(import_graph)
        for earthling in nodes:
            assert earthling in sys.modules


if __name__ == '__main__':
    test = TestLoader().loadTestsFromName('__main__')
    TextTestRunner().run(test)
