import math
import arcade
import time

s_w, s_h = arcade.get_display_size()


class GameWindow(arcade.Window):
    def __init__(self, screen_width, screen_height, title):
        super(GameWindow, self).__init__(screen_width, screen_height, title, True, True)
        arcade.set_background_color(arcade.color.WHITE)
        self.is_positions_chosen = False
        self.is_first_player_choose = False
        self.is_first_player_turn = True
        self.screen_mid = screen_width / 2
        self.atack_radius = int(screen_height / 60)
        self.tank_count = 10
        self.tank_radius = int(screen_height / 60)
        self.player1_tank_count = 0
        self.player2_tank_count = 0
        self.player1_tanks = []
        self.player2_tanks = []
        self.atack_coord = None
        self.atack_time = None
        self.atack_duration = 0.1
        self.check_time = False
        self.title_height = screen_height / 10
        self.is_game_ended = False
        self.is_first_player_winner = False

    def setup(self):
        self.is_positions_chosen = False
        self.is_first_player_choose = False
        self.is_first_player_turn = True
        self.player1_tank_count = 0
        self.player2_tank_count = 0
        self.player1_tanks = []
        self.player2_tanks = []
        self.atack_coord = None
        self.atack_time = None
        self.atack_duration = 0.1
        self.check_time = False
        self.is_game_ended = False
        self.is_first_player_winner = False

    def on_draw(self):
        arcade.start_render()
        arcade.draw_line(s_w / 2, 0, s_w / 2, s_h, arcade.color.BLACK, 3)
        arcade.draw_rectangle_filled(s_w / 2, s_h - self.title_height / 2, s_w, self.title_height, arcade.color.BLUE)
        for tank in self.player1_tanks:
            arcade.draw_circle_filled(tank[0], tank[1], self.tank_radius, arcade.color.BLACK)

        for tank in self.player2_tanks:
            arcade.draw_circle_filled(tank[0], tank[1], self.tank_radius, arcade.color.BLACK)

        if self.atack_coord is not None:
            arcade.draw_circle_filled(self.atack_coord[0], self.atack_coord[1], self.atack_radius, arcade.color.RED)

        self.draw_title()

    def on_update(self, delta_time: float):
        if self.atack_coord is not None and time.time() - self.atack_time >= self.atack_duration:
            self.atack_coord = None

        self.check_atacks_accurancy()
        if self.is_positions_chosen:
            self.is_game_ended = self.check_is_winner_exists()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if not self.is_game_ended:
            if not self.is_positions_chosen:
                if not self.is_first_player_choose and x < self.screen_mid - self.tank_radius and\
                        self.tank_radius < y < s_h - self.title_height - self.tank_radius:
                    self.player1_tanks.append([x, y])
                    self.player1_tank_count += 1
                    if self.player1_tank_count == 10:
                        self.is_first_player_choose = True

                elif self.is_first_player_choose and x > self.screen_mid + self.tank_radius and\
                        self.tank_radius < y < s_h - self.title_height - self.tank_radius:
                    self.player2_tanks.append([x, y])
                    self.player2_tank_count += 1
                    if self.player2_tank_count == 10:
                        self.is_positions_chosen = True

            else:
                if self.atack_coord is None:
                    if self.is_first_player_turn and x < self.screen_mid - self.tank_radius:
                        self.atack_coord = [2 * self.screen_mid - x, y]
                        self.atack_time = time.time()
                        self.check_time = True
                        self.is_first_player_turn = False

                    elif not self.is_first_player_turn and x > self.screen_mid + self.tank_radius:
                        self.atack_coord = [2 * self.screen_mid - x, y]
                        self.atack_time = time.time()
                        self.check_time = True
                        self.is_first_player_turn = True

        else:
            self.setup()

    def draw_title(self):
        if not self.is_positions_chosen:
            text = "Choose your tanks positions"
            if self.is_first_player_choose:
                pos_x = s_w * 0.99
                anchor = "right"
            else:
                pos_x = 0.01 * s_w
                anchor = "left"
        else:
            text = "Game"
            if not self.is_first_player_turn:
                pos_x = s_w * 0.99
                anchor = "right"
            else:
                pos_x = 0.01 * s_w
                anchor = "left"

        if self.is_game_ended:
            text = "K.O."
            if self.is_first_player_winner:
                winner = 1
            else:
                winner = 2

            arcade.draw_text(f"Player{winner} is Winner", s_w / 2, s_h / 2, arcade.color.BLACK, s_h / 10,
                             anchor_x="center")
        arcade.draw_text(text, s_w / 2, s_h, arcade.color.BLACK, s_h / 20,
                         anchor_x="center", anchor_y="top")
        if not self.is_game_ended:
            arcade.draw_text("Your turn", pos_x, s_h - self.title_height, arcade.color.BLACK, s_h / 30,
                             anchor_x=anchor, anchor_y="bottom")

    def check_atacks_accurancy(self):
        if self.check_time and self.atack_coord is not None:
            if self.atack_coord[0] > self.screen_mid:
                tank_list = self.player2_tanks
                player = 2
            else:
                tank_list = self.player1_tanks
                player = 1

            for tank in tank_list:
                distance = math.sqrt((tank[0] - self.atack_coord[0]) ** 2 + (tank[1] - self.atack_coord[1]) ** 2)
                if distance < self.tank_radius + self.atack_radius:
                    tank_list.remove(tank)
                    if player == 1:
                        self.player1_tank_count -= 1
                    else:
                        self.player2_tank_count -= 1

            self.check_time = False

    def check_is_winner_exists(self):
        if self.player2_tank_count <= 0:
            self.is_first_player_winner = True
            return True
        if self.player1_tank_count <= 0:
            self.is_first_player_winner = False
            return True

        return False


window = GameWindow(s_w, s_h, "Tanks")
window.setup()
arcade.set_window(window)
arcade.run()
