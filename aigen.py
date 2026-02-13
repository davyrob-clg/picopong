from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import time

# --- Display setup ---
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)
WIDTH, HEIGHT = display.get_bounds()
display.set_backlight(1.0)

# --- Controls (A/B buttons on the Display Pack) ---
button_up = Button(12)
button_down = Button(13)

# --- Game objects ---
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
paddle_x = 10
paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle_speed = 4

BALL_SIZE = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 3
ball_dy = 3

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

# --- Game loop ---
while True:
    # Paddle movement
    if button_up.read() and paddle_y > 0:
        paddle_y -= paddle_speed
    if button_down.read() and paddle_y < HEIGHT - PADDLE_HEIGHT:
        paddle_y += paddle_speed

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce off top/bottom
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy = -ball_dy

    # Paddle collision
    if (paddle_x < ball_x < paddle_x + PADDLE_WIDTH and
        paddle_y < ball_y < paddle_y + PADDLE_HEIGHT):
        ball_dx = -ball_dx

    # Reset if ball goes off left side
    if ball_x < 0:
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = -ball_dx

    # Clear screen
    display.set_pen(BLACK)
    display.clear()

    # Draw paddle
    display.set_pen(WHITE)
    display.rectangle(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Draw ball
    display.rectangle(ball_x, ball_y, BALL_SIZE, BALL_SIZE)

    # Update display
    display.update()

    time.sleep(0.01)
