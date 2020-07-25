from instabot import Bot
from datetime import datetime, timedelta
from random import *
import os, random, time
from config import *

posting = True
i = 0

# login into instagram
bot = Bot() 
bot.login(username = user, password = passwd) 

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

        # checks if the follower count has a comma
        if ',' in filename[1]:
            followers = filename[1].split(',')
            followersInt = (int(followers[0]) * 1000 + int(followers[1]))
        # checks if the follower count has a k
        elif 'k' in filename[1]:
            followers = filename[1].split('k')
            followersInt = float(followers[0]) * 1000
        # checks if the follower count has a m
        elif 'm' in filename[1]:
            followers = filename[1].split('m')
            followersInt = float(followers[0]) * 1000000
        # if there isn't anything speciall it's just turned into the followers var
        else:
            followersInt = int(filename[1])

        # checks if the likes has a comma
        if ',' in filename[3]:
            likes = filename[3].split(',')
            likesInt = int(''.join(likes))
        # if there isn't anything speciall it's just turned into the likes var
        else:
            likesInt = int(filename[3])

        # gets the current datetime and the datetime of the post and 
        datePost = datetime.strptime(filename[2], "%Y-%m-%dT%H:%M:%S.%fZ")
        dateDif = datetime.now() - datePost

        # calculates the engagement
        engagement = likesInt / followersInt

        # prints out some info about the photo     
        print('the poster has ' + str(followersInt) + ' followers, ' + str(likesInt) + ' likes on this post and it was posted ' + str(dateDif) + ' ago. This is an engagement rate of ' + str(engagement))

        # checks if the post is above the minimun engagement rate and age
        # had to make 2 if statements since doing if engagement > minEngagementRate & dateDif.days > minAge: freaked it out
        if engagement > minEngagementRate: 
            if dateDif.days > minAge:
                 # random caption shit
                if randomCaption == True:
                    i = randint(0, (len(topCaption) - 1))
                else:
                    i += 1
                
                #upload the file
                bot.upload_photo(filepath + file, caption = (topCaption[i] + bottomCaption))
                    
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