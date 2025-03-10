from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from scoundrel import DIAMONDS, Card, Game, GameState
from kivy.factory import Factory
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label


class ScoundrelGame(GridLayout):

    def __init__(self):
        super().__init__()
        self.cards: list[Image] = [self.ids[f"c{i}"] for i in range(1,5)]
        self.run_button: Button = self.ids["run_away"]
        self.weapon_image: Image = self.ids["weapon"]
        self.last_monster_image: Image = self.ids["last_monster"]
        self.health_label: Label = self.ids["health"]
        self.deck_label: Label = self.ids["deck"]
        self.restart_game()

    def card(self, idx: int):
        self.g.choose_from_room(idx)
        self.transition()

    def run_away(self):
        self.g.run_from_room()
        self.transition()

    def set_status_labels(self):
        self.health_label.text = f"{max(0, self.g.health)}/20"
        if self.g.weapon:
            self.weapon_image.source = self.card_image(Card(self.g.weapon, DIAMONDS))
            if self.g.last_monster:
                self.last_monster_image.source = self.card_image(self.g.last_monster)
            else:
                self.last_monster_image.source = "images/cards/card-blank.png"
        else:
            self.weapon_image.source = "images/cards/card-blank.png"
            self.last_monster_image.source = "images/cards/card-blank.png"
        self.deck_label.text = f"{len(self.g.deck)}"

    def restart_game(self):
        self.g = Game()
        self.g.start()
        self.transition()

    def card_image(self, card: Card):
        value = (card.value - 1) % 13 + 1
        return f"./images/cards/card-{card.suit_name()}-{value}.png"

    def transition(self):
        match self.g.state:
            case GameState.START:
                print('start')
                for i in range(len(self.g.room)):
                    self.cards[i].disabled = False
                    self.cards[i].source = self.card_image(self.g.room[i])
            case GameState.CHOOSE_WEAPON:
                print('choose weapon')
                # todo allow choice
                self.g.fight_with_weapon()
                self.transition()
            case GameState.PICK_CARD:
                print('pick card')
                self.set_status_labels()
                self.run_button.disabled = not self.g.can_run()
                for c in self.cards:
                    c.disabled = True
                    c.source = "./images/cards/card-blank.png"
                for i in range(len(self.g.room)):
                    self.cards[i].disabled = False
                    self.cards[i].source = self.card_image(self.g.room[i])
                    # self.cards[i].text = repr(self.g.room[i])
            case GameState.TURN:
                print('turn')
                self.set_status_labels()
                # for now just call next turn and then transition
                self.g.next_turn()
                self.transition()

            case GameState.END:
                for i in range(4):
                    self.cards[i].disabled = True
                print('end')
                game_end_popup: Popup = Factory.GameEndPopup()
                game_end_popup.bind(on_dismiss=(lambda _: self.restart_game()))
                game_end_popup.open()



class ScoundrelApp(App):
    def build(self):
        return ScoundrelGame()

    help_text = Game.help_text


if __name__ == '__main__':
    ScoundrelApp().run()
