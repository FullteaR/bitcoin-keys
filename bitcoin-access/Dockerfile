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


WORKDIR /mnt
RUN pip install --upgrade pip
RUN pip install ecdsa bitcoin leveldb python-bitcoinrpc bitcoinlib tqdm retry
RUN pip install git+https://github.com/FullteaR/LevelDictionary
CMD python /mnt/access.py && sleep infinity
