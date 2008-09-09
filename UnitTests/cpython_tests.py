import sys
sys.path.append('.')
from unittest import main, TestCase
from finddep import find_dependencies
from testdata.importgraph import import_graph
from pprint import pprint


class cpython_tests(TestCase):
    def test_gengraph(self):
        generated_graph = find_dependencies('testdata\\human.py')
        pprint(generated_graph)
        self.assertEquals(generated_graph, import_graph)

if __name__ == '__main__':
    main()
