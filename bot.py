import os
from twitchio.ext import commands
from twitchio.ext import routines
from urllib import request
import json
from time import sleep

API_URL = 'https://tmi.twitch.tv/group/user/davidshelbs/chatters'
VIEWERS_PER_SESSION = set()

class Bot(commands.Bot):
    
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=os.environ['TMI_TOKEN'], 
                         prefix=os.environ['BOT_PREFIX'], 
                         initial_channels=[os.environ['CHANNEL']], 
                         client_id=os.environ['CLIENT_ID'], 
                         nick=os.environ['BOT_NICK'])

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        self.greet_loop.start()
        
    @routines.routine(seconds=5.0)
    async def greet_loop(self):
        viewer_greet_list = list()
        new_viewer = False
        req = request.Request(API_URL)
        viewers = json.loads(request.urlopen(req).read())['chatters']['viewers']
        for viewer in viewers:
            if viewer not in VIEWERS_PER_SESSION:
                viewer_greet_list.append(viewer)
                new_viewer = True
        if new_viewer:
            VIEWERS_PER_SESSION.update(viewers)
            await self.get_channel(os.environ['CHANNEL']).send(f'Hello, {", ".join(viewer_greet_list)}! Welcome to the Channel! PogChamp')

bot = Bot()
bot.run()