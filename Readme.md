FastAPI server with an endpoint that accepts a POST request containing a Base64 encoded image.

---
API Endpoint

URL: /process-image

Method: POST

Payload: {"image": "Base64EncodedString"}

Response: {"message": "accepted"}

---
Question 1: The server should accept multiple requests (simultaneously) by spinning worker nodes

To handle multiple simultaneous requests, we must address Python's Global Interpreter Lock (GIL). A standard Python process can only utilize one CPU core at a time. To achieve true concurrency and utilize multiple CPU cores, we need to spin up multiple worker processes.

Solution: Gunicorn with Uvicorn Workers
```py
# Install dependencies
pip install gunicorn uvicorn fastapi pydantic

# Run the server with 4 worker nodes
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

While Uvicorn handles requests asynchronously, if the Base64 image decoding or any subsequent processing (like saving to disk or running ML inference) is CPU-intensive, it will block the worker node. For heavy processing, it is best practice to immediately offload the image to a message queue (like Celery or RabbitMQ) or a background task and return the "accepted" response immediately.

---
Question 2: How to spin up multiple instances of the same server?

Step 1: Containerization
Step 2: Orchestration & Scaling 
- Once containerized, you can spin up multiple instances using one of the following methods:
  -  Docker Compose `docker-compose up --scale app=4`
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    deploy:
      replicas: 4  # Spins up 4 instances of the server
    environment:
      - PORT=8000
  
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
```

   - Kubernetes `deployment.yaml`
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment
spec:
  replicas: 4  # Spins up 4 instances
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: your-docker-image:latest
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: LoadBalancer
  selector:
    app: fastapi
  ports:
    - port: 80
      targetPort: 8000
```