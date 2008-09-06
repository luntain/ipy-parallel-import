import sys, pprint

import modulefinder

class ModuleDependencyFinder(modulefinder.ModuleFinder):
    def __init__(self,*args,**kwargs):
        self.depgraph = {}
        modulefinder.ModuleFinder.__init__(self,*args,**kwargs)

    def import_hook(self, name, caller=None, fromList=None):
        self.add_dependencies(name, caller, fromList)
        return modulefinder.ModuleFinder.import_hook(self,name,caller,fromList)

    def add_dependencies(self, name, caller, fromList):
        from_names = map(lambda n: '.'+ n, fromList or [])
        from_names.append('')
        dependencies = map(lambda n: name + n, from_names)

        def f(partial_prefixes, component):
            ps = map(lambda p: component + '.' + p, partial_prefixes)
            ps.append(component)
            return ps
        dependencies.extend(reduce(f, reversed(name.split('.')), []))
        for dependency in dependencies:
            self.depgraph.setdefault(caller.__name__,set()).add(dependency)


def gengraph(root):
    path = sys.path[:]
    path.append('.')
    mdf = ModuleDependencyFinder(path, debug=0, excludes=[])
    mdf.run_script(root)
    return repair(mdf.depgraph, mdf.modules)


def repair(graph, modules):
    main_module_path = modules['__main__'].__file__
    root_module_name = main_module_path.rstrip('.py').replace('/', '.').replace('\\', '.')
    graph[root_module_name] = graph['__main__']
    del graph['__main__']

    result = dict()
    for module, dependencies_dict in graph.items():
        result[module] = set(elem for elem in dependencies_dict if not module.startswith(elem) and elem in modules)
    return result


def main(argv):
    depgraph = gengraph(argv[0])
    print 'imports = ',
    pprint.pprint(depgraph)

if __name__=='__main__':
    main(sys.argv[1:])
