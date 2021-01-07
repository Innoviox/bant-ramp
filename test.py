from enum import Enum
from dataclasses import dataclass
from random import shuffle
from matplotlib import pyplot as plt
import statistics as st

class Type(Enum):
    WINCON = 0
    RAMPER = 1
    LAND = 2
    SEARCHER = 3
    UNTAPPER = 4

@dataclass
class Card:
    t: Type
    cost: int
    value: int
    name: str

    def play(self, deck, cast=True):
        # print("Playing", self.name)
        if self.t == Type.WINCON:
            deck.wincons += 1
            if self.name == "Kozilek, Butcher of Truth" and cast:
                deck.draw(4)
        elif self.t == Type.RAMPER:
            deck.ramps += self.value
        elif self.t == Type.LAND:
            deck.lands += 1
        elif self.t == Type.SEARCHER:
            if self.name in ["Chord of Calling", "Wargate"]:
                # todo
                ...
            elif self.name == "Gifts Ungiven":
                toFind = min([deck.wincons, deck.untaps, deck.ramps])
                if toFind == deck.untaps:
                    deck.search(Type.UNTAPPER, self.value)
                elif toFind == deck.ramps:
                    deck.search(Type.RAMPER, self.value)
                else:
                    deck.search(Type.WINCON, self.value)
            elif self.name in ["Eladamri's Call", "Signal the Clans"]:
                toFind = min([deck.wincons, deck.untaps])
                if toFind == deck.untaps:
                    deck.search(Type.UNTAPPER, self.value)
                else:
                    deck.search(Type.WINCON, self.value)
            elif self.name == "Tooth and Nail":
                # todo
                deck.search(Type.WINCON, self.value)
                cards = [i for i in deck.hand if i.t == Type.WINCON]
                for i in cards[:2]:
                    i.play(deck, False)
                    deck.hand.remove(i)
                
        elif self.t == Type.UNTAPPER:
            deck.untaps += self.value

class Deck():
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.cards = []

        self.cards.append(Card(t=Type.WINCON, cost=8, value=-1, name="Avacyn, Angel of Hope"))
        self.cards.append(Card(t=Type.WINCON, cost=6, value=-1, name="Carnage Tyrant"))
        self.cards.append(Card(t=Type.WINCON, cost=6, value=-1, name="Dragonlord Dromoka"))
        self.cards.append(Card(t=Type.WINCON, cost=15, value=-1, name="Emrakul, the Aeons Torn"))
        self.cards.append(Card(t=Type.WINCON, cost=8, value=-1, name="Griselbrand"))
        self.cards.append(Card(t=Type.WINCON, cost=9, value=-1, name="Inkwell Leviathan"))
        self.cards.append(Card(t=Type.WINCON, cost=9, value=-1, name="Iona, Shield of Emeria"))
        self.cards.append(Card(t=Type.WINCON, cost=10, value=-1, name="Kozilek, Butcher of Truth"))
        self.cards.append(Card(t=Type.WINCON, cost=10, value=-1, name="Ulamog, the Ceaseless Hunger"))
        
        self.cards.append(Card(t=Type.RAMPER, cost=4, value=2, name="Dawn's Reflection"))
        self.cards.append(Card(t=Type.RAMPER, cost=4, value=2, name="Market Festival"))
        self.cards.append(Card(t=Type.RAMPER, cost=1, value=1, name="Utopia Sprawl"))
        self.cards.append(Card(t=Type.RAMPER, cost=1, value=1, name="Utopia Sprawl"))
        self.cards.append(Card(t=Type.RAMPER, cost=2, value=1, name="Fertile Ground"))
        self.cards.append(Card(t=Type.RAMPER, cost=2, value=1, name="Fertile Ground"))
        self.cards.append(Card(t=Type.RAMPER, cost=2, value=1, name="Fertile Ground"))
        self.cards.append(Card(t=Type.RAMPER, cost=2, value=1, name="Fertile Ground"))

        for _ in range(20): # todo
            self.cards.append(Card(t=Type.LAND, cost=0, value=1, name="Forest"))

        self.cards.append(Card(t=Type.SEARCHER, cost=-1, value=1, name="Chord of Calling"))
        self.cards.append(Card(t=Type.SEARCHER, cost=-1, value=1, name="Wargate"))
        self.cards.append(Card(t=Type.SEARCHER, cost=4, value=2, name="Gifts Ungiven"))
        self.cards.append(Card(t=Type.SEARCHER, cost=4, value=2, name="Gifts Ungiven"))
        self.cards.append(Card(t=Type.SEARCHER, cost=4, value=2, name="Gifts Ungiven"))
        self.cards.append(Card(t=Type.SEARCHER, cost=4, value=2, name="Gifts Ungiven"))
        self.cards.append(Card(t=Type.SEARCHER, cost=2, value=1, name="Eladamri's Call"))
        self.cards.append(Card(t=Type.SEARCHER, cost=2, value=1, name="Signal the Clans"))
        self.cards.append(Card(t=Type.SEARCHER, cost=2, value=1, name="Signal the Clans"))
        self.cards.append(Card(t=Type.SEARCHER, cost=9, value=2, name="Tooth and Nail"))
        self.cards.append(Card(t=Type.SEARCHER, cost=9, value=2, name="Tooth and Nail"))

        for i in range(4):
            self.cards.append(Card(t=Type.UNTAPPER, cost=1, value=1, name="Arbor Elf"))
            self.cards.append(Card(t=Type.UNTAPPER, cost=2, value=1, name="Kiora's Follower"))
            self.cards.append(Card(t=Type.UNTAPPER, cost=2, value=1, name="Voyaging Satyr"))

        shuffle(self.cards)

        self.wincons = 0
        self.lands = 0
        self.untaps = 0
        self.ramps = 0

        self.turn = 0
        
        self.hand = []

    @property
    def mana(self):
        return self.lands - 1 + (self.ramps + 1) * (self.untaps + 1)


    def draw(self, n):
        for _ in range(n):
            self.hand.append(self.cards.pop())

    def search(self, t, n, add=True):
        c = [i for i in self.cards if i.t == t]
        if add:
            for i in range(n):
                if i < len(c):
                    # print("\tFound", c[i].name)
                    self.hand.append(c[i])
                    self.cards.remove(c[i])
        else:
            return c[:n]

    def take_turn(self):
        self.draw(1)
        # print([i.name for i in self.hand])
        
        self.play_card(Type.LAND, 0)
        m = self.mana

        for t in [Type.UNTAPPER, Type.RAMPER, Type.WINCON, Type.SEARCHER]:
            c = -1
            while c != 0 and m > 0:
                c = self.play_card(t, m)
                m -= c        

    def play_card(self, t, m):
        cards = [i for i in self.hand if i.t == t and i.cost <= m]
        if len(cards) > 0:
            for c in cards:
                if c.name in ["Chord of Calling", "Wargate"]:
                    toFind = min([self.wincons, self.untaps])
                    if toFind == self.untaps and self.mana < 10:
                        found = [i for i in self.cards if i.t == Type.UNTAPPER]
                    else:
                        found = [i for i in self.cards if i.t == Type.WINCON]
                    if found:
                        minCost = min(found, key=lambda i: i.cost)
                        if minCost.cost + 3 <= m:
                            self.hand.remove(c)
                            c.play(self)
                            # print("\t =>", minCost.name)
                            self.cards.remove(minCost)
                            minCost.play(self)
                            return minCost.cost + 3
                else:
                    self.hand.remove(c)
                    c.play(self)
                    return c.cost
        return 0

    def play_game(self):
        self.initialize()
        self.draw(7)

        mana, wincons = [], []

        for i in range(10):
            self.take_turn()

            mana.append(self.mana)
            wincons.append(self.wincons)

        return mana, wincons
    
        

d = Deck()

ms = []
ws = []
for _ in range(200):
    m, w = d.play_game()
    ms.append(m)
    ws.append(w)

    # plt.plot(range(0, 10), m)

# plt.show()

avgs = [st.mean([i[j] for i in ms]) for j in range(10)]
print(avgs)

avgs = [st.mean([i[j] for i in ws]) for j in range(10)]
print(avgs)
