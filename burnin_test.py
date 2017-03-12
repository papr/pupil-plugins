'''
(*)~----------------------------------------------------------------------------------
 Pupil - eye tracking platform
 Copyright (C) 2012-2016  Pupil Labs

 Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
 License details are in the file license.txt, distributed as part of this software.
---
'''

from plugin import Plugin
from time import time, strftime, gmtime
from pyglui import ui
from audio import say
import logging
from zmq_tools import Msg_Receiver

logger = logging.getLogger(__name__)


class Burnin_Test(Plugin):

    burnin_time = 60*60+1  # 60x 60sec

    def __init__(self, g_pool):
        super(Burnin_Test, self).__init__(g_pool)
        self.running = False
        self.end_time = 0
        self.button = None
        self.log_receiver = Msg_Receiver(g_pool.zmq_ctx, g_pool.ipc_sub_url, topics=('logging.info',))

    def init_gui(self):
        self.button = ui.Thumb('running', self, setter=self.toggle, label='B', hotkey='b')
        self.button.on_color[:] = (1, .0, .0, .8)
        self.g_pool.quickbar.insert(2, self.button)

    def deinit_gui(self):
        if self.button:
            self.g_pool.quickbar.remove(self.button)
            self.button = None

    def toggle(self, _=None):
        if self.running:
            self.running = False
            self.button.status_text = ''
        else:
            self.end_time = time()+self.burnin_time
            self.running = True

    def recent_events(self, events):
        while self.log_receiver.new_data:
            topic, payload = self.log_receiver.recv()
            if self.running and payload['msg'] == 'Camera stopped providing frames. Reinitialising camera.':
                fail_reason = 'Camera in process {} disconnected. Burn in test failed.'.format(payload['processName'])
                say(fail_reason)
                logger.critical(fail_reason)
                self.toggle()

        if self.running:
            remaining_time = self.end_time-time()
            self.button.status_text = strftime("%H:%M:%S", gmtime(remaining_time))
            if remaining_time < 0:
                self.toggle()
                say("Burn in test successful")
                logger.info("Burn in test successful")

    def get_init_dict(self):
        return {}

    def cleanup(self):
        """gets called when the plugin get terminated.
           either volunatily or forced.
        """
        self.deinit_gui()
        del self.log_receiver
