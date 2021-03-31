
import os
from git import Git
import shutil
from pprint import pprint

ipDict={}

def pullListsFromGit():
    try:
        print("--: Pulling new datasets from GIT, this could take a minute or two, please wait..")

        # remove previous data
        dirpath = './blocklist-ipsets'

        try:
            os.makedirs(dirpath)
        except OSError as e:
            print ("Data Directory not found, creating it")

        # pull new data
        print("----: Getting new data Lists.....")
        Git(".").clone("git://github.com/firehol/blocklist-ipsets.git")
        print("----: Updated data sets recieved, moving forward with analysis")
    except:
        print("Error: Trouble with GIT Clone")

def readFiles(filename):
    tagArray = []
    print("   Processing File: ", filename)
    with open(filename, "r") as filehandler:
        for line in filehandler:
            if line[0] == "#":  # skips comment lines at beginning
                continue
            else:
                strDescription = filename
                strDescription = strDescription.replace(".ipset", "")
                strDescription = strDescription.replace("./blocklist-ipsets/", "")
                line = line.replace("\n", "")
                # print(line, ":", filename, ":", strDescription)
                if line in ipDict.keys():
                    # already in dictionary
                    ipDict[line].append(strDescription)
                    # print ("---- Duplicate:", self.ipDict[line])

                else:
                    # new ip
                    tagArray.append(strDescription)
                    ipDict[line] = tagArray.copy()
                    tagArray.clear()
                    # print ("New IP added:", self.ipDict[line])
# for testing
def viewData():
    pprint(ipDict)

def saveYAML():
    print("--: Saving YAML File Please Wait.. ")
    yamlWriter = open("firehol_consolidated.yaml", "w")
    for item in ipDict:
        strLineToWrite = item + " : " + str(ipDict[item]) + "\n"
        yamlWriter.write(strLineToWrite)
    yamlWriter.close()

def saveCSV():
    print("--: Saving CSV File Please Wait.. ")
    csvWriter = open("firehol_consolidated.csv", "w")
    for item in ipDict:
        csvTags=str(ipDict[item])
        csvTags=csvTags.replace('[','')
        csvTags = csvTags.replace(']', '')
        csvTags = csvTags.replace("'", "")
        strLineToWrite = item + "," + '"' + csvTags+'"' + "\n"
        csvWriter.write(strLineToWrite)
    csvWriter.close()

if __name__ == '__main__':
    dataSet={}

    #fireHolProcessor = libFireHol.fireHolProcssorv1(dataSet)

    # pull iplists from git
    pullListsFromGit()

    #get files
    for file in os.listdir("./blocklist-ipsets"):
        if file.endswith(".ipset"):
            strFilename=os.path.join("./blocklist-ipsets", file)
            readFiles(strFilename)

    # viewData()
    saveYAML()
    saveCSV()
