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
                                currentLine[len(currentLine)-1] = currentLine[len(currentLine)-1][:-1]
                                for i in range(len(titles)):
                                        data2[titles[i]] = currentLine[i]
                                        data[currentLine[0]] = data2
                        inputFile.close()      

                        writeToJSONFile(directoryWrite, fileName, data)

pywalkerFull('./RATP_GTFS_FULL')


def pywalkerLines(path):
    for root, dirs, files in os.walk(path):
        folder = root.split("/")[-1]
        directoryWrite = "./" +"JSON Files Lines" + '/' + folder + "_JSON"
        directoryRead = "./" + folder
        if not os.path.exists(directoryWrite):
                os.makedirs(directoryWrite)
        
        for file_ in files:
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
                                for i in range(len(titles)):
                                      data2[titles[i]] = currentLine[i]
                                      data[currentLine[0]] = data2
                        inputFile.close()      

                        writeToJSONFile(directoryWrite, fileName, data)

pywalkerLines('./RATP_GTFS_LINES')
