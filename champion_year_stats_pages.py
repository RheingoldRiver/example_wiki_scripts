from mwrogue.esports_client import EsportsClient
from mwrogue.auth_credentials import AuthCredentials

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)
new_year = '2021'
summary = 'Creating year stats pages for {}'.format(new_year)


for champion_row in site.cargo_client.query(tables="Champions", fields="Name", limit="max"):
	champion = champion_row['Name']
	site.save_title(champion + '/Statistics/{}'.format(new_year), '{{ChampionYearStatsPage}}', summary=summary)
	site.save_title(champion + '/Statistics', '#redirect [[{}/Statistics/{}]]'.format(champion, new_year))
