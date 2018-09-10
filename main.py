# coding: utf-8

import abcjs_basic_5_2_0
from random import choice
from time import time


class VueAdapter:

    def __init__(self):
        options = {'el': self.el,
                   'data': self.data}
        if hasattr(self, 'mounted'):
            options['mounted'] = self.mounted
        methods = getattr(self, 'methods', None)
        if not methods:
            methods = []
        options['methods'] = {method_name: getattr(self, method_name)
                              for method_name in methods}
        self.app = __new__(Vue(options))


class Game(VueAdapter):
    el = '#app'
    data = {'pitch': '',
            'score': 0,
            'time_left': '',
            'point_indicators': [],
            'face_down': True}
    methods = ['start']
    note_map = {'c': 'C',
                'd': 'D',
                'e': 'E',
                'f': 'F',
                'g': 'G',
                'a': 'A',
                'h': 'B'}
    duration = 30

    def __init__(self):
        super().__init__()
        self.started = False
        self.card = document.getElementById('music')

    def next_card(self):
        answer = choice(self.note_map.keys())
        abc = self.note_map[answer]
        ABCJS.renderAbc(self.card, abc, {'scale': 2})
        self.expect_key = answer
        self.data['face_down'] = False
        self.card_time = time()

    def start(self):
        self.started = True
        self.start_time = time()
        self.data['score'] = 0
        self.data['point_indicators'].clear()
        self.next_card()
        self.tick()
        self.timer = setInterval(self.tick, 1000)

    def tick(self):
        time_left = int(self.start_time + self.duration - time())
        if time_left < 1:
            self.started = False
            self.data['face_down'] = True
            ABCJS.renderAbc(self.card, '')
            clearInterval(self.timer)
        self.data['time_left'] = time_left

    def keypress(self, event):
        if not self.started:
            return
        if event.key == self.expect_key:
            elapsed = time() - self.card_time
            points = min(10, int(13 * 1.7 ** -elapsed))
            self.data['score'] += points
            self.data['point_indicators'].append(points)
            self.data['face_down'] = True
            setTimeout(self.next_card, 500)
        else:
            self.data['score'] -= 5
            self.data['point_indicators'].append(-5)

    def mounted(self, foo):
        document.addEventListener('keypress', self.keypress)


game = Game()
window.game = game
