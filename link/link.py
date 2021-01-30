import os
import requests
import favicon
import subprocess
import gi
import pkg_resources

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

""" TODO
- tradurre tutto in inglese
- favicon delle app google fatto
- risolvere eventuali errori e notificarli: url non valido fatto 
- chiudere quando il lanciatore è creato fatto
- inserire opzione rimuovi
- impostare un'icona
- informarsi su come rendere installabile 
- informarsi sulle licenze fatto
- mettere su github fatto
"""

#xml da importare sottoforma di stringa
xml = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.36.0 -->
<interface>
  <requires lib="gtk+" version="3.22"/>
  <object class="GtkApplicationWindow" id="window">
    <property name="can_focus">False</property>
    <property name="title" translatable="yes">Url launcher</property>
    <signal name="destroy" handler="on_destroy" swapped="no"/>
    <child>
      <object class="GtkBox">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkEntry" id="url">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="margin_start">20</property>
            <property name="margin_end">20</property>
            <property name="margin_top">25</property>
            <property name="margin_bottom">25</property>
            <property name="placeholder_text" translatable="yes">Inserire qui l'url del sito</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkEntry" id="name">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="margin_start">20</property>
            <property name="margin_end">20</property>
            <property name="margin_bottom">25</property>
            <property name="placeholder_text" translatable="yes">Inserire il nome del lanciatore</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkCheckButton" id="checkdesktop">
            <property name="label" translatable="yes">Salvare il lanciatore sulla Scrivania</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">False</property>
            <property name="margin_start">20</property>
            <property name="draw_indicator">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkCheckButton" id="checkapplist">
            <property name="label" translatable="yes">Salvare il lanciatore tra le applicazioni</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">False</property>
            <property name="margin_start">20</property>
            <property name="draw_indicator">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkToggleButton" id="button">
            <property name="label" translatable="yes">Crea lanciatore</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="halign">center</property>
            <property name="margin_bottom">10</property>
            <signal name="clicked" handler="on_button_clicked" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">False</property>
            <property name="position">4</property>
          </packing>
        </child>
      </object>
    </child>
    <child type="titlebar">
      <placeholder/>
    </child>
  </object>
</interface>"""

class Link():
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_string(xml)
		self.builder.connect_signals(self)
		self.url = self.builder.get_object("url")
		self.name = self.builder.get_object("name")
		self.checkapplist = self.builder.get_object("checkapplist")
		self.checkdesktop = self.builder.get_object("checkdesktop")
		self.window = self.builder.get_object("window")
		self.window.show()
		
	def on_destroy(*args):
        	Gtk.main_quit()
        	
	def on_button_clicked(self, button):
		url=self.url.get_text()
		name=self.name.get_text()
		
		#cartella home tramite comando terminale
		home = subprocess.check_output(['xdg-user-dir', 'HOME']).decode("utf-8").rstrip()
		
		if not 'https://' in url and not 'http://' in url: url='https://'+url
		urlIcon=url
		
		#google apps
		if 'www.google' in url: urlIcon='https://about.google/'
		if 'mail.google' in url : urlIcon='https://www.google.com/intl/it/gmail/about/'
		if 'drive.google' in url : urlIcon='https://www.google.com/drive/'
		if 'docs.google.com/document' in url : urlIcon='https://www.google.com/docs/about/'
		if 'docs.google.com/presentation' in url : urlIcon='https://www.google.com/slides/about/'
		if 'photos.google' in url : urlIcon='https://www.google.com/photos/about/'
		if 'calendar.google' in url : urlIcon='https://www.google.com/calendar/about/'
		if 'docs.google.com/spreadsheets' in url : urlIcon='https://www.google.com/sheets/about/'
		if 'keep.google' in url : urlIcon='https://www.google.com/keep/'
		
		try:
			#prendere favicon
			icons = favicon.get(urlIcon)
			icon = icons[0]

			#salvare favicon
			response = requests.get(icon.url, stream=True)
			if not os.path.isdir(home+"/.local/share/link/icons") : os.makedirs(home+"/.local/share/link/icons") 
			icon_path=home+"/.local/share/link/icons/"+name+'.'+icon.format
			with open(icon_path, 'wb') as image:
				for chunk in response.iter_content(1024):
					image.write(chunk)
		
		except:
			icon_path=''

		#creazione lanciatore sul desktop
		if self.checkdesktop.get_active:
			desktop = subprocess.check_output(['xdg-user-dir', 'DESKTOP']).decode("utf-8").rstrip()		#cartella desktop tramite comando terminale
			f=open(desktop+"/"+name+".desktop","w+")
			f.write("#!/usr/bin/env xdg-open\n[Desktop Entry]\nVersion=1.0\nType=Application\nTerminal=false\nExec=firefox -new-tab '"+url+"'\nName="+name+"\nIcon="+icon_path)		#creazione del file .desktop
			f.close()
			
		#creazione lanciatore nella cartella applications
		if self.checkapplist.get_active():
			f=open(home+"/.local/share/applications/"+name+".desktop","w+")
			f.write("#!/usr/bin/env xdg-open\n[Desktop Entry]\nVersion=1.0\nType=Application\nTerminal=false\nExec=xdg-open "+url+"\nName="+name+"\nIcon="+icon_path)		#creazione del file .desktop
			f.close()
		
		Gtk.main_quit()
		
if __name__ == "__main__":
	main=Link()
	Gtk.main()

