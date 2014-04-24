# Copyright (c) 2014  Donovan Keith
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
    py-cinema4dsdk/gui/persistent-data-dialog.pyp
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    description: This file demonstrates how to create a dialog that loads/saves custom
        data into the document's container.
    tags: command gui
    level: medium
    seealso:
    links:
"""

import c4d

PLUGIN_ID = 1032046

# GUI IDS #

## Commands ##
"""ID's for the various buttons/commands that affect the contents of the dialog. These numbers are
intentionally lower than those of the dynamic entries to avoid potential ID conflicts/limits."""

ID_COMMAND_GROUP = 1000
ID_ADD = 1001
ID_SUBTRACT = 1002

## Entries ##
"""Each line in the dialog/list gets an ID assigned to it like so:
ID_DYNAMIC_LIST_GROUP + i*ID_OFFSET_LINE + ID_OFFSET_STATE/NAME/??

So the ids for the 3rd list entry would be

Boolean State: 20000 + 3*10 + 1 = 20031
String Name: 20000 + 3*10 + 2 = 20032
"""

ID_DYNAMIC_LIST_GROUP = 20000 #Starting id for the dynamic list
ID_OFFSET_LINE = 10 #Each entry can store up to 10 pieces of data
ID_OFFSET_STATE = 1
ID_OFFSET_NAME = 2

class PersistentDataDialog(c4d.gui.GeDialog):

    def CreateLayout(self):
        """Build the dialog's interface"""

        #Title in the menu bar of the dialog
        self.SetTitle('Persistent Data Dialog')

        #Dyanmic List of Elements Group
        self.GroupBegin(ID_DYNAMIC_LIST_GROUP, c4d.BFH_LEFT|c4d.BFV_TOP, cols=0, rows=1)
        self.AddCheckbox(ID_DYNAMIC_LIST_GROUP + ID_OFFSET_STATE, 0, initw=0, inith=0, name="")
        self.AddEditText(ID_DYNAMIC_LIST_GROUP + ID_OFFSET_NAME, 0, initw=300, inith=0)
        self.GroupEnd()

        #Modify List Buttons
        self.GroupBegin(ID_COMMAND_GROUP, c4d.BFH_CENTER|c4d.BFV_BOTTOM, cols=0, rows=1)
        self.AddButton(ID_ADD, 0, name="+")
        self.AddButton(ID_SUBTRACT, 0, name="-")
        self.GroupEnd()
        return True

    def Command(self, param, bc):
        return True

    def Restore(self, pluginid, secref):
        return super(PersistentDataDialog, self).Restore(pluginid, secref)

class Command(c4d.plugins.CommandData):

    def Register(self):
        return c4d.plugins.RegisterCommandPlugin(
                PLUGIN_ID, "Persistent Data Dialog", 0, None, "", self)

    @property
    def dialog(self):
        if not hasattr(self, '_dialog'):
            self._dialog = PersistentDataDialog()
        return self._dialog

    def Execute(self, doc):
        return self.dialog.Open(c4d.DLG_TYPE_ASYNC, PLUGIN_ID)

    def RestoreLayout(self, secref):
        return self.dialog.Restore(PLUGIN_ID, secref)

if __name__ == '__main__':
    Command().Register()

