import random
from time import sleep


def clear():
    print("\n"*80)


def save_score(score):
    with open("dist_high_score", "w") as f:
        f.write(str(score))


def get_random_color():
    colors = ["green", "red", "yellow", "blue"]
    return colors[random.randint(0, 3)]


def game_over(score):
    try:
        with open("dist_high_score") as f:
            high_score = int(f.read())

    except FileNotFoundError:
        save_score(score)
        high_score = score

    if score > high_score:
        save_score(score)
        high_score = score

    print(f"Game Over\n{score = }\n{high_score = }")


def main():
    sequence = []
    score = 0
    run = True

    while run:
        sleep(0.25)
        sequence.append(get_random_color())

        for color in sequence:
            print(color)
            sleep(1)
            clear()

        temp_score = 0
        for color in sequence:
            guess = input("color: ").lower()
            clear()

            if guess == color:
                temp_score += 1

                if temp_score > score:
                    score = temp_score

            else:
                game_over(score)
                run = False
                break


if __name__ == "__main__":
    main()
