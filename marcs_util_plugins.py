import logging
from plugin import Plugin

logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


class Remove_Thumbs(Plugin):
    order = .9

    def init_gui(self):
        del self.g_pool.quickbar[:3]


class High_Res_Scaling(Plugin):
    order = .9

    def __init__(self, g_pool, scale=2.):
        super().__init__(g_pool)
        self.scale = scale

    def init_gui(self):
        from pyglui import ui
        del self.g_pool.sidebar[0][1]

        self.old_scale = self.g_pool.gui_user_scale

        self.g_pool.sidebar[0].insert(1, ui.Selector('gui_user_scale', self.g_pool, setter=self.set_scale, selection=[.8, .9, 1., 1.1, 1.2, 2.0, 2.5, 3.0], label='Interface size'))
        self.set_scale(self.scale)

    def set_scale(self, new_scale):
        import glfw
        window = self.g_pool.main_window
        hdpi_factor = float(glfw.glfwGetFramebufferSize(window)[0] / glfw.glfwGetWindowSize(window)[0])
        self.g_pool.gui_user_scale = new_scale
        self.g_pool.gui.scale = self.g_pool.gui_user_scale * hdpi_factor
        width, height = glfw.glfwGetFramebufferSize(self.g_pool.main_window)
        self.g_pool.gui.update_window(width, height)
        logger.info('Setting scale to {}'.format(new_scale))

    def get_init_dict(self):
        scale = self.g_pool.gui_user_scale
        self.set_scale(self.old_scale)
        return {'scale': scale}
