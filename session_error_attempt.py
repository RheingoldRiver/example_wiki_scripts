import time

from mwrogue.gamepedia_client import GamepediaClient
from mwrogue.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
# Not an esports client!
site = GamepediaClient('wikisandbox-ucp', credentials=credentials)
summary = 'Bot edit'

# Attempt to encounter login errors and count approximately how frequently they occur
# The goal was just to obtain some data
# After running this I ended up adding a bunch of error-checking/retrying code to mwrogue

for trial in range(0, 10):
    i = 0
    while True:
        try:
            site.client.pages['User:RheingoldRiver/counter'].save(str(i))
            time.sleep(60)
            i += 1
        except Exception as e:
            site.login()
            break
    site.client.pages['User:RheingoldRiver/counter report'].append('\n' + str(i))
