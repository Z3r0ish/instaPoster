from instabot import Bot
from datetime import datetime, timedelta
import os, random, time
from config import *

posting = True
i = 0

# loops the posting function ever x secs
while posting == True:
    posted = False

    # checks if the folder is empty
    if [f for f in os.listdir(filepath) if not f.startswith('.')] == []:
        posted = True
        print("The folder is empty")
        posting = False

    # in the event that i becomes larger than they array it will reset to 0
    if i > (len(topCaption) - 1):
        i = 0

    while posted == False:
        # get a random file
        file = random.choice(os.listdir(filepath))

        # splits up the file name
        filename = file.split('&')

        # gets the current datetime and the datetime of the post and 
        datePost = datetime.strptime(filename[2], "%Y-%m-%dT%H:%M:%S.%fZ")
        dateDif = datetime.now() - datePost

        # calculates the engagement
        engagement = float(filename[3]) / float(filename[1])

        # prints out some info about the photo     
        print('the poster has ' + filename[1] + ' followers, ' + filename[3] + ' likes on this post and it was posted ' + str(dateDif) + ' ago. This is an engagement rate of ' + str(engagement))

        # checks if the post is above the minimun engagement rate and age
        # had to make 2 if statements since doing if engagement > minEngagementRate & dateDif.days > minAge: freaked it out
        if engagement > minEngagementRate: 
            if dateDif.days > minAge:
                # login into instagram
                bot = Bot() 
                bot.login(username = user, password = passwd) 

                #upload the file
                bot.upload_photo(filepath + file, caption = (topCaption[i] + bottomCaption))
                i += 1
                posted = True
        
        # delete the file once it's done with it
        try:
            os.remove(filepath + file + '.REMOVE_ME')
        except:
            print("Wasn't able to delete " + str(filepath + file + '.REMOVE_ME'))

        # checks if the folder is empty
        if [f for f in os.listdir(filepath) if not f.startswith('.')] == []:
            posted = True
            print("The folder is empty")
            posting = False

    time.sleep(timeout)