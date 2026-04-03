import pygame
import random
import copy

pygame.init()

columns = 11
strings = 21

screen_x = 300
screen_y = 650

score = 0
best_score = 0

font = pygame.font.Font(None, 32)
menu_font = pygame.font.Font(None, 48)
help_font = pygame.font.Font(None, 24)

screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

state = "menu"

next_det_choice = None

play_button = pygame.Rect(screen_x // 2 - 50, screen_y // 2 - 40, 100, 40)
help_button = pygame.Rect(screen_x // 2 - 50, screen_y // 2 + 10, 100, 40)
back_button = pygame.Rect(screen_x // 2 - 50, screen_y // 2 + 60, 100, 40)

game_height = 600

cell_x = screen_x / (columns - 1)
cell_y = game_height / (strings - 1)

def draw_panel(score, best_score):

    pygame.draw.rect(screen, (50, 50, 50), (0, 0, screen_x, 50))
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, screen_x, 50), 2)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 3))

    best_text = font.render(f"Best: {best_score}", True, (255, 215, 0))
    screen.blit(best_text, (10, 25))

    next_text = font.render("Next:", True, (255, 255, 255))
    screen.blit(next_text, (screen_x - 150, 15))

    preview_rect = pygame.Rect(screen_x - 90, 8, 80, 35)
    pygame.draw.rect(screen, (30, 30, 30), preview_rect)
    pygame.draw.rect(screen, (100, 100, 100), preview_rect, 1)

    if next_det_choice:
        min_x = min(rect.x for rect in next_det_choice)
        min_y = min(rect.y for rect in next_det_choice)

        preview_start_x = screen_x - 70
        preview_start_y = 15

        size = 11

        for rect in next_det_choice:
            rel_x = (rect.x - min_x) // cell_x
            rel_y = (rect.y - min_y) // cell_y

            cell_rect = pygame.Rect(preview_start_x + rel_x * size, preview_start_y + rel_y * size, size - 1, size - 1)

            pygame.draw.rect(screen, next_color, cell_rect)
            pygame.draw.rect(screen, (200, 200, 200), cell_rect, 1)

def save_best_score(score, best_score):
    if score > best_score:
        best_score = score

        try:
            with open("best_score.txt", "w") as f:
                f.write(str(best_score))
        except:
            pass
    return best_score

def load_best_score():
    try:
        with open("best_score.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def draw_menu():
    screen.fill(pygame.Color(222, 248, 116, 100))

    title_text = menu_font.render("TETRIS", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(screen_x // 2, screen_y // 2 - 100))
    screen.blit(title_text, title_rect)

    pygame.draw.rect(screen, (100, 150, 50), play_button)
    pygame.draw.rect(screen, (0, 0, 0), play_button, 2)
    play_text = font.render("Play", True, (255, 255, 255))
    play_text_rect = play_text.get_rect(center=play_button.center)
    screen.blit(play_text, play_text_rect)

    pygame.draw.rect(screen, (100, 150, 50), help_button)
    pygame.draw.rect(screen, (0, 0, 0), help_button, 2)
    help_text = font.render("Help", True, (255, 255, 255))
    help_text_rect = help_text.get_rect(center=help_button.center)
    screen.blit(help_text, help_text_rect)

    best_text = font.render(f"Best:{best_score}", True, (0, 0, 0))
    best_rect = best_text.get_rect(center=(screen_x // 2, screen_y - 50))
    screen.blit(best_text, best_rect)

def draw_cell(x, y, cell_color):
    rect = pygame.Rect(x, y + 50, cell_x, cell_y)
    pygame.draw.rect(screen, cell_color, rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 1)

def draw_help():
    screen.fill(pygame.Color(222, 248, 116, 100))

    title_text = menu_font.render("HOW TO PLAY", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(screen_x // 2, 50))
    screen.blit(title_text, title_rect)

    instructions = [
        "LEFT/RIGHT arrows to move",
        "DOWN arrow to speed up",
        "ESC to leave game",
        "UP arrow to rotate",
        "",
        "1. Fill in the lines",
        "2. Get Points",
        "3. Don't give up"
    ]

    y_offset = 120
    for line in instructions:
        text = help_font.render(line, True, (0, 0, 0))
        text_rect = text.get_rect(center=(screen_x // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 25

    pygame.draw.rect(screen, (100, 150, 50), back_button)
    pygame.draw.rect(screen, (0, 0, 0), back_button, 2)
    back_text = font.render("Back", True, (255, 255, 255))
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)


def get_color(figure_index):
    figure_colors = [
        pygame.Color(255, 0, 0),
        pygame.Color(255, 255, 0),
        pygame.Color(255, 128, 0),
        pygame.Color(0, 255, 0),
        pygame.Color(0, 255, 255),
        pygame.Color(255, 0, 255),
        pygame.Color(0, 0, 255)
    ]
    return figure_colors[figure_index % len(figure_colors)]

def get_next_figure():
    figure_index = random.randint(0, len(det) - 1)
    figure = copy.deepcopy(det[figure_index])
    color = get_color(figure_index)
    return figure, color, figure_index

def reset_game():
    global grid, score, det_choice, color, count, best_score, next_det_choice, next_color, next_figure_index, figure_index

    if score > best_score:
        best_score = score
        save_best_score(score, best_score)

    for i in range(columns):
        for j in range(strings):
            grid[i][j][0] = 1
            grid[i][j][2] = pygame.Color("Gray")

    score = 0

    det_choice, color, figure_index = get_next_figure()
    next_det_choice, next_color, next_figure_index = get_next_figure()
    count = 0

fps = 60

grid = []

for i in range(columns):
    grid.append([])
    for j in range(strings):
        grid[i].append([1])

for i in range(columns):
    for j in range(strings):
        grid[i][j].append(pygame.Rect(i * cell_x, j * cell_y, cell_x, cell_y))
        grid[i][j].append(pygame.Color("Gray"))

details = [
    [[-2, 0], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [-1, 0], [0, 0], [1, 0]],
    [[1, 1], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [0, 1], [0, 0], [-1, 0]],
    [[-1, 0], [0, 0], [0, 1], [1, 1]],
    [[0, 1], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [0, 1], [0, 0], [1, 0]],
]

det = [[], [], [], [], [], [], []]

for i in range(len(details)):
    for j in range(4):
        det[i].append(
            pygame.Rect(details[i][j][0] * cell_x + cell_x * (columns // 2), details[i][j][1] * cell_y, cell_x, cell_y))

detail = pygame.Rect(0, 0, cell_x, cell_y)
det_choice = copy.deepcopy(random.choice(det))
color = random.choice([pygame.Color(255, 0, 0)])

next_color = None

figure_index = 0

next_figure_index = 0

count = 0
game = True
rotate = False

best_score = load_best_score()

def CanMove(det_choice, dx, dy):
    for i in range(4):
        x = int((det_choice[i].x + dx * cell_x) // cell_x)
        y = int((det_choice[i].y + dy * cell_y) // cell_y)

        if x < 0 or x >= columns or y > strings:
            return False

        if y >= 0 and grid[x][y][0] == 0:
            return False
    return True

while game:
    if state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_button.collidepoint(mouse_pos):
                        reset_game()
                        state = "game"
                    elif help_button.collidepoint(mouse_pos):
                        state = "help"

        draw_menu()
        pygame.display.flip()
        clock.tick(fps)
        continue

    elif state == "help":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button.collidepoint(mouse_pos):
                        state = "menu"
        draw_help()
        pygame.display.flip()
        clock.tick(fps)
        continue

    elif state == "game":
        delta_x = 0
        delta_y = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    delta_x = -1
                elif event.key == pygame.K_RIGHT:
                    delta_x = 1
                elif event.key == pygame.K_UP:
                    rotate = True
                elif event.key == pygame.K_ESCAPE:
                    state = "menu"
                    continue

        key = pygame.key.get_pressed()

        if key[pygame.K_DOWN]:
            count = 31 * fps

        screen.fill(pygame.Color(222, 248, 116, 100))

        for i in range(columns):
            for j in range(strings):
                if grid[i][j][0] == 0:
                    draw_cell(grid[i][j][1].x, grid[i][j][1].y, grid[i][j][2])
                else:
                    rect = pygame.Rect(grid[i][j][1].x, grid[i][j][1].y + 50, cell_x, cell_y)
                    pygame.draw.rect(screen, grid[i][j][2], rect, 1)

        if state != "game":
            continue

        for i in range(4):
            if ((det_choice[i].x + delta_x * cell_x < 0) or (det_choice[i].x + delta_x * cell_x >= screen_x)):
                delta_x = 0
            if ((det_choice[i].y + cell_y >= game_height) or (grid[int(det_choice[i].x // cell_x)][int(det_choice[i].y // cell_y) + 1][0] == 0)):
                delta_y = 0
                for i in range(4):
                    x = int(det_choice[i].x // cell_x)
                    y = int(det_choice[i].y // cell_y)
                    if 0 <= y < strings:
                        grid[x][y][0] = 0
                        grid[x][y][2] = color
                detail.x = 0
                detail.y = 0

                det_choice = copy.deepcopy(next_det_choice)
                color = next_color
                figure_index = next_figure_index

                next_det_choice, next_color, next_figure_index = get_next_figure()

                top = False
                for i in range(4):
                    x = int(det_choice[i].x // cell_x)
                    y = int(det_choice[i].y // cell_y)
                    if 0 <= x and 0 <= y < strings and grid[x][y][0] == 0:
                        top = True
                        break
                    if y < 0:
                        top = True
                        break

                if top:
                    state = "menu"
                    continue

        if CanMove(det_choice, delta_x, 0):
            for i in range(4):
                det_choice[i].x += delta_x * cell_x

        count += fps

        if count > 30 * fps:
            if CanMove(det_choice, 0, 1):
                for i in range(4):
                    det_choice[i].y += delta_y * cell_y
            else:
                delta_y = 0
            count = 0

        for i in range(4):
            draw_cell(det_choice[i].x, det_choice[i].y, color)

        C = det_choice[2]
        if rotate:
            temp = copy.deepcopy(det_choice)

            for i in range(4):
                x = temp[i].y - C.y
                y = temp[i].x - C.x
                temp[i].x = C.x - x
                temp[i].y = C.y + y

            shifts = [0, -1, 1, -2, 2]
            rotated = False

            for shift in shifts:
                if CanMove(temp, shift, 0):
                    for i in range(4):
                        temp[i].x += shift * cell_x
                    det_choice = temp
                    rotated = True
                    break

            rotate = False

        for j in range(strings - 1, -1, -1):
            count_cells = 0
            for i in range(columns):
                if grid[i][j][0] == 0:
                    count_cells += 1
                elif grid[i][j][0] == 1:
                    break
            if count_cells == (columns - 1):
                score += 10
                if score > best_score:
                    best_score = score
                    save_best_score(score, best_score)
                for l in range(columns):
                    grid[l][0][0] = 1
                for k in range(j, 0, -1):
                    for l in range(columns):
                        grid[l][k][0] = grid[l][k - 1][0]
                        grid[l][k][2] = grid[l][k - 1][2]

        draw_panel(score, best_score)

    pygame.display.flip()
    clock.tick(fps)
