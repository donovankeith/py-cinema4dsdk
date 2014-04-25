The `task-list.pyp` demonstrates:

1. How to create a dynamic dialog
2. How to respond to retrieve user-input
3. How to store data from a dialog within a scene file
4. How to make a simple list from which you can add/subtract the last entry
5. How to detect if a new scene is open

## Details

When reading through the code it may be helpful to generally understand more-or-less what's happening.

* When the user clicks on the plugin's entry a dialog opens up.
* This dialog starts by building it's interface with default values.
* Then it searches the document's data container for any data the plugin might have saved previously in a sub-container
with the same id as the plugin.
* That data is converted into a python list `._task_list` which is a member of the dialog's class.
* The data from the python list is then used to add the appropriate number of dialog elements and fill them with data.
* Whenever the user clicks on the buttons, or modifies the data in some way, that list gets updated and the updated
list gets fed back into the document's container.
* While all of this is happening, the dialog is listening for messages from C4D, specifically
the `EVMSG_DOCUMENTRECALCULATED` message, which might indicate a new document has been activated.
* If a new document has been activated, the dialog flushes it's internal list and loads any data the plugin has stored
in the newly activated document.