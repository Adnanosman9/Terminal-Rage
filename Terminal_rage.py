import time
import random
from blessed import Terminal
from yaspin import yaspin
import emoji

# w = 12
# h = 8

# print(emoji.emojize(":red_heart:"))
# print(emoji.demojize("⬜"))

# for unicode_char, details in emoji.EMOJI_DATA.items():
    
#     shortcode = details.get('en')
#     print(f"{unicode_char} : {shortcode}")


player = emoji.emojize(":cowboy_hat_face:")
# print(player)
enemy = emoji.emojize(":ogre:")
sword = emoji.emojize(":dagger:")
# print(sword)
boom = emoji.emojize(":collision:")
wall = emoji.emojize(":brick:")
empty = emoji.emojize(":white_large_square:")

class Game:
    def __init__(self):
        self.term = Terminal()
        self.player_x = 2
        self.player_y = 2
        self.enemy_x = 7
        self.enemy_y = 5
        self.sword_x = 5
        self.sword_y = 3
        self.has_sword = False
        self.log_message = ["Use WASD to move"]

        self.running = True
        self.floor = 1

        self.start_time = time.time()
        self.traps = []
        self.gen_traps()

    def gen_traps(self):
        self.traps = []

        num_traps = min((self.floor * 2), 15)

        while len(self.traps) < num_traps:
            tx = random.randint(1, w-2)
            ty = random.randint(1, h-2)

            trap_pos = (tx, ty)

            if (trap_pos != (2, 2) and 
                trap_pos != (self.sword_x, self.sword_y) and 
                trap_pos != (self.enemy_x, self.enemy_y) and 
                trap_pos not in self.traps):
                
                self.traps.append(trap_pos)

    def move(self):
        print("hhh")

        with yaspin (text=f'going down to{self.floor + 1}') as spinner:
            time.sleep(1)
            spinner.ok("arrived")

        time.sleep(0.4)

        self.floor += 1
        self.has_sword = False
        self.player_x, self.player_y = 2,2

        self.sword_x = random.randint(2, w-2)
        self.sword_y = random.randint(2, h-2)
        self.enemy_x = random.randint(4, w-2)
        self.enemy_y = random.randint(4, h-2)

        self.gen_traps()

        print(self.term.clear,end="")

    def add_log(self,text):
        self.log_messages.append(text)
        if len(self.log_messeages) > 4:
            self.log_messages.pop(0)

    def process(self):
        with self.term.cbreak:
            key = self.term.inkey(timeout=0.1).lower()

            nx,ny = self.player_x, self.player_y
            if key =='w':ny = 1
            elif key == 's':ny = 1
            elif key == 'd': nx = 1
            elif key =='q': self.running = False
            self.log_messages = ["welcome to the quest for the missing emoji", "watch your steps for traps!", "use wasd to move.Q to quit."]
            self.running = True
            self.floor = 1

            self. start_time = time.time()
            self.traps = []

            num_traps = min(2+(self.floor*2), 15)

            while len(self.traps) < num_traps:
                tx = random.randint(1, w - 2)
                ty = random.randint(1, h - 2)

                self.traps.append((tx, ty))

# print("chekc1")

    def move(self):
        with yaspin(text = f'going to {self.floor + 1}') as spinner:
            time.sleep(0.5)

        time.sleep(0.4)

        self.floor += 1
        self.has_sword = False
        self.player_x, self.player_y = 2,2
        self.sword_x = random.randint(2, w-3)
        self.sword_y = random.randint(2, h-3)
        self.enemy_x = random.randint(4, w-2)
        self.enemy_y = random.randint(4, h-2)

        self.gen_traps()

        # print("check 2")

    def log(self, text):
        self.log_message.append(text)
        self.log_message.pop(0)

    def process(self):
        with self.term.cbreak():
            key = self.term.inkey(timeout = 0.1).lower()

            if key == 'q':
                self.running = False
                return

            moves = {
                'w' : (0, -1),
                's' : (0, 1),
                'a' : (-1, 0),
                'd' : (1, 0)
            }

            if key in moves:
                dx, dy = moves[key]
                nx = self.player_x + dx
                ny = self.player_y + dy

                if 0 < nx < w - 1 and 0 < ny < h - 1:
                    self.player_y = ny
                    self.player_x = nx

            self.collision()


    def collision(self):
        player_pos = (self.player_x, self.player_y)
        enemy_pos = (self.enemy_x, self.enemy_y)
        sword_pos = (self.sword_x, self.sword_y)

        if player_pos in self.traps:
            self.log(f"{boom} stepped on trap, +5 penaltyy")
            self.start_time -= 5
            self.player_x, self.player_y = 2,2

            return

        if player_pos == sword_pos and not self.has_sword:
            self.has_sword = True
            self.log(f"picked a dagger {sword}")


        if player_pos == enemy_pos:
            if self.has_sword:
                self.log(f"Demon killed {enemy}")
                self.enemy_x, self.enemy_y = -1,-1

                self.move()

            else:
                self.log(f"Here is a demon dude {enemy}")
                self.player_x, self.player_y = 2,2

    
    def draw(self):

        print(self.term.move_yx(0, 0), end="")

        elaps_time = int(time.time() - self.start_time)

        output = []
        for y in range(h):
            row = ""

            for x in range(w):
                pos = (x,y)

                if pos == (self.player_x, self.player_y):
                    row += player

                elif pos == (self.enemy_x, self.enemy_y):
                    row += enemy
                elif pos == (self.sword_x, self.sword_y) and not self.has_sword:
                    row += sword

                elif pos in self.traps:
                    row += boom

                elif x == 0 or x == w-1 or y == 0 or y== h-1:
                    row += wall

                else:
                    row += empty

            output.append(row)
        print("\n".join(output))

        inve = sword if self.has_sword else " "

        print("=" * 30)

        print(f" Floor: {self.floor} | ⏱️ Time: {elaps_time}s | Inv: [{inve}]")

        for msg in self.log_message:
            print(msg + self.term.clear_eol)


    def run(self):
        print(self.term.clear, end="")
        with self.term.hidden_cursor(), self.term.fullscreen():
            while self.running:
                self.draw()
                self.process()

if __name__ == "__main__":
    game = Game()
    game.run()
        

                
                
                     


# print(f"picked a dagger {sword}")

        
