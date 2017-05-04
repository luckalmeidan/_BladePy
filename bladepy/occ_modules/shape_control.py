"""@package occ_modules.shape_control

File that contains the class ShapeManager that is inherited by Core.BladePyCore for Shape Control purposes.

The class has a object compost in Core.BladePyCore. In this file the shape color definitions are also defined and
imported through the GUI for painting shapes and for painting the TreeView widget icons.

"""
import os
from collections import OrderedDict
from math import pi

import OCC.Quantity as OCC_Color
import pyparsing
from OCC.AIS import AIS_ColoredShape
from OCC.Graphic3d import Graphic3d_NOM_SATIN
from OCC.IGESCAFControl import IGESCAFControl_Reader
from OCC.TCollection import TCollection_ExtendedString
from OCC.TDF import TDF_LabelSequence
from OCC.TDataStd import TDataStd_Name_GetID, Handle_TDataStd_Name
from OCC.TDocStd import Handle_TDocStd_Document
from OCC.TopLoc import TopLoc_Location
from OCC.XCAFApp import _XCAFApp
from OCC.XCAFDoc import XCAFDoc_DocumentTool
from OCC.gp import gp_Trsf, gp_Pnt, gp_Ax1, gp_Dir, gp_Vec
from PyQt4 import QtGui
from pyparsing import Word, nums, alphanums, alphas

# set dictionaries for shape colors
shape_colordictionary = OrderedDict([("Blue", 422),
                                     ("Red", 415),
                                     ("Golden", 362),
                                     ("Black", 0),
                                     ("White", 3),
                                     ("Yellow", 257)])

rev_shape_colordictionary = {v: k for k, v in shape_colordictionary.items()}

rgb = tuple([172, 201, 227])
shape_colordictionary["Custom"] = OCC_Color.Quantity_Color(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255,
                                                           OCC_Color.Quantity_TOC_RGB)

# This shape colors are for the icons on tree view list
shape_colordictionaryhex = {"Black": QtGui.QColor(0, 0, 0),
                            "White": QtGui.QColor(255, 255, 255),
                            "Blue": QtGui.QColor(0, 0, 240),
                            "Golden": QtGui.QColor(230, 153, 0),
                            "Yellow": QtGui.QColor(255, 255, 0),
                            "Red": QtGui.QColor(255, 0, 0),
                            "Custom": QtGui.QColor(rgb[0], rgb[1], rgb[2])}


class ShapeManager(object):
    """
    This class is a group of methods related to shape properties control.

    All these methods are a linked to Core.BladePyCore by composition. Contains methods that manages the Shape
    appearance such transparency, quality, color. It also has a method capable of transforming the shape by displacing
    or rotating it.

    """

    def __init__(self, OutputViewerWidget):

        ## Object reference to main object
        self.op_viewer = OutputViewerWidget

    def loadShape(self, shape_list):
        """
        Method for loading one or more shapes and displaying to Output Viewer.

        This method uses libraries of iges caf control for fetching sub-shape names within .igs files. This method
        is used when adding a case in the main routine.

        @param shape_list [list] First index contains the path of shape, second index contains a list of display
        exceptions, e.g: [[igs_2d_shape_path, ["HUB", "SHROUD"], [igs_3d_shape_path, ["STREAM"]]
        @return First return contains list of AIS_ColoredShapes handles and second return contains a list of sub-shape names
        in strings
        """
        loaded_ais_shapes = []
        loaded_h_ais_shapes = []
        loaded_blade_h_ais_shapes = []
        loaded_stream_shroud_h_ais_shapes = []
        loaded_subshape_names = []
        h_copy_blades = []
        default_displaying_h_ais_shapes = []

        default_material = Graphic3d_NOM_SATIN
        pre_load_blades = self.op_viewer.preferences_widget.default_preload_blades_check_state

        n_blades = 1
        bladepro_version = "-"
        created_on_date = "-"

        for shape_case in shape_list:

            loaded_shape_filename = os.path.basename(shape_case[0])

            # Read number of blades from geometry file
            with open(shape_case[0]) as file:
                shape_header = [next(file) for iterator in range(3)]

            bladepro_line_in_file = shape_header[0]
            date_line_in_file = shape_header[1]
            n_blades_line_in_file = shape_header[2]

            # style of information in header to parse
            bladepro_header_model = "Created by" + Word(alphas) + Word(alphanums + "." + "-")
            date_header_model = "Created on" + Word(alphanums + "-")
            blade_header_model = "Number of blades:" + Word(nums)

            try:
                n_blades = int(blade_header_model.parseString(n_blades_line_in_file)[1])
                bladepro_version = " ".join(bladepro_header_model.parseString(bladepro_line_in_file)[1:])
                created_on_date = date_header_model.parseString(date_line_in_file)[1]
            except pyparsing.ParseException:
                print("Unable to fetch number of blades")

            if "cur" in loaded_shape_filename:
                type_of_loaded_shape = "Curve"
            else:
                type_of_loaded_shape = "Surface"

            exception_list = shape_case[1]
            exception_list = list(filter(None, exception_list))  # Mistake-prevention of user filling of exception list
            # creates a handle for TdocStd documents
            h_doc = Handle_TDocStd_Document()

            # create the application
            app = _XCAFApp.XCAFApp_Application_GetApplication().GetObject()
            app.NewDocument(TCollection_ExtendedString(""), h_doc)

            # get root assembly
            doc = h_doc.GetObject()
            h_shape_tool = XCAFDoc_DocumentTool().ShapeTool(doc.Main())

            # creates a reader responsible for reading an IGS file
            reader = IGESCAFControl_Reader()
            reader.ReadFile(shape_case[0])

            #  Translates currently loaded IGES file into the document
            reader.Transfer(doc.GetHandle())

            # labels for the shapes. Every IGS file contains a name for each individual shape
            labels = TDF_LabelSequence()

            shape_tool = h_shape_tool.GetObject()
            shape_tool.GetShapes(labels)

            # gets the number of individual shapes contained in the igs file
            nb = reader.NbShapes()

            # for each individual shape gets the label nad creates a AIS_ColoredShape for data contained in reader.Shape()
            for i in range(1, nb + 1):
                label = labels.Value(i)
                h_name = Handle_TDataStd_Name()
                label.FindAttribute(TDataStd_Name_GetID(), h_name)

                str_dump = h_name.GetObject().DumpToString()

                name_subshape = str_dump.split('|')[-2]

                string_to_remove_loc = name_subshape.rfind("(")

                name = "%s - %s" % (type_of_loaded_shape, name_subshape[:string_to_remove_loc])

                loaded_subshape_names.append(name)

                shape = AIS_ColoredShape(reader.Shape(i))
                shape.SetWidth(2)
                shape.SetMaterial(default_material)

                loaded_ais_shapes.append(shape)
                loaded_h_ais_shapes.append(shape.GetHandle())

                if not any(iterator in name_subshape for iterator in exception_list):
                    default_displaying_h_ais_shapes.append(shape.GetHandle())

                # TODO: COMMENTT THIS LINE
                if any(iterator in name_subshape for iterator in ['LE', 'TE', 'UPPER', 'LOWER', 'MEANLINE']):
                    loaded_blade_h_ais_shapes.append(shape.GetHandle())

                if any(iterator in name_subshape for iterator in ['SHROUD', 'STREAM']):
                    loaded_stream_shroud_h_ais_shapes.append(shape.GetHandle())

            # number of cases is a variable used to make the loaded shape color different from the previous one
            number_of_cases = self.op_viewer.model.rowCount(self.op_viewer.ui_case_treeview.rootIndex())

            loaded_shape_color = self.op_viewer.preferences_widget.default_shape_color

            # TODO: Explain color setting logic

            if self.op_viewer.root_node.childCount() != 0:
                used_colors = []
                for case in self.op_viewer.root_node._children:
                    used_colors.append(case.shapeColor())

                if loaded_shape_color in used_colors:
                    for color in list(shape_colordictionary.keys()):
                        if color not in used_colors:
                            loaded_shape_color = color
                            break

                else:
                    pass

            # sets the default attributes for ais shapes handles
            for ais_shape in loaded_ais_shapes:
                ais_shape.SetOwnDeviationCoefficient(self.op_viewer.DC /
                                                     self.op_viewer.preferences_widget.default_shape_factor)

                ais_shape.SetOwnHLRDeviationCoefficient(self.op_viewer.DC_HLR /
                                                        self.op_viewer.preferences_widget.default_shape_factor)
                ais_shape.SetColor(shape_colordictionary[loaded_shape_color])

                ais_shape.SetTransparency(self.op_viewer.preferences_widget.default_shape_transparency / 100)

            for h_ais_shape in loaded_stream_shroud_h_ais_shapes:
                ais_shape = h_ais_shape.GetObject()
                ais_shape.SetTransparency(.8)

        # displays the handles of the ais_shapes in the viewer3d context.

        if pre_load_blades:
            for j in range(1, n_blades):
                h_copy_blade = []
                for i in range(0, len(loaded_blade_h_ais_shapes)):
                    copy_blade = AIS_ColoredShape(loaded_blade_h_ais_shapes[i])
                    copy_blade.SetOwnDeviationCoefficient(
                        self.op_viewer.DC / self.op_viewer.preferences_widget.default_shape_factor)
                    h_copy_blade.append(copy_blade.GetHandle())

                self.specialSetTranslation(h_copy_blade, "Z", 0, 0, 0, 360 / n_blades * j)

                for i in range(0, len(h_copy_blade)):
                    self.op_viewer.display.Context.Display(h_copy_blade[i], False)

                h_copy_blades.extend(h_copy_blade)

            for h_ais_shape in h_copy_blades:
                self.op_viewer.display.Context.Erase(h_ais_shape, False)

        for handles_list in [default_displaying_h_ais_shapes]:
            for h_ais_shape in handles_list:
                self.op_viewer.display.Context.Display(h_ais_shape, False)

        return [loaded_h_ais_shapes,
                loaded_blade_h_ais_shapes,
                h_copy_blades,
                loaded_subshape_names,
                [bladepro_version, created_on_date, n_blades]]

    def setQuality(self):
        """
        Sets quality to the current working AIS Shape

        @return None

        """
        if self._exceptionCatch():
            return

        factor = self.op_viewer.ui_shape_quality_dspn.value()

        for i in range(0, len(self.op_viewer.current_h_ais_shape)):
            self.op_viewer.display.Context.SetDeviationCoefficient(self.op_viewer.current_h_ais_shape[i],
                                                                   self.op_viewer.DC / factor, False)
            self.op_viewer.display.Context.SetHLRDeviationCoefficient(self.op_viewer.current_h_ais_shape[i],
                                                                      self.op_viewer.DC_HLR / factor, False)

        if self.op_viewer.selectionMode == "surf":
            if self.op_viewer.ui_subcase_list.count() / 2 < len(self.op_viewer.ui_subcase_list.selectedIndexes()):
                self.op_viewer.case_node.setShapeQuality(factor)

        self.op_viewer.display.Repaint()

    def setTransparency(self):
        """
        Sets transparency to the current working AIS Shape

        @return None

        """

        if self._exceptionCatch():
            return

        transparency = self.op_viewer.ui_shape_transparency_sld.value()

        for i in range(0, len(self.op_viewer.current_h_ais_shape)):
            self.op_viewer.display.Context.SetTransparency(self.op_viewer.current_h_ais_shape[i], transparency / 100,
                                                           False)

        if self.op_viewer.selectionMode == "surf":
            # If the selected items is the majority of the list, then the property is set to the whole Case
            if self.op_viewer.ui_subcase_list.count() / 2 < len(self.op_viewer.ui_subcase_list.selectedIndexes()):
                self.op_viewer.case_node.setShapeTransparency(transparency / 100)

                # set the properties to to the selected shapes

        self.op_viewer.display.Repaint()

    def setColor(self):
        """
        Sets color to the current working AIS Shape

        @return None

        """
        if self._exceptionCatch():
            return

        current_color_combo = self.op_viewer.ui_shape_setcolor_combo.currentText()

        for i in range(0, len(self.op_viewer.current_h_ais_shape)):
            self.op_viewer.display.Context.SetColor(self.op_viewer.current_h_ais_shape[i],
                                                    shape_colordictionary[current_color_combo], False)

            self.op_viewer.model.dataChanged.emit(self.op_viewer.ui_case_treeview.currentIndex(),
                                                  self.op_viewer.ui_case_treeview.indexAbove(
                                                      self.op_viewer.ui_case_treeview.currentIndex()))

        if self.op_viewer.selectionMode == "surf":
            # If the selected items is the majority of the list, then the property is set to the whole Case
            if self.op_viewer.ui_subcase_list.count() / 2 < len(self.op_viewer.ui_subcase_list.selectedIndexes()):
                self.op_viewer.case_node.setShapeColor(current_color_combo)

        self.op_viewer.display.Repaint()

        return

    def setTranslation(self):
        """
        Creates an axis in x, y or z depending on user preference.

        gp_Ax1 describes an axis in 3D space. An axis is defined by a point (gp_Pnt) and a direction (gp_Dir) reference

        @return None

        """
        if self._exceptionCatch():
            return

        rotataxis_index_combo = self.op_viewer.ui_shape_rotataxis_combo.currentIndex()

        if self.op_viewer.ui_shape_rotataxis_combo.currentText() == "Z":
            ax1 = gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1))
        elif self.op_viewer.ui_shape_rotataxis_combo.currentText() == "Y":
            ax1 = gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 1, 0))
        elif self.op_viewer.ui_shape_rotataxis_combo.currentText() == "X":
            ax1 = gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(1, 0, 0))

        # Retrieve the displacements set by user

        x = float(self.op_viewer.ui_shape_xdispl_dspn.value())
        y = float(self.op_viewer.ui_shape_ydispl_dspn.value())
        z = float(self.op_viewer.ui_shape_zdispl_dspn.value())
        teta = float(self.op_viewer.ui_shape_tetarotat_dspn.value()) * pi / 180

        # creates objects of shape transformation (Returns the identity transformation),
        # one for axial and other for x, y, z coordinates
        transf_teta = gp_Trsf()
        transf_xyz = gp_Trsf()

        transf_teta.SetRotation(ax1, teta)

        transf_xyz.SetTranslation(gp_Vec(x, y, z))

        # Calculates the transformation matrix with respect of both transformations.
        transf_matrix = transf_xyz * transf_teta

        # Constructs an local coordinate system object. Note: A Location constructed from a default datum is said
        # to be "empty".
        # ref: https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_top_loc___location.html
        cube_toploc = TopLoc_Location(transf_matrix)

        # Then applies the local coordinate to the current shape
        for i in range(0, len(self.op_viewer.current_h_ais_shape)):
            self.op_viewer.display.Context.SetLocation(self.op_viewer.current_h_ais_shape[i], cube_toploc)

        if self.op_viewer.selectionMode == "surf":
            # If the selected items is the majority of the list, then the property is set to the whole Case
            if self.op_viewer.ui_subcase_list.count() / 2 < len(self.op_viewer.ui_subcase_list.selectedIndexes()):
                self.op_viewer.case_node.setShapeTransformation(x, 0)
                self.op_viewer.case_node.setShapeTransformation(y, 1)
                self.op_viewer.case_node.setShapeTransformation(z, 2)
                self.op_viewer.case_node.setShapeTransformation(teta / pi * 180, 3)
                self.op_viewer.case_node.setShapeTransformation(rotataxis_index_combo, 4)

            for i in range(0, len(self.op_viewer.ui_subcase_list.selectedIndexes())):
                index = self.op_viewer.ui_subcase_list.selectedIndexes()[i]
                self.op_viewer.case_node.subshape[index.row()][0] = [x, y, z, teta / pi * 180, rotataxis_index_combo]

        if self.op_viewer.selectionMode == "shape":
            for i in range(0, len(self.op_viewer.case_node.subshape)):
                self.op_viewer.case_node.subshape[i][0][0] = x
                self.op_viewer.case_node.subshape[i][0][1] = y
                self.op_viewer.case_node.subshape[i][0][2] = z
                self.op_viewer.case_node.subshape[i][0][3] = teta / pi * 180
                self.op_viewer.case_node.subshape[i][0][4] = rotataxis_index_combo

        self.op_viewer.display.Context.UpdateCurrentViewer()

        self.op_viewer.display.Repaint()

        return

    def hideShape(self):
        """
        Method for hiding selected shape.

        @return None
        """
        if self._exceptionCatch():
            return

        self.op_viewer.display.Context.EraseSelected()

    def displayShape(self):
        """
        Method for displaying selected shape.

        @return None
        """
        if self._exceptionCatch():
            return

        self.op_viewer.display.Context.DisplaySelected()
        self.op_viewer._surfaceChanged()

    def viewBlades(self, mode):
        """

        :param mode:
        :return:
        """

        # TODO: Docstrings
        if self._exceptionCatch():
            return

        n_blades = self.op_viewer.case_node._n_blades
        # TODO: (MED) COMMENT
        if not self.op_viewer.case_node.h_copied_blades:

            for j in range(1, n_blades):
                h_copy_blade = []
                for i in range(0, len(self.op_viewer.case_node._blade_h_aisshape)):
                    copy_blade = AIS_ColoredShape(self.op_viewer.case_node._blade_h_aisshape[i])
                    copy_blade.SetOwnDeviationCoefficient(
                        self.op_viewer.DC / self.op_viewer.preferences_widget.default_shape_factor)
                    h_copy_blade.append(copy_blade.GetHandle())

                self.specialSetTranslation(h_copy_blade, "Z", 0, 0, 0, 360 / n_blades * j)

                for i in range(0, len(h_copy_blade)):
                    self.op_viewer.display.Context.Display(h_copy_blade[i], False)

                self.op_viewer.case_node.h_copied_blades.extend(h_copy_blade)

        for h_ais_shape in self.op_viewer.case_node.h_copied_blades:
            self.op_viewer.display.Context.Erase(h_ais_shape, False)

        if mode == "all":
            for i in range(0, len(self.op_viewer.case_node.h_copied_blades)):
                self.op_viewer.display.Context.Display(self.op_viewer.case_node.h_copied_blades[i], False)

        elif mode == "passage" and n_blades > 1:
            for i in range(0, int(len(self.op_viewer.case_node.h_copied_blades) / (n_blades - 1))):
                self.op_viewer.display.Context.Display(self.op_viewer.case_node.h_copied_blades[i], False)

        if self.op_viewer.selectionMode == "shape":
            self.op_viewer.current_h_ais_shape.extend(self.op_viewer.case_node.h_copied_blades)

        # TODO: comment section
        # TODO: DOCSTRINGS
        # TODO: NO CASE EXCEPTION
        # TODO: PEP8

        self.op_viewer.display.Repaint()

        pass

    def review(self):
        pass

    def deactivateBlades(self):
        if self._exceptionCatch():
            return

        for h_ais_shape in self.op_viewer.case_node.h_copied_blades:
            self.op_viewer.display.Context.Erase(h_ais_shape, False)

        self.op_viewer.display.Repaint()
        # TODO: COMMENT
        # TODO: DOCSTRINGS

    def shapeDeletion(self, to_remove_shape, remove_copied=False, repaint=True):
        if self._exceptionCatch():
            return

        for i in range(0, len(to_remove_shape)):
            self.op_viewer.display.Context.Remove(to_remove_shape[i], False)

        if remove_copied:
            self.op_viewer.case_node.h_copied_blades = []

        # TODO: COMMENT
        # TODO: DOCSTRINGS

        if repaint:
            self.op_viewer.display.Repaint()

    def specialSetTranslation(self, h_ais_shapes, axis, x, y, z, teta):
        """
        Creates an axis in x, y or z depending on user preference.

        gp_Ax1 describes an axis in 3D space. An axis is defined by a point (gp_Pnt) and a direction (gp_Dir) reference

        @return None

        """

        if axis == "Z":
            ax1 = gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1))
        elif axis == "Y":
            ax1 = gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 1, 0))
        elif axis == "X":
            ax1 = gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(1, 0, 0))

        x = x
        y = y
        z = z

        teta = teta * pi / 180

        transf_teta = gp_Trsf()
        transf_xyz = gp_Trsf()

        transf_teta.SetRotation(ax1, teta)

        transf_xyz.SetTranslation(gp_Vec(x, y, z))

        transf_matrix = transf_xyz * transf_teta

        cube_toploc = TopLoc_Location(transf_matrix)

        for h_ais_shape in h_ais_shapes:
            self.op_viewer.display.Context.SetLocation(h_ais_shape, cube_toploc)

        return

    def _exceptionCatch(self):
        """
        This functions is a exception catcher: if user tries to wrongly set properties when there is nothing to be
        applied by them


        @return None
        """

        number_of_cases = self.op_viewer.model.rowCount(self.op_viewer.ui_case_treeview.rootIndex())
        if self.op_viewer.current_h_ais_shape is None or number_of_cases == 0:
            print("Action not feasible")
            return True
