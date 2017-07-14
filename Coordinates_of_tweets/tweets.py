import json
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

tweet_files = ['@TatasteelLtd_2017-06-21_to_2017-06-27.json','tatasteel_2017-06-28_to_2017-07-04.json']
tweets = []
for file in tweet_files:
    with open(file, 'r') as f:
        for line in f.readlines():
            tweets.append(json.loads(line))

def populate_tweet_df(tweets):
    df = pd.DataFrame()

    df['text'] = list(map(lambda tweet: tweet['text'], tweets))

    df['location'] = list(map(lambda tweet: tweet['user']['location'], tweets))

    df['country_code'] = list(map(lambda tweet: tweet['place']['country_code']
                                  if tweet['place'] != None else '', tweets))

    df['long'] = list(map(lambda tweet: tweet['coordinates']['coordinates'][0]
                        if tweet['coordinates'] != None else 'NaN', tweets))

    df['latt'] = list(map(lambda tweet: tweet['coordinates']['coordinates'][1]
                        if tweet['coordinates'] != None else 'NaN', tweets))

    return df
df = populate_tweet_df(tweets)
# plot the blank world map
my_map = Basemap(projection='merc', lat_0=50, lon_0=-100,
                     resolution = 'l', area_thresh = 5000.0,
                     llcrnrlon=-140, llcrnrlat=-55,
                     urcrnrlon=160, urcrnrlat=70)
# set resolution='h' for high quality

# draw elements onto the world map
my_map.drawcountries()
#my_map.drawstates()
my_map.drawcoastlines(antialiased=False,
                      linewidth=0.005)

# add coordinates as red dots
longs = list(df.loc[(df.long != 'NaN')].long)
latts = list(df.loc[df.latt != 'NaN'].latt)
x, y = my_map(longs, latts)
my_map.plot(x, y, 'ro', markersize=6, alpha=0.5)
plt.show()
'''plt.savefig("temp.png")'''
