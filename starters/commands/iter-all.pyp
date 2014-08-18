# Copyright (c) 2014  Niklas Rosenstein
# Copyright (c) 2014 Donovan Keith
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
    py-cinema4dsdk/starters/commands/iter-all.pyp
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    description: This plugin command demonstrates how to iterate through all objects, tags,
    materials, and layers in a scene and print their name to the console.
    tags: command simple muchdoc hierarchy-iteration tag-iteration tags types
    level: beginner
    read-before: create-cube.pyp group-objects.pyp iter-hierarchy.pyp


    TO DO
    -----

    [ ] Add iterators for only selected elements.
    [ ] Add iterators for tags/materials/etc that belong to passed objects.
    [ ] Add iterators for Tracks, & Keys
"""

#=====================================================================================================================#
#   STANDARD LIBRARY IMPORTS
#=====================================================================================================================#

import c4d


#=====================================================================================================================#
#   GLOBALS
#=====================================================================================================================#

PLUGIN_ID = 1033540


#=====================================================================================================================#
#   UTILS
#=====================================================================================================================#

def GetNextNode(op, stop_at=None):
    """Returns the next object in the hierarchy.
    `op` is a BaseList2D node.

    For a fuller explanation on how/why this works, read:
    http://www.peranders.com/w/index.php?title=Python_Object_Iteration
    """

    if op is None or op == stop_at:
        return None

    if op.GetDown():
        return op.GetDown()

    while not op.GetNext() and op.GetUp():
        op = op.GetUp()

    return op.GetNext()

def YieldObjects(doc=c4d.documents.GetActiveDocument()):
    """Yields the next object in the document in turn.
    """

    #Ensure the document exists and is is Alive
    if (not doc) or (not doc.IsAlive()):
        return

    cur_obj = doc.GetFirstObject()
    while cur_obj is not None:
        yield cur_obj
        cur_obj = GetNextNode(cur_obj)

def YieldMaterials(doc=c4d.documents.GetActiveDocument()):
    """Yields each material in document in turn.
    """

    #Ensure the document exists and is is Alive
    if (not doc) or (not doc.IsAlive()):
        return

    cur_mat = doc.GetFirstMaterial()
    while cur_mat is not None:
        yield cur_mat
        cur_mat = GetNextNode(cur_mat)

def YieldLayers(doc=c4d.documents.GetActiveDocument()):
    """Yields each layer in the document in turn.
    """

    #Ensure the document exists and is is Alive
    if (not doc) or (not doc.IsAlive()):
        return

    #Iterate through all layers in the document.
    layer_root = doc.GetLayerObjectRoot()
    cur_layer = layer_root.GetDown()
    while cur_layer is not None:
        yield cur_layer
        cur_layer = GetNextNode(cur_layer)

def YieldTags(doc=c4d.documents.GetActiveDocument()):
    """Yields every tag in the scene.
    """

    #Ensure the document exists and is is Alive
    if (not doc) or (not doc.IsAlive()):
        return

    #Go through all objects and tags, and yield each tag in turn.
    for obj in YieldObjects(doc):
        for tag in obj.GetTags():
            yield tag

def PrintHeading(heading="", rule_width=64, indent_width=8):
    """Prints a heading to the console.
    Assume that heading is short than rule_width"""

    #Make a line of ======'s X characters long.
    horizontal_rule = "=" * rule_width

    print " "
    print " "
    print horizontal_rule
    print (" " * indent_width) + heading
    print horizontal_rule

#=====================================================================================================================#
#   CLASSES
#=====================================================================================================================#

class IterAllCommand(c4d.plugins.CommandData):

    def Register(self):
        """Registers the plugin with Cinema 4D. Necessary to create a menu entry."""

        help_string = 'Python SDK Example Command Plugin: Demonstrates ' \
                      'iterating through most key elements a user interacts with. ' \

        return c4d.plugins.RegisterCommandPlugin(
                PLUGIN_ID,
                "starters/commands/Iter All",
                c4d.PLUGINFLAG_COMMAND_HOTKEY,
                None,
                help_string,
                self,
        )

    def Execute(self, doc):
        """Prints a list of all tags to the console when the user run this command plugin."""

        #Print a formatted heading
        PrintHeading("ITER-ALL COMMAND PLUGIN")

        #Print Objects
        PrintHeading("Objects")
        for obj in YieldObjects(doc):
            print obj.GetName()

        #Print Tags
        PrintHeading("Tags")
        for tag in YieldTags(doc):
            print tag.GetName()

        #Print Materials
        PrintHeading("Materials")
        for mat in YieldMaterials(doc):
            print mat.GetName()

        #Print Layers
        PrintHeading("Layers")
        for layer in YieldLayers(doc):
            print layer.GetName()

        return True


#=====================================================================================================================#
#   REGISTRATION
#=====================================================================================================================#

if __name__ == '__main__':
    IterAllCommand().Register()