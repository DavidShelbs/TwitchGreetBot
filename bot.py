import os
import twitchio
from twitchio.ext import commands
from twitchio.ext import routines
from urllib import request
import json
import logging

DEBUG = False
API_URL = f'https://tmi.twitch.tv/group/user/{os.environ["CHANNEL"]}/chatters'
VIEWERS_PER_SESSION = set()

logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)
class Bot(commands.Bot):
    
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot
        super().__init__(token=os.environ['TMI_TOKEN'], 
                         prefix=os.environ['BOT_PREFIX'], 
                         initial_channels=[os.environ['CHANNEL']], 
                         client_id=os.environ['CLIENT_ID'], 
                         nick=os.environ['BOT_NICK'])

    async def event_ready(self):
        # We are logged in and ready to chat and use commands
        logging.info(f'Logged in as | {self.nick}')
        logging.info(f'User id is | {self.user_id}')
        # Start greet loop routine
        self.greet_loop.start()
    
    @routines.routine(seconds=5.0)
    async def greet_loop(self):
        chatter_greet_list = list()
        sub_greet_list = list()
        sub_viewing = False
        chatter_viewing = False
        
        if DEBUG:
            sub_greet_list = ['testsub', 'lsdkjf', 'dsklfj']
            chatter_greet_list = ['testchatter', 'tsetjch', 'lksjdgk']
            sub_viewing = True
            chatter_viewing = True
        
        # Get current chatters
        req = request.Request(API_URL) 
        viewers = json.loads(request.urlopen(req).read())['chatters']['viewers']
        viewers += json.loads(request.urlopen(req).read())['chatters']['moderators']
        viewers += json.loads(request.urlopen(req).read())['chatters']['vips']
        for viewer in viewers:
            if viewer not in VIEWERS_PER_SESSION and viewer != os.environ['BOT_NICK']:
                # if self.get_channel(os.environ['CHANNEL']).get_chatter(viewer).is_subscriber:
                #     sub_greet_list.append(viewer)
                #     sub_viewing = True
                # else:
                chatter_greet_list.append(viewer)
                chatter_viewing = True
                
        if sub_viewing:
            if len(sub_greet_list) == 1:
                bot_msg = f'The myth, the legend, {sub_greet_list[0]} is in the chat! PogChamp  '
            elif len(sub_greet_list) == 2:
                bot_msg = f'The myths, the legends, {sub_greet_list[0]} and {sub_greet_list[1]} are in the chat! PogChamp  '
            elif len(sub_greet_list) > 2:
                bot_msg = f'The myths, the legends, {", ".join(sub_greet_list[:-1])}, and {sub_greet_list[-1]} are in the chat! PogChamp  '
            await self.get_channel(os.environ['CHANNEL']).send(bot_msg)

        if chatter_viewing:
            if len(chatter_greet_list) == 1:
                bot_msg = f'Hello, {chatter_greet_list[0]}! Welcome to the Channel! PogChamp'
            if len(chatter_greet_list) == 2:
                bot_msg = f'Hello, {chatter_greet_list[0]} and {chatter_greet_list[1]}! Welcome to the Channel! PogChamp'
            if len(chatter_greet_list) > 2:
                bot_msg = f'Hello, {", ".join(chatter_greet_list[:-1])}, and {chatter_greet_list[-1]}! Welcome to the Channel! PogChamp'
            await self.get_channel(os.environ['CHANNEL']).send(bot_msg)
        
        # Update a set of viewer each session the bot is ran so we dont greet viewers multiple times
        VIEWERS_PER_SESSION.update(viewers)
        
if __name__ == "__main__":
    bot = Bot()
    bot.run()