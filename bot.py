import discord
import json
import guild_info
from discord.ext import commands

if __name__ == '__main__':
    intent = discord.Intents(messages=True, members=True, guilds=True)
    bot = commands.Bot(command_prefix="!", intents=intent)
    guild_map = []

    #TODO: map guild objects with GuildInfo objects

    @bot.event
    async def on_ready():
        # create GuildInfo objects for all guilds
        for g in bot.guilds:
            guild_map.append((g, guild_info.GuildInfo(g.id, g.channels[0].id)))

    def load_from_data(filename):
        with open(f'data/{filename}.json', 'r', encoding='utf-8') as doc:
            return json.load(doc)

    @bot.command()
    async def ping(ctx):
        print('pong')
        await ctx.send('pong')
        
    @bot.event
    async def on_member_join(member):
        g_id = member.guild.id
        text_channel = 'default channel here'
        welcome_message = 'default message'
        for g in _guilds:
            text_channel = g[1].get_msg_from_input('LANDING_PAGE_ID')
            welcome_message = g[1].get_msg_from_input('WELCOME_MESSAGE')
            landing_page = member.guild.get_channel(text_channel).mention # ???
            await member.send(f"Jag heter Pierre-Bengt, och är en bot. Du gick nyss med i **{member.guild.name}**.\n{welcome_message}\nBörja här: {landing_page} :blue_heart:")
            break

    @bot.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def new_welcome_message(ctx, *args):
        new_message = ' '.join(args)
        for g in guild_map:
            g[1].set_new_message('WELCOME_MESSAGE', new_message)
            await ctx.send(f'I set the new welcome message to: \n"{new_message}"')
            break

    @bot.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_default_channel_id(ctx, arg):
        try:
            new_id = int(arg)
            for g in guild_map:
                g[1].set_new_message('LANDING_PAGE_ID', new_id)
                await ctx.send(f'I set the new default channel ID to: \n"{ctx.guild.get_channel(new_id).mention}"')
        except TypeError:
            await ctx.send(f'I could not set the new ID, try entering a number!')

    print('Pierre-Bengt is online!')
    bot.run(load_from_data('config')['DISCORD_TOKEN'])