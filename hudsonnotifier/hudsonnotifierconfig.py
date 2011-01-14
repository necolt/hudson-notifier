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

# THIS IS Hudsonnotifier CONFIGURATION FILE
# YOU CAN PUT THERE SOME GLOBAL VALUE
# Do not touch until you know what you're doing.
# you're warned :)

# where your project will head for your data (for instance, images and ui files)
# by default, this is ../data, relative your trunk layout
__hudsonnotifier_data_directory__ = '../data/'


import os
from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record
from hudsonnotifier.Event import Event

class project_path_not_found(Exception):
    pass

def getdatapath():
    """Retrieve hudsonnotifier data path

    This path is by default <hudsonnotifier_lib_path>/../data/ in trunk
    and /usr/share/hudsonnotifier in an installed version but this path
    is specified at installation time.
    """

    # get pathname absolute or relative
    if __hudsonnotifier_data_directory__.startswith('/'):
        pathname = __hudsonnotifier_data_directory__
    else:
        pathname = os.path.dirname(__file__) + '/' + __hudsonnotifier_data_directory__

    abs_data_path = os.path.abspath(pathname)
    if os.path.exists(abs_data_path):
        return abs_data_path
    else:
        raise project_path_not_found


class HudsonNotifierConfig(object):

    def __init__(self):
        #set up couchdb and the preference info
        self.__db_name = "hudson-notifier"
        self.__database = CouchDatabase(self.__db_name, create=True)
        self.__preferences = None
        self.__key = None

        #set the record type and then initalize the preferences
        self.__record_type = "http://wiki.ubuntu.com/Quickly/RecordTypes/Hudsonnotifier/Preferences"
        self.__preferences = self.__get_preferences()
        
        #configuration change event
        self.configurationChanged = Event()
        

    def __get_preferences(self):
        """get_preferences  -returns a dictionary object that contain
        preferences for hudsonnotifier. Creates a couchdb record if
        necessary.
        """

        if self.__preferences == None: #the dialog is initializing
            self.__load_preferences()

        #if there were no saved preference, this
        return self.__preferences

    def __load_preferences(self):
        #TODO: add prefernces to the self.__preferences dict
        #default preferences that will be overwritten if some are saved
        self.__preferences = {"record_type":self.__record_type}

        results = self.__database.get_records(record_type=self.__record_type, create_view=True)

        if len(results.rows) == 0:
            #no preferences have ever been saved
            #save them before returning
            self.__key = self.__database.put_record(Record(self.__preferences))
        else:
            self.__preferences = results.rows[0].value
            del self.__preferences['_rev']
            self.__key = results.rows[0].value["_id"]

    def __save_preferences(self):
        self.__database.update_fields(self.__key, self.__preferences)
        self.configurationChanged(self)

    def getUrl(self):
        return self.__preferences.get("url", None)

    def setUrl(self, url):
        self.__preferences["url"] = url
        self.__save_preferences()

    def save_project(self, project, value):
        self.__preferences["project_%s"%(project)] = value
        self.__save_preferences()

    def get_project(self, project):
        print "Loading project %s"%project
        return self.__preferences.get("project_%s"%(project), True)

    url = property(getUrl, setUrl, doc="Url to connect to the hudson build server on")

globalConfig = HudsonNotifierConfig()

def getconfig():
    return globalConfig
