FROM docker.phorest.com/java:8

ENV container docker
RUN yum -y update && \
    yum -y install systemd && \
    yum install -y which unzip openssh-server sudo openssh-clients && \
    yum -y autoremove && \
    yum clean all

# enable no pass and speed up authentication
RUN sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords yes/;s/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config

# enabling sudo group
RUN echo '%wheel ALL=(ALL) ALL' >> /etc/sudoers
# enabling sudo over ssh
RUN sed -i 's/.*requiretty$/#Defaults requiretty/' /etc/sudoers

ENV INSTALL4J_JAVA_HOME $JAVA_HOME/jre

# command line goodies
RUN echo "alias ll='ls -l --color=auto'" >> /etc/profile
RUN echo "alias grep='grep --color=auto'" >> /etc/profile

WORKDIR /home/activemq

ENV ACTIVE_MQ_VERSION 5.14.0
ENV ACTIVE_MQ_PORT 61616
ENV ACTIVE_MQ_CONSOLE_PORT 8161
ENV ACTIVE_MQ_CONSOLE_PATH "/admin"
RUN curl  --output apache-mq.zip http://central.maven.org/maven2/org/apache/activemq/apache-activemq/$ACTIVE_MQ_VERSION/apache-activemq-$ACTIVE_MQ_VERSION-bin.zip && \
    unzip apache-mq.zip && \
    rm apache-mq.zip

WORKDIR /home/activemq/apache-activemq-$ACTIVE_MQ_VERSION/bin

VOLUME /home/activemq/apache-activemq-$ACTIVE_MQ_VERSION/data

RUN chmod u+x ./activemq

WORKDIR /home/activemq/apache-activemq-$ACTIVE_MQ_VERSION/

RUN echo >> data/activemq.log

COPY run.sh run.sh
COPY cluster.py cluster.py

EXPOSE 22 1099 61616 8161 5672 61613 1883 61614

ENTRYPOINT ["/bin/sh"]
CMD ["run.sh"]
