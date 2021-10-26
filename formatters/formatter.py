from abc import ABCMeta, abstractmethod
from collections import Mapping, Sequence

import shutil
import subprocess
import sublime
import os
import tempfile

class Formatter:
    __metaclass__ = ABCMeta

    view = None
    use_tempfile = False
    executables = []
    config_filenames = []

    _tempdir = None
    _tempfile = None

    def __init__(self, view):
        self.view = view

    @abstractmethod
    def get_cmd(self):
        pass

    def format(self, code):
        temporary_file = None

        if (self.use_tempfile == True):
            self.make_tempfile(code)

        executable = self.executable()

        if executable is None:
            sublime.error_message('Could not find executable.')
            raise Exception('Could not find executable.')

        cmd = self.get_cmd()
        cmd = executable + ' ' + self.build_cmd(cmd)
        cmd = self.substitute_variables(cmd, self.get_context())

        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        try:
            code, err = process.communicate()
        except subprocess.CalledProcessError as e:
            print(e)

        if (self.use_tempfile == True):
            return self.get_tempfile()

        return code

    def get_context(self):
        context = self.view.window().extract_variables()

        filename = self.view.file_name()
        if filename:
            basename = os.path.basename(filename)
            file_base_name, file_extension = os.path.splitext(basename)

            context['file'] = filename
            context['file_path'] = os.path.dirname(filename)
            context['file_name'] = basename
            context['file_base_name'] = file_base_name
            context['file_extension'] = file_extension

        if self.use_tempfile:
            context['file'] = self._tempfile;

        return context

    def build_cmd(self, cmd):
        if isinstance(cmd, list):
            return ' '.join(cmd)
        if isinstance(cmd, tuple):
            return ' '.join(cmd)

        return cmd

    # @see https://github.com/SublimeLinter/SublimeLinter/blob/7c2f2922067bd794e9c094e03316402bfd981c0c/lint/linter.py#L323-L341
    def substitute_variables(self, value, variables):
        # type: (Mapping, Any) -> Any
        # Utilizes Sublime Text's `expand_variables` API, which uses the
        # `${varname}` syntax and supports placeholders (`${varname:placeholder}`).

        if isinstance(value, str):
            # Workaround https://github.com/SublimeTextIssues/Core/issues/1878
            # (E.g. UNC paths on Windows start with double slashes.)
            value = value.replace(r'\\', r'\\\\')
            value = sublime.expand_variables(value, variables)
            return os.path.expanduser(value)
        elif isinstance(value, Mapping):
            return {key: self.substitute_variables(variables, val)
                    for key, val in value.items()}
        elif isinstance(value, Sequence):
            return [self.substitute_variables(variables, item)
                    for item in value]
        else:
            return value

    def make_tempfile(self, code):
        self._tempdir = tempfile.TemporaryDirectory()
        self._tempfile = self._tempdir.name + '/tempfile'

        file = open(self._tempfile, 'w+b')
        file.write(code.encode('utf-8'))
        file.close()

    def get_tempfile(self):
        file = open(self._tempfile, 'r')

        return file.read()

    def executable(self):
        if not self.executables:
            return None

        for executable in self.executables:
            executable = self.substitute_variables(executable, self.get_context())

            if shutil.which(executable) is not None:
                return executable

        return None

    def configuration_file(self):
        if not self.config_filenames:
            return None

        file_name = self.view.file_name()

        if file_name is None:
            return None

        if not isinstance(file_name, str):
            return None

        if not len(file_name) > 0:
            return None

        checked = []
        check_dir = os.path.dirname(file_name)

        while check_dir not in checked:
            for candidate in self.config_filenames:
                configuration_file = os.path.join(check_dir, candidate)

                if os.path.isfile(configuration_file):
                    return configuration_file

            checked.append(check_dir)
            check_dir = os.path.dirname(check_dir)

        return None