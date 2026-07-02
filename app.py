from math import factorial
from flask import Flask, request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

# Set up OpenTelemetry resource attributes for the service
resource = Resource.create({
	ResourceAttributes.SERVICE_NAME: "demo-service",
	ResourceAttributes.SERVICE_VERSION: "0.2.1"
})
# Set up OpenTelemetry tracing and initialize the tracer provider with the resource attributes
tracer_provider = TracerProvider(resource=resource)

# Add a BatchSpanProcessor to the tracer provider, which will export spans to the OTLP exporter
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317"))

# Add the processor to the tracer provider
tracer_provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(tracer_provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("demo_tracer")

# Create a Flask application
app = Flask(__name__)

# Define a route for the Flask applicaton
@app.route("/home")

def demo():
	# Start a new span named "demo_span" using the tracer
	with tracer.start_as_current_span("demo_span") as parent:
		# Set various semanticattributes for the parent span based on the incoming HTTP request
		parent.set_attribute(SpanAttributes.HTTP_METHOD, request.method)
		parent.set_attribute(SpanAttributes.HTTP_ROUTE, request.path)
		parent.set_attribute(SpanAttributes.HTTP_URL, request.url)
		parent.set_attribute(SpanAttributes.SERVER_ADDRESS, request.environ.get("SERVER_NAME"))
		parent.set_attribute(SpanAttributes.SERVER_PORT, request.environ.get("SERVER_PORT"))
		parent.set_attribute(SpanAttributes.CLIENT_ADDRESS, request.remote_addr)
		parent.set_attribute(SpanAttributes.CLIENT_PORT, request.environ.get("REMOTE_PORT"))
		
		with tracer.start_as_current_span("child_span") as child:
			result = factorial(5)
			# Set attributes for the child span, custom:input value and the result, semantic: status code
			child.set_attribute("factorial_input", 5)
			child.set_attribute("factorial_result", result)
			child.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)

			return str(f"The factorial of 5 is: {result}")
	
