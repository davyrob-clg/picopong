from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import machine
import time
import random
import os

# -----------------------------
# Display Setup
# -----------------------------
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)
WIDTH, HEIGHT = display.get_bounds()

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

# -----------------------------
# Buttons
# -----------------------------
button_a = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)  # up
button_b = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)  # down

# -----------------------------
# Game State
# -----------------------------
paddle_w = 5
paddle_h = 40

player_x = 10
player_y = HEIGHT // 2 - paddle_h // 2
player_speed = 4

ai_x = WIDTH - 10 - paddle_w
ai_y = HEIGHT // 2 - paddle_h // 2
ai_speed = 2  # difficulty

ball_size = 5
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = -5
ball_dy = 5

score = 0
highscore = 0

# -----------------------------
# High Score Load/Save
# -----------------------------
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_highscore(value):
    with open("highscore.txt", "w") as f:
        f.write(str(value))

highscore = load_highscore()

# -----------------------------
# Helpers
# -----------------------------
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-2, -3])
    ball_dy = random.choice([-2, -1, 1, 2])
    ball_dx = 5;
    ball_dy=-5;

def draw():
    display.set_pen(BLACK)
    display.clear()

    # Player paddle
    display.set_pen(WHITE)
    display.rectangle(player_x, player_y, paddle_w, paddle_h)

    # AI paddle
    display.rectangle(ai_x, ai_y, paddle_w, paddle_h)

    # Ball
    display.rectangle(ball_x, ball_y, ball_size, ball_size)

    # Score
    display.text(f"Score: {score}", 5, 5, scale=1)
    display.text(f"High: {highscore}", WIDTH - 80, 5, scale=1)

    display.update()

def game_over_flash():
    display.set_pen(WHITE)
    display.clear()
    display.text("GAME OVER", WIDTH//2 - 40, HEIGHT//2 - 10, scale=2)
    display.update()
    time.sleep(1)

# -----------------------------
# Main Loop
# -----------------------------
while True:

    # -------------------------
    # Player movement
    # -------------------------
    if not button_a.value():
        player_y -= player_speed
    if not button_b.value():
        player_y += player_speed

    player_y = max(0, min(HEIGHT - paddle_h, player_y))

    # -------------------------
    # AI movement
    # -------------------------
    if ai_y + paddle_h/2 < ball_y:
        ai_y += ai_speed
    elif ai_y + paddle_h/2 > ball_y:
        ai_y -= ai_speed

    ai_y = max(0, min(HEIGHT - paddle_h, ai_y))

    # -------------------------
    # Ball movement
    # -------------------------
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce top/bottom
    if ball_y <= 0 or ball_y + ball_size >= HEIGHT:
        ball_dy = -ball_dy

    # Player collision
    if (player_x < ball_x < player_x + paddle_w and
        player_y < ball_y + ball_size and
        ball_y < player_y + paddle_h):
        
        ball_dx = -ball_dx
        score += 1

    # AI collision
    if (ai_x < ball_x + ball_size < ai_x + paddle_w and
        ai_y < ball_y + ball_size and
        ball_y < ai_y + paddle_h):
        ball_dx = -ball_dx

    # -------------------------
    # Missed ball → Game Over
    # -------------------------
    if ball_x <= 0:
        if score > highscore:
            highscore = score
            save_highscore(highscore)

        game_over_flash()
        score = 0
        reset_ball()

    # Bounce off right wall if AI misses (rare)
    if ball_x + ball_size >= WIDTH:
        ball_dx = -ball_dx

    draw()
    time.sleep(0.01)
