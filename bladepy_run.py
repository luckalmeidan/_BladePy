import sys

from bladepy.layout_creator import pyui_creator

update_argument = False
compiling = False

try:
    if sys.argv[1] == "update":
        update_argument = True
    elif sys.argv[1] == "update_compile":
        update_argument = True
        compiling = True
    else:
        print("%s argument not recognized" % sys.argv[1])
except:
    pass

if update_argument:
    print("\nBladePy Application will now update\n")
    pyui_creator.updateApplication()

if not compiling:
    from bladepy.software_core import Core

    Core.main()
else:
    print("\nCompilation of BladeBy will now start \n\n")
