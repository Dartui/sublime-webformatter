import sublime
import subprocess
import tempfile
import json
import re

class PhpFormatter:
    def format(self, code):
        with tempfile.TemporaryDirectory() as tmpdirname:
            filename = tmpdirname + '/tempfile'

            file = open(filename, 'w+b')
            file.write(code.encode('utf-8'))
            file.close()

            rules = {
                "@PSR1": True,
                "@PSR2": True,
                "align_multiline_comment": True,
                "array_indentation": True,
                "array_syntax": {
                    "syntax": "short",
                },
                "binary_operator_spaces": {
                    "default": "align_single_space_minimal",
                },
                "blank_line_before_statement": {
                    "statements":  ["break", "case", "continue", "declare", "default", "die", "do", "exit", "for", "foreach", "goto", "if", "include", "include_once", "require", "require_once", "return", "switch", "throw", "try", "while", "yield"]
                },
                "concat_space": {
                    "spacing": "one"
                },
                "constant_case": {
                    "case": "lower"
                },
                "explicit_indirect_variable": True,
                "explicit_string_variable": True,
                "function_typehint_space": True,
                "global_namespace_import": {
                    "import_classes": True,
                },
                "include": True,
                "linebreak_after_opening_tag": True,
                "lowercase_keywords": True,
                "lowercase_static_reference": True,
                "magic_constant_casing": True,
                "magic_method_casing": True,
                "method_chaining_indentation": True,
                "multiline_comment_opening_closing": True,
                "native_function_type_declaration_casing": True,
                "new_with_braces": True,
                "no_alternative_syntax": True,
                "no_binary_string": True,
                "no_blank_lines_after_class_opening": True,
                "no_blank_lines_after_phpdoc": True,
                "no_blank_lines_before_namespace": False,
                "no_empty_phpdoc": True,
                "no_empty_statement": True,
                "no_extra_blank_lines":  ['break', 'case', 'continue', 'curly_brace_block', 'default', 'extra', 'parenthesis_brace_block', 'return', 'square_brace_block', 'switch', 'throw', 'use', 'useTrait', 'use_trait'],
                "no_leading_import_slash": True,
                "no_leading_namespace_whitespace": True,
                "no_mixed_echo_print": True,
                "no_null_property_initialization": True,
                "no_short_echo_tag": True,
                "no_singleline_whitespace_before_semicolons": True,
                "no_spaces_around_offset": True,
                "no_trailing_comma_in_singleline_array": True,
                "no_unneeded_control_parentheses": True,
                "no_unneeded_curly_braces": True,
                "no_unused_imports": True,
                "no_useless_else": True,
                "no_useless_return": True,
                "no_whitespace_before_comma_in_array": True,
                "no_whitespace_in_blank_line": True,
                "normalize_index_brace": True,
                "object_operator_without_whitespace": True,
                "ordered_imports": {
                    "sortAlgorithm": "alpha"
                },
                "return_assignment": True,
                "return_type_declaration": True,
                "semicolon_after_instruction": True,
                "short_scalar_cast": True,
                "simple_to_complex_string_variable": True,
                "simplified_null_return": True,
                "single_quote": True,
                "ternary_operator_spaces": True,
                "trailing_comma_in_multiline_array": True,
                "trim_array_spaces": True,
                "unary_operator_spaces": True,
                "yoda_style": False,
            }

            command = ['php-cs-fixer', 'fix', '--stop-on-violation', '--using-cache=no', '--rules=' + json.dumps(rules), filename];
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

            try:
                res, err = process.communicate()
            except subprocess.CalledProcessError as e:
                print(e)

            error_pattern = 'Files that were not fixed due to errors reported during linting before fixing'

            if (re.search(error_pattern, err.decode('utf-8'))):
                return sublime.error_message('An error(s) occurred while linting code. Fix it manually and re-run script.')

            file = open(filename, 'r')
            return file.read()
