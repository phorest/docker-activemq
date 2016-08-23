#!/usr/bin/python
import os
import xml.etree.ElementTree as ET

ET.register_namespace('', 'http://www.springframework.org/schema/beans')
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

activeMqVersion = os.environ['ACTIVE_MQ_VERSION']
configFile = '/home/activemq/apache-activemq-{}/conf/activemq.xml'.re
tree = ET.parse(configFile)
root = tree.getroot()

broker = root.find('{http://activemq.apache.org/schema/core}broker')
broker.set('xmlns', 'http://activemq.apache.org/schema/core')

shutdownHooks = broker.find('{http://activemq.apache.org/schema/core}shutdownHooks')

bean = shutdownHooks.find('{http://www.springframework.org/schema/beans}bean')

bean.set('xmlns', 'http://www.springframework.org/schema/beans')

nodes = []
for key in os.environ.keys():
    if key.endswith('_PORT_61616_TCP'):
        nodes.append(os.environ[key])
if len(nodes) > 0:
    networkConnectors = ET.SubElement(broker, 'networkConnectors')
    for node in nodes:
        networkConnector = ET.SubElement(networkConnectors, 'networkConnector')
        networkConnector.set('name', os.environ['HOSTNAME'])
        networkConnector.set('uri', 'static:(%s)' % node)
        networkConnector.set('duplex', 'true')
        networkConnector.set('decreaseNetworkConsumerPriority', 'false')
        networkConnector.set('networkTTL', '5')
        networkConnector.set('dynamicOnly', 'true')

tree.write(configFile)
