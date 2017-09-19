from plugin import Plugin
from pyglui import ui


class Progress_Animator(Plugin):
    def __init__(self, g_pool, animating=True):
        super().__init__(g_pool)
        self.accelerate = True
        self.animating = animating

    def init_ui(self):
        self.add_menu()
        self.menu_icon.indicator_start = 0.
        self.menu_icon.indicator_stop = 0.1
        self.menu.append(ui.Switch('animating', self, label='Toggle Animation'))

    def deinit_ui(self):
        self.remove_menu()

    def recent_events(self, events):
        if self.animating:
            if self.accelerate:
                self.menu_icon.indicator_start += 0.01
                self.menu_icon.indicator_stop += 0.02
            else:
                self.menu_icon.indicator_start += 0.02
                self.menu_icon.indicator_stop += 0.01
            d = abs(self.menu_icon.indicator_start - self.menu_icon.indicator_stop)
            if self.accelerate and d > .5:
                self.accelerate = False
            elif not self.accelerate and d < .1:
                self.accelerate = True

    def get_init_dict(self):
        return {'animating': self.animating}
