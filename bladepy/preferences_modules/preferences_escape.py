from PyQt4 import QtCore

dct = {"true": True, "false": False, True: True, False: False}

last_settings = QtCore.QSettings("BladePy", "BladePy\MainApp\LastMainOptions".format(number=1))
user_settings = [QtCore.QSettings("BladePy", "BladePy\MainApp\Options{number}".format(number=1))]
list_settings = []
list_settings.append(last_settings)
list_settings.extend(user_settings)

print("Resetting preferences")
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

list_settings[1].beginGroup("shapes_settings")

list_settings[1].setValue("default_shape_color", to_be_default_shape_color)
list_settings[1].setValue("default_shape_quality", to_be_default_shape_factor)
list_settings[1].setValue("default_shape_transparency", to_be_default_shape_transparency)
list_settings[1].setValue("default_zoomfactor", to_be_default_zoom_step)
list_settings[1].setValue("default_transformation", [0, 0, 0, 0, 2])

list_settings[1].setValue("default_preload_blades_check_state", False)


list_settings[1].endGroup()

list_settings[1].beginGroup("outputs_settings")

list_settings[1].setValue("default_igs_surf_check_state", to_be_default_igs_surf_check_state)
list_settings[1].setValue("default_igs_surf_exception", to_be_default_igs_surf_exception)
list_settings[1].setValue("default_igs_3d_cur_check_state", to_be_default_igs_3d_cur_check_state)
list_settings[1].setValue("default_igs_3d_cur_exception", to_be_default_igs_3d_cur_exception)
list_settings[1].setValue("default_igs_2d_cur_check_state", to_be_default_igs_2d_cur_check_state)
list_settings[1].setValue("default_igs_2d_cur_exception", to_be_default_igs_2d_cur_exception)
list_settings[1].setValue("default_tecplot_check_state", to_be_default_tecplot_2d_check_state)

list_settings[1].endGroup()

list_settings[1].beginGroup("bladepro_settings")

list_settings[1].setValue("default_bladebro_version", to_be_default_bladebro_version)


list_settings[1].endGroup()