import sys
sys.path.append('.')
from unittest import main, TestCase
from gengraph import gengraph
from testdata.importgraph import import_graph

class cpython_tests(TestCase):
    def test_gengraph(self):
        generated_graph = gengraph('testdata\\human.py')
        self.assertEquals(generated_graph, import_graph)

if __name__ == '__main__':
    main()
