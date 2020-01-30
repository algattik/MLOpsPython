FROM conda/miniconda3

LABEL org.label-schema.vendor = "Microsoft" \
      org.label-schema.url = "https://hub.docker.com/r/microsoft/mlopspython" \
      org.label-schema.vcs-url = "https://github.com/microsoft/MLOpsPython"

COPY diabetes_regression/ci_dependencies.yml /setup/

RUN conda env create -f /setup/ci_dependencies.yml

# activate environment
ENV PATH /usr/local/envs/mlopspython_ci/bin:$PATH
RUN /bin/bash -c "source activate mlopspython_ci"

# Install Azure CLI ML extension
RUN az extension add -n azure-cli-ml
