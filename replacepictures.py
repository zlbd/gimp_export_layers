#!/usr/bin/env python
# A replace_pictures for gimp python-fu script
# Author: zlbd

from gimpfu import *
import os, sys, platform

################################################################################
# define function
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
    return

def fwrite(fname, text):
    with open(fname,'w') as f:
        f.write(text)

def get_slash():
    ch='/';
    if(platform.system()=="Windows"):
        ch='\\'
    return ch;

def get_imgpath(basepath, midFolder = ''):
    """ e.g.
    sName  = os.path.basename(img.filename)
    imgDir = get_imgpath(sDir)
    """
    sSlash = get_slash()
    if(basepath[-1] != sSlash):
        basepath += sSlash
    imgpath = basepath
    if(midFolder != ''):
        imgpath = basepath + midFolder + sSlash
        if not os.path.exists(imgpath):
            os.mkdir(imgpath)
    return imgpath;

def walk_groupLayer(layerInput, cb, params_outside):
    layers = layerInput.layers
    nCount = len(layers)
    for i in range(0, nCount):
        layer = layers[i]
        if(layer.__class__ == gimp.GroupLayer):
            if(walk_groupLayer(layer, cb, params_outside)):
                return True
        elif(layer.__class__ == gimp.Layer):
            params_walk = [layers, i, layerInput]
            if(cb(layer, params_outside, params_walk)):
                return True
        else:
            print("[Error] layer class is wrong: "+layer.name)
    return False

def set_layer_rect(layer, rect):
    x, y, w, h = rect
    layer.set_offsets(x, y)
    layer.scale(w, h)

def replace_picture(layer, params_outside, params_walk):
    sDir, sFmt, img = params_outside
    layers, index, layerParent = params_walk
    fName = sDir + layer.name + "." + sFmt
    if not os.path.exists(fName):
        return False
    # load image as new layer
    newlayer = pdb.gimp_file_load_layer(img, fName)
    if(layerParent == img):
        layerParent = 0
    pdb.gimp_image_set_active_layer(img, layer)
    pdb.gimp_image_insert_layer(img, newlayer, None, -1)
    # move new layer
    rect = layer.offsets[0], layer.offsets[1], layer.width, layer.height
    set_layer_rect(newlayer, rect)
    # merge down
    layer.visible = True
    newlayer.visible = True
    layer = pdb.gimp_image_merge_down(img, newlayer, 0)
    return False


def main_replace_pictures(sDir, sFmt, img):
    #### protect code
    if( img == None ):
        gimp.message("[Error] Image None    \nPlease open a psd file...    ")
        return
    if( sDir == "" or sDir == None ):
        sDir = os.path.dirname(img.filename)
    else:
        sDir += get_slash()
    #### get base path
    #img = gimp.image_list()[0]
    layer = img.active_layer
    rect = layer.offsets[0], layer.offsets[1], layer.width, layer.height
    #gimp.message(sDir)
    params = [sDir, sFmt, img]
    walk_groupLayer(img, replace_picture, params)
    gimp.message("replace_pictures run OK!" + "\n" 
            + "The rectangle of layer selected:" + "\n\n" 
            + str(rect))
    return
 
################################################################################
# call function
################################################################################
init_log()
register(
    "python_fu_replace_pictures",
    "A simple Python-Fu 'replace_pictures' plug-in.",
    "When run this plug-in, show 'Test OK' message.",
    "zlbd",
    "zlbd 2018.",
    "2018",
    "<Toolbox>/Layer/_Replace Pictures (Py)",
    "RGB*, GRAY*",
    [
        (PF_DIRNAME, "string", "Directory",     None),
        (PF_RADIO,   "format", "Image Format",  "png", (("png", "png"), ("bmp(32-bit)", "bmp"))),
        (PF_IMAGE,   "image",  "Input Sselect", None),
    ],
    [],
    main_replace_pictures)
 
main()
