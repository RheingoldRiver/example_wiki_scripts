from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)
summary = 'Creating year stats pages for 2021'


for champion_row in site.cargo_client.query(tables="Champions", fields="Name", limit="max"):
	champion = champion_row['Name']
	site.save_title(champion + '/Statistics/2021', '{{ChampionYearStatsPage}}', summary=summary)
