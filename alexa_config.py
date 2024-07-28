
import asyncio
import aiohttp
from datetime import datetime, timedelta
import logging
import json
import pprint
import sys

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

f = open('config.json', 'r')
script_config = json.load(f)
f.close()

class HAConnection:
    def __init__(self, endpoint, access_token):
        self.access_token = access_token
        self.endpoint = endpoint
        self.connected = False
        self.ws = None
        self.command_number = 10

    async def get_config(self):
        endpoint = self.endpoint
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(endpoint) as ws:
                    self.ws = ws
                    msg = await ws.receive_json()
                    logger.info('HA     Server info: %s', msg)
                    
                    await ws.send_json({
                          "type": "auth",
                          "access_token": self.access_token
                        })

                    self.connected = True
                    logger.debug('HA Connected')
                    await ws.send_json({
                            "id": 3,
                            "type": "get_states"
                        })
                    await ws.send_json({
                            "id": 4,
                            "type": "get_panels"
                        })
                    await ws.send_json({
                            "id": 5,
                            "type": "lovelace/config",
                            "url_path": script_config['dashboard'],
                            "force": False
                        })

                    friendlynames = {}

                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            logger.debug('HA    Message: %s', pprint.pformat(json.loads(msg.data),width=140))
                            data = json.loads(msg.data)
                            logger.debug(data)
                            if 'id' in data and data['id'] == 3:
                                for entity in data['result']:
                                    try:
                                        entityid = entity['entity_id']
                                        friendlyname = entity['attributes']['friendly_name']
                                    except:
                                        continue
                                    friendlynames[entityid] = friendlyname

                            if 'id' in data and data['id'] == 5:
                                cards = data['result']['views'][0]['cards']
                                for card in cards:
                                    if card['type'] == 'entities':
                                        title = card.get('title')
                                        logger.info('Card %s',title)
                                        for entity in card['entities']:
                                            logger.info(entity['entity'])

                                config_text = '  smart_home:\n    filter:\n      include_entities:\n'
                                for card in cards:
                                    if card['type'] == 'entities':
                                        for entity in card['entities']:
                                            config_text += '        - %s\n' % (entity['entity'],)

                                config_text += '    entity_config:\n'
                                for card in cards:
                                    if card['type'] == 'entities':
                                        title = card.get('title')
                                        for entity in card['entities']:
                                            if 'name' in entity:
                                                name = entity['name']
                                            else:
                                                name = friendlynames[entity['entity']]
                                            config_text += '      %s:\n        name: "%s"\n        description: "%s"\n' % (entity['entity'],name,'%s:%s' % (title,name))
                                f = open('alexa.yaml','w')
                                f.write(config_text)
                                f.close() 
                                return

                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            break
        except:
            logger.exception('Exception in HA receive loop')


hac = HAConnection(script_config['url'], script_config['access_token'])
loop = asyncio.get_event_loop()
loop.run_until_complete(hac.get_config())

