import sys

from System.Threading import Monitor, Thread, ThreadStart

class ImportTaskMaster(object):
    def __init__(self, graph):
        self.mod2dep = graph
        self.leaves = set()
        for module in self.all_modules():
            if module not in self.mod2dep or not self.mod2dep[module]:
                self.leaves.add(module)
        self.lock = object()

    def all_modules(self):
        for module, dependencies in self.mod2dep.iteritems():
            for dep in dependencies:
                yield dep
            yield module

    def next(self):
        Monitor.Enter(self.lock)
        try:
            if self.leaves:
                module = self.leaves.pop()
                if module in self.mod2dep:
                    del self.mod2dep[module]
                return module
            else:
                if self.mod2dep:
                    return None
                else:
                    return '!all_done!'
        finally:
            Monitor.Exit(self.lock)

    def done(self, imported):
        Monitor.Enter(self.lock)
        try:
            for module, deps in self.mod2dep.items():
                if module == imported:
                    del self.mod2dep[imported]
                else:
                    if imported in deps:
                        deps.remove(imported)
                    if not deps:
                        self.leaves.add(module)
        finally:
            Monitor.Exit(self.lock)


def preimport(graph, threads=4):

    taskmaster = ImportTaskMaster(graph)

    def worker():
        while 1:
            next_module = taskmaster.next()
            if next_module == '!all_done!':
                return
            if next_module is None:
                print 'no modules eligible to import, sleeping'
                Thread.Sleep(200)
            else:
                __import__(next_module)
                taskmaster.done(next_module)

    workers = []
    for _ in range(threads):
        w = Thread(ThreadStart(worker))
        w.Start()
        workers.append(w)

    for w in workers:
        w.Join()

