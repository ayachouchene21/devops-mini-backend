# DevOps Mini Backend

A lightweight FastAPI backend application demonstrating DevOps best practices including containerization, Kubernetes deployment, CI/CD pipelines, and observability.

## 📋 Table of Contents

- **FastAPI** - Modern, fast web framework for building APIs
- **Prometheus Metrics** - Built-in metrics endpoint for monitoring
- **OpenTelemetry Tracing** - Distributed tracing support
- **Docker** - Containerized application
- **Kubernetes** - Production-ready K8s manifests
- **CI/CD** - GitHub Actions workflows for automation
- **Testing** - Unit tests with pytest

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
The API will be available at: **http://localhost:8000**

### Access the Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc


### Build the Docker Image

docker build -t fastapi-app:latest .

### Run the Container
docker run -d -p 8000:8000 --name fastapi-app fastapi-app:latest





## Kubernetes Deployment

### Using Minikube (Local Development)

#### 1. Start Minikube

```bash
minikube start
```

#### 2. Load Local Docker Image (if not using registry)

```bash
# Point Docker to Minikube's daemon
eval $(minikube docker-env)

# Build the image inside Minikube
docker build -t fastapi-app:latest .
```

#### 3. Deploy to Kubernetes

```bash
kubectl apply -f k8s.yaml
```

#### 4. Check Deployment Status

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

#### 5. Access the Application

```bash
# Get the service URL
minikube service fastapi-service --url

# Or use port-forward
kubectl port-forward service/fastapi-service 8080:80
```

The app will be accessible at: **http://localhost:8080**

### Kubernetes Resources

| Resource | Name | Description |
|----------|------|-------------|
| Deployment | `fastapi-app` | 2 replicas of the FastAPI application |
| Service | `fastapi-service` | NodePort service exposing port 30080 |

---

## 📡 API Reference

### Base URL

```
http://localhost:8000
```

### Endpoints

#### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

---

#### Root Endpoint

```http
GET /The 
```

**Response:**
```json
{
  "message": "API is running"
}
```

---

#### Get All Items

```http
GET /items
```

**Response:**
```json
[]
```

---

#### Add an Item

```http
POST /items
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "example-item"
}
```

**Response:**
```json
{
  "message": "Item added",
  "item": {
    "name": "example-item"
  }
}
```

---

#### Prometheus Metrics

```http
GET /metrics
```



-

##  Observability

### Metrics

The application exposes Prometheus metrics at `/metrics`:

| Metric | Type | Description |
|--------|------|-------------|
| `request_count` | Counter | Total number of requests by method and endpoint |
| `request_latency_seconds` | Histogram | Request latency by endpoint |

### Logging

Structured logging is enabled with the following format:

```
2024-01-15 10:30:00 INFO method=GET path=/health status=200 duration=0.0012s
```

### Tracing

OpenTelemetry tracing is configured with console export. Each request generates spans for distributed tracing.




## CI/CD Pipeline

This project includes GitHub Actions workflows for:

- **CI Pipeline**: Runs on pull requests
  - Dast
  - Security scanning (bandit)
  - Unit tests (pytest)

- **CD Pipeline**: Runs on merge to main
  - Build Docker image
  - Push to Docker Hub
  - Deploy to Kubernetes




