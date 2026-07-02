import os


def configure_comprehend_telemetry(service_name: str, app=None):
    token = os.getenv("COMPREHEND_SDK_TOKEN")
    if not token:
        return None

    try:
        from comprehend_telemetry import ComprehendDevSpanProcessor
        from opentelemetry import trace
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
    except ImportError:
        return None

    resource = Resource.create({
        "service.name": service_name,
        "deployment.environment": os.getenv("OTEL_ENVIRONMENT", "prod"),
    })

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        ComprehendDevSpanProcessor(
            organization="bijan-sandbox",
            token=token,
            debug=False,
        )
    )

    current_tracer_provider = trace.get_tracer_provider()
    if current_tracer_provider.__class__.__name__ == "ProxyTracerProvider":
        trace.set_tracer_provider(tracer_provider)

    if app is not None:
        FlaskInstrumentor().instrument_app(app)

    return tracer_provider
