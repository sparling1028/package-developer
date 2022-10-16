# This is a package managed, and written by the package_developer package.
# Code should not be changed manually, but only by the methods provided in the package_developer package.
# 
# package_developer is copyrighted 2022 by Solomon Sparling under the GNU General Public License, Version 3.
#
# I hope you get as much value out of this as possible.
# The world is full of opportunities, and automation of data processes, I think, is the biggest one.


#  +-----------------------------------------------------------------------------------------------------------------+
#  |-----------------------------------------------------------------------------------------------------------------|
#  |-----------------------------------------------------------------------------------------------------------------|
#  |  888b     d888             888        888           8888888                                    888              |
#  |  8888b   d8888             888        888             888                                      888              |
#  |  88888b.d88888             888        888             888                                      888              |
#  |  888Y88888P888 .d88b.  .d88888888  888888 .d88b.      888  88888b.d88b. 88888b.  .d88b. 888d888888888.d8888b    |
#  |  888 Y888P 888d88""88bd88" 888888  888888d8P  Y8b     888  888 "888 "88b888 "88bd88""88b888P"  888   88K        |
#  |  888  Y8P  888888  888888  888888  88888888888888     888  888  888  888888  888888  888888    888   "Y8888b.   |
#  |  888   "   888Y88..88PY88b 888Y88b 888888Y8b.         888  888  888  888888 d88PY88..88P888    Y88b.      X88   |
#  |  888       888 "Y88P"  "Y88888 "Y88888888 "Y8888    8888888888  888  88888888P"  "Y88P" 888     "Y888 88888P'   |
#  |                                                                         888                                     |
#  |                                                                         888                                     |
#  |                                                                         888                                     |
#  |-----------------------------------------------------------------------------------------------------------------|
#  |-----------------------------------------------------------------------------------------------------------------|
#  +-----------------------------------------------------------------------------------------------------------------+

import os
import re
import types
import sys

import pandas as pd

from pyfiglet import Figlet
from inspect import getsource, signature
from typing import Union
from importlib import reload


#  +--------------------------------------------------------------------------------------------------------------------------------+
#  |--------------------------------------------------------------------------------------------------------------------------------|
#  |--------------------------------------------------------------------------------------------------------------------------------|
#  |  888b     d888             888        888                  d8888888   888          d8b888             888                      |
#  |  8888b   d8888             888        888                 d88888888   888          Y8P888             888                      |
#  |  88888b.d88888             888        888                d88P888888   888             888             888                      |
#  |  888Y88888P888 .d88b.  .d88888888  888888 .d88b.        d88P 888888888888888888d88888888888b. 888  888888888 .d88b. .d8888b    |
#  |  888 Y888P 888d88""88bd88" 888888  888888d8P  Y8b      d88P  888888   888   888P"  888888 "88b888  888888   d8P  Y8b88K        |
#  |  888  Y8P  888888  888888  888888  88888888888888     d88P   888888   888   888    888888  888888  888888   88888888"Y8888b.   |
#  |  888   "   888Y88..88PY88b 888Y88b 888888Y8b.        d8888888888Y88b. Y88b. 888    888888 d88PY88b 888Y88b. Y8b.         X88   |
#  |  888       888 "Y88P"  "Y88888 "Y88888888 "Y8888    d88P     888 "Y888 "Y888888    88888888P"  "Y88888 "Y888 "Y8888  88888P'   |
#  |--------------------------------------------------------------------------------------------------------------------------------|
#  |--------------------------------------------------------------------------------------------------------------------------------|
#  +--------------------------------------------------------------------------------------------------------------------------------+

pseudo_imported_names = dict()

#  +------------------------------------------------------------------------------------------------------------------------+
#  |------------------------------------------------------------------------------------------------------------------------|
#  |------------------------------------------------------------------------------------------------------------------------|
#  |  888b     d888             888        888           8888888888                     888   d8b                           |
#  |  8888b   d8888             888        888           888                            888   Y8P                           |
#  |  88888b.d88888             888        888           888                            888                                 |
#  |  888Y88888P888 .d88b.  .d88888888  888888 .d88b.    8888888888  88888888b.  .d8888b888888888 .d88b. 88888b. .d8888b    |
#  |  888 Y888P 888d88""88bd88" 888888  888888d8P  Y8b   888    888  888888 "88bd88P"   888   888d88""88b888 "88b88K        |
#  |  888  Y8P  888888  888888  888888  88888888888888   888    888  888888  888888     888   888888  888888  888"Y8888b.   |
#  |  888   "   888Y88..88PY88b 888Y88b 888888Y8b.       888    Y88b 888888  888Y88b.   Y88b. 888Y88..88P888  888     X88   |
#  |  888       888 "Y88P"  "Y88888 "Y88888888 "Y8888    888     "Y88888888  888 "Y8888P "Y888888 "Y88P" 888  888 88888P'   |
#  |------------------------------------------------------------------------------------------------------------------------|
#  |------------------------------------------------------------------------------------------------------------------------|
#  +------------------------------------------------------------------------------------------------------------------------+

#  +-------------------------------------------------------------------------------+
#  |   _          _                    __                  _   _                   |
#  |  | |        | |                  / _|                | | (_)                  |
#  |  | |__   ___| |_ __   ___ _ __  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___   |
#  |  | '_ \ / _ \ | '_ \ / _ \ '__| |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|  |
#  |  | | | |  __/ | |_) |  __/ |    | | | |_| | | | | (__| |_| | (_) | | | \__ \  |
#  |  |_| |_|\___|_| .__/ \___|_|    |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/  |
#  |               | |                                                             |
#  |               |_|                                                             |
#  +-------------------------------------------------------------------------------+
#  function group: helper functions

def __print_nice_dictionary__(d):
    return '{\n   '+'},\n\n  '.join(str(d)[1:-1].split('},')) + '\n}'


def dedent_method(text):
    tqt = triple_quote_tracker(text).next()
    dedented_lines = []
    while tqt.line_number != None:
        if (tqt.prev_line_hanging == True):
            #print('not dedenting', tqt.line)
            dedented_lines.append(tqt.line)
        else:
            assert (({x for x in tqt.line[:4]} in ({' '}, set()))
                or (tqt.line[:3] in ('f""', "f''", '"""', "'''"))
                   ), "If you're reading this Solomon screwed up... or possible you did... There is a problem in dedent_method or triple_quote_tracker... Or you are just reading this in the actual code\n" + text + "\n-----------------------------------------------"
            #print('dedenting', tqt.line)
            dedented_lines.append(tqt.line[4:])
        tqt.check_next()   
    return '\n'.join(dedented_lines)


def get_things_from_dir(target, object_type='all', filter_function=lambda group: [x for x in group if (x[:2]+x[-2:] != '____')]):
    if object_type == 'all':
        isinstance_function = lambda x: True
    elif isinstance(object_type, type):
        isinstance_function = lambda x: isinstance(x, object_type)
    elif isinstance(object_type, types.FunctionType):
        isinstance_function = object_type
    else:
        isinstance_function = lambda x: len(['_' for t in object_type if isinstance(x, t)]) > 0
    things = {}
    for x in filter_function(dir(target)):
        exec(f"locals()['value'] = target.{x}", {}, locals())
        if isinstance_function(locals()['value']):
            things[x] = locals()['value']
    return things


def print_what_is(code):
    exec(f"""print(f"{{{code} = }}")""")


def indent_method(text):
    tqt = triple_quote_tracker(text).next()
    indented_lines = []
    while tqt.line_number != None:
        if (tqt.prev_line_hanging == True):
            indented_lines.append(tqt.line)
        else:
            indented_lines.append(f"    {tqt.line}")
        tqt.check_next()   
    return '\n'.join(indented_lines)


#  +--------------------------------------------------------------------+
#  |             _                  _     _   _     _                   |
#  |            | |                | |   | | | |   (_)                  |
#  |    _____  _| |_ _ __ __ _  ___| |_  | |_| |__  _ _ __   __ _ ___   |
#  |   / _ \ \/ / __| '__/ _` |/ __| __| | __| '_ \| | '_ \ / _` / __|  |
#  |  |  __/>  <| |_| | | (_| | (__| |_  | |_| | | | | | | | (_| \__ \  |
#  |   \___/_/\_\\__|_|  \__,_|\___|\__|  \__|_| |_|_|_| |_|\__, |___/  |
#  |                                                         __/ |      |
#  |                                                        |___/       |
#  +--------------------------------------------------------------------+
#  function group: extract things

def __extract_from_path_by_tag__(path, tag):
    return ['.'.join(x.split('.')[:-1])
            for x in path.split(os.path.sep)
            if x.split('.')[-1] == tag]


def __extract_functions_from_body__(body):
    # find function_names and function_texts
    function_tuples = re.findall(fr"(^def (\w+).+?)(?=[\n\r]def \w+)", body+'\ndef nonexistentfunction', re.MULTILINE + re.DOTALL)
    function_names = [tup[1] for tup in function_tuples]
    function_texts = [tup[0] for tup in function_tuples]
    # return in dictionary format
    return dict(zip(function_names, function_texts))


def __extract_methods_from_body__(body, class_indent='    '):
    # find method_names and method_texts
    method_tuples = re.findall(fr"(^{class_indent}def (\w+).+?)(?=[\n\r]{class_indent}def \w+)", body+'\n'+f"{class_indent}def nonexistentfunction", re.MULTILINE + re.DOTALL)
    method_names = [tup[1] for tup in method_tuples]
    method_texts = [dedent_method(tup[0]) for tup in method_tuples]
    # return in dictionary format
    return dict(zip(method_names, method_texts))


def __extract_next_heading__(heading_iterator, verbose=True):
    heading_text, text_between_headings = ('\n'.join([line for line in x.splitlines()
                                                      if line.strip() != ''
                                                      ])
                                            for x in next(heading_iterator).groups()
                                            )
    if verbose == True:
        print('heading_text')
        print('88888888888888888888888888888888888888888888888888')
        print(heading_text)
        print('88888888888888888888888888888888888888888888888888')
        print('\n\n')
        print('text_between_headings')
        print('88888888888888888888888888888888888888888888888888')
        print(text_between_headings)
        print('88888888888888888888888888888888888888888888888888')
        print('\n\n')
    heading_type = __heading_type__(heading_text)
    return (heading_type, heading_text, text_between_headings)


def __extract_shared_attributes_from_body__(body, class_indent='    '):
    # find method_names and method_texts
    attribute_tuples = re.findall(fr"^{class_indent}(?!def)(\w+)[^\S\r\n]*?=(.*?)(?=^{class_indent}\w)", body+'\n'+f"{class_indent}def nonexistentfunction", re.MULTILINE + re.DOTALL)
    # trim off white space from attribute right hand code
    attribute_tuples = [(left, right.strip()) for left, right in attribute_tuples]
    attribute_names = [tup[0] for tup in attribute_tuples]
    attribute_texts = [tup[1] for tup in attribute_tuples]
    # return in dictionary format
    return dict(zip(attribute_names, attribute_texts))


#  +-------------------------------------------------------------------+
#  |                  _ _   _                    _ _                   |
#  |                 (_|_) | |                  | (_)                  |
#  |    __ _ ___  ___ _ _  | |__   ___  __ _  __| |_ _ __   __ _ ___   |
#  |   / _` / __|/ __| | | | '_ \ / _ \/ _` |/ _` | | '_ \ / _` / __|  |
#  |  | (_| \__ \ (__| | | | | | |  __/ (_| | (_| | | | | | (_| \__ \  |
#  |   \__,_|___/\___|_|_| |_| |_|\___|\__,_|\__,_|_|_| |_|\__, |___/  |
#  |                                                        __/ |      |
#  |                                                       |___/       |
#  +-------------------------------------------------------------------+
#  function group: ascii headings

def __heading_iterator__(text):
    return re.finditer(r'(#\s*?[+]-+[+].*?)(?=^\s*?$(.*?)#\s*?[+]-+[+].*?)', text, re.MULTILINE + re.DOTALL)


def __heading_type__(heading):
    heading = '\n'.join([x for x in heading.splitlines() if x.strip() != ''])
    last_line = heading.splitlines()[-1]
    words = [x for x in re.findall(r'\w+', last_line)]
    if words == []:
        known_wordless_headings = ['Module Imports', 'Module Functions', 'Module Attributes']
        for h in known_wordless_headings:
            if heading == render_class_heading(h):
                return h
        else:
            return 'class'
    else:
        assert len(words) >= 3, f"{words = }"
        assert words[1] == 'group', f"{words = }"
        return (' '.join(words[:2]), 
                ' '.join(words[2:])
               )


def find_quote(_text_, start_position=0):
    _text_ = _text_[start_position:]
    x = re.search(r'f?r?(\'|")', _text_, flags=re.MULTILINE + re.IGNORECASE)
    if x == None:
        return None
    # is this an f-string
    is_f_string = (x.group()[0].lower() == 'f')
    # type of quote
    quote_type = x.group()[-1]
    # is this a triple quote?
    is_triple = bool(re.match(fr"{quote_type}{{2}}", _text_[x.end(): x.end()+2]))
    if is_triple:
        quote_type = quote_type*3
    # find the end of the quote
    pattern = fr'(\\*){quote_type}'
    skip_chars = 0
    while True:
    # making sure that we ignore escaped quotes   
        end_match = re.search(pattern, _text_[x.end()+skip_chars: ], flags=re.MULTILINE)
        if len(end_match.groups()[0]) % 2 == 0:
            end = end_match.end() + x.end() + skip_chars
            break
        else:
        # searching beyond escaped quote
            skip_chars += end_match.end()
    return match_w_pos(_text_[x.start(): end], x.start(), end)


def render_class_heading(class_name):
    class_name = class_name.replace('_', ' ')
    text_lines = Figlet(font='colossal', direction='horizontal', width=800).renderText(class_name).splitlines()
    text_lines = [f"  {line}  " 
                  for line in text_lines
                  if line.strip() != ''
                 ]
    text_lines = [line + ' '*max((60-len(line)), 0) for line in text_lines]
    max_line = max([len(x) for x in text_lines])
    decorator_line = '-'*max_line
    heading_lines = [decorator_line]*3 + text_lines + [decorator_line]*3
    heading_lines = [
             f"#  +{heading_lines[i]}+" if i in {0, len(heading_lines)-1}
        else f"#  |{heading_lines[i]}|"
        for i in range(len(heading_lines))
                    ]
    heading_text = '\n'.join(heading_lines)
    return heading_text


def render_group_heading(group_name, method_or_function='method'):
    assert method_or_function in {'method', 'function'}
    fake_name = group_name.replace('_', ' ')
    text_lines = Figlet(font='big', direction='horizontal', width=800).renderText(fake_name).splitlines()
    text_lines = [f"  {line}  " 
                  for line in text_lines
                  if line.strip() != ''
                 ]
    text_lines = [line + ' '*max((30-len(line)), 0) for line in text_lines]
    max_line = max([len(x) for x in text_lines])
    decorator_line = '-'*max_line
    heading_lines = [decorator_line] + text_lines + [decorator_line]
    heading_lines = [
             f"#  +{heading_lines[i]}+" if i in {0, len(heading_lines)-1}
        else f"#  |{heading_lines[i]}|"
        for i in range(len(heading_lines))
                    ]
    heading_text = '\n'.join(heading_lines + [f"#  {method_or_function} group: {group_name}"])
    return heading_text


#  +-----------------------------------------------------------------------------+
#  |                       _       _                             _               |
#  |                      | |     | |                           (_)              |
#  |   _ __ ___   ___   __| |_   _| | ___   _ __   __ _ _ __ ___ _ _ __   __ _   |
#  |  | '_ ` _ \ / _ \ / _` | | | | |/ _ \ | '_ \ / _` | '__/ __| | '_ \ / _` |  |
#  |  | | | | | | (_) | (_| | |_| | |  __/ | |_) | (_| | |  \__ \ | | | | (_| |  |
#  |  |_| |_| |_|\___/ \__,_|\__,_|_|\___| | .__/ \__,_|_|  |___/_|_| |_|\__, |  |
#  |                                       | |                            __/ |  |
#  |                                       |_|                           |___/   |
#  +-----------------------------------------------------------------------------+
#  function group: module parsing

def __get_first_level_class_indent__(class_name, text_body):
    # find class_name in text_body
    args = (fr'^[^\S\r\n]*class[^\S\r\n]+{class_name}\b.*?^', text_body, re.MULTILINE+re.DOTALL)
    assert len(re.findall(*args)) == 1
    class_name_match = re.search(*args)
    lines_after_class_match = text_body[class_name_match.end():]
    # ignore text block
    triple_quotes = re.search(r'(""")|(\'\'\')', lines_after_class_match.splitlines()[0])
    if triple_quotes == None:
        lines_after_text_block = lines_after_class_match
    else:
        triple_quotes = triple_quotes.group()
        triple_quote_match = re.search(fr'{triple_quotes}.*?{triple_quotes}', lines_after_class_match, re.MULTILINE+re.DOTALL)
        lines_after_text_block = lines_after_class_match[triple_quote_match.end():]
    # find first thing
    lines = iter(lines_after_text_block.splitlines())
    while True:
        line = next(lines)
        if line.strip() != '':
            break
    indent = re.search(r'[^\S\r\n]*', line).group()
    return indent


def __parse_by_ascii_headings__(text, verbose=True):
    heading_iterator = __heading_iterator__(text + '\n\n\n' + render_group_heading('end'))
    module_directory = {}
    while True:
        # parse text into sections by ascii headings
        try:
            h_type, h_text, h_body = __extract_next_heading__(heading_iterator, verbose=verbose)
        except StopIteration:
            break
        # -------------- h_type == 'Module Imports' --------------
        if h_type == 'Module Imports':
            module_directory['Module Imports'] = {
                        line.strip(): get_import_names_from_text(line.strip()) 
                        for line in h_body.splitlines()
                                                  }
        # -------------- h_type == 'Module Functions' --------------
        elif h_type == 'Module Attributes':
            module_directory['Module Attributes'] = __extract_shared_attributes_from_body__(h_body, class_indent='')
        # -------------- h_type == 'Module Functions' --------------
        elif h_type == 'Module Functions':
            module_directory['Module Functions'] = __extract_functions_from_body__(h_body)
        # -------------- h_type == 'class' --------------
        elif h_type == 'class':
            if 'Module Classes' not in module_directory.keys():
                module_directory['Module Classes'] = {}
            class_name = re.findall(r"class (\w+?)\b", h_body.splitlines()[0])
            print(h_body)
            assert len(class_name) == 1, f"{class_name = }"
            class_name = class_name[0]
            class_indent = __get_first_level_class_indent__(class_name, text)
            last_major_heading = class_name
            module_directory['Module Classes'][class_name] = __extract_methods_from_body__(h_body, class_indent=class_indent)
            module_directory['Module Classes'][class_name]['shared attributes'] = __extract_shared_attributes_from_body__(h_body, class_indent=class_indent)
        # extract information from h_body, and store it somewhere       
        # -------------- h_type == (group_type, group_name) --------------
        else:
            assert type(h_type) == tuple, f"{h_type = }"
            assert len(h_type) == 2, f"{h_type = }"
            assert h_type[0] in {'function group', 'method group'}, f"{h_type = }"
            group_name = h_type[1]
            # ---------------- function group ----------------
            if h_type[0] == 'function group':
                module_directory['Module Functions'][group_name] = __extract_functions_from_body__(h_body)
            # ---------------- method group ----------------
            else:
                module_directory['Module Classes'][last_major_heading][group_name] = __extract_methods_from_body__(h_body)
    # Done
    return module_directory


def get_import_names_from_text(line):
        names = set()
        if line[:7] == 'import ':
            names_and_aliases = [x.strip() for x in line[6:].split(',')]
        else:
            assert line[:5] == 'from '
            assert len(line.split(' import ')) == 2
            names_and_aliases = [x.strip() for x in line.split(' import ')[1].split(',')]
        for nanda in names_and_aliases:
            if ' as ' in nanda:
                assert len(nanda.split(' as ')) == 2
                names.add(nanda.split(' as ')[1].strip())
            else:
                assert ' ' not in nanda
                names.add(nanda.replace(' ', ''))
        return names


def remove_quoted_things(text):
    while True:
        quote = find_quote(text)
        if quote == None:
            return text
        text = text.replace(quote.match, '', 1)
    return text


def import_pseudonymously(phrase):
    d = dict()
    program = f"""
    {phrase}
    for name in get_import_names_from_text('{phrase}'):
        d[name] = eval(name)
    """
    program = dedent_method(program)
    exec(program, {'d':d, 'get_import_names_from_text': get_import_names_from_text})
    return d


#  +-------------------------------------------------------------------------------------------------------------+
#  |-------------------------------------------------------------------------------------------------------------|
#  |-------------------------------------------------------------------------------------------------------------|
#  |          888                                888                        888                                  |
#  |          888                                888                        888                                  |
#  |          888                                888                        888                                  |
#  |   .d8888b888 8888b. .d8888b .d8888b     .d88888 .d88b. 888  888 .d88b. 888 .d88b. 88888b.  .d88b. 888d888   |
#  |  d88P"   888    "88b88K     88K        d88" 888d8P  Y8b888  888d8P  Y8b888d88""88b888 "88bd8P  Y8b888P"     |
#  |  888     888.d888888"Y8888b."Y8888b.   888  88888888888Y88  88P88888888888888  888888  88888888888888       |
#  |  Y88b.   888888  888     X88     X88   Y88b 888Y8b.     Y8bd8P Y8b.    888Y88..88P888 d88PY8b.    888       |
#  |   "Y8888P888"Y888888 88888P' 88888P'    "Y88888 "Y8888   Y88P   "Y8888 888 "Y88P" 88888P"  "Y8888 888       |
#  |                                                                                   888                       |
#  |                                                                                   888                       |
#  |                                                                                   888                       |
#  |-------------------------------------------------------------------------------------------------------------|
#  |-------------------------------------------------------------------------------------------------------------|
#  +-------------------------------------------------------------------------------------------------------------+

class class_developer:

    developer_root = os.path.join('C:', os.path.sep, 'Users', 'ssparling', 'Data-Analysis', 'Python-Projects', 'Package-Developer', 'development_mods')
    src_package_root = os.path.join('C:', os.path.sep, 'Users', 'ssparling', 'Data-Analysis', 'Python-Projects', 'Package-Developer', 'sourceable_modules')

    def __write_module_cascading_directories__(self):
        # write levels above module if they don't exist
        modules_to_write = self.__module_root__.split(self.developer_root)[1].split(os.path.sep)[1:-1]
        for i in range(len(modules_to_write)):
            path = os.path.join(self.developer_root, *modules_to_write[:i+1])
            if os.path.isdir(path):
                pass
            else:
                os.mkdir(path)
        # module level folder should not exists
        assert os.path.isdir(self.__module_root__) == False, f"{self.__module_root__} already exists"
        # ---------- write module level ----------
        os.mkdir(self.__module_root__)
        # write module imports
        path = os.path.join(self.__module_root__, f"module_imports.imports")
        with open(path, 'x') as flasdfkjerkjas:
            flasdfkjerkjas.write(__print_nice_dictionary__(self.module_directory('Module Imports')))
        # write module attributes
        path = os.path.join(self.__module_root__, f"module_attributes.attributes")
        with open(path, 'x') as flasdfkjerkjas:
            flasdfkjerkjas.write(__print_nice_dictionary__(self.module_directory('Module Attributes')))
        # write ungrouped module functions
        for key, value in self.module_directory('Module Functions').items():
            if isinstance(value, str):
                path = os.path.join(self.__module_root__, f"{key}.function")
                with open(path, 'x') as flasdfkjerkjas:
                    flasdfkjerkjas.write(value)
            # write grouped module functions
            else:
                assert isinstance(value, dict)
                group_root = os.path.join(self.__module_root__, f"{key}.function_group")
                os.mkdir(group_root)
                for function_name, function_text in value.items():
                    path = os.path.join(group_root, f"{function_name}.function")
                    with open(path, 'x') as flasdfkjerkjas:
                        flasdfkjerkjas.write(function_text)
        # write each class
        for class_name, class_dictionary in self.module_directory('Module Classes').items():
            print(class_name, '++++++++++', class_dictionary)
            assert isinstance(class_dictionary, dict) 
            class_root = os.path.join(self.__module_root__, f"{class_name}.class")
            os.mkdir(class_root)
            # write shared attributes
            if 'shared attributes' in class_dictionary:
                path = os.path.join(class_root, 'shared_attributes.attributes')
                with open(path, 'x') as flasdfkjerkjas:
                    flasdfkjerkjas.write(__print_nice_dictionary__(class_dictionary['shared attributes']))
            # write ungrouped methods
            for key, value in class_dictionary.items():
                if isinstance(value, str):
                    path = os.path.join(class_root, f"{key}.method")
                    with open(path, 'x') as flasdfkjerkjas:
                        flasdfkjerkjas.write(value)
                # write grouped methods
                elif key != 'shared attributes':
                    assert isinstance(value, dict)
                    os.mkdir(os.path.join(class_root, f"{key}.method_group"))
                    for method_name, method_text in value.items():
                        path = os.path.join(class_root, f"{key}.method_group", f"{method_name}.method")
                        with open(path, 'x') as flasdfkjerkjas:
                            flasdfkjerkjas.write(method_text)
        # save module directory
        self.__save_module_directory__()
        return self




    def ungrouped_methods(self, filter_function=lambda group: [x for x in group if x[:2] + x[-2:] != '____']):
        return {method_name: method for method_name, method in self.methods(filter_function=filter_function).items()
                if method_name not in self.grouped_methods(filter_function=lambda x:x).keys()
                }


    def construct_pseudo_imported_names(self):
        global pseudo_imported_names
        pseudo_imported_names[f'{self.target_module.__name__}.{self.target_class.__name__}'] = dict()
        for key, value in self.module_attributes().items():
            pseudo_imported_names[f'{self.target_module.__name__}.{self.target_class.__name__}'][key] = value
        for key, value in self.module_functions().items():
            pseudo_imported_names[f'{self.target_module.__name__}.{self.target_class.__name__}'][key] = value
        for key, value in self.module_classes().items():
            pseudo_imported_names[f'{self.target_module.__name__}.{self.target_class.__name__}'][key] = value
        for phrase in self.module_imports().keys():
            for key, value in import_pseudonymously(phrase).items():
                pseudo_imported_names[f'{self.target_module.__name__}.{self.target_class.__name__}'][key] = value
        return None


#  +---------------------------------------+
#  |   _     _           _ _               |
#  |  | |   (_)         | (_)              |
#  |  | |__  _ _ __   __| |_ _ __   __ _   |
#  |  | '_ \| | '_ \ / _` | | '_ \ / _` |  |
#  |  | |_) | | | | | (_| | | | | | (_| |  |
#  |  |_.__/|_|_| |_|\__,_|_|_| |_|\__, |  |
#  |                                __/ |  |
#  |                               |___/   |
#  +---------------------------------------+
#  method group: binding

    def get_sibling_class_lines(self, sibling_class):
        return getsource(self.module_classes()[sibling_class]).splitlines()




    def get_self_class_lines(self):
        def add(*lines_to_add, leading_spaces=0): 
            for line in lines_to_add: class_lines.append(' '*leading_spaces + line)
        def skip_line(n=1): 
            for _ in range(n): add('')
        class_lines = []
        # Class heading
        add(f"class {self.target_class.__name__}:")
        # Text block
        path = os.path.join(self.__class_root__, f"{self.target_class.__name__}.text_block")
        if os.path.isfile(path):
            add('\"\"\"', leading_spaces=4)
            with open(path, 'r') as flasdfkjerkjas:
                add(*flasdfkjerkjas.read().splitlines())
            add('\"\"\"', leading_spaces=4)
        skip_line()
        # shared attributes
        for left, right in self.class_directory('shared attributes').items():
            add(f'{left} = {right}', leading_spaces=4)
        skip_line()
        def add_method(*method_names, indents=1):
            # Search for method
            nonlocal add
            for method_name in method_names:
                path = [x[0] for x in os.walk(self.__class_root__)
                        if f"{method_name}.method" in x[2]]
                assert len(path) == 1, f"{method_name = }" + '\n' + f"{path = }"
                with open(os.path.join(*path, f"{method_name}.method"), 'r') as flasdfkjerkjas:
                    method_lines = flasdfkjerkjas.read().splitlines()
                # is there a text block?
                path = [x[0] for x in os.walk(self.__class_root__)
                        if f"{method_name}.text_block" in x[2]]
                if len(path) == 0:
                    add(*method_lines, leading_spaces=indents*4)
                else:
                    assert len(path) == 1
                    for line in method_lines:
                        add(line, leading_spaces=indents*4)
                        method_lines.remove(line)
                        if '):' in line:
                            break
                    with open(path[0], 'r') as flasdfkjerkjas:
                        lines = flasdfkjerkjas.read().splitlines()
                    add('\"\"\"', leading_spaces = (indents+1)*4)
                    add(*lines)
                    add('\"\"\"', leading_spaces = (indents+1)*4)
                    add(*method_lines, leading_spaces=indents*4)
                skip_line(2)
            return None
        # Methods by group
        # ungrouped methods
        known_underscored_stuff = ['__init__', '__str__', '__repr__']
        for method_name in known_underscored_stuff:
            if method_name in self.ungrouped_methods(filter_function=lambda x: x).keys():
                add_method(method_name)
                skip_line(2)
        for method_name in self.ungrouped_methods(filter_function=lambda x: x).keys():
            if method_name not in known_underscored_stuff:
                add_method(method_name)
                skip_line(2)
        # grouped methods
        for method_group in self.method_groups():
            skip_line()
            add(render_group_heading(method_group))
            skip_line()
            for method in self.method_groups(filter_function=lambda x: x)[method_group]:
                add_method(method)
                skip_line(2)
        return class_lines




    def bind(self, where=None):
        if where == None: where = self.__module_root__
        global_lines = []
        def add(*lines_to_add): 
            for line in lines_to_add: global_lines.append(line)
        def skip_line(n=1): 
            for _ in range(n): add('')
        # Document Heading
        with open(os.path.join(self.developer_root, 'default.text_block')) as flasdfkjerkjas:
            lines = flasdfkjerkjas.read().splitlines()
            lines = ['# '+line for line in lines]
        add(*lines)
        skip_line(2)
        # We will start with the imports
        add(render_class_heading('Module Imports'))
        skip_line()
        all_imports = self.module_imports().keys()
        straight_imports = [x for x in all_imports if (' as ' not in x) & (' from ' not in f" {x} ")]
        aliased_imports = [x for x in all_imports if (' from ' not in f" {x} ") & (x not in straight_imports)]
        remaining_imports = [x for x in all_imports if x not in straight_imports + aliased_imports]
        add(*straight_imports)
        skip_line()
        add(*aliased_imports)
        skip_line()
        add(*remaining_imports)
        skip_line(2)
        # add module attributes
        add(render_class_heading('Module Attributes'))
        skip_line()
        for left, right in self.module_directory('Module Attributes').items():
            add(f"{left} = {right}")
            skip_line()
        # add module functions
        add(render_class_heading('Module Functions'))
        skip_line() 
        # add ungrouped_functions
        for function_name in self.ungrouped_functions(lambda x: x).keys():
            function_text = self.module_directory('Module Functions', function_name)
            add(function_text)
            skip_line(2)
        # add grouped_functions
        for group_name in self.function_groups().keys():
            add(render_group_heading(group_name, 'function'))
            skip_line()
            for function_name, function_text in self.module_directory('Module Functions', group_name).items():
                add(function_text)
                skip_line(2)
        # Add each class
        for class_name in self.module_classes().keys():
            add(render_class_heading(class_name))
            skip_line()
            if class_name == self.target_class.__name__:
                add(*self.get_self_class_lines())
            else:
                add(*self.get_sibling_class_lines(class_name))
            skip_line(2)
        sourceable_text = '\n'.join(global_lines)
        # write to file
        with open(os.path.join(self.src_package_root, 
                               *self.target_module.__name__.split('.')[:-1],
                               self.target_module.__name__.split('.')[-1]+'.py'), 'w') as flasdfkjerkjas:
            flasdfkjerkjas.write(sourceable_text)
        # add to .pth file
        pth_location = [x for x in sys.path if x.split('\\')[-1]=='site-packages'][0]
        pth_location = os.path.join(pth_location, 'package-developer.pth')
        with open(pth_location, 'r') as flasdfkjerkjas:
            all_src_paths = {l for l in flasdfkjerkjas.read().splitlines()}
            print(f"{all_src_paths = }")
        if self.src_package_root not in all_src_paths:
            print("writing to source .pth file")
            with open(pth_location, 'a') as flasdfkjerkjas:
                flasdfkjerkjas.write('\n' + self.src_package_root)
                print(f"'{self.src_package_root}' added to package-developer.pth file for sourcing package\nPackage is now sourceable")
        print('Binding complete')
        self.__save_module_directory__()
        return self





#  +------------------------------------------------------------------------------------------------------------------+
#  |         _   _        _ _           _                               _             _       _   _                   |
#  |        | | | |      (_) |         | |                             (_)           | |     | | (_)                  |
#  |    __ _| |_| |_ _ __ _| |__  _   _| |_ ___   _ __ ___   __ _ _ __  _ _ __  _   _| | __ _| |_ _  ___  _ __  ___   |
#  |   / _` | __| __| '__| | '_ \| | | | __/ _ \ | '_ ` _ \ / _` | '_ \| | '_ \| | | | |/ _` | __| |/ _ \| '_ \/ __|  |
#  |  | (_| | |_| |_| |  | | |_) | |_| | ||  __/ | | | | | | (_| | | | | | |_) | |_| | | (_| | |_| | (_) | | | \__ \  |
#  |   \__,_|\__|\__|_|  |_|_.__/ \__,_|\__\___| |_| |_| |_|\__,_|_| |_|_| .__/ \__,_|_|\__,_|\__|_|\___/|_| |_|___/  |
#  |                                                                     | |                                          |
#  |                                                                     |_|                                          |
#  +------------------------------------------------------------------------------------------------------------------+
#  method group: attribute manipulations

    def remove_module_attribute(self, name):
        assert (name in globals().keys()) | (name not in self.module_attributes().keys())
        self.shared_attributes().pop(name)
        self.module_directory('Module Attributes').pop(name)
        globals().pop(name)
        delattr(self.target_module, name, attribute)
        path = os.path.join(self.__class_root__, "shared_attributes.attributes")
        self.__save_module_directory__()
        return self



    def add_module_imports(self, *imports):
        # Add import, and imported names to directory
        for statement in imports:
            for name, value in import_pseudonymously(statement).items():
                pseudo_imported_names[f"{self.target_module.__name__}.{self.target_class.__name__}"][name] = value
            self.module_imports()[statement] = get_import_names_from_text(statement)
            self.module_directory()['Module Imports'][statement] = get_import_names_from_text(statement)
        self.__save_module_directory__()
        return self



    def add_shared_attribute(self, name, attribute_code, type_function=lambda x: x):
        assert isinstance(attribute_code, str), "attribute code must be the code that would be stored in the sourceable file. Righthand of the attribute name."
        attribute = eval(attribute_code)
        self.shared_attributes()[name] = attribute
        self.class_directory('shared attributes')[name] = attribute_code
        setattr(self.target_class, name, attribute)
        for instance_name, instance in self.instances().items():
            setattr(instance, name, type_function(attribute))
        path = os.path.join(self.__class_root__, "shared_attributes.attributes")
        with open(path, 'w') as flasdfkjerkjas:
            flasdfkjerkjas.write(__print_nice_dictionary__(self.class_directory('shared attributes')))
        self.__save_module_directory__()
        return self




    def add_module_attribute(self, name, attribute_code, type_function=lambda x: x):
        assert isinstance(attribute_code, str), "attribute code must be the code that would be stored in the sourceable file. Righthand of the attribute name."
        assert (name not in globals().keys()) | (name in self.module_attributes().keys()), f"unfortunately, because of the way things are defined in your module from my 'pagage-developer' module, we can't have overlapping things in the namespace. {name} is already taken. This may be a future fix"
        attribute = eval(attribute_code)
        self.shared_attributes()[name] = attribute
        self.module_directory('Module Attributes')[name] = attribute_code
        exec(f"{name} = {attribute_code}", globals())
        setattr(self.target_module, name, attribute)
        path = os.path.join(self.__class_root__, "shared_attributes.attributes")
        self.__save_module_directory__()
        return self




    def delete_module_imports(self, *imports):
        for statement in imports:
            names = get_import_names_from_text(statement)
            self.module_imports().pop(statement)
            self.module_directory('Module Imports').pop(statement)
            for name in names:
                # remove name from module
                delattr(self.target_module, name)
        self.__save_module_directory__()
        return self




    def remove_shared_attribute(self, attribute_name):
        self.shared_attributes().pop(attribute_name)
        delattr(self.target_class, attribute_name)
        self.class_directory('shared attributes').pop(attribute_name)
        path = os.path.join(self.__class_root__, "shared_attributes.attributes")
        with open(path, 'w') as flasdfkjerkjas:
            flasdfkjerkjas.write(__print_nice_dictionary__(self.class_directory('shared attributes')))
        self.__save_module_directory__()
        return self





#  +-----------------------------------------------------------+
#  |       _ _      _   _                        _             |
#  |      | (_)    | | (_)                      (_)            |
#  |    __| |_  ___| |_ _  ___  _ __   __ _ _ __ _  ___  ___   |
#  |   / _` | |/ __| __| |/ _ \| '_ \ / _` | '__| |/ _ \/ __|  |
#  |  | (_| | | (__| |_| | (_) | | | | (_| | |  | |  __/\__ \  |
#  |   \__,_|_|\___|\__|_|\___/|_| |_|\__,_|_|  |_|\___||___/  |
#  +-----------------------------------------------------------+
#  method group: dictionaries

    def method_groups(self, *groups, filter_function=lambda group: [x for x in group if x[:2] + x[-2:] != '____']):
        assert set(groups).issubset({key for key, value in self.class_directory().items() if hasattr(value, 'keys') & (key != 'shared attributes')})
        if groups == ():
            groups = {
                    key for key, value in self.class_directory().items()
                    if hasattr(value, 'keys')
                    & (key != 'shared attributes')
                             }
        return {group: self.methods(group, filter_function=filter_function) for group in groups}




    def instances(self, key_filter=lambda l: {x for x in l if bool(re.match(r'[_\d].*',x))==False}):
        return {
            key: value for key, value in self.__calling_env_globals__.items()
            if (key in key_filter(self.__calling_env_globals__.keys()))
            & isinstance(value, self.target_class)
                }




    def function_groups(self, *groups, filter_function=lambda group: [x for x in group if x[:2] + x[-2:] != '____']):
        assert set(groups).issubset({key for key, value in self.module_directory('Module Functions').items() if hasattr(value, 'keys')})
        if groups == ():
            groups = {key for key, value in self.module_directory('Module Functions').items()if hasattr(value, 'keys')}
        return {group: self.module_functions(group, filter_function=filter_function) for group in groups}




    def shared_attributes(self, filter_function=lambda group: [x for x in group if (x[:2]+x[-2:] != '____')]):
        if filter_function == None:
            filter_function = lambda x: x
        def not_these_things(x):
            for t in {types.BuiltinFunctionType, types.BuiltinMethodType, 
                      types.FunctionType, types.LambdaType, 
                      types.MethodType, types.ModuleType}:
                if isinstance(x, t):
                    return False
            return True
        return get_things_from_dir(self.target_class, not_these_things, filter_function=filter_function)




    def module_imported_names(self):
        return set().union(*self.module_imports().values())




    def env_globals(self, thing=None, ignore_underscore=True):
        if thing==None:
            return self.__calling_env_globals__
        else:
            return self.__calling_env_globals__[thing]




    def grouped_functions(self, *function_groups, filter_function=lambda group: [x for x in group if x[:2] + x[-2:] != '____']):
        if function_groups == ():
            function_groups = {
                    key for key, value in self.module_directory('Module Functions').items()
                    if hasattr(value, 'keys')
                             }
        return {function_name: function for function_group in function_groups
                for function_name, function in self.module_functions(function_group).items()}




    def ungrouped_functions(self, filter_function=lambda group: [x for x in group if x[:2] + x[-2:] != '____']):
        return {function_name: function for function_name, function in self.module_functions(filter_function=filter_function).items()
                if function_name not in self.grouped_functions()}




    def methods(self, *method_groups, filter_function=None):
        if (filter_function == None) & (method_groups == ()):
            filter_function = lambda group: {x for x in group if (x[:2]+x[-2:] != '____')}
        elif filter_function == None:
            filter_function = lambda group: {method_name for value in [value for key, value in self.class_directory().items()
                                                                       if hasattr(value, 'keys')
                                                                       & (key in method_groups)]
                                             for method_name in value.keys()
                                             }
        elif method_groups == ():
            pass
        else:
            # in this case, both method groups and filter_function are something
            lambda_filter = filter_function
            group_filter = lambda group: {method_name for value in [value for key, value in self.class_directory().items()
                                                      if hasattr(value, 'keys')
                                                      & (key in method_groups)]
                                          for method_name in value.keys()
                                          }
            filter_function = lambda group: {x for x in group 
                                             if (x in lambda_filter(group)) 
                                             & (x in group_filter(group))
                                            }
        return get_things_from_dir(self.target_class, types.FunctionType, filter_function=filter_function)




    def module_imports(self):
        return self.__module_imports__




    def grouped_methods(self, *method_groups, filter_function=lambda group: [x for x in group if x[:2] + x[-2:] != '____']):
        if method_groups == ():
            method_groups = {
                    key for key, value in self.class_directory().items()
                    if hasattr(value, 'keys')
                    & (key != 'shared attributes')
                             }
        return {method_name: method for group_name, method_dictionary in self.method_groups(filter_function=filter_function).items() 
                for method_name, method in method_dictionary.items()}




    def module_classes(self):
        return get_things_from_dir(self.target_module, 
                                   type, 
                                   filter_function=lambda group: [x for x in group if x not in self.module_imported_names()]
                                   )




    def module_functions(self, *function_groups, filter_function=None):
        if (filter_function == None) & (function_groups == ()):
            filter_function = lambda group: {x for x in group if (x[:2]+x[-2:] != '____')}
        elif filter_function == None:
            filter_function = lambda group: {function_name for value in [value for key, value in self.module_directory('Module Functions').items()
                                                                         if hasattr(value, 'keys')
                                                                         & (key in function_groups)
                                                                         & (key[:2]+key[-2:] != '____')]
                                             for function_name in value.keys()
                                             }
        elif function_groups == ():
            pass
        else:
            # in this case, both method groups and filter_function are something
            lambda_filter = filter_function
            group_filter = lambda group: {function_name for value in [value for value in self.module_directory('Module Functions').values()
                                                                      if hasattr(value, 'keys')]
                                          for function_name in value.keys()
                                          }
            filter_function = lambda group: {x for x in group 
                                             if (x in lambda_filter(group)) 
                                             & (x in group_filter(group))
                                            }
        # ignoring names in module imports
        final_filter_function = lambda group: {x for x in group 
                                               if (x in filter_function(group)) 
                                               & (x not in self.module_imported_names())
                                               }
        return get_things_from_dir(self.target_module, types.FunctionType, filter_function=final_filter_function)




    def module_directory(self, *keys, output_filter=lambda output: output):
        return output_filter(eval('self.__module_directory__' + ''.join([f"['{key}']" for key in keys])))




    def class_directory(self, *args):
        return self.module_directory('Module Classes', self.target_class.__name__, *args)




    def module_attributes(self, filter_function=lambda group: [x for x in group if (x[:2]+x[-2:] != '____')]):
        if filter_function == None:
            filter_function = lambda group: group
        full_filter_function = lambda group: [x for x in filter_function(group) if x not in self.module_imported_names()]
        def not_these_things(x):
            for t in {types.BuiltinFunctionType, types.BuiltinMethodType, 
                      types.FunctionType, types.GeneratorType, types.LambdaType, 
                      types.MethodType, types.ModuleType, type}:
                if isinstance(x, t):
                    return False
            return True
        return get_things_from_dir(self.target_module, not_these_things, filter_function=full_filter_function)





#  +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
#  |                  _   _               _                   _    __                  _   _                                     _             _       _   _                   |
#  |                 | | | |             | |                 | |  / _|                | | (_)                                   (_)           | |     | | (_)                  |
#  |   _ __ ___   ___| |_| |__   ___   __| |   __ _ _ __   __| | | |_ _   _ _ __   ___| |_ _  ___  _ __    _ __ ___   __ _ _ __  _ _ __  _   _| | __ _| |_ _  ___  _ __  ___   |
#  |  | '_ ` _ \ / _ \ __| '_ \ / _ \ / _` |  / _` | '_ \ / _` | |  _| | | | '_ \ / __| __| |/ _ \| '_ \  | '_ ` _ \ / _` | '_ \| | '_ \| | | | |/ _` | __| |/ _ \| '_ \/ __|  |
#  |  | | | | | |  __/ |_| | | | (_) | (_| | | (_| | | | | (_| | | | | |_| | | | | (__| |_| | (_) | | | | | | | | | | (_| | | | | | |_) | |_| | | (_| | |_| | (_) | | | \__ \  |
#  |  |_| |_| |_|\___|\__|_| |_|\___/ \__,_|  \__,_|_| |_|\__,_| |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_| |_| |_| |_|\__,_|_| |_|_| .__/ \__,_|_|\__,_|\__|_|\___/|_| |_|___/  |
#  |                                                                                                                              | |                                          |
#  |                                                                                                                              |_|                                          |
#  +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
#  method group: method and function manipulations

    def commit_str(self, function=None):
        if function == None: 
            return self.commit_method(self.__calling_env_globals__['__str__'])
        else:
            return self.commit_method(function, method_name='__str__')




    def get_init(self): return self.get_method('__init__')


    def add_pseudo_imported_names(self, text):
        for name in (
                set(self.module_attributes().keys())
                .union(set(self.module_functions().keys()))
                .union(self.module_imported_names())
                .union(set(self.module_classes().keys()))
                     ):
            text = re.sub(
                pattern = fr"(?<=[^\w\.]){name}(?=[^\w])", 
                repl = f"pseudo_imported_names['{self.target_module.__name__}.{self.target_class.__name__}']['{name}']",
                string = text
                          )
        return text


    def get_method(self, method_name, return_text=False, print_method=True, return_path=False):
        path = [x[0] for x in os.walk(self.__class_root__)
                if method_name+'.method' in x[2]
               ]
        assert len(path) != 0, f'Method, {method_name}, does not exist!'
        assert len(path) == 1, f'Method, {method_name}, is not unique, Solomon broke something, or you messed with the folders manually'
        path = os.path.join(path[0], method_name+'.method')
        with open(path) as flasdfkjerkjas:
            method_text = flasdfkjerkjas.read()
        if print_method: print(method_text)
        if return_text & return_path: 
            return (method_text, path)
        elif return_text:
            return method_text
        elif return_path:
            return path




    def commit_function(self, function, group_name=None, function_name=None, function_text=None):
        if function_name==None: 
            function_name = function.__name__
        # Find old function location
        old_path = [os.path.join(folder, file)
             for folder, subfolders, files in os.walk(self.__module_root__)
             for file in files
             if file == function_name+'.function']
        assert len(old_path) < 2 , f"{function_name} exists more than once in development_mods, please remove one copy"
        # remove from old location
        if len(old_path) == 1:
            old_path = old_path[0]
            os.remove(old_path)
        # find new location
        if (group_name == None) & (old_path != []):
            new_path = old_path
        elif group_name != None:
            new_path = os.path.join(self.__module_root__, f"{group_name}.function_group", f"{function_name}.function")
        else:
            new_path = os.path.join(self.__module_root__, f"{function_name}.function")
        # Get function text
        if function_text == None:
            function_text = getsource(function)
        # Change function_text name to 'function_name'
        if function_name != function.__name__:
            function_text = re.sub(r"(?<=def )\w*", function_name, function_text)
        # Write to file
        with open(new_path, 'w') as flasdfkjerkjas:
            flasdfkjerkjas.write(function_text)
        # bring into module environment
        exec(function_text, globals())
        # set to module
        setattr(self.target_module, function_name, eval(function_name))
        # remove from directory
        if old_path != []:
            group_in_list = __extract_from_path_by_tag__(old_path, 'function_group')
            assert len(group_in_list) < 2
            self.module_directory('Module Functions', *group_in_list).pop(function_name)
        # add to directory
        group_in_list = __extract_from_path_by_tag__(new_path, 'function_group')
        assert len(group_in_list) < 2
        self.module_directory('Module Functions', *group_in_list)[function_name] = function_text
        self.__save_module_directory__()
        return self




    def get_str(self): return self.get_method('__str__')


    def commit_method(self, unbound_method, group_name=None, method_name=None, method_text=None):
        if method_name==None: 
            method_name = unbound_method.__name__
        # Find old method location
        old_path = [os.path.join(folder, file)
             for folder, subfolders, files in os.walk(self.__class_root__)
             for file in files
             if file == method_name+'.method']
        assert len(old_path) < 2 , "Method exists more than once in development_mods, please remove one copy"
        # remove from old location
        if len(old_path) == 1:
            old_path = old_path[0]
            os.remove(old_path)
        # Get Method Text
        if method_text == None:
            method_text = getsource(unbound_method)
        # Change method_text method name to 'method_name'
        if method_name != unbound_method.__name__:
            method_text = re.sub(fr"(?<=def )\w*", method_name, method_text)
        # Write to file
        with open(os.path.join(self.__class_root__, f"{method_name}.method"), 'w') as flasdfkjerkjas:
            flasdfkjerkjas.write(method_text)
        # remove from directory
        if old_path != []:
            group_in_list = __extract_from_path_by_tag__(old_path, 'method_group')
            assert len(group_in_list) < 2
            self.class_directory(*group_in_list).pop(method_name)
        # add to directory
        self.class_directory()[method_name] = method_text
        self.__save_module_directory__()
            # move to group
        if group_name != None:
            if group_name in self.method_groups():
                self.add_to_method_group(group_name, method_name)
            else:
                self.add_method_group(group_name, method_name)
        # alter text for pseudonymous names
        method_text = self.add_pseudo_imported_names(method_text)
        exec(method_text, globals(), locals())
        # set method to class and instances of class
        setattr(self.target_class, method_name, eval(method_name))
        for key, value in self.instances().items():
            setattr(value, method_name, types.MethodType(eval(method_name), value))

        return self




    def commit_init(self, function=None):
        if function == None: 
            return self.commit_method(self.__calling_env_globals__['__init__'])
        else: 
            return self.commit_method(function, method_name='__init__')




    def commit_repr(self, function=None):
        if function == None: 
            return self.commit_method(self.__calling_env_globals__['__repr__'])
        else: 
            return self.commit_method(function, method_name='__repr__')




    def delete_functions(self, *function_names):
        for function_name in function_names:
            # Find the function location
            old_path = [
                    os.path.join(folder, file)
                    for folder, subfolders, files in os.walk(self.__module_root__)
                    for file in files
                    if file == function_name+'.function'
                        ]
            assert len(old_path) != 0 , f"Function, {function_name}, does not exist"
            assert len(old_path) == 1 , f"Function, {fucntion_name} exists more than once in directory"
            old_path = old_path[0]
            # Delete .function file
            os.remove(old_path)
            # delete from module
            delattr(self.target_module, function_name)
            # delete from class_directory
            group_in_list = __extract_from_path_by_tag__(old_path, 'function_group')
            self.module_directory('Module Functions', *group_in_list).pop(function_name)
        self.__save_module_directory__()
        return self




    def get_repr(self): return self.get_method('__repr__')




    def get_function(self, function_name, return_text=False, print_function=True, return_path=False):
        path = [x[0] for x in os.walk(self.__module_root__)
                if function_name+'.function' in x[2]
               ]
        assert len(path) != 0, f'Function, {function_name}, does not exist!'
        assert len(path) == 1, f'Function, {function_name}, is not unique, Solomon broke something, or you messed with the folders manually'
        path = os.path.join(path[0], f"{function_name}.function")
        with open(path) as flasdfkjerkjas:
            function_text = flasdfkjerkjas.read()
        if print_function: print(function_text)
        if return_text & return_path: 
            return (function_text, path)
        elif return_text:
            return function_text
        elif return_path:
            return path




    def method_exists(self, method_name):
        path = [
                    x[0] for x in os.walk(self.__class_root__)
                    if f"{method_name}.method" in x[2]
                ]
        assert len(path) < 2
        return len(path) == 1




    def delete_methods(self, *method_names):
        for method_name in method_names:
            # Find the method location
            old_path = [os.path.join(folder, file)
             for folder, subfolders, files in os.walk(self.__class_root__)
             for file in files
             if file == method_name+'.method']
            assert len(old_path) != 0 , f"Method, {method_name}, does not exist"
            assert len(old_path) == 1 , "Method exists more than once in directory"
            old_path = old_path[0]
            # Delete .method file
            os.remove(old_path)
            # delete from class itself
            delattr(self.target_class, method_name)
            # delete from instances of class
            for instance in self.instances().values():
                delattr(instance, method_name)
            # delete from class_directory
            group_in_list = __extract_from_path_by_tag__(old_path, 'method_group')
            self.class_directory(*group_in_list).pop(method_name)
        self.__save_module_directory__()
        return self





#  +---------------------------------------------------------------------------------------------------+
#  |                   _                                                   _   _               _       |
#  |                  | |                                                 | | | |             | |      |
#  |   _   _ _ __   __| | ___ _ __ ___  ___ ___  _ __ ___   _ __ ___   ___| |_| |__   ___   __| |___   |
#  |  | | | | '_ \ / _` |/ _ \ '__/ __|/ __/ _ \| '__/ _ \ | '_ ` _ \ / _ \ __| '_ \ / _ \ / _` / __|  |
#  |  | |_| | | | | (_| |  __/ |  \__ \ (_| (_) | | |  __/ | | | | | |  __/ |_| | | | (_) | (_| \__ \  |
#  |   \__,_|_| |_|\__,_|\___|_|  |___/\___\___/|_|  \___| |_| |_| |_|\___|\__|_| |_|\___/ \__,_|___/  |
#  +---------------------------------------------------------------------------------------------------+
#  method group: underscore methods

    def __init__(self, _class_, env_globals, new=False, overwrite=True, verbose=True):
        self.verbose = verbose
        self.__calling_env_globals__ = env_globals
        if isinstance(_class_, str):
            assert new == True, "If this is a new class, set new=True, if not, _class_ should not be a string"
            self.__make_new_class__(_class_)
        else:
            self.target_class = _class_
        self.__get_target_module__()
        self.__get_module_imports__()
        self.__get_roots__()
        self.__get_module_directory__(new, overwrite)
        if overwrite == True:
            self.delete_module()
            self.__write_module_cascading_directories__()
        elif new == True:
            self.__write_module_cascading_directories__()
        self.construct_pseudo_imported_names()




    def __underscore_methods__(self):
        return get_things_from_dir(
                        target = self.target_class, 
                        object_type = types.FunctionType,
                        filter_function = lambda l: [x for x in l if (x[:2]+x[-2:] == '____')]
                                    )




    def __get_roots__(self):
        self.__module_root__ = os.path.join(self.developer_root, *[f"{x}.module" for x in self.target_module.__name__.split('.')])
        self.__class_root__ = os.path.join(self.__module_root__, f"{self.target_class.__name__}.class")
        module_cascade = self.target_module.__name__.split('.')
        if len(module_cascade) == 1:
            self.__src_module_root__ = os.path.join(self.src_package_root, f"{module_cascade[0]}.py")
        else:
            higher_modules = module_cascade[:-1]
            this_module = module_cascade[-1]
            self.__src_module_root__ = os.path.join(self.src_package_root, *higher_modules, f"{this_module}.py")
        return self




    def __get_module_directory__(self, new, overwrite):
        if new|overwrite:
            with open(self.__src_module_root__, 'r') as flasdfkjerkjas:
                text = flasdfkjerkjas.read()
            self.__module_directory__ = __parse_by_ascii_headings__(text, self.verbose)
        else:
            path = os.path.join(self.__module_root__, 'module_directory.directory')
            with open(path, 'r') as flasdfkjerkjas:
                self.__module_directory__ = eval(flasdfkjerkjas.read())
        self.__assert_that_class_dictionary_match_module_directory__()
        return self




    def __get_module_imports__(self):
        text = getsource(self.target_module)
        # Removing comments from text
        text = '\n'.join([x for x in [line for line in text.splitlines() 
                                      if line.strip() != ''
                                      ]
                          if (x.strip()[0] != '#')
                         ])
        # Removing quoted things
        text = remove_quoted_things(text)
        # Finding lines with import
        import_lines = [line for line in text.splitlines() if ' import ' in f" {line} "]
        assert '*' not in ''.join(import_lines), "import statements containing * are not yet supported by package_developer"
        # get import names for each line
        self.__module_imports__ =  {
                    import_line: get_import_names_from_text(import_line) 
                    for import_line in import_lines
                                    }
        return self




    def __get_target_module__(self):
        # possible module names depending on import 
        possible_names_and_tails = [
                (name, self.target_class.__module__.replace(name, ''))
                for name in {'.'.join(self.target_class.__module__.split('.')[::-1][i:][::-1])
                             for i in range(len(self.target_class.__module__.split('.')))
                             }               
                                    ]
        matched_aliases = []                            
        for name, tail in possible_names_and_tails:
            search = {
                key
                for key, value in {k: v
                                   for k, v in self.env_globals().items()
                                   if hasattr(v, '__name__')
                                   }.items()
                if value.__name__ == name
                      }
            if len(search) > 0:
                assert len(search) == 1, 'Multiple imports of module not supported\n' + f"{search = }"
                # add match to matches
                matched_aliases.append((search.pop(), tail))
        # case when matches exist
        if len(matched_aliases) != 0:
            # We would like to have only one match
            assert len(matched_aliases) <= 1, 'Multiple imports of module not supported'
            # replaceing env name with module name to get module alias
            alias, tail = matched_aliases[0]
            self.target_module = eval(f"self.env_globals()[alias]{tail}")
        # case when no matches...maybe module wasn't imported but only class
        else:
            # Import the target module to this modules environment
            module_cascade = self.target_class.__module__.split('.')
            if len(module_cascade) == 1:
                import_program = f"import {module_cascade[0]} as module_imported_to_developer_module"
            else:
                import_program = f"from {'.'.join(module_cascade[:-1])} import {module_cascade[-1]} as module_imported_to_developer_module"
            exec(import_program, globals())
            # assign the attribute
            setattr(self, 'target_module', module_imported_to_developer_module)
        return self




    def __save_module_directory__(self):
        print(os.path.join(self.__module_root__, 'module_directory.directory'))
        with open(os.path.join(self.__module_root__, 'module_directory.directory'), 'w') as flasdfkjerkjas:
            flasdfkjerkjas.write(__print_nice_dictionary__(self.module_directory()))
        return self




    def __make_new_class__(self, class_import_statement):
        class_import_statement
        target_class = class_import_statement.split(' as ')[0]
        target_class_list = target_class.split('.')
        assert len(target_class_list) > 1, "cannot assign a class without a module, _class_ should be at a minimum 'module_name.class_name'"
        module_cascade = ['.'.join(target_class_list[:i])
                          for i in range(1, len(target_class_list))[::-1]
                         ]
        class_name = target_class_list[-1]
        # seeing if any levels of the module_cascade exist
        def does_module_exist(module):
            try:
                exec(f"import {module} as nonsensical_import_alias", globals())
                return True
            except ModuleNotFoundError:
                print(f"{module} not found")
                return False
        existing_module = next((x for x in module_cascade if does_module_exist(x) == True), None)
        print(f"{existing_module = }")
        # existing module must be a package, unless it is the final module itself
        if existing_module != None:
            if ((os.path.basename(nonsensical_import_alias.__file__) != '__init__.py')
              & (existing_module != module_cascade[0])):
                # make module_name a directory, and rename module_name.py as __init__.py
                new_package_path = os.path.join(
                        os.path.dirname(nonsensical_import_alias.__file__),
                        os.path.basename(nonsensical_import_alias.__file__)[:-3]
                                                )
                print(f"making new directory: {new_package_path = }")
                os.mkdir(new_package_path)
                with open(nonsensical_import_alias.__file__) as f:
                    module_text = f.read()
                with open(os.path.join(new_package_path, '__init__.py'), 'x') as f:
                    f.write(module_text)
                os.rename(nonsensical_import_alias.__file__, 
                          os.path.join(new_package_path, f"copy_of__{os.path.basename(nonsensical_import_alias.__file__)[:-3]}__.py")
                          )
        # make packages between existing_module and target_module
        if existing_module == None:
            new_packages = module_cascade[1:]
        else:
            new_packages = module_cascade[1:module_cascade.index(existing_module)][::-1]
        for np in new_packages:
            os.mkdir(os.path.join(self.src_package_root, *np.split('.')))
            with open(os.path.join(self.src_package_root, *np.split('.'), '__init__.py'), 'x') as f:
                pass
        # make target module
        if existing_module != module_cascade[0]:
            target_module_path = os.path.join(
                                    self.src_package_root, 
                                    *module_cascade[0].split('.')[:-1],
                                    module_cascade[0].split('.')[-1] + '.py'
                                              )
            with open(os.path.join(self.developer_root, 'blank_sourceable_module.template'), 'r') as template:
                with open(target_module_path, 'x') as f:
                    f.write(template.read() + 
                            '\n' + 
                            render_class_heading(target_class_list[-1]) + 
                            "\n\n" + 
                            "class " + target_class_list[-1] + ":\n    pass"
                            )
        # remove nonsensical_import_alias
        if 'nonsensical_import_alias' in globals():
            reload(nonsensical_import_alias)
            globals().pop('nonsensical_import_alias')
        # import new_class
        __module__ = '.'.join(target_class_list[:-1])
        __class__ = target_class_list[-1]
        if ' as ' in class_import_statement:
            alias = class_import_statement.split(' as ')[1]
            exec(f"from {__module__} import {__class__} as {alias}", globals())
        else:
            exec(f"from {__module__} import {__class__}")
            alias = __class__
        # add to calling environment globals()
        self.__calling_env_globals__[alias] = eval(alias)
        self.target_class = eval(alias)




    def __assert_that_class_dictionary_match_module_directory__(self):
        # module imports
        assert self.module_directory('Module Imports') == self.module_imports()
        # module attributes
        module_attributes = self.module_attributes(lambda group: [x for x in group if x not in {'__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__'}])
        ###assert module_attributes().keys() == self.module_directory('Module Attributes').keys()
        # module functions
        ungrouped_functions = self.module_directory(
                                    'Module Functions',
                                     output_filter = lambda d: {
                                              x for key in {k for k in d.keys() if hasattr(d[k], 'keys')} 
                                              for x in d[key].keys()
                                                                }
                                                   )
        grouped_functions = self.module_directory('Module Functions', output_filter = lambda d: {k for k in d.keys() if hasattr(d[k], 'keys') == False})
        ###assert set(self.module_functions().keys()) == ungrouped_functions.union(grouped_functions)
        # module classes
        assert self.module_directory('Module Classes').keys() == self.module_classes().keys()
        # class_methods
        assert set(self.methods(filter_function = lambda g: g).keys()) == {
            method for key in {k for k in self.module_directory('Module Classes', self.target_class.__name__).keys()
                               if isinstance(self.module_directory('Module Classes', self.target_class.__name__, k), dict)
                              }
            for method in self.module_directory('Module Classes', self.target_class.__name__, key).keys()
            if key != 'shared attributes'
        }.union({
            k for k in self.module_directory('Module Classes', self.target_class.__name__).keys()
            if isinstance(self.module_directory('Module Classes', self.target_class.__name__, k), dict) == False
                })
        # class shared attributes
        assert self.shared_attributes().keys() == self.module_directory('Module Classes', self.target_class.__name__, 'shared attributes').keys()
        return None





#  +-----------------------------------------------------------------------------------+
#  |                               _     _               _   _     _                   |
#  |                              (_)   (_)             | | | |   (_)                  |
#  |    ___  _ __ __ _  __ _ _ __  _ _____ _ __   __ _  | |_| |__  _ _ __   __ _ ___   |
#  |   / _ \| '__/ _` |/ _` | '_ \| |_  / | '_ \ / _` | | __| '_ \| | '_ \ / _` / __|  |
#  |  | (_) | | | (_| | (_| | | | | |/ /| | | | | (_| | | |_| | | | | | | | (_| \__ \  |
#  |   \___/|_|  \__, |\__,_|_| |_|_/___|_|_| |_|\__, |  \__|_| |_|_|_| |_|\__, |___/  |
#  |              __/ |                           __/ |                     __/ |      |
#  |             |___/                           |___/                     |___/       |
#  +-----------------------------------------------------------------------------------+
#  method group: organizing things

    def add_function_group(self, group_name, *functions_to_include):
        # Make directory
        path = os.path.join(self.__module_root__, f"{group_name}.function_group")
        assert os.path.isdir(path) == False, "Function group already exists, use method add_to_function_group to add functions to this group"
        os.mkdir(path)
        # add to attribute method_groups
        self.module_directory('Module Functions')[group_name] = {}
        # move methods from other places
        self.add_to_function_group(group_name, *functions_to_include)
        self.__save_module_directory__()
        return self




    def delete_module(self):
        path = self.__module_root__
        if os.path.isdir(path)==False:
            print('Module does not exist in developement mods!\nNothing deleted')
        else:
            file_list = os.walk(path, topdown=False)
            for d, sub_d, files in file_list:
                for f in files: os.remove(os.path.join(path, d, f))
                os.rmdir(d)
            print(f"{self.target_module.__name__} removed from development_mods.")
        return self




    def ungroup_methods(self, *methods_to_include):
        for method in methods_to_include:
            text, old_path = self.get_method(method, return_text=True, return_path=True, print_method=False)
            assert os.path.isfile(old_path), f"{method} does not exist."
            new_path = os.path.join(self.__class_root__, f"{method}.method")
            # remove old file
            os.remove(old_path)
            # make new file
            with open(new_path, 'w') as flasdfkjerkjas:
                flasdfkjerkjas.write(text)
            # find method in class directory
            group_matches = {key for key, value in {
                                            key: value 
                                            for key, value in self.class_directory().items() 
                                            if hasattr(value, 'keys')
                                                    }.items()
                             if method in value.keys()
                             }
            assert group_matches != {}, f"{method} not in any group. May be ungrouped already, or may not exist"
            assert len(group_matches) == 1, f"class_directory has method more than once"
            old_group = group_matches.pop()
            method_text_from_directory = self.class_directory()[old_group].pop(method)
            assert method_text_from_directory == text
            # add method class_directory
            self.class_directory()[method] = method_text_from_directory
        self.__save_module_directory__()
        return self




    def add_to_function_group(self, group_name, *functions_to_include):
        for function in functions_to_include:
            text, old_file = self.get_function(function, return_text=True, return_path=True, print_function=False)
            group_path = os.path.join(self.__module_root__, f"{group_name}.function_group")
            assert os.path.isdir(group_path), f"function_group does not exist. use {self.__name__}.add_function_group"
            # add text to new file
            with open(os.path.join(group_path, f"{function}.function"), 'w') as flasdfkjerkjas:
                flasdfkjerkjas.write(text)
            # remove old file
            os.remove(old_file)
            # find function in module directory
            group_matches = {
                        key for key, value in {key: value 
                                               for key, value in self.module_directory('Module Functions').items() 
                                               if hasattr(value, 'keys')
                                               }.items()
                        if function in value.keys()
                            }
            assert len(group_matches) < 2, f"class_dirctory has method more than once"
            # remove from module_directory
            function_text_from_directory = self.module_directory('Module Functions', *group_matches).pop(function)
            assert function_text_from_directory == text
            # add to module directory
            self.module_directory('Module Functions', group_name)[function] = function_text_from_directory
        self.__save_module_directory__()
        return self




    def add_method_group(self, group_name, *methods_to_include):
        # Make directory
        path = os.path.join(self.__class_root__, f"{group_name}.method_group")
        assert os.path.isdir(path) == False, "Method group already exists, use method add_to_method_group to add methods to this group"
        os.mkdir(path)
        # add to attribute method_groups
        self.class_directory()[group_name] = {}
        # move methods from other places
        self.add_to_method_group(group_name, *methods_to_include)
        self.__save_module_directory__()
        return self




    def add_to_method_group(self, group_name, *methods_to_include):
        for method in methods_to_include:
            text, old_file = self.get_method(method, return_text=True, return_path=True, print_method=False)
            group_path = os.path.join(self.__class_root__, f"{group_name}.method_group")
            assert os.path.isdir(group_path), f"method_group does not exist. use {self.__name__}.add_method_group"
            # remove old file
            os.remove(old_file)
            # add text to new file
            with open(os.path.join(group_path, f"{method}.method"), 'w') as flasdfkjerkjas:
                flasdfkjerkjas.write(text)
            # find method in class directory
            group_matches = {key for key, value in {
                                            key: value 
                                            for key, value in self.class_directory().items() 
                                            if hasattr(value, 'keys')
                                                    }.items()
                             if method in value.keys()
                             }
            print(f"{group_matches = }")
            assert len(group_matches) < 2, f"class_directory has method more than once"
            # remove from class_directory
            method_text_from_directory = self.class_directory(*group_matches).pop(method)
            print(method_text_from_directory)
            assert method_text_from_directory == text
            # add method to group_name
            self.class_directory(group_name)[method] = method_text_from_directory
        self.__save_module_directory__()
        return self




    def ungroup_functions(self, *functions_to_include):
        for function in functions_to_include:
            text, old_path = self.get_function(function, return_text=True, return_path=True, print_function=False)
            assert os.path.isfile(old_path), f"{function} does not exist."
            new_path = os.path.join(self.__module_root__, f"{function}.function")
            # remove old file
            os.remove(old_path)
            # make new file
            with open(new_path, 'w') as flasdfkjerkjas:
                flasdfkjerkjas.write(text)
            # find method in class directory
            group_matches = {key for key, value in {
                                            key: value 
                                            for key, value in self.module_directory('Module Functions').items() 
                                            if hasattr(value, 'keys')
                                                    }.items()
                             if function in value.keys()
                             }
            assert group_matches != {}, f"{function} not in any group. May be ungrouped already, or may not exist"
            assert len(group_matches) == 1, f"module_dirctory has function more than once"
            old_group = group_matches.pop()
            function_text_from_directory = self.module_directory('Module Functions')[old_group].pop(function)
            assert function_text_from_directory == text
            # add method class_directory
            self.module_directory('Module Functions')[function] = function_text_from_directory
        self.__save_module_directory__()
        return self




    def delete_function_group(self, group_name: str, send_to_top: Union[bool, str] =True):
        """
            Deletes a method group.
            if send_to_top == True, all functions in the group will remain, but will be ungrouped functions
            if send_to_top == False, all functions will be deleted, and will no longer be available to module or its objects
            if send_to_top == 'some other group', all functions will be moved to the group 'some other group'
                    """
        assert isinstance(group_name, str) & (isinstance(send_to_top, bool) | isinstance(send_to_top, str))
        # delete functions if send_to_top == False
        if send_to_top == False:
            self.delete_functions(*self.function_groups()[group_name].keys())
        # Send methods where they need to go
        if send_to_top == True: 
            self.ungroup_functions(*self.function_groups()[group_name].keys())
        else:
            self.add_to_function_group(where_to_send, *self.method_groups[group_name].keys())     
        # Removing file directory
        os.rmdir(os.path.join(self.__module_root__, f"{group_name}.function_group"))
        # removing from class directory
        self.module_directory('Module Functions').pop(group_name)
        self.__save_module_directory__()
        return self




    def delete_method_group(self, group_name: str, send_to_top: Union[bool, str] =True):
        """
            Deletes a method group.
            if send_to_top == True, all methods in the group will remain, but will be ungrouped methods
            if send_to_top == False, all methods will be deleted, and will no longer be available to the class, or instances
            if send_to_top == 'some other group', all methods will be moved to the group 'some other group'
                    """
        assert isinstance(group_name, str) & (isinstance(send_to_top, bool) | isinstance(send_to_top, str))
        # delete methods if send_to_top == False
        if send_to_top == False:
            self.delete_methods(*self.method_groups()[group_name].keys())
        # Send methods where they need to go
        if send_to_top == True: 
            self.ungroup_methods(*self.method_groups()[group_name].keys())
        else:
            self.add_to_method_group(send_to_top, *self.method_groups()[group_name].keys())     
        # Removing file directory
        os.rmdir(os.path.join(self.__class_root__, f"{group_name}.method_group"))
        # removing from class directory
        self.class_directory().pop(group_name)
        self.__save_module_directory__()
        return self






#  +-------------------------------------------------------------------------------------------+
#  |-------------------------------------------------------------------------------------------|
#  |-------------------------------------------------------------------------------------------|
#  |                       888           888                                                   |
#  |                       888           888                                                   |
#  |                       888           888                                                   |
#  |  88888b.d88b.  8888b. 888888 .d8888b88888b.    888  888  888   88888b.  .d88b. .d8888b    |
#  |  888 "888 "88b    "88b888   d88P"   888 "88b   888  888  888   888 "88bd88""88b88K        |
#  |  888  888  888.d888888888   888     888  888   888  888  888   888  888888  888"Y8888b.   |
#  |  888  888  888888  888Y88b. Y88b.   888  888   Y88b 888 d88P   888 d88PY88..88P     X88   |
#  |  888  888  888"Y888888 "Y888 "Y8888P888  888    "Y8888888P"    88888P"  "Y88P"  88888P'   |
#  |                                                                888                        |
#  |                                                                888                        |
#  |                                                                888                        |
#  |-------------------------------------------------------------------------------------------|
#  |-------------------------------------------------------------------------------------------|
#  +-------------------------------------------------------------------------------------------+

class match_w_pos:
    
    def __init__(self, match, start, end):
        self.match = match
        self.start = start
        self.end = end
        
    def __repr__(self):
        if ("'" in self.match) & ('"' not in self.match):
            return f'<match_with_pos object, "{self.match[:25]}">'
        replacement = "\\'"
        return f"""<match_with_pos object, '{self.match[:25].replace("'", replacement)}'>"""


#  +----------------------------------------------------------------------------------------------------------------------------------------+
#  |----------------------------------------------------------------------------------------------------------------------------------------|
#  |----------------------------------------------------------------------------------------------------------------------------------------|
#  |  888          d8b        888                                   888              888                          888                       |
#  |  888          Y8P        888                                   888              888                          888                       |
#  |  888                     888                                   888              888                          888                       |
#  |  888888888d88888888888b. 888 .d88b.     .d88888888  888 .d88b. 888888 .d88b.    888888888d888 8888b.  .d8888b888  888 .d88b. 888d888   |
#  |  888   888P"  888888 "88b888d8P  Y8b   d88" 888888  888d88""88b888   d8P  Y8b   888   888P"      "88bd88P"   888 .88Pd8P  Y8b888P"     |
#  |  888   888    888888  88888888888888   888  888888  888888  888888   88888888   888   888    .d888888888     888888K 88888888888       |
#  |  Y88b. 888    888888 d88P888Y8b.       Y88b 888Y88b 888Y88..88PY88b. Y8b.       Y88b. 888    888  888Y88b.   888 "88bY8b.    888       |
#  |   "Y888888    88888888P" 888 "Y8888     "Y88888 "Y88888 "Y88P"  "Y888 "Y8888     "Y888888    "Y888888 "Y8888P888  888 "Y8888 888       |
#  |                  888                        888                                                                                        |
#  |                  888                        888                                                                                        |
#  |                  888                        888                                                                                        |
#  |----------------------------------------------------------------------------------------------------------------------------------------|
#  |----------------------------------------------------------------------------------------------------------------------------------------|
#  +----------------------------------------------------------------------------------------------------------------------------------------+

class triple_quote_tracker:
    
    def __init__(self, text):
        self.lines = iter(text.splitlines())
        self.hanging_triples = None
        self.line_number = -1
        self.line_position = -1
        self.prev_line_hanging = False
        
    
    def next(self):
        try:
            self.line = next(self.lines)
            self.line_number += 1
            self.line_position = 0
        except StopIteration:
            #print('Iteration Complete')
            self.line_number = None
            self.line_position = None
        return self
        
    
    def get_next_match_in_line(self):
        #print(self.line_position)
        line_tail = self.line[self.line_position:]
        #print(f"{line_tail = }")
        #print(f"{self.hanging_triples = }")
        if self.hanging_triples == None:
            match = re.search(r"(\"\"\"|''')", line_tail)
            #print(f"{match = }")
            if match == None:
                self.line_position = None
            else:
                self.hanging_triples = match.group()
                self.line_position += match.end()
                #print(f"{match.group() = }")
        else:
            pattern = fr"({self.hanging_triples})"
            match = re.search(pattern, line_tail)
            #print(f"{match = }")
            if match == None:
                self.line_position = None
                return None
            else:
                self.hanging_triples = None
                self.line_position += match.end()
                #print(f"{match.group() = }")
        return self

        
    def check_line(self):
        while self.line_position != None:
            self.get_next_match_in_line()
            
        return self
    
    def check_next(self):
        #print('---------------------------------')
        if self.hanging_triples == None:
            self.prev_line_hanging = False
        else:
            self.prev_line_hanging = True
        return self.next().check_line()
