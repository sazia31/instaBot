import requests
from keys import APP_ACCESS_TOKEN
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import pylab
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#Token Owner : acadtest
#Sandbox Users : AVinstaBot.test0, AVinstaBot.test1, AVinstaBot.test2...... AVinstaBot.test10
#sandboxSK: _as1228_ , pktest1111


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

def follow_request():
    # get the number of users who have requested to follow you.
    request_url=( BASE_URL + 'users/self/requested-by?access_token=%s') % (APP_ACCESS_TOKEN)
    follow_requests= requests.get(request_url).json()

    if follow_requests['meta']['code']== 200:
        if len(follow_requests['data']):
            for x in range (0,len(follow_requests['data'])):
                follow = follow_requests['data'][x]['username']
                print 'The users with this username are: %s\n' % (follow)

        else:
            print 'No follow requests!'
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

def user_search():
    search_result = raw_input("Enter the name: ")
    request_url=(BASE_URL + 'users/search?q=%s&access_token=%s') % (search_result, APP_ACCESS_TOKEN)
    Q=requests.get(request_url).json()

    if Q['meta']['code']==200:
        if len(Q['data']):
            for x in range (0,len(Q['data'])):
                search = Q['data'][x]['id']
                print 'The users with this username are: %s\n' % search

        else:
            print 'No results found for this user!'
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
            #url library is used to fetch the post and save it
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
            max_like= MAX_LIKE_ID['data'][0]['id']+ '.jpeg'
            image_url=MAX_LIKE_ID['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, max_like)
            print 'The recent post you liked has been downloaded!'
        else:
            print 'There is no recent post!'
    else:
        print 'Status code other than 200 received!'

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()



def list_users_liked(insta_username):
    user_liked = get_post_id(insta_username)
    if user_liked == None:
        print 'This user doesnot exist!'
        exit()
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (user_liked, APP_ACCESS_TOKEN)
    media = requests.get(request_url).json()

    if media['meta']['code'] == 200:
        if len(media['data']):

            for x in range(0, len(media["data"])):
                print media['data'][x]['username']

        else:
            print 'There are no likes on this picture!'
    else:
        print 'Status code other than 200 received!'


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"

def view_comments(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") %(media_id, APP_ACCESS_TOKEN)
    print "Get Request URL: %s" %(request_url)
    user_comments = requests.get(request_url).json()

    if user_comments["meta"]["code"] == 200:
        if len(user_comments["data"]):
            for x in range(0, len(user_comments["data"])):
                print user_comments["data"][x]["text"]
        else:
            print "There are no comments on the post!"
            exit()
    else:
        print "Status code other than 200 received!"
        exit()

def delete_negative_comment(insta_username):
    #this function will delete the negative comments from the user post by using NLP
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #implementation of how to delete the negative comments!
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

def hash_tag(insta_username):
    tags_dictionary = {}
    #this function is used to analyze hashtag data!
    user_id = get_user_id(insta_username)
    if user_id==None:
        print 'no existing user'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    hash_items=requests.get(request_url).json()

    if hash_items['meta']['code'] == 200:
        if len(hash_items['data']):
            # implementation of how to fetch the hashtag data!
            for x in range(0,len(hash_items['data'])):
                my_tag_len=len(hash_items['data'][x]['tags'])

                #print hash_items['data'][x]['tags']


                for y in range(0, my_tag_len):
                  #var = hash_items['data'][y]['tags']
                  #s = {y: var.count(y) for y in var}
                  if hash_items['data'][x]['tags'][y] in tags_dictionary:
                        tags_dictionary[hash_items['data'][x]['tags'][y]]+=1
                  else:
                      tags_dictionary[hash_items['data'][x]['tags'][y]]=1

                # this counts the number of different hashtags occuring on a post!
        else:
            print 'no data!'
    else:
        print 'Status code other than 200 received!'
    print tags_dictionary

    wordcloud = WordCloud().generate_from_frequencies(tags_dictionary)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.show()


    pylab.figure(1)
    x= range(len(tags_dictionary))
    pylab.xticks(x,tags_dictionary.keys())
    pylab.plot(x,tags_dictionary.values(),"b")
    pylab.show()




def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to InstaBot!!'
        print "a. Get your own details! "
        print "b. Get details of a user by username! "
        print "c. Get your recent post! "
        print "d. Get the user recent posts! "
        print "e. Get the recent media liked by the user!"
        print 'f. Search for a user!'
        print 'g. Get a list of users who liked a post!'
        print "h. Like a post!"
        print "i. Comment on a post!"
        print "j. View the list of comments on a particular post!"
        print "k. Delete negative comment on a user's post!"
        print "l. Retrieve tags!"
        print "m. Exit"

        user_choice=raw_input("Enter you choice: ")
        if user_choice=="a":
            self_info()
        #elif user_choice == 's':
            #follow_request()
        elif user_choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry."
            else:
               get_user_info(insta_username)
        elif user_choice == "c":
            get_own_post()
        elif user_choice == "d":
            insta_username = raw_input('Enter the name of the user: ')
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry."
            else:
                get_user_post(insta_username)
        elif user_choice == "e":
            recent_media_like()
        elif user_choice == "f":
            user_search()
        elif user_choice == 'g':
            insta_username= raw_input('Enter the name of the user:')
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry."
            else:
                list_users_liked(insta_username)

        elif user_choice == "h":
            insta_username=raw_input('Which user post you want to like?')
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry."
            else:
               like_a_post(insta_username)
        elif user_choice == "i":
            insta_username = raw_input('Enter the username on who\'s post you want to comment ?')
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry."
            else:
               post_a_comment(insta_username)
        elif user_choice == "j":
            insta_username = raw_input('Enter the user to view his post\'s comments!')
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry."
            else:
               view_comments(insta_username)
        elif user_choice == "k":
            insta_username = raw_input('From which user\'s post would you like to delete negative comments?')
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry."
            else:
              delete_negative_comment(insta_username)
        elif user_choice=="l":
            insta_username=raw_input('Enter the user:')
            if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                print "Invalid entry."
            else:
              hash_tag(insta_username)
        elif user_choice=="m":
            exit()
        else:
            print "Invalid Choice!"

start_bot()