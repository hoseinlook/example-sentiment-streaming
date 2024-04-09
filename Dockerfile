#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
FROM registry.docker.ir/python:3.8-bullseye as build-stage

COPY requirements.txt requirements.txt
ARG PIP_CACHE_DIR=/tmp/pip-cache
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    pip install build \
 && pip wheel \
        --wheel-dir=/tmp/wheels \
        -r requirements.txt



FROM registry.docker.ir/ubuntu:focal

# Switch to user root so we can add additional jars and configuration files.
USER root

# Install java
RUN apt update -y && \
    apt upgrade -y && \
    apt install openjdk-8-jdk -y && \
    apt install tar -y && \
    apt install gpg -y && \
    apt install tzdata && \
    apt install wget -y

ENV TZ="Asia/Tehran"
# Install tini
ENV TINI_VERSION v0.19.0
RUN wget -P / https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini
RUN wget -P /  https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini.asc
RUN chmod +x /tini
RUN mv /tini /usr/bin/tini


ENV SPARK_VERSION=3.2.4 \
HADOOP_VERSION=3.2 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz



RUN mkdir /opt/spark/work-dir
RUN chown root:root -R /opt/spark
RUN chmod 777 -R /opt/spark

WORKDIR /opt/spark/work-dir


ENV SPARK_HOME /opt/spark


RUN apt install -y unzip zip

RUN chmod 777 -R $SPARK_HOME/jars


# Setup for the Prometheus JMX exporter.
# Add the Prometheus JMX exporter Java agent jar for exposing metrics sent to the JmxSink to Prometheus.
RUN wget -P /prometheus/ https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.11.0/jmx_prometheus_javaagent-0.11.0.jar
RUN chmod 777 /prometheus/jmx_prometheus_javaagent-0.11.0.jar
RUN echo "" > /tmp/java_opts.txt
RUN chmod 777 -R /tmp

RUN mkdir -p /etc/metrics/conf

RUN chmod 777 -R /tmp
RUN addgroup --gid 5000 hdfs
RUN adduser --disabled-password --gecos "hdfs,," --uid 5000 --gid 5000 --home  /home/hdfs hdfs
RUN chown hdfs:hdfs -R /opt/spark

# install wheels built in the build-stage

RUN apt-get update \
 && apt-get upgrade --yes \
 && apt-get install --yes --no-install-recommends \
	python3-pip \
        ca-certificates \
        dnsutils \
        iputils-ping \
	libkrb5-dev \
        # requirement for nbgitpuller
        git \
	vim \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
ARG PIP_CACHE_DIR=/tmp/pip-cache
RUN #apt-get install --yes --no-install-recommends build-essential
RUN pip install -U pip setuptools
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    --mount=type=cache,from=build-stage,source=/tmp/wheels,target=/tmp/wheels \
    pip install \
        --find-links=/tmp/wheels/ \
        -r /tmp/requirements.txt


WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 8080 7077 7000

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG




USER root

COPY start-spark.sh /

CMD ["/bin/bash", "/start-spark.sh"]