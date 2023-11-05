FROM python:3.11

RUN apt update && apt upgrade && apt autoremove

RUN pip install --upgrade pip setuptools
RUN pip install\
	jupyter\
	tqdm\
	requests


RUN mkdir -p /root/.jupyter && touch /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py && \
 echo c.NotebookApp.open_browser = False >> /root/.jupyter/jupyter_notebook_config.py
RUN mkdir /root/.ssh && \
 echo "StrictHostKeyChecking no" >> /root/.ssh/config && \
 echo "UserKnownHostsFile /dev/null" >> /root/.ssh/config


WORKDIR /mnt
CMD jupyter notebook --allow-root --NotebookApp.token=''