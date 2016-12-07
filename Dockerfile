FROM tiangolo/uwsgi-nginx-flask:flask

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Add generate_public_url configuration to Nginx
COPY nginx.conf /etc/nginx/conf.d/

# Delete all default files in /generate_public_url directory
RUN rm -rf /app/*

# Copy files to /generate_public_url directory
COPY ./uwsgi.ini /app/uwsgi.ini
COPY ./generate_public_url /app/generate_public_url
