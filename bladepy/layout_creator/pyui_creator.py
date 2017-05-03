import os
import sys

from PyQt4 import QtCore
from PyQt4.uic.driver import Driver
update_ui = True

class pyOutputObject(object):
    #
    def __init__(self, py_output):
        self.indent = 4
        self.execute = True
        self.output = py_output
        self.pyqt3_wrapper = False
        self.debug = False
        self.preview = False
        self.resource_suffix = '_rc'
        self.from_imports = False


def createPyUI(input_ui_file_dir, output_py_file_dir):
    """
    Function to translate a .ui file created in Qt Designer to a .py file that is readable by PyQt.

    This is a tailored version of pyuic and it is under PyQt GNU v3

    @param input_ui_file_dir [.ui file] A file created in Qt Designer
    @param output_py_file_dir [.py file] A file that will be the translation of the file created in Qt Designer
    @return None
    """

    Version = "Python User Interface Compiler %s for Qt version %s" % (QtCore.PYQT_VERSION_STR, QtCore.QT_VERSION_STR)
    if update_ui:
        if sys.hexversion >= 0x03000000:
            from PyQt4.uic.port_v3.invoke import invoke
        else:
            from PyQt4.uic.port_v2.invoke import invoke

        opts = pyOutputObject(output_py_file_dir)
        args = [input_ui_file_dir]

        if len(args) != 1:
            sys.stderr.write("Error: one input ui-file must be specified\n")
            sys.exit(1)

        invoke(Driver(opts, args[0]))

    # Former code
    # def createPyUI(input_ui_file_dir, output_py_file_dir):
    #     """
    #     Function to translate a .ui file created in Qt Designer to a .py file that is readable by PyQt.
    #
    #     @param input_ui_file_dir [.ui file] A file created in Qt Designer
    #     @param output_py_file_dir [.py file] A file that will be the translation of the file created in Qt Designer
    #     @return None
    #     """
    #
    #     # Finds the absolute path for the PyQt .ui translator module
    #     pyui_creator_dir = os.path.join(os.path.dirname(__file__), "pyuic.py")
    #
    #     # Creates a variable that is "python absolute_path\pyuic.py" to be run afterwards
    #     command_starter = "python %s" % pyui_creator_dir
    #
    #     # Display a message that the translated .py files are being updated (or created)
    #     print("Updating %s..." % os.path.basename(output_py_file_dir))
    #
    #     # Executes the command in a Terminal
    #     os.system("%s -x %s -o %s" % (command_starter, input_ui_file_dir, output_py_file_dir))
    #
    #     return
    # parser = optparse.OptionParser(usage="pyuic4 [options] <ui-file>",
    #                                version=Version)
    # parser.add_option("-p", "--preview", dest="preview", action="store_true",
    #                   default=False,
    #                   help="show a preview of the UI instead of generating code")
    # parser.add_option("-o", "--output", dest="output", default="-", metavar="FILE",
    #                   help="write generated code to FILE instead of stdout")
    # parser.add_option("-x", "--execute", dest="execute", action="store_true",
    #                   default=False,
    #                   help="generate extra code to test and display the class")
    # parser.add_option("-d", "--debug", dest="debug", action="store_true",
    #                   default=False, help="show debug output")
    # parser.add_option("-i", "--indent", dest="indent", action="store", type="int",
    #                   default=4, metavar="N",
    #                   help="set indent width to N spaces, tab if N is 0 [default: 4]")
    # parser.add_option("-w", "--pyqt3-wrapper", dest="pyqt3_wrapper",
    #                   action="store_true", default=False,
    #                   help="generate a PyQt v3 style wrapper")
    #
    # g = optparse.OptionGroup(parser, title="Code generation options")
    # g.add_option("--from-imports", dest="from_imports", action="store_true",
    #              default=False, help="generate imports relative to '.'")
    # g.add_option("--resource-suffix", dest="resource_suffix", action="store",
    #              type="string", default="_rc", metavar="SUFFIX",
    #              help="append SUFFIX to the basename of resource files [default: _rc]")
    # parser.add_option_group(g)
    #
    # opts, args = parser.parse_args()
