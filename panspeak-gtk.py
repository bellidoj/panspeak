#!/usr/bin/env python3

import os
import subprocess
import re
from gi.repository import Gtk
from contextlib import closing

class myMain:

    def __init__(self):
        self.gladefile = "panspeak.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.handlers = {
            "on_window1_destroy": self.windowDestroy,
            #"on_window1_delete_event": self.windowDestroy,
            #"on_window1_destroy_event": self.windowDestroy,
            "on_menuHelpAbout_activate": self.menuAboutActivate,
            "on_menuFileOpen_activate": self.menuOpenActivate,
            "on_menuFileSave_activate": self.menuSaveActivate,
            "on_menuFileExit_activate": self.QuitActivate,
            "on_runButton_clicked": self.translate,
            }
        self.builder.connect_signals(self.handlers)
        self.window = self.builder.get_object("window1")
        self.window.set_title("Panspeak")
        self.window.set_default_size(640, 480)
        self.mytextview = self.builder.get_object("textview")
        self.mytextview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.mybuffer = self.mytextview.get_buffer()
        self.mybuffer.connect("changed", self.contentChanged)

        self.window.show()

        self.documentName = "Untitled document"
        self.modified = False
                
    def windowDestroy(*args):
        for i in args:
            message = "event {0} fired.".format(str(i))
            print(message)
            
        print("Destroy!!!!!!!")
        Gtk.main_quit()

    def contentChanged(self, textbuffer):
        self.modified = True
        self.updateTitle()
    
    def updateTitle(self):
        if self.modified == False:
            appendix = ''
        else:
            appendix = '*'

        title = "Panspeak: {0}{1}".format(os.path.basename(self.documentName), appendix)  
        self.window.set_title(title)
    
    def menuAboutActivate(self, widget):
        dialog = Gtk.AboutDialog(None, self.window, None)
        dialog.set_program_name("Panspeak")
        dialog.set_version("0.1")
        dialog.set_comments("Get text and text to speech at once")
        dialog.set_website("http://peregilllica.com") 
        dialog.set_website_label("Peregilllica.com") 
        response = dialog.run()
        dialog.destroy()
     
        
    def menuOpenActivate(self, widget):
        dialog = Gtk.FileChooserDialog("Elige un archivo", self.window,
            Gtk.FileChooserAction.OPEN)
        dialog.add_button("Abrir", Gtk.ResponseType.OK)
        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        
        self.add_filters(dialog)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.documentName = dialog.get_filename()
            self.loadFile()
        elif response == Gtk.ResponseType.CANCEL:
            pass
            
        dialog.destroy()
        
        self.modified = False 

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Todos los archivos de texto")
        filter_text.add_mime_type("text/plain")
        filter_all = Gtk.FileFilter()
        filter_all.set_name("Todos los archivos")
        filter_all.add_pattern("*.*")
        dialog.add_filter(filter_text)
        dialog.add_filter(filter_all)

    def menuSaveActivate(self, widget):
        if self.modified:
            self.saveFile()
        else:
            message = "{0} is updated. Nothing done.".format(os.path.basename(self.documentName))
            print(message)
            pass

    def QuitActivate(self, widget):
        if self.modified:
            message = "Document {0} was not saved. Exit anyway?".format(os.path.basename(self.documentName)) 
            dialog = Gtk.MessageDialog(self.window, Gtk.DialogFlags.MODAL, 
                Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, message)
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                dialog.destroy()
                Gtk.main_quit()
            elif response == Gtk.ResponseType.NO:
                dialog.destroy()
        else:
            Gtk.main_quit()
                    
    def loadFile(self):
        with closing(open(self.documentName)) as text_file:
            self.mybuffer.set_text(text_file.read())
            self.mytextview.set_buffer(self.mybuffer)
            start_iter = self.mybuffer.get_start_iter()
            end_iter = self.mybuffer.get_end_iter()

            mytext = self.mybuffer.get_text(start_iter, end_iter, True)
            self.updateTitle()
        message = "{0} loaded.".format(os.path.basename(self.documentName))
        print(message)

    def saveFile(self):
        
        start_iter = self.mybuffer.get_start_iter()
        end_iter = self.mybuffer.get_end_iter()
        mytext = self.mybuffer.get_text(start_iter, end_iter, True)
            
        with closing(open(self.documentName, "w")) as text_file:
            print(mytext, file=text_file)
            self.modified = False
            self.updateTitle()

        message = "File saved: {0}".format(os.path.basename(self.documentName))
        print(message)

    def translate(self, widget):
        pattern = re.compile(r'#-(?P<text>.*?)\|(?P<speech>.*?)-#')
        start_iter = self.mybuffer.get_start_iter()
        end_iter = self.mybuffer.get_end_iter()

        mytext = self.mybuffer.get_text(start_iter, end_iter, True)
        splitedFileName = os.path.splitext(self.documentName)
        text_file = splitedFileName[0] + "-text.txt"
        speech_file = splitedFileName[0] + "-speech.txt"
        
        with closing(open(text_file, "w")) as t_file:
            for line in mytext.split("\n"):
                while True:
                    match = re.search(pattern, line)
                    if match: 
                        line = re.sub(pattern, match.group("text"), line, 1)
                    else:
                        break
                t_file.write(line + "\n")
            
        with closing(open(speech_file, "w")) as s_file:
            for line in mytext.split("\n"):
                while True:
                    match = re.search(pattern, line)
                    if match: 
                        line = re.sub(pattern, match.group("speech"), line, 1)
                    else:
                        break
                s_file.write(line + "\n")

if __name__ == "__main__":
    main = myMain()
    Gtk.main()
