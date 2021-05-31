def buildDeck():
    cardList = [] #stores cards
    colors = ["Red", "Green", "Blue", "Yellow"]

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
      cardList.append("Wild Card")
      cardList.append("Wild Card +4")

    print(cardList)


buildDeck()
