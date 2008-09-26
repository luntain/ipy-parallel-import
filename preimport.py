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

class ProgressReporter(object):
    def __init__(self, module_sizes, callback):
        self.module_sizes = module_sizes
        self.callback = callback
        self.total_size = sum(module_sizes.values())
        self.current_size = 0.0
        self.lock = object()

    def done(self, module_name):
        Monitor.Enter(self.lock)
        try:
            self.current_size += self.module_sizes[module_name]
            self.callback(self.current_size / self.total_size)
        finally:
            Monitor.Exit(self.lock)


def preimport(graph, module_sizes=None, callback=None, threads=4):

    taskmaster = ImportTaskMaster(graph)
    if module_sizes and callback:
        report_progress = ProgressReporter(module_sizes, callback).done
    else:
        report_progress = lambda *_: None

    def worker():
        while 1:
            next_module = taskmaster.next()
            if next_module == '!all_done!':
                return
            if next_module is None:
                Thread.Sleep(200)
            else:
                __import__(next_module)
                taskmaster.done(next_module)
                report_progress(next_module)

    workers = []
    for _ in range(threads):
        w = Thread(ThreadStart(worker))
        w.Start()
        workers.append(w)

    for w in workers:
        w.Join()

