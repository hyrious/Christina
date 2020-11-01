import sublime
import sublime_plugin

class JsonAutoCompletion(sublime_plugin.ViewEventListener):
    def is_match_scope(self, point):
        return self.view.match_selector(point, "source.json meta.structure.dictionary.json")

    def on_query_completions(self, prefix, locations):
        if not all(self.is_match_scope(point) for point in locations): return None
        return [[prefix, '"{0}": ${{1:true}},$0'.format(prefix)]]
