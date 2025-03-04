from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, Line
from kivy.core.window import Window

class TicTacToe(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player = 'X'
        self.game_over = False
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        # Responsive Grid Layout
        self.grid = GridLayout(cols=3, size_hint=(1, 0.85))

        for row in range(3):
            for col in range(3):
                btn = CustomButton()
                btn.bind(on_press=self.make_move_wrapper(row, col))
                self.buttons[row][col] = btn
                self.grid.add_widget(btn)

        # Adding widgets
        self.add_widget(self.grid)

    def make_move_wrapper(self, row, col):
        return lambda instance: self.make_move(row, col)

    def make_move(self, row, col):
        if not self.game_over and self.board[row][col] == '':
            self.board[row][col] = self.player
            self.buttons[row][col].text = self.player

            # Responsive Font Size (60% of Button Height)
            self.buttons[row][col].font_size = self.buttons[row][col].height * 0.6
            self.buttons[row][col].bold = True

            winner, win_positions = self.check_winner()
            if winner:
                self.game_over = True
                self.draw_winning_line(win_positions)
                self.show_winner_popup(winner)
            elif all(self.board[r][c] != '' for r in range(3) for c in range(3)):
                self.game_over = True
                self.show_winner_popup("No one (It's a Draw)")
            else:
                self.player = 'O' if self.player == 'X' else 'X'

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != '':
                return self.board[i][0], [(i, 0), (i, 1), (i, 2)]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != '':
                return self.board[0][i], [(0, i), (1, i), (2, i)]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '':
            return self.board[0][0], [(0, 0), (1, 1), (2, 2)]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '':
            return self.board[0][2], [(0, 2), (1, 1), (2, 0)]
        return None, None

    def draw_winning_line(self, win_positions):
        """Draws a bold red line over the winning positions."""
        if win_positions:
            with self.grid.canvas.after:
                Color(1, 0, 0, 1)  # Red Color
                Line(points=[
                    self.buttons[win_positions[0][0]][win_positions[0][1]].center_x,
                    self.buttons[win_positions[0][0]][win_positions[0][1]].center_y,
                    self.buttons[win_positions[2][0]][win_positions[2][1]].center_x,
                    self.buttons[win_positions[2][0]][win_positions[2][1]].center_y
                ], width=Window.width * 0.02)  # Dynamic line thickness

    def show_winner_popup(self, winner):
        """Displays a styled popup announcing the winner with a centered Restart button."""
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=15)

        # Winner message
        message = Label(text=f"{winner} Wins!", font_size=Window.width * 0.06, bold=True, color=(0, 0, 0, 1))
        popup_content.add_widget(message)

        # Restart Button (Blue, Black Bold Font, Centered)
        restart_button = Button(text="Restart", size_hint=(None, None),
                                size=(Window.width * 0.3, Window.height * 0.08),
                                background_color=(0, 0, 1, 1), color=(0, 0, 0, 1), bold=True)
        
        button_container = BoxLayout(size_hint=(1, None), height=Window.height * 0.1, padding=(10, 10))
        button_container.add_widget(restart_button)
        
        popup_content.add_widget(button_container)

        popup = Popup(title="Game Over", content=popup_content, size_hint=(0.8, 0.4))  # Scales with screen
        restart_button.bind(on_press=lambda instance: (popup.dismiss(), self.restart_game()))

        popup.open()

    def restart_game(self):
        """Resets the game state and clears the board."""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.player = 'X'
        self.game_over = False

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].text = ""

        self.grid.canvas.after.clear()  # Clear the winning line

class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 1, 1)  # Blue background
        self.bold = True
        self.size_hint = (1, 1)  # Makes buttons auto-scale
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.canvas.after.clear()
        with self.canvas.after:
            Color(1, 0, 0, 1)  # Red color for border
            Line(rectangle=(self.x, self.y, self.width, self.height), width=Window.width * 0.02)  # Dynamic thickness

class TicTacToeApp(App):
    def build(self):
        Window.size = (360, 640)  # Set default mobile-friendly size
        return TicTacToe()

if __name__ == '__main__':
    TicTacToeApp().run()
