#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import re
from string import Template
from core.controller import Controller


def print_hint():
    print("""
Usage:
    python manage.py 
        - run
        - new filter [name]
        - new collector [name]
        - new processor [name]
    """)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "run":
            controller = Controller()
            controller.run()
            exit(0)
    elif len(sys.argv) == 4:
        name = sys.argv[3]
        template_path = 'templates/'
        target_directory = ""
        if sys.argv[1] != "new":
            print("Unknown command: " + " ".join(sys.argv))
            print_hint()
            exit(0)

        if sys.argv[2] == "filter":
            template_path += "filter.tmp"
            target_directory = "filters/"

        elif sys.argv[2] == "collector":
            template_path += "collector.tmp"
            target_directory = "collectors/"

        elif sys.argv[2] == "processor":
            template_path += "processor.tmp"
            target_directory = "processors/"

        else:
            print("Unknown command: " + " ".join(sys.argv))
            print_hint()
            exit(0)

        if not re.match("^[_|a-zA-Z][_|0-9a-zA-Z]*$", name):
            print("Invalid variable name: {}".format(name))
            exit(0)

        t_fname = name

        filename = ""
        if t_fname[0].isupper():
            t_fname = t_fname[0].lower() + t_fname[1:]
        for _s_ in t_fname:
            filename += _s_ if not _s_.isupper() else '_' + _s_.lower()

        ans = input("file name [Press enter to set as \"{}.py\"]: ".format(filename))

        if ans != "":
            filename = ans

        maxcount = 3
        while filename + ".py" in os.listdir(target_directory):
            filename = input("file name\"{}.py\" duplicates in the directory, please input again: ".format(filename))
            maxcount -= 1
            if maxcount <= 0:
                print("The number of input failures exceeds the limit")
                exit(0)
        target_file = target_directory + filename + ".py"
        with open(template_path, "r") as f:
            template = Template(f.read())

        with open(target_file, "w") as f:
            f.write(template.safe_substitute(dict(name=name)))

        print("New python file has been created as {}.".format(target_file))
        exit(0)

    print("Unknown command " + " ".join(sys.argv))
    print_hint()
