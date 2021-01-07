from enum import Enum
from dataclasses import dataclass

class Type(Enum):
    WINCON = 0
    RAMPER = 1
    LAND = 2
    SEARCHER = 3
    UNTAPPER = 4

class Card(dataclass):
    t: Type
    cost: int
    value: int

class Deck():
    def __init__(self):
        self.cards = []

        self.cards.append(t=Type.WINCON, cost=8, value=-1, name="Avacyn, Angel of Hope")
        self.cards.append(t=Type.WINCON, cost=6, value=-1, name="Carnage Tyrant")
        self.cards.append(t=Type.WINCON, cost=6, value=-1, name="Dragonlord Dromoka")
        self.cards.append(t=Type.WINCON, cost=15, value=-1, name="Emrakul, the Aeons Torn")
        self.cards.append(t=Type.WINCON, cost=8, value=-1, name="Griselbrand")
        self.cards.append(t=Type.WINCON, cost=9, value=-1, name="Inkwell Leviathan")
        self.cards.append(t=Type.WINCON, cost=9, value=-1, name="Iona, Shield of Emeria")
        self.cards.append(t=Type.WINCON, cost=10, value=-1, name="Kozilek, Butcher of Truth")
        self.cards.append(t=Type.WINCON, cost=10, value=-1, name="Ulamog, the Ceaseless Hunger")
        
        self.cards.append(t=Type.WINCON, cost=4, value=2, name="Dawn's Reflection")
        self.cards.append(t=Type.WINCON, cost=4, value=2, name="Market Festival")
        self.cards.append(t=Type.WINCON, cost=1, value=1, name="Utopia Sprawl")
        self.cards.append(t=Type.WINCON, cost=1, value=1, name="Utopia Sprawl")
        self.cards.append(t=Type.WINCON, cost=2, value=1, name="Fertile Ground")
        self.cards.append(t=Type.WINCON, cost=2, value=1, name="Fertile Ground")
        self.cards.append(t=Type.WINCON, cost=2, value=1, name="Fertile Ground")
        self.cards.append(t=Type.WINCON, cost=2, value=1, name="Fertile Ground")

        for _ in range(20): # todo
            self.cards.append(t=Type.LAND, cost=0, value=1, name="Forest")

        self.cards.append(t=Type.SEARCHER, cost=-1, value=1, name="Chord of Calling")
        self.cards.append(t=Type.SEARCHER, cost=-1, value=1, name="Wargate")
        self.cards.append(t=Type.SEARCHER, cost=4, value=2, name="Gifts Ungiven")
        self.cards.append(t=Type.SEARCHER, cost=4, value=2, name="Gifts Ungiven")
        self.cards.append(t=Type.SEARCHER, cost=4, value=2, name="Gifts Ungiven")
        self.cards.append(t=Type.SEARCHER, cost=4, value=2, name="Gifts Ungiven")
        self.cards.append(t=Type.SEARCHER, cost=2, value=1, name="Eladamri's Call")
        self.cards.append(t=Type.SEARCHER, cost=2, value=1, name="Signal the Clans")
        self.cards.append(t=Type.SEARCHER, cost=2, value=1, name="Signal the Clans")
        self.cards.append(t=Type.SEARCHER, cost=9, value=2, name="Tooth and Nail")
        self.cards.append(t=Type.SEARCHER, cost=9, value=2, name="Tooth and Nail")

        for i in range(4):
            self.cards.append(t=Type.UNTAPPER, cost=1, value=1, name="Arbor Elf")
            self.cards.append(t=Type.UNTAPPER, cost=2, value=1, name="Kiora's Follower")
            self.cards.append(t=Type.UNTAPPER, cost=2, value=1, name="Voyaging Satyr")

        self.wincons = 0
        self.lands = 0
        self.untaps = 0
        self.ramps = 0

        self.turn = 0

    @property
    def mana(self):
        return self.lands - 1 + (self.ramps + 1) * (self.untaps + 1)

    def take_turn(self):
        ...
