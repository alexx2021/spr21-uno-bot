import random
from utils.frontend import playerSetup

# variables
class Player(object):
  def __init__(self, x, y):
    self.name = x
    self.deck = list(y)
  def validate(self, attempt):
    for card in self.deck:
      if card == attempt:
        return True
    return False
  def canStack(self, lastPlayed):
    if lastPlayed == "CLEAR":
      return True
    for card in self.deck:
      if card[2] == '+' and int(card[3]) >= int(lastPlayed[3]):
        return True
    return False



# build Deck ( just regular ordered deck )
async def buildDeck():
    cardList = [] #stores cards
    colors = ["R", "G", "B", "Y"] #color name (red, green, blue, yellow)

    for color in colors:
      for number in range(13):
        if number == 0:
          cardList.append(f"{color} {number}")
        elif number == 10:
          cardList.append(f"{color} +2")
          cardList.append(f"{color} +2")
        elif number == 11:
          cardList.append(f"{color} Skip")
          cardList.append(f"{color} Skip")
        elif number == 12:
          cardList.append(f"{color} Reverse")
          cardList.append(f"{color} Reverse")
        else: #default 
          cardList.append(f"{color} {number}")
          cardList.append(f"{color} {number}")
      
    for wildNum in range(4):
      cardList.append("W C") # Wild card (all color allow)
      cardList.append("W +4") # wild card(drawing four cards)
  
    # shuffle deck before send the cards eachd players
    random.shuffle(cardList)
    return cardList



# asking player's number
# bot : need to ask the total number of players OR count down player names to check player's number automatically

# Shuffle deck(takes list of cards, randomizes them)
# returns randomized list
async def createPlayerDecks(playerNum): 
  playerDecks = []
  for p in range(int(playerNum)): 
    playerDecks.append([])  
  return playerDecks


async def dealCards(playerDeckLists, playerList, mainDeck):
  playerDeck = []
  #testing initialization....... need front end to get Names <@@@@@@@@@
  # Bot : need to send the each players card deck separately(personal DM)
  #       After sending, bot need to start the game with asking first    player's input
  for i in range(len(playerList)):
    name = playerList[i]
    #players.append(Player(name,["R 6", "R 6", "R 8", "W +4", "W +4", "R Reverse", "R Skip"]))
    for j in range(7):
      playerDeckLists[i].append(mainDeck[0])
      mainDeck.pop(0)

  #testDeck = ["R 6", "R 6", "R 8", "W +4", "G +2", "R Reverse", "R Skip"]
  #playerDeck.append(Player(x=name,y=testDeck))
    playerDeck.append(Player(x=name,y=playerDeckLists[i]))
    print(playerDeckLists[i])

  return playerDeck


async def draw(drawNo, p, deck):
  for i in range(drawNo):
    chosenI = random.randint(0, len(deck) - 1)
    p.deck.append(deck[chosenI])
    deck.remove(deck[chosenI])

async def isPlayable(lastPlayed, current):
  valueI = 2
  # print("@@@@@@@@@@@@@@@@@@@@@")
  # print(lastPlayed)
  # print(current)
  # print("@@@@@@@@@@@@@@@@@")
  if lastPlayed != "CLEAR":
    if lastPlayed[valueI] == '+':
      if current[2] != '+':
        return False
      valueI = 3
    if current[0] != 'W' and lastPlayed[0] != current[0] and lastPlayed[valueI] != current[valueI]: 
      return False
  return True

async def chooseWild():
  uInput = input("Color? - ")
  return uInput[0]

