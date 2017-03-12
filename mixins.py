from pyglui import ui


class Plugin_UI_Mixin(object):
    """Creates basic ui for plugins"""
    def init_gui(self):
        """Initializes sidebar menu"""
        super().init_gui()
        self.menu = ui.Growing_Menu(self.pretty_class_name)
        self.g_pool.sidebar.append(self.menu)

        def close():
            self.alive = False
        self.menu.append(ui.Button('Close', close))

    def deinit_gui(self):
        if self.menu:
            self.g_pool.sidebar.remove(self.menu)
            self.menu = None

    def cleanup(self):
        super().cleanup()
        self.deinit_gui()
