import pygame
import math
import random

from resource.fwa_named_colors import *

gun_image = pygame.image.load("graphics/rivet_gun.png")

def demo_screen(arduino, screen, time):
    draw_rivetrace_bkg(arduino, screen, time, "Learn How")

    text_w_drop(screen, 'Pick up a rivet gun to play', screen.get_width() * 0.5, 240, 60, (255, 255, 255), 5, 100)

    gun_image_rotated = pygame.transform.rotate(gun_image, math.sin(time) * 50 + 45)
    screen.blit(gun_image_rotated, (
        screen.get_width() * 0.3 - gun_image_rotated.get_width() * 0.5 + math.sin(time) * 100 - 40,
        screen.get_height() * 0.75 - gun_image_rotated.get_height() * 0.5 + math.sin(time) * 200))
    screen.blit(pygame.transform.flip(gun_image_rotated, 1, 0), (
        screen.get_width() * 0.7 - gun_image_rotated.get_width() * 0.5 - math.sin(time) * 100,
        screen.get_height() * 0.75 - gun_image_rotated.get_height() * 0.5 + math.sin(time) * 200))


def training_screen(arduino, screen, time):
    draw_rivetrace_bkg(arduino, screen, time, "Instructions")

    column_y = screen.get_height() * 0.2

    text_w_drop(screen, 'Place the end of your gun over a red rivet hole to get the largest circle',
                screen.get_width() * 0.5, column_y, 40,
                (255, 255, 255), 5, 100)

    column_x = screen.get_width() * 0.3

    
    draw_box(screen, column_x, column_y + 220, 400, 300)
    draw_box(screen, screen.get_width() - column_x, column_y + 220, 400, 300)

    color_0 = (255, 0, 0)
    score_0 = arduino.get_rivets(player_num=0)
    if score_0 > 0:
        color_0 = (0, 255, 0)
    pygame.draw.circle(screen, color_0, (int(column_x), int(column_y + 220)), 100 + score_0)

    color_1 = (255, 0, 0)
    score_1 = arduino.get_rivets(player_num=1)
    if score_1 > 0:
        color_1 = (0, 255, 0)
    pygame.draw.circle(screen, color_1, (int(screen.get_width() - column_x), int(column_y + 220)), 100 + score_1)

    text_w_drop(screen, 'Left gun position', column_x, column_y + 330, 30, fwa_white, 5)
    text_w_drop(screen, 'Right gun position', screen.get_width() - column_x, column_y + 330, 30, fwa_white, 5)

    column_y = screen.get_height() * 0.6

    text_w_drop(screen, 'Orient the gun perpendicular to the metal sheet', screen.get_width() * 0.5, column_y, 40,
                (255, 255, 255), 5, 100)

    color_0 = fwa_medium_blue
    angle_0 = arduino.get_angle(player_num=0)
    if abs(angle_0) < 20 or abs(angle_0 - 180) < 20 or abs(angle_0 - 360) < 20:
        color_0 = fwa_medium_green
    color_1 = fwa_medium_blue
    angle_1 = arduino.get_angle(player_num=1)
    print("ANGLE1", angle_1)
    if abs(angle_1) < 20 or abs(angle_1 - 180) < 20 or abs(angle_1 - 360) < 20:
        color_1 = fwa_medium_green
    draw_box(screen, column_x, column_y + 220, 400, 300, background_color=color_0)
    draw_box(screen, screen.get_width() - column_x, column_y + 220, 400, 300, background_color=color_1)

    angle_0 = 180 + arduino.get_angle(player_num=0)
    gun_image_xform = pygame.transform.scale(gun_image, (200, 200))
    gun_image_xform = pygame.transform.rotate(gun_image_xform, angle_0)
    screen.blit(gun_image_xform,
                (column_x - gun_image_xform.get_width() * 0.5, column_y + 220 - gun_image_xform.get_width() * 0.5))

    angle_1 = 360 - arduino.get_angle(player_num=1)
    gun_image_xform = pygame.transform.scale(gun_image, (200, 200))
    gun_image_xform = pygame.transform.rotate(gun_image_xform, angle_1)
    screen.blit(gun_image_xform, (screen.get_width() - column_x - gun_image_xform.get_width() * 0.5,
                                  column_y + 220 - gun_image_xform.get_width() * 0.5))

    text_w_drop(screen, 'Left gun orientation', column_x, column_y + 330, 30, fwa_white, 5)
    text_w_drop(screen, 'Right gun orientation', screen.get_width() - column_x, column_y + 330, 30, fwa_white, 5)

    remaining_time = arduino.get_remaining_time()
    if remaining_time > 0:
        text_w_drop(screen,
                    'Training Successful continue in {}'.format(remaining_time),
                    screen.get_width() * 0.5,
                    screen.get_height() * 0.95, 20,
                    (255, 255, 255), 5)


def training_complete_screen(arduino, screen, time):
    draw_rivetrace_bkg(arduino, screen, time, "Congratulations!")

    text_w_drop(screen, 'Training Successful', screen.get_width() * 0.5, screen.get_height() * 0.45, 150,
                (255, 255, 255), 15)
    text_w_drop(screen, 'Pull Trigger to Continue', screen.get_width() * 0.5, screen.get_height() * 0.88, 80, fwa_grey,
                7, math.sin(time * 10) * 100 + 100)


def game_screen(arduino, screen, time):
    draw_rivetrace_bkg(arduino, screen, time, "RIVET RACE!")

    text_w_drop(screen, 'Set as many rivets as you can before time runs out!', screen.get_width() * 0.5, 230, 50,
                (255, 255, 255), 5, 100)

    # left player score display

    column_x = screen.get_width() * 0.2
    column_y = screen.get_height() * 0.35
    subtext_size = 50

    pygame.draw.rect(screen, fwa_2nd_teal_dk, (0, column_y - 50, screen.get_width() * 0.35, 480), 5)
    pygame.draw.rect(screen, fwa_medium_blue, (0, column_y - 50, screen.get_width() * 0.35, 480))

    text_w_drop(screen, 'Left Player', column_x, column_y - 30, subtext_size + 10, (255, 255, 255), 5)
    text_w_drop(screen,
                "Attempts/Rivet: %d/%d" % (arduino.get_rivet_attempts(player_num=0), arduino.get_rivets(player_num=0)),
                column_x,
                column_y + subtext_size * 1, subtext_size - 10, left_player_color, 5)
    accuracy_0 = 0
    attempts = arduino.get_rivet_attempts(player_num=0)
    if attempts > 0:
        accuracy_0 = arduino.get_rivets(player_num=0) / attempts
    text_w_drop(screen,
                "Accuracy: %d%%" % accuracy_0,
                column_x,
                column_y + subtext_size * 2, subtext_size - 10, left_player_color, 5)
    text_w_drop(screen, "Streak: %d" % (arduino.get_combo(player_num=0)), column_x, column_y + subtext_size * 3,
                subtext_size - 10, left_player_color, 5)
    text_w_drop(screen, 'Score:', column_x, column_y + subtext_size * 4.5, subtext_size, left_player_color, 5)
    text_w_drop(screen, str(arduino.get_points(player_num=0)), column_x, column_y + 290, 140, left_player_color, 10)

    # right player score display

    column_x = screen.get_width() * 0.8

    pygame.draw.rect(screen, fwa_2nd_teal_dk,
                     (screen.get_width() * 0.65, column_y - 50, screen.get_width() * 0.35, 480), 5)
    pygame.draw.rect(screen, fwa_medium_blue,
                     (screen.get_width() * 0.65, column_y - 50, screen.get_width() * 0.35, 480))

    text_w_drop(screen, 'Right Player', column_x, column_y - 30, subtext_size + 10, (255, 255, 255), 5)
    text_w_drop(screen,
                "Attempts/Rivet: %d/%d" % (arduino.get_rivet_attempts(player_num=0), arduino.get_rivets(player_num=1)),
                column_x,
                column_y + subtext_size * 1, subtext_size - 10, right_player_color, 5)
    accuracy_1 = 0
    attempts = arduino.get_rivet_attempts(player_num=1)
    if attempts > 0:
        accuracy_1 = arduino.get_rivets(player_num=1) / attempts
    text_w_drop(screen,
                "Accuracy: %d%%" % accuracy_1,
                column_x,
                column_y + subtext_size * 2, subtext_size - 10, right_player_color, 5)
    text_w_drop(screen, "Streak: %d" % (arduino.get_combo(player_num=1)), column_x, column_y + subtext_size * 3,
                subtext_size - 10, right_player_color, 5)
    text_w_drop(screen, 'Score:', column_x, column_y + subtext_size * 4.5, subtext_size, right_player_color, 5)
    text_w_drop(screen, str(arduino.get_points(player_num=1)), column_x, column_y + 290, 140, right_player_color, 10)

    # countdown

    remaining_seconds = arduino.get_remaining_time()
    text_w_drop(screen, '{}:{}'.format(remaining_seconds // 60, remaining_seconds % 60), screen.get_width() * 0.5,
                screen.get_height() * 0.65, 300, (255, 255, 255), 15)
    text_w_drop(screen, 'Time Remaining', screen.get_width() * 0.5, screen.get_height() * 0.92, 50, (255, 255, 255), 5)


def game_complete_screen(arduino, screen, time):
    draw_rivetrace_bkg(arduino, screen, time, "Congratulations!")

    column_x = screen.get_width() * 0.2
    column_y = screen.get_height() * 0.35
    subtext_size = 50

    pygame.draw.rect(screen, fwa_2nd_teal_dk, (0 - ease(time) * 800, column_y - 50, screen.get_width() * 0.35, 480), 5)
    pygame.draw.rect(screen, fwa_medium_blue, (0 - ease(time) * 800, column_y - 50, screen.get_width() * 0.35, 480))

    text_w_drop(screen, 'Left Player', column_x + ease(time) * 200, column_y - ease(time) * 60,
                60 + int(ease(time) * 40), (255, 255, 255), 5)
    text_w_drop(screen, 'Score:', column_x + ease(time) * 200, column_y + 100, 60 + int(ease(time) * 40),
                left_player_color, 5)
    text_w_drop(screen, str(arduino.get_points(player_num=0)), column_x + ease(time) * 200, column_y + 290,
                140 + int(ease(time) * 250), left_player_color, 10)

    # right player score display

    column_x = screen.get_width() * 0.8

    pygame.draw.rect(screen, fwa_2nd_teal_dk,
                     (screen.get_width() * 0.65 + ease(time) * 800, column_y - 50, screen.get_width() * 0.35, 480), 5)
    pygame.draw.rect(screen, fwa_medium_blue,
                     (screen.get_width() * 0.65 + ease(time) * 800, column_y - 50, screen.get_width() * 0.35, 480))

    text_w_drop(screen, 'Right Player', column_x - ease(time) * 200, column_y - ease(time) * 60,
                60 + int(ease(time) * 40), (255, 255, 255), 5)
    text_w_drop(screen, 'Score:', column_x - ease(time) * 200, column_y + 100, 60 + int(ease(time) * 40),
                right_player_color, 5)
    text_w_drop(screen, str(arduino.get_points(player_num=1)), column_x - ease(time) * 200, column_y + 290,
                140 + int(ease(time) * 250), right_player_color, 10)


def leaderboard(arduino, screen, time):
    draw_rivetrace_bkg(arduino, screen, time, "Leaderboard")

    top_score = arduino.get_leaderboard()

    start_y = screen.get_height() * 0.3

    text_w_drop(screen, 'Place', screen.get_width() * 0.3, start_y - 70, 50, fwa_2nd_teal_lt, 7)
    text_w_drop(screen, 'Score', screen.get_width() * 0.5, start_y - 70, 50, fwa_2nd_teal_lt, 7)
    # text_w_drop(screen, 'Date', screen.get_width() * 0.7, start_y - 70, 50, fwa_2nd_teal_lt, 7)

    player_0_score = arduino.get_points(player_num=0)
    player_1_score = arduino.get_points(player_num=1)

    for i, score in enumerate(top_score):
        text_w_drop(screen, str(i + 1), screen.get_width() * 0.3, start_y + i * 60, 50, fwa_grey, 5)
        text_w_drop(screen, str(score), screen.get_width() * 0.5, start_y + i * 60, 50, fwa_grey, 5)
        if abs(score - player_0_score) < 0.01:
            text_w_drop(screen, 'New High Score!', screen.get_width() * 0.7, start_y + i * 60, 50, left_player_color, 5)
        if abs(score - player_1_score) < 0.01:
            text_w_drop(screen, 'New High Score!', screen.get_width() * 0.7, start_y + i * 60, 50, right_player_color, 5)


def ease(time):
    return 0.5 - math.cos(min(3.14159, time)) * 0.5


def draw_rivetrace_bkg(arduino, screen, time, screen_title):
    bkg_image = pygame.image.load("graphics/interface_bkg.png")
    screen.fill((0, 0, 0))
    screen.blit(bkg_image, (0, 0))

    text_w_drop(screen, screen_title, screen.get_width() * 0.5, 50, 140, (255, 196, 51), 10)

    text_w_drop(screen, str(arduino.get_state()), 20, 20, 20, (255, 196, 51), 2, 50)  # print state for debugging

    text_w_drop(screen, 'v1.0', 20, screen.get_height() - 20, 20, (255, 196, 51), 2, 50)  # print version number


def text_w_drop(screen, text_string, x, y, size, text_color, drop_dist, drop_opacity=None, justify=None):
    font = pygame.font.Font("fonts/Politica XT Bold.ttf", size)

    if drop_opacity is None:
        drop_opacity = 140

    if justify is None:
        justify = 1

    img = font.render(text_string, True, (0, 0, 0))
    alpha_img = pygame.Surface(img.get_size(), pygame.SRCALPHA)  # creates a temp surface
    alpha_img.fill((255, 255, 255, drop_opacity))  # fills temp surface w alpha
    img.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)  # blits with original text surface

    if justify == 0:
        offset = -img.get_width()  # right justified
    elif justify == 1:
        offset = -img.get_width() * 0.5  # centered
    else:
        offset = 0  # left justified

    screen.blit(img, (x + offset + drop_dist, y + drop_dist))  # dropshadow blit

    img = font.render(text_string, True, text_color)  # rerender text
    screen.blit(img, (x + offset, y))  # regular text blit


def draw_box(screen, x_center, y_center, x_width, y_width, background_color=fwa_medium_blue):
    pygame.draw.rect(screen, background_color, (x_center - x_width * 0.5, y_center - y_width * 0.5, x_width, y_width))
    pygame.draw.rect(screen, fwa_2nd_teal_dk, (x_center - x_width * 0.5, y_center - y_width * 0.5, x_width, y_width), 5)
