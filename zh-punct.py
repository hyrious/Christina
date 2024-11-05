import sublime, sublime_plugin
import re

zh_punct_replacements = {
  '：': ': ',
  '，': ', ',
  '；': '; ',
  '、': ', ',
  '。': '. ',
  '（': ' (',
  '）': ') ',
}

zh_punct_keys = '[' + ''.join(zh_punct_replacements.keys()) + ']'

class ReplaceZhPunctOnSave(sublime_plugin.ViewEventListener):
  @classmethod
  def applies_to_primary_view_only(cls):
    return True
  def on_pre_save(self):
    self.view.run_command('replace_zh_punct')

class ReplaceZhPunct(sublime_plugin.TextCommand):
  def is_enabled(self):
    name = self.view.file_name()
    return name.endswith('.js')
  def run(self, edit):
    start_pt = 0
    while start_pt >= 0:
      region = self.view.find(zh_punct_keys, start_pt)
      if region.empty(): break
      key = self.view.substr(region)
      replacement = zh_punct_replacements[key]
      # print('replace', region, (key, replacement))
      self.view.replace(edit, region, replacement)
      start_pt = region.end()
