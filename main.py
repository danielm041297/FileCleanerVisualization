import os
import pathlib
import glob
import argparse
import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import math

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

                time_minimum = datetime.datetime(2017, 12, 15)

                if access_time < time_minimum:
                    continue

                fdata = FileData(access_time, mod_time, size)
                if file in self.files:
                    if access_time != self.files[file]:
                        self.files[file] = fdata
                else:
                    self.files[file] = fdata

    def showGraph(self):
        adates = [fil.access_time for fil in self.files.values()]
        sizes = [fil.file_size for fil in self.files.values()]
        if verbosity:
            print("Showing a scatter plot graph of your accessed files and sizes")
        sigmoid = lambda x: 1 / (1 + math.exp(-.0001 * x))

        sizesnp = np.asarray([sigmoid(x) for x in sizes])
        colors = np.random.rand(len(adates))
        scalingFactor = 80
        fracts = (sizesnp / max(sizesnp)) ** 2
        areas = np.pi * fracts * scalingFactor

        plt.scatter(adates, sizes, s=areas, c=colors, alpha=.5)
        plt.legend(scatterpoints=10)
        plt.grid(True)
        plt.xlabel('Dates')
        plt.ylabel('Sizes (bytes)')
        plt.title('Last Accessed Files & Sizes with extension ' + file_type)

        time_minimum = min(adates)
        time_maximum = max(adates)
        plt.xlim(time_minimum, time_maximum)

        plt.show()

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
if visualize:
    finder.showGraph()

#TODO: If any files get above 1 months old I should email myself reminding me to delete certain files. make a subprocess