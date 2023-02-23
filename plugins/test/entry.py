from plugins import PluginTemplate, on_init, on_progress, on_screen_draw

class obstacles(PluginTemplate):
    def enable(self, size):
        super().enable()
        self.WIDTH, self.HEIGHT = size

    # @on_init
    # def func_on_init(self, group):
    #     print("Init")
    @on_progress
    def func_on_progress(self, car):
        pass
        #car.score += 1
    # @on_screen_draw
    # def func_on_frame(self, scren):
    #     print("Frame")