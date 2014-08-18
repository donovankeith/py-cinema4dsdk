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
    py-cinema4dsdk/gui/todo-list.pyp
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    description: This ToDo List plugin demonstrates common issues when working with a dialog:
        1. Creating and updating a dynamic dialog.
        2. Saving the dialog's data within the active document.
        3. Refreshing the dialog when a new document is opened.
    tags: command gui persistent-data async-dialog
    level: medium
    links:
        http://www.plugincafe.com/forum/forum_posts.asp?TID=9828
"""

import c4d

# Unique plugin ID, get yours from http://plugincafe.com/forum/developer.asp
PLUGIN_ID = 1032046

# GUI/CONTAINER IDS #

## Scene Info ##
"""IDs for text at the top of the dialog."""
ID_LIST_LENGTH = 10

ID_DOC_INFO_GROUP = 1000
ID_DOC_NAME = 1001

## Entries ##
"""Each task in the dialog/list gets an ID assigned to it like so:
ID_DYNAMIC_LIST_GROUP + i*ID_OFFSET_TASK + ID_OFFSET_NAME/IS_COMPLETE/????

So the ids for the 3rd list entry would be

Boolean State: 20000 + 3*10 + 1 = 20031
String Name: 20000 + 3*10 + 2 = 20032
"""

ID_SCROLL_GROUP = 20000

#Starting id for the dynamic list, note that it's a # larger than all others
ID_DYNAMIC_LIST_GROUP = 30000

#Each entry can store up to 10 pieces of data
ID_OFFSET_TASK = 10
ID_OFFSET_IS_COMPLETE = 1
ID_OFFSET_TASK_NAME = 2


## Commands ##
"""ID's for the various buttons/commands that affect the contents of the dialog. These numbers are
intentionally lower than those of the dynamic entries to avoid potential ID conflicts/limits."""

ID_COMMAND_GROUP = 2000
ID_ADD = 2001
ID_SUBTRACT = 2002


class PersistentDataDialog(c4d.gui.GeDialog):
    """Class which implements a simple ToDo list dialog and data construct."""

    def __init__(self):
        #Persistent values to see if doc has changed.
        self._last_doc = c4d.documents.GetActiveDocument()

        #Default Values
        self._default_is_complete = False
        self._default_task_name = "Task"

        #List of Entries in Dialog
        self._todo_list = [{
            'is_complete': self._default_is_complete,
            'name': self._default_task_name
        }]

    def CreateLayout(self):
        """Build the dialog's interface"""

        #Title in the menu bar of the dialog
        self.SetTitle('Persistent Data Dialog')

        self.GroupBegin(ID_DOC_INFO_GROUP, flags=c4d.BFH_CENTER)
        self.AddDocumentInfo()
        self.GroupEnd()

        #Dyanmic List of Elements Group
        self.ScrollGroupBegin(ID_SCROLL_GROUP, flags=c4d.BFH_LEFT|c4d.BFV_TOP|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
                              scrollflags=c4d.SCROLLGROUP_VERT|c4d.SCROLLGROUP_AUTOVERT)
        self.GroupBegin(ID_DYNAMIC_LIST_GROUP, flags=c4d.BFH_LEFT|c4d.BFV_TOP|c4d.BFH_SCALEFIT, cols=2, rows=0)

        #Call automation function to add menu entries for each task
        self.AddListToLayout()

        self.GroupEnd()
        self.GroupEnd()

        #Modify List Buttons
        self.GroupBegin(ID_COMMAND_GROUP, c4d.BFH_CENTER|c4d.BFV_BOTTOM, cols=0, rows=1)
        self.AddButton(ID_ADD, 0, name="+")
        self.AddButton(ID_SUBTRACT, 0, name="-")
        self.GroupEnd()
        return True

    def AddDocumentInfo(self, active_doc=None):
        """Retrieves the name of active_doc and displays it in the dialog."""

        if active_doc is None:
            active_doc = c4d.documents.GetActiveDocument()

        #Retrieve and display the active document's name
        active_doc_name = ""
        if (active_doc is not None) and active_doc.IsAlive():
            active_doc_name = active_doc.GetDocumentName()

        #Empty out the dialog and put in the active document's name.
        self.LayoutFlushGroup(ID_DOC_INFO_GROUP)
        self.AddStaticText(ID_DOC_NAME, flags=0, name="To Do in: "+active_doc_name)
        self.LayoutChanged(ID_DOC_INFO_GROUP)

    def CalcCurrentTask(self, i):
        return ID_DYNAMIC_LIST_GROUP + i*ID_OFFSET_TASK

    def AddListToLayout(self):
        """Adds an entry to the layout for each element in the classes _todo_list."""

        self.LayoutFlushGroup(ID_DYNAMIC_LIST_GROUP)
        for i, row in enumerate(self._todo_list):
            current_task = self.CalcCurrentTask(i)
            self.AddCheckbox(current_task + ID_OFFSET_IS_COMPLETE, 0, initw=0, inith=0, name="")
            self.SetBool(current_task + ID_OFFSET_IS_COMPLETE, row['is_complete'])

            self.AddEditText(current_task + ID_OFFSET_TASK_NAME, flags=c4d.BFH_SCALEFIT, initw=0, inith=0)
            self.SetString(current_task + ID_OFFSET_TASK_NAME, row['name'])
        self.LayoutChanged(ID_DYNAMIC_LIST_GROUP)

    def Refresh(self):
        """Recalculates the _todo_list and refreshes the dialog with the new information."""

        def RefreshDialog():
            """Convenience function to reduce duplication of code."""

            self.AddDocumentInfo()
            self.AddListToLayout()

        #If there isn't a document, wipe the dialog and return
        active_doc = c4d.documents.GetActiveDocument()
        if (active_doc is None) or not active_doc.IsAlive():
            self._last_doc = active_doc
            self._todo_list = [{
                'is_complete': self._default_is_complete,
                'name': self._default_task_name
            }]
            RefreshDialog()
            return

        #Otherwise, try and build up the dialog from the data in the document.

        #flush the data
        self._todo_list = []

        doc_bc = active_doc.GetDataInstance()
        if doc_bc is None:
            return

        #Retrieve this plugin's data stored in the document
        list_bc = doc_bc.GetContainer(PLUGIN_ID)
        if list_bc is None:
            return

        #Convert the contents of the container into a python list
        list_length = list_bc.GetInt32(ID_LIST_LENGTH)

        #Empty list, fill in with the defaults
        if list_length == 0:
            self._todo_list = [{
                'is_complete': self._default_is_complete,
                'name': self._default_task_name
            }]

        #Pull the data from the container
        for i in range(list_length):
            current_task = self.CalcCurrentTask(i)
            is_complete = list_bc.GetBool(current_task + ID_OFFSET_IS_COMPLETE)
            name = list_bc.GetString(current_task + ID_OFFSET_TASK_NAME)
            self._todo_list.append({'is_complete': is_complete,
                                'name': name}
            )

        #We have the data we need, so refresh the dialog
        RefreshDialog()

    def ListToContainer(self):
        """Takes the _todo_list member variable and converts it into a container which is then stuffed into the
        active document's container."""

        #Get the current document's container
        active_doc = c4d.documents.GetActiveDocument()
        if (active_doc is None) or not active_doc.IsAlive():
            return

        doc_bc = active_doc.GetDataInstance()
        if doc_bc is None:
            return

        #Get this plugin's sub-container
        list_bc = doc_bc.GetContainer(PLUGIN_ID)

        if list_bc is None:
            list_bc = c4d.BaseContainer()

        #Store the length of the list
        list_length = len(self._todo_list)
        list_bc.SetInt32(ID_LIST_LENGTH, list_length)

        #Update each of the list items
        for i, task in enumerate(self._todo_list):
            current_task = self.CalcCurrentTask(i)
            list_bc.SetBool(current_task + ID_OFFSET_IS_COMPLETE, task['is_complete'])
            list_bc.SetString(current_task + ID_OFFSET_TASK_NAME, task['name'])

        #Save the container to the document
        doc_bc.SetContainer(PLUGIN_ID, list_bc)


    def CoreMessage(self, id, msg):
        """Responds to what's happening inside of Cinema 4D. In this case, we're looking to see
        if we've got a new document."""

        #We've got a new document, or the document is being recalculated
        if id == c4d.EVMSG_DOCUMENTRECALCULATED:
            doc = c4d.documents.GetActiveDocument()

            #Is there a living active document?
            if (doc is not None) and doc.IsAlive():
                #How about a living cached document?
                if (self._last_doc is not None) and self._last_doc.IsAlive():
                    #Are we in a different document?
                    if doc != self._last_doc:
                        #Great, update the dialog
                        self.Refresh()
                #Cache the active document for later comparison
                self._last_doc = doc

        return True

    def Command(self, param, bc):
        """Responds to user mouse-clicks and data entry. Typically updates the python list, and then writes the
        whole thing to the plugin's sub-container within the document's container. Perhaps inefficient because
        more than needs to be is written, but for a simple dialog like this it shouldn't result in any
        considerable slow-down."""

        #User is adding a row
        if param == ID_ADD:
            self._todo_list.append(
                {
                    'is_complete': self._default_is_complete,
                    'name': self._default_task_name
                }
            )
            self.ListToContainer()
            self.AddListToLayout()

        #User is subtracting a row
        elif param == ID_SUBTRACT:
            #Remove the last item from the list
            if len(self._todo_list) > 1:
                self._todo_list.pop()
            #Unless there's only one item, in that case restore the default values.
            else:
                self._todo_list = [{
                    'is_complete': self._default_is_complete,
                    'name': self._default_task_name
                }]
            self.ListToContainer()
            self.AddListToLayout()

        #One of the dynamic list entries is being affected
        elif param > ID_DYNAMIC_LIST_GROUP:

            #figure out which offset id it is within it's task so we can retrieve the right data type
            task_number = int((param - ID_DYNAMIC_LIST_GROUP)/ID_OFFSET_TASK)
            offset_id = param % ID_OFFSET_TASK

            if offset_id == ID_OFFSET_IS_COMPLETE:
                self._todo_list[task_number]['is_complete'] = self.GetBool(param)
            elif offset_id == ID_OFFSET_TASK_NAME:
                self._todo_list[task_number]['name'] = self.GetString(param)

            #Store the update in the document's container
            self.ListToContainer()

        return True

    def Restore(self, pluginid, secret):
        return super(PersistentDataDialog, self).Restore(pluginid, secret)

class Command(c4d.plugins.CommandData):
    """Registers the plugin with Cinema 4D and opens the dialog when the command is clicked by the user."""

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