import requests
from keys import APP_ACCESS_TOKEN
import urllib

#Token Owner : acadtest
#Sandbox Users : AVinstaBot.test0, AVinstaBot.test1, AVinstaBot.test2...... AVinstaBot.test10


BASE_URL = 'https://api.instagram.com/v1/'

def self_info():
#this function is defined to access the self information of the user.
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'USERNAME: %s' % (user_info['data']['username'])
            print 'Number of your followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'Number of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'Total number of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'This user does not exist!'
    else:
        print 'Status code other than 200 received!'


def get_user_id(insta_username):
    #this function will access the id of a user by a particular username
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


def get_user_info(insta_username):
#this function will provide the information of the user

    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'Number of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'Number of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'Total number of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'No data exists for this user!'
    else:
        print 'Status code other than 200 received!'


def get_own_post():
    #This function is used to download the image from the url and store it in some file by giving the specific path!
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'Get request URL : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

def recent_media_like():
    #used to get the number of the likes on the certain post!
    request_url=(BASE_URL + 'users/self/media/liked?access_token=%s')% ( APP_ACCESS_TOKEN)
    print 'Get request URL : %s' % (request_url)
    MAX_LIKE_ID = requests.get(request_url).json()

    if MAX_LIKE_ID['meta']['code'] == 200:
        if len(MAX_LIKE_ID['data']):
            return MAX_LIKE_ID['data'][0]['likes']
        else:
            print 'There are no likes on this post!'
    else:
        print 'Status code other than 200 received!'

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to InstaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details! "
        print "b.Get details of a user by username! "
        print "c.Get your recent post! "
        print "d.Get the user recent posts! "
        print "e.Get the recent media liked by the user!"
        print "f.Exit"

        user_choice=raw_input("Enter you choice: ")
        if user_choice=="a":
            self_info()
        elif user_choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif user_choice == "c":
            get_own_post()
        elif user_choice == "d":
            insta_username = raw_input('Enter the name of the user: ')
            get_user_post(insta_username)
        elif user_choice == "e":
            recent_media_like()

        elif user_choice=="f":
            exit()
        else:
            print "Invalid Choice!"

start_bot()