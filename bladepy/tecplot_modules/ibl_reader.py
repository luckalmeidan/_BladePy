import os
import csv as csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Section:
    def __init__(self, name):
        n = 15
        self.type = name

        if any(["All points" in name]):
            n = 1

        self.x = [np.array([]) for x in range(n)]
        self.y = [np.array([]) for x in range(n)]
        self.z = [np.array([]) for x in range(n)]

        self.r = [np.array([]) for x in range(n)]
        self.th = [np.array([]) for x in range(n)]

    def numberSubSections(self):
        return len(self.z)

    def __str__ (self):
        return self.type



class IblReader:
    def __init__(self):
        self.hub = Section("Hub")
        self.tip = Section("Tip")
        self.surface = Section("Surface")
        self.le_surface = Section("Leading Edge Surface")
        self.te_surface = Section("Trailing Edge Surface")

        self.all_points = Section("All points")


    def readFile(self, ibl_file):
        with open(ibl_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')

            index = 0

            current_reading = None
            previous_reading = None


            for row in reader:
                try:
                    if any(["Begin " in row[0],
                            "!end" in row[0],
                            "CORDINATES" in row[0],
                            "There are  4 blades" in row[0],
                            "Open Index Arclength" in row[0]]):

                        continue

                    if "HUB" in row[0]:
                        current_reading = self.hub

                        if current_reading is previous_reading:
                            index += 1
                        else:
                            index = 0

                    elif "TIP" in row[0]:
                        current_reading = self.tip

                        if current_reading is previous_reading:
                            index += 1
                        else:
                            index = 0


                    elif "LE-SURFACE" in row[0]:
                        current_reading = self.le_surface

                        if current_reading is previous_reading:
                            index += 1
                        else:
                            index = 0

                    elif "TE-SURFACE" in row[0]:
                        current_reading = self.te_surface

                        if current_reading is previous_reading:
                            index += 1
                        else:
                            index = 0

                    elif "SURFACE" in row[0]:
                        current_reading = self.surface

                        if current_reading is previous_reading:
                            index += 1
                        else:
                            index = 0

                    elif "!" in row[0] or "/*" in row[0]:
                        continue


                    else:
                        # if line is no breaker line, it will start appending the data to the last breaker read stored
                        # "current_reading"


                        if len(row) != 4 :
                            row = list(filter(None, row))
                            temp_row = []
                            for item in row:
                                temp_row.extend(item.split())

                            row = temp_row

                        r = np.array(row[1]).astype(float)
                        th =  np.array(row[2]).astype(float)
                        z =  np.array(row[3]).astype(float)

                        th_rad = np.deg2rad(th)

                        for set_object, set_index in zip([current_reading, self.all_points], [index, 0]):

                            set_object.r[set_index] = np.append(set_object.r[set_index], r)
                            set_object.th[set_index] = np.append(set_object.th[set_index], th)
                            set_object.z[set_index] = np.append(set_object.z[set_index], z)

                            set_object.x[set_index] = np.append(set_object.x[set_index], r * np.cos(th_rad))
                            set_object.y[set_index] = np.append(set_object.y[set_index], r * np.sin(th_rad))



                    previous_reading = current_reading


                except Exception as e:
                    print(row)
                    print(e)


            for section in [self.hub, self.tip, self.surface, self.le_surface, self.te_surface]:
                section.r = [item for item in section.r if len(item) != 0]
                section.z = [item for item in section.z if len(item) != 0]
                section.th = [item for item in section.th if len(item) != 0]
                section.x = [item for item in section.x if len(item) != 0]
                section.y = [item for item in section.y if len(item) != 0]






def main():
    path = os.path.join("./tecplot_sample/BLAN-056.ibl")
    ibl_reader = IblReader()
    ibl_reader.readFile(path)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #
    print(ibl_reader.all_points.x[0][1])

    ax.scatter(ibl_reader.all_points.x, ibl_reader.all_points.y, ibl_reader.all_points.z)

    plt.show()


if __name__ == "__main__":
    main()
