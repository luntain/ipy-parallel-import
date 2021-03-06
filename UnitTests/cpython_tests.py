import sys, os
sys.path.append('.')
from unittest import main, TestCase
from finddep import approx_size, find_dependencies, get_enclosing_packages, path2name
from testdata.importgraph import import_graph, expected_module_sizes
from pprint import pprint


class cpython_tests(TestCase):
    def test_finddep(self):
        generated_graph, module_sizes = find_dependencies(['testdata\\human.py'])
        self.assertEquals(generated_graph, import_graph)
        self.assertEquals(module_sizes, expected_module_sizes)

    def test_many_roots(self):
        generated_graph, module_sizes = find_dependencies(['testdata\\human.py', 'testdata\\sea\\fisherman.py'])
        full_graph = dict(import_graph)
        full_graph.update({'testdata.sea.fisherman': set(['testdata.sea.fish', 'testdata.sea', 'testdata'])})
        self.assertEquals(generated_graph, full_graph)
        self.assertTrue('testdata.human' in module_sizes, "lost first root's size")

    def test_get_enclosing_packages(self):
        self.assertEquals(get_enclosing_packages('modulefinder'), [])
        self.assertEquals(get_enclosing_packages('Main.Resolver'), ['Main'])
        self.assertEquals(set(get_enclosing_packages('Library.Engine.ResultGenerator')), set(['Library', 'Library.Engine']))

    def test_path2name(self):
        self.assertEquals(path2name(os.path.join('foo', 'bar', 'module.py')), 'foo.bar.module')

    def test_approx_size(self):
        class Mock: pass
        module = Mock()
        module.__code__ = Mock()
        module.__code__.co_code = range(2)
        self.assertEquals(approx_size(module), 2)

        module.__code__ = None
        self.assertEquals(approx_size(module), 1, 'codeless modules have size of 1')


if __name__ == '__main__':
    main()
