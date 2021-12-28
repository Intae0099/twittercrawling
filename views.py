from django.shortcuts import render
from .forms import SearchForm
import twitter

t_consumer_key = "agLXI1dXGBKA5dMEGt7qIMu1P"
t_consumer_secret = "GNU7YH9rEOF3PTzGyPRg3wgtH2Bu9pD0qlccdcoqWWMK3nNr6O"

t_access_token = "1473502327575576584-mirZ1Nuyd078ro1MdvgzVYOyPGpjyT"
t_access_token_secret = "H0iS1S1Epaou6prCalJ4IvzIECtv1gZtri0mHMN7Z7Cib"

twitter_api = twitter.Api(consumer_key=t_consumer_key,
                          consumer_secret=t_consumer_secret,
                          access_token_key=t_access_token,
                          access_token_secret=t_access_token_secret)
id = "@elonmusk"
tweet = twitter_api.GetUserTimeline(screen_name=id, count=1000, include_rts=False, exclude_replies=True)
today_tweet = tweet[0].text
tweet_date = tweet[0].created_at

keyword = "Tesla"

keyword_tweet = []
numcount = 0
for i in (tweet):
    if i.text.find(keyword) != -1:
        keyword_tweet.append(i.text)
        if numcount > 4:
            numcount = 0
            break
        else:
            numcount = numcount + 1

# Create your views here.
def example(request):
    return render(request, 'example.html',{'user_id': id, 'tweet_text': today_tweet,'tweet_date': tweet_date, 'keyword_tweet': keyword_tweet,'keyword': keyword, 'form': SearchForm})
