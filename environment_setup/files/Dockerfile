FROM conda/miniconda3

RUN apt-get update

RUN apt-get install -y gcc

RUN apt-get install -y icu-devtools

# Uncomment to run R
# RUN conda install -c r r-essentials

COPY requirements.txt  /setup/

RUN pip install --upgrade -r /setup/requirements.txt
