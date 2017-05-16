"""
@package tecplot_modules.tecplot_reader

File that contains the class TecPlotCore for reading tecplot outputs.

"""
import csv as csv
from pyparsing import Word, nums, alphanums, alphas
import matplotlib.pyplot as plt

# Set the color list to be used by the plotter. The user is free to customize it.

tecplot_colors = ['#800000', '#e60000', '#ff4d4d', '#006600', '#00b33c', '#33cc33', '#000099', '#3333ff', '#4d79ff',
                  '#990099', '#cc00cc', '#ff4dff']


class TecPlotCore(object):
    """
    Class for reading tecplot outputs.

    A object of this class will be in a composition association with a object of a
    tecplot_display.TecPlotWindow class.

    """

    def __init__(self):
        # Setups instance variables. PEP 8 requirement of instance variables to be defined in _init_
        self.hub_z = []
        self.hub_r = []

        self.shroud_z = []
        self.shroud_r = []

        self.trailing_z = []
        self.trailing_r = []

        self.leading_z = []
        self.leading_r = []

        self.stackcur_r = []
        self.stackcur_z = []
        self.stackcur_th = []
        self.stackcur_mp = []

        self.stream_z_list = []
        self.stream_r_list = []


        self.bladeprofile_mp_list = []
        self.bladeprofile_th_list = []

        self.meanline_s_list = []
        self.meanline_m_list = []
        self.meanline_mp_list = []
        self.meanline_th_list = []
        self.meanline_beta_list = []

        self.thickness_s_list = []
        self.thickness_t_list = []

        self.n_blades = 1

    def tecplotReader(self, read_csv):
        """
        Function to dig into a csv file and to record it to instance variables lists.

        @param read_csv [csv_file] The file where tecplot data is 
        @return None
        
        """

        col_dict = {"X": 0,
                    "Y": 1,
                    "Z": 2,
                    "R": 3,
                    "TH": 4,
                    "RTH": 5,
                    "M": 6,
                    "MP": 7,
                    "BETA": 8,
                    "S": 9,
                    "T": 10}

        stream_z = []
        stream_r = []

        bladeprofile_mp = []
        bladeprofile_th = []

        meanline_s = []
        meanline_mp = []
        meanline_m = []

        meanline_th = []
        meanline_beta = []

        thickness_t = []
        thickness_s = []

        try:
            with open(read_csv, 'r') as f:
                reader = csv.reader(f, delimiter='\t')

                current_reading = ""

                # Start iterating line by line in the file to be read, identifying the breakers first and appending
                # all sub sequent values to correspondent list of the breaker until a new break. If the new break is a
                # a sequence of blade profiles, mean lines, thickness or stream curves, it appends the previous
                # temporary list to a main list and clears the temporary. It is a list of lists.

                for row in reader:
                    try:
                        if "Number of blades" in row[0]:
                            blade_header_model = "# Number of blades:" + Word(nums)
                            self.n_blades = n_blades = int(blade_header_model.parseString(row[0])[1])

                        if "TITLE" in row[0]:
                            pass
                            continue

                        if "VARIABLES" in row[0]:
                            pass
                            continue

                        if "Hub" in row[0]:
                            current_reading = "Hub"

                        elif "Shroud" in row[0]:
                            current_reading = "Shroud"

                        elif "Trailing" in row[0]:
                            current_reading = "Trailing Edge"

                        elif "Leading" in row[0]:
                            current_reading = "Leading Edge"

                        elif "Stacking" in row[0]:
                            current_reading = "Stacking Curve"

                        elif "Streamcurve" in row[0]:
                            current_reading = "Stream Curves"
                            if stream_z:
                                self.stream_z_list.append(stream_z)
                                self.stream_r_list.append(stream_r)

                            # clears the current stream curve #?
                            stream_z = []
                            stream_r = []

                        elif "Bladeprofile" in row[0]:
                            current_reading = "Blade Profiles"

                            # This condition is to check in case the list to be appended is not empty. This is the case
                            # when the program identifies the first breaker for that section. The same is valid for
                            #  meanline and thickness
                            if bladeprofile_mp:
                                self.bladeprofile_mp_list.append(bladeprofile_mp)
                                self.bladeprofile_th_list.append(bladeprofile_th)

                            bladeprofile_mp = []
                            bladeprofile_th = []

                        elif "Meanline" in row[0]:
                            current_reading = "Mean Line"
                            if meanline_mp:
                                self.meanline_mp_list.append(meanline_mp)
                                self.meanline_m_list.append(meanline_m)
                                self.meanline_s_list.append(meanline_s)
                                self.meanline_th_list.append(meanline_th)
                                self.meanline_beta_list.append(meanline_beta)

                            meanline_mp = []
                            meanline_m = []
                            meanline_s = []
                            meanline_th = []
                            meanline_beta = []

                        elif "Thickness" in row[0]:
                            current_reading = "Thickness"
                            if thickness_s:
                                self.thickness_s_list.append(thickness_s)
                                self.thickness_t_list.append(thickness_t)

                            thickness_s = []
                            thickness_t = []

                        elif "ZONE" in row[0]:
                            # Not implemented ZONES will fall to this elif case
                            print("NOT IMPLEMENTED IN READER: %s" % row[0])
                            current_reading = "New Zone"

                        else:
                            # if line is no breaker line, it will start appending the data to the last breaker read stored
                            # "current_reading"
                            if current_reading == "Hub":
                                self.hub_z.append(row[col_dict["Z"]])
                                self.hub_r.append(row[col_dict["R"]])

                            if current_reading == "Shroud":
                                self.shroud_z.append(row[col_dict["Z"]])
                                self.shroud_r.append(row[col_dict["R"]])

                            if current_reading == "Stream Curves":
                                stream_z.append(row[col_dict["Z"]])
                                stream_r.append(row[col_dict["R"]])

                            if current_reading == "Leading Edge":
                                self.leading_z.append(row[col_dict["Z"]])
                                self.leading_r.append(row[col_dict["R"]])

                            if current_reading == "Trailing Edge":
                                self.trailing_z.append(row[col_dict["Z"]])
                                self.trailing_r.append(row[col_dict["R"]])

                            if current_reading == "Blade Profiles":
                                bladeprofile_mp.append(row[col_dict["MP"]])
                                bladeprofile_th.append(row[col_dict["TH"]])

                            if current_reading == "Mean Line":
                                # The try/except here is for the case that beta is not a parameter in the tecplot file,
                                # which is possible to exist
                                meanline_mp.append(row[col_dict["MP"]])
                                meanline_m.append(row[col_dict["M"]])
                                meanline_th.append(row[col_dict["TH"]])

                                try:
                                    meanline_beta.append(row[col_dict["BETA"]])
                                except IndexError:
                                    meanline_beta.append([])
                            if current_reading == "Thickness":
                                # print("Thickness Appending")
                                thickness_s.append(row[col_dict["S"]])
                                thickness_t.append(row[col_dict["T"]])

                            if current_reading == "Stacking Curve":
                                self.stackcur_r.append(float(row[col_dict["R"]]))
                                self.stackcur_z.append(float(row[col_dict["Z"]]))
                                self.stackcur_th.append(float(row[col_dict["TH"]]))
                                self.stackcur_mp.append(float(row[col_dict["MP"]]))

                            if current_reading == "New Zone":
                                pass
                    except IndexError:
                        pass

        except FileNotFoundError:
            pass
        # Finish appending temporary lists to their main list of lists. This is necessary to be done here because
        # it only appends the temporary list in case of a new same-type breaker. E.g. Stream Curvess #1, Stream Curvess #2.
        # The last last set of data will never find a new breaker to enter and execute the appending.


        self.bladeprofile_mp_list.append(bladeprofile_mp)
        self.bladeprofile_th_list.append(bladeprofile_th)

        self.stream_z_list.append(stream_z)
        self.stream_r_list.append(stream_r)

        self.meanline_s_list.append(meanline_s)
        self.meanline_mp_list.append(meanline_mp)
        self.meanline_m_list.append(meanline_m)
        self.meanline_th_list.append(meanline_th)
        self.meanline_beta_list.append(meanline_beta)

        self.thickness_s_list.append(thickness_s)
        self.thickness_t_list.append(thickness_t)

        # TODO: refactor this section. Not practical in any way


    #


# lines that are not meant to be executed outside running this file itself.
if __name__ == "__main__":
    pass


