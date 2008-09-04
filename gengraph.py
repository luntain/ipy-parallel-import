from py2depgraph import mymf
import sys, pprint

def main(argv):
    path = sys.path[:]
    path.append('.')
    debug = 0
    exclude = argv[1:]
    exclude.extend(["Main.Document.InputStream", "Library.Engine.ResultGenerator", 'unittest', 'copy'])
    mf = mymf(path,debug,exclude)
    mf.run_script(argv[0])
    print 'imports = ',
    pprint.pprint(mf._depgraph)

if __name__=='__main__':
    main(sys.argv[1:])
