from enum import Enum
from dataclasses import dataclass
import random
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

    def play(self, deck, cast=True, out=True):
        if out: print("Playing", self.name)
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
                    i.play(deck, cast=False, out=out)
                    deck.hand.remove(i)
                
        elif self.t == Type.UNTAPPER:
            deck.untaps += self.value

class Deck():
    def __init__(self, config=(), out=True):
        self.config = config
        self.out = out

    def initialize(self):
        wincons, rampers, lands, searchers, untappers = self.config
        
        self.cards = []

        for i in random.sample(((10, -1, 'Ulamog, the Ceaseless Hunger'),
                                (8, -1, 'Avacyn, Angel of Hope'),
                                (6, -1, 'Dragonlord Dromoka'),
                                (15, -1, 'Emrakul, the Aeons Torn'),
                                (6, -1, 'Carnage Tyrant'),
                                (9, -1, 'Iona, Shield of Emeria'),
                                (10, -1, 'Kozilek, Butcher of Truth'),
                                (8, -1, 'Griselbrand'),
                                (9, -1, 'Inkwell Leviathan'),
                                (8, -1, 'Akroma, Angel of Fury'),
                                (8, -1, 'Zetalpa, Primal Dawn'),
                                (9, -1, 'Void Winnower')), wincons):
            self.cards.append(Card(t=Type.WINCON, cost=i[0], value=i[1], name=i[2]))
        
        self.cards.append(Card(t=Type.RAMPER, cost=4, value=2, name="Dawn's Reflection"))
        self.cards.append(Card(t=Type.RAMPER, cost=4, value=2, name="Market Festival"))
        self.cards.append(Card(t=Type.RAMPER, cost=1, value=1, name="Utopia Sprawl"))
        self.cards.append(Card(t=Type.RAMPER, cost=2, value=1, name="Fertile Ground"))

        r = rampers - 4
        if r > 0:
            self.cards.append(Card(t=Type.RAMPER, cost=1, value=1, name="Utopia Sprawl"))
            r -= 1
        for i in range(min(3, r)):
            self.cards.append(Card(t=Type.RAMPER, cost=2, value=1, name="Fertile Ground"))
            r -= 1

        for _ in range(lands):
            self.cards.append(Card(t=Type.LAND, cost=0, value=1, name="Forest"))

        for i in random.sample(((-1, 1, 'Chord of Calling'),
                                (-1, 1, 'Wargate'),
                                (4, 2, 'Gifts Ungiven'),
                                (4, 2, 'Gifts Ungiven'),
                                (4, 2, 'Gifts Ungiven'),
                                (4, 2, 'Gifts Ungiven'),
                                (2, 1, "Eladamri's Call"),
                                (2, 1, "Eladamri's Call"),
                                (2, 1, "Eladamri's Call"),
                                (2, 1, "Eladamri's Call"),
                                (2, 1, 'Signal the Clans'),
                                (2, 1, 'Signal the Clans'),
                                (2, 1, 'Signal the Clans'),
                                (2, 1, 'Signal the Clans'),
                                (9, 2, 'Tooth and Nail'),
                                (9, 2, 'Tooth and Nail'),
                                (9, 2, 'Tooth and Nail'),
                                (9, 2, 'Tooth and Nail')), searchers):
            self.cards.append(Card(t=Type.SEARCHER, cost=i[0], value=i[1], name=i[2]))

        for i in range(4):
            self.cards.append(Card(t=Type.UNTAPPER, cost=1, value=1, name="Arbor Elf"))
        r = untappers - 6
        for name in ["Kiora's Follower", "Voyaging Satyr"]:
            self.cards.append(Card(t=Type.UNTAPPER, cost=2, value=1, name=name))
            for i in range(min(3, r)):
                self.cards.append(Card(t=Type.UNTAPPER, cost=2, value=1, name=name))
                r -= 1

        random.shuffle(self.cards)

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
                    if self.out: print("\tFound", c[i].name)
                    self.hand.append(c[i])
                    self.cards.remove(c[i])
        else:
            return c[:n]

    def take_turn(self):
        self.draw(1)
        if self.out: print([i.name for i in self.hand])
        
        self.play_card(Type.LAND, 0)
        m = self.mana

        for t in [Type.WINCON, Type.UNTAPPER, Type.RAMPER, Type.SEARCHER]:
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
                            c.play(self, out=self.out)
                            if self.out: print("\t =>", minCost.name)
                            self.cards.remove(minCost)
                            minCost.play(self, out=self.out)
                            return minCost.cost + 3
                else:
                    self.hand.remove(c)
                    c.play(self, out=self.out)
                    return c.cost
        return 0

    def play_game(self):
        self.initialize()
        self.draw(7)

        mana, wincons = [], []

        for i in range(10):
            self.take_turn()

            if self.out: print(self.mana, self.wincons, self.lands, self.untaps, self.ramps)

            mana.append(self.mana)
            wincons.append(self.wincons)

        return mana, wincons
    
def change(config):
    config[random.randrange(0, len(config))] += 1
    config[random.randrange(0, len(config))] -= 1
    return tuple(config)

base = [9, 8, 20, 11, 12]

results = {}

for i in range(10):
    b = change(base)
    d = Deck(config=b, out=False)

    ms = []
    ws = []
    first_wincons = []
    for _ in range(10000):
        m, w = d.play_game()

        ms.append(m)
        ws.append(w)
        first_wincons.append(len(w) - w[::-1].index(0) + 1)

    nums = [first_wincons.count(i) / len(first_wincons) for i in range(1, 10)]
    avg_ms = [st.mean([i[j] for i in ms]) for j in range(10)]
    avg_ws = [st.mean([i[j] for i in ws]) for j in range(10)]

    results[b] = (nums, avg_ms, avg_ws)

print(max(results, key=lambda i: results[i][nums][3]))
