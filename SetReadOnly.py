import sublime
import sublime_plugin

class SetReadOnlyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view.set_read_only(True)
