#!/usr/bin/python
import os
import xml.etree.ElementTree as ET

ET.register_namespace('', 'http://www.springframework.org/schema/beans')
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

activeMqVersion = os.environ['ACTIVE_MQ_VERSION']
configFile = '/home/activemq/apache-activemq-{}/conf/activemq.xml'.format(activeMqVersion)
configTree = ET.parse(configFile)
configRoot = configTree.getroot()

broker = configRoot.find('{http://activemq.apache.org/schema/core}broker')
broker.set('xmlns', 'http://activemq.apache.org/schema/core')

shutdownHooks = broker.find('{http://activemq.apache.org/schema/core}shutdownHooks')

bean = shutdownHooks.find('{http://www.springframework.org/schema/beans}bean')

bean.set('xmlns', 'http://www.springframework.org/schema/beans')


transportConnectors = broker.find('{http://activemq.apache.org/schema/core}transportConnectors')

for transportConnector in transportConnectors:
    if transportConnector.get('name') == 'openwire':
        activeMqPort = os.environ['ACTIVE_MQ_PORT']
        transportConnector.set('uri', 'tcp://0.0.0.0:{}?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600'.format(activeMqPort))

nodes = []
for key in os.environ.keys():
    if key.endswith('CLUSTER_WITH'):
        print "Clustering with node: " + os.environ[key]
        nodes.append(os.environ[key])
if len(nodes) > 0:
    networkConnectors = ET.SubElement(broker, 'networkConnectors')
    for node in nodes:
        networkConnector = ET.SubElement(networkConnectors, 'networkConnector')
        networkConnector.set('uri', 'static:(%s)' % node)
        networkConnector.set('duplex', 'true')
        networkConnector.set('decreaseNetworkConsumerPriority', 'false')
        networkConnector.set('networkTTL', '5')
        networkConnector.set('dynamicOnly', 'true')

configTree.write(configFile)

webConsoleFile = '/home/activemq/apache-activemq-{}/conf/jetty.xml'.format(activeMqVersion)
webConsoleTree = ET.parse(webConsoleFile)
webConsoleBeans = webConsoleTree.getroot()

for webConsoleBean in webConsoleBeans:
    if webConsoleBean.get('id') == 'jettyPort':
        for property in webConsoleBean:
            if property.get('name') == 'port':
                activeMqConsolePort = os.environ['ACTIVE_MQ_CONSOLE_PORT']
                property.set('value', activeMqConsolePort)

webConsoleTree.write(webConsoleFile)
