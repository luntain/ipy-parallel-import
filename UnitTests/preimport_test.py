from unittest import main, TestCase
from preimport import gengraph, preimport
import sys

import_graph = {
    'testdata.human': 'testdata.bear',
    'testdata.human': 'testdata.pelican',
    'testdata.bear': 'testdata.sea.fish',
    'testdata.pelican': 'testdata.sea.fish',
    'testdata.sea.fish': 'testdata.sea.plankton',
}

class preimport_test(TestCase):

    def test_empty_graph(self):
        preimport({})
        # should not blow up

    def test_one_edge_graph(self):
        nodes = set(import_graph.keys()).union(set(import_graph.values()))
        for earthling in nodes:
            assert earthling not in sys.modules
        preimport(import_graph)
        for earthling in nodes:
            assert earthling in sys.modules


    def test_gengraph(self):
        generated_graph = gengraph('testdata/bear.py')
        self.assertEquals(generated_graph, import_graph)


if __name__ == '__main__':
    main()
