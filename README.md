# docker-activemq
Docker image for Apache ActiveMQ (AMQ) (v5.13.0).

---

**NOTE:** Binary distribution is downloaded from rediris mirror located in Spain.

Launch the image:

```bash
docker run \
  -d \
  -p 61616:61616 \
  -p 8161:8161 \
  javierprovecho/docker-activemq
```

---

## Example running a cluster

Launch `amq1`:

```bash
docker run \
  -it \
  --rm \
  --name amq1 \
  javierprovecho/docker-activemq
```

Launch `amq2` linked to `amq1`:

```bash
docker run \
  -it \
  --rm \
  --name amq2 \
  --link amq1:amq1 \
  javierprovecho/docker-activemq
```

Launch `consumer` against `amq2`:

```bash
docker run \
  -it \
  --rm \
  --link amq2:amq2 \
  --name consumer \
  javierprovecho/docker-activemq \
  consumer.sh
```

Launch `producer` against `amq1`:

```bash
docker run \
  -it \
  --rm \
  --link amq1:amq1 \
  --name producer \
  javierprovecho/docker-activemq \
  producer.sh
```

You can even launch `amq3` linked both to `amq1` and `amq2`:

```bash
docker run \
  -it \
  --rm \
  --name amq3 \
  --link amq1:amq1 \
  --link amq2:amq2 \
  javierprovecho/docker-activemq
```

By default `cluster.py` search for Docker links and modify `activemq.xml`.
It adds new instances with this template:

```xml
<networkConnectors>
  <networkConnector
    uri="static:($AMQ1_PORT_61616_TCP, $AMQ2_PORT_61616_TCP, $AMQN_PORT_61616_TCP)"
    duplex="true"
    decreaseNetworkConsumerPriority="false"
    networkTTL="2"
    dynamicOnly="true">
  </networkConnector>
</networkConnectors>
```
