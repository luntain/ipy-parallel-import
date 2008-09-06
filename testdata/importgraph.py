import_graph = {
    'testdata.human': set(['testdata.bear', 'testdata.pelican']),
    'testdata.bear': set(['testdata.sea.fish', 'testdata.sea']),
    'testdata.pelican': set(['testdata.sea.fish', 'testdata.sea']),
    'testdata.sea.fish': set(['testdata.sea.plankton']),
}
