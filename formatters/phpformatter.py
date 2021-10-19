from .formatter import Formatter

class PHPFormatter(Formatter):
    config_filenames = ['.php-cs-fixer.php', '.php-cs-fixer.dist.php', '.php_cs', '.php_cs.dist']
    use_tempfile = True

    def get_cmd(self):
        cmd = []

        cmd.append('${folder}/vendor/bin/php-cs-fixer')
        cmd.append('fix')
        cmd.append('${file}')
        cmd.append('--show-progress=none')
        cmd.append('--stop-on-violation')
        cmd.append('--using-cache=no')
        cmd.append('--no-ansi')
        cmd.append('--allow-risky=yes')

        configuration = self.configuration_file()

        if (configuration is not None):
            cmd.append('--config=' + configuration)

        return cmd;