import sys, pprint, os

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

def approx_size(module):
    if module.__code__ is None:
        return 1
    return len(module.__code__.co_code)

def find_dependencies(roots):
    path = sys.path[:]
    path.append('.')
    mdf = ModuleDependencyFinder(path, debug=0, excludes=[])
    for root in roots:
        mdf.run_script(root)
        rename_main_module(mdf.depgraph, mdf.modules)
    module_sizes = {}
    for name, module in mdf.modules.iteritems():
        module_sizes[name] = approx_size(module)
    return repair(mdf.depgraph, mdf.modules), module_sizes


def path2name(path):
    return path.rstrip('.py').replace(os.path.sep, '.')

def rename_main_module(graph, modules):
    main_module_path = modules['__main__'].__file__
    root_module_name = path2name(main_module_path)
    graph[root_module_name] = graph['__main__']
    del graph['__main__']
    modules[root_module_name] = modules['__main__']
    del modules['__main__']


def repair(graph, modules):
    result = dict()
    for module, dependencies_dict in graph.items():
        enc_packages = get_enclosing_packages(module)
        result[module] = set(elem for elem in dependencies_dict if elem in modules)
    return result


def main(argv):
    depgraph, module_sizes = find_dependencies(argv)
    print 'imports = ',
    pprint.pprint(depgraph)
    print 'module_sizes = ',
    pprint.pprint(module_sizes)

if __name__=='__main__':
    main(sys.argv[1:])
