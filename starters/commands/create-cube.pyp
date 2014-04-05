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
    py-cinema4dsdk/starters/commands/create-cube.pyp
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    description: This plugin command creates a Cube object and places
           it at the position of the selected object. If there is
           no active object, it is placed at the world's origin.
    tags: command simple muchdoc
    level: beginner
"""

# Import the c4d module which is our connection to Cinema 4D.
import c4d

# This number is the unique ID that is assigned to the plugin. Every
# plugin must have a unique ID which can be obtained from
# http://plugincafe.com/forum/developer.asp
PLUGIN_ID = 1031975

class CreateCubeCommand(c4d.plugins.CommandData):
    r""" This class implements the behavior of the command plugin
    and is registered to Cinema 4D later. """

    def Register(self):
        r""" It is good practice to keep the registration tied
        to the class that will be registered. """

        help_string = 'C++ SDK Example Command Plugin: Creates a cube and ' \
                      'assigns the matrix of the selected object to it.'

        return c4d.plugins.RegisterCommandPlugin(
                PLUGIN_ID,                   # The Plugin ID, obviously
                "starters/commands/Create Cube",  # The name of the plugin
                c4d.PLUGINFLAG_COMMAND_HOTKEY,    # Sort of options
                None,                        # Icon, None here
                help_string,                 # The help text for the command
                self,                        # The plugin implementation
        )

    # c4d.plugins.CommandData

    def Execute(self, doc):
        r""" This method is called when the command is executed by the
        user or a by another script. *doc* is the active scene visible
        in Cinema 4D. """

        # We first create the cube by allocating a BaseObject with
        # the Plugin ID of the cube objectself.
        cube = c4d.BaseObject(c4d.Ocube)

        # Next, we'll get the currently selected object (which is
        # only when there is exactly one object selected).
        active_object = doc.GetActiveObject()

        # If we got one, we'll assign the global matrix of the
        # object (global position, scale & rotation) to the cube.
        if active_object:
            # Get the global matrix.
            mg = active_object.GetMg()

            # And set it as the local matrix for the cube.
            cube.SetMl(mg)
        else:
            # The default matrix for an object is the local
            # origin, so we won't have to adjust that.
            pass

        # Then we tell the document to start an undo-step (we want
        # that the user can undo the creation of the cube).
        doc.StartUndo()

        # No matter what happens, the undo should be closed again.
        # We'll better be safe than sorry (good practice, too).
        # The finally clause will end the undo.
        try:
            # Insert the object into the document (aka scene).
            doc.InsertObject(cube)

            # Tell the cube that it was just inserted into
            # the document (some primitives, such as the sphere, creat
            # a Phong Tag in this procedure).
            cube.Message(c4d.MSG_MENUPREPARE)

            # Tell the document that the cube was just added and
            # that should be included when undoing.
            doc.AddUndo(c4d.UNDOTYPE_NEW, cube)
        finally:
            # End the undo.
            doc.EndUndo()

            # Tell Cinema that something has changed (resulting in a
            # UI update). Needs to be called only once after everything
            # is complete (many beginners call it everytime they did
            # perform a change).
            c4d.EventAdd()

        # Return True to signal that everything's fine.
        return True

# Python scripts can be executed with different values for the
# __name__ variable. We only want to register the plugins when
# it equals '__main__'.
if __name__ == '__main__':
    # 1. Create an instance of the Command
    # 2. Register it to Cinema 4D
    CreateCubeCommand().Register()

