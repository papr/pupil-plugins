from pyglui import ui
from plugin import Plugin
from mixins import Plugin_UI_Mixin
from pyglui.cygl.utils import draw_polyline_norm, RGBA
import logging

logger = logging.getLogger(__name__)


class Recent_Gaze(Plugin_UI_Mixin, Plugin):
    """docstring for Recent_Gaze"""
    def __init__(self, g_pool, store_duration=1., min_alpha=.0, max_alpha=1.):
        super().__init__(g_pool)
        self.store_duration = store_duration
        self.queue = []
        self.min_alpha = min_alpha
        self.max_alpha = max_alpha

    def get_init_dict(self):
        return {'store_duration': self.store_duration, 'min_alpha': self.min_alpha, 'max_alpha': self.max_alpha}

    def init_gui(self):
        super().init_gui()
        self.menu.append(ui.Text_Input('store_duration', self, label='Duration'))
        self.menu.append(ui.Slider('min_alpha', self, label='Min. Alpha', min=0., max=1., step=0.05))
        self.menu.append(ui.Slider('max_alpha', self, label='Max. Alpha', min=0., max=1., step=0.05))

    def recent_events(self, events):
        # add new gaze positions
        self.queue.extend(events['gaze_positions'])

        now = self.g_pool.get_timestamp()
        # remove outdated gaze positions
        for idx, gp in enumerate(self.queue):
            if gp['timestamp'] < now - self.store_duration:
                del self.queue[:idx]

    def gl_display(self):
        for idx in range(1, len(self.queue)):
            newest = self.queue[-1]['timestamp']
            current = self.queue[idx]['timestamp']
            normalized_age = 1 - (newest - current)/self.store_duration
            res_alpha = self.min_alpha + (self.max_alpha - self.min_alpha) * normalized_age
            draw_polyline_norm([self.queue[idx-1]['norm_pos'], self.queue[idx]['norm_pos']],
                               thickness=int(self.g_pool.gui.scale * 10 + 1), color=RGBA(1., 0.2, 0.4, res_alpha))
