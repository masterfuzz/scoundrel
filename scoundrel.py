from kivy.app import App
# from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
import random

HEARTS = '♥'
DIAMONDS = '♦'
SPADES = '♠'
CLUBS = '♣'

class Card:
    suits = ['♥', '♦', '♠', '♣']

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{value_name(self.value)}{self.suit}"

    def __eq__(self, o):
        return o.suit == self.suit and o.value == self.value

def value_name(value):
    if value < 11:
        return str(value)
    return {
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A',
    }[value]

def new_deck():
    return [Card(v, s) for v in range(2,15) for s in Card.suits]

class Game:
    REMOVED_CARDS = [Card(v, s) for v in range(11,15) for s in ['♥', '♦']]

    def __init__(self):
        self.deck = new_deck()
        self.deck = [c for c in self.deck if c not in self.REMOVED_CARDS]
        random.shuffle(self.deck)

        self.room = []
        self.weapon = None
        self.last_monster = None
        self.health = 20
        self.has_run_already = False

    def help(self):
        return f"""
              == SCOUNDREL SOLITARE CARD GAME ==
              Each "room" of the dungeon you must select a card. Its behaviour matches its suit
              You start with 20 life and you must clear every room of the dungeon.

              {CLUBS}/{SPADES}  A monster! If you attack it, it will deal its value in damage to you
              {HEARTS}    A health potion! You'll immediately heal its value
              {DIAMONDS}    A weapon! You'll equip this weapon (replacing any existing one)

              Weapons:
              When you choose to fight with your weapon, you subtract its value from the monster's damage.
              However, you can only use the weapon to fight monsters which are weaker than the last monster you fought with that weapon.

              Running away:
              You can choose to run from a room, placing the room cards on the bottom of the deck and drawing four new ones.
              You cannot run twice in a row!

              Good luck!
              """

    def start(self):
        print(self.help())
        if self.deal_room():
            print()
            print('congratulations! you cleared the dungeon!')
        else:
            print()
            print('you have perished :(')

    def deal_room(self):
        if self.room:
            if len(self.deck) < 3:
                return True
            self.room += [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        else:
            self.room = [self.deck.pop(), self.deck.pop(), self.deck.pop(), self.deck.pop()]
        return self.choose_from_room()

    def show_room_choices(self):
        print(" ".join(map(repr, self.room)))
        print(f"HP: {self.health}/20")
        if self.weapon:
            print(f"Weapon: {self.weapon}{DIAMONDS} ({self.last_monster})")
        print("Choose card or run")

    def run_from_room(self):
        random.shuffle(self.room)
        self.deck = self.room + self.deck
        self.room = []
        self.has_run_already = True
        return self.deal_room()

    def choose_from_room(self):
        self.show_room_choices()
        choice = input('> ')
        if not choice:
            return self.choose_from_room()
        if choice[0] == 'q':
            return False
        if choice[0] == 'r':
            if self.has_run_already:
                print("you already ran!")
                return self.choose_from_room()
            return self.run_from_room()
        c = int(choice[0])
        if c < 1 or c > 4:
            print('invalid choice')
            return self.choose_from_room()
        card = self.room.pop(c - 1)
        self.do_card(card)
        if self.health <= 0:
            return False

        if len(self.room) == 1:
            self.has_run_already = False
            return self.deal_room()
        return self.choose_from_room()

    def do_card(self, card: Card):
        print(f"you chose {card}")
        if card.suit == HEARTS:
            self.health = min(20, self.health + card.value)
            print("you healed")
            return
        if card.suit == DIAMONDS:
            print(f"you equiped {card}")
            self.weapon = card.value
            self.last_monster = None
            return
        # fight!
        # TODO: choice
        if self.weapon and (self.last_monster is None or self.last_monster > card.value):
            w = input('Fight with weapon? ')
            if w == 'y':
                self.fight_with_weapon(card.value)
            else:
                self.fight_with_fists(card.value)
        else:
            self.fight_with_fists(card.value)

        # if self.weapon:
        #     if self.last_monster is None:
        #         self.fight_with_weapon(card.value)
        #     elif self.last_monster > card.value:
        #         self.fight_with_weapon(card.value)
        #     self.fight_with_fists(card.value)
        # else:
        #     self.fight_with_fists(card.value)

    def fight_with_weapon(self, value):
        dmg = max(0, value - self.weapon)
        print(f"you fight the monster with your weapon and take {dmg} damage!")
        self.health -= dmg
        self.last_monster = value

    def fight_with_fists(self, value):
        print(f"you fight the monster and take {value} damage!")
        self.health -= value

class ScoundrelGame(GridLayout):
    pass



class ScoundrelApp(App):
    def build(self):
        return ScoundrelGame()


if __name__ == '__main__':
    ScoundrelApp().run()
