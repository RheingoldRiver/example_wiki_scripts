import re

from mwrogue.esports_client import EsportsClient
from mwrogue.auth_credentials import AuthCredentials
from mwcleric.page_modifier import PageModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)
summary = 'Updating to new ExtendedRoster template'

class PageModifier(PageModifierBase):
	def update_plaintext(self, text):
		"""
		We want to change the following text:
		
		{{ExtendedRosterStart|team1=KnockOut Esports|team2=Galaxy Racer Esports
		}}
		{{ExtendedRosterLine|flag=Egypt|res=None|player=Maged|name=Maged Marawan|role=Top
		|r= }}
		{{ExtendedRosterLine}}
		
		to:
		
		{{ExtendedRoster|team1=KnockOut Esports|team2=Galaxy Racer Esports
		|{{ExtendedRoster/Line|flag=Egypt|res=None|player=Maged|name=Maged Marawan|role=Top
		|r= }}
		}}
		
		Note the need for the re.MULTILINE flag. Also note the use of the *? lazy quantifier instead of
		the * greedy quantifier.
		Originally I used +? but then actually there were some pages where ExtendedRosterStart had no
		parameters and I had to change it to *?
		"""
		text = text.replace('{{ExtendedRosterLine', '|{{ExtendedRoster/Line')
		text = text.replace('{{ExtendedRosterEnd}}', '}}')
		text = re.sub(re.compile(r'ExtendedRosterStart([^}]*?)}}', re.MULTILINE),
		              r'ExtendedRoster\1', text)
		return text


PageModifier(site, page_list=site.pages_using('ExtendedRosterStart'),
             summary=summary).run()
