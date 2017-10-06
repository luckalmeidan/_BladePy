import os
import subprocess
import sys

user_home = os.path.expanduser('~')
os.environ['MPLCONFIGDIR'] = os.path.join(user_home, ".config/BladePy/matplotlib/.cache")

from bladepy.layout_creator import pyui_creator

update = False
compiling = False
start_case = None

print(os.getcwd())
try:
    if sys.argv[1] in ("--update", "-u"):
        update = True
    elif sys.argv[1] in ("--compile", "-c"):
        update = True
        compiling = True
    else:
        start_case = []
        print("Application starting with ", sys.argv[1:])

        for arg in sys.argv[1:]:
            start_case.append(os.path.join(os.getcwd(), arg))
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

    Core.main(start_case)
