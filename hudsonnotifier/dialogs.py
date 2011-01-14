import pynotify
import os

from hudsonnotifier.hudsonnotifierconfig import getdatapath

title = 'Hudson Build Notification'
pynotify.init('Hudson Notify')

def success(job):
	n = pynotify.Notification(title,
		'%s build #%s successfully built' %(job.name, job.build),
		'dialog-ok')
	# n.set_urgency(pynotify.URGENCY_CRITICAL)
	return n

def unstable(job):
	n = pynotify.Notification(title,
		'%s build #%s is unstable' % (job.name, job.build),
		'dialog-warning')
	# n.set_urgency(pynotify.URGENCY_CRITICAL)
	return n

def failure(job):
	n = pynotify.Notification(title,
		'%s build #%s failed' %(job.name, job.build),
		'dialog-error')
	# n.set_urgency(pynotify.URGENCY_CRITICAL)
	return n
