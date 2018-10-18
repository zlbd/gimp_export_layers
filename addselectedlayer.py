#!/usr/bin/env python
# Add the selected area as a layer
# Author: zlbd

from gimpfu import *
import os, sys, platform

################################################################################
# define functions
################################################################################
def get_slash():
    ch='/';
    if(platform.system()=="Windows"):
        ch='\\'
    return ch;

def init_log():
    sSlash  = get_slash()
    sHome   = os.path.expanduser('~')
    sLogDir = sHome + sSlash + 'gimp_script' + sSlash
    sLog    = sLogDir + 'el_log.txt'
    sErr    = sLogDir + 'el_err.txt'
    if not os.path.exists(sLogDir):
        os.mkdir(sLogDir)
    if os.path.exists(sLog):
        os.remove(sLog)
    if os.path.exists(sErr):
        os.remove(sErr)
    sys.stdout = open(sLog, 'a')
    sys.stderr = open(sErr, 'a')
    return


def insert_layer_from_selecttion(img):
    selRet = pdb.gimp_selection_bounds(img)
    if(selRet[0]):
        pdb.gimp_edit_copy(img.active_layer)
        newimage=pdb.gimp_edit_paste_as_new()
        drawable=newimage.layers[0]
        layer_copy = pdb.gimp_layer_new_from_drawable(drawable, img)
        pdb.gimp_image_insert_layer(img, layer_copy, None, 0)
        pdb.gimp_layer_set_offsets(layer_copy, selRet[1], selRet[2])
        pdb.gimp_image_delete(newimage)
    else:
        gimp.message("[Error] No selection")


def add_selected_layer(sTips, img):
    # protect code
    if( img == None ):
        gimp.message("[Error] Image None    \nPlease open a psd file...    ")
        return
    #img = gimp.image_list()[0]
    insert_layer_from_selecttion(img);
    #gimp.message("Finished")
    return

 
################################################################################
# call functions
################################################################################

init_log()

register(
    "python_fu_add_selected_layer",
    "A simple Python-Fu 'Add selected layer' plug-in.",
    "Add the selected area as a layer",
    "zlbd",
    "zlbd 2018.",
    "2018",
    "<Toolbox>/Layer/_Add Selected Layer(Py)",
    "",
    [
        (PF_STRING, "tips", "Help tips",   "Please selected an area first"),
        (PF_IMAGE,  "img",  "Input Image", None),
    ],
    [],
    add_selected_layer)
 
main()
