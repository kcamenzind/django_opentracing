## Example

This is an example of a Django site with tracing implemented using the django_opentracing package. To run the example, make sure you've installed packages `lightstep` and `opentracing`. If you have a lightstep token and would like to view the created spans, then go into `example_site/settings.py` and change the OpenTracing tracer token. If you would like to use a different OpenTracing tracer implementation, then you may also replace the lightstep tracer with the tracer of your choice. 

Navigate to this directory and then run:

```
> python manage.py runserver 8000
```

Open in your browser `localhost:8000/client`.

### Trace a Request and Response

Navigate to `/client/simple` to send a request to the server. There will be a span created for both the client request and the server response from the tracing decorators, `@tracer.trace()`.

### Log a Span

Navigate to `/client/log` to send a request to the server and log something to the server span. There will be a span created for both the client request and server response from the tracing decorators. The server views.py handler will manually log the server span with the message 'Hello, world!'.

### Create a Child Span manually

Navigate to `/client/childspan` to send a request to the server and create a child span for the server. There will be span created for both the client request and server response from the tracing decorators. The server views.py handler will manually create and finish a child span for the server span. 

### Don't Trace a Request

Navigating to `/client` will not produce any traces because there is no `@trace.trace()` decorator. However, if `settings.OPENTRACING['TRACE_ALL_REQUESTS'] == True`, then every request (including this one) will be traced, regardless of whether or not it has a tracing decorator.