from TwitterSearch import *
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['ADNSporting']) # let's define all words we would like to have a look for
    tso.set_language('pt') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'MFpmoi9o2v1t3AfiVvq3FLfx0',
        consumer_secret = 'qzcwYGhWADg4Ki6f3h9Ah439Y6yqSIlwyCJ9XpztXehWRHPmnG',
        access_token = '1231903899487023104-v85tu1G7AK1KA4ewbqXd237c1Gb73K',
        access_token_secret = 'i3LeVRf8gF8AZKZaf0FibkbRPr9TndbWc159694zj6nf7'
     )

     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)