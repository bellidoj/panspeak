#!/usr/bin/env python3

import os
import subprocess
import re
from gi.repository import Gtk
from contextlib import closing

class myMain:

    

    def __init__(self):
        self.Encode = False
        self.gladefile = "panspeak.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.handlers = {
            "on_window1_destroy": self.windowDestroy,
            "on_window1_destroy_event": self.windowDestroy,
            "on_menuHelpAbout_activate": self.menuAboutActivate,
            "on_menuFileOpen_activate": self.menuOpenActivate,
            "on_menuFileSave_activate": self.menuSaveActivate,
            "on_menuFileSaveAs_activate": self.menuSaveAsActivate,
            "on_menuFileExit_activate": self.QuitActivate,
            "on_runButton_clicked": self.translate,
            "on_menuPreferences_activate": self.showPreferencesWindow,
            "on_preferencesCloseButton_clicked": self.closePreferencesWindow,
            "on_menuAddMarker_activate":self.addMarker,
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
        dialog.set_version("0.2")
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
        filter_pspk = Gtk.FileFilter()
        filter_pspk.set_name("Todos los archivos panspeak")
        filter_pspk.add_pattern("*.pspk")
        dialog.add_filter(filter_pspk)
        dialog.add_filter(filter_text)
        dialog.add_filter(filter_all)

    def menuSaveActivate(self, widget):
        if self.modified:
            self.saveFile()
        else:
            message = "{0} is updated. Nothing done.".format(os.path.basename(self.documentName))
            print(message)
            pass

    def menuSaveAsActivate(self, widget):
        dialog = Gtk.FileChooserDialog("Save file", self.window,
            Gtk.FileChooserAction.SAVE)

        dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        dialog.add_button("Guardar", Gtk.ResponseType.ACCEPT)

        dialog.set_current_name(self.documentName)
        dialog.set_do_overwrite_confirmation(True)
        
        self.add_filters(dialog)

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            self.documentName = dialog.get_filename()
            self.saveFile()
            
        elif response == Gtk.ResponseType.CANCEL:
            pass
            
        dialog.destroy()
        self.updateTitle()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*.*")
        filter_pspk = Gtk.FileFilter()
        filter_pspk.set_name("Todos los archivos panspeak")
        filter_pspk.add_pattern("*.pspk")
        dialog.add_filter(filter_pspk)
        dialog.add_filter(filter_text)
        dialog.add_filter(filter_all)


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
        if self.Encode:
            with closing(open(speech_file)) as encode_file:
                self.tts(speech_file, encode_file.read())
            self.encode(speech_file)

    def showPreferencesWindow(self, widget):
        self.preferenceswindow = self.builder.get_object("preferencesWindow")
        self.preferenceswindow.show()

    def closePreferencesWindow(self, widget):
        if widget.get_active():
            self.Encode = True
            print("Encoding: " + str(self.Encode))
        else:
            self.Encode = False
            print("Enconding: " + str(self.Encode)) 

        self.preferenceswindow.hide()

    def addMarker(self, widget):
        marker = "#-|-#"
        self.mybuffer.insert_at_cursor(marker)
        cursorPosition = self.mybuffer.get_property("cursor-position")
        myiter = self.mybuffer.get_iter_at_offset(cursorPosition -3)
        self.mybuffer.place_cursor(myiter)
        
    def tts(self, filename, text):
        fileout = filename + ".wav"
        command = 'pico2wave|--wave={0}|--lang=es-ES|--|{1}'.format(fileout, text)
        subprocess.call(command.split('|'), shell=False)
        return True

    def encode(self, filename):
        filein = filename + ".wav"
        fileout = filename + ".mp3"

        command = 'lame|{0}|{1}'.format(filein, fileout)
        
        subprocess.call(command.split("|"), shell=False)

        return True

if __name__ == "__main__":
    main = myMain()
    Gtk.main()
