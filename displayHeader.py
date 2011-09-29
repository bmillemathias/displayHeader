#!/usr/bin/python

import sys
from gi.repository import Soup, SoupGNOME, Gtk

#if len(sys.argv) < 2:
 #   sys.exit(1)

#URL = sys.argv[1]

class displayHeader():

    def clicked_button_action (button,entry):
        url = entry.get_text()
        if len(url) == 0:
                return
        if not url.startswith('http://'):
                url = "http://"+ url
        message = Soup.Message.new('GET', url)
        session.send_message(message)

        if message.status_code == '200':
                entry.set_text('')
                
        print message.status_code
        print message.reason_phrase

    def add_log_to_treeview (logger, printer, data, laa, loo):
        textbuffer=textview.get_buffer()
        textbuffer.set_text(textbuffer.get_text(textbuffer.get_start_iter(),
                                                textbuffer.get_end_iter(),
                                                False)
                                                 +  "%c %s \n"%(data, laa))
        textview.set_buffer(textbuffer)

    global session
    session = Soup.SessionSync.new()

    Logger = Soup.Logger.new(Soup.LoggerLogLevel.HEADERS, -1)
    Logger.set_printer(add_log_to_treeview, None)

    CookiesJar = Soup.CookieJarText.new("cookies.txt", False)
    session.add_feature_by_type(SoupGNOME.ProxyResolverGNOME)
    session.add_feature(Logger)
    session.add_feature(CookiesJar)

    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    window.set_size_request(340, 400)
    window.set_border_width(10)

    hbox = Gtk.Box()
    hbox.set_spacing(6)
    hbox.set_orientation(Gtk.Orientation.HORIZONTAL)

    vbox = Gtk.Box()
    vbox.set_spacing(6)
    vbox.set_orientation(Gtk.Orientation.VERTICAL)
    vbox.pack_start(hbox, False, True, 6)
    window.add(vbox)

    entry = Gtk.Entry()
    button= Gtk.Button.new_from_stock(Gtk.STOCK_OK)
    button.connect("clicked", clicked_button_action, entry)
    hbox.pack_start(entry, True, True, 0)
    hbox.pack_start(button, False, False, 0)

    scrollwidget = Gtk.ScrolledWindow()
    scrollwidget.set_shadow_type(Gtk.ShadowType.IN)
    vbox.pack_start(scrollwidget, True, True, 0)

    global textview
    textview = Gtk.TextView()
    textview.set_editable(False)
    scrollwidget.add(textview)

    window.show_all()

    Gtk.main()

if __name__ == '__main__':
    displayHeader()
