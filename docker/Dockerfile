# This image is based on:
# * Image infrahelpers/dpp:jdk8-python3.9.16 on Docker Hub
# * Generated with the following Dockerfile: https://github.com/data-engineering-helpers/dpp-images/blob/main/corretto-emr-dbs-universal-pyspark/Dockerfile
#
# The base image is an environment with two Python versions: one for Databricks, and one for EMR.
#
# This Dockerfile simply installs the project package in both Python environments.
FROM infrahelpers/dpp:jdk8-python3.11-de0cc99

LABEL authors "Nicolas Gibaud <nicolas.gibaud.partner@decathlon.com>"

# Arguments
ARG PACKAGE_VERSION
ARG INDEX_URL
ARG PACKAGE_NAME="spark-training-workshop-pyspark"

# Authenticate with AWS CodeArtifact
ADD .netrc /root/.netrc
RUN chmod 600 /root/.netrc

# Install project package in newly installed system Python - for AWS EMR
RUN python3 -mpip install --no-cache --upgrade pip && \
    python3 -mpip install --no-cache --extra-index-url ${INDEX_URL} ${PACKAGE_NAME}==${PACKAGE_VERSION}

# Install project package in newly created Python virtual env - for Databricks
RUN /databricks/python3/bin/python3 -mpip install --no-cache --upgrade pip && \
    /databricks/python3/bin/python3 -mpip install --no-cache --extra-index-url ${INDEX_URL} ${PACKAGE_NAME}==${PACKAGE_VERSION}


