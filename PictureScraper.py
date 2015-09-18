"""
    David Baker
    Last Revision : 9/18/2015

    Objective
        Write a program that will download pictures from the given Imgur links
        The program will create a folder to hold all the pictures (if one doesn't exist)
        The program will also create a folder for each subreddit that it is sent to

    Current Issues:
        The user cannot select a file path the default is a folder on the desktop
        The user cannot run this on non windows systems it will not recognize the file path
            UPDATE : This should now run on non windows systems, but is not tested yet
        The Program cannot differentiate between imgur urls and regular reddit urls
            It is advised until this is fixed go to picture only subreddits
"""

import os
import simplejson
import urllib.request


'''
    Function reads Json file and downloads all unique imgur URLS
    Function will check log file so it only downloads newFiles
'''
def downloadPhoto(file_name):
    data_file = open(file_name , "r")
    data = simplejson.load(data_file)


    sub = file_name[len(file_name)-7:len(file_name) - 5] #removes .txt to leave sub name
   # valid_urls = ["http://imgur.com/", "http://i.imgur.com/"]
    num_photos = 0

    print (sub)

    for index in range(1,26): ''' 25 entries on front page '''
        photo_name = data['data']['children'][index]['data']['title']
        imgUrl = data["data"]["children"][index]["data"]["url"]
        if not isInDirectory(sub, imgUrl):
            writeUrlToLog(sub, imgUrl)
            ''' download picture'''
            urllib.request.urlretrieve(imgUrl, photo_name)
            num_photos += 1
        print("\n" + num_photos + " new photos have been added")

'''
    Function will right new URL's to log file
    Each new Entry will be will be on a new line

    Possible Future update  : store values in dictionary by using the last
        of the url as a Hash, but this could be problematic since
        the last of the url is randomized. Though cool in theory waste of time
        since an O(n) algorithm is plenty for this use unless someone downloads
        millions upon millions of photos...then RIP hard drive
'''
def writeUrlToLog(sub_name,picture_url):
    if not isInDirectory(sub_name, picture_url):
        path = defaultPath() + "Reddit_Pictures/" + sub_name + "_Pictures/" + sub_name + ".txt"
        if os.path.isfile(path):
            with open(path, "a") as file:
                file.write("" + picture_url + os.linesep)
        else:
            print("no log file found at path " + path + "/n")


'''
    function will check if a file is in directory's log
'''
def isInDirectory(sub_name, picture_url):
    path = defaultPath() + "/Reddit_Pictures/" + sub_name + "_Pictures"
    file_name = path + "/" + sub_name + ".txt"
    in_log = False

    if os.path.isfile(path + "/" + sub_name + ".txt"):
        file = open(file_name,"r")
        for line in file:
            if line is picture_url:
                in_log = True

        file.close()
    else:
        print("run createPhotoLogFile first! If you have, something else went wrong have fun!")
    # if function reaches this point the photo is not in the log file
    return in_log


'''
    Will create a default path to where the program is being executed
    Ex : C:/Users/*/PycharmProjects/Filelocation
'''
def defaultPath():
    return os.path.dirname(os.path.realpath(__file__))

'''
    Creates a directory for the pictures
'''
def createPictureDirectory():
    path = defaultPath()
    if not os.path.exists(path + "/Reddit_Pictures"):
        os.mkdir(path + "/Reddit_Pictures")


'''
    Creates picture directory for specified sub
'''
def createSubsDirectory(sub_name):
    path = defaultPath()
    if os.path.exists(path + "/Reddit_Pictures/"):
        os.mkdir(path+ "/Reddit_Pictures/" + sub_name + "_Pictures")
    else:
        createPictureDirectory()

'''
    Creates log file
'''
def createPhotoLogFile(sub_name):
    path = defaultPath() + "/Reddit_Pictures/" + sub_name + "_Pictures"
    if os.path.exists(path):
        os.chdir(path)
        file = open("" + sub_name + "_Pictures_Log.txt", "w") # THIS WILL OVERWRITE AN EXISTING FILE
        print (file.name + " has been created")
        file.close()

    else:
        print("Run createPictureDirectory() first!")


'''
    Save the subs json URL to a file to be read
'''
def urlToFile(sub_reddit):
    if checkForDirectorys(sub_reddit):
        os.chdir(defaultPath()+ "/Reddit_Pictures/" + sub_reddit + "_Pictures")
        url = "https://www.reddit.com/r/" + sub_reddit + "/.json"
        file_name = "" + sub_reddit + ".json"
        urllib.request.urlretrieve(url, file_name)
        os.chdir(defaultPath())
    else:
        print ("There is no proper directory to write to log file")


'''
    Function checks for two folders
        * Reddit_Pictures
        * sub_name_Pictures
    If it doesn't find one, the function will return false
'''
def checkForDirectorys(sub_name):
    rf_exists = os.path.exists(defaultPath() + "/Reddit_Pictures")
    sr_exists = os.path.exists(defaultPath() + "/Reddit_Pictures/" + sub_name + "_Pictures")

    return rf_exists and sr_exists



def main():
    sub = "aww"
    if not checkForDirectorys(sub):
        if not os.path.exists(defaultPath()+"/Reddit_Pictures"):
            createPictureDirectory()

        if not os.path.exists(defaultPath() + "/Reddit_Pictures/" + sub + "_Pictures"):
            createSubsDirectory(sub)

        if not os.path.exists(defaultPath() + "/Reddit_Pictures/" + sub + "_Pictures" + sub + ".txt"):
            createPhotoLogFile(sub)

    urlToFile(sub)
    path_to_json = defaultPath() + "/Reddit_Pictures/" + sub + "_Pictures/" + sub + ".json"
    downloadPhoto(path_to_json)