import sys, pprint

import modifiedmodulefinder

def get_enclosing_packages(name):
    def f(partial_prefixes, component):
        ps = map(lambda p: component + '.' + p, partial_prefixes)
        ps.append(component)
        return ps
    return reduce(f, reversed(name.split('.')[:-1]), [])


class ModuleDependencyFinder(modifiedmodulefinder.ModuleFinder):
    def __init__(self,*args,**kwargs):
        self.depgraph = {}
        modifiedmodulefinder.ModuleFinder.__init__(self,*args,**kwargs)

    def import_hook(self, name, caller=None, fromList=None):
        self.add_dependencies(name, caller, fromList)
        return modifiedmodulefinder.ModuleFinder.import_hook(self,name,caller,fromList)

    def add_dependencies(self, name, caller, fromList):
        from_names = map(lambda n: '.'+ n, fromList or [])
        from_names.append('')
        dependencies = map(lambda n: name + n, from_names)

        dependencies.extend(get_enclosing_packages(name))
        for dependency in dependencies:
            self.depgraph.setdefault(caller.__name__,set()).add(dependency)


def find_dependencies(roots):
    path = sys.path[:]
    path.append('.')
    mdf = ModuleDependencyFinder(path, debug=0, excludes=[])
    for root in roots:
        mdf.run_script(root)
        rename_main_module(mdf.depgraph, mdf.modules)
    return repair(mdf.depgraph, mdf.modules), {}


def rename_main_module(graph, modules):
    main_module_path = modules['__main__'].__file__
    root_module_name = main_module_path.rstrip('.py').replace('/', '.').replace('\\', '.')
    graph[root_module_name] = graph['__main__']
    del graph['__main__']


def repair(graph, modules):
    result = dict()
    for module, dependencies_dict in graph.items():
        enc_packages = get_enclosing_packages(module)
        result[module] = set(elem for elem in dependencies_dict if not elem in enc_packages and elem in modules)
    return result


def main(argv):
    depgraph, _ = find_dependencies(argv[0])
    print 'imports = ',
    pprint.pprint(depgraph)

if __name__=='__main__':
    main(sys.argv[1:])
