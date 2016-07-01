from django.shortcuts import render
from django.http import HttpResponse
from django_opentracing import DjangoTracer
from django.conf import settings
import lightstep.tracer

tracer = DjangoTracer(lightstep.tracer.init_tracer(group_name="django server", access_token="{your_lightstep_token}"))
# Create your views here.

def server_index(request):
	return HttpResponse("Hello, world. You're at the server index.")

@tracer.trace()
def server_simple(request):
	return HttpResponse("This is a simple traced request.")

@tracer.trace()
def server_log(request):
	span = tracer.get_span(request)
	span.log_event("hello world")
	return HttpResponse("Something was logged")

@tracer.trace()
def server_child_span(request):
	span = tracer.get_span(request)
	child_span = tracer.tracer.start_span("child span", span)
	child_span.finish()
	return HttpResponse("A child span was created")