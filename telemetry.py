import os


def configure_comprehend_telemetry(service_name: str, app=None):
    token = os.getenv("COMPREHEND_SDK_TOKEN")
    if not token:
        return None

    try:
        from comprehend_telemetry import ComprehendDevSpanProcessor
        from opentelemetry import trace
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
        from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
    except ImportError:
        return None

    resource = Resource.create({
        "service.name": service_name,
        "deployment.environment": os.getenv("OTEL_ENVIRONMENT", "prod"),
    })

    span_processor = ComprehendDevSpanProcessor(
        organization="bijan-sandbox",
        token=token,
        debug=False,
    )

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(span_processor)

    current_tracer_provider = trace.get_tracer_provider()
    if current_tracer_provider.__class__.__name__ == "ProxyTracerProvider":
        trace.set_tracer_provider(tracer_provider)
        active_tracer_provider = trace.get_tracer_provider()
    else:
        active_tracer_provider = current_tracer_provider
        if hasattr(active_tracer_provider, "add_span_processor"):
            active_tracer_provider.add_span_processor(span_processor)

    if app is not None:
        FlaskInstrumentor().instrument_app(app)

    Psycopg2Instrumentor().instrument()

    return active_tracer_provider
