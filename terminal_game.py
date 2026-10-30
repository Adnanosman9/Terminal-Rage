import os
import random
import sys
import time
import emoji


WIDTH = 12
HEIGHT = 8


PLAYER = emoji.emojize(":cowboy_hat_face:")
ENEMY = emoji.emojize(":ogre:")
SWORD = emoji.emojize(":dagger:")
TRAP = emoji.emojize(":collision:")
WALL = emoji.emojize(":brick:")
EMPTY = emoji.emojize(":white_large_square:")


def get_keypress():
    import msvcrt
    return msvcrt.getch().decode("utf-8").lower()


floor = 1
player_x, player_y = 2, 2
sword_x, sword_y = 5, 3
enemy_x, enemy_y = 7, 5
has_sword = False

start_time = time.time()
time_penalty = 0
log_message = "Use WASD to move instantly. Q to quit."


traps = []
for i in range(2):
    tx = random.randint(1, WIDTH - 2)
    ty = random.randint(1, HEIGHT - 2)
    traps.append((tx, ty))


running = True
while running:
    
    os.system("cls" if os.name == "nt" else "clear")


    for y in range(HEIGHT):
        row_cells = ""
        for x in range(WIDTH):
            if x == player_x and y == player_y:
                row_cells += PLAYER
            elif x == enemy_x and y == enemy_y:
                row_cells += ENEMY
            elif x == sword_x and y == sword_y and not has_sword:
                row_cells += SWORD
            elif (x, y) in traps:
                row_cells += TRAP
            elif x == 0 or x == WIDTH - 1 or y == 0 or y == HEIGHT - 1:
                row_cells += WALL
            else:
                row_cells += EMPTY
        print(row_cells)


    elapsed_time = int(time.time() - start_time) + time_penalty
    inventory = SWORD if has_sword else "Empty"

    print("=" * 35)
    print(f" Floor: {floor} | ⏱️ Time: {elapsed_time}s | Inv: [{inventory}]")
    print("=" * 35)
    print(log_message)


    move = get_keypress()


    if move == "q":
        running = False
        continue
    elif move == "w":
        player_y -= 1
    elif move == "s":
        player_y += 1
    elif move == "a":
        player_x -= 1
    elif move == "d":
        player_x += 1
    else:
        continue


    if player_x < 1:
        player_x = 1
    if player_x > WIDTH - 2:
        player_x = WIDTH - 2
    if player_y < 1:
        player_y = 1
    if player_y > HEIGHT - 2:
        player_y = HEIGHT - 2


    if (player_x, player_y) in traps:
        log_message = "%5 penalty for trap"
        time_penalty += 5
        player_x, player_y = 2, 2

    elif player_x == sword_x and player_y == sword_y and not has_sword:
        has_sword = True
        log_message = f"{SWORD} sword in INV"

    elif player_x == enemy_x and player_y == enemy_y:
        if has_sword:
            log_message = f"✨ Level Clear! {floor + 1}..."
            floor += 1
            has_sword = False

            player_x, player_y = 2, 2
            sword_x = random.randint(2, WIDTH - 2)
            sword_y = random.randint(2, HEIGHT - 2)
            enemy_x = random.randint(4, WIDTH - 2)
            enemy_y = random.randint(4, HEIGHT - 2)

            traps = []
            num_traps = min(floor * 2, 12)
            while len(traps) < num_traps:
                tx = random.randint(1, WIDTH - 2)
                ty = random.randint(1, HEIGHT - 2)

                
                if (tx, ty) not in traps and (tx, ty) != (sword_x, sword_y) and (tx, ty) != (2, 2) and (tx, ty) != (enemy_x, enemy_y):
                    traps.append((tx, ty))
    
            log_message = f"{ENEMY} Dead! Pick sword first"
            player_x, player_y = 2, 2


