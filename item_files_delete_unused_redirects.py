import time
from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from mwclient.page import Page
from mwclient.image import Image

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials, max_retries=10)
summary = "Updating with category & licensing"

# Delete unused file redirects to item squares
# These tend to collect over a while which isn't *really* a problem per se
# but does result in a ton of double redirects - after processing the most recent
# batch job, there were over 300 double redirects to fix, and I'd rather not
# have that happening, so I'm just going to delete all unused redirects now.

# For example, we had a bunch of Chinese names of items existing due to a
# failed experiment in the past to create scoreboards with Chinese item names
# entered in them - these redirects are totally unneeded at this point in time,
# and there's literally no reason to keep them around anymore.

for page in site.client.categories['Item Icons']:
	page: Image
	print('Starting page {}...'.format(page.name))
	for link in page.backlinks(redirect=True):
		print(link.name)
		link: Image
		if not link.redirect:
			continue
		i = 0
		
		# note because `link` is a file, and not a page, we MUST use imageusage and NOT backlinks here to check usage
		# link.backlinks() will return no results
		for backlink in link.imageusage():
			backlink: Page
			i += 1
		if i == 0:
			print('Deleting backlink {}...'.format(link.name))
			site.delete(link)
			
			# rate-limit myself so I can verify the code is actually working.
			# after verifying it works, I comment this out and re-run without any limiting.
			# time.sleep(5)
