#!/usr/bin/env python
# Export each leaf layer into the image
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
    return

def fwrite(fname, text):
    with open(fname,'w') as f:
        f.write(text)

def add_image_to_html(imgname, layername, x, y, w, h):
    global s_css
    global s_body
    global s_index
    sFmt = getImageFmt()
    s_css += '\n\
        #dv'+str(s_index)+' {\n\
            position:absolute;\n\
            left:'+str(x)+'; top:'+str(y)+'; width:'+str(w)+'; height:'+str(h)+';\n\
            z-index:'+str(s_index)+';\n\
        }'
    s_body += '\n\
        <div id="dv{0}"><img src="img/{1}.{2}"/><!--{3}--></div>'.format(str(s_index), imgname, sFmt, layername)
    s_index -= 1

def export_html(htmlDir, htmlName):
    global s_css
    global s_body
    sHtml = '<html>\n\
    <style type="text/css">{0}\n\
    </style>\n\
    <body>{1}\n\
    </body>\n</html>'.format(s_css, s_body)
    sSlash = get_slash()
    if(htmlDir[-1] != sSlash):
        htmlDir += sSlash
    fname = htmlDir + htmlName
    fwrite(fname, sHtml)

def init_params():
    # init html params
    global s_css
    global s_body
    global s_index
    s_css  = ""
    s_body = ""
    s_index = 10000
    return

def get_htmlname(name):
    htmlname = ''
    if(name[-4:] == '.psd'):
        htmlname = name[:-4] + '.html'
    elif(name[-5:] == '.html'):
        htmlname = name
    else:
        htmlname = name[:-4] + '.html'
    return htmlname

def get_slash():
    ch='/';
    if(platform.system()=="Windows"):
        ch='\\'
    return ch;

def get_layername(layer):
    layername = layer.name
    chs=[' ', '\t', '\\', '/', '.', '#']
    for ch in chs:
        layername = layername.replace(ch, '_')
    return layername

def get_imgpath(basepath):
    sSlash = get_slash()
    if(basepath[-1] != sSlash):
        basepath += sSlash
    imgpath = basepath + 'img' + sSlash
    if not os.path.exists(imgpath):
        os.mkdir(imgpath)
    return imgpath;

def getImageFmt():
    global s_Fmt
    return s_Fmt


def setImageFmt(sFmt):
    global s_Fmt
    s_Fmt = sFmt
    return

def save_layer(fdir, layer):
    fbasename = get_layername(layer)
    x = layer.offsets[0]
    y = layer.offsets[1]
    w = layer.width
    h = layer.height
    add_image_to_html(fbasename, layer.name, x, y, w, h)
    pdb.gimp_edit_copy(layer)
    newimage = pdb.gimp_edit_paste_as_new()
    drawable = newimage.layers[0]
    fname = fdir + fbasename + '.' + getImageFmt()
    pdb.gimp_file_save(newimage, drawable, fname, fname)
    pdb.gimp_image_delete(newimage)
    return

def walk_groupLayer(layerInput, imgDir):
    layers = layerInput.layers
    nCount = len(layers)
    for i in range(0, nCount):
        layer = layers[i]
        if(layer.__class__ == gimp.GroupLayer):
            walk_groupLayer(layer, imgDir)
        elif(layer.__class__ == gimp.Layer):
            save_layer(imgDir, layer)
        else:
            print("[Error]: "+layer.name)
    return


def export_layers(sDir, sFmt, img):
    # do init 
    #gimp.message(sFmt)
    setImageFmt(sFmt)
    init_params();
    # protect code
    if( img == None ):
        gimp.message("[Error] Image None    \nPlease open a psd file...    ")
        return
    # get base path
    if( sDir == "" or sDir == None ):
        sDir = os.path.dirname(img.filename)
    #if( sName == "" or sName == None ):
    #    sName  = os.path.basename(img.filename)
    ##Export file name, using PSD name by default.
    sName  = os.path.basename(img.filename)
    imgDir = get_imgpath(sDir)
    # use img as GroupLayer to export
    walk_groupLayer(img, imgDir)
    # save html 
    sHtml = get_htmlname(sName)
    export_html(sDir, sHtml)
    ## show result path
    #gimp.message("Export Path:\n"+sDir+"\n\nExport Name:\n"+sHtml)
    return
 
################################################################################
# call functions
################################################################################

init_log()

register(
    "python_fu_export_layers",
    "A simple Python-Fu 'Export layers' plug-in.\n(Export file name, using PSD name by default.)",
    "When run this plug-in, export layers for PSD. ",
    "zlbd",
    "zlbd 2018.",
    "2018",
    "<Toolbox>/Layer/_Export Layers(Py)",
    "RGB*, GRAY*",
    [
        (PF_DIRNAME, "dir", "Export Path",  None),
        (PF_RADIO,   "fmt", "Export Format", "png", (("png", "png"), ("bmp", "bmp"))),
        (PF_IMAGE,   "img", "Input Image",  None),
    ],
    [],
    export_layers)
 
main()
