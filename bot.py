import discord
import json
from discord.ext import commands
intents = discord.Intents()
intents.members = True

client = commands.Bot(command_prefix="<", intents=intents)

def load_from_data(filename):
    with open(f'data/{filename}.json', 'r', encoding='utf-8') as doc:
        return json.load(doc)

@client.command()
async def ping(ctx):
    await ctx.send('pong')

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def set_welcome_message(ctx, *args):
    json_object["WELCOME_MESSAGE"] = ' '.join(args)
    messages = load_from_data('messages')
    json.dump(json_object, messages)
    messages.close()

@client.event
async def on_member_join(member):
    messages = load_from_data('messages')
    await member.send(f"{messages['WELCOME_MESSAGE']} {messages['DEFAULT_CHANNEL_ID']}")

print('Pierre-Bengt is online!')
client.run(load_from_data('config')['DISCORD_TOKEN'])