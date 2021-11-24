from mwparserfromhell.nodes.extras import Parameter
from mwrogue.wiki_client import WikiClient
from mwrogue.auth_credentials import AuthCredentials
from mwrogue.template_modifier import TemplateModifierBase
from mwparserfromhell.nodes import Template

credentials = AuthCredentials(user_file="bot")
site = WikiClient(url='https://wingsoffirefanon.fandom.com', credentials=credentials)
summary = 'Updating template prameter names to make them more consistent, requested by [Redacted]'

# renames these parameter names

params = {
	'image': 'file',
	'image artist': 'artist',
	'theme animal': 'animal',
	'theme song': 'song'
}

class TemplateModifier(TemplateModifierBase):
	def update_template(self, template: Template):
		if self.current_page.name.startswith('User blog'):
			return
		for old_param_name, new_param_name in params.items():
			if template.has(old_param_name):
				param: Parameter
				param = template.get(old_param_name)
				param.name = new_param_name
				

TemplateModifier(site, 'Character', startat_page='Storm (IceWing/NightWing Hybrid)',
                 summary=summary).run()
