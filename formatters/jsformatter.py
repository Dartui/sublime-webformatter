from .formatter import Formatter

class JSFormatter(Formatter):
    executables = ['${folder}/node_modules/.bin/eslint']
    config_filenames = ['.eslintrc.js', 'eslintrc.cjs', 'eslintrc.yaml', 'eslintrc.yml', 'eslintrc.json']
    use_tempfile = True

    def get_cmd(self):
        cmd = []

        cmd.append('${file}')
        cmd.append('--fix')
        cmd.append('--quiet')

        configuration = self.configuration_file()

        if (configuration is not None):
            cmd.append('--config=' + configuration)

        return cmd;