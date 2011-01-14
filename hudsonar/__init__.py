import feedparser

class HudsonServer(object):
    def __init__(self, url):
        self.url = url
        self.old_items = None

    def get_current_status(self):
        feed = feedparser.parse(self.url)
        items = [t['title'] for t in feed['entries']]
        return [HudsonBuildResult(item) for item in items]

    def get_updates(self):
        if self.old_items is None:
            self.old_items = self.get_current_status()
        items = self.get_current_status()
        item_names = [item.name for item in items]
        item_names.sort()
        deleted_items = filter(lambda item: item.name not in item_names, self.old_items)
       
        # print "Items: %s"%(items)
        new_items = list(set(items).difference(self.old_items))
        
        # print "New items: %s"%(new_items)
        # print "Old items: %s"%(old_items)
        if len(new_items) > 0:
            print "Found items: %s"%([str(item) for item in new_items])
        
        self.old_items = items
        return deleted_items, new_items
        

class HudsonBuildResult(object):
    def __init__(self, status):
        i = status.split(' ', 2)
        self.name, self.build, self.status = (i[0], i[1], i[2])
        self.build = self.build.strip('#')
        self.status = self.status.replace('(', '').replace(')','').split(' ')[0]
        if self.status == 'stable' or self.status == 'back':
            self.status = 'SUCCESS' 
        elif self.status == 'aborted':
            self.status = 'UNSTABLE' 
        elif self.status == 'broken':
            self.status = 'FAILURE' 


    def __eq__(self, obj):
        return self.name == obj.name and self.build == obj.build and self.status == obj.status
        
    def __ne__(self, obj):
        return not self.__eq__(obj)
        
    def __hash__(self):
        return hash(self.name) ^ hash(self.build) ^ hash(self.status)

    def __str__(self):
        return "%s %s %s"%(self.name, self.build, self.status)
   
