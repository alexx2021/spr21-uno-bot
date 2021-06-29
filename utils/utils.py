import discord

async def sendToPlayerChannel(self, player, message:str):
    chID = self.bot.channel_assignments[player.name]
    ch = self.bot.get_channel(chID)
    if ch:
        if len(message) <= 0:
            print('Messages cannot be empty!')
        else:
            await ch.send(message)
    else:
        print(f'Could not get channel {chID}')