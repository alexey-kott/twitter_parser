# -*- coding: utf-8 -*-  
import re
import json
from asyncio import sleep as async_sleep

from channels.generic.websocket import AsyncWebsocketConsumer
from aiohttp import ClientSession
from bs4 import BeautifulSoup


def is_retweet(tweet):
    retweet_text = tweet.find_all(class_="js-retweet-text")
    if len(retweet_text) > 0:
        return True
    return False


def parse_tweet_info(tweet):
    text = tweet.find_all(class_="tweet-text")[0].text
    text = re.sub(r'(https://[^\s]+)', r' <a target="_blank" href="\1">\1</a> ', text)
    text = re.sub(r'(pic.twitter.com[^\s]+)', r' <a taget="_blank" href="https://\1">\1</a>', text)
    text = re.sub(r'@([^\s]+)', r' <a target="_blank" href="https://twitter.com/\1">@\1</a> ', text)
    timestamp = tweet.find_all(class_="tweet-timestamp")[0]['title']

    return {
        'text': text,
        'timestamp': timestamp,
        'is_retweet': is_retweet(tweet),
        'tweet_id': tweet['data-tweet-id'],
        'link': tweet['data-permalink-path']
    }


def user_exist(page):
    if page.find("that page doesn’t exist") == -1:
        return True
    return False


async def parser(username=None, app_consumer=None):
    async with ClientSession() as session:
        async with session.get(f"https://www.twitter.com/{username}") as response:
            response_data = await response.text()

            if not user_exist(response_data):
                await app_consumer.send(text_data=json.dumps({'action': 'user_not_exist'}))
                return

        soup = BeautifulSoup(response_data, "lxml")
        stream_container = soup.find_all(class_="stream-container")[0]
        data_min_position = stream_container['data-min-position']

        tweets = soup.find_all(class_="tweet")
        tweets = [parse_tweet_info(tweet) for tweet in tweets]
        await app_consumer.send(text_data=json.dumps(tweets))
            
        while True:
            params = {
                    'include_available_features': '1',
                    'include_entities': '1',
                    'max_position': data_min_position,
                    'reset_error_state': 'false'
            }

            async with session.get(f"https://twitter.com/i/profiles/show/{username}/timeline/tweets", params=params) as response:
                response_data = await response.text()

            response_json = json.loads(response_data)
            data_min_position = response_json['min_position']
            content = response_json['items_html']
            if data_min_position is None:
                await app_consumer.send(text_data=json.dumps({'action': 'complete'}))
                return

            soup = BeautifulSoup(content, "lxml")
            tweets = soup.find_all(class_="tweet")
            tweets = [parse_tweet_info(tweet) for tweet in tweets]
            await app_consumer.send(text_data=json.dumps(tweets))
            




class AppConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data['username']
        username = username.lstrip('@')

        await parser(username=username, app_consumer=self)


    async def disconnect(self, close_code):
        self.close()
        
