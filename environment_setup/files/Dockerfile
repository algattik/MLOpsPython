FROM conda/miniconda3

RUN apt-get update

RUN apt-get install -y gcc

RUN conda install -c r r-essentials

COPY environment_setup/requirements.txt  /setup/

RUN pip install --upgrade -r /setup/requirements.txt
