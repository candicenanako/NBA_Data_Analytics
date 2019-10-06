from TwitterSearch import *
import pandas as pd

# get tweets data with Keywords
def getKeywords(player_list,team_list,data):
    for i in range(len(player_list)):
        tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
        tso.set_keywords([player_list[i], team_list[i]])  # let's define all words we would like to have a look for

        # it's about time to create TwitterSearch object again
        ts = TwitterSearch(
            consumer_key='xS8fpqO1s8upG1ckRwVyFuZaa',
            consumer_secret='paND54SRGIcWHF0iLkDDxvFSZxYrIxaU1FUryc9sflGnXFY3UP',
            access_token='1177214448844587009-NS7vOJ8wUCBxPCVR2AaQbKFUVTudvu',
            access_token_secret='vFFvBAQB2FnAmtoYMoHAXtWTuTByK5KqKpUmrjrtyb7IG'
        )
        # start asking Twitter about the keywords
        for tweet in ts.search_tweets_iterable(tso):
            data.append(
                [tweet['created_at'], [player_list[i],team_list[i]],tweet['entities']['hashtags'],tweet['text'],tweet['entities']['user_mentions'],tweet['retweet_count'],
                tweet[ 'favorite_count']])
            print(len(data))

if __name__ == '__main__':
    try:
        # player keywords
        player_list = ['Antetokounmpo', 'Harden', 'Westbrook', 'Curry', 'Durant', 'James','Rose','James','Bryant']
        # team keywords
        team_list = ['Bucks', 'Rockets', 'Thunder', 'Warriors', 'Thunder', 'Heat','Bulls','Cavaliers','Lakers']
        data = []
        getKeywords(player_list,team_list,data)
        df = pd.DataFrame(columns=['time', 'key_words',  'hashtags', 'text', 'user_mentions', 'retweet_count','favorite_count'], data=data)
        df.to_csv('tweets_keywords.csv', encoding='utf-8')

    except TwitterSearchException as e: # catch all those ugly errors
        print(e)