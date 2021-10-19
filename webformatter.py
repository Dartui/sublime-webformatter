import sublime
import sublime_plugin
import re

from .formatters.phpformatter import PHPFormatter
from .formatters.jsformatter import JSFormatter

class WebFormatCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view

    def available_formatters(self):
        return {
            'php': PHPFormatter(self.view),
            'javascript': JSFormatter(self.view),
            'vue component': JSFormatter(self.view),
        }

    def get_syntax(self):
        pattern = re.compile(r'Packages/.*/(.+?).(?=tmLanguage|sublime-syntax)')
        matches = pattern.search(self.view.settings().get('syntax'))
        found = ''

        if matches and len(matches.groups()) > 0:
            found = matches.groups()[0]

        return found.lower()

    def supports_syntax(self, syntax):
        return syntax in self.available_formatters().keys()

    def get_formatter(self, syntax):
        if (self.supports_syntax(syntax) == False):
            return None

        return self.available_formatters().get(syntax)

    def run(self, edit):
        syntax = self.get_syntax()
        formatter = self.get_formatter(syntax)

        if (formatter is None):
            return sublime.error_message('Syntax "%s" is not supported in Code Formatter.' % syntax)

        self.format(edit, formatter, syntax)

    def format(self, edit, formatter, syntax):
        region = sublime.Region(0, self.view.size())

        code = self.view.substr(region)
        formatted_code = formatter.format(code)

        self.view.replace(edit, region, formatted_code)
