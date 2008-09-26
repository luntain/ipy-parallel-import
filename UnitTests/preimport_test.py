from unittest import TestCase, TestLoader, TextTestRunner
from preimport import preimport, ImportTaskMaster, ProgressReporter
from testdata.importgraph import import_graph, expected_module_sizes
import sys


class preimport_test(TestCase):

    def test_empty_graph(self):
        preimport({})
        # should not blow up

    def test_real_importing(self):
        progress = []
        callback = progress.append
        nodes = reduce(set.union, import_graph.values(), set(import_graph.keys()))
        nodes.remove('testdata')
        for earthling in nodes:
            assert earthling not in sys.modules
        preimport(import_graph, expected_module_sizes, callback)
        for earthling in nodes:
            assert earthling in sys.modules
            del sys.modules[earthling]

        self.assertEquals(len(progress), len(expected_module_sizes))
        self.assertEquals(progress, sorted(progress), 'values are not increasing')
        self.assertEquals(progress[-1], 1.0)


class ImportTaskMasterTest(TestCase):

    def test_empty_graph(self):
        tm = ImportTaskMaster({})
        self.assertEquals(tm.next(), '!all_done!')
        self.assertEquals(tm.next(), '!all_done!')

    def test_simple_dependency(self):
        tm = ImportTaskMaster({'bear': set(['seal'])})
        self.assertEquals([tm.next(), tm.next(), tm.next()], ['seal', None, None])
        tm.done('seal')
        self.assertEquals([tm.next(), tm.next()], ['bear', '!all_done!'])

    def test_more_involved_case(self):
        tm = ImportTaskMaster({
            'human': set(['bear']),
            'bear': set(['seal', 'honey'])})

        self.assertEquals(set([tm.next(), tm.next()]), set(['seal', 'honey']))
        self.assertEquals(tm.next(), None)
        tm.done('seal')
        self.assertEquals(tm.next(), None)
        tm.done('honey')
        self.assertEquals([tm.next(), tm.next()], ['bear', None])
        tm.done('bear')
        self.assertEquals([tm.next(), tm.next()], ['human', '!all_done!'])


class ProgressReporterTest(TestCase):

    def test_it(self):
        module_sizes = {
            'foo': 1,
            'bar': 3,
        }
        calls = []
        reporter = ProgressReporter(module_sizes, calls.append)
        reporter.done('foo')
        reporter.done('bar')
        self.assertEquals(calls, [0.25, 1.0])



if __name__ == '__main__':
    test = TestLoader().loadTestsFromName('__main__')
    TextTestRunner().run(test)
