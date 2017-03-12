'''
(*)~----------------------------------------------------------------------------------
 Pupil - eye tracking platform
 Copyright (C) 2012-2016  Pupil Labs

 Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
 License details are in the file license.txt, distributed as part of this software.
---
'''

from os import path as pth
from plugin import Plugin
from pyglui import ui
from pprint import pformat

import logging
logger = logging.getLogger(__name__)


class Test_Plugin(Plugin):

    burnin_time = 60*60+1  # 60x 60sec

    def __init__(self, g_pool):
        super(Test_Plugin, self).__init__(g_pool)

    def init_gui(self):
        pass

    def deinit_gui(self):
        pass

    def recent_events(self, events):
        gaze = pformat(events['gaze_positions'])
        loc = pth.join(pth.dirname(__file__), 'testing-data.txt')
        with open(loc, mode='w') as f:
            f.write(gaze)
        self.alive = False

    # def get_init_dict(self):
    #     return {}

    def cleanup(self):
        self.deinit_gui()
