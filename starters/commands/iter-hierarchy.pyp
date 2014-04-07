# Copyright (c) 2014  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
r"""
    py-cinema4dsdk/starters/commands/iter-hierarchy.pyp
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    description: This plugin command demonstrates how to recursively
        iterate over a documents object hierarchy and print them to
        the console.
    tags: command simple muchdoc hierarchy-iteration recursion console
    level: beginner
    read-before: create-cube.cpp group-objects.cpp
"""

import c4d

PLUGIN_ID = 1031978

class IterHierarchyCommand(c4d.plugins.CommandData):

    def Register(self):
        help_string = 'C++ SDK Example Command Plugin: Demonstrates ' \
                      'working through the object tree recursively and ' \
                      'printing the hierarchly structure to the console.'

        return c4d.plugins.RegisterCommandPlugin(
                PLUGIN_ID,
                "starters/commands/Iter Hierarchy",
                c4d.PLUGINFLAG_COMMAND_HOTKEY,
                None,
                help_string,
                self,
        )

    # c4d.plugins.CommandData

    def Execute(self, doc):
        # Get a list of all the objects on the top-level of the scene.
        objects = doc.GetObjects()

        # Iterate over them and continue the procedure recursively.
        for op in objects:
            print_hierarchy(op)

        return True

def print_hierarchy(op, depth=0):
    # Print to the console the indentation (as defined by the
    # recursion `depth`) and the name of the object.
    print '    ' * depth + op.GetName()

    # Continue with the children of the current object with
    # an increased depth.
    for child in op.GetChildren():
        print_hierarchy(child, depth + 1)

if __name__ == '__main__':
    IterHierarchyCommand().Register()

