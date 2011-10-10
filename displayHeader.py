#!/usr/bin/python

import sys
from gi.repository import Soup, SoupGNOME, Gtk
class displayHeader(Gtk.Box):

    @staticmethod
    def clicked_button_action (button,dhobject):
        url = dhobject.entry.get_text()
        if len(url) == 0:
            return
        if not url.startswith('http://'):
            url = "http://"+ url
        message = Soup.Message.new('GET', url)
        dhobject.session.send_message(message)

        if message.status_code == '200':
            dhobject.entry.set_text('')

        print message.status_code
        print message.reason_phrase

    @staticmethod
    def add_log_to_treeview (logger, printer, direction, header_line, textview):
        textbuffer=textview.get_buffer()
        textbuffer.set_text(textbuffer.get_text(textbuffer.get_start_iter(),
            textbuffer.get_end_iter(),
            False) +
            "%c %s \n" % (direction, header_line))
        textview.set_buffer(textbuffer)


    def __init__(self):
        Gtk.Box.__init__(self)
        self.session = Soup.SessionSync.new()
        self.session.add_feature_by_type(SoupGNOME.ProxyResolverGNOME)

        self.session.add_feature(Soup.CookieJarText.new("cookies.txt", False))
        self.set_spacing(6)
        self.set_orientation(Gtk.Orientation.VERTICAL)

        hbox = Gtk.Box()
        hbox.set_spacing(6)
        hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.pack_start(hbox, False, True, 6)

        self.entry = Gtk.Entry()
        self.entry.connect("activate", displayHeader.clicked_button_action, self)
        hbox.pack_start(self.entry, True, True, 0)

        button = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        button.connect("clicked", displayHeader.clicked_button_action, self)
        hbox.pack_start(button, False, False, 0)

        scrollwidget = Gtk.ScrolledWindow()
        scrollwidget.set_shadow_type(Gtk.ShadowType.IN)
        self.pack_start(scrollwidget, True, True, 0)

        textview = Gtk.TextView()
        textview.set_editable(False)
        scrollwidget.add(textview)

        Logger = Soup.Logger.new(Soup.LoggerLogLevel.HEADERS, -1)
        Logger.set_printer(displayHeader.add_log_to_treeview, textview)	
        self.session.add_feature(Logger)

if __name__ == '__main__':
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    window.set_size_request(340, 400)
    window.set_border_width(10)

    my_app = displayHeader()
    window.add(my_app)

    window.show_all()

    Gtk.main()
