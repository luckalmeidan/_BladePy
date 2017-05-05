"""
@package tecplot_modules.tecplot_display

File that contains the class TecPlotWindow for adding functions to the BladePy TecplotWidget function-less layout
created in Qt Designer for the Blade Tecplot viewer. Functions include plotting, displaying and managing tecplot
graphics.

"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from scipy import interpolate

from bladepy.layout_creator import pyui_creator
from bladepy.tecplot_modules.tecplot_reader import TecPlotCore
from bladepy.tecplot_modules.tecplot_reader import tecplot_colors

ui_file = os.path.join(os.path.dirname(__file__), "tecplot_displayUI.ui")
py_ui_file = os.path.join(os.path.dirname(__file__), "tecplot_displayUI.py")

# Translate layout .ui file to .py file
pyui_creator.createPyUI(ui_file, py_ui_file)

from bladepy.tecplot_modules import tecplot_displayUI


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming
class TecPlotWindow(QtGui.QMainWindow, tecplot_displayUI.Ui_MainWindow):
    """
    Class for creating a GUI for the BladePy TecplotViewer Widget

    A object of this class will be created and integrated to the OutputViewer. This class has the function of displaying
    tecplot graphics, and  managing its appearance in the functions setVisibility() and setNeutral(). The padding, label
    and adjustments are made when plotting in plotFunction(). This object instantiates composition association object of
    tecplot_reader.TecPlotCore class. The object of this class is used for reading tecplot csv files.

    plotFunction() actually has the objective of directing the plots to the right canvas. The plotting and line creation
    are in fact made in methods tecplotDisplay_1(), tecplotDisplay_2(), tecplotDisplay_3(), and tecplotDisplay_4().

    The reason for having four different methods for plotting is the fact that each canvas has it own rule for plotting.

    This class is responsible for adding functions to the inherited tecplot_displayUI.Ui_MainWindow function-less
    layout created in Qt Designer.

    """

    def __init__(self, parent=None, OutputViewerWidget=None):
        super(TecPlotWindow, self).__init__(parent)
        self.ax1 = None
        self.ax2 = None
        self.ax3 = None
        self.ax4= None

        self.tecplot_blade_plotlines = []
        self.tecplot_stream_plotlines = []
        self.tecplot_profile_plotlines = []
        self.tecplot_mean_plotlines = []
        self.tecplot_profile_plotlines = []
        self.tecplot_mean_plotlines = []
        self.tecplot_meanbeta_plotlines = []
        self.tecplot_thickness_plotlines = []
        self.tecplot_stackcur_plotlines = []
        self.tecplot_stackpnts_plotlines = []
        # setup the initial display here
        self.setupUi(self)
        self.setCentralWidget(None)
        self.setWindowTitle("Tecplot Viewer Widget")

        # Object for Output Viewer
        self.op_viewer = OutputViewerWidget

        # Object for reading tecplot files and plotting
        self.tecplot_core = TecPlotCore()

        # Creates an object to read/process and plot tecplot files

        self._figure1 = plt.figure(1)
        self._figure2 = plt.figure(2)

        # Creates objects for the plots, FigureCanvas and NavigationToolbar
        self._canvas_1 = FigureCanvas(self._figure1)
        self._canvas_2 = FigureCanvas(self._figure2)
        self._toolbar_1 = NavigationToolbar(self._canvas_1, self, coordinates=True)
        self._toolbar_2 = NavigationToolbar(self._canvas_2, self, coordinates=True)

        # Adds the created objects for plots to the widgets in the GUI
        self.ui_tecplot1_widget_vl.addWidget(self._canvas_1)
        self.ui_tecplot1_widget_vl.addWidget(self._toolbar_1)
        self.ui_tecplot2_widget_vl.addWidget(self._canvas_2)
        self.ui_tecplot2_widget_vl.addWidget(self._toolbar_2)

        # Set transparency to the plots
        self._figure1.set_facecolor('none')
        self._figure2.set_facecolor('none')

    def openTecplot(self, tecplot_path=None):
        """
        Calls the function for reading tecplot csv files of tecplot_reader.TecPlotCore

        Then calls plotFunction() to plot the read files.

        @return None
        """
        # cleaning the reader
        self.tecplot_core.__init__()
        self.tecplot_core.tecplotReader(tecplot_path)

        self.plotFunction()

    def plotFunction(self):
        """
        Calls tecplot_core functions and saves it in instance variables and adjust graphics preferences_modules like padding

        @return None
        """


        plt.figure(self._figure1.number)
        self.ax1 = plt.subplot(211)

        plt.axis('equal')
        plt.tight_layout()

        self.ax1.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        self.tecplot_blade_plotlines, self.tecplot_stream_plotlines, self.tecplot_stackcur_plotlines =\
            self.tecplotDisplay_1()

        self.ax1.set_xlabel(self.ax1.get_xlabel(), fontsize=12, labelpad=0)
        self.ax1.set_ylabel(self.ax1.get_ylabel(), fontsize=12, labelpad=5)

        self.ax2 = plt.subplot(212)

        plt.axis('equal')

        self.tecplot_profile_plotlines, self.tecplot_mean_plotlines, self.tecplot_stackpnts_plotlines =\
            self.tecplotDisplay_2()

        self.ax2.set_xlabel(self.ax2.get_xlabel(), fontsize=12, labelpad=0)
        self.ax2.set_ylabel(self.ax2.get_ylabel(), fontsize=12, labelpad=-5)

        plt.subplots_adjust(top=.96, bottom=.07, right=.95, left=.12)
        plt.figure(self._figure2.number)

        self.ax3 = plt.subplot(211)

        plt.tight_layout()

        self.ax3.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        self.tecplot_thickness_plotlines = self.tecplotDisplay_3()
        self.ax3.set_xlabel(self.ax3.get_xlabel(), fontsize=12, labelpad=0)
        self.ax3.set_ylabel(self.ax3.get_ylabel(), fontsize=12, labelpad=5)

        self.ax4 = plt.subplot(212)

        self.ax4.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

        try:
            self.tecplot_meanbeta_plotlines = self.tecplotDisplay_4()
        except:
            pass

        self.ax4.set_xlabel(self.ax4.get_xlabel(), fontsize=12, labelpad=0)
        self.ax4.set_ylabel(self.ax4.get_ylabel(), fontsize=12, labelpad=5)

        plt.subplots_adjust(top=.96, bottom=.07, right=.90, left=.12)

        try:
            if self.op_viewer.ui_tecplot_toggle_grid_chk.isChecked():
                self.toggleGrid()
        except AttributeError:
            pass

        # plt.tight_layout(pad=1.3, w_pad=0.1, h_pad=.1)

        self.canvas(1).draw()
        self.canvas(2).draw()

    def tecplotDisplay_1(self):
        """
        Methods that are going to be called by the the TecplotWidget.

        @return [list] List of blade plotlines and list of lists of Stream Lines plotlines

        """

        # Te variable m is to make tecplot colors cycle according to tecplot_colors variables.
        # Matplotlib disposes of set of colors but they are not good as it can be.

        m = 0

        tecplotlist_stream_plotlines = []

        for n in range(0, len(self.tecplot_core.stream_z_list)):
            streamline = plt.plot(self.tecplot_core.stream_z_list[n], self.tecplot_core.stream_r_list[n],
                                  color=tecplot_colors[m % len(tecplot_colors)],
                                  lw=1.0,
                                  label='Streamline {i}'.format(i=n),)

            tecplotlist_stream_plotlines.append(streamline[0])

            # resets m counter or sums +1 to cycle colors.
            m += 1

        # Stores the plots in variables, that is, the lines of the plots. These variables can be used later to
        # modify the plot lines in the main GUI.
        hubline = plt.plot(self.tecplot_core.hub_z, self.tecplot_core.hub_r, 'k', label="_Hub")
        shroudline = plt.plot(self.tecplot_core.shroud_z, self.tecplot_core.shroud_r, 'k', label="_Shroud")

        trailingline = plt.plot(self.tecplot_core.trailing_z, self.tecplot_core.trailing_r, 'k',
                                label="_Trailing")
        leadingline = plt.plot(self.tecplot_core.leading_z, self.tecplot_core.leading_r, 'k',
                               label="_Leading")

        # converting stackcur coordinates to numpy objects
        self.tecplot_core.stackcur_z = np.asarray(self.tecplot_core.stackcur_z[::-1])
        self.tecplot_core.stackcur_r = np.asarray(self.tecplot_core.stackcur_r[::-1])

        # Creating interpolating object



        try:
            splining_points = 500
            tck, u = interpolate.splprep([self.tecplot_core.stackcur_z, self.tecplot_core.stackcur_r], s=0)
            u_smooth = np.linspace(u.min(), u.max(), splining_points)
            self.tecplot_core.stackcur_z_smooth, self.tecplot_core.stackcur_r_smooth = interpolate.splev(u_smooth, tck, der=0)

            tecplotlist_stackcur_plotline = plt.plot(self.tecplot_core.stackcur_z_smooth,
                                                      self.tecplot_core.stackcur_r_smooth, '#ff6600',
                                                      label="_Stackcur")
        except (TypeError, ValueError):
            tecplotlist_stackcur_plotline = []

        plt.xlabel("Z")
        plt.ylabel("R")

        # The main reason that the lines for the blades is stored separately from the streamlines is that they
        # are not going to pass through same modifications. E.g. it is set that the blade lines will not be dashed
        # in "neutral mode" as the stream lines.
        tecplotlist_blade_plotlines = hubline + shroudline + trailingline + leadingline

        return tecplotlist_blade_plotlines, tecplotlist_stream_plotlines, tecplotlist_stackcur_plotline

    def tecplotDisplay_2(self):
        """
        Methods that are going to be called by the the TecplotWidget.

        @return [list] List of lists of blade profiles plotlines and list of lists of Mean Lines plotlines


        """

        m = 0

        tecplotlist_profile_plotlines = []
        tecplotlist_mean_plotlines = []

        tecplotlist_stackpnts_plotline = plt.plot(self.tecplot_core.stackcur_mp, self.tecplot_core.stackcur_th,
                                                 color = '#ff6600',
                                                 marker="o",
                                                 linestyle='None',
                                                 label = '_Stackcur')


        for n in range(0, len(self.tecplot_core.bladeprofile_mp_list)):
            profileline = plt.plot(self.tecplot_core.bladeprofile_mp_list[n], self.tecplot_core.bladeprofile_th_list[n],
                                   color=tecplot_colors[m],
                                   label='Bladeprofile {i}'.format(i=n))

            meanline = plt.plot(self.tecplot_core.meanline_mp_list[n], self.tecplot_core.meanline_th_list[n],
                                color=tecplot_colors[m % len(tecplot_colors)],
                                label='Meanline {i}'.format(i=n))


            tecplotlist_profile_plotlines.append(profileline[0])
            tecplotlist_mean_plotlines.append(meanline[0])

            m += 1



        plt.xlabel("MP")
        plt.ylabel("TH")

        return tecplotlist_profile_plotlines, tecplotlist_mean_plotlines, tecplotlist_stackpnts_plotline

    def tecplotDisplay_3(self):
        """
        Methods that are going to be called by the the TecplotWidget.

        @return [list] List of lists of thickness plotlines

        """

        m = 0
        tecplotlist_thickness_plotlines = []
        for n in range(0, len(self.tecplot_core.thickness_s_list)):
            thicknessline = plt.plot(self.tecplot_core.thickness_s_list[n], self.tecplot_core.thickness_t_list[n],
                                     color=tecplot_colors[m % len(tecplot_colors)],
                                     label='Thickness {i}'.format(i=n))

            tecplotlist_thickness_plotlines.append(thicknessline[0])

            m += 1

        plt.xlabel("S")
        plt.ylabel("T")

        return tecplotlist_thickness_plotlines

    def tecplotDisplay_4(self):
        """
        Methods that are going to be called by the the TecplotWidget.

        @return [list] List of lists of thickness plotlines

        """

        m = 0
        tecplotlist_meanbeta_plotlines = []


        # Exception is case list is empty to not crash "all" built-in function

        for n in range(0, len(self.tecplot_core.meanline_beta_list)):
            # TODO: weak condition to verify meanline_s

            # if "S" coordinate is empty or only zeros, plot MP x Beta.
            meanbetaline = plt.plot(self.tecplot_core.meanline_m_list[n], self.tecplot_core.meanline_beta_list[n],
                                    color=tecplot_colors[m % len(tecplot_colors)],
                                    label='Meanline {i}'.format(i=n))
            tecplotlist_meanbeta_plotlines.append(meanbetaline[0])

            x_label = "M"



            m += 1

        plt.xlabel(x_label)
        plt.ylabel("BETA")

        return tecplotlist_meanbeta_plotlines

    def setNeutral(self) -> None:
        """
        Toggles tecplot display to neutral.

        Sets to neutral mode - black and dashed lines - or to standard for the selected case. For hub and
        shroud there is no neutral state. Only stream lines will become dashed a blacked.

        @return None

        """

        # First checks the state of tecplot graphics. Then switch to neutral or to colorful
        if self._exceptionCatch():
            return

        try:
            temp_line_list_color = []
            to_save_color_list = []

            if self.op_viewer.case_node.tecplotIsNeutral:
                # Iterates through all sub-plots of the tecplots graphics.

                for n in range(1, len(self.op_viewer.case_node.tecplotLists)):
                    # m is a variable for cycling through tecplot_colors
                    for index, line in enumerate(self.op_viewer.case_node.tecplotLists[n]):
                        line.set_color(self.op_viewer.case_node.tecplotSavedColorList[n-1][index])

                        if line.get_linestyle() != "None":
                            line.set_linestyle('-')

                # the attribute below is to setup the condition of the current state of tecplot

                self.op_viewer.case_node.tecplotMode = "standard"

                # Every modifying in the graphics appearances of tecplot must be redrawn.
                self.canvas(1).draw()
                self.canvas(2).draw()

                # Sends the signal to treeview to update tecplot condition

                self.op_viewer.model.dataChanged.emit(self.op_viewer.ui_case_treeview.currentIndex(),
                                                      self.op_viewer.ui_case_treeview.indexBelow(
                                                          self.op_viewer.ui_case_treeview.currentIndex()))

            else:
                for n in range(1, len(self.op_viewer.case_node.tecplotLists)):
                    for line in self.op_viewer.case_node.tecplotLists[n]:
                        temp_line_list_color.append(line.get_color())
                        line.set_color("k")
                        if line.get_linestyle() != "None":
                            line.set_linestyle("--")

                    to_save_color_list.append(temp_line_list_color)
                    temp_line_list_color = []

                self.op_viewer.case_node.tecplotSavedColorList = to_save_color_list
                self.op_viewer.case_node.tecplotMode = "neutral"
                self.canvas(1).draw()
                self.canvas(2).draw()

                self.op_viewer.model.dataChanged.emit(self.op_viewer.ui_case_treeview.currentIndex(),
                                                      self.op_viewer.ui_case_treeview.indexBelow(
                                                          self.op_viewer.ui_case_treeview.currentIndex()))
        except AttributeError:
            pass

    def setVisibility(self) -> None:
        """
        Toggles tecplot display to visible or invisible for the selected case.

        @return  None

        """

        if self._exceptionCatch():
            return

        # First checks if any tecplot output was in fact loaded to start manipulating the condition.
        try:
            # if it is visible, turns to invisible and vice-versa
            if self.op_viewer.case_node.tecplotIsVisible:
                # it must save the style list to recover it for re-displaying in way before making it invisbile.
                temp_line_list = []
                to_save_style_list = []

                for n in range(0, len(self.op_viewer.case_node.tecplotLists)):
                    for line in self.op_viewer.case_node.tecplotLists[n]:
                        temp_line_list.append(line.get_visible())
                        line.set_visible(False)

                    to_save_style_list.append(temp_line_list)
                    temp_line_list = []

                self.op_viewer.ui_tecplot_setneutral_btn.setEnabled(False)
                self.op_viewer.ui_tecplot_toggle_bladeprofiles_btn.setEnabled(False)
                self.op_viewer.ui_tecplot_toggle_meanlines_btn.setEnabled(False)
                self.op_viewer.ui_tecplot_toggle_streamlines_chk.setEnabled(False)
                self.op_viewer.ui_tecplot_toggle_stackcurves_btn.setEnabled(False)

                self.op_viewer.case_node.tecplotSavedStyleList = to_save_style_list
                self.op_viewer.case_node.tecplotVisibility = "invisible"

                self.op_viewer.model.dataChanged.emit(self.op_viewer.ui_case_treeview.currentIndex(),
                                                      self.op_viewer.ui_case_treeview.indexBelow(
                                                          self.op_viewer.ui_case_treeview.currentIndex()))
            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.
                for n in range(0, len(self.op_viewer.case_node.tecplotLists)):
                    for index, line in enumerate(self.op_viewer.case_node.tecplotLists[n]):
                        line.set_visible(self.op_viewer.case_node.tecplotSavedStyleList[n][index])


                self.op_viewer.ui_tecplot_setneutral_btn.setEnabled(True)
                self.op_viewer.ui_tecplot_toggle_bladeprofiles_btn.setEnabled(True)
                self.op_viewer.ui_tecplot_toggle_meanlines_btn.setEnabled(True)
                self.op_viewer.ui_tecplot_toggle_streamlines_chk.setEnabled(True)
                self.op_viewer.ui_tecplot_toggle_stackcurves_btn.setEnabled(True)

                self.op_viewer.case_node.tecplotVisibility = "visible"

                self.op_viewer.model.dataChanged.emit(self.op_viewer.ui_case_treeview.currentIndex(),
                                                      self.op_viewer.ui_case_treeview.indexBelow(
                                                          self.op_viewer.ui_case_treeview.currentIndex()))

            self.canvas(1).draw()
            self.canvas(2).draw()
        except AttributeError:
            pass

    def toggleMeanLines(self):
        """
        Toggles tecplot display to visible or invisible for the selected case mean lines.


        @return  None
        """
        # TODO: implement method toggleMeanLines
        # TODO: describe docstring
        # TODO: Comment
        if self._exceptionCatch():
            return

        try:
            # if it is visible, turns to invisible and vice-versa
            if self.op_viewer.case_node.tecplotMeanLinesIsVisible:
                # it must save the style list to recover it for re-displaying in way before making it invisbile.
                temp_line_list = []
                to_save_style_list = []

                for line in self.op_viewer.case_node.tecplotLists[4]:
                    temp_line_list.append(line.get_visible())
                    line.set_visible(False)

                to_save_style_list.append(temp_line_list)

                self.op_viewer.case_node.tecplotMeanLinesSavedStyleList = to_save_style_list

                self.op_viewer.case_node.tecplotMeanLinesVisibility = "invisible"


            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.

                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[4]):
                    line.set_visible(self.op_viewer.case_node.tecplotMeanLinesSavedStyleList[0][index])


                self.op_viewer.case_node.tecplotMeanLinesVisibility = "visible"

            self.canvas(1).draw()
            self.canvas(2).draw()

        except AttributeError:
            pass

    def toggleBladeProfiles( self ):
        """
        Toggles tecplot display to visible or invisible for the selected case mean lines.



        @return  None
        """
        # TODO: describe docstring
        # TODO: Comment
        # TODO: Prevent user from clicking before
        if self._exceptionCatch():
            return

        try:
            if self.op_viewer.case_node.tecplotBladeProfilesIsVisible:
                # it must save the style list to recover it for re-displaying in way before making it invisbile.
                temp_line_list = []
                to_save_style_list = []

                for line in self.op_viewer.case_node.tecplotLists[3]:
                    temp_line_list.append(line.get_visible())
                    line.set_visible(False)

                to_save_style_list.append(temp_line_list)

                self.op_viewer.case_node.tecplotBladeProfilesSavedStyleList = to_save_style_list

                self.op_viewer.case_node.tecplotBladeProfilesVisibility = "invisible"


            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.


                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[3]):
                    line.set_visible(self.op_viewer.case_node.tecplotBladeProfilesSavedStyleList[0][index])

                self.op_viewer.case_node.tecplotBladeProfilesVisibility = "visible"

            self.canvas(1).draw()
            self.canvas(2).draw()

        except AttributeError:
            pass

    def toggleStreamLines(self):
        """
        Toggles tecplot display to visible or invisible for the selected case mean lines.



        @return  None
        """
        # TODO: describe docstring
        # TODO: Comment
        # TODO: Prevent user from clicking before
        if self._exceptionCatch():
            return

        try:
            if self.op_viewer.case_node.tecplotStreamLinesIsVisible:
                # it must save the style list to recover it for re-displaying in way before making it invisbile.
                temp_line_list = []
                to_save_style_list = []

                for line in self.op_viewer.case_node.tecplotLists[2]:
                    temp_line_list.append(line.get_visible())
                    line.set_visible(False)

                to_save_style_list.append(temp_line_list)

                self.op_viewer.case_node.tecplotStreamLinesSavedStyleList = to_save_style_list

                self.op_viewer.case_node.tecplotStreamLinesVisibility = "invisible"


            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.


                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[2]):
                    line.set_visible(self.op_viewer.case_node.tecplotStreamLinesSavedStyleList[0][index])

                self.op_viewer.case_node.tecplotStreamLinesVisibility = "visible"

            self.canvas(1).draw()
            self.canvas(2).draw()
        except AttributeError:
            pass

    def toggleStackCur(self):
        """
        Toggles tecplot display to visible or invisible for the selected case mean lines.



        @return  None
        """
        if self._exceptionCatch():
            return

        # TODO: describe docstring
        # TODO: Comment
        # TODO: Prevent user from clicking before

        try:
            if self.op_viewer.case_node.tecplotStackCurIsVisible:
                # it must save the style list to recover it for re-displaying in way before making it invisbile.
                temp_line_list = []
                to_save_style_list = []

                for line in self.op_viewer.case_node.tecplotLists[1]:
                    temp_line_list.append(line.get_visible())
                    line.set_visible(False)

                to_save_style_list.append(temp_line_list)

                self.op_viewer.case_node.tecplotStackCurSavedStyleList = to_save_style_list

                self.op_viewer.case_node.tecplotStackCurVisibility = "invisible"


            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.
                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[1]):
                    line.set_visible(self.op_viewer.case_node.tecplotStackCurSavedStyleList[0][index])

                self.op_viewer.case_node.tecplotStackCurVisibility = "visible"

            self.canvas(1).draw()
            self.canvas(2).draw()
        except AttributeError:
            pass

    def toggleGrid(self):
        """

        :return:
        """
        try:
            if self.op_viewer.ui_tecplot_toggle_grid_chk.isChecked():
                check = True
            elif not self.op_viewer.ui_tecplot_toggle_grid_chk.isChecked():
                check = False

            for axis in [self.ax1, self.ax2, self.ax3, self.ax4]:
                axis.grid(check)

            self.canvas(1).draw()
            self.canvas(2).draw()

        except AttributeError:
            pass


        # TODO: DOCSTRINGS

    def tighten(self):
        """

        :return:
        """
        try:
            for axis in [self.ax1, self.ax2, self.ax3, self.ax4]:
                axis.relim(visible_only=True)
                axis.autoscale(enable=True, axis='both', tight=True)


            self.canvas(1).draw()
            self.canvas(2).draw()

        except AttributeError:
            pass

        # TODO: Docstrings, Comment

    def relimScale(self):
        """

        :return:
        """

        # TODO: Docsstrings
        try:
            for axis in [self.ax1, self.ax2, self.ax3, self.ax4]:
                axis.relim()
                axis.autoscale_view()

            self.canvas(1).draw()
            self.canvas(2).draw()

        except AttributeError:
            pass

    def canvas(self, canvas_number):
        """

        :param canvas_number:
        :return:
        """
        # TODO : Docstring
        if canvas_number == 1:
            return self._canvas_1
        elif canvas_number == 2:
            return self._canvas_2

    def _exceptionCatch(self):
        """
        This functions is a exception catcher: if user tries to wrongly set properties when there is nothing to be
        applied by them


        @return None
        """
        number_of_cases = self.op_viewer.model.rowCount(self.op_viewer.ui_case_treeview.rootIndex())

        if self.op_viewer.case_node.tecplotMode == "None" or number_of_cases == 0:
            print("Action not feasible")
            return True

    def debug(self):
           pass





def main( ):
    app = QtGui.QApplication(sys.argv)
    tecplot_window = TecPlotWindow()

    tecplot_window.show()
    tecplot_window.openTecplot("./tecplot_sample/612-0-1.2d.tec.dat")
    tecplot_window.debug()
    # MainWindow.setgui()
    app.exec_()

    # inifile.close()
    print("End of Main Function UI")
    return tecplot_window


if __name__ == "__main__":
    main()

