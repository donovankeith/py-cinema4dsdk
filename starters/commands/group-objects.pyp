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
    py-cinema4dsdk/starters/commands/group-objects.pyp
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    description: This plugin command groups all selected objects under a
            single Null object.
    tags: command simple muchdoc object-creation hierarchy-modifications undos
    level: beginner
    read-before: create-cube.cpp
"""

import c4d

PLUGIN_ID = 1031976

class GroupObjectsCommand(c4d.plugins.CommandData):

    def Register(self):
        help_string = 'Python Cinema 4D SDK Example Command: Groups the ' \
                      'selected objects by inserting them under a Null.'
        return c4d.plugins.RegisterCommandPlugin(
                PLUGIN_ID,
                "starters/commands/Group Objects",
                c4d.PLUGINFLAG_COMMAND_HOTKEY,
                None,
                help_string,
                self,
        )

    # c4d.plugins.CommandData

    def Execute(self, doc):

        # Get a list of all the selected objects in the Object
        # Manager (excluding the children of selected objects).
        objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)

        # Don't do anything if there are none selected.
        if not objects:
            return True

        # Create a new Null-Object that will serve as the new
        # parent for selected objects.
        root = c4d.BaseObject(c4d.Onull)

        # Create a new undo-step in the document.
        doc.StartUndo()

        # Try-finally clause to make sure the undo will be closed
        # even if an error occurs.
        try:
            # Iterate over all objects in the list and remove them
            # from their current position in the hierarchy. Then move
            # them to their new parent.
            for op in objects:

                # Tell the document that we are about to remove the
                # object from the document and then actually do it.
                doc.AddUndo(c4d.UNDOTYPE_DELETE, op)
                op.Remove()

                # And insert it under the new root object.
                op.InsertUnderLast(root)

            # Insert the root object into the document and tell
            # the object about it.
            doc.InsertObject(root)
            root.Message(c4d.MSG_MENUPREPARE)

            # And finally thell the document that the root Null-Object
            # is new so it will be included when undoing. We will
            # also set the object being the only selected one.
            doc.AddUndo(c4d.UNDOTYPE_NEW, root)
            doc.SetActiveObject(root)
        finally:
            # End the undo-step and tell Cinema 4D to update.
            doc.EndUndo()
            c4d.EventAdd()

        return True

if __name__ == '__main__':
    GroupObjectsCommand().Register()

