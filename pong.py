import pygame
import sys
# import math
import random
from pygame.locals import *
from pygame.math import Vector2

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption('Pong')


def draw_text(text, FONT, surface, x, y):
    textobj = FONT.render(text, 1, TEXT_COLOR)
    textrect = textobj.get_rect()
    textrect.topleft = x, y
    surface.blit(textobj, textrect)


def wait_for_player_to_press_key():
    pressed = False
    while not pressed:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                return  # start game for any other key down


WHITE = (71, 180, 250)
GRAY = (154, 84, 160)
PINK = Color('#FF69B4')
TEXT_COLOR = PINK
main_clock = pygame.time.Clock()

paddle = pygame.Rect(30, 80, 30, 100)
paddle_up = pygame.Rect(0, 0, 30, 175)
paddle_down = pygame.Rect(0, WINDOW_HEIGHT - 30, 30, 175)
compPaddle = pygame.Rect(WINDOW_WIDTH - 60, WINDOW_HEIGHT - 190, 30, 100)
comp_up = pygame.Rect(WINDOW_WIDTH - 175, 0, 30, 175)
comp_down = pygame.Rect(WINDOW_WIDTH - 175, WINDOW_HEIGHT - 30, 30, 175)
musicPlaying = True
paddleImage = pygame.image.load('player_paddle.png')  # SHOULD BE 30 X 100
paddleImage_UD = pygame.image.load('paddle2.jpg')
comPaddleImage = pygame.image.load('com_paddle.png')
comPaddleImage_UD = pygame.image.load('com_paddle2.png')
moveUp = False
moveDown = False
moveRight = False
moveLeft = False
MOVE_SPEED = 3
play_game_again = True
hit_sound = pygame.mixer.Sound('hitsound.wav')
game_over_music = pygame.mixer.Sound('defeat.wav')
victory_music = pygame.mixer.Sound('victory.wav')
pygame.mixer.music.load('background.mid')
pygame.mixer.music.play(-1, 0.0)

"""
def comp(ball_, ball_xpos, paddle2):
    if ball_xpos == -1:
        if paddle2.centery < 300:
            paddle2.y += 1
        elif paddle2.centery > 300:
            paddle2.y -= 1
    elif ball_xpos == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -=1
    return paddle2
"""


def vector2(xy_tuple, scale):
    v = Vector2()
    v[0], v[1] = xy_tuple[0], xy_tuple[1]
    return v * scale


def direction():
    return random.randrange(-10, 10)


class Ball:
    def __instancecheck__(self, rect, bg_color, velocity, scale=1):
        self.bg_color = WHITE
        self.rect_ = pygame.Rect(rect)
        # Direction of ball
        self.velocity_ = vector2(velocity, scale)

    def __str__(self):
        return '*Box: clr={}, rect={}, velocity={}'.format(self.bg_color, self.rect_, self.velocity_)

    def get_velocity(self):
        return self.velocity_

    def get_rect(self):
        return self.rect_

    def move_ball(self):
        self.ball.left += self.velocity[0]
        self.ball.top += self.velocity[1]



while play_game_again:

    font = pygame.font.Font(None, 48)
    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(-1, 0.0)
    comp_score = 0
    player_score = 0
    ball = {'rect': pygame.Rect(600, 300, 20, 20), 'color': WHITE, 'vel': (direction(), direction())}
    # ball.reset()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    moveUp = True
                    moveDown = False
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = True
                    moveLeft = False
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False
                if event.key == K_a or event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_m:
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying

        windowSurface.fill(GRAY)
        r = ball['rect']
        v = ball['vel']
        r.left += v[0]
        r.top += v[1]
        draw_text(str(player_score), font, windowSurface, 245, 30)
        draw_text(str(comp_score), font, windowSurface, WINDOW_WIDTH - 175, 30)
        posi = 0
        for i in range(posi, WINDOW_HEIGHT):
            pygame.draw.rect(windowSurface, WHITE, pygame.Rect(600, posi, 10, 10))
            posi += 20
        if moveDown and paddle.bottom < WINDOW_HEIGHT:
            paddle.top += MOVE_SPEED
        if moveUp and paddle.top > 0:
            paddle.top -= MOVE_SPEED
        if moveRight and (paddle_down.right < 445 and paddle_up.right < 445):
            paddle_up.right += MOVE_SPEED
            paddle_down.right += MOVE_SPEED
        if moveLeft and (paddle_down.left > 0 and paddle_up.left > 0):
            paddle_up.left -= MOVE_SPEED
            paddle_down.left -= MOVE_SPEED
        windowSurface.blit(paddleImage_UD, paddle_up)
        windowSurface.blit(paddleImage_UD, paddle_down)
        windowSurface.blit(paddleImage, paddle)
        windowSurface.blit(comPaddleImage, compPaddle)
        windowSurface.blit(comPaddleImage_UD, comp_up)
        windowSurface.blit(comPaddleImage_UD, comp_down)
        if paddle.colliderect(r) or compPaddle.colliderect(r):
            v[0] *= -1
            # if musicPlaying:
                # hit_sound.play()
        if paddle_up.colliderect(r) or paddle_down.colliderect(r) or \
                comp_up.colliderect(r) or comp_down.colliderect(r):
            v[1] *= -1
            # if musicPlaying:
                # hit_sound.play()
        if r.left <= 600 and (r.left < 0 or r.top < 0 or r.bottom > WINDOW_HEIGHT):
            comp_score += 1
            r.x = 600
            r.y = 300
            # v['vel'] = {direction(), direction()}
        if r.right > 600 and (r.right > WINDOW_WIDTH or r.top < 0 or r.bottom > WINDOW_HEIGHT):
            player_score += 1
            r.x = 600
            r.y = 300
            # v['vel'] = {direction(), direction()}
        pygame.draw.rect(windowSurface, WHITE, r)
        pygame.display.update()
        if player_score >= 11 and player_score - comp_score > 1:
            pygame.mixer.music.stop()
            victory_music.play()
            draw_text('VICTORY', font, windowSurface, 600, 300)
            draw_text('Press a key to play again', font, windowSurface, 600, 400)
            wait_for_player_to_press_key()
        elif comp_score > 11 and comp_score - player_score > 1:
            pygame.mixer.music.stop()
            game_over_music.play()
            draw_text('GAME OVER', font, windowSurface, 600, 300)
            draw_text('Press a key to play again', font, windowSurface, 600, 400)
            wait_for_player_to_press_key()
        main_clock.tick(60)
