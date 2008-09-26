import sys, os
sys.path.append('.')
from unittest import main, TestCase
from finddep import find_dependencies, get_enclosing_packages, path2name
from testdata.importgraph import import_graph, expected_module_sizes
from pprint import pprint


class cpython_tests(TestCase):
    def test_finddep(self):
        generated_graph, module_sizes = find_dependencies(['testdata\\human.py'])
        self.assertEquals(generated_graph, import_graph)
        self.assertEquals(module_sizes, expected_module_sizes)

    def test_many_roots(self):
        generated_graph, _ = find_dependencies(['testdata\\human.py', 'testdata\\sea\\fisherman.py'])
        full_graph = dict(import_graph)
        full_graph.update({'testdata.sea.fisherman': set(['testdata.sea.fish', 'testdata.sea', 'testdata'])})
        self.assertEquals(generated_graph, full_graph)

    def test_get_enclosing_packages(self):
        self.assertEquals(get_enclosing_packages('modulefinder'), [])
        self.assertEquals(get_enclosing_packages('Main.Resolver'), ['Main'])
        self.assertEquals(set(get_enclosing_packages('Library.Engine.ResultGenerator')), set(['Library', 'Library.Engine']))

    def test_path2name(self):
        self.assertEquals(path2name(os.path.join('foo', 'bar', 'module.py')), 'foo.bar.module')

if __name__ == '__main__':
    main()
