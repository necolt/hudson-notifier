# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright (C) 2009 Philip Peitsch <philip.peitsch@gmail.com>
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.
#
#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import sys
import os
import gtk

from hudsonnotifier.hudsonnotifierconfig import getconfig, getdatapath

class PreferencesHudsonnotifierDialog(gtk.Dialog):
    __gtype_name__ = "PreferencesHudsonnotifierDialog"
    prefernces = {}

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a PreferencesHudsonnotifierDialog requires redeading the associated ui
        file and parsing the ui definition extrenally,
        and then calling PreferencesHudsonnotifierDialog.finish_initializing().

        Use the convenience function NewPreferencesHudsonnotifierDialog to create
        NewAboutHudsonnotifierDialog objects.
        """

        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a AboutHudsonnotifierDialog object with it in order to finish
        initializing the start of the new AboutHudsonnotifierDialog instance.
        """

        #get a reference to the builder and set up the signals
        self.urlEntry = builder.get_object("address_value")
        if getconfig().url == None:
            self.urlEntry.set_text('')
        else:
            self.urlEntry.set_text(getconfig().url)
        self.builder = builder
        self.builder.connect_signals(self)

    def ok(self, widget, data=None):
        """ok - The user has elected to save the changes.
        Called before the dialog returns gtk.RESONSE_OK from run().
        """
        getconfig().url = self.urlEntry.get_text()

    def cancel(self, widget, data=None):
        """cancel - The user has elected cancel changes.
        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """
        pass

def NewPreferencesHudsonnotifierDialog():
    """NewPreferencesHudsonnotifierDialog - returns a fully instantiated
    PreferencesHudsonnotifierDialog object. Use this function rather than
    creating a PreferencesHudsonnotifierDialog instance directly.
    """

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'PreferencesHudsonnotifierDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    dialog = builder.get_object("preferences_hudsonnotifier_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewPreferencesHudsonnotifierDialog()
    dialog.show()
    gtk.main()

