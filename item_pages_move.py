import time
from mwrogue.esports_client import EsportsClient
from mwrogue.auth_credentials import AuthCredentials
from mwclient.page import Page

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials, max_retries=10)
summary = "Moving item pages"

for page in site.client.categories['Items']:
    page: Page
    name: str = page.name
    print(name)
    if not name.endswith('(Item)'):
        continue
    if page.namespace != 0:
        continue
    clean_name = page.name.replace(' (Item)', '')
    clean_page = site.client.pages[clean_name]
    clean_page_text = clean_page.text()
    if clean_page.exists and 'redirect' not in clean_page_text.lower():
        continue
    print('Moving to {}'.format(clean_name))
    # Delete and then move because the redirect has a history so we get an error, even with ignore_warnings
    if clean_page.exists:
        site.delete(clean_page)
    mh_page: Page = site.client.pages[name + '/Match History']
    if mh_page.exists:
        clean_mh_page = site.client.pages[clean_name + '/Match History']
        if clean_mh_page.exists:
            site.delete(clean_mh_page)

    # at this time, move_subpages=True is in my fork of mwclient, I have a PR to upstream to merge it in
    site.move(page, clean_name, move_subpages=True)
