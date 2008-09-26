import_graph = {
    'testdata.human': set(['testdata', 'testdata.bear', 'testdata.pelican']),
    'testdata.bear': set(['testdata', 'testdata.sea.fish', 'testdata.sea']),
    'testdata.pelican': set(['testdata', 'testdata.sea.fish', 'testdata.sea']),
    'testdata.sea.fish': set(['testdata', 'testdata.sea', 'testdata.sea.plankton']),
}
expected_module_sizes = {
    'testdata': 4,
    'testdata.human': 22,
    'testdata.bear': 17,
    'testdata.pelican': 23,
    'testdata.sea': 4,
    'testdata.sea.fish': 28,
    'testdata.sea.plankton': 49,
}
