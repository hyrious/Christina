import sublime, sublime_plugin

have_a_rest = False
replacements = {
    "，": ", ",
    "（": " (",
    "）": ")",
    "：": ": ",
    "；": "; ",
    "。": ".",
    "【": " [",
    "】": "]",
}

class FixCjkCommaListener(sublime_plugin.TextChangeListener):
    def on_text_changed(self, changes):
        global have_a_rest
        if len(changes) != 1 or have_a_rest: return
        c = changes[0]
        if c.str not in replacements: return
        i = c.b.pt
        v = sublime.active_window().active_view()
        if i and v:
            have_a_rest = True
            v.run_command("fix_cjk_comma", { 'pt': i, 'replacement': replacements[c.str] })

class FixCjkComma(sublime_plugin.TextCommand):
    def run(self, edit, pt=-1, replacement=''):
        sublime.set_timeout(self.recover, 500)
        self.view.replace(edit, sublime.Region(pt, pt + 1), replacement)

    def recover(self):
        global have_a_rest
        have_a_rest = False
