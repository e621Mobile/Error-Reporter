from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Max
from django.template import loader, Context
from error_report.models import *


def login(request,username,password):
	user = authenticate(email=username, password=password)

	if(user != None):
		try:
			user.errorreportuser
			auth_login(request,user)
			return True
		except:
			return False
	else:
		return False


def is_logged_in(request):
	if(request.user.is_authenticated()):
		try:
			request.user.errorreportuser
			return True
		except:
			return False
	else:
		return False

def get_apps(request):
	if(is_logged_in(request)):
		return App.objects.filter(user__user__email = request.user.email)
	else:
		return []

def get_reports(request,app,offset=0,limit=20,has_messages=None,has_description=True,tags=[]):
	if(is_logged_in(request)):
		query = Report.objects.filter(app_id=app)
		if(has_messages != None):
			query = query.annotate(max_message=Max('message__local_id'))
			query = query.exclude(max_message=None) if has_messages else query.filter(max_message=None)
		if(has_description!=None):
			query = query.filter(text__gt="") if has_description else query.filter(text="")
		for tag in tags:
			query = query.filter(reporttag__tag=tag)
		return (query.count(),list(query[offset:offset+limit]))
	else:
		return (0,[])

@transaction.atomic
def add_report(request,text,log,tags,app):
	try:
		if((text or log) and App.objects.filter(pk=app).exists()):
			ip = "";
			
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
			if x_forwarded_for:
				ip = x_forwarded_for.split(',')[0]
			else:
				ip = request.META.get('REMOTE_ADDR')
			
			app = App.objects.get(app_id = app)
			report = None
			
			try:
				report = Report.objects.create(ip = ip, text=text.strip(), log=log.strip(), app=app)
			except Exception as e:
				print e
				return None;
			
			tags.sort()
			
			for tag in tags:
				ReportTag.objects.create(tag=tag,report=report)

			if(text):
				template = loader.get_template('mail/error_report_notification_new_report.html')
				context = Context({
					'report': report,
					'domain': settings.DOMAIN_NAME,
				})

				msg = EmailMultiAlternatives('New report for ' + app.app_id,template.render(context),'noreply@'+settings.DOMAIN_NAME,[app.email])
				msg.send()
			
			return report.hash
		
		return None
	except Exception as e:
		print e
		return None

@transaction.atomic
def add_message(request,report,message,author):
	"""
		@type report: str
		@type message: str
		@type author: str
	"""
	try:
		report = Report.objects.get(hash = report)

		author = author.strip()
		message = message.strip()

		if(author.__len__()==0 or message.__len__()==0):
			return None

		message = Message.objects.create(text=message, report=report, author=author)

		template = loader.get_template('mail/error_report_notification_new_message.html')
		context = Context({
			'message': message,
			'domain': settings.DOMAIN_NAME,
		})

		msg = EmailMultiAlternatives('New message for ' + report.app.app_id,template.render(context),'noreply@'+settings.DOMAIN_NAME,[report.app.email])
		msg.send()

		return True

	except Exception as e:
		print e
		return None

@transaction.atomic
def get_messages(request,report):
	"""
		@type report: str
	"""
	try:
		ret = Message.objects.all().filter(report__hash=report).order_by('local_id').values("time","author","text","local_id")

		for i in xrange(len(ret)):
			ret[i]["time"] = str(ret[i]["time"])

		return ret;

	except Exception as e:
		print e
		return None

def get_report(request,report):
	try:
		if(not is_logged_in(request)):
			return None
		return Report.objects.get(hash = report)
	except Exception as e:
		print e
		return None
