import pygame
import os
import sys


def load_image(filename, name='', n_scale_divided=None, n_scale_multiply=None, n_scale_plus=None, n_plus_wide=None, flip=False):
    fullname = os.path.join('data/' + name, filename)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if n_scale_multiply is not None:
        image = pygame.transform.scale(image, (image.get_size()[0] * n_scale_multiply,
                                               image.get_size()[1] * n_scale_multiply))
    if n_plus_wide is not None:
        image = pygame.transform.scale(image, (image.get_size()[0] + n_plus_wide, image.get_size()[1]))
    if n_scale_plus is not None:
        image = pygame.transform.scale(image, (image.get_size()[0] + n_scale_plus, image.get_size()[1] + n_scale_plus))
    if n_scale_divided is not None:
        image = pygame.transform.scale(image, (image.get_size()[0] // n_scale_divided,
                                               image.get_size()[1] // n_scale_divided))
    if flip is not False:
        image = pygame.transform.flip(image, True, False)
    return image
