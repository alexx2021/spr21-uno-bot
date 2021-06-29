import discord
from discord.ext import commands
import asyncio
import random
from utils.frontend import channelCleanup, channelSetup, playerSetup, queryPlayerForMove
from utils.backend import buildDeck, chooseWild, createPlayerDecks, dealCards, draw, isPlayable
from utils.utils import sendToPlayerChannel

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def uno(self, ctx: commands.Context):

        playerList = await playerSetup(self, ctx)
        if len(playerList) < 2: #error msg already sent in function but need to stop it from continuing
            return

        activeChannels = await channelSetup(self, ctx, playerList)
        if (activeChannels is None) or (activeChannels == []):
            return

        deck = await buildDeck()
        playerDeckLists = await createPlayerDecks(len(playerList))

        playerDeck = await dealCards(playerDeckLists, playerList, deck)


        #debug
        for p in playerDeck:
            await ctx.send(f'ID {p.name} -  DECK {p.deck}')



        update = 1   # 1 means going ->     -1 means going <- (For Reverse)
        current = 0
        lastPlayed = "CLEAR"
        gameOver = False
        drawNo = 0


        specialCounter = 0

        while not gameOver:
            # for player in playerDeck:
            #     print(str(player.name) + "---------------------")
            #     print(player.deck)
            #     print(lastPlayed)
            #     print(len(deck))


            if specialCounter == 2 or lastPlayed[2] == '+' and not playerDeck[current].canStack(lastPlayed):
                uInput = "draw"
            else:
                uInput = await queryPlayerForMove(self, playerDeck[current], lastPlayed)

                #commented out because you dont need to put a prefix in discord in ur own priv channel
                #uInput = uInput[1:] #assumes valid input of "{color} {type}" or "!draw"

                print(f'TESTING {playerDeck[current].validate(uInput)}')

            if uInput == "draw":
                if drawNo != 0:
                    print("forced---------------------------------")
                    await draw(drawNo, playerDeck[current], deck)
                    drawNo = 0
                    lastPlayed = lastPlayed[0] + " ?"
                    specialCounter = 0
                else:
                    await draw(1, playerDeck[current], deck)
                    current = (current + update)%len(playerDeck)
            elif playerDeck[current].validate(uInput) and await isPlayable(lastPlayed, uInput):
                playerDeck[current].deck.remove(uInput)
                if uInput[2] == '+':
                    specialCounter += 1
                    drawNo += int(uInput[3])
                elif uInput[2] == 'R':
                    update *= -1
                elif uInput[2] == 'S':
                    pass
                if len(playerDeck[current].deck) == 0:
                    gameOver = True
                    print('game over!')
                elif len(playerDeck[current].deck) == 1:
                    #need front end func to check who is most recent person who said uno <@@@@@@@@@
                    pass
                if uInput[0] == 'W':
                    buffer = list(lastPlayed)
                    buffer[0] = await chooseWild()
                    lastPlayed = "".join(buffer)

                lastPlayed = uInput
                current = (current + update)%len(playerDeck)
            else:
                await sendToPlayerChannel(self, playerDeck[current], "The card you chose is not valid!")


        #cleanup channels
        await ctx.send('Waiting 10 seconds before I delete the channels!')
        await asyncio.sleep(10)
        await channelCleanup(self, ctx, activeChannels)



def setup(bot):
    bot.add_cog(games(bot))