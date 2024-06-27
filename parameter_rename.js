/*
 * This is a script to be run using node.js or any other JavaScript runtime like bun.
 * Make sure to install the dependencies using your preferred package manager:
 * 
 * npm i @quority/core mwparser
 * yarn add @quority/core mwparser
 */
import { Wiki } from '@quority/core'
import { parse } from 'mwparser'

/*
 * Rename a parameter from a template in all pages that transclude it.
 * In this example, we want to rename the `|range=` parameter from the
 * `InfoboxTropa` template in https://clashofclans.wiki.gg/es
 * to use `|rango=` instead.
 */
async function main() {
	// Create a "Wiki" instance with the URL to the /api.php endpoint.
	const wiki = new Wiki({
		api: 'https://clashofclans.wiki.gg/es/api.php',
	})

	// Login to your bot account using your BotPasswords.
	const bot = await wiki.login('username@bot', 'botpassword')

	// Get all the pages trancluding a template through API:Transcludedin. https://www.mediawiki.org/wiki/API:Transcludedin
	const transclusions = await wiki.queryProp({
		prop: 'transcludedin',
		tinamespace: 0,
		titles: 'Template:InfoboxTropa',
	})
	const pages = transclusions.flatMap(t => t.transcludedin.map(p => p.title))

	// Iterate through the obtained pages.
	for await (const page of wiki.iterPages(pages)) {
		const { content } = page.revisions[0].slots.main
		const parsed = parse(content)

		// Find the infobox template.
		const infobox = parsed.templates.find(t => t.name.toLowerCase().includes('infoboxtropa'))

		// You may not find the infobox if it is transcluded through a redirect.
		if (!infobox) {
			console.info(`Could not find infobox: ${ page.title }`)
			continue
		}

		// Get a parameter from the infobox.
		const range = infobox.getParameter('range')

		// Skip the page if the infobox doesn't have such parameter - there is nothing to update.
		if (!range) {
			continue
		}

		// Rename the parameter.
		range.name = 'rango'

		// Save your edit.
		await bot.edit({
			bot: true,
			summary: 'Updating parameter name',
			text: `${ parsed }`,
			title: page.title,
		})
		await sleep(1500)
	}
}

await main()
