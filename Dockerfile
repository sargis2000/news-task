# Base image
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Copy project files to container
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt


# Run migrations
RUN python manage.py migrate

# Create superuser
RUN echo "from django.contrib.auth.models import User; \
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')" \
    | python manage.py shell


# Collect staic files
RUN python manage.py collectstatic

# Expose port 8000
EXPOSE 8000

# Start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
