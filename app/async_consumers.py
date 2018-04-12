from channels.generic.websocket import AsyncWebsocketConsumer
from asyncio import sleep as async_sleep
import json

import asyncio

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import uuid

from bs4 import BeautifulSoup

def is_retweet(tweet_block):
    tweet = tweet_block.find_all(class_="tweet")[0]
    try:
        retweeter = tweet['data-retweeter']
        return False
    except:
        return True

def diff(old_list, new_list):

    return new_list[len(old_list):]


driver_tasks = {}

async def parser(username=None, app_consumer=None, task_uid=None):
    if username is None:
        return False

    print(f"Start parsing: {username}")
    options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    driver = webdriver.Chrome("./app/webdriver/chromedriver", chrome_options=options)
    
    # driver_tasks[task_uid] = driver
    try:

        driver.get(f"https://www.twitter.com/{username}")
        driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

        

        for i in range(1000):
            driver.find_element_by_tag_name('body').send_keys(Keys.END)


            source_code = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
            soup = BeautifulSoup(source_code, "lxml")
            tweets_block = soup.find(id="stream-items-id")

            
            
            
            tweet_list = []
            old_tweet_list = []
            await app_consumer.send(text_data=json.dumps({'text':'HELLO'}))
            # for tweet_block in tweets_block.find_all(class_="stream-item"):
                

                # tweet_text = tweet_block.find_all(class_="tweet-text")[0].text
                # name = None
                # tweet_date = tweet_block.find_all(class_="tweet-timestamp")[0]['title']
                # tweet_id = tweet_block['data-item-id']
                
                # tweet_list.append({
                #     "text": tweet_text,
                #     "date": tweet_date,
                #     "is_retweet": is_retweet(tweet_block),
                #     "link": f"https://twitter.com/vkozulya/status/{tweet_id}"            
                #     })

            # tweet_diff = diff(old_tweet_list, tweet_list)

            # old_tweet_list = tweet_list
            # tweet_list = []
            # print('\n')
                # print("  ________________________________________________________________________________________________________________________________________________")

    except Exception as e:  
        print("PARSING END")
        print(str(e))
        print(e)
        driver.close()


class AppConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        # Called on connection.
        # To accept the connection call:
        await self.accept()
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        # await self.accept("subprotocol")
        # To reject the connection, call:
        # await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        
        uid = uuid.uuid4()
        # print(text_data)
        data = json.loads(text_data)
        username = data['username']

        await parser(username=username, app_consumer=self, task_uid = uid)
        # await self.send(text_data=json.dumps({'text': 'lol'}))

        # for i in range(100000):
        #     await self.send(text_data=json.dumps({'text': "Hello, world!"}))
        #     await async_sleep(1)



        # Or, to send a binary frame:
        # await self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        # await self.close()
        # Or add a custom WebSocket error code!
        # await self.close(code=4123)

    async def disconnect(self, close_code):
        # Called when the socket closes
        print("DISCONNECT")
        print(self.__dict__)
        self.close()
        
