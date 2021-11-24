from mwrogue.esports_client import EsportsClient
from mwrogue.auth_credentials import AuthCredentials
from mwclient.page import Page
import mwparserfromhell

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials, max_retries=10)
summary = "Create speculated item redirect"

# Recently I did a bunch of file rearranging, but it was kinda incomplete in making *all* of the
# needed file redirects I needed, so I'm now trying to fix that

for item_page in site.pages_using('Infobox Item'):
	page: Page
	file_name = 'File:ItemSquare{}.png'.format(item_page.name)
	item = item_page.name
	
	item_page_text = item_page.text()
	
	# first try and find out from the Infobox Item template on the page what the redirect should be
	# this part of the script actually ended up with some self-redirects that I didn't want
	# because I didn't realize that people had filled in the |image= with the name of the item
	# unnecessarily....so I should have added a check for that
	# but whatever, it didn't really create THAT much extra work for myself
	used_infobox = False
	for template in mwparserfromhell.parse(item_page_text).filter_templates():
		template: mwparserfromhell.nodes.Template
		if not template.name.matches('Infobox Item'):
			continue
		if template.has('image'):
			target = template.get('image').value.strip()
			file_page = site.client.pages[file_name]
			
			# this part is important, make sure we're not doing anything destructive
			if file_page.exists:
				continue
			
			file_page.save(
				'#redirect[[{}]]'.format('File:ItemSquare' + target),
				summary = summary + ' based on infobox |image= value'
			)
			
			# it's hard to break out of nested for loops lol
			used_infobox = True
	if used_infobox:
		continue
	
	print('Starting item {}...'.format(item))
	redirects = item_page.backlinks(filterredir='redirects')
	for redir in redirects:
		redir: Page
		redir_name = redir.name
		
		# (Item) redirects aren't actual content redirects, they're legacy
		if '(Item)' in redir_name:
			continue
			
		new_file_page = site.client.pages['File:ItemSquare{}.png'.format(redir_name)]
		# This check is the more expensive of the two (requires api call) so do it last
		if new_file_page.exists:
			continue
		
		# otherwise create a file redirect
		print(redir_name)
		new_file_page.save(
			'#redirect[[{}]]'.format(file_name), summary=summary
		)
