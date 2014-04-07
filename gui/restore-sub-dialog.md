The `restore-sub-dialog.pyp` example demonstrates how sub-dialogs of a main
dialog can be managed easily in Python. It also demonstrates a few useful
techniques that easen the life of a developer.

_This demo plugin was developed to answer the question [Multiple SubDialog][link]
on the PluginCafe._

  [link]: (http://plugincafe.com/forum/forum_posts.asp?TID=10015&PID=38923#38923)


## Details

A sub-dialog can refer to two distinct and yet not distinct things. There
is a class `SubDialog` in the C++ SDK that is not available in Python, but
it basically allows you to embed a dialog as a widget in another dialog which
can also be undocked. When its undocked, it is the same as if we open just
another dialog from the main dialog and refer to it as sub-dialog since it
is sub-ordinate to the main dialog.

When the sub-dialog is embedded into the Cinema 4D layout and saved, Cinema
will invoke a `CommandData` plugins `RestoreLayout()` method. It knows what
plugin to invoke from the Plugin ID that is passed to `GeDialog.Open()`. To
distinguish the main and the sub-dialog, it is possible to open a dialog
with a sub ID. This ID does not have to be a Plugin ID, you can use any you
want.

```python
class MainDialog(c4d.gui.GeDialog):

    # ...

    def Command(self, param, bc):
        if param == MY_COOL_BUTTON_THAT_OPENS_ANOTHER_DIALOG:
            self.sub_dialog.Open(c4d.DLG_TYPE_ASYNC, PLUGIN_ID, subid=1)
        return True
```

Now in `CommandData.RestoreLayout()`, the `sec_ref` parameter is a dictionary
that contains the subid of the dialog that needs to be restored. From this,
you can distinguish the main and sub-dialog.

It is a recommended pattern to let the main dialog handle the sub-dialog and
not transfer the responsibility partially to the CommandData plugin. Therefore,
we write

```python
class Command(c4d.plugins.CommandData):

    # ...

    def RestoreLayout(self, secref):
        return self.dialog.Restore(PLUGIN_ID, secref)

class MainDialog(c4d.gui.GeDialog):

    # ...

    def Restore(self, pluginid, secref):
        # We override this method so we don't have to handle the sub-
        # dialog from the CommandData plugin. THIS dialog is responsible
        # for the sub-dialog, do not split such management throughout
        # your program or it gets confusing.
        if secref['subid'] == 1:
            return self.sub_dialog.Restore(pluginid, secref)
        else:
            return super(MainDialog, self).Restore(pluginid, secref)
```

