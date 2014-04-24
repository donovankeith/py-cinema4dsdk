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

#Unique plugin ID, get your own from PluginCafe.com\
PLUGIN_ID = 1032046

# GUI IDS #

## Scene Info ##
"""IDs for text at the top of the dialog."""

ID_DOC_NAME = 1000


## Entries ##
"""Each line in the dialog/list gets an ID assigned to it like so:
ID_DYNAMIC_LIST_GROUP + i*ID_OFFSET_LINE + ID_OFFSET_STATE/NAME/????

So the ids for the 3rd list entry would be

Boolean State: 20000 + 3*10 + 1 = 20031
String Name: 20000 + 3*10 + 2 = 20032
"""

ID_SCROLL_GROUP = 20000

#Starting id for the dynamic list
ID_DYNAMIC_LIST_GROUP = 30000

#Each entry can store up to 10 pieces of data
ID_OFFSET_LINE = 10
ID_OFFSET_STATE = 1
ID_OFFSET_NAME = 2


## Commands ##
"""ID's for the various buttons/commands that affect the contents of the dialog. These numbers are
intentionally lower than those of the dynamic entries to avoid potential ID conflicts/limits."""

ID_COMMAND_GROUP = 2000
ID_ADD = 2001
ID_SUBTRACT = 2002


class PersistentDataDialog(c4d.gui.GeDialog):
    def __init__(self):
        #Default Values
        self._default_entry = {
            'state': False,
            'name': "Default"
        }

        #List of Entries in Dialog
        self._list = [self._default_entry]

    def CreateLayout(self):
        """Build the dialog's interface"""

        #Title in the menu bar of the dialog
        self.SetTitle('Persistent Data Dialog')

        #Retrieve and display the active document's name
        active_doc = c4d.documents.GetActiveDocument()
        active_doc_name = ""
        if active_doc is not None and active_doc.IsAlive():
            active_doc_name = active_doc.GetDocumentName()

        self.AddStaticText(ID_DOC_NAME, flags=0, name="Active Document: "+active_doc_name)

        #Dyanmic List of Elements Group
        self.ScrollGroupBegin(ID_SCROLL_GROUP, flags=c4d.BFH_LEFT|c4d.BFV_TOP|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
                              scrollflags=c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT)
        self.GroupBegin(ID_DYNAMIC_LIST_GROUP, flags=c4d.BFH_LEFT|c4d.BFV_TOP|c4d.BFH_SCALEFIT, cols=2, rows=0)
        self.AddListToLayout()
        self.GroupEnd()
        self.GroupEnd()

        #Modify List Buttons
        self.GroupBegin(ID_COMMAND_GROUP, c4d.BFH_CENTER|c4d.BFV_BOTTOM, cols=0, rows=1)
        self.AddButton(ID_ADD, 0, name="+")
        self.AddButton(ID_SUBTRACT, 0, name="-")
        self.GroupEnd()
        return True

    def AddListToLayout(self):
        """Adds an entry to the layout for each element in the classes _list. Be sure to Flush the group
        before doing this. And update the layout after."""

        self.LayoutFlushGroup(ID_DYNAMIC_LIST_GROUP)
        for i, row in enumerate(self._list):
            current_line = ID_DYNAMIC_LIST_GROUP + i*ID_OFFSET_LINE
            self.AddCheckbox(current_line + ID_OFFSET_STATE, 0, initw=0, inith=0, name="")
            self.AddEditText(current_line + ID_OFFSET_NAME, flags=c4d.BFH_SCALEFIT, initw=0, inith=0)
        self.LayoutChanged(ID_DYNAMIC_LIST_GROUP)

    def Command(self, param, bc):
        #User is adding a row
        if param == ID_ADD:
            self._list.append(self._default_entry)
            self.AddListToLayout()

        #User is subtracting a row
        if param == ID_SUBTRACT:
            #Remove the last item from the list
            if len(self._list) > 1:
                self._list.pop()
            #Unless there's only one item, in that case restore the default values.
            else:
                self._list = [self._default_entry]
            self.AddListToLayout()
        return True

    def Restore(self, pluginid, secret):
        return super(PersistentDataDialog, self).Restore(pluginid, secret)

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

    def RestoreLayout(self, secret):
        return self.dialog.Restore(PLUGIN_ID, secret)

if __name__ == '__main__':
    Command().Register()

