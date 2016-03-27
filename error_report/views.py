import json
from django.core.urlresolvers import reverse
from django.http import *
from django.template import loader, RequestContext
from error_report import controller
from math import ceil

def index(request):
	if(not controller.is_logged_in(request)):
		return HttpResponseRedirect(reverse("error_report.views.login"))

	template = loader.get_template('html/error_report/index.html')

	context = RequestContext(request, {
		'apps': controller.get_apps(request),
	})

	return HttpResponse(template.render(context))

def report_page(request,report):
	if(not controller.is_logged_in(request)):
		return HttpResponseRedirect(reverse("error_report.views.login"))
	if(request.method == "POST"):
		controller.add_message(request, request.POST.get("report", ""), request.POST.get("message", ""), request.POST.get("author", ""))
		return HttpResponseRedirect(reverse("error_report.views.report_page", kwargs={'report':report}))

	report = controller.get_report(request, report)

	if(report == None):
		return HttpResponseRedirect(reverse("error_report.views.index"))

	template = loader.get_template('html/error_report/report.html')

	context = RequestContext(request, {
		'report': report,
		'message_list': controller.get_messages(request, report.hash),
	})

	return HttpResponse(template.render(context))

def get_report(request,report):
	if(request.method != "GET"):
		return HttpResponseBadRequest("Bad Request")
	else:
		report = controller.get_report(request, report)
		return HttpResponse(json.dumps({"status":"success","response":
			{
				'id': report.hash,
				'text': report.text,
				'log': report.log,
				'time': str(report.time),
				'tags': list(report.reporttag_set.values_list("tag",flat=True))
			}} if report else {"status":"failure"}),content_type="application/json")

def app(request,app_id):
	if(not controller.is_logged_in(request)):
		return HttpResponseRedirect(reverse("error_report.views.login"))
	if(request.method != "GET"):
		return HttpResponseBadRequest("Bad Request")

	page = int(request.GET.get('page',0))
	results_per_page = 20

	description = request.GET.get('description','1')
	description = (description!='0') if description else None

	messages = request.GET.get('messages','')
	messages = (messages!='0') if messages else None

	tags = request.GET.get('tags','').strip()
	tags = tags.split() if tags else []

	reports = controller.get_reports(request, app_id, offset=page * results_per_page, limit=results_per_page, has_messages=messages, has_description=description, tags=tags)

	total_pages=int(ceil(float(reports[0])/results_per_page))

	template = loader.get_template('html/error_report/app.html')

	context = RequestContext(request, {
		'app_id': app_id,
		'reports': reports[1],
		'page':page,
		'total_pages':total_pages,
		'page_loop':range(total_pages),
		'description':description,
		'has_messages':messages,
		'tags':request.GET.get('tags','').strip(),
	})

	return HttpResponse(template.render(context))

def login(request):
	if(request.method=="POST"):
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)

		if(controller.login(request, username, password)):
			return HttpResponseRedirect(reverse("error_report.views.index"))
		else:
			template = loader.get_template('html/error_report/login.html')

			context = RequestContext(request, {
													'user': request.user,
													'error': True,
													'non_subscribe_account': False,
										})

			return HttpResponse(template.render(context))
	else:
		template = loader.get_template('html/error_report/login.html')

		context = RequestContext(request, {
												'user': request.user,
												'error': False,
												'non_subscribe_account': False,
									})

		return HttpResponse(template.render(context))

def report(request,app):
	if(request.method == "GET"):
		request_dict = request.GET
	elif(request.method == "POST"):
		request_dict = request.POST
	
	ret = controller.add_report(request, request_dict.get("text", ""), request_dict.get("log", ""), request_dict.getlist("tag", []), app)
	
	return HttpResponse(json.dumps({"status":"success","response":ret} if ret else {"status":"failure"}),content_type="application/json")

def add_message(request,report):
	if(request.method != "POST"):
		return HttpResponseBadRequest("Bad Request")
	else:
		ret = controller.add_message(request, report, request.POST.get("message", ""), request.POST.get("author", ""))
		return HttpResponse(json.dumps({"status":"success"} if ret else {"status":"failure"}),content_type="application/json")

def get_messages(request,report):
	if(request.method != "GET"):
		return HttpResponseBadRequest("Bad Request")

	ret = controller.get_messages(request, report)
	return HttpResponse(json.dumps({"status":"success","response":list(ret)} if ret!=None else {"status":"failure"}),content_type="application/json")