import json
import random
import requests
import hashlib
import hmac
import tqdm
import urllib


def generate_random_key(length):
    xx = "0123456789ABCDEF"
    return ''.join(random.choice(xx) for _ in range(length))

def randomUUID():
    UUID8 = generate_random_key(8)
    UUID4 = generate_random_key(4)
    UUID4_2 = generate_random_key(3)
    UUID4_3 = generate_random_key(4)
    UUID12 = generate_random_key(12)
    randomUUID = "{}-{}-4{}-{}-{}".format(UUID8,UUID4,UUID4_2,UUID4_3,UUID12)
    return randomUUID

def GuestToken():
    url = 'https://api.twitter.com/1.1/guest/activate.json'
    headers = {'Host': 'api.twitter.com',
                'X-Twitter-Client-DeviceID': randomUUID(),
                'Authorization':'Bearer {}'.format('AAAAAAAAAAAAAAAAAAAAAAj4AQAAAAAAPraK64zCZ9CSzdLesbE7LB%2Bw4uE%3DVJQREvQNCZJNiz3rHO7lOXlkVOQkzzdsgu6wWgcazdMUaGoUGm'),
                'X-Client-UUID': randomUUID()}

    get_guest_token_ = requests.post(url, headers=headers)
    json_guest_token = json.loads(get_guest_token_.content)
    guest_token=json_guest_token['guest_token']
    return guest_token
def login(Username,Password):
    url = 'https://api.twitter.com/auth/1/xauth_password.json'
    headers = {'User-Agent':'Twitter-HEXXXX/8.27.1 iOS/13.3 (Apple;hex,6;;;;;1;2017)',
               'Host': 'api.twitter.com' ,
               'X-Twitter-Client-DeviceID':randomUUID(),
               'Authorization':'Bearer {}'.format('AAAAAAAAAAAAAAAAAAAAAAj4AQAAAAAAPraK64zCZ9CSzdLesbE7LB%2Bw4uE%3DVJQREvQNCZJNiz3rHO7lOXlkVOQkzzdsgu6wWgcazdMUaGoUGm'),
               'X-Client-UUID':randomUUID(),
               'X-Guest-Token':GuestToken(),
               'Content-Type':'application/x-www-form-urlencoded'}
    data  = 'send_error_codes=1&x_auth_identifier={}&x_auth_login_verification=true&x_auth_password={}'.format(Username,Password)
    login = requests.post(url , data=data ,headers=headers)
    return login


def DestoyTweets(oauth_token_secret,oauth_token,ids):
    key = "GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU&{}".format(oauth_token_secret)
    databeforeEnc = "POST&https%3A%2F%2Fapi.twitter.com%2F1.1%2Fstatuses%2Fdestroy%2F{}.json&oauth_consumer_key%3DIQKbtAYlXLripLGPWd0HUA%26oauth_nonce%3D133333333337%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1631907844%26oauth_token%3D{}%26oauth_version%3D1.0".format(
        ids, oauth_token)
    signature = urllib.pathname2url(hmac.new(key, msg=databeforeEnc, digestmod=hashlib.sha1).digest().encode('base64'))
    headers = {'Connection': 'close', 'X-Twitter-Client-Language': 'en',
               'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'api.twitter.com',
               'Authorization': 'OAuth oauth_signature="{}", oauth_nonce="133333333337", oauth_timestamp="1631907844", oauth_consumer_key="IQKbtAYlXLripLGPWd0HUA", oauth_token="{}", oauth_version="1.0", oauth_signature_method="HMAC-SHA1"'.format(
                   signature, oauth_token)}
    req1 = requests.post("https://api.twitter.com/1.1/statuses/destroy/"+ids+".json", headers=headers)
    if req1.status_code == 200:
        print("sucsess delete","\n")
    elif "Timestamp out of bounds." in req1.text:
        print("timestamp change it manualy ")
    else:
        print("error")
        print(req1.text)


def main():
    print("hi there remember disable 2FA")
    tweets = raw_input("enter file : ")
    tweets_id = []
    try:
        ff = open(tweets, 'r')
        ff = json.loads(ff.read())
        for xx in ff:
            tweets_id.append(xx["tweet"]["id"])
            #if "0000 2016" in xx["tweet"]["created_at"] or "0000 2015" in xx["tweet"]["created_at"] or "0000 2014" in xx["tweet"]["created_at"] or "0000 2013" in xx["tweet"]["created_at"] or "0000 2012" in xx["tweet"]["created_at"]:
                #tweets_id.append(xx["tweet"]["id"])
    except FileNotFoundError as dd:
        exit(dd)

    user = raw_input("enter username: ")
    password = raw_input("enter passowrd: ")
    trylogin = login(user,password)
    if trylogin.status_code == 401:
        print("are you sure about login information ?")
    elif trylogin.status_code == 200:
        try:
            jsondata = json.loads(trylogin.content)
            auth_token = jsondata['oauth_token']
            oauth_token_secret = jsondata['oauth_token_secret']
            for ids in tqdm.tqdm(tweets_id):
                DestoyTweets(oauth_token_secret,auth_token,ids)

        except KeyError:
            print("oops something wrong")

if __name__ == '__main__':
    main()
