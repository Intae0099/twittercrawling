from django.shortcuts import render
from .forms import SearchForm
import json
import twitter
import pyupbit

t_consumer_key = "agLXI1dXGBKA5dMEGt7qIMu1P"
t_consumer_secret = "GNU7YH9rEOF3PTzGyPRg3wgtH2Bu9pD0qlccdcoqWWMK3nNr6O"

t_access_token = "1473502327575576584-mirZ1Nuyd078ro1MdvgzVYOyPGpjyT"
t_access_token_secret = "H0iS1S1Epaou6prCalJ4IvzIECtv1gZtri0mHMN7Z7Cib"

twitter_api = twitter.Api(consumer_key=t_consumer_key,
                          consumer_secret=t_consumer_secret,
                          access_token_key=t_access_token,
                          access_token_secret=t_access_token_secret)

global_id = None
global_word = None

def getApi(id, keyword):
#id = "@elonmusk"
    tweet = twitter_api.GetUserTimeline(screen_name=id, count=1000, include_rts=False, exclude_replies=True)
    #그림일때 텍스트 불러들여오기 실패
    if tweet:
        pass
    else:
        today_tweet = "Fail to load"
        tweet_date = None
        keyword_tweet = None
        return today_tweet, tweet_date, tweet, keyword_tweet

    today_tweet = tweet[0].text
    tweet_date = tweet[0].created_at
#keyword = "Tesla"
    keyword_tweet = find_keyword(tweet, keyword)
    if keyword_tweet:
        pass
    else:
        keyword_tweet = None
    return today_tweet, tweet_date, tweet ,keyword_tweet

def find_keyword(tweet, keyword):
    numcount = 0
    keyword_tweet = []
    for i in (tweet):
        if i.text.find(keyword) != -1:
            keyword_tweet.append(i.text)
            if numcount > 4:
                numcount = 0
                break
            else:
                numcount = numcount + 1
    return keyword_tweet


def get_upbit_api():
    chart_data = pyupbit.get_ohlcv(ticker="KRW-DOGE", interval="minute60", count=24)
    result_date = []
    result_open = []
    result_close = []
    result_high = []
    result_low = []
    for k in chart_data.index:
        result_date.append(str(k))
    for p in chart_data['open'].values:
        result_open.append(float(p))
    for n in chart_data['close'].values:
        result_close.append(float(n))
    for n in chart_data['high'].values:
        result_high.append(float(n))
    for n in chart_data['low'].values:
        result_low.append(float(n))

    return result_date, result_open, result_close, result_high, result_low

def orderbook():
    orderbook = pyupbit.get_orderbook(ticker="KRW-DOGE", limit_info=1)
    total_ask_price = orderbook[0]['total_ask_size']
    total_bid_price = orderbook[0]['total_bid_size']
    ask_size = 1
    bid_size = 1
    return total_ask_price, total_bid_price, ask_size, bid_size

# Create your views here.
def example(request):
    id = "@elonmusk"
    keyword = "Tesla"
    global global_id
    global global_word
    global_id = id
    global_word = keyword
    today_tweet, tweet_date, tweet, keyword_tweet = getApi(id, keyword)
    result_date, result_open, result_close, result_high, result_low = get_upbit_api()
    price = pyupbit.get_current_price("KRW-DOGE")
    recent_tweet = []
    if tweet:
        for i in tweet:
            recent_tweet.append(i.text)

    total_ask_price, total_bid_price, ask_size, bid_size = orderbook()
    """
    numid = ['44196397']
    streaming = twitter_api.GetStreamFilter(follow=numid)
    temp = streaming['user']
    if temp['id_str'] == numid[0]:
        stream = temp['text']
    """
    keyword = "recent tweet"
    return render(request, 'example.html',{'user_id': id, 'tweet_text': today_tweet,'tweet_date': tweet_date,
                            'recent_tweet': recent_tweet, 'keyword_tweet': keyword_tweet,'keyword': keyword,
                            'result_date': json.dumps(result_date), 'result_open': result_open, 'result_close': result_close,
                            'result_high': result_high, 'result_low': result_low, 'price': price,
                            'total_ask_price': total_ask_price, 'total_bid_price': total_bid_price, 'ask_size': ask_size, 'bid_size': bid_size})

def search(request):
    if request.method == 'POST':
        twitter_id = request.POST['ID']
        word = request.POST['word']
        context = {}
        today_tweet, tweet_date, tweet, keyword_tweet = getApi(twitter_id, word)
        result_date, result_open, result_close, result_high, result_low = get_upbit_api()
        price = pyupbit.get_current_price("KRW-DOGE")
        recent_tweet = []
        if tweet:
            for i in tweet:
                recent_tweet.append(i.text)

        total_ask_price, total_bid_price, ask_size, bid_size = orderbook()
        return render(request, 'example.html', {'user_id': twitter_id, 'tweet_text': today_tweet, 'tweet_date': tweet_date,
                                                'keyword_tweet': keyword_tweet, 'keyword': word,
                                                'result_date': json.dumps(result_date), 'result_open': result_open,
                                                'result_close': result_close,
                                                'result_high': result_high, 'result_low': result_low, 'price': price,
                                                'total_ask_price': total_ask_price, 'total_bid_price': total_bid_price,
                                                'ask_size': ask_size, 'bid_size': bid_size
                                                })
def refresh(request):
    global global_id
    global global_word
    today_tweet, tweet_date, tweet, keyword_tweet = getApi(global_id, global_word)
    result_date, result_open, result_close, result_high, result_low = get_upbit_api()
    price = pyupbit.get_current_price("KRW-DOGE")
    recent_tweet = []
    if tweet:
        for i in tweet:
            recent_tweet.append(i.text)

    total_ask_price, total_bid_price, ask_size, bid_size = orderbook()

    return render(request, 'example.html', {'user_id': global_id, 'tweet_text': today_tweet, 'tweet_date': tweet_date,
                                            'keyword_tweet': keyword_tweet, 'keyword': global_word,
                                            'result_date': json.dumps(result_date), 'result_open': result_open,
                                            'result_close': result_close,
                                            'result_high': result_high, 'result_low': result_low, 'price': price,
                                            'total_ask_price': total_ask_price, 'total_bid_price': total_bid_price,
                                            'ask_size': ask_size, 'bid_size': bid_size
                                            })

def stream(request):
    global global_id
    global global_word
    myid = ['1473487493375082500']
    today_tweet, tweet_date, tweet, keyword_tweet = getApi(global_id, global_word)
    return render(request, 'example.html', {'user_id': global_id, 'tweet_text': today_tweet, 'tweet_date': tweet_date,
                                            'keyword_tweet': keyword_tweet, 'keyword': global_word})
