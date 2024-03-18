# Stage 1: Build Flask app
FROM python:3.11 AS flask-builder

WORKDIR /app

COPY flask_app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
ENV PATH="/root/.local/bin:${PATH}"
COPY flask_app .

# Stage 2: Build Streamlit app
FROM python:3.11 AS streamlit-builder

WORKDIR /app

COPY streamlit_app/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY streamlit_app .

# Stage 3: Final image
FROM python:3.11

# Install nginx for reverse proxy
RUN apt-get update && apt-get install -y nginx

# Remove default nginx site
RUN rm /etc/nginx/sites-enabled/default

# Copy nginx configuration
COPY nginx.conf /etc/nginx/sites-enabled/

# Copy Flask app from stage 1
COPY --from=flask-builder /app /flask_app

# Copy Streamlit app from stage 2
COPY --from=streamlit-builder /app /streamlit_app

# Expose ports
EXPOSE 5000 8501

# Start nginx and Flask app
CMD service nginx start && streamlit run /streamlit_app/app.py & python /flask_app/app.py
