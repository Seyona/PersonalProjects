'''
    David Baker
    Last Revision : 9/17/2015
    
    Objective
        Write a program that will download pictures from the given Imgur links
        The program will create a folder to hold all the pictures (if one doesn't exist)
        The program will also create a folder for each subreddit that it is sent to
    
    Current Issues:
        The user cannot select a file path the default is a folder on the desktop
        The user cannot run this on non windows systems it will not recognize the file path 
            To remedy this I will most likely write a seperate program to run on MacOS don't know about linux
        The Program cannot differentiate between imgur urls and regular reddit urls 
            It is advised until this is fixed go to picture only subreddits

'''


import getpass
import os
import json
from pprint import pprint
import urllib.request

'''
    Function reads Json file and downloads all unique imgur URLS
    Function will check log file so it only downloads newFiles
'''
def downloadPhoto(file_name):
    #with open(file_name) as data_file: data = json.load(data_file)
    ''' Hey dummy, json is a dictionary, gotta fix this ... later'''
    data_file = open(file_name , "r")
    data = json.load(data_file)

    
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
    #print (getLogPath(sub) + "/" + sub + ".txt")
    #os.remove(getLogPath(sub) + "/" + sub + ".txt")

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
        path = getLogPath(sub_name)
        if os.path.isfile(path):
            with open(path, "a") as file:
                file.write("" + picture_url + os.linesep)
        else:
            print("no log file found at path " + path + "/n")
    
'''
    function will check if a file is in directory's log
'''
def isInDirectory(sub_name, picture_url):
    path = getLogPath(sub_name)
    in_log = False
    
    if os.path.isfile(path + "/" + sub_name + ".txt"):
        file = open(path,"r")
        for line in file:
            if line is picture_url:
                in_log = True
        
        file.close()
    else:
        print("run createPhotoLogFile first! If you have, something else went wrong have fun!")
    # if function reaches this point the photo is not in the log file
    return in_log
    
'''
    Save the subs json URL to a file to be read
'''
def urlToFile(sub_reddit):
    url = "https://www.reddit.com/r/" + sub_reddit + "/.json"
    file_name = "" + sub_reddit + ".json"
    urllib.request.urlretrieve(url, file_name) 
    
'''
    Creates a log file for photos that are added
    Will also create directory if it does not exist
'''
def createPhotoLogFile(sub_name):
    path = getLogPath(sub_name)
    if os.path.exists(path):
        os.chdir(path)
        file = open("" + sub_name + "_Pictures_Log.txt", "w") # THIS WILL OVERWRITE AN EXISTING FILE
        print (file.name + " has been created")
        file.close()
        
    else:
        print("Run createPictureDirectory() first!")
    return
    
'''
    Creates a directory for the pictures
'''
def createPictureDirectory(sub_name): 
    path = getPath()
    os.chdir(path)
    if os.path.exists(path + "/Reddit_Pictures"):
        os.chdir(path + "/Reddit_Pictures")
        os.mkdir(sub_name + "_Pictures")
    else:
        os.mkdir("Reddit_Pictures")
        createPictureDirectory(sub_name)
        
'''
    Function checks for two folders
        * Reddit_Pictures
        * sub_name_Pictures
    If it doesn't find one, the function will return false
'''
def checkForDirectorys(sub_name):
    rf_exists = os.path.exists(getPath() + "/Reddit_Pictures")
    sr_exists = os.path.exists(getPath() + "/Reddit_Pictures/" + sub_name + "_Pictures")
    
    print (rf_exists,sr_exists)
    return rf_exists and sr_exists
'''
    Function checks for log file for specified sub
    returns True if found, false otherwise
'''
def checkForLogFile(sub_name):
    return os.path.exists(getLogPath(sub_name)) 

''' 
    Will create a path str, default will be desktop 
    will add option to create a custom path, eventually
'''
def getPath():
    user = getpass.getuser()
    path = "C:/Users/" + user + "/Desktop"
    return path
'''
    Function returns the path of the log
'''
def getLogPath(sub_name):  
    path = getPath() + "/" +"Reddit_Pictures/" + sub_name + "_Pictures"
    return path
    
'''
    Print the given Json file
'''
def printFile(json_file_name):
    with open(json_file_name) as data_file: data = json.load(data_file)
    pprint(data)

def main():
    print("What subreddit to you want to take pictures from?")
    
    sub = "aww"
   # sub = input()
 
    if not checkForDirectorys(sub):
        createPictureDirectory(sub)
    if not checkForLogFile(sub):
        createPhotoLogFile(sub)
    ''' Assume from here that there is a valid directory AND log file '''
    
    os.chdir(getLogPath(sub))
    urlToFile(sub)
   # printFile(getLogPath(sub) + "/" + sub + ".json")
    
   # writeUrlToLog(sub,"http://imgur.com/Wg5XVyK")
    
    os.chdir(getPath())
    downloadPhoto(getLogPath(sub) + "/" + sub + ".json")


main()