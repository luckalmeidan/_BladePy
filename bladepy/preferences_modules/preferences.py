"""
@package preferences_modules.preferences

File that contains the class PreferencesBladePy, for adding functions, for managing
user preferences, to the function-less Dialog Layout preferencesUI.Ui_PreferencesDialog


"""

import os

from bladepy.layout_creator import pyui_creator

ui_file = os.path.join(os.path.dirname(__file__), "preferencesUI.ui")
py_ui_file = os.path.join(os.path.dirname(__file__), "preferencesUI.py")

# Translate layout .ui file to .py file
pyui_creator.createPyUI(ui_file, py_ui_file)

from PyQt4 import QtCore, QtGui
from bladepy.occ_modules.shape_control import shape_colordictionaryhex, shape_colordictionary

from bladepy.preferences_modules import preferencesUI

dct = {"true": True, "false": False, True: True, False: False}


class PreferencesBladePy(QtGui.QDialog, preferencesUI.Ui_PreferencesDialog):
    """
    Class with the methods for customizing user preferences.

    """

    def __init__(self, parent=None, OutputViewerWidget=None):

        super(PreferencesBladePy, self).__init__(parent)
        self.setupUi(self)
        self.last_settings = QtCore.QSettings("BladePy", "BladePy\MainApp\LastMainOptions".format(number=1))
        self.user_settings = [QtCore.QSettings("BladePy", "BladePy\MainApp\Options{number}".format(number=1))]
        self.list_settings = []
        self.list_settings.append(self.last_settings)
        self.list_settings.extend(self.user_settings)
        self.first_default = True

        # sets a instace variable of the main object of Core
        self.op_viewer = OutputViewerWidget

        # Setup combobox
        for index, item_color in enumerate(list(shape_colordictionary.keys())):
            self.op_viewer.ui_shape_setcolor_combo.addItem(item_color)
            self.ui_preferences_default_color_combo.addItem(item_color)
            pixmap = QtGui.QPixmap(15, 15)
            pixmap.fill(shape_colordictionaryhex[item_color])
            icon = QtGui.QIcon(pixmap)
            self.op_viewer.ui_shape_setcolor_combo.setItemIcon(index, icon)
            self.ui_preferences_default_color_combo.setItemIcon(index, icon)

        # The try/except below is to prevent the program crashing when opening for the first time in a computer
        try:
            self.setProgramDefaults()

        except (TypeError, AttributeError, KeyError):
            # Set standard configuration if it is the first time
            print("Critical error found in preferences")

            while self.list_settings[1].group() is not "":
                self.list_settings[1].endGroup()

            self.saveSettings(1, restore=True)

            self.setProgramDefaults()

        finally:

            self.setInitialGUI()

        # TODO: Explain this section


        self.ui_preferences_ok_btn.clicked.connect(self.okAction)
        self.ui_preferences_cancel_btn.clicked.connect(self.cancelAction)
        self.ui_preferences_apply_btn.clicked.connect(self.applyAction)

    def setProgramDefaults(self):
        """

        :return:
        """
        # TODO: DOCSTRINGS

        self.list_settings[1].beginGroup("shapes_settings")

        self.default_shape_color = (self.list_settings[1].value("default_shape_color"))
        self.default_shape_factor = float(self.list_settings[1].value("default_shape_quality"))
        self.default_shape_transparency = int(self.list_settings[1].value("default_shape_transparency"))
        self.default_zoom_step = float(self.list_settings[1].value("default_zoomfactor"))
        self.op_viewer.canva.zoomfactor = float(self.list_settings[1].value("default_zoomfactor"))
        self.default_preload_blades_check_state = dct[self.list_settings[1].value("default_preload_blades_check_state")]

        self.list_settings[1].endGroup()

        self.list_settings[1].beginGroup("outputs_settings")

        self.default_igs_surf_check_state = dct[self.list_settings[1].value("default_igs_surf_check_state")]
        self.default_igs_surf_exception = self.list_settings[1].value("default_igs_surf_exception")
        self.default_igs_3d_cur_check_state = dct[self.list_settings[1].value("default_igs_3d_cur_check_state")]
        self.default_igs_3d_cur_exception = self.list_settings[1].value("default_igs_3d_cur_exception")
        self.default_igs_2d_cur_check_state = dct[self.list_settings[1].value("default_igs_2d_cur_check_state")]
        self.default_igs_2d_cur_exception = self.list_settings[1].value("default_igs_2d_cur_exception")
        self.default_tecplot_2d_check_state = dct[self.list_settings[1].value("default_tecplot_check_state")]

        self.list_settings[1].endGroup()

        self.list_settings[1].beginGroup("bladepro_settings")

        self.default_bladebro_version = self.list_settings[1].value("default_bladebro_version")

        self.list_settings[1].endGroup()

        return

    def setInitialGUI(self):
        """

        :return:
        """
        # TODO: Docstrings
        # TODO: I want to update this section in the future with better way to add new configurations.

        # it is necessary to update the preferences widgets with values set by user in previous sections.
        self.ui_preferences_zoom_dpsn.setValue(float(self.default_zoom_step))
        self.ui_preferences_default_color_combo.setCurrentIndex(
            list(shape_colordictionary.keys()).index(self.default_shape_color))
        self.ui_preferences_default_quality_dspn.setValue(self.default_shape_factor)
        self.ui_preferences_default_transparency_dspn.setValue(int(self.default_shape_transparency))
        self.ui_preferences_igs_preload_chk.setChecked(self.default_preload_blades_check_state)

        self.ui_preferences_igs_surf_chk.setChecked(self.default_igs_surf_check_state)
        self.ui_preferences_igs_surf_exception_edit.setText(self.default_igs_surf_exception)

        self.ui_preferences_igs_preload_chk.setChecked(self.default_preload_blades_check_state)

        self.ui_preferences_igs_3d_cur_chk.setChecked(self.default_igs_3d_cur_check_state)
        self.ui_preferences_igs_3d_cur_exception_edit.setText(self.default_igs_3d_cur_exception)

        self.ui_preferences_igs_2d_cur_chk.setChecked(self.default_igs_2d_cur_check_state)
        self.ui_preferences_igs_2d_cur_exception_edit.setText(self.default_igs_2d_cur_exception)

        self.ui_preferences_tecplot_2d_chk.setChecked(self.default_tecplot_2d_check_state)

        self.ui_preferences_running_bladepro_version_edit.setText(self.default_bladebro_version)

        # It is necessary also to update Main GUI preferences fields with the values set by user.
        self.op_viewer.ui_shape_setcolor_combo.setCurrentIndex(
            list(shape_colordictionary.keys()).index(self.default_shape_color))
        self.op_viewer.ui_shape_quality_dspn.setValue(self.default_shape_factor)
        self.op_viewer.ui_shape_transparency_sld.setValue(self.default_shape_transparency)
        self.op_viewer.ui_display_zoomfactor_dspn.setValue(self.default_zoom_step)

    def okAction(self):
        """
        Method for applying user preferences and closing the dialog.

        @return None
        """
        self.applyAction()

        self.close()

    def cancelAction(self):
        """
        Method simply for closing the dialog.

        @return None
        """
        self.close()

    def applyAction(self):
        """
        Method for applying user preferences but not closing the dialog.

        @return None
        """
        self.saveSettings(1)
        self.setProgramDefaults()

        # will only update fields in the output_viewer GUI in case the program just started.

    def saveSettings(self, setting, restore=False):
        """
        Method called by applyAction() that indeed sets the configurations.

        @param setting [int] always 1 for the moment. It support a number of different preferences_modules, but not yet
        implemented
        @return None
        """
        if not restore:
            # Get values from GUI to save.

            to_be_default_shape_color = self.ui_preferences_default_color_combo.currentText()
            to_be_default_shape_factor = self.ui_preferences_default_quality_dspn.value()
            to_be_default_shape_transparency = self.ui_preferences_default_transparency_dspn.value()
            to_be_default_zoom_step = self.ui_preferences_zoom_dpsn.value()

            to_be_default_preload_blades_check_state = self.ui_preferences_igs_preload_chk.isChecked()

            to_be_default_igs_surf_check_state = self.ui_preferences_igs_surf_chk.isChecked()
            to_be_default_igs_surf_exception = self.ui_preferences_igs_surf_exception_edit.text()

            to_be_default_igs_3d_cur_check_state = self.ui_preferences_igs_3d_cur_chk.isChecked()
            to_be_default_igs_3d_cur_exception = self.ui_preferences_igs_3d_cur_exception_edit.text()

            to_be_default_igs_2d_cur_check_state = self.ui_preferences_igs_2d_cur_chk.isChecked()
            to_be_default_igs_2d_cur_exception = self.ui_preferences_igs_2d_cur_exception_edit.text()

            to_be_default_tecplot_2d_check_state = self.ui_preferences_tecplot_2d_chk.isChecked()

            to_be_default_bladebro_version = self.ui_preferences_running_bladepro_version_edit.text()

        else:
            # below there is the "standard" values for preferences. This is standard values are set every time a user
            # starts the program for the first time. This can be necessary for recovering application
            to_be_default_shape_color = "Golden"
            to_be_default_shape_factor = 15
            to_be_default_shape_transparency = 0
            to_be_default_zoom_step = 1.2
            to_be_default_preload_blades_check_state = False

            to_be_default_igs_surf_check_state = True
            to_be_default_igs_surf_exception = 'HUB; SHROUD; STREAM'
            to_be_default_igs_3d_cur_check_state = True
            to_be_default_igs_3d_cur_exception = 'HUB; SHROUD'
            to_be_default_igs_2d_cur_check_state = False
            to_be_default_igs_2d_cur_exception = ''

            to_be_default_tecplot_2d_check_state = True

            to_be_default_bladebro_version = "bladepro"

        self.list_settings[setting].beginGroup("shapes_settings")

        self.list_settings[setting].setValue("default_shape_color", to_be_default_shape_color)
        self.list_settings[setting].setValue("default_shape_quality", to_be_default_shape_factor)

        self.list_settings[setting].setValue("default_shape_transparency", to_be_default_shape_transparency)
        self.list_settings[setting].setValue("default_zoomfactor", to_be_default_zoom_step)
        self.list_settings[setting].setValue("default_transformation", [0, 0, 0, 0, 2])
        self.list_settings[setting].setValue("default_preload_blades_check_state",
                                             to_be_default_preload_blades_check_state)

        self.list_settings[setting].endGroup()

        self.list_settings[setting].beginGroup("outputs_settings")

        self.list_settings[setting].setValue("default_igs_surf_check_state", to_be_default_igs_surf_check_state)
        self.list_settings[setting].setValue("default_igs_surf_exception", to_be_default_igs_surf_exception)
        self.list_settings[setting].setValue("default_igs_3d_cur_check_state", to_be_default_igs_3d_cur_check_state)
        self.list_settings[setting].setValue("default_igs_3d_cur_exception", to_be_default_igs_3d_cur_exception)
        self.list_settings[setting].setValue("default_igs_2d_cur_check_state", to_be_default_igs_2d_cur_check_state)
        self.list_settings[setting].setValue("default_igs_2d_cur_exception", to_be_default_igs_2d_cur_exception)
        self.list_settings[setting].setValue("default_tecplot_check_state", to_be_default_tecplot_2d_check_state)

        self.list_settings[setting].endGroup()

        self.list_settings[setting].beginGroup("bladepro_settings")

        self.list_settings[setting].setValue("default_bladebro_version", to_be_default_bladebro_version)

        self.list_settings[setting].endGroup()


        # quality_preferences = [[self.default_shape_factor, self.ui_preferences_default_quality_dspn,
        #                         self.op_viewer.ui_shape_quality_dspn, "dpsn", "shapes_settings", "default_shape_quality",
        #                         10]]
        #
        # igs_surf_preferences = [[self.default_igs_surf_check_state, self.ui_preferences_igs_surf_chk, None,
        #                          "chk", "outputs_settings", "default_igs_surf_check_state", True],
        #                         [self.default_igs_surf_exception, self.ui_preferences_igs_surf_exception_edit, None,
        #                          "edit", "outputs_settings", "default_igs_surf_exception", "SHROUD"]]
        #
        # igs_surf_preferences = [[self.ui_preferences_igs_surf_chk, None,
        #                          "chk", "outputs_settings", "default_igs_surf_check_state"],
        #                         [self.ui_preferences_igs_surf_exception_edit, None,
        #                          "edit", "outputs_settings", "default_igs_surf_exception"]]
        #
        # igs_surf_preload_blades = [[self.ui_preferences_igs_surf_chk, None,
        #                             "chk", "outputs_settings", "default_igs_surf_check_state"]]
        # Preferences Objects
