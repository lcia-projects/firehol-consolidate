
# Louisiana State Police / Louisiana Cyber Investigators Alliance
# FireHol Processor: downloads the firehol block ipsets and converts them into a single csv and yaml file. This can be
# used/imported into various tools & network appliances.
#
# Resources:
# http://la-safe.org
# https://github.com/lcia-projects
# http://iplists.firehol.org/


import os
from git import Git
import shutil
from pprint import pprint

ipDict={}
dirpath = './blocklist-ipsets'

def pullListsFromGit():
    try:
        print("--: Pulling new datasets from GIT, this could take a minute or two, please wait..")
        # remove previous data
        if os.path.isdir(dirpath):
            shutil.rmtree(dirpath)

        os.mkdir(dirpath)

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
                if line in ipDict.keys():
                    # already in dictionary
                    ipDict[line].append(strDescription)

                else:
                    # new ip
                    tagArray.append(strDescription)
                    ipDict[line] = tagArray.copy()
                    tagArray.clear()
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

    #cleans up and saves output
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

    # pull iplists from git
    pullListsFromGit()

    #get file names and process them
    for file in os.listdir("./blocklist-ipsets"):
        if file.endswith(".ipset"):
            strFilename=os.path.join("./blocklist-ipsets", file)
            readFiles(strFilename)

    saveYAML()
    saveCSV()

    # removes ipset data
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
