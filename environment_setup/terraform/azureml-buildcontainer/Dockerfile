FROM conda/miniconda3

ARG SPARK_VERSION=2.4.4
ARG HADOOP_VERSION=2.7

LABEL org.label-schema.vendor = "Microsoft" \
      org.label-schema.url = "https://hub.docker.com/r/microsoft/mlopspython" \
      org.label-schema.vcs-url = "https://github.com/microsoft/MLOpsPython"

RUN apt-get update

# Install PySpark. You can delete this block unless you will be running PySpark
# unit tests as part of the build.
WORKDIR /
RUN apt-get install -y wget openjdk-8-jdk
RUN wget -q https://www-eu.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz
RUN tar -zxf spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz
RUN rm spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz
ENV SPARK_HOME /spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION

# Install R. You can delete this block unless you will be running R as part
# of the build.
RUN conda install -c r r-essentials

# Install Python dependencies.
RUN apt-get install -y gcc
COPY *.txt /setup/
RUN pip install --upgrade -r /setup/requirements.txt

CMD ["python"]
