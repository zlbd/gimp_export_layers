#!/usr/bin/env python
# Export each leaf layer into the image
# Author: zlbd

from gimpfu import *
import os, sys, platform
#sys.stderr = open('~/temp/gimp_err.txt', 'a')
#sys.stdout = open('~/temp/gimp_log.txt', 'a')

global s_css
global s_body
global s_index

def fwrite(fname, text):
    with open(fname,'w') as f:
        f.write(text)

def add_image_to_html(imgname, x, y, w, h):
    global s_css
    global s_body
    global s_index
    s_css += '\n\
    #'+imgname+' {\n\
        position:absolute;left:'+str(x)+';top:'+str(y)+';width:'+str(w)+';height:'+str(h)+';\n\
        z-index:'+str(s_index)+';\n\
    }'
    s_index -= 1
    s_body += '\n\
    <div id="{0}"><img src="img/{1}.png"/></div>'.format(imgname, imgname)

def export_html(htmlDir, htmlName):
    global s_css
    global s_body
    sHtml = '\
<html>\n\
<style type="text/css">\n\
{0}\n\
</style>\n\
<body>\n\
{1}\n\
</body>\n\
</html>'.format(s_css, s_body)
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
    # init log params
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
    sys.stderr = open(sErr, 'a')
    sys.stdout = open(sLog, 'a')
    return

def get_htmlname(name):
    htmlname = 'index.html'
    if(name[-4:] == '.psd'):
        htmlname = name[:-4] + '.html'
    return htmlname

def get_slash():
    ch='/';
    if(platform.system()=="Windows"):
        ch='\\'
    return ch;

def get_layername(layer):
    layername = layer.name
    chs=[' ', '\t', '\\', '/', '.']
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

def save_layer(fdir, fbasename, layer):
    x = layer.offsets[0]
    y = layer.offsets[1]
    w = layer.width
    h = layer.height
    add_image_to_html(fbasename, x, y, w, h)
    pdb.gimp_edit_copy(layer)
    newimage = pdb.gimp_edit_paste_as_new()
    drawable = newimage.layers[0]
    fname = fdir + fbasename + '.png'
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
            layername = get_layername(layer)
            save_layer(imgDir, layername, layer)
        else:
            print("[Error]: "+layer.name)
    layers = layerInput.layers
    return

def export_layers1(tips, img, sDir = ""):
    pass
 
def export_layers(tips, img, sDir = ""):
    # do init 
    init_params();
    # test code
    print("hello world")
    img = gimp.image_list()[0]
    sDir = "/home/zhaolong/temp/"
    # protect code
    if( img == None ):
        gimp.message("[Error] Image None    \nPlease open a psd file...    ")
        return
    # get base path
    if( sDir == "" ):
        sDir = os.path.dirname(img.filename)
    imgDir = get_imgpath(sDir)
    # use img as GroupLayer to export
    walk_groupLayer(img, imgDir)
    # save html 
    psdName = os.path.basename(img.filename)
    sHtml = get_htmlname(psdName)
    export_html(sDir, sHtml)
    # show result path
    gimp.message("Export Path:    \n" + sDir + "    ")
    return
 
register(
    "python_fu_export_layers",
    "A simple Python-Fu 'Export layers' plug-in    ",
    "When run this plug-in, export layers for PSD. ",
    "zlbd",
    "zlbd 2018.",
    "2018",
    "<Image>/Layer/_Export Layers (Py)",
    "RGB*, GRAY*",
    [
        (PF_STRING, "string", "Text:", "https://www.gimp.org/docs/python")
        (PF_IMAGE, "image", "Input image", None),
        (PF_DIRNAME, "dir", "Directory", None)
    ],
    [],
    export_layers1)
 
main()
