import importlib.util as imputils
import asyncio
import console
import os.path as osp
import yaml
import os

class PluginTemplate:
    def __init__(self, console, name):
        self.console = console
        self.name    = name
    def enable(self):
        self.console.log("Plugin",self.name,"enabled!")
    def disable(self):
        self.console.log("Plugin",self.name,"disabled!")

class PluginManager:
    plugins = {}
    def __get_path(self, file):
        return osp.join(self.path, file)
    def __init__(self, path, ignore_list=["__pycache__"]):
        self.path = path
        self.ignore_list = ignore_list

    def search_plugins(self):
        # Check if the plugins folder exists
        if not osp.exists(self.path) or not osp.isdir(self.path):
            #console.error("[red][ERROR][/red]")
            console.error("The folder \""+self.path+"\" that should contain the plugins doesn't exist!")
            console.error("Shutting down!")
            exit(1)
        
        # get list of files and directories in that folder
        folders = os.listdir(self.path)
        # filter out files, folders on ignore list, folders without plugin.yml
        for i in folders:
            if not osp.isdir(self.__get_path(i)):
                folders.remove(i)
            elif i in self.ignore_list:
                folders.remove(i)
            elif not osp.exists(osp.join(self.__get_path(i), "plugin.yml")) or not osp.isfile(osp.join(self.__get_path(i), "plugin.yml")):
                folders.remove(i)
        # if empty, skip plugins
        if len(folders) == 0:
            console.warn("No plugins found, skipping plugin loading!")
        
        for i in folders:
            self.load_plugin(self.__get_path(i))
    
    def load_plugin(self, path):
        config_path = osp.join(path, "plugin.yml") # get path to the config file
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) # load the config file and parse it
        if not config["enabled"]:
            console.log("Skipped loading plugin", config["name"], "because it is disabled")
            return
        console.log("Loading plugin", config["name"], "version", config["version"]) # log

        mod_name = config["alias"] # get the plugin name used in code
        main_file = osp.join(path, config["entry"]["file"]) # get the plugin main code file
        spec = imputils.spec_from_file_location(mod_name, main_file) # do some magic (initialize something that points to the plugin code file?)
        module = imputils.module_from_spec(spec) # load module
        spec.loader.exec_module(module) # initialize (exec it, thus define the main class) it
        self.init_plugin(path, module, config) # run it, hook it, whatever

    def init_plugin(self, path, module, config):
        name = config["name"]
        try:
            main_class = config["entry"]["class"] # get the entry class name from plugin config
        except:
            console.error(f"Error loading plugin \"{name}\", the main class isn't defined in config, skipping loading!")
            return
        try:
            plugin = module.__getattribute__(main_class)(console, name) # get the class itself and execute it,
                # arguments are the console instance and plugin name(probably gona add some more stuff later (keypresses, etc.))
        except AttributeError:
            console.error(f"Error loading plugin \"{name}\", class \"{main_class}\" is not defined, skipping loading!")
            return
        self.plugins.update({config["alias"]: [plugin, config]}) # append it to the plugin list

    def enable_all(self, *arg): # enable all plugins
        plugins = self.get_all_plugin_instances() # get all loaded plugins
        for i in plugins:
            try:
                i.enable(*arg) # enable them one by one
            except Exception as err: # if error
                console.warn("Plugin", self.get_plugin_name_from_instance(i), "could'n be enabled properly, trying to start normally anyway!")
                console.warn("Error:", err)
                # inform the user and continue
                # maybe in future i will implement dependency system and if some dependency fails to load, the program will exit
    def disable_all(self, *arg): # disable all plugins
        plugins = self.get_all_plugin_instances() # get all loaded plugins
        for i in plugins:
            try:
                i.disable(*arg) # enable them one by one
            except Exception as err: # if error
                console.warn("Plugin", self.get_plugin_name_from_instance(i), "could'n be disabled properly, trying to stop normaly but data loss may occur!")
                console.warn("Error:", err)
                # inform the user and continue
                # if the plugin is currently doing something and has some information loaded
                # due to the plugin not being able to save the information
    
    def register_hook(self, name):
        if not name + "_list" in globals().keys(): # if list isn't already defined
            globals().update({name+"_list": []}) # create list of functions
        # make function from template
        template="""def {}(func):
                        {}.append(func)
                        return func""".format(name, name+"_list")
        exec(template, globals())

    async def run_hook(self, name, *args):
        instances = self.get_all_plugin_instances()
        functions = globals()[name + "_list"]
        
        if len(instances)==0 or len(functions)==0:
            return
        
        functions = [
            functions[i](instances[i], *args) for i in range(len(functions))
        ]
        await asyncio.gather(*functions)

    def get_plugin(self, name):
        return self.plugins[name][0]
    def get_all_plugin_instances(self):
        return [i[0] for i in self.plugins.values()]
    def get_all_plugins(self):
        return list(self.plugins.keys())
    def get_plugin_name_from_instance(self, instance):
        try:
            return self.plugins[ self.get_all_plugins() [ self.get_all_plugin_instances() .index(instance) ] ] [1]["name"]
        except:
            return ""
