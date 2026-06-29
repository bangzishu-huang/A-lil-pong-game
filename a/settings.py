import pygame
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
SIZE = {'paddle': (40,100), 'ball': (30,30)}
POSITION = {'player': (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2), 'opp': (50, WINDOW_HEIGHT / 2)}
SPEED = {'player':500, 'opp': 290, 'ball': 450}
COLORS = {
    'paddle': '#A1E8FF',
    'paddle shadow': "#81C1D4",
    'ball': '#FFFCAD',
    'ball shadow': '#EBE78D',
    'background': '#013C7A',
    'bg detail': '#0054AD',
    'title': '#FCFBD2',
    'button text': '#003359'
}