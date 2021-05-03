import sublime
import sublime_plugin

class WrapWithParenthesesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        for region in v.sel():
            if not region.empty():
                code = v.substr(region)
                v.erase(edit, region)
                v.insert(edit, region.begin(), R"\left(" + code + R"\right)")
