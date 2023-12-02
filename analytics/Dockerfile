FROM python:3.11

RUN apt update && apt upgrade -y && apt install -y\
	libsnappy-dev\
	wget\
	build-essential\
	git\
	cmake\
	&& apt autoremove -y



RUN git clone --recurse-submodules --depth 1 https://github.com/google/leveldb.git /leveldb
RUN mkdir -p /leveldb/build
WORKDIR /leveldb/build
RUN cmake -DCMAKE_BUILD_TYPE=Release .. && cmake --build .

WORKDIR /
RUN pip install --upgrade pip setuptools
RUN pip install\
	jupyter\
	tqdm\
	requests\
	bitcoin\
	python-bitcoinrpc\
	ecdsa\
	base58\
	bitcoinlib\
	leveldb

RUN pip install git+https://github.com/FullteaR/LevelDictionary

RUN mkdir -p /root/.jupyter && touch /root/.jupyter/jupyter_notebook_config.py
RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py && \
 echo c.NotebookApp.open_browser = False >> /root/.jupyter/jupyter_notebook_config.py
RUN mkdir /root/.ssh && \
 echo "StrictHostKeyChecking no" >> /root/.ssh/config && \
 echo "UserKnownHostsFile /dev/null" >> /root/.ssh/config


WORKDIR /mnt
CMD jupyter notebook --allow-root --NotebookApp.token=''
