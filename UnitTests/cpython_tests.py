import sys
sys.path.append('.')
from unittest import main, TestCase
from finddep import find_dependencies, get_enclosing_packages
from testdata.importgraph import import_graph
from pprint import pprint


class cpython_tests(TestCase):
    def test_finddep(self):
        generated_graph = find_dependencies('testdata\\human.py')
        self.assertEquals(generated_graph, import_graph)

    def test_removing_dependencies_on_enclosing_pacakges(self):
        generated_graph = find_dependencies('testdata\\sea\\fisherman.py')
        self.assertEquals(generated_graph['testdata.sea.fisherman'], set(['testdata.sea.fish']))

    def test_get_enclosing_packages(self):
        self.assertEquals(get_enclosing_packages('modulefinder'), [])
        self.assertEquals(get_enclosing_packages('Main.Resolver'), ['Main'])
        self.assertEquals(set(get_enclosing_packages('Library.Engine.ResultGenerator')), set(['Library', 'Library.Engine']))


if __name__ == '__main__':
    main()
