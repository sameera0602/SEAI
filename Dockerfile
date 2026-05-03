FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
# Note: we are installing Flask and google-generativeai on top of existing requirements
COPY requirements ./
RUN pip install --no-cache-dir -r requirements || echo "Requirements failed, installing bare minimum"
RUN pip install --no-cache-dir Flask werkzeug google-generativeai

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
