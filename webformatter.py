import sublime
import sublime_plugin
import re
from .formatter import Formatter

class WebFormatCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
        self.formatter = Formatter(self.view)

    def run(self, edit):
        syntax = self.syntax()

        if (self.formatter.supportsSyntax(syntax) == False):
            sublime.error_message('Syntax "%s" is not supported in Code Formatter.' % syntax)

        self.format(edit, syntax)

    def syntax(self):
        pattern = re.compile(r'Packages/.*/(.+?).(?=tmLanguage|sublime-syntax)')
        matches = pattern.search(self.view.settings().get('syntax'))
        found = ''

        if matches and len(matches.groups()) > 0:
            found = matches.groups()[0]

        return found.lower()

    def format(self, edit, syntax):
        self.view.replace(edit, sublime.Region(0, self.view.size()), self.formatter.format(syntax))
