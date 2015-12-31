#!/bin/sh
cd /opt/activemq
bin/activemq producer \
  --brokerUrl $AMQ1_PORT_61616_TCP \
  --destination queue://foo.bar
