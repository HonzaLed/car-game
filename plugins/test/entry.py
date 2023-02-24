from plugins import PluginTemplate, on_progress
import asyncio

class test(PluginTemplate):
    def enable(self, size):
        super().enable()
        self.WIDTH, self.HEIGHT = size
    @on_progress
    async def func_on_progress(self, car):
        pass