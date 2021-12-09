from mwcleric.template_modifier import TemplateModifierBase
from mwparserfromhell.nodes import Template
from mwrogue.auth_credentials import AuthCredentials
from mwrogue.esports_client import EsportsClient

credentials = AuthCredentials(user_file="me")
site = EsportsClient('lol', credentials=credentials)
summary = 'Int-ify damage to champs & vision score'


# Two parameters in the template Scoreboard/Player are sometimes incorrectly entered with decimal values
# We need to convert them to ints everywhere that they appear.


class TemplateModifier(TemplateModifierBase):
    def update_template(self, template: Template):
        self.convert_to_int(template, 'damagetochamps')
        self.convert_to_int(template, 'visionscore')

    @staticmethod
    def convert_to_int(template: Template, param_name):
        if not template.has(param_name):
            return
        try:
            param_value = round(float(template.get(param_name).value.strip()))
        except ValueError:
            # if it's empty string
            return
        template.add(param_name, str(param_value))


TemplateModifier(site, 'Scoreboard/Player',
                 summary=summary).run()
