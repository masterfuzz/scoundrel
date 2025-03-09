from enum import Enum
import random

HEARTS = '♥'
DIAMONDS = '♦'
SPADES = '♠'
CLUBS = '♣'

SUIT_NAMES = {
    HEARTS: 'hearts',
    DIAMONDS: 'diamonds',
    SPADES: 'spades',
    CLUBS: 'clubs',
}

class Card:
    suits = [HEARTS, DIAMONDS, SPADES, CLUBS]

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def suit_name(self):
        return SUIT_NAMES[self.suit]

    def __repr__(self):
        return f"{value_name(self.value)}{self.suit}"

    def __eq__(self, o):
        return o.suit == self.suit and o.value == self.value

def value_name(value, long=False):
    if value < 11:
        return str(value)
    name = {
        11: 'jack',
        12: 'queen',
        13: 'king',
        14: 'ace',
    }[value]
    if long:
        return name
    return name[0].upper()

def new_deck():
    return [Card(v, s) for v in range(2,15) for s in Card.suits]

class GameState(Enum):
    START = 0
    PICK_CARD = 1
    CHOOSE_WEAPON = 2
    TURN = 10
    END = 20


class Game:
    REMOVED_CARDS = [Card(v, s) for v in range(11,15) for s in ['♥', '♦']]

    def __init__(self):
        self.deck = new_deck()
        self.deck = [c for c in self.deck if c not in self.REMOVED_CARDS]
        random.shuffle(self.deck)

        self.room = []
        self.weapon: int | None = None
        self.last_monster = None
        self.health = 20
        self.has_run_already = False
        self.monster_state: int | None = None

        self.state = GameState.START

    help_text = f"""
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
        self.deal_room()

    def deal_room(self):
        if self.room:
            if len(self.deck) < 3:
                self.state = GameState.END
                return
            self.room += [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        else:
            self.room = [self.deck.pop(), self.deck.pop(), self.deck.pop(), self.deck.pop()]
        self.state = GameState.PICK_CARD

    # def show_room_choices(self):
    #     print(" ".join(map(repr, self.room)))
    #     print(f"HP: {self.health}/20")
    #     if self.weapon:
    #         print(f"Weapon: {self.weapon}{DIAMONDS} ({self.last_monster})")
    #     print("Choose card or run")

    def run_from_room(self):
        if self.state != GameState.PICK_CARD:
            raise Exception("invalid game state")

        random.shuffle(self.room)
        self.deck = self.room + self.deck
        self.room = []
        self.has_run_already = True
        self.deal_room()

    def next_turn(self):
        if self.state != GameState.TURN:
            raise Exception(f"tried to go to next turn when game state is {self.state}")
        if self.health <= 0:
            self.state = GameState.END
            return
        if len(self.room) <= 1:
            self.deal_room()
            return
        self.state = GameState.PICK_CARD

    def choose_from_room(self, idx: int):
        if self.state != GameState.PICK_CARD:
            raise Exception(f"tried to pick card when state is {self.state}")
        if idx < 1 or idx > len(self.room):
            raise Exception(f"invalid choice {idx} from {self.room}")

        card = self.room.pop(idx - 1)
        self.do_card(card)

    def do_card(self, card: Card):
        print(f"you chose {card}")
        if card.suit == HEARTS:
            self.health = min(20, self.health + card.value)
            print("you healed")
            self.state = GameState.TURN
            return
        if card.suit == DIAMONDS:
            print(f"you equiped {card}")
            self.weapon = card.value
            self.last_monster = None
            self.state = GameState.TURN
            return
        # fight!
        if self.weapon and (self.last_monster is None or self.last_monster > card.value):
            self.monster_state = card.value
            self.state = GameState.CHOOSE_WEAPON
        else:
            self.fight_with_fists(card.value)


    def fight_with_weapon(self):
        if self.monster_state is None or self.state != GameState.CHOOSE_WEAPON or self.weapon is None:
            raise Exception(f"tried to fight with weapon. gamestate: {self.state} monster_state: {self.monster_state} weapon: {self.weapon}")

        dmg = max(0, self.monster_state - self.weapon)
        print(f"you fight the monster with your weapon and take {dmg} damage!")
        self.health -= dmg
        self.last_monster = self.monster_state
        self.state = GameState.TURN
        self.monster_state = None

    def fight_with_fists(self, value):
        print(f"you fight the monster and take {value} damage!")
        self.health -= value
        self.state = GameState.TURN

