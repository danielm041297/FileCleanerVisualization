import os
import pathlib
import glob
import argparse
import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
class FileData:
    def __init__(self, access_time, modify_time, file_size):
        self.access_time = access_time
        self.modify_time = modify_time
        self.file_size = file_size

class FileCleaner:
    def __init__(self, dir):
        self.files = dict()
        self.directory = dir
        if verbosity:
            print("Looking in directory: " + dir)

    def getSubDirectories(self):
        os.chdir(self.directory)
        dirs = [s for s in os.listdir(self.directory) if os.path.isdir(s)]
        dirs.insert(0, '')
        return dirs

    def getFiles(self):
        dirs = self.getSubDirectories()

        if verbosity:
            print("Searching subdirectories: " + str(dirs))

        path = os.getcwd()
        extension = '.py' if file_type is None else file_type

        if verbosity:
            print("Searching for file type with extension = " + extension)

        for dir in dirs:
            if dir is '': #search folder first before subfolders
                _files = glob.glob(path + '/' + '*' + extension)
            else:
                _files = glob.glob(path + '/' + dir + '/' + '*' + extension)
            #host a blog would be cool for this application
            for file in _files:

                statinfo = os.stat(file)
                access_time = datetime.datetime.fromtimestamp(round(statinfo.st_atime))
                mod_time = datetime.datetime.fromtimestamp(round(statinfo.st_mtime))
                size = statinfo.st_size
                print(size)
                fdata = FileData(access_time, mod_time, size)
                if file in self.files:
                    if access_time != self.files[file]:
                        self.files[file] = fdata
                else:
                    self.files[file] = fdata

    def showGraph(self):
        return



parser = argparse.ArgumentParser(description="Visualize file accesses to decide if you need to delete")
parser.add_argument("--verbosity", help="increase output verbosity")
parser.add_argument("--visualize", help = "Show matplot of python file accesses")
parser.add_argument("--directory", help = "The directory you want to access")
parser.add_argument("--file_type", help = "The file type extension you want to search for")

args = parser.parse_args()

if args.directory is None or not os.path.isdir(args.directory):
    parser.error("Must specify a valid directory path to check")

verbosity = args.verbosity
visualize = args.visualize
directory = args.directory
file_type = args.file_type

finder = FileCleaner(directory)
finder.getFiles()

# adates = []
# sizes = []
# for fil in finder.files.values():
#     adates.append(fil.access_time)
#     sizes.append(fil.file_size)
# plt.scatter(adates, sizes, marker="x", color="black", linewidths=1, label="Crosses")
# plt.legend(scatterpoints=1)
#
# plt.show()

#TODO: If any files get above 1 months old I should email myself reminding me to delete certain files. make a subprocess