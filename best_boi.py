import discord
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from discord.ext.commands.bot import Bot

emoji = ['\U0001F1E6', '\U0001F1E7', '\U0001F1E8', '\U0001F1E9',
			'\U0001F1EA', '\U0001F1EB', '\U0001F1EC', '\U0001F1ED',
			'\U0001F1EE', '\U0001F1EF', '\U0001F1F0', '\U0001F1F1',
			'\U0001F1F2', '\U0001F1F3', '\U0001F1F4', '\U0001F1F5',
			'\U0001F1F6', '\U0001F1F7', '\U0001F1F8', '\U0001F1F9',
			'\U0001F1FA', '\U0001F1FB', '\U0001F1FC', '\U0001F1FD',
			'\U0001F1FE', '\U0001F1FF']

bot = Bot(command_prefix='/', help_command=None)
TOKEN = 'your.bot.token'

@bot.event
async def on_ready():
	print(f'Bot connected as {bot.user}')
	await bot.change_presence(activity = discord.Game('Pornhub'))

@bot.command(name='help')
async def fetchHelpInfo(helpInfo):
	await helpInfo.message.delete()
	embed = discord.Embed(title="Current available functions: ")
	embed.add_field(name='/r', value='Replies with letter boxes, usage:\n/r message_id text')
	embed.add_field(name='/meme', value='Displays random meme.\nIdea by Artif3x')
	await helpInfo.channel.send(content=None, embed=embed)

# @bot.command(name='meme')
# async def findFunMeme(memeFind):
	

@bot.command()
async def r(context, *, text):
	await context.message.delete()
	writing = ''
	arguments = text.split()
	message_id = arguments[0]

	for words in range(1, len(arguments)):
		writing = writing + arguments[words].lower()

	arguments.clear()
	context.message.id = message_id
	check_single = {}

	if len(writing) <= 20:
		for letter in writing:
			if letter in check_single:
				check_single[letter] += 1
			else:
				check_single[letter] = 1

		for key in check_single:
			if check_single[key] > 1:
				flag = False
				await context.channel.send('Each character is allowed only once!')
				break
			else:
				flag = True
		if flag == True:
			for character in range(len(writing)):
				await context.message.add_reaction(emoji[ord(writing[character]) - 97])
	else:
		await context.channel.send('Too many characters. Max: 20')

@r.error
async def info_error(ctx, error):
	await ctx.message.delete()
	await ctx.channel.send('Wrong arguments. Try /help for commands info. Message will self destruct in 10s.', delete_after = 10)

@bot.event
async def on_message(message):
	if '9gag.com/gag/' in message.content:
		driver = webdriver.Safari()
		link = re.search(r"(?P<url>https?://[^\s]+)", message.content).group("url")
		driver.get(link)
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="sc-ifAKCX jLyDeZ"]'))).click()
		mention = message.author.mention
		response = f"Hey {mention}, your meme is great!"

		try:
			found_element = driver.find_element_by_xpath('//*[@type="video/mp4"]').get_attribute("src")
			await message.channel.send(response)
			await message.channel.send(found_element)
		except:
			try:
				found_element = driver.find_element_by_xpath('//*[@rel="image_src"]').get_attribute("href")
				await message.channel.send(response)
				await message.channel.send(found_element)
			except:
				await message.channel.send(response + " But something went wrong, try pasting link next time ;)")		
		driver.close()
	await bot.process_commands(message)

bot.run(TOKEN)