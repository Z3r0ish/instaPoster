from instabot import Bot
from datetime import datetime, timedelta
from random import *
import os, random, time
from config import *
import json
import discord
from discord.ext import commands
from threading import Thread

#
# functions to parse the json file, I'm not going to comment all of them
#

def getPrefix(client, message):
    with open(jsonPath, 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def getPath():
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    return str(path['path-' + user])

def getEngagementRate():
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    return path['minEngagementRate-' + user]

def getMinAge():
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    return path['minAge-' + user]

def getTimeout():
    with open(jsonPath, 'r') as f:
        path = json.load(f)
    return int(path['timeout-' + user])



# log into the client
client = discord.Client()

# login into instagram
bot = Bot() 
bot.login(username = user, password = passwd) 

# when the bot is logged in print it in the terminal
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    
class postingClass(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):

        posting = True
        i =0

        # loops the posting function ever x secs
        while posting == True:
            posted = False

            # checks if the folder is empty
            if [f for f in os.listdir(getPath()) if not f.startswith('.')] == []:
                posted = True
                posting = False

            # random caption shit
            if randomCaption == True:
                i = randint(-1, (len(topCaption) - 1))
            elif randomCaption == False:
                i += 1
            # in the event that i becomes larger than they array it will reset to 0
            if i > (len(topCaption) - 1):
                i = 0


            if posted == False:
                # get a random file
                file = random.choice(os.listdir(getPath()))
                print(file)

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
                #await ctx.send('the poster has ' + str(followersInt) + ' followers, ' + str(likesInt) + ' likes on this post and it was posted ' + str(dateDif) + ' ago. This is an engagement rate of ' + str(engagement))

                # checks if the post is above the minimun engagement rate and age
                # had to make 2 if statements since doing if engagement > minEngagementRate & dateDif.days > minAge: freaked it out
                
                if engagement > getEngagementRate(): 
                    if dateDif.days > getMinAge():
                        #upload the file
                        bot.upload_photo(getPath() + file, caption = "test")
                            
                        posted = True
                

                # delete the file once it's done with it
                try:
                    os.remove(getPath() + file + '.REMOVE_ME')
                except:
                    print("Wasn't able to delete " + getPath() + file + '.REMOVE_ME')
                else:
                    print("removed " + getPath() + file + '.REMOVE_ME')

                # checks if the folder is empty
                if [f for f in os.listdir(getPath()) if not f.startswith('.')] == []:
                    posted = True
                    #await ctx.send(getPath + " is empty") 
                    posting = False
            
            time.sleep(getTimeout() + randint(-getTimeout(), getTimeout()))

postingClass()

# immport the token
client.run(token)