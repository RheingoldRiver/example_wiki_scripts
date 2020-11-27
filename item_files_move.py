import time
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from mwclient.page import Page

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials, max_retries=10)
summary = "Moving item pages"

failed = []

try:
	for page in site.client.categories['Items']:
		page: Page
		name: str = page.name.replace(' (Item)', '')
		print('Starting {}'.format(name))
		file = site.client.pages['File:{}.png'.format(name)]
		if not file.exists:
			failed.append(name)
			continue
		if 'redirect' in file.text().lower():
			continue
		site.move(file, 'File:ItemSquare{}.png'.format(name))
except Exception as e:
	print(failed)
	print(e.__traceback__)
	
print('Printing failed items...')

print(failed)
