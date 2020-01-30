FROM conda/miniconda3

LABEL org.label-schema.vendor = "Microsoft" \
      org.label-schema.url = "https://hub.docker.com/r/microsoft/mlopspython" \
      org.label-schema.vcs-url = "https://github.com/microsoft/MLOpsPython"

# Utilities for package installation
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    gcc

# Packages for running R
RUN conda install -c r r-essentials

# Install Python modules
COPY environment_setup/requirements.txt  /setup/
RUN pip install --upgrade -r /setup/requirements.txt
