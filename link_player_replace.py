from river_mwclient.esports_client import EsportsClient
from river_mwclient.auth_credentials import AuthCredentials
from river_mwclient.template_modifier import TemplateModifierBase

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('lol', credentials=credentials)  # Set wiki
summary = 'Use just |player=, no |link='  # Set summary


class TemplateModifier(TemplateModifierBase):
    def update_template(self, template):
        """
        Previously we specified both |player= as the name of the player, and |link= as an optional
        disambiguation of the exact page name of the player's page. But I eventually realized that because
        page names are always of the form IGN (IRL Name), we can just specify the link and determine the IGN
        from that, so there's no need for the player param period. We can therefore eliminate |player= and
        ONLY specify |link=.

        I wanted to call this param |player= in the update, so this script gets rid of |player= and replaces
        it with the value of |link=, if a |link= was present.

        Sometimes in the past people misused the |link= param though, so we needed to make sure that
        wasn't being done; if it was, then we could go back and fix that case by hand later after the fact.
        :param template:
        :return:
        """

        # in this case there was already no disambiguating |link= parameter
        if not template.has('link'):
            return

        player = template.get('player').value.strip()
        link = template.get('link').value.strip()

        # in this case the link isn't simply disambiguating the |player= parameter, it's
        # an entirely different thing, so we need to be careful with whatever is going on and check by hand
        if not link.lower().startswith(player.lower()):
            return

        # remove |link= and set that as the |player= instead
        template.remove('link')
        template.add('player', link)


TemplateModifier(site, 'ExtendedRosterLine',
                 summary=summary).run()
