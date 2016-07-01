from django.conf import settings 
import opentracing
import sys

class DjangoTracer(object):
	'''
	@param tracer the OpenTracing tracer to be used
	to trace requests using this DjangoTracer
	'''
	def __init__(self, tracer):
		self.tracer = tracer
		self.current_spans = {}

	def get_span(self, request): 
		'''
		@param request 
		Returns the span tracing this request
		'''
		return self.current_spans.get(request, None)

	def inject_as_headers(self, span, request):
		'''
		@param span
		@param request
		Injects the span as headers into the request so that 
		the trace can be continued across the wire.
		'''
		text_carrier = {}
		self.tracer.inject(span, opentracing.Format.TEXT_MAP, text_carrier)
		for k, v in text_carrier.iteritems():
			request.add_header(k,v)

	def trace(self, *attributes):
		'''
		Function decorator that traces functions
		NOTE: Must be placed after the @app.route decorator

		@param attributes any number of flask.Request attributes
		(strings) to be set as tags on the created span
		'''
		def decorator(view_func):
			def wrapper(request):
				operation_name = view_func.__name__
				headers = {}
				for k,v in request.META.iteritems():
					k = k.lower().replace('_','-')
					if k.startswith('http-'):
						k = k[5:]
					headers[k] = v				
				span = None

				try:
					span = self.tracer.join(operation_name, opentracing.Format.TEXT_MAP, headers)
				except:
					span = self.tracer.start_span(operation_name)
				self.current_spans[request] = span
				for attr in attributes:
					if hasattr(request, attr):
						payload = str(getattr(request, attr))
						if payload is not "":
							span.set_tag(attr, payload)
				
				r = view_func(request)

				span.finish()
				self.current_spans.pop(request)
				return r
			return wrapper
		return decorator