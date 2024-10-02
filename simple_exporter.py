import sys
import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel


# this plugin menu setup creates a single menu entry
# to create a menu under Windows/my-tool

# The below sample will create a new menu and menu-item: ToolsMenu/My cool tool
# MENU_NAME is the name maya assigns to a menu, this is not always the same as the visible label
# e.g. to parent to the default Maya menu 'Windows', use MENU_NAME="mainWindowMenu"
MENU_NAME = "mainWindowMenu"  # no spaces in names, use CamelCase. Used to find and parent to a menu.
MENU_LABEL = "Tools"  # spaces are allowed in labels, only used when we create a new menu
MENU_ENTRY_LABEL = "Simple Exporter"

MENU_PARENT = "MayaWindow"  # do not change

__menu_entry_name = "" # Store generated menu item, used when unregister


def maya_useNewAPI():  # noqa
    """dummy method to tell Maya this plugin uses the Maya Python API 2.0"""
    pass


import maya.cmds as cmds


def UI():
	# Global setups
	global RenameText
	global StartValue
	global PaddingValue
	global PrefixText
	global SuffixText
	global option_menu_pivot
	global option_menu_file
	global triangulate
	global center_object
	global delete_history
	global freeze_transformations

    # UI Width
	sizeX = 280
	
	if cmds.window("SmartExport", exists=True):
		cmds.deleteUI("SmartExport", window=True)

    # Creating UI
	SmartExport = cmds.window("SmartExport", title="SmartExport", width=sizeX+6, height=420, mnb = True, mxb = False, sizeable = False, rtf=False)

	# Creating interface elements
	mainLayout = cmds.columnLayout(adj=False)

	# Main label - Renamer
	cmds.text(label="   Renamer", w=sizeX+10 ,font="boldLabelFont", p=mainLayout, bgc=(0.28, 0.66, 0.71), h=20 ,align="left")
	cmds.separator(w=sizeX+3, h=10, nbg=False)

	# Renamer interface
	renamerLayout = cmds.columnLayout(co=("left", 10),adj=False)

	# Rename Field
	cmds.rowColumnLayout(numberOfRows=1, w=sizeX)
	cmds.text(label="Rename:", font = "boldLabelFont", w = 50, align="left")
	RenameText = cmds.textField(w = 210)

	cmds.setParent(renamerLayout)
	cmds.separator(h=10)

	# Numeration and Padding
	cmds.rowLayout( numberOfColumns=4, columnWidth4=(30, 70, 50, 70), columnAttach=[(1, 'both', 0), (2, 'right', 34), (3, 'both', 0), (4, 'both', 0)])
	cmds.text(label="Start:", font = "boldLabelFont", w = 30, align="left")
	StartValue = cmds.textField(w = sizeX/4, tx="0")
	cmds.text(label="Padding:", font = "boldLabelFont", w = 50, align="left")
	PaddingValue = cmds.textField(w = sizeX/4, tx="2")

	cmds.setParent(renamerLayout)

	# Rename button
	cmds.separator(h=10)
	cmds.button(l="Rename", w=sizeX-20, bgc=(0.5,0.5,0.5), c=Rename)
	cmds.separator(h=10)

	# Add Prefix
	cmds.rowColumnLayout( numberOfRows=1, w=sizeX, cs = [(5,5)])
	cmds.text(label="Prefix:", font = "boldLabelFont", w = 40, align="left")
	PrefixText = cmds.textField(w = 150, tx="prefix_")
	cmds.button(label = "Add", w=sizeX/4-10, h=25, align = "Center", c=AddPrefix)

	cmds.setParent(renamerLayout)
	cmds.separator(h=5)

	# Add Suffix
	cmds.rowColumnLayout( numberOfRows=1, w=sizeX, cs = [(5,5)])
	cmds.text(label="Suffix:", font = "boldLabelFont", w = 40, align="left")
	SuffixText = cmds.textField(w = 150, tx="_suffix")
	cmds.button(label = "Add", w=sizeX/4-10, h=25, align = "Center", c=AddSuffix)

	cmds.setParent(renamerLayout)
	cmds.separator(h=20)

	# ----------------------------------------------------------------------------------------------------------
	
	# Main label - Exporter
	cmds.setParent(mainLayout)
	cmds.text(label="   Exporter", w=sizeX+10 ,font="boldLabelFont", p=mainLayout, bgc=(0.28, 0.66, 0.71), h=20 ,align="left")
	cmds.separator(w=sizeX+3, h=10, nbg=False)

	# Exporter interface
	exporterLayout = cmds.columnLayout(co=("left", 10),adj=False)

	# Dropdown Pivot
	cmds.rowLayout( numberOfColumns=3, columnWidth3=(50, 125, 90), columnAttach=[(1, 'both', 10), (2, 'both', 10), (3, 'both', 10)] )
	cmds.text(label="Pivot:", font="boldLabelFont")
	option_menu_pivot = cmds.optionMenu()
	cmds.menuItem(label="Center")
	cmds.menuItem(label="Center Bottom")
	cmds.menuItem(label="Center Top")
	cmds.button(label="Apply", c=ApplyPivot)

	cmds.setParent(exporterLayout)
	cmds.separator(h=5, vis=True)

	# Export options
	# - Checkbox titles
	cmds.columnLayout(columnAlign='center', w=sizeX)
	cmds.separator(h=7)
	cmds.rowLayout(nc=4, columnWidth4=[70, 70, 80, 70])
	cmds.text(l="Triangulate")
	cmds.text(l="Center Grid")
	cmds.text(l="Delete history")
	cmds.text(l="Freeze")
	cmds.setParent(exporterLayout)

	# - Checkboxes
	cmds.rowLayout(nc=5, columnWidth5=[20, 70, 70, 70, 70])
	cmds.text(l="")
	triangulate = cmds.checkBox(l="", w=70, v=False)
	center_object = cmds.checkBox(l="", w=70, v=False)
	delete_history = cmds.checkBox(l="", w=70, v=False)
	freeze_transformations = cmds.checkBox(l="", w=70, v=False)

	cmds.setParent(exporterLayout)
	cmds.separator(w=sizeX-20, h=10)

	# Dropdown File type
	cmds.rowLayout( numberOfColumns=3, columnWidth3=(70, 50, 110))
	cmds.text(label="")
	cmds.text(label="File:", font="boldLabelFont")
	option_menu_file = cmds.optionMenu()
	cmds.menuItem(label=".fbx")
	cmds.menuItem(label=".obj")

	cmds.setParent(exporterLayout)
	cmds.separator(h=10)

	cmds.setParent(exporterLayout)
	cmds.separator(h=10)

	# Export button
	cmds.button(l="Export", w=sizeX-20, bgc=(0.5,0.5,0.5), c=Export)

	# Parent Reset
	cmds.setParent(mainLayout)

    # Show UI:
	cmds.showWindow(SmartExport)


def Rename(*args):

	# Get all selected objects in the scene
	selection = cmds.ls(selection=True)
	rename = cmds.textField(RenameText, q=True, tx=True)

	# Get padding & start
	start = cmds.textField(StartValue, q=True, tx=True)
	start = int(start)
	padding = cmds.textField(PaddingValue, q=True, tx=True)
	padding = int(padding)

	# Get the padding to work
	zeros = ""
	for i in range(int(padding)):
		if len(str(start)) <= i:
			zeros = zeros+"0"

	# Rename all selected objects in the scene
	for obj in selection:
		# Test for duplicate names and return the name without parents
		trueName = testDuplicateName(obj)
		oldName = trueName

		if rename == '':
			# Rename
			name = 'None' + "_" + "{:0>"+str(padding) + "}"
			newNameList = name.format(start)
			cmds.rename(obj, name.format(start))
		else:
			# Rename
			name = rename + "_" + "{:0>"+str(padding) + "}"
			newNameList = name.format(start)
			cmds.rename(obj, name.format(start))

		# Rename all to new names
		for x in range(len(selection)):
			newParentName = selection[x].replace(oldName, newNameList)
			selection[x] = newParentName
			
		
		start = int(start+1)


def AddPrefix(*args):

	# Get all selected objects in the scene
	selection = cmds.ls(selection=True)

	# Get prefix
	prefix = cmds.textField(PrefixText, q=True, tx=True)

	iteration = 0	
	for obj in selection:
		cmds.rename(obj, prefix + selection[iteration])
		iteration += 1

	
def AddSuffix(*args):

	# Get all selected objects in the scene
	selection = cmds.ls(selection=True)

	# Get suffix
	suffix = cmds.textField(SuffixText, q=True, tx=True)

	iteration = 0	
	for obj in selection:
		cmds.rename(obj, selection[iteration] + suffix)
		iteration += 1


def ApplyPivot(*args):

	# Get selected objects
	selection = cmds.ls(selection=True)

	# Get selected option from menu
	selected_option = cmds.optionMenu(option_menu_pivot, q=True, value=True)
	
	# Set pivot location according to menu value
	if selected_option == 'Center':	
		# Keep
		for obj in selection:
			bbox = cmds.exactWorldBoundingBox(obj)
			center = [(bbox[0] + bbox[3]) / 2, (bbox[1] + bbox[4]) / 2, (bbox[2] + bbox[5]) / 2]
			cmds.xform(obj, piv=center, ws=True)

	elif selected_option == 'Center Bottom':
		# Center bottom
		for obj in selection:
			bbox = cmds.exactWorldBoundingBox(obj)
			bottom = [(bbox[0] + bbox[3]) / 2, bbox[1], (bbox[2] + bbox[5]) / 2]
			cmds.xform(obj, piv=bottom, ws=True)

	elif selected_option == 'Center Top':
		# Center top
		for obj in selection:
			bbox = cmds.exactWorldBoundingBox(obj)
			top = [(bbox[0] + bbox[3]) / 2, bbox[4], (bbox[2] + bbox[5]) / 2]
			cmds.xform(obj, piv=top, ws=True)


def Export(*args):
	
	# Get checkbox values
	tri = cmds.checkBox(triangulate, q=True, value=True)
	center = cmds.checkBox(center_object, q=True, value=True)
	del_his = cmds.checkBox(delete_history, q=True, value=True)
	freeze = cmds.checkBox(freeze_transformations, q=True, value=True)
	# Get selected objects
	selection = cmds.ls(selection=True)

	# Apply whats true to objects
	for obj in selection:
		if tri:
			# Triangulate objects
			cmds.polyTriangulate(obj)
		if center:
			# Place object at 0, 0, 0
			# Get origin
			origin = cmds.createNode("transform")
			# Move object
			cmds.matchTransform(obj, origin, position=True)
			# Delete node
			cmds.delete(origin)
		if freeze:
			# Freeze transformations
			cmds.makeIdentity(obj, apply=True, translate=True, rotate=True, scale=True)
		if del_his:
			# Delete history
			cmds.DeleteHistory(obj)

	# Get file type option
	selected_file_type = cmds.optionMenu(option_menu_file, q=True, value=True)

	if selected_file_type == '.obj':
		# Get output path
		export_path = cmds.fileDialog2(dialogStyle=2, cap="Select the export location:", fm=0, ff="OBJ Files (*.obj)")
		cmds.select(clear=True)
		for obj in selection:
			cmds.select(obj, add=True)
		# Export
		try:
			cmds.file(export_path[0], type="OBJexport", options="groups=1;ptgroups=1;materials=0;smoothing=1;normals=1", force=True, es=True, pr=True)
		except Exception as e:
			pass

	else:
		# Get output path
		export_path = cmds.fileDialog2(dialogStyle=2, cap="Select the export location:", fm=0, ff="FBX Files (*.fbx)")
		cmds.select(clear=True)
		for obj in selection:
			cmds.select(obj, add=True)
		# Export
		cmds.file(export_path[0]+".fbx", type="FBX", force=True, es=True, pr=True)


def testDuplicateName(Obj):

	# Get name without parents
	try:
		name =  Obj.split("|")
		return name[len(name)-1]
	except:
		return Obj


# =============================== Menu ===========================================
def show(*args):
    UI()


def loadMenu():
    """Setup the Maya menu, runs on plugin enable"""
    global __menu_entry_name

    # Maya builds its menus dynamically upon being accessed, so they don't exist if not yet accessed.
    # We force a menu build to allow parenting any new menu under a default Maya menu
    mel.eval("evalDeferred buildFileMenu")  # delete this if not parenting menus to a default Maya Menu

    if not cmds.menu(f"{MENU_PARENT}|{MENU_NAME}", exists=True):
        cmds.menu(MENU_NAME, label=MENU_LABEL, parent=MENU_PARENT)
    __menu_entry_name = cmds.menuItem(label=MENU_ENTRY_LABEL, command=show, parent=MENU_NAME)


def unloadMenuItem():
    """Remove the created Maya menu entry, runs on plugin disable"""
    if cmds.menu(f"{MENU_PARENT}|{MENU_NAME}", exists=True):
        menu_long_name = f"{MENU_PARENT}|{MENU_NAME}"
        # Check if the menu item exists; if it does, delete it
        if cmds.menuItem(__menu_entry_name, exists=True):
            cmds.deleteUI(__menu_entry_name, menuItem=True)
        # Check if the menu is now empty; if it is, delete the menu
        if not cmds.menu(menu_long_name, query=True, itemArray=True):
            cmds.deleteUI(menu_long_name, menu=True)


# =============================== Plugin (un)load ===========================================
def initializePlugin(plugin):
    """Code to run when the Maya plugin is enabled, this can be manual or during Maya startup"""
    # register_command(plugin)
    loadMenu()


def uninitializePlugin(plugin):
    """Code to run when the Maya plugin is disabled."""
    # to allow the user to enable and disable your plugin on the fly without any issues
    # anything created or setup during initializePlugin should be cleaned up in this method.
    # however if you don't, a user can instead disable the plugin & then restart Maya.

    # unregister_command(plugin)
    unloadMenuItem()
    
