from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.esports_client import EsportsClient
from river_mwclient.page_modifier import PageModifierBase

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)
summary = 'Bot edit'


class PageModifier(PageModifierBase):
	def update_plaintext(self, text):
		return '-'
	
	def update_wikitext(self, wikitext):
		return


PageModifier(site, title_list=["MediaWiki:dpl-tag-tracking-category",
                               "MediaWiki:dpl-intersection-tracking-category",
                               "MediaWiki:dpl-parserfunc-tracking-category",
                               "MediaWiki:dplnum-parserfunc-tracking-category",
                               "MediaWiki:dplvar-parserfunc-tracking-category",
                               "MediaWiki:dplreplace-parserfunc-tracking-category",
                               "MediaWiki:dplchapter-parserfunc-tracking-category",
                               "MediaWiki:dplmatrix-parserfunc-tracking-category"],
             summary=summary).run()
