# Introduction
This quick-and-dirty demo Docker composition started took inspiration from https://thenewstack.io/implementing-service-discovery-of-microservices-with-consul/

Main changes to the approach in that article:
- All three Flask apps are based on the same boilerplate code. Differences, i.e. the service name, the port, and the upstream service are passed in environment variables (`docker-compose.yml`).
- Instead of using hard coded upstream service URLs, Consul is queried for the upstream service, and the upstream service's URL is generated from the output.

# Running
- Start Docker.
- Build and start this composition:
    ```bash
    $ source bounce.docker
    ```
- Microservices' dependencies:
    - _Order_ is dependent on _Invoice_.
    - _Invoice_, in turn, is dependent on _Tax_.
- Run queries:
    ```bash
    ➤ http http://localhost:5000
    HTTP/1.0 200 OK
    Content-Length: 110
    Content-Type: text/html; charset=utf-8
    Date: Mon, 30 Nov 2020 13:51:17 GMT
    Server: Werkzeug/1.0.1 Python/3.9.0

    {"service": "Order", "version": 1.0}
    {"service": "Invoice", "version": 1.0}
    {"service": "Tax", "version": 1.0}

    kontza@über-mbp:~/W/v/consul-n-python|main⚡*
    ➤ http http://localhost:5001
    HTTP/1.0 200 OK
    Content-Length: 73
    Content-Type: text/html; charset=utf-8
    Date: Mon, 30 Nov 2020 13:51:20 GMT
    Server: Werkzeug/1.0.1 Python/3.9.0

    {"service": "Invoice", "version": 1.0}
    {"service": "Tax", "version": 1.0}


    kontza@über-mbp:~/W/v/consul-n-python|main⚡*
    ➤ http http://localhost:5002
    HTTP/1.0 200 OK
    Content-Length: 34
    Content-Type: text/html; charset=utf-8
    Date: Mon, 30 Nov 2020 13:51:23 GMT
    Server: Werkzeug/1.0.1 Python/3.9.0

    {
        "service": "Tax",
        "version": 1.0
    }
    ```