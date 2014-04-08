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
    py-cinema4dsdk/gui/restore-sub-dialog.pyp
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    description: This file demonstrates how to manage sub-dialogs
        of main dialog including the restoration of the sub-dialog
        in the layout.
    tags: command gui sub-dialogs layout-restore
    level: medium
    seealso: restore-sub-dialog.md
    links:
        http://plugincafe.com/forum/forum_posts.asp?TID=10015&PID=38923#38923
"""

import c4d

PLUGIN_ID = 1031982

class MainDialog(c4d.gui.GeDialog):

    # Do not create the object on class-level, although it might
    # be unimportant since you do not open multiple objects of your
    # MainDialog, it is contradicting to have one instance of sub
    # dialog for all instances of the main dialog.
    # A property that creates the dialog on-demand is perfect for
    # this purpose.

    @property
    def sub_dialog(self):
        if not hasattr(self, '_sub_dialog'):
            self._sub_dialog = SubDialog()
        return self._sub_dialog

    # c4d.gui.GeDialog

    def CreateLayout(self):
        self.SetTitle('Main Dialog')
        self.AddButton(1000, 0, name="Open Sub-Dialog")
        return True

    def Command(self, param, bc):
        if param == 1000:
            self.sub_dialog.Open(c4d.DLG_TYPE_ASYNC, PLUGIN_ID, subid=1)
        return True

    def Restore(self, pluginid, secref):
        # We override this method so we don't have to handle the sub-
        # dialog from the CommandData plugin. THIS dialog is responsible
        # for the sub-dialog, do not split such management throughout
        # your program or it gets confusing.
        if secref['subid'] == 1:
            return self.sub_dialog.Restore(pluginid, secref)
        else:
            return super(MainDialog, self).Restore(pluginid, secref)

class SubDialog(c4d.gui.GeDialog):

    # c4d.gui.GeDialog

    def CreateLayout(self):
        self.SetTitle('Sub-Dialog')
        self.AddStaticText(1000, 0, name="This is the sub-dialog.")
        return True

class Command(c4d.plugins.CommandData):

    def Register(self):
        return c4d.plugins.RegisterCommandPlugin(
                PLUGIN_ID, "Sub-Dialog Docking Test", 0, None, "", self)

    @property
    def dialog(self):
        if not hasattr(self, '_dialog'):
            self._dialog = MainDialog()
        return self._dialog

    # c4d.plugins.CommandData

    def Execute(self, doc):
        return self.dialog.Open(c4d.DLG_TYPE_ASYNC, PLUGIN_ID)

    def RestoreLayout(self, secref):
        return self.dialog.Restore(PLUGIN_ID, secref)

if __name__ == '__main__':
    Command().Register()

