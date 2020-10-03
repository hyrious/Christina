import sublime
import sublime_plugin

class CloseWithoutSavingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.is_dirty():
            self.view.set_scratch(True)
        self.view.close()
