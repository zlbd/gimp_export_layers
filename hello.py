#!/usr/bin/env python
# Show Hello message
# Author: zlbd

import gtk
from gimpfu import *


class PyApp(gtk.Window):
    def __init__(self, sTips):
        super(PyApp, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.set_default_size(300,200)
        self.set_title("Message in PyGTK")
        label = gtk.Label(sTips)
        self.add(label)
        self.show()

def hello_msg(sTips):
    PyApp(sTips)
    gtk.main()

register(
    "python_fu_hello_msg",
    "A simple Python-Fu 'Hello Msg' plug-in.",
    "When run this plug-in, show a message hello world. ",
    "zlbd",
    "zlbd 2018.",
    "2018",
    "<Toolbox>/Layer/_Hello Msg(Py)",
    "",
    [
        (PF_STRING, "string", "hello string", "hello world"),
    ],
    [],
    hello_msg)

main()


