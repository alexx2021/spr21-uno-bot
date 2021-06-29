import discord
from discord.ext import commands
import asyncio




async def channelCleanup(self, ctx, activeChannels):
    for channelID in activeChannels:
        if ctx.guild.me.guild_permissions.manage_channels:
            channel = ctx.guild.get_channel(int(channelID))
            await channel.delete(reason='Uno game cleanup')
            await asyncio.sleep(1)
    await ctx.send('Channels have been cleaned up.')


async def queryPlayerForMove(self, player, lastPlayed):    
    try:

        chID = self.bot.channel_assignments[player.name]
        ch = self.bot.get_channel(chID)
        if ch:
            def check(message: discord.Message):
                return message.channel == ch

            tempString = ""
            for card in player.deck:
                tempString += f'\n{card}'

            eDesc = "Default"
            eTitle = "Make a move!"
            e = discord.Embed(color=discord.Color.random(), title=eTitle)
            e.set_footer(text='Send the exact value of a card or "draw" to draw a card.')

            if "CLEAR" in lastPlayed:
                e.add_field(name='Your deck:', value = tempString)
                await ch.send(content=f'<@{player.name}>', embed = e)
            
            else:
                e.add_field(name='Your deck:', value = tempString)
                e.add_field(name='Last played card:', value=lastPlayed)
                await ch.send(f'<@{player.name}>', embed = e)
                
        
            msg = await self.bot.wait_for('message', check=check, timeout=60)

            return msg.content
    except asyncio.exceptions.TimeoutError:
        return "draw"


#creates a channel for each individual player
async def channelSetup(self, ctx: commands.Context, players):
    activeChannels = []
    if ctx.guild.me.guild_permissions.manage_channels and ctx.guild.me.guild_permissions.manage_roles:
        for player in players:
            await asyncio.sleep(1)
            memberPlayer = ctx.guild.get_member(player)
            if not memberPlayer:
                memberPlayer = await ctx.guild.fetch_member(player)
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            memberPlayer: discord.PermissionOverwrite(read_messages=True)

            }
            channel = await ctx.guild.create_text_channel(f'{memberPlayer.name}-uno', overwrites=overwrites)

            await asyncio.sleep(0.5)

            self.bot.channel_assignments[memberPlayer.id] = channel.id #global dictionary that contains a player and their corresponding channel
            activeChannels.append(channel.id)

            await channel.send(f'{memberPlayer.mention}, You will recieve your deck and other game info in here.')
        return activeChannels
    else:
        await ctx.send('I do not have permissions to create channels/manage roles (edit channel permissions)')
        return None
        


#gets called after the user info has been collected AND players >= 2
async def postCollectUser(self, ctx, players):
    desc = ''
    for i in players:
        desc += f'<@{i}>\n'

    e = discord.Embed(color=0, description=desc)

    await ctx.send(content=f'**{len(players)}** players were registered for the upcoming game', embed=e)

#gets called to collect info on who is playing
async def collectUser(self, ctx, players):
    def check(message: discord.Message):
        return message.channel == ctx.channel
    
    try:
        msg = await self.bot.wait_for('message', check=check, timeout=5)
    except asyncio.exceptions.TimeoutError:
        if len(players) < 2:
            return await ctx.send('At least 2 players are required to play. Run the command again to start another game.')
        else:
            return await postCollectUser(self, ctx, players)


    if msg.author.id not in players:
        if len(players) <= 6:
            try:
                if self.bot.channel_assignments[msg.author.id]:
                    await ctx.send(f'{msg.author.mention} already is part of a game in progress. They have not been added to this game.')
            except KeyError:
                players.append(msg.author.id)
                await ctx.send(f'{msg.author.mention} :thumbsup:')
            finally:
                await collectUser(self, ctx, players)
        else:
            return await postCollectUser(self, ctx, players)
    else:
        #function recurrs (I cant spell) until len(players) <= 6
        await collectUser(self, ctx, players)



#starts the game
async def playerSetup(self, ctx):
    await ctx.send(f'**Anyone who would like to play, please speak within the next 30 seconds!**')

    players = []
    await collectUser(self, ctx, players)
    return players