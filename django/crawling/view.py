from django.shortcuts import render
import json
import twitter
import pyupbit
from django.contrib import messages
import re

t_consumer_key = "agLXI1dXGBKA5dMEGt7qIMu1P"
t_consumer_secret = "GNU7YH9rEOF3PTzGyPRg3wgtH2Bu9pD0qlccdcoqWWMK3nNr6O"

t_access_token = "1473502327575576584-mirZ1Nuyd078ro1MdvgzVYOyPGpjyT"
t_access_token_secret = "H0iS1S1Epaou6prCalJ4IvzIECtv1gZtri0mHMN7Z7Cib"

twitter_api = twitter.Api(consumer_key=t_consumer_key,
                          consumer_secret=t_consumer_secret,
                          access_token_key=t_access_token,
                          access_token_secret=t_access_token_secret)

access_key = "2makOa4sKDRgdlIBE7fSyJc2H9wT2nEcGnti70r6"
secret_key = "DSnFTqXKNhCD50h5KoF0BmPFm9VsDBStxpeijt5a"

upbit = pyupbit.Upbit(access_key, secret_key)

global_id = "@elonmusk"
global_word = "Tesla"
stream_data = []



def getApi(id, keyword):
    tweet = twitter_api.GetUserTimeline(screen_name=id, count=1000, include_rts=False, exclude_replies=True)
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
    keyword_tweet = []
    for i in (tweet):
        if i.text.find(keyword) != -1:
            keyword_tweet.append(i.text)
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
    ask_size = orderbook[0]['orderbook_units'][1]['ask_size']
    bid_size = orderbook[0]['orderbook_units'][1]['bid_size']
    var_orderbook = orderbook[0]['orderbook_units']
    return total_ask_price, total_bid_price, ask_size, bid_size, var_orderbook

def myupbitinfo():
    info = upbit.get_balances()
    myubpitlist = []
    market_name = []
    market_balance = []
    avg_buy_price = []
    total_price = []
    for myinfo in info:
        market_name.append(myinfo['currency'])
        market_balance.append(myinfo['balance'])
        avg_buy_price.append(myinfo['avg_buy_price'])
        total_price.append(float(myinfo['balance']) * float(myinfo['avg_buy_price']))
        if(myinfo['currency'] != 'KRW'):
            myubpitlist.append([myinfo['currency'], float(myinfo['balance']) * float(myinfo['avg_buy_price']) , myinfo['avg_buy_price'], myinfo['balance']])

    return myubpitlist

# Create your views here.
def index(request):
    return (render(request, 'index.html', {}))

def checkAPI(request):
    if request.method == 'POST':
        check_consumer_key = request.POST['consumer_key']
        check_consumer_secret = request.POST['consumer_secret']
        check_access_token = request.POST['access_token']
        check_access_token_secret = request.POST['access_secret']
        check_access_key = request.POST['access_key']
        check_secret_key = request.POST['secret_key']
        check_twitter_api = twitter.Api(consumer_key=check_consumer_key,
                                  consumer_secret=check_consumer_secret,
                                  access_token_key=check_access_token,
                                  access_token_secret=check_access_token_secret)
        global twitter_api
        twitter_api = check_twitter_api
        global upbit
        upbit = pyupbit.Upbit(check_access_key, check_secret_key)
        if check_twitter_api:
            if upbit:
                messages.add_message(request, messages.SUCCESS, 'API가 일치합니다')
                return example(request)
            else:
                messages.add_message(request, messages.ERROR, 'UPBIT API key가 일치하지 않습니다')
                return (render(request, 'index.html', {}))
        else:
            messages.add_message(request, messages.ERROR, 'Twiter API key가 일치하지 않습니다')
            return (render(request, 'index.html', {}))


def example(request):
    id = "@elonmusk"
    keyword = "Tesla"
    global global_id
    global global_word
    global upbit
    global_id = id
    global_word = keyword
    today_tweet, tweet_date, tweet, keyword_tweet = getApi(id, keyword)
    result_date, result_open, result_close, result_high, result_low = get_upbit_api()
    price = pyupbit.get_current_price("KRW-DOGE")
    recent_tweet = []
    if tweet:
        for i in tweet:
            recent_tweet.append(i.text)

    mymoney = upbit.get_balance(ticker="KRW")
    allamount = upbit.get_amount('ALL')
    bitamount = upbit.get_balance(ticker="KRW-DOGE")
    myorderlist = upbit.get_order("KRW-DOGE", state="done")
    total_ask_price, total_bid_price, ask_size, bid_size, var_orderbook = orderbook()
    myubpitlist = myupbitinfo()
    keyword = "recent tweet"
    return render(request, 'example.html',{'user_id': id, 'tweet_text': today_tweet,'tweet_date': tweet_date,
                            'recent_tweet': recent_tweet, 'keyword_tweet': keyword_tweet,'keyword': keyword,
                            'result_date': json.dumps(result_date), 'result_open': result_open, 'result_close': result_close,
                            'result_high': result_high, 'result_low': result_low, 'price': price, 'orderbook': var_orderbook,
                            'total_ask_price': total_ask_price, 'total_bid_price': total_bid_price, 'ask_size': ask_size, 'bid_size': bid_size,
                            'mymoney': mymoney, 'allmount': allamount,'bitamount': bitamount, 'myorderlist': myorderlist,
                            'myubpitlist': myubpitlist})

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

        global upbit
        mymoney = upbit.get_balance(ticker="KRW")
        allamount = upbit.get_amount('ALL')
        bitamount = upbit.get_balance(ticker="KRW-DOGE")
        myorderlist = upbit.get_order("KRW-DOGE", state="done")
        total_ask_price, total_bid_price, ask_size, bid_size, var_orderbook = orderbook()
        myubpitlist = myupbitinfo()
        return render(request, 'example.html', {'user_id': twitter_id, 'tweet_text': today_tweet, 'tweet_date': tweet_date,
                                                'keyword_tweet': keyword_tweet, 'keyword': word, 'recent_tweet' : keyword_tweet,
                                                'result_date': json.dumps(result_date), 'result_open': result_open,
                                                'result_close': result_close, 'orderbook': var_orderbook,
                                                'result_high': result_high, 'result_low': result_low, 'price': price,
                                                'total_ask_price': total_ask_price, 'total_bid_price': total_bid_price,
                                                'ask_size': ask_size, 'bid_size': bid_size, 'mymoney': mymoney, 'allmount': allamount,
                                                'bitamount': bitamount, 'myorderlist': myorderlist,
                                                'myubpitlist': myubpitlist})
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

    total_ask_price, total_bid_price, ask_size, bid_size, var_orderbook = orderbook()
    global upbit
    mymoney = upbit.get_balance(ticker="KRW")
    allamount = upbit.get_amount('ALL')
    bitamount = upbit.get_balance(ticker="KRW-DOGE")
    myorderlist = upbit.get_order("KRW-DOGE", state="done")
    myubpitlist = myupbitinfo()
    return render(request, 'example.html', {'user_id': global_id, 'tweet_text': today_tweet, 'tweet_date': tweet_date,
                                            'keyword_tweet': keyword_tweet, 'keyword': global_word,'recent_tweet' : keyword_tweet,
                                            'result_date': json.dumps(result_date), 'result_open': result_open,
                                            'result_close': result_close, 'orderbook': var_orderbook,
                                            'result_high': result_high, 'result_low': result_low, 'price': price,
                                            'total_ask_price': total_ask_price, 'total_bid_price': total_bid_price,
                                            'ask_size': ask_size, 'bid_size': bid_size, 'mymoney': mymoney, 'allmount': allamount,
                                            'bitamount': bitamount, 'myorderlist': myorderlist,
                                            'myubpitlist': myubpitlist})

def cancelorder(request):
    if request.method == 'POST':
        num = None
        if 'num' in request.POST:
            num = request.POST['num']
            numbers = re.sub(r'[^0-9]', '', num)
        global upbit
        #uuid 가져오기

        global global_id
        global global_word
        today_tweet, tweet_date, tweet, keyword_tweet = getApi(global_id, global_word)
        result_date, result_open, result_close, result_high, result_low = get_upbit_api()
        price = pyupbit.get_current_price("KRW-DOGE")
        recent_tweet = []
        if tweet:
            for i in tweet:
                recent_tweet.append(i.text)

        mymoney = upbit.get_balance(ticker="KRW")
        allamount = upbit.get_amount('ALL')
        bitamount = upbit.get_balance(ticker="KRW-DOGE")
        total_ask_price, total_bid_price, ask_size, bid_size, var_orderbook = orderbook()
        messages.info(request, '주문 취소')
        myorderlist = upbit.get_order("KRW-DOGE", state="done")
        uuid_list = []
        for uuid in myorderlist:
            uuid_list.append(uuid[num])
        upbit.cancel_order(uuid_list[int(num)])
        myorderlist = upbit.get_order("KRW-DOGE", state="done")
        myubpitlist = myupbitinfo()
        return render(request, 'example.html',{'user_id': global_id, 'tweet_text': today_tweet,'tweet_date': tweet_date,
                            'recent_tweet': keyword_tweet, 'keyword_tweet': keyword_tweet,'keyword': global_word,
                            'result_date': json.dumps(result_date), 'result_open': result_open, 'result_close': result_close,
                            'result_high': result_high, 'result_low': result_low, 'price': price, 'orderbook': var_orderbook,
                            'total_ask_price': total_ask_price, 'total_bid_price': total_bid_price, 'ask_size': ask_size, 'bid_size': bid_size,
                            'mymoney': mymoney, 'allmount': allamount,'bitamount': bitamount, 'myorderlist': myorderlist,
                            'myubpitlist': myubpitlist})

def purchase(request):
    if request.method == 'POST':
        price = request.POST['purchase']
        global global_id
        global global_word
        global upbit
        state = upbit.buy_market_order("KRW-DOGE", int(price))
        context = {}
        today_tweet, tweet_date, tweet, keyword_tweet = getApi(global_id, global_word)
        result_date, result_open, result_close, result_high, result_low = get_upbit_api()
        price = pyupbit.get_current_price("KRW-DOGE")
        recent_tweet = []
        if tweet:
            for i in tweet:
                recent_tweet.append(i.text)

        mymoney = upbit.get_balance(ticker="KRW")
        allamount = upbit.get_amount('ALL')
        bitamount = upbit.get_balance(ticker="KRW-DOGE")
        myorderlist = upbit.get_order("KRW-DOGE", state="done")
        total_ask_price, total_bid_price, ask_size, bid_size, var_orderbook = orderbook()
        myubpitlist = myupbitinfo()
        try:
            if (state is None):
                messages.add_message(request, messages.ERROR, '잔액 부족 또는 최소 주문 금액 미달')
            else:
                messages.add_message(request, messages.SUCCESS, '주문 성공')
            return render(request, 'example.html', {'user_id': global_id, 'tweet_text': today_tweet,'tweet_date': tweet_date,
                            'recent_tweet': keyword_tweet, 'keyword_tweet': keyword_tweet,'keyword': global_word,
                            'result_date': json.dumps(result_date), 'result_open': result_open, 'result_close': result_close,
                            'result_high': result_high, 'result_low': result_low, 'price': price, 'orderbook': var_orderbook,
                            'total_ask_price': total_ask_price, 'total_bid_price': total_bid_price, 'ask_size': ask_size, 'bid_size': bid_size,
                            'mymoney': mymoney, 'allmount': allamount,'bitamount': bitamount, 'myorderlist': myorderlist,
                            'myubpitlist': myubpitlist})
        except:
            messages.add_message(request, messages.ERROR, 'ERROR 주문 실패')
            return render(request, 'example.html', {'user_id': global_id, 'tweet_text': today_tweet,'tweet_date': tweet_date,
                            'recent_tweet': recent_tweet, 'keyword_tweet': keyword_tweet,'keyword': global_word,
                            'result_date': json.dumps(result_date), 'result_open': result_open, 'result_close': result_close,
                            'result_high': result_high, 'result_low': result_low, 'price': price, 'orderbook': var_orderbook,
                            'total_ask_price': total_ask_price, 'total_bid_price': total_bid_price, 'ask_size': ask_size, 'bid_size': bid_size,
                            'mymoney': mymoney, 'allmount': allamount,'bitamount': bitamount, 'myorderlist': myorderlist,
                            'myubpitlist': myubpitlist})


