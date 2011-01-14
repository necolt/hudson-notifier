import gtk

from hudsonnotifier import AboutHudsonnotifierDialog, PreferencesHudsonnotifierDialog
from hudsonnotifier.dialogs import success, unstable, failure
from hudsonnotifier import dialogs

class HudsonNotifierTrayIcon:

  def __init__(self, config):
    self.config = config
    self.projects = {}

    self.statusIcon = gtk.StatusIcon()
    self.statusIcon.set_from_stock(gtk.STOCK_DIALOG_QUESTION)
    self.statusIcon.set_visible(True)
    self.statusIcon.set_tooltip(dialogs.title)

    self.menu = gtk.Menu()

    self.menu.append(gtk.SeparatorMenuItem())
    self.executeItem = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
    self.executeItem.connect('activate', self.execute_cb, self.statusIcon)
    self.menu.append(self.executeItem)
    self.aboutItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
    self.aboutItem.connect('activate', self.about_cb, self.statusIcon)
    self.menu.append(self.aboutItem)
    self.quitItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    self.quitItem.connect('activate', self.quit_cb, self.statusIcon)
    self.menu.append(self.quitItem)
    self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)

  def finish_initializing(self):
    self.statusIcon.set_visible(1)

  def add_project(self, item):
    self.projects[item.name] = ProjectEntry()
    self.projects[item.name].include = self.config.get_project(item.name)
    self.projects[item.name].menu = gtk.CheckMenuItem(label=None)
    self.projects[item.name].menu.set_active(self.projects[item.name].include)
    self.projects[item.name].menu.connect('toggled', self.toggle_include_project, item.name)
    hbox = gtk.HBox(homogeneous=False, spacing=0)
    label = gtk.Label(item.name)
    label.set_alignment(xalign=0, yalign=0.5)
    hbox.pack_start(label, True, True, 0)
    self.projects[item.name].icon = gtk.Image()
    hbox.pack_start(self.projects[item.name].icon, False, False, 0)
    self.projects[item.name].menu.add(hbox)
    self.menu.prepend(self.projects[item.name].menu)
    self.update_project(item, alertChange=False)

  def remove_projects(self):
    for key, value in self.projects.iteritems():
	  self.menu.remove(value.menu)
    self.projects.clear()

  def remove_project(self, item):
    if self.projects.has_key(item.name):
        self.menu.remove(self.projects[item.name].menu)
        del self.projects[item.name]

  def update_project(self, item, alertChange=True):
    if(self.projects.has_key(item.name)):
        self.projects[item.name].icon.set_from_stock(self.__status_to_icon__(item.status), gtk.ICON_SIZE_MENU)
    else:
        self.add_project(item)
    self.projects[item.name].status = item.status
    self.__update_notification_icon__()
    if self.projects[item.name].include and alertChange:
        if item.status == 'SUCCESS':
            success(item).show()
        elif item.status == 'UNSTABLE':
            unstable(item).show()
        elif item.status == 'FAILURE':
            failure(item).show()

  def toggle_include_project(self, widget, project_name):
    self.projects[project_name].include = self.projects[project_name].menu.get_active()
    self.__update_notification_icon__()
    self.config.save_project(project_name, self.projects[project_name].menu.get_active())

  def __update_notification_icon__(self):
    resultIcon = gtk.STOCK_YES
    for key,item in self.projects.iteritems():
        if not item.include:
            continue
        if item.status == 'UNSTABLE':
            resultIcon = gtk.STOCK_DIALOG_WARNING
        elif item.status == 'FAILURE':
            resultIcon = gtk.STOCK_DIALOG_ERROR
            break
    self.statusIcon.set_from_stock(resultIcon)

  def __status_to_icon__(self, status):
    if status == 'SUCCESS':
        return gtk.STOCK_YES
    elif status == 'UNSTABLE':
        return gtk.STOCK_DIALOG_WARNING
    elif status == 'FAILURE':
        return gtk.STOCK_DIALOG_ERROR
    else:
        return gtk.STOCK_DIALOG_QUESTION

  def execute_cb(self, widget, event, data = None):
    prefs = PreferencesHudsonnotifierDialog.NewPreferencesHudsonnotifierDialog()
    response = prefs.run()
    if response == gtk.RESPONSE_OK:
        #make any updates based on changed preferences here
        pass
    prefs.destroy()

  def about_cb(self, widget, data = None):
    """about - display the about box for hudsonnotifier """
    about = AboutHudsonnotifierDialog.NewAboutHudsonnotifierDialog()
    response = about.run()
    about.destroy()

  def quit_cb(self, widget, data = None):
    gtk.main_quit()

  def popup_menu_cb(self, widget, button, time, data = None):
    if button == 3:
      if data:
        data.show_all()
        data.popup(None, None, gtk.status_icon_position_menu,
                   3, time, self.statusIcon)

class ProjectEntry(object):
    menu = None
    icon = None
    status = None
    include = True
