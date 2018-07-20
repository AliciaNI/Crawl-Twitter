#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
author NJ

"""
import json
from abc import abstractclassmethod,ABCMeta
# from log_exception import log_exception
from bs4 import BeautifulSoup
from collections import deque
from lxml import etree
import requests
import urllib3
import urllib
import chardet
import lxml
import time


class stand(object):
    def __init__(self,url):
        self.url = url

    def get_code(self):
        header = {
            'Host': 'twitter.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': 'personalization_id="v1_0bX/3jJBXjfZuVgyPxW2JA=="; guest_id=v1%3A152764746430367475; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCM2NLmhkAToMY3NyZl9p%250AZCIlN2QyZWFhYmU5ZmM0N2NhOGUwMzc0YjVhMjljNjlhNjk6B2lkIiVjNzE1%250ANzVhNjQ3ZTIwY2Y3NGQ4OTBlZDgyNTQxZDMzZA%253D%253D--ba03ec182d985941082c07a67f728db990d115c6; external_referer=padhuUp37zhCDepgXWiVsH%2FCSp%2BRC3DyasExw9bKMpYQyy2Bp5I5d1zwkCmAUEMOSpasjFfpo2T%2FbKlLNYBPb8PfD%2FtkZAWN%2FxB5orB%2BC5cwVzIQCKSLBRkqTLvPmY37CA5YMOU3EMO8CYWxmbjhR%2FF6O%2BQI%2B50soZ0jHC%2Fu9wtIq6i1E%2BeJNghwzvraf7tv|0|8e8t2xd8A2w%3D; ct0=ffb7ad5543b707ad2774b1fccb47b7bf; _ga=GA1.2.2136415474.1530756250; _gid=GA1.2.577590670.1530756250; gt=1014691382936498176; lang=zh-cn; __utma=43838368.2136415474.1530756250.1530756390.1530756390.1; __utmc=43838368; __utmz=43838368.1530756390.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); tfw_exp=0; _gat=1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # resp =urllib.request.urlopen(self.url).read().decode('utf-8')
        resp = requests.get(self.url.strip(),headers = header)
        with open('a.txt','wb')as f:
            f.write(resp.text.encode('utf-8'))
        soup = BeautifulSoup(resp.text,'html.parser')
        # pagesource = etree.HTML(resp)
        # resp_json = json.loads(resp.text)

        return soup

    def save_twitter(self,twitter):
        pass

    @classmethod            #类方法 可以调用类内的我i他方法
    def get_article(cls):
        source = cls(url.strip()).get_code()
        li_list = source.find_all('li',class_='js-stream-item')   #得到所有的评论
        myStack = deque([])
        for i in li_list[1:]:

            tweet_id = i['data-item-id']
            article_url_path_short = i.find('div')['data-permalink-path']
            article_url_path = article_url_path_short if 'http' in article_url_path_short else 'https://twitter.com'+article_url_path_short
            user_id = i.find('div')['data-user-id']
            screen_name = i.find('div')['data-screen-name']
            user_name = i.find('div')['data-name']
            p_list = i.select('.js-tweet-text-container p')
            for p_c in p_list:
                twitte_content = p_c.get_text()

            picture = i.find(class_='AdaptiveMedia-photoContainer js-adaptive-photo ')
            if picture:
                picture_url = picture['data-image-url']
            comment_count = i.find(class_='ProfileTweet-action--reply u-hiddenVisually').find(class_='ProfileTweet-actionCount')['data-tweet-stat-count']
            retweet_count = i.find(class_='ProfileTweet-action--retweet u-hiddenVisually').find(class_='ProfileTweet-actionCount')['data-tweet-stat-count']
            favorite_count = i.find(class_='ProfileTweet-action--favorite u-hiddenVisually').find(class_='ProfileTweet-actionCount')['data-tweet-stat-count']
            publishtime = i.find(class_='_timestamp js-short-timestamp js-relative-timestamp')['data-time']
            publishtime_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(publishtime)))

            tw_json = {
                'tweet-id': i['data-item-id'],
                'article_url_path': article_url_path,
                'user_id': user_id,
                'screen_name': screen_name,  # 显示名称
                'user_name': user_name,  # 用户名称
                'twitte_content':twitte_content,
                'picture_url': picture_url,  # 图片
                'comment_count': comment_count,  # 评论数
                'retweet_count': retweet_count,  # 转推数
                'favorite_count': favorite_count,  # 喜欢数
                'publishtime': publishtime_

            }
            myStack.push(tw_json)
            cls().save_twitter(tw_json)
        return myStack

    @classmethod
    def get_comments(cls):    #抓取评论
        """
        1:将保存到栈中的字典信息，循环读取ID，继续抓取评论
        2：问题：1）：栈如果为空    出现原因：抓取失败   停顿继续抓取
        :return:
        """
        myStack = stand.get_article()
        if myStack.isEmpty():
            time.sleep(8*60)        #如果栈为空，则等待8分钟 继续执行
        else:
            for i in range(0,len(myStack)):
                tw_json = myStack.pop()
                source = cls(tw_json['article_url_path']).get_code()         #获取带有评论的源码
                user_list = source.find_all('div', class_='content')
                try:
                    for i in user_list[1:]:
                        # print(i)
                        print('--------------')
                        reply_content = i.find('p', class_='TweetTextSize js-tweet-text tweet-text')  # 评论内容
                        print(reply_content.text)
                        Breply_name = i.find('a', class_='pretty-link js-user-profile-link')['data-user-id']  # 被回复人id
                        print(Breply_name)
                        reply_name = i.find('strong', class_='fullname show-popup-with-id u-textTruncate ')  # 评论人名
                        print(reply_name.text)
                        reply_short_name = i.find('span', class_='username u-dir u-textTruncate')  # 评论人shortname
                        print(reply_short_name.text)
                        user_id = i.find('a',
                                         class_='account-group js-account-group js-action-profile js-user-profile-link js-nav')[
                            'data-user-id']  # 用户ID
                        print(user_id)
                        publishtime = i.find('span', class_='_timestamp js-short-timestamp js-relative-timestamp')[
                            'data-time']
                        punlishtime_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(publishtime)))  # 发布时间
                        print(punlishtime_)
                        reply_reply = i.find('span', class_='ProfileTweet-action--reply u-hiddenVisually')  # 回复数
                        print(reply_reply.text)
                        retweet_count = i.find('span', class_='ProfileTweet-action--retweet u-hiddenVisually')  # 转推数
                        print(retweet_count.text)
                        favorite_count = i.find('span', class_='ProfileTweet-action--favorite u-hiddenVisually')  # 喜欢数
                        print(favorite_count.text)

                        comment_json = {
                            'reply_id' : Breply_name,
                            'reply_name':reply_name.tex,
                            'reply_replyCount':reply_reply.text,
                            'reply_retweetCount':retweet_count.text,
                            'reply_favoriteCount':favorite_count.text,
                            'repkly_time':punlishtime_,
                            'reply_content':reply_content.text
                        }
                    cls().save_twitter(tw_json)

                except Exception as ex:
                    print(ex)


if __name__ == '__main__':

    with open('keywords','rb') as f:
        for i in f.readlines():
            print('i:', i.decode('utf-8'))
            url = 'https://twitter.com/hashtag/{}'.format(i.decode('utf-8'))
            print('url', url)
            stand(url).get_article()
            break

