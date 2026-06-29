from math import factorial
from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Set up OpenTelemetry tracing and initialize the tracer provider
tracer_provider = TracerProvider()

# Add a BatchSpanProcessor to the tracer provider, which will export spans to the console using the ConsoleSpanExporter
processor = BatchSpanProcessor(ConsoleSpanExporter())

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
	with tracer.start_as_current_span("demo_span"):
		result = factorial(5)
		with tracer.start_as_current_span("child_span"):
			pass  # This is a placeholder for any additional logic you want to include in the child span
		return str(f"The factorial of 5 is: {result}")
	
