#!/usr/bin/python

import sys
from gi.repository import Soup, SoupGNOME, Gtk

class displayHeader(Gtk.Window):

    def __init__(self):
        super(displayHeader, self).__init__()

        global session
        session = Soup.SessionAsync.new()

        Logger = Soup.Logger.new(Soup.LoggerLogLevel.HEADERS, -1)
        Logger.set_printer(self.add_log_to_treeview, None)

        CookiesJar = Soup.CookieJarText.new("cookies.txt", False)
        session.add_feature_by_type(SoupGNOME.ProxyResolverGNOME)
        session.add_feature(Logger)
        session.add_feature(CookiesJar)

        self.connect("delete-event", Gtk.main_quit)
        self.set_size_request(340, 400)
        self.set_border_width(10)

        hbox = Gtk.Box()
        hbox.set_spacing(6)
        hbox.set_orientation(Gtk.Orientation.HORIZONTAL)

        vbox = Gtk.Box()
        vbox.set_spacing(6)
        vbox.set_orientation(Gtk.Orientation.VERTICAL)
        vbox.pack_start(hbox, False, True, 6)
        self.add(vbox)

        global entry 
        entry = Gtk.Entry()
        entry.connect("activate", self.clicked_button_action)
        button= Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        button.connect("clicked", self.clicked_button_action)
        hbox.pack_start(entry, True, True, 0)
        hbox.pack_start(button, False, False, 0)

        scrollwidget = Gtk.ScrolledWindow()
        scrollwidget.set_shadow_type(Gtk.ShadowType.IN)
        vbox.pack_start(scrollwidget, True, True, 0)

        global textview
        textview = Gtk.TextView()
        textview.set_editable(False)
        scrollwidget.add(textview)

        self.show_all()

    def add_log_to_treeview (logger, printer, direction, header, *args):
        textbuffer=textview.get_buffer()
        textbuffer.set_text(textbuffer.get_text(textbuffer.get_start_iter(),
                                                textbuffer.get_end_iter(),
                                                False)
                                                 +  "%c %s \n"%(direction, header))
        textview.set_buffer(textbuffer)

    def clicked_button_action (self, *args):
        url = entry.get_text()
        if len(url) == 0:
                return
        if not url.startswith('http://'):
                url = "http://"+ url
        message = Soup.Message.new('GET', url)
        session.queue_message(message, self.add_log_to_treeview, *args)

        if message.status_code == '200':
                entry.set_text('')
        entry.set_text('')

        print message.status_code
        print message.reason_phrase

if __name__ == '__main__':
    displayHeader()
    Gtk.main()
