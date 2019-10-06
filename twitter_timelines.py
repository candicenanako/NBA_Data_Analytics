from TwitterSearch import *
import pandas as pd

# get tweets data of one user's timelines with his username
def getTimelines(list,data,type):
    for name in list:
        tuo = TwitterUserOrder(name) # create a TwitterUserOrder

        # it's about time to create TwitterSearch object again
        ts = TwitterSearch(
            consumer_key = 'xS8fpqO1s8upG1ckRwVyFuZaa',
            consumer_secret = 'paND54SRGIcWHF0iLkDDxvFSZxYrIxaU1FUryc9sflGnXFY3UP',
            access_token = '1177214448844587009-NS7vOJ8wUCBxPCVR2AaQbKFUVTudvu',
            access_token_secret = 'vFFvBAQB2FnAmtoYMoHAXtWTuTByK5KqKpUmrjrtyb7IG'
        )

        # start asking Twitter about the timeline
        for tweet in ts.search_tweets_iterable(tuo):
            data.append([tweet['user']['screen_name'],tweet['created_at'],type,tweet['entities']['hashtags'],tweet['text'],tweet['entities']['user_mentions'],tweet['retweet_count'],
                tweet['favorite_count']])
            print(len(data))

if __name__ == '__main__':
    try:
        # player name
        player_list=['Giannis_An34','JHarden13','russwest44','StephenCurry30','KDTrey5','KingJames','drose','kobebryant']
        # team name
        team_list=['Bucks','HoustonRockets','okcthunder','warriors','okcthunder','MiamiHEAT','chicagobulls','cavs','Lakers']
        data=[]
        getTimelines(player_list,data,'player')
        getTimelines(team_list,data,'team')

        df = pd.DataFrame(columns=['screen_name', 'time', 'type', 'hashtags', 'text', 'user_mentions','retweet_count','favorite_count'], data=data)
        df.to_csv('tweets_timelines.csv', encoding='utf-8')

    except TwitterSearchException as e: # catch all those ugly errors
        print(e)