from channels.generic.websocket import AsyncWebsocketConsumer
from asyncio import sleep as async_sleep
import json

import asyncio

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import uuid

from bs4 import BeautifulSoup



async def parser(username=None, app_consumer=None):
    if username is None:
        return False

    uid = uuid.uuid4()

    print(f"Start parsing: {username}")
    options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    driver = webdriver.Chrome("./app/webdriver/chromedriver", chrome_options=options)

    # driver.get("https://twitter.com/hashtag/АнжиСпартак?src=tren")
    # driver.get("https://www.twitter.com/katecherryway13")
    driver.get(f"https://www.twitter.com/{username}")
    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

    for i in range(1000):
        # print(uid)
        driver.find_element_by_tag_name('body').send_keys(Keys.END)

        # await async_sleep(0.5) 
        # await app_consumer.send(text_data=json.dumps({'text': i}))
        source_code = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
        soup = BeautifulSoup(source_code, "lxml")
        tweets_block = soup.find(id="stream-items-id")
        print(len(tweets_block.find_all(class_="stream-item")))
        continue
        for tweet_block in tweets_block.find_all(class_="stream-item"):

            # print(tweet_block.prettify())


            tweet_text = tweet_block.find_all(class_="tweet-text")
            print(tweet_text)

            print("________________________________________________________________________________________________________________________________________________")





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

        n = await parser(username=username, app_consumer=self)
        print(n)

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
        print(close_code)
        self.close()
        
