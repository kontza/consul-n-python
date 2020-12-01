from flask import Flask
import consul
import json
import logging
import requests
import os
import time

app = Flask(__name__)
logger_name = os.environ.get("SERVICE_NAME")
if logger_name is None:
    logger_name = "root"
logger = logging.getLogger(logger_name)


@app.route("/health")
def get_health():
    return json.dumps({"status": "UP"})


@app.route("/")
def get_handler():
    service_name = os.environ.get("SERVICE_NAME")
    logger.warning(f"Service name = {service_name}")
    payload = json.dumps({"service": service_name, "version": 1.0})
    upstream_service = os.environ.get("UPSTREAM_SERVICE")
    if upstream_service is not None:
        cons = consul.Consul(host="consul", port=8500)
        (index, found_services) = cons.catalog.service(upstream_service)
        logger.warning(f"Found services = {found_services}")
        response = requests.get(f"http://{found_services[0]['ServiceAddress']}:{found_services[0]['ServicePort']}")
        payload = f"{payload}\n{response.text}"
    return payload


def register(client):
    port = os.environ.get("SERVICE_PORT")
    service_name = os.environ.get("SERVICE_NAME").lower()
    check_http = consul.Check.http(f"http://{service_name}:{port}/health", interval="5s")
    while True:
        try:
            client.agent.service.register(
                service_name, address=service_name, port=int(port), check=check_http, tags=[service_name]
            )
            break
        except (ConnectionError, consul.ConsulException) as e:
            logger.error(f"Consul host is down, reconnecting after 500ms...: reason = {e}")
            time.sleep(5)


if __name__ == "__main__":
    port = os.environ.get("SERVICE_PORT")
    logger.warning(f"Listening for port {port}")
    cons = consul.Consul(host="consul", port=8500)
    logger.warning(f"Consul client = {cons}")
    register(cons)
    app.run(debug=True, host="0.0.0.0", port=port)
