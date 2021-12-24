import twitter

t_consumer_key = "agLXI1dXGBKA5dMEGt7qIMu1P"
t_consumer_secret = "GNU7YH9rEOF3PTzGyPRg3wgtH2Bu9pD0qlccdcoqWWMK3nNr6O"

t_access_token = "1473502327575576584-mirZ1Nuyd078ro1MdvgzVYOyPGpjyT"
t_access_token_secret = "H0iS1S1Epaou6prCalJ4IvzIECtv1gZtri0mHMN7Z7Cib"

twitter_api = twitter.Api(consumer_key=t_consumer_key,
                          consumer_secret=t_consumer_secret,
                          access_token_key=t_access_token,
                          access_token_secret=t_access_token_secret)

text2 = input('찾으시는 유저를 입력해 주세요 : ')
text = input('찾으시는 단어를 입력해 주세요 : ')

tweet = twitter_api.GetUserTimeline(screen_name=text2, count=100, include_rts=True, exclude_replies=False)
result = []

for i in tweet:
    result.append([i.text])

for p in result:
    if any(text in s for s in p):
        print(p)
