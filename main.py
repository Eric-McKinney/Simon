import pygame
import random
from time import sleep


WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simon")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GREEN = (0, 153, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Light colors for when pressed
L_GREEN = (51, 255, 51)
L_RED = (255, 153, 153)
L_YELLOW = (255, 255, 153)
L_BLUE = (153, 153, 255)


def save_score(score):
    with open("high_score", "w") as f:
        f.write(str(score))


def draw_window():
    WIN.fill(WHITE)

    # Colored Quadrants
    pygame.draw.rect(WIN, rect=(0, 0, WIDTH/2, HEIGHT/2), color=GREEN)
    pygame.draw.rect(WIN, rect=(WIDTH/2, 0, WIDTH/2, HEIGHT/2), color=RED)
    pygame.draw.rect(WIN, rect=(0, HEIGHT/2, WIDTH/2, HEIGHT/2), color=YELLOW)
    pygame.draw.rect(WIN, rect=(WIDTH/2, HEIGHT/2, WIDTH/2, HEIGHT/2), color=BLUE)

    # Grid Lines
    pygame.draw.line(WIN, color=BLACK, start_pos=(0, HEIGHT / 2), end_pos=(WIDTH, HEIGHT / 2), width=2)
    pygame.draw.line(WIN, color=BLACK, start_pos=(WIDTH/2, 0), end_pos=(WIDTH/2, HEIGHT), width=2)

    pygame.display.update()


def light_up(color):
    colors = {
        "G": {"top": 0,            "left": 0,           "lit_color": L_GREEN},
        "R": {"top": 0,            "left": WIDTH/2 + 2, "lit_color": L_RED},
        "Y": {"top": HEIGHT/2 + 2, "left": 0,           "lit_color": L_YELLOW},
        "B": {"top": HEIGHT/2 + 2, "left": WIDTH/2 + 2, "lit_color": L_BLUE}
    }

    pygame.draw.rect(WIN, rect=(colors[color]["left"], colors[color]["top"], WIDTH/2, HEIGHT/2),
                     color=colors[color]["lit_color"])

    pygame.display.update()
    sleep(0.5)
    draw_window()


def get_color_clicked(mouse_pos):
    mx, my = mouse_pos
    col = mx // (WIDTH/2)
    row = my // (HEIGHT / 2)
    quadrant = (col, row)

    if quadrant == (0, 0):
        return "G"
    elif quadrant == (1, 0):
        return "R"
    elif quadrant == (0, 1):
        return "Y"
    elif quadrant == (1, 1):
        return "B"
    else:
        print("Out of bounds somehow")


def get_random_color():
    colors = ["G", "R", "Y", "B"]
    return colors[random.randint(0, 3)]


def game_over(score):
    # Saves score if it's a high score and prints game over message
    try:
        with open("high_score") as f:
            high_score = int(f.read())
    except FileNotFoundError:
        save_score(score)
        high_score = score

    if score > high_score:
        save_score(score)
        high_score = score
    
    # I wanted to draw the text in the game window, but pygame makes it complicated for some reason
    print(f"Game Over\n{score = }\n{high_score = }")


def main():
    score = 0
    sequence = []

    run = True
    draw_window()

    while run:

        sleep(0.25)
        sequence.append(get_random_color())
        for color in sequence:
            light_up(color)
            sleep(0.1)

        temp_score = 0
        for color in sequence:
            # Wait for event in queue to be mouse click or quit
            action = pygame.event.wait()
            while action.type != pygame.QUIT and action.type != pygame.MOUSEBUTTONDOWN:
                action = pygame.event.wait()

            if action.type == pygame.QUIT:
                run = False
                break
            elif action.type == pygame.MOUSEBUTTONDOWN:
                color_clicked = get_color_clicked(pygame.mouse.get_pos())
                light_up(color_clicked)

                if color_clicked == color:
                    temp_score += 1
                    if temp_score > score:
                        score = temp_score
                else:
                    game_over(score)
                    run = False
                    break

    pygame.quit()


if __name__ == '__main__':
    main()
