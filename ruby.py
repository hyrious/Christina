import sublime, sublime_plugin
import subprocess, glob

def spawn(args):
    si = None
    if sublime.platform() == "windows":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.run(args, startupinfo=si, capture_output=True, text=True).stdout

def json_parse(data):
    return sublime.decode_value(data)

class AutoCompleteRequire(sublime_plugin.ViewEventListener):
    @classmethod
    def applies_to_primary_view_only(cls):
        return True

    shorts = None
    longs = None
    def on_activated_async(self):
        if not self.shorts and not self.longs:
            shorts, longs = [], []
            paths = json_parse(spawn(['ruby', '-e', 'p $:']))
            for path in paths:
                for file in glob.glob(path + '/*.rb'):
                    shorts.append(file[len(path)+1:-3])
                for file in glob.glob(path + '/**/*.rb'):
                    longs.append(file[len(path)+1:-3].replace('\\', '/'))
            self.shorts = sorted(shorts)
            self.longs = sorted(longs)

    def on_query_completions(self, prefix, locations):
        if self.shorts and self._is_ruby_require(locations):
            pt = locations[0]
            if region := self.view.expand_to_scope(pt, "meta.string.ruby"):
                a, b = region.begin() + 1, region.end() - 1
                if a <= b:
                    prefix = self.view.substr(sublime.Region(a, pt))
                    items = self.longs if '/' in prefix else self.shorts
                    return [self._to_completion_item(e) for e in items if e.startswith(prefix)]

    def _to_completion_item(self, trigger):
        item = sublime.CompletionItem(trigger)
        item.kind = sublime.KIND_NAMESPACE
        return item

    def _is_ruby_require(self, locations):
        for point in locations:
            if self.view.match_selector(point, "meta.require.ruby"):
                return True
        return False
