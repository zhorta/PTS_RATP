# Code that converts GTFS files from the RATP_GTFS_FULL and RATP_GTFS_LINES folders to JSON
# so we can put them in a database

import json
import os

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

def pywalkerFull(path):
    for root, dirs, files in os.walk(path):
        folder = root.split("/")[-1]
        directoryWrite = "./" +"JSON Files Full"
        directoryRead = "./" + folder
        if not os.path.exists(directoryWrite):
                os.makedirs(directoryWrite)
        
        for file_ in files:
                
                fileName = file_.split(".")[0]
                if(fileName != ""):
                        print(fileName)
                        directoryRead = "./RATP_GTFS_FULL/" + "/" + fileName + ".txt"
                        inputFile = open(directoryRead, 'r')
                        firstLine = inputFile.readline()[:-1] #to remove the \n
                        titles = firstLine.split(",")
                        data = {}
                        data2 = {}
                        for line in inputFile:
                                currentLine = line.split(",")             
                                currentLine[len(currentLine)-1] = currentLine[len(currentLine)-1][:-1] #to remove the \n
                                data[k] = {}
                                for i in range(len(titles)):
                                      data[k][titles[i]] = currentLine[i]
                                k = k + 1
                                
                                      
                        inputFile.close()

                        writeToJSONFile(directoryWrite, fileName, data)

pywalkerFull('./RATP_GTFS_FULL')


def pywalkerLines(path):
    for root, dirs, files in os.walk(path):
        folder = root.split("/")[-1]
        directoryWrite = "./" +"JSON Files Lines" + '/' + folder + "_JSON"
        directoryRead = "./" + folder
        print(folder)
        if not os.path.exists(directoryWrite):
                os.makedirs(directoryWrite)
        
        for file_ in files:
                k = 0
                fileName = file_.split(".")[0] 
                if(fileName != ""):
                        directoryRead = "./RATP_GTFS_LINES/" + folder + "/" + fileName + ".txt"
                        
                        inputFile = open(directoryRead, 'r')
                        firstLine = inputFile.readline()[:-1] #to remove the \n
                        titles = firstLine.split(",")
                        data = {}
                        data2 = {}
                        for line in inputFile:
                                currentLine = line.split(",")             
                                currentLine[len(currentLine)-1] = currentLine[len(currentLine)-1][:-1] #to remove the \n
                                data[k] = {}
                                for i in range(len(titles)):
                                      data[k][titles[i]] = currentLine[i]
                                k = k + 1
                                
                                      
                        inputFile.close()
                              
                        writeToJSONFile(directoryWrite, fileName, data)

pywalkerLines('./RATP_GTFS_LINES')
