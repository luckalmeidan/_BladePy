"""@package data_structure.case_node

File that contains the class CaseNode to structure all data loaded in BladePy.

"""

from PyQt4 import QtCore

from ..occ_modules.shape_control import rev_shape_colordictionary


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming
class CaseNode(object):
    """
    Class to structure all data loaded in Core.BladePyCore._addCase().

    This is the structure to be read by the model set to tree list view. The case node contains information of
    name of the case, handle of the AIS_ColoredShape, the name of the sub-shapes in the loaded igs and the graphics
    generate by TecplotReader Widget.
    The model used to represent a CaseNode is an case_model.CaseModel object.

    """

    def __init__(self, name, loaded_shapes=[[], [], [], [[], [], []]], plot_lists=None, parent=None):
        """
        The constructor of the class.

        A CaseNode object is created in Core.BladePyCore._addCase()

        @param name [str] Name of the case
        @param shape [Handle_AIS_InteractiveObject] Handles of AIS_ColoredShape for shape controlling
        @param plot_lists [list] List of lists of graphics generated by TecplotReader
        @param subshape_names [list] List of strings of sub-shapes names.
        @param parent [CaseNode] Is a CaseNode object itself. It is the parent of the node.

        """

        super(CaseNode, self).__init__()

        if parent is not None:
            self.subshape = []
            self._name = name
            self._tecplot_lists = plot_lists

            self._h_aisshape = loaded_shapes[0]  # List with all entities
            self._blade_h_aisshape = loaded_shapes[1]  # List with blade entities
            self._h_copied_blades = loaded_shapes[2]

            self._subshape_names = loaded_shapes[3]

            self._bladepro_version = loaded_shapes[4][0]
            self._created_date = loaded_shapes[4][1]
            self._n_blades = loaded_shapes[4][2]

            self._parent = parent

            # loading the default preferences_modules.
            list_settings = []

            last_settings = QtCore.QSettings("BladePy", "BladePy\MainApp\LastMainOptions".format(number=1))
            user_settings = [QtCore.QSettings("BladePy", "BladePy\MainApp\Options{number}".format(number=1))]

            list_settings.append(last_settings)
            list_settings.extend(user_settings)

            # TODO: Exception in case the user loaded only case with only tecplot file
            try:
                try:
                    node_shape_color = rev_shape_colordictionary[self.shapeHAIS[0].GetObject().Color()]
                except KeyError:
                    node_shape_color = "Custom"

                node_shape_transparency = int(self.shapeHAIS[0].GetObject().Transparency() * 100)
                node_shape_quality = 0.001 / self.shapeHAIS[0].GetObject().OwnDeviationCoefficient()[1]

            except IndexError:
                node_shape_color = "Custom"
                node_shape_transparency = 0
                node_shape_quality = 0

            self.shapeTransparency = node_shape_transparency
            self.shapeColor = node_shape_color
            self.shapeQuality = node_shape_quality
            # TODO: Explain below

            list_settings[1].beginGroup("shapes_settings")

            self._transformation = list_settings[1].value("default_transformation")

            for h_shape in self._h_aisshape:
                self.subshape.append([(list_settings[1].value("default_transformation"))])

            list_settings[1].endGroup()

            # if list not empty, tecplot mode is standard

            if self._tecplot_lists:
                self.tecplotMode = "standard"
            else:
                self.tecplotMode = "None"

            self.tecplotVisibility = "visible"
            self.tecplotMeanLinesVisibility = "visible"
            self.tecplotBladeProfilesVisibility = "visible"
            self.tecplotStackCurVisibility = "visible"
            self.tecplotStreamLinesVisibility = "visible"

            self.tecplotSavedStyleList = ([])
            self.tecplotBladeProfilesSavedStyleList = ([])
            self.tecplotMeanLinesSavedStyleList = ([])
            self.tecplotStackCurSavedStyleList = ([])

            parent.addChild(self)

        self._children = []

    # Below is defining the methods for getting and setting protected members of the class.
    @property
    def bladeProVersion(self):
        """

        :return:
        """
        # TODO: Docstrings
        return self._bladepro_version

    @property
    def creationDate(self):
        """

        :return:
        """
        # TODO: Docstrings
        return self._created_date

    @property
    def shapeNames(self):
        """

        :return:
        """
        # TODO: Docstrings
        return self._subshape_names

    @property
    def numberBlades(self):
        """

        :return:
        """
        # TODO: Docstrings
        return self._n_blades

    @property
    def ownShape(self):
        """

        :return:
        """
        # TODO: Docstrings
        if self.shapeHAIS:
            return True
        else:
            return False

    @property
    def ownPlot(self):
        """

        :return:
        """
        # TODO: Docstrings
        if self.tecplotLists:
            return True
        else:
            return False

    @property
    def shapeHAIS(self):
        """
        Method for retrieving the handle of AIS_ColoredShape for the node
        
        @return [Handle_AIS_InteractiveObject] The AIS_ColoredShape Handle.
        """
        return self._h_aisshape

    @property
    def bladeHAIS(self):
        """
        Method for retrieving the handle of blade AIS_ColoredShape for the node

        @return [Handle_AIS_InteractiveObject] The AIS_ColoredShape Handle.
        """
        return self._blade_h_aisshape

    @property
    def copiedBladesHAIS(self):
        """
        Method for retrieving the handle of created blades AIS_ColoredShape for the node

        @return [Handle_AIS_InteractiveObject] The AIS_ColoredShape Handle.
        """
        return self._h_copied_blades

    @property
    def shapeTransformation(self):
        """
        Method for getting the transformation for the shape of this case

        @return [list] The list of coordinates.
        """
        return self._transformation

    @shapeTransformation.setter
    def shapeTransformation(self, transformation_coord):
        """
        Method for setting the transformation for the shape of this case

        @param transformation [int] The value of transformation
        @param coord [int] Coordinate of transformation application. Indexes: [x:0, y:1, z:2, axis:3, theta:4]

        @return None
        """
        transformation = transformation_coord[0]
        coord = transformation_coord[1]
        self._transformation[coord] = transformation

    @property
    def shapeTransparency(self):
        """
        Method for getting the transparency for the shape of this case

        @return [float] The transparency
        """
        return self._transparency

    @shapeTransparency.setter
    def shapeTransparency(self, transparency):
        """
        Method for setting the transparency for the shape of this case

        @param transparency [float] The value of transparency
        @return None
        """
        self._transparency = transparency

    @property
    def shapeColor(self):
        """
        Method for getting the color for the shape of this case

        @return [int] The index of the color list of occ_modules.shapeproperties.shape_colorlist
        """
        return self._color

    @shapeColor.setter
    def shapeColor(self, color):
        """
        Method for setting the color for the shape of this case

        @param color [int] The index of the color list of occ_modules.shapeproperties.shape_colorlist
        @return None
        """
        self._color = color

    @property
    def shapeQuality(self):
        """
        Method for getting the quality for the shape of this case

        @return [float] The quality of the shape of this case
        """
        return self._quality

    @shapeQuality.setter
    def shapeQuality(self, quality):
        """
        Method for setting the quality for the shape of this case

        @param quality [float] The quality of the shape of this case
        @return None
        """
        self._quality = quality

    @property
    def tecplotLists(self):
        """
        Method for getting the tecplot graphics of this case

        @return [list] List of tecplots lines
        """
        return self._tecplot_lists

    @property
    def tecplotSavedStyleList(self):
        """
        Method for getting the saved tecplot graphics line-styles of this case.

        This is useful for retrieving the last line-style when manipulating with Core.tecplot_setNeutral(),
        Core.tecplot_setVisibility(). The program must remember it when toggling the options to save user's preference.

        @return [list] List of tecplots lines
        """
        return self._tecplot_savedstyle_list

    @property
    def tecplotSavedColorList(self):
        """
        Method for getting the saved tecplot graphics line-color of this case.

        @return [list] List of tecplots lines
        """
        return self._tecplot_savedcolor_list

    @property
    def tecplotMeanLinesSavedStyleList(self):
        """
        Method for getting the saved tecplot graphics line-styles of this case.

        This is useful for retrieving the last line-style when manipulating with Core.tecplot_setNeutral(),
        Core.tecplot_setVisibility(). The program must remember it when toggling the options to save user's preference.

        @return [list] List of tecplots lines
        """
        return self._tecplot_meanline_savedstyle_list

    @property
    def tecplotBladeProfilesSavedStyleList(self):
        """
        Method for getting the saved tecplot graphics line-styles of this case.

        This is useful for retrieving the last line-style when manipulating with Core.tecplot_setNeutral(),
        Core.tecplot_setVisibility(). The program must remember it when toggling the options to save user's preference.

        @return [list] List of tecplots lines
        """
        return self._tecplot_bladeprofile_savedstyle_list

    @property
    def tecplotStackCurSavedStyleList(self):
        """
        Method for getting the saved tecplot graphics line-styles of this case.

        This is useful for retrieving the last line-style when manipulating with Core.tecplot_setNeutral(),
        Core.tecplot_setVisibility(). The program must remember it when toggling the options to save user's preference.

        @return [list] List of tecplots lines
        """
        return self._tecplot_stackcur_savedstyle_list

    @property
    def tecplotStreamLinesSavedStyleList(self):
        """
        Method for getting the saved tecplot graphics line-styles of this case.

        This is useful for retrieving the last line-style when manipulating with Core.tecplot_setNeutral(),
        Core.tecplot_setVisibility(). The program must remember it when toggling the options to save user's preference.

        @return [list] List of tecplots lines
        """
        return self._tecplot_streamline_savedstyle_list

    @tecplotSavedStyleList.setter
    def tecplotSavedStyleList(self, tecplot_list):
        """
        Method for setting the saved tecplot graphics line-styles of this case.

        See datastructure.case_node.tecplotSavedStyleList()

        @param tecplot_list [list] List of tecplot graphics line-styles to save
        @return None
        """
        self._tecplot_savedstyle_list = tecplot_list

    @tecplotSavedColorList.setter
    def tecplotSavedColorList(self, teplot_list):
        """
        Method for getting the saved tecplot graphics line-color of this case.

        @return [list] List of tecplots lines
        """
        self._tecplot_savedcolor_list = teplot_list

    @tecplotMeanLinesSavedStyleList.setter
    def tecplotMeanLinesSavedStyleList(self, tecplot_list):
        """
        Method for setting the saved tecplot graphics line-styles of MeanLines of this case.

        See datastructure.case_node.tecplotSavedStyleList()

        @param tecplot_list [list] List of tecplot graphics line-styles to save
        @return None
        """
        self._tecplot_meanline_savedstyle_list = tecplot_list

    @tecplotBladeProfilesSavedStyleList.setter
    def tecplotBladeProfilesSavedStyleList(self, tecplot_list):
        """
        Method for setting the saved tecplot graphics line-styles of MeanLines of this case.

        See datastructure.case_node.tecplotSavedStyleList()

        @param tecplot_list [list] List of tecplot graphics line-styles to save
        @return None
        """
        self._tecplot_bladeprofile_savedstyle_list = tecplot_list

    @tecplotStackCurSavedStyleList.setter
    def tecplotStackCurSavedStyleList(self, tecplot_list):
        """
        Method for setting the saved tecplot graphics line-styles of MeanLines of this case.

        See datastructure.case_node.tecplotSavedStyleList()

        @param tecplot_list [list] List of tecplot graphics line-styles to save
        @return None
        """
        self._tecplot_stackcur_savedstyle_list = tecplot_list

    @tecplotStreamLinesSavedStyleList.setter
    def tecplotStreamLinesSavedStyleList(self, tecplot_list):
        """
        Method for setting the saved tecplot graphics line-styles of MeanLines of this case.

        See datastructure.case_node.tecplotSavedStyleList()

        @param tecplot_list [list] List of tecplot graphics line-styles to save
        @return None
        """
        self._tecplot_streamline_savedstyle_list = tecplot_list

    @property
    def tecplotVisibility(self):
        """
        Method for getting the current state of visibility the tecplot graphics for this case

        @return [str] The state of the tecplot. Can be "visible" or "invisible"
        """
        return self._tecplot_visibility

    @property
    def tecplotBladeProfilesVisibility(self):
        """
        Method for getting the current state of visibility the tecplot graphics for this case

        @return [str] The state of the tecplot. Can be "visible" or "invisible"
        """
        return self._tecplot_bladeprofile_visibility

    @property
    def tecplotMeanLinesVisibility(self):
        """
        Method for getting the current state of visibility the tecplot graphics for this case

        @return [str] The state of the tecplot. Can be "visible" or "invisible"
        """
        return self._tecplot_meanline_visibility

    @property
    def tecplotStackCurVisibility(self):
        """
        Method for getting the current state of visibility the tecplot graphics for this case

        @return [str] The state of the tecplot. Can be "visible" or "invisible"
        """
        return self._tecplot_stackcur_visibility

    @property
    def tecplotStreamLinesVisibility(self):
        """
        Method for getting the current state of visibility the tecplot graphics for this case

        @return [str] The state of the tecplot. Can be "visible" or "invisible"
        """
        return self._tecplot_streamline_visibility

    @tecplotVisibility.setter
    def tecplotVisibility(self, visibility):
        """
        Method for setting a state for the tecplot graphics for this case

        @param visibility [str] The visibility for this case. Can be "visible" or "invisible"
        @return None
        """
        self._tecplot_visibility = visibility

    @tecplotBladeProfilesVisibility.setter
    def tecplotBladeProfilesVisibility(self, visibility):
        """
        Method for setting a state for the tecplot graphics for this case

        @param visibility [str] The visibility for this case. Can be "visible" or "invisible"
        @return None
        """
        self._tecplot_bladeprofile_visibility = visibility

    @tecplotMeanLinesVisibility.setter
    def tecplotMeanLinesVisibility(self, visibility):
        """
        Method for setting a state for the tecplot graphics for this case

        @param visibility [str] The visibility for this case. Can be "visible" or "invisible"
        @return None
        """
        self._tecplot_meanline_visibility = visibility

    @tecplotStackCurVisibility.setter
    def tecplotStackCurVisibility(self, visibility):
        """
        Method for setting a state for the tecplot graphics for this case

        @param visibility [str] The visibility for this case. Can be "visible" or "invisible"
        @return None
        """
        self._tecplot_stackcur_visibility = visibility

    @tecplotStreamLinesVisibility.setter
    def tecplotStreamLinesVisibility(self, visibility):
        """
        Method for setting a state for the tecplot graphics for this case

        @param visibility [str] The visibility for this case. Can be "visible" or "invisible"
        @return None
        """
        self._tecplot_streamline_visibility = visibility

    @property
    def tecplotIsVisible(self):
        """
         Method for verifying if tecplot is visible

         @return [bool] True if it is "visible" False if it is "invisible"
         """
        if self.tecplotVisibility == "visible":
            return True
        else:
            return False

    @property
    def tecplotMeanLinesIsVisible(self):
        """
         Method for verifying if tecplot MeanLines is visible

         @return [bool] True if it is "visible" False if it is "invisible"
         """
        if self.tecplotMeanLinesVisibility == "visible":
            return True
        else:
            return False

    @property
    def tecplotBladeProfilesIsVisible(self):
        """
         Method for verifying if tecplot BladeProfiles is visible

         @return [bool] True if it is "visible" False if it is "invisible"
         """
        if self.tecplotBladeProfilesVisibility == "visible":
            return True
        else:
            return False

    @property
    def tecplotStackCurIsVisible(self):
        """
         Method for verifying if tecplot BladeProfiles is visible

         @return [bool] True if it is "visible" False if it is "invisible"
         """
        if self.tecplotStackCurVisibility == "visible":
            return True
        else:
            return False

    @property
    def tecplotStreamLinesIsVisible(self):
        """
         Method for verifying if tecplot BladeProfiles is visible

         @return [bool] True if it is "visible" False if it is "invisible"
         """
        if self.tecplotStreamLinesVisibility == "visible":
            return True
        else:
            return False

    @property
    def tecplotMode(self):
        """
        Method for getting the current state of mode the tecplot graphics for this case.

        The mode is whether all the lines in tecplot graphics are neutral - black - and dashed.

        @return [str] The state of mode of the tecplot. Can be "neutral" or "standard"
        """

        return self._tecplot_mode

    @tecplotMode.setter
    def tecplotMode(self, mode):
        """
        Method for setting the current state of mode the tecplot graphics for this case. 
        
        @param mode [str] The mode for this case. Can be "neutral" or "standard"
        @return None
        """
        self._tecplot_mode = mode

    @property
    def tecplotIsNeutral(self):
        """
         Method for verifying if tecplot is neutral

         @return [bool] True if it is "neutral" False if it is "standard"
         """
        if self.tecplotMode == "neutral":
            return True
        else:
            return False

    def addChild(self, child):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        self._children.append(child)

    def insertChild(self, position, child):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        if position < 0 or position > len(self._children):
            return False

        child = self._children.pop(position)
        child._parent = None

        return True

    def name(self):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        return self._name

    def setName(self, name):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        self._name = name

    def child(self, row):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        return self._children[row]

    @property
    def children(self):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        return self._children

    def childCount(self):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        return len(self._children)

    def parent(self):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        return self._parent

    def row(self):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        if self.parent() is not None:
            return self.parent().children.index(self)
