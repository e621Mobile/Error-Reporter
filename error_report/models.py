from django.db import models
from django.utils import timezone
import string
from random import randint

class ErrorReportUser(models.Model):
	user = models.OneToOneField('RSS.User')

	def __unicode__(self):
		return self.user.__unicode__()

class App(models.Model):
	user = models.ForeignKey("ErrorReportUser", null=False, blank=False)
	email = models.EmailField()
	app_id = models.CharField(max_length=16, primary_key=True)
	
	def __unicode__(self):
		return self.app_id

class Report(models.Model):
	HASH_CHARS = string.letters+string.digits;

	ip = models.IPAddressField()
	app = models.ForeignKey(App)
	
	report_id = models.IntegerField(default=0, blank=True)
	
	log = models.TextField(default="")
	text = models.TextField()

	hash = models.CharField(max_length=32, default="",primary_key=True)
	
	time = models.DateTimeField(null=False, blank=False, default=timezone.now())
	
	def save(self,*args,**kwargs):
		if(not self.report_id):
			report_max = Report.objects.filter(app=self.app_id).aggregate(models.Max('report_id'))['report_id__max']
			self.report_id = report_max+1 if report_max else 1

		if(not self.hash):
			self.hash = ''.join([self.HASH_CHARS[randint(0,self.HASH_CHARS.__len__()-1)] for i in xrange(32)])
			while(Report.objects.filter(hash=self.hash).exists()):
				self.hash = ''.join([self.HASH_CHARS[randint(0,self.HASH_CHARS.__len__()-1)] for i in xrange(32)])

		super(Report,self).save(*args,**kwargs)
	
	def __unicode__(self):
		return "Report %d from app %s: %s" % (self.report_id, self.app, (self.text[:100]+"..." if len(self.text) > 100 else self.text))

class ReportTag(models.Model):
	tag = models.CharField(max_length=32, db_index=True, null=False, blank=False)
	report = models.ForeignKey(Report, db_index=True, null=False, blank=False)
	
	def __unicode__(self):
		return "Tag %s on report %s" % (self.tag, self.report.report_id)

class Message(models.Model):
	report = models.ForeignKey(Report, null=False, blank=False)
	time = models.DateTimeField(null=False, blank=False, default=timezone.now)
	author = models.CharField(default="", max_length=32)
	text = models.TextField()
	local_id = models.IntegerField(default=0)

	def save(self,*args,**kwargs):
		if(not self.local_id):
			local_id = Message.objects.filter(report=self.report_id).aggregate(models.Max('local_id'))['local_id__max']
			self.local_id = local_id+1 if local_id else 1

		super(Message,self).save(*args,**kwargs)

	def __unicode__(self):
		return "%d. Message %d from %s from report %s: %s" % (self.id, self.local_id, self.author, self.report_id, (self.text[:100]+"..." if len(self.text) > 100 else self.text))