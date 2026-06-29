from math import factorial
from flask import Flask

# Create a Flask application
app = Flask(__name__)

# Define a route for the Flask applicaton
@app.route("/home")

def demo():
	result = factorial(5)
	return str(f"The factorial of 5 is: {result}")
