from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from django_opentracing import trace
import opentracing

import urllib2

tracer = settings.TRACER
# Create your views here.

def client_index(request):
	return HttpResponse("Client index page")

@trace
def client_simple(request):
	url = "http://localhost:8000/server/simple"
	new_request = urllib2.Request(url)
	current_span = tracer.get_span(request)
	tracer.inject_as_headers(current_span, new_request)
	try:
		response = urllib2.urlopen(new_request)
		return HttpResponse("Made a simple request")
	except urllib2.URLError as e:  
		return HttpResponse("Error: " + str(e))

@trace
def client_child_span(request):
	url = "http://localhost:8000/server/childspan"
	new_request = urllib2.Request(url)
	current_span = tracer.get_span(request)
	tracer.inject_as_headers(current_span, new_request)
	try:
		response = urllib2.urlopen(new_request)
		return HttpResponse("Sent a request that should produce an additional child span")
	except urllib2.URLError as e:  
		return HttpResponse("Error: " + str(e))

@trace
def client_log(request):
	url = "http://localhost:8000/server/log"
	new_request = urllib2.Request(url)
	current_span = tracer.get_span(request)
	tracer.inject_as_headers(current_span, new_request)
	try:
		response = urllib2.urlopen(new_request)
		return HttpResponse("Sent a request to log")
	except urllib2.URLError as e:  
		return HttpResponse("Error: " + str(e))

