# Petstore Catalog

## Telemetry setup

This service exports traces to comprehend.dev through the OpenTelemetry SDK when the COMPREHEND_SDK_TOKEN environment variable is present.

### Required environment variables

```powershell
$env:COMPREHEND_SDK_TOKEN="<your-comprehend-token>"
$env:OTEL_ENVIRONMENT="dev"
```

### Runtime behavior

The catalog service initializes Flask and PostgreSQL instrumentation automatically when the token is available. This keeps secrets out of source control and allows traces to be sent at runtime.
