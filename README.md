# Introduction
This quick-and-dirty demo Docker composition started took inspiration from https://thenewstack.io/implementing-service-discovery-of-microservices-with-consul/

Main changes to the approach in that article:
- All three Flask apps are based on the same boilerplate code. Differences, i.e. the service name, the port, and the upstream service are passed in environment variables (`docker-compose.yml`).
- Instead of using hard coded upstream service URLs, Consul is queried for the upstream service, and the upstream service's URL is generated from the output.