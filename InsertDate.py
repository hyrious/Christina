import sublime
import sublime_plugin
import time

class InsertDateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        s = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        v = self.view
        sel = v.sel()[0]
        i, j = sel.begin(), sel.end()
        if i != j: v.erase(edit, sublime.Region(i, j))
        v.insert(edit, i, s)
