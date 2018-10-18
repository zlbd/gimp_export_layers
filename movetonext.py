#!/usr/bin/env python
# Move current layer according to next layer
# Author: zlbd

from gimpfu import *
import os, sys, platform

################################################################################
# define functions
################################################################################

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
    return sHome

def fwrite(fname, text):
    with open(fname,'w') as f:
        f.write(text)

def equal_layer(src, dst):
    if(src == dst):
        return True
    return False

def walk_find_next_layer(layerInput, srcLayer):
    layers = layerInput.layers
    nCount = len(layers)
    for i in range(0, nCount):
        layer = layers[i]
        if(layer.__class__ == gimp.GroupLayer):
            retLayer = walk_find_next_layer(layer, srcLayer)
            if(retLayer != None):
                return retLayer
        elif(layer.__class__ == gimp.Layer):
            if(layer == srcLayer):
                if(i+1<nCount):
                    return layers[i+1]
        else:
            print("[Error]: "+layer.name)
    return None


def get_slash():
    ch='/';
    if(platform.system()=="Windows"):
        ch='\\'
    return ch;

def move_layer_to_next(tips, img, x, y, w, h):
    # protect code
    if( img == None ):
        gimp.message("[Error] Image None    \nPlease open a psd file...    ")
        return
    #img = gimp.image_list()[0]
    selLayer = img.active_layer
    if(x==-1 and y==-1):
        nextLayer = walk_find_next_layer(img, selLayer)
        if(nextLayer == None):
            gimp.message("[Erro] The next layer of the current image is not found!")
        else:
            selLayer.visible = True
            nextLayer.visible = True
            selLayer.set_offsets(nextLayer.offsets[0], nextLayer.offsets[1])
            selLayer.scale(nextLayer.width, nextLayer.height)
    else:
        selLayer.visible = True
        selLayer.set_offsets(x, y)

    if(w!=-1 and h!=-1):
        selLayer.scale(w, h)

    return 0
 
################################################################################
# call functions
################################################################################
global s_sHome
s_sHome = init_log()

register(
    "python_fu_move_layer_to_next",
    "A simple Python-Fu 'Move Layer' plug-in.\n",
    "When run this plug-in, move layer as offset given. ",
    "zlbd",
    "zlbd 2018.",
    "2018",
    "<Toolbox>/Layer/_Move Layer To Next(Py)",
    "RGB*, GRAY*",
    [
        (PF_DIRNAME, "tips",    "tips",         "Please click ok to continue..."),
        (PF_IMAGE,   "img",     "Input Image",  None),
        (PF_INT,     "x",       "Input x",      -1),
        (PF_INT,     "y",       "Input y",      -1),
        (PF_INT,     "w",       "Input w",      -1),
        (PF_INT,     "h",       "Input h",      -1),
    ],
    [],
    move_layer_to_next)
 
main()
