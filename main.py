from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from scoundrel import Game, GameState

class ScoundrelGame(GridLayout):

    def __init__(self):
        super().__init__()
        self.g = Game()
        self.g.start()
        self.cards = [self.ids[f"c{i}"] for i in range(1,5)]
        self.transition()

    def card(self, idx: int):
        self.g.choose_from_room(idx)
        self.transition()

    def set_status_labels(self):
        self.ids['health'].text = f"{self.g.health}/20"
        self.ids['weapon'].text = f"{self.g.weapon}" if self.g.weapon else "None"
        self.ids['deck'].text = f"{len(self.g.deck)}"

    def transition(self):
        match self.g.state:
            case GameState.START:
                print('start')
                for i in range(len(self.g.room)):
                    self.cards[i].disabled = False
                    self.cards[i].text = repr(self.g.room[i])
            case GameState.CHOOSE_WEAPON:
                print('choose weapon')
                # todo allow choice
                self.g.fight_with_weapon()
                self.transition()
            case GameState.PICK_CARD:
                print('pick card')
                for c in self.cards:
                    c.disabled = True
                for i in range(len(self.g.room)):
                    self.cards[i].disabled = False
                    self.cards[i].text = repr(self.g.room[i])
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



class ScoundrelApp(App):
    def build(self):
        return ScoundrelGame()


if __name__ == '__main__':
    ScoundrelApp().run()
