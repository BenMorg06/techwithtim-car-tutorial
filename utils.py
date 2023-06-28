import pygame, sys, os, math
from pygame.locals import *

#Scaling imgs
def scale_img(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

#rotating imgs
def blit_rotate_img(win, img, top_left, angle):
    rotated_img = pygame.transform.rotate(img, angle)
    new_rect = rotated_img.get_rect(center=img.get_rect(topleft=top_left).center) #makes the center of rotation not be the top left of the img
    # when rotating x and y change so this new rect tries to remove offset
    # gets rectangle from new rect and makes the center the top left of the new img the top left of the old img and gets the center from that
    win.blit(rotated_img, new_rect.topleft)
