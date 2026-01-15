from fastapi import FastAPI
from pydantic import BaseModel
import logging
import time
from fastapi import Request
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


app = FastAPI(title="DevOps Mini Backend")
# setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

logger = logging.getLogger("app")

# setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

FastAPIInstrumentor.instrument_app(app)


items = []
REQUEST_COUNT = Counter(
    "request_count", "Total number of requests", ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency", ["endpoint"]
)


@app.middleware("http")
async def metrics_and_logs(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    endpoint = request.url.path
    REQUEST_COUNT.labels(request.method, endpoint).inc()
    REQUEST_LATENCY.labels(endpoint).observe(duration)

    logger.info(
        f"method={request.method} path={endpoint} "
        f"status={response.status_code} duration={duration:.4f}s"
    )
    return response


class Item(BaseModel):
    name: str

# Request API (get and post items )


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def get_items():
    return items


@app.post("/items")
def add_item(item: Item):
    items.append(item)
    return {"message": "Item added", "item": item}


# add metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
