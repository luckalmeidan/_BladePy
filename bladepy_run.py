import os
import subprocess
import sys

os.environ['MPLCONFIGDIR'] = "./bladepy/tecplot_modules/.cache"

from bladepy.layout_creator import pyui_creator

update = False
compiling = False

try:
    if sys.argv[1] == "update":
        update = True
    elif sys.argv[1] == "compile":
        update = True
        compiling = True
    else:
        print("%s argument not recognized" % sys.argv[1])
except:
    pass

if update:
    print("\nBladePy Application will now update\n")
    pyui_creator.updateApplication()

if compiling:
    print("\nCompilation of BladeBy will now start \n\n")
    os.chdir("./bin")
    subprocess.call(["pyinstaller", "bladepy_run_linux.spec"])
else:
    from bladepy.software_core import Core
    Core.main()


