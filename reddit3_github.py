#cirkeltrek is the example subreddit, this can be changed

#imports all nececary modules -
import praw
import urllib.request
import time
import os, glob, os.path, shutil, math
from InstagramAPI import InstagramAPI
#-

#defines the directory of where your pictures will be stored -
mydir='/home/pi/Desktop/python/fotos/'
os.chdir(mydir)
#-

#logs in on Instagram-
InstagramAPI = InstagramAPI("Username", "Password")
InstagramAPI.login()
#-

#gets userfeed and uses that to delete any post on there
InstagramAPI.getSelfUserFeed()
MediaList = InstagramAPI.LastJson
Media = MediaList['items']

for f in Media:
    MediaID = f['id']
    MediaType = f['media_type']
    print(MediaID)
    isDeleted = InstagramAPI.deleteMedia(MediaID)

    if isDeleted:
        print("Your Media {0} has been deleted".format(
            MediaID
        ))
    else:
        print("Your Media Not Deleted")
#-

#creates lists and sets up a few variables-

aantal = 0

#sections will be used to specify how many pictures will be uploaded in one go, this will be used later
sections = 4
#-

#gets you connected with the reddit api using praw https://praw.readthedocs.io/en/latest/-
reddit = praw.Reddit(client_id='Client_id',
                     client_secret='Client_secret',
                     user_agent='User_agent',
                     username='Username',
                     password='Password')
#-

#an infinite while loop
while True:
    mylist1 = []
    mylist2 = []

    #deletes folders and png pictures in you directory-
    filelist = glob.glob(os.path.join(mydir, "*.png"))
    for f in filelist:
        os.remove(f)

    for x in range((len(next(os.walk(mydir))[1]))):
        shutil.rmtree(mydir + str(x) + '/')
    #-

    #defines f for later use
    f = 1

    #checks how many posts are to be downloaded-
    for submissions in reddit.subreddit('cirkeltrek').top('day'):
        aantal += 1
    print(aantal)
    #-

    #downloads the posts-
    for submissions in reddit.subreddit('cirkeltrek').top('day'):
        try:
            print(f, submissions.title, submissions.url)
        except Exception as e:
            print(e)
            pass
        try:
            urllib.request.urlretrieve(submissions.url, mydir + str(f) +".png")
            #puts title and author in lists for later use
            mylist1.append(submissions.title)
            mylist2.append(submissions.author.name)
        except Exception as e:
            print(e)
            continue

        f += 1
        #-

    #checks how many pictures have succesfully been downloaded and using you specified sections makes directories-
    newaantal = len(glob.glob1(mydir,"*.png"))
    for x in range(math.ceil(newaantal/sections)):
        os.mkdir(mydir + str(x))
    #-

    #moves pictures in the just made folders and deviding them evenly-
    q = 1
    c = 0
    newaantal = len(glob.glob1(mydir,"*.png"))
    for x in range(int(newaantal)):
        os.rename(mydir + str(q) + ".png", mydir + str(c) + r'/' + str(q) + '.png')
        q += 1
        c += 1
        if c == math.ceil(newaantal/sections):
            c = 0
    #-

    #using information and math grabs the pictures of a folder, grabs the corresponding items from the lists made previously and uploads them in bursts of the specified number throughout the a 12 hour cycle-
    folders = math.ceil(newaantal/sections) #folders = amount of folders the pictures are devided in, this will be used to define the amount of time instagram has to do "upload bursts" hoi is a variable that counts which step it is on, this will also be used
    for hoi in range(folders):
        filelist2 = glob.glob(os.path.join(mydir + str(hoi) + '/', "*.png")) #is used to define which folder we are currently on
        for fotos in filelist2: # for each foto in the previously defined folder it gets the caption and uploads the fotos in a burst
            photo_path = fotos
            print(fotos)
            fotos2 = fotos.replace(mydir + str(hoi) + r'\ '.replace(' ', ''), '').replace('.png', '').replace(mydir + str(hoi) + r'/', '') #grabs the number which is used to find where the caption is stored in the lists
            print(fotos2)
            caption = mylist1[int(fotos2) - 1] + '\n\nCredits naar:\nHttps://reddit.com/r/cirkeltrek\nhttps://reddit.com/u/' + mylist2[int(fotos2) - 1] + '\n\n #memes #meme #bot #reddit #cirkeltrek'
            try:
                print(caption)
            except Exception as e: #we need a try and exception here, because sometimes it uses characters python can't print
                print(e)
                pass
            try:
                InstagramAPI.uploadPhoto(photo_path, caption=caption) # actually uploads the photo
            except Exception as e:
                print(e)
                continue
        print(43200/folders)
        time.sleep(43200/folders) #sleeps 12 hours devided by the amount of photobursts
        #deletes all the photos-
        InstagramAPI.getSelfUserFeed()
        MediaList = InstagramAPI.LastJson
        Media = MediaList['items']
        for f in Media:
            MediaID = f['id']
            MediaType = f['media_type']
            print(MediaID)
            isDeleted = InstagramAPI.deleteMedia(MediaID)

            if isDeleted:
                print("Your Media {0} has been deleted".format(
                    MediaID
                ))
            else:
                print("Your Media Not Deleted")
        #-
        #loops back to the for hoi loop until it is done with all of the photobursts at which point it loops back to the while loop
    #-
