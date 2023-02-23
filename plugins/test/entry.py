from plugins import PluginTemplate, on_init, on_progress, on_screen_draw

class obstacles(PluginTemplate):
    def enable(self, size):
        super().enable()
        self.WIDTH  = size[0]
        self.HEIGHT = size[1]

    # @on_init
    # def func_on_init(self, group):
    #     print("Init")
    @on_progress
    def func_on_progress(self, car):
        car.score += 1
    # @on_screen_draw
    # def func_on_frame(self, scren):
    #     print("Frame")