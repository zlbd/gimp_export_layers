#!/usr/bin/env python
# A template for gimp python-fu script
# Author: zlbd

from gimpfu import *
import os, sys, platform

################################################################################
# lib function
################################################################################
#pdb.file_psd_save(img, None, name, name, 1, 1)

################################################################################
# define function
################################################################################
global s_Home
def init_log():
    global s_Home
    sSlash  = get_slash()
    s_Home   = os.path.expanduser('~')
    sLogDir = s_Home + sSlash + 'gimp_script' + sSlash
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

def walk_groupLayer(layerInput, func, param):
    layers = layerInput.layers
    nCount = len(layers)
    for i in range(0, nCount):
        layer = layers[i]
        if(layer.__class__ == gimp.GroupLayer):
            if(walk_groupLayer(layer, func, param)):
                return True
        elif(layer.__class__ == gimp.Layer):
            if(func(layer, param, layers, i)):
                return True
        else:
            print("[Error] layer class is wrong: "+layer.name)
    return False

def main_template(sDir, sFmt, img):
    #### protect code
    if( img == None ):
        gimp.message("[Error] Image None    \nPlease open a psd file...    ")
        return
    if( sDir == "" or sDir == None ):
        sDir = os.path.dirname(img.filename)
    #### get base path
    #img = gimp.image_list()[0]
    layer = img.active_layer
    rect = layer.offsets[0], layer.offsets[1], layer.width, layer.height
    gimp.message("Template run OK!" + "\n" 
            + "The rectangle of layer selected:" + "\n\n" 
            + str(rect))
    return
 
################################################################################
# call function
################################################################################
init_log()
register(
    "python_fu_template",
    "A simple Python-Fu 'template' plug-in.",
    "When run this plug-in, show 'Test OK' message.",
    "zlbd",
    "zlbd 2018.",
    "2018",
    "<Toolbox>/Layer/_Template(Py)",
    "RGB*, GRAY*",
    [
        (PF_DIRNAME, "string", "Directory",     s_Home),
        (PF_RADIO,   "format", "Image Format",  "png", (("png", "png"), ("bmp(32-bit)", "bmp"))),
        (PF_IMAGE,   "image",  "Input Sselect", None),
    ],
    [],
    main_template)
 
main()
