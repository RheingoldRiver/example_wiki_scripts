from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from mwclient.page import Page

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials, max_retries=10)
summary = "Updating with category & licensing"

# Ran this after item_pages_move.py

for page in site.client.categories['Items']:
	page: Page
	name: str = page.name.replace(' (Item)', '')
	print('Starting {}'.format(name))
	file = site.client.pages['File:ItemSquare{}.png'.format(name)]
	if not file.exists:
		continue
	text = file.text()
	if 'redirect' in text:
		continue
	if not '[[category:' in text.lower():
		text = text + '\n[[Category:Item Icons]]'
	if not '{{fairuse}}' in 'text'.lower():
		text = text + '\n{{Fairuse}}'
	site.save(file, text, summary=summary)
