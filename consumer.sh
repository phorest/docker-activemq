#!/bin/sh
cd /opt/activemq
bin/activemq consumer \
  --brokerUrl $AMQ2_PORT_61616_TCP \
  --destination queue://foo.bar
