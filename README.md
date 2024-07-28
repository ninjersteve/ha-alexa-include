# HA Alexa Include

Generates an Alexa configuration YAML for Home Assistant from only the entities listed on a specific dashboard. Create a new dashboard (perhaps named "Alexa") consisting of Entities Cards. Add the entities you wish to make available to Alexa to the cards. The title of each card will appear in the description of each entity within Alexa. One use is to title each card with a room name, so that that room name appears in the entity descriptions when trying to create groups within the Alexa app. You can also set a display name for each entity on each card and that name will be used for Alexa instead of the original entity name, so that you can use names that work better with speech or within the app.

**NOTE:** This was a personal script posted with the quickest of cleanups to satisfy a request to share.

## Procedure

### Install aiohttp:

Install the aiohttp package using pip. This was tested with version 3.8.3 of the aiohttp package.

`pip install aiohttp`

### Create configuration:

Provide the URL to your Home Assistant instance, an access token, and the identifier of the dashboard to use in config.json:

`{
    "dashboard": "dashboard-alexa",
    "url": "http://localhost:8123/api/websocket",
    "access_token": "aLoNgToKeNsTrInG-123123123123123123123123123"
}`

### Run: 

Run alexa_config.py to generate a new alexa.yaml.

`python alexa_config.py`

### Include:

Include it in your Home Assistant's configuration.yaml:

`alexa: !include alexa.yaml`

Then restart Home Assistant for it to take effect.