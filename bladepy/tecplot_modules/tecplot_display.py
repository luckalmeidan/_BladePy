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
from math import pi

from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from scipy import interpolate

from bladepy.layout_creator import pyui_creator
from bladepy.tecplot_modules.tecplot_reader import TecPlotCore
from bladepy.tecplot_modules.tecplot_reader import tecplot_colors
from bladepy.tecplot_modules.ibl_reader import IblReader

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
        self.ax4 = None

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

    def openTecplot(self, tecplot_path=None, points_reader=None):
        """
        Calls the function for reading tecplot csv files of tecplot_reader.TecPlotCore

        Then calls plotFunction() to plot the read files.

        @return None
        """
        # cleaning the reader
        self.tecplot_core.__init__()
        self.tecplot_core.tecplotReader(tecplot_path)

        self.plotFunction(points_reader)

    def plotFunction(self, points_reader):
        """
        Calls tecplot_core functions and saves it in instance variables and adjust graphics preferences_modules like
        padding

        @return None
        """

        plt.figure(self._figure1.number)
        self.ax1 = plt.subplot(211)

        plt.axis('equal')
        plt.tight_layout()

        self.ax1.ticklabel_format(axis='y',  style='sci', scilimits=(0, 0), useOffset=False)
        self.ax1.ticklabel_format(axis='x', useOffset=False)
        self.tecplot_blade_plotlines, self.tecplot_stream_plotlines, self.tecplot_stackcur_plotlines, self.tecplot_stream_vectors_plotlines, self.points_list = self.tecplotDisplay_1(points_reader)

        self.ax1.set_xlabel(self.ax1.get_xlabel(), fontsize=12, labelpad=0)
        self.ax1.set_ylabel(self.ax1.get_ylabel(), fontsize=12, labelpad=5)

        self.ax2 = plt.subplot(212)

        plt.axis('equal')

        self.tecplot_profile_plotlines, self.tecplot_mean_plotlines, self.tecplot_stackpnts_plotlines, self.tecplot_profile_vectors_plotlines = \
            self.tecplotDisplay_2()

        self.ax2.set_xlabel(self.ax2.get_xlabel(), fontsize=12, labelpad=0)
        self.ax2.ticklabel_format(axis='y', style='sci', scilimits=(0, 0), useOffset=False)
        self.ax2.ticklabel_format(axis='x', useOffset=False)

        plt.subplots_adjust(top=.98, bottom=.04, right=.95, left=.13, hspace=0.12)
        plt.figure(self._figure2.number)

        self.ax3 = plt.subplot(211)

        plt.tight_layout()

        self.ax3.ticklabel_format(axis='y', style='sci', scilimits=(0, 0), useOffset=False)
        self.ax3.ticklabel_format(axis='x', useOffset=False)

        self.tecplot_thickness_plotlines = self.tecplotDisplay_3()
        self.ax3.set_xlabel(self.ax3.get_xlabel(), fontsize=12, labelpad=0)
        self.ax3.set_ylabel(self.ax3.get_ylabel(), fontsize=12, labelpad=5)

        self.ax4 = plt.subplot(212)

        self.ax4.ticklabel_format(axis='y', style='sci', scilimits=(0, 0),useOffset=False)
        self.ax4.ticklabel_format(axis='x', useOffset=False)

        try:
            self.tecplot_meanbeta_plotlines = self.tecplotDisplay_4()
        except:
            pass

        self.ax4.set_xlabel(self.ax4.get_xlabel(), fontsize=12, labelpad=0)
        self.ax4.set_ylabel(self.ax4.get_ylabel(), fontsize=12, labelpad=5)

        plt.subplots_adjust(top=.98, bottom=.04, right=.95, left=.13, hspace=0.12)

        try:
            if self.op_viewer.ui_tecplot_toggle_grid_chk.isChecked():
                self.toggleGrid()
        except AttributeError:
            pass

        # plt.tight_layout(pad=1.3, w_pad=0.1, h_pad=.1)

        self.canvas(1).draw()
        self.canvas(2).draw()

    def _getVector(self, x_list, y_list, color='k', pos=3):

        context_color = color

        list_middle_index = int(len(x_list) / pos)
        coordinates = np.array(([x_list[list_middle_index],
                                 y_list[list_middle_index],
                                 x_list[list_middle_index + 1],
                                 y_list[list_middle_index + 1]])).astype(np.float)

        X, Y, U, V = coordinates

        vector = plt.arrow(X, Y, U - X, V - Y,
                         shape='full',
                         lw=0,
                         length_includes_head=True,
                         head_width=self._ref_length * 0.02,
                         color=context_color)

        return vector

    @staticmethod
    def _computeLength(x_list, y_list):
        length = 0
        x_array = np.array(x_list).astype(np.float)
        y_array = np.array(y_list).astype(np.float)

        for n in range(0, len(x_array) - 1):
            length += ((x_array[n + 1] - x_array[n]) ** 2 + (y_array[n + 1] - y_array[n]) ** 2) ** .5

        return length

    def tecplotDisplay_1(self, points_reader):
        """
        Methods that are going to be called by the the TecplotWidget.

        @return [list] List of blade plotlines and list of lists of Stream Lines plotlines

        """

        # Te variable m is to make tecplot colors cycle according to tecplot_colors variables.
        # Matplotlib disposes of set of colors but they are not good as it can be.



        # geometric mean for length reference
        self._ref_length = (self._computeLength(self.tecplot_core.hub_z, self.tecplot_core.hub_r)*
                      self._computeLength(self.tecplot_core.leading_z, self.tecplot_core.leading_r))**.5

        # Quadratic mean
        #ref_length = ((computeLength(self.tecplot_core.hub_z, self.tecplot_core.hub_r)**2+
        # computeLength(self.tecplot_core.leading_z, self.tecplot_core.leading_r)**2)/2.0)**.5

        # Quadratic mean for leading and trailing
        #ref_length = ((computeLength(self.tecplot_core.trailing_z, self.tecplot_core.trailing_r)**2+
        #              computeLength(self.tecplot_core.leading_z, self.tecplot_core.leading_r)**2)/2.0)**.5



        m = 0

        tecplotlist_stream_plotlines = []
        points_list = []
        vectors_plotlines = []


        for n in range(0, len(self.tecplot_core.stream_z_list)):
            streamline = plt.plot(self.tecplot_core.stream_z_list[n], self.tecplot_core.stream_r_list[n],
                                  color=tecplot_colors[m % len(tecplot_colors)],
                                  lw=1.0,
                                  label='Streamline {i}'.format(i=n))


            # stream_vectors = plt.quiver(X, Y, U-X, V-Y, angles = 'xy',
            #                            scale_units = 'xy',
            #                            headlength= 30,
            #                            width = 0.0005,
            #
            #                            headwidth= 30,
            #
            #                            scale = .5,
            #                            color= tecplot_colors[m % len(tecplot_colors)])

            vectors_plotlines.append(self._getVector(self.tecplot_core.stream_z_list[n], self.tecplot_core.stream_r_list[n],
                                               color=tecplot_colors[m % len(tecplot_colors)]))
            tecplotlist_stream_plotlines.append(streamline[0])

            # resets m counter or sums +1 to cycle colors.
            m += 1

        # Stores the plots in variables, that is, the lines of the plots. These variables can be used later to
        # modify the plot lines in the main GUI.
        hubline = plt.plot(self.tecplot_core.hub_z, self.tecplot_core.hub_r, 'k', label="_Hub")
        vectors_plotlines.append(self._getVector(self.tecplot_core.hub_z, self.tecplot_core.hub_r))
        vectors_plotlines.append(self._getVector(self.tecplot_core.hub_z, self.tecplot_core.hub_r))


        shroudline = plt.plot(self.tecplot_core.shroud_z, self.tecplot_core.shroud_r, 'k', label="_Shroud")
        vectors_plotlines.append(self._getVector(self.tecplot_core.shroud_z, self.tecplot_core.shroud_r))

        trailingline = plt.plot(self.tecplot_core.trailing_z, self.tecplot_core.trailing_r, 'k', label="_Trailing")
        vectors_plotlines.append(self._getVector(self.tecplot_core.trailing_z, self.tecplot_core.trailing_r))

        leadingline = plt.plot(self.tecplot_core.leading_z, self.tecplot_core.leading_r, 'k', label="_Leading")
        vectors_plotlines.append(self._getVector(self.tecplot_core.leading_z, self.tecplot_core.leading_r))

        # converting stackcur coordinates to numpy objects
        self.tecplot_core.stackcur_z = np.asarray(self.tecplot_core.stackcur_z)
        self.tecplot_core.stackcur_r = np.asarray(self.tecplot_core.stackcur_r)

        # Creating interpolating object

        if points_reader:
            points_list = []
            points_list.extend(plt.plot(points_reader.hub.z[0], points_reader.hub.r[0], 'ko', markersize="3", label="_HubPoints"))
            points_list.extend(plt.plot(points_reader.tip.z[0], points_reader.tip.r[0], 'ko',  markersize="3",label="_HubPoints"))
            m = 0
            for n in range(points_reader.surface.numberSubSections()):
                color = tecplot_colors[m % len(tecplot_colors)]
                points_list.extend(plt.plot(points_reader.surface.z[n], points_reader.surface.r[n], "o", markersize="3", color=color))
                points_list.extend(plt.plot(points_reader.te_surface.z[n], points_reader.te_surface.r[n], "o", markersize="3", color=color))
                points_list.extend(plt.plot(points_reader.le_surface.z[n], points_reader.le_surface.r[n], "o", markersize="3", color=color))

                m += 1

        try:
            splining_points = 500
            tck, u = interpolate.splprep([self.tecplot_core.stackcur_z, self.tecplot_core.stackcur_r], s=0)
            u_smooth = np.linspace(u.min(), u.max(), splining_points)
            self.tecplot_core.stackcur_z_smooth, self.tecplot_core.stackcur_r_smooth = interpolate.splev(u_smooth, tck,
                                                                                                         der=0)

            tecplotlist_stackcur_plotline = plt.plot(self.tecplot_core.stackcur_z_smooth,
                                                     self.tecplot_core.stackcur_r_smooth, '#ff6600',
                                                     label="_Stackcur")

            vectors_plotlines.append(self._getVector(self.tecplot_core.stackcur_z, self.tecplot_core.stackcur_r,
                                               color='#ff6600'))
        except (TypeError, ValueError):
            tecplotlist_stackcur_plotline = []

        plt.xlabel("Z [mm]")
        plt.ylabel("Radius [mm]")

        # The main reason that the lines for the blades is stored separately from the streamlines is that they
        # are not going to pass through same modifications. E.g. it is set that the blade lines will not be dashed
        # in "neutral mode" as the stream lines.
        tecplotlist_blade_plotlines = hubline + shroudline + trailingline + leadingline

        return tecplotlist_blade_plotlines, tecplotlist_stream_plotlines, tecplotlist_stackcur_plotline, vectors_plotlines, points_list

    def tecplotDisplay_2(self):
        """
        Methods that are going to be called by the the TecplotWidget.

        @return [list] List of lists of blade profiles plotlines and list of lists of Mean Lines plotlines


        """

        tecplotlist_profile_plotlines = []
        tecplotlist_mean_plotlines = []
        tecplotlist_stackpnts_plotline = []
        tecplotlist_profile_vectors_plotline = []


        blade_number = self.tecplot_core.n_blades

        stackline = plt.plot(self.tecplot_core.stackcur_mp,
                             np.asarray(self.tecplot_core.stackcur_th).astype(np.float) + 2 * pi / blade_number * 0,
                             color='#ff6600',
                             marker='o',
                             linestyle='None',
                             label='Blade {j}: _Stackcur'.format(j=0))

        tecplotlist_stackpnts_plotline.append(stackline[0])

        # Reference lenght is the size of the
        self._ref_length = (self._computeLength(self.tecplot_core.bladeprofile_mp_list[(len(self.tecplot_core.bladeprofile_mp_list)//2)],
                                                self.tecplot_core.bladeprofile_th_list[(len(self.tecplot_core.bladeprofile_th_list)//2)]))

        for j in range(0, blade_number):

            m = 0

            for n in range(0, len(self.tecplot_core.bladeprofile_mp_list)):

                profileline = plt.plot(self.tecplot_core.bladeprofile_mp_list[n],
                                       np.asarray(self.tecplot_core.bladeprofile_th_list[n]).astype(np.float)
                                       + (2 * pi / blade_number * j),
                                       color=tecplot_colors[m],
                                       label='Blade {j}: Bladeprofile {i}'.format(i=n, j=j))



                meanline = plt.plot(self.tecplot_core.meanline_mp_list[n],
                                    np.asarray(self.tecplot_core.meanline_th_list[n]).astype(np.float)
                                    + (2 * pi / blade_number * j),
                                    color=tecplot_colors[m % len(tecplot_colors)],
                                    label='Blade {j}: Meanline {i} '.format(i=n, j=j))

                if j != 0:
                    for line in (profileline[0], meanline[0]):
                        line.set_visible(False)
                else:
                    tecplotlist_profile_vectors_plotline.append(
                        self._getVector(self.tecplot_core.bladeprofile_mp_list[n],
                                        self.tecplot_core.bladeprofile_th_list[n],
                                        color=tecplot_colors[m % len(tecplot_colors)], pos=1.2))

                    tecplotlist_profile_vectors_plotline.append(
                        self._getVector(self.tecplot_core.bladeprofile_mp_list[n],
                                        self.tecplot_core.bladeprofile_th_list[n],
                                        color=tecplot_colors[m % len(tecplot_colors)], pos=6))

                tecplotlist_profile_plotlines.append(profileline[0])
                tecplotlist_mean_plotlines.append(meanline[0])

                m += 1

        self.tighten()
        plt.xlabel("MP [-]")
        plt.ylabel("Theta [rad]")

        return tecplotlist_profile_plotlines, tecplotlist_mean_plotlines, tecplotlist_stackpnts_plotline,\
               tecplotlist_profile_vectors_plotline

    def tecplotDisplay_3(self):
        """
        Methods that are going to be called by the the TecplotWidget.

        @return [list] List of lists of thickness plotlines

        """

        m = 0
        tecplotlist_thickness_plotlines = []

        try:
            normalize = self.op_viewer.preferences_widget.default_tecplot_2d_normalize_thickness_check_state
        except AttributeError:
            normalize = True

        try:
            for n in range(0, len(self.tecplot_core.thickness_s_list)):
                if normalize:
                    self.tecplot_core.thickness_s_list[n] = np.asarray(self.tecplot_core.thickness_s_list[n]).astype(
                        np.float)
                    meanline_coordinate = self.tecplot_core.thickness_s_list[n] / self.tecplot_core.thickness_s_list[
                        n].max()
                    x_label = "Relative meanline length [-]"
                else:
                    meanline_coordinate = self.tecplot_core.thickness_s_list[n]

                    x_label = "Meanline length [mm]"

                thicknessline = plt.plot(meanline_coordinate, self.tecplot_core.thickness_t_list[n],
                                         color=tecplot_colors[m % len(tecplot_colors)],
                                         label='Thickness {i}'.format(i=n))

                tecplotlist_thickness_plotlines.append(thicknessline[0])

                m += 1
        except ValueError:
            return []

        plt.xlabel(x_label)
        plt.ylabel("Thickness [mm]")

        return tecplotlist_thickness_plotlines

    def tecplotDisplay_4(self):
        """
        Methods that are going to be called by the the TecplotWidget.

        @return [list] List of lists of thickness plotlines

        """

        m = 0
        tecplotlist_meanbeta_plotlines = []

        try:
            normalize = self.op_viewer.preferences_widget.default_tecplot_2d_normalize_beta_check_state
        except AttributeError:
            normalize = True

        # Exception is case list is empty to not crash "all" built-in function

        for n in range(0, len(self.tecplot_core.meanline_beta_list)):
            if normalize:
                self.tecplot_core.meanline_m_list[n] = np.asarray(self.tecplot_core.meanline_m_list[n]).astype(np.float)
                m_coord_le = self.tecplot_core.meanline_m_list[n].min()
                m_coord_te = self.tecplot_core.meanline_m_list[n].max()

                m_coordinate = (self.tecplot_core.meanline_m_list[n] - m_coord_le) / (m_coord_te - m_coord_le)
                x_label = "Meridional coordinate  norm. [-]"
            else:
                m_coordinate = self.tecplot_core.meanline_m_list[n]
                x_label = "Meridional coordinate [mm]"

            # TODO: weak condition to verify meanline_s

            # if "S" coordinate is empty or only zeros, plot MP x Beta.
            meanbetaline = plt.plot(m_coordinate, self.tecplot_core.meanline_beta_list[n],
                                    color=tecplot_colors[m % len(tecplot_colors)],
                                    label='Meanline {i}'.format(i=n))
            tecplotlist_meanbeta_plotlines.append(meanbetaline[0])

            m += 1

        plt.xlabel(x_label)
        plt.ylabel("Beta [deg]")

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

                for n in range(0, len(self.op_viewer.case_node.tecplotLists)):
                    # m is a variable for cycling through tecplot_colors
                    for index, line in enumerate(self.op_viewer.case_node.tecplotLists[n]):
                        line.set_color(self.op_viewer.case_node.tecplotSavedColorList[n][index])

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
                for n in range(0, len(self.op_viewer.case_node.tecplotLists)):

                    for line in self.op_viewer.case_node.tecplotLists[n]:
                        try:
                            temp_line_list_color.append(line.get_color())
                        except AttributeError: # Case for fancy arrows
                            temp_line_list_color.append(line.get_facecolor())

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
        except Exception as e:
            print(e)
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

                enabled = False




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

                enabled = True

                self.op_viewer.case_node.tecplotVisibility = "visible"

                self.op_viewer.model.dataChanged.emit(self.op_viewer.ui_case_treeview.currentIndex(),
                                                      self.op_viewer.ui_case_treeview.indexBelow(
                                                          self.op_viewer.ui_case_treeview.currentIndex()))

            self.canvas(1).draw()
            self.canvas(2).draw()
            self.op_viewer.ui_tecplot_setneutral_btn.setEnabled(enabled)
            self.op_viewer.ui_tecplot_toggle_bladeprofiles_btn.setEnabled(enabled)
            self.op_viewer.ui_tecplot_toggle_meanlines_btn.setEnabled(enabled)
            self.op_viewer.ui_tecplot_toggle_streamlines_chk.setEnabled(enabled)
            self.op_viewer.ui_tecplot_toggle_stackcurves_btn.setEnabled(enabled)
            self.op_viewer.ui_tecplot_toggle_direction_vectors_chk.setEnabled(enabled)
            self.op_viewer.ui_data_points_chk.setEnabled(enabled and self.op_viewer.case_node.ownPoints)


            if self.op_viewer.case_node.ownPoints:
                self.op_viewer.ui_data_points_chk.setEnabled(enabled)
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

        blade_number = self.op_viewer.case_node.numberBlades
        blade_mode = self.op_viewer.case_node.bladeMode

        try:
            # if it is visible, turns to invisible and vice-versa
            if self.op_viewer.case_node.tecplotMeanLinesIsVisible:
                # it must save the style list to recover it for re-displaying in way before making it invisbile.
                temp_line_list = []
                to_save_style_list = []

                for line in self.op_viewer.case_node.tecplotLists[4]:
                    temp_line_list.append(line.get_visible())
                    line.set_visible(False)

                to_save_style_list.extend(temp_line_list)

                self.op_viewer.case_node.tecplotMeanLinesSavedStyleList = to_save_style_list

                self.op_viewer.case_node.tecplotMeanLinesVisibility = "invisible"

            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.

                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[4]):
                    if blade_mode == "all":
                        line.set_visible(self.op_viewer.case_node.tecplotMeanLinesSavedStyleList[index % blade_number])

                    if blade_mode == "passage":
                        if index / int(len(self.op_viewer.case_node.tecplotLists[4]) / blade_number) < 2:
                            line.set_visible(
                                self.op_viewer.case_node.tecplotMeanLinesSavedStyleList[index % blade_number])

                    if blade_mode == "single":
                        if index / int(len(self.op_viewer.case_node.tecplotLists[4]) / blade_number) < 1:
                            line.set_visible(
                                self.op_viewer.case_node.tecplotMeanLinesSavedStyleList[index % blade_number])

                self.op_viewer.case_node.tecplotMeanLinesVisibility = "visible"

            self.canvas(1).draw()
            self.canvas(2).draw()

        except AttributeError:
            pass

    def viewBlades(self, mode):
        """

        :param mode:
        :return:
        """
        # TODO: Docstring
        if self._exceptionCatch():
            return

        n_blades = self.op_viewer.case_node.numberBlades

        if mode == "all":
            k = 0
            for i in range(int(len(self.op_viewer.case_node.tecplotLists[3]) / n_blades),
                           len(self.op_viewer.case_node.tecplotLists[3])):
                self.op_viewer.case_node.tecplotLists[3][i].set_visible(
                    self.op_viewer.case_node.tecplotLists[3][k % self.op_viewer.case_node.numberBlades].get_visible())

                self.op_viewer.case_node.tecplotLists[4][i].set_visible(
                    self.op_viewer.case_node.tecplotLists[4][k % self.op_viewer.case_node.numberBlades].get_visible())

            k += 1

        elif mode == "passage" and n_blades > 1:
            for i in range(2 * int(len(self.op_viewer.case_node.tecplotLists[3]) / n_blades),
                           len(self.op_viewer.case_node.tecplotLists[3])):
                self.op_viewer.case_node.tecplotLists[3][i].set_visible(False)
                self.op_viewer.case_node.tecplotLists[4][i].set_visible(False)

            k = 0
            for i in range(int(len(self.op_viewer.case_node.tecplotLists[3]) / n_blades),
                           2 * int(len(self.op_viewer.case_node.tecplotLists[3]) / n_blades)):
                self.op_viewer.case_node.tecplotLists[3][i].set_visible(
                    self.op_viewer.case_node.tecplotLists[3][k % self.op_viewer.case_node.numberBlades].get_visible())

                self.op_viewer.case_node.tecplotLists[4][i].set_visible(
                    self.op_viewer.case_node.tecplotLists[4][k % self.op_viewer.case_node.numberBlades].get_visible())

        elif mode == "single":
            for i in range(int(len(self.op_viewer.case_node.tecplotLists[3]) / n_blades),
                           len(self.op_viewer.case_node.tecplotLists[3])):
                self.op_viewer.case_node.tecplotLists[3][i].set_visible(False)
                self.op_viewer.case_node.tecplotLists[4][i].set_visible(False)

        self.op_viewer.case_node.bladeMode = mode
        self.op_viewer.tecplot_widget.tighten()

    def toggleBladeProfiles(self):
        """
        Toggles tecplot display to visible or invisible for the selected case mean lines.



        @return  None
        """
        # TODO: describe docstring
        # TODO: Comment
        # TODO: Prevent user from clicking before
        if self._exceptionCatch():
            return

        blade_number = self.op_viewer.case_node.numberBlades
        blade_mode = self.op_viewer.case_node.bladeMode

        try:
            if self.op_viewer.case_node.tecplotBladeProfilesIsVisible:
                # it must save the style list to recover it for re-displaying in way before making it invisbile.
                temp_line_list = []
                to_save_style_list = []

                for line in self.op_viewer.case_node.tecplotLists[3]:
                    temp_line_list.append(line.get_visible())
                    line.set_visible(False)

                to_save_style_list.extend(temp_line_list)

                self.op_viewer.case_node.tecplotBladeProfilesSavedStyleList = to_save_style_list

                self.op_viewer.case_node.tecplotBladeProfilesVisibility = "invisible"

            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.

                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[3]):
                    if blade_mode == "all":
                        line.set_visible(
                            self.op_viewer.case_node.tecplotBladeProfilesSavedStyleList[index % blade_number])

                    if blade_mode == "passage":
                        if index / int(len(self.op_viewer.case_node.tecplotLists[3]) / blade_number) < 2:
                            line.set_visible(
                                self.op_viewer.case_node.tecplotBladeProfilesSavedStyleList[index % blade_number])

                    if blade_mode == "single":
                        if index / int(len(self.op_viewer.case_node.tecplotLists[3]) / blade_number) < 1:
                            line.set_visible(
                                self.op_viewer.case_node.tecplotBladeProfilesSavedStyleList[index % blade_number])

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

                to_save_style_list.extend(temp_line_list)

                self.op_viewer.case_node.tecplotStreamLinesSavedStyleList = to_save_style_list

                self.op_viewer.case_node.tecplotStreamLinesVisibility = "invisible"

            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.

                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[2]):
                    line.set_visible(self.op_viewer.case_node.tecplotStreamLinesSavedStyleList[index])

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

                to_save_style_list.extend(temp_line_list)

                self.op_viewer.case_node.tecplotStackCurSavedStyleList = to_save_style_list

                self.op_viewer.case_node.tecplotStackCurVisibility = "invisible"

            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.
                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[1]):
                    line.set_visible(self.op_viewer.case_node.tecplotStackCurSavedStyleList[index])

                self.op_viewer.case_node.tecplotStackCurVisibility = "visible"

            self.canvas(1).draw()
            self.canvas(2).draw()
        except AttributeError:
            pass

    def toggleVectors(self):
        """
        Toggles vectors display to visible or invisible for the selected case Vectors.



        @return  None
        """
        if self._exceptionCatch():
            return

        # TODO: describe docstring
        # TODO: Comment
        # TODO: Prevent user from clicking before

        try:
            if self.op_viewer.case_node.tecplotVectorsIsVisible:
                # it must save the style list to recover it for re-displaying in way before making it invisbile.
                temp_line_list = []
                to_save_style_list = []

                for line in self.op_viewer.case_node.tecplotLists[6]:
                    temp_line_list.append(line.get_visible())
                    line.set_visible(False)

                to_save_style_list.extend(temp_line_list)

                self.op_viewer.case_node.tecplotVectorsSavedStyleList = to_save_style_list

                self.op_viewer.case_node.tecplotVectorsVisibility = "invisible"

            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.
                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[6]):
                    line.set_visible(self.op_viewer.case_node.tecplotVectorsSavedStyleList[index])

                self.op_viewer.case_node.tecplotVectorsVisibility = "visible"

            self.canvas(1).draw()
            self.canvas(2).draw()
        except Exception as e:
            print(e)
            pass

    def togglePoints(self):
        """
        Toggles points display to visible or invisible for the selected case points.



        @return  None
        """
        if self._exceptionCatch() or not self.op_viewer.case_node.ownPoints:
            return

        # TODO: describe docstring
        # TODO: Comment
        # TODO: Prevent user from clicking before

        try:
            if self.op_viewer.case_node.dataPointsIsVisible:
                # it must save the style list to recover it for re-displaying in way before making it invisbile.
                temp_line_list = []
                to_save_style_list = []
                for line in self.op_viewer.case_node.tecplotLists[7]:
                    temp_line_list.append(line.get_visible())
                    line.set_visible(False)

                to_save_style_list.extend(temp_line_list)

                self.op_viewer.case_node.dataPointsSavedStyleList = to_save_style_list

                self.op_viewer.case_node.dataPointsVisibility = "invisible"

            else:
                # Makes tecplot lines visible. Recovers the linestyle calling tecplotSavedStyleList method.
                for index, line in enumerate(self.op_viewer.case_node.tecplotLists[7]):
                    line.set_visible(self.op_viewer.case_node.dataPointsSavedStyleList[index])

                self.op_viewer.case_node.dataPointsVisibility = "visible"

            self.canvas(1).draw()
            self.canvas(2).draw()
        except Exception as e:
            print(e)
            pass

    def toggleGrid(self):
        """

        :return:
        """
        # TODO: Docstrings
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
            for axis in (self.ax1, self.ax2, self.ax3, self.ax4):
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
            for axis in (self.ax1, self.ax2, self.ax3, self.ax4):
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

        if number_of_cases == 0:
            # print("Action not feasible")
            return True

        if not self.op_viewer.case_node.ownPlot:
            # print("Action not feasible")
            return True

def main():
    app = QtGui.QApplication(sys.argv)
    tecplot_window = TecPlotWindow()

    tecplot_window.show()

    path_tec = os.path.join("./tecplot_sample/BLAN-056_mod.2d.tec.dat")
    path_ibl = os.path.join("./tecplot_sample/BLAN-056_mod.ibl")

    ibl_reader = IblReader()
    ibl_reader.readFile(path_ibl)


    tecplot_window.openTecplot(path_tec, ibl_reader)
    # MainWindow.setgui()


    #
    #
    # plt.figure(tecplot_window._figure1.number)
    # tecplot_window.ax1 = plt.subplot(211)
    #
    # plt.axis('equal')
    # plt.tight_layout()
    #
    # tecplot_window.ax1.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    # tecplot_window.ax1.set_xlabel(tecplot_window.ax1.get_xlabel(), fontsize=12, labelpad=0)
    # tecplot_window.ax1.set_ylabel(tecplot_window.ax1.get_ylabel(), fontsize=12, labelpad=5)
    #
    # plt.plot(ibl_reader.hub.z[0]/1.76,ibl_reader.hub.r[0]/1.76, "ko", linewidth="2", )
    # plt.plot(ibl_reader.tip.z[0]/1.76,ibl_reader.tip.r[0]/1.76, "ko", linewidth="2", )
    #
    # # m=0
    # for n in range(ibl_reader.surface.numberSubSections()):
    #
    #     color = tecplot_colors[m % len(tecplot_colors)]
    #     plt.plot(ibl_reader.surface.z[n],ibl_reader.surface.r[n], "o", linewidth="2", color=color)
    #     m += 1



    app.exec_()

    # inifile.close()
    print("End of Main Function UI")
    return tecplot_window


if __name__ == "__main__":
    main()
