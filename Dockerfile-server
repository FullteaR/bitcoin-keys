FROM ubuntu:22.04

RUN apt update && apt upgrade -y && apt autoremove
RUN apt install -y build-essential libtool autotools-dev automake pkg-config bsdmainutils python3 libevent-dev libboost-dev libsqlite3-dev git libminiupnpc-dev libnatpmp-dev libzmq3-dev systemtap-sdt-dev
RUN git clone https://github.com/bitcoin/bitcoin.git /bitcoin

WORKDIR /bitcoin
RUN ./autogen.sh
RUN ./configure
RUN make -j"$(nproc)" && make install
ENV PATH $PATH:/bitcoin


RUN mkdir -p /root/.bitcoin
ADD bitcoin.conf /root/.bitcoin/bitcoin.conf
WORKDIR /mnt
CMD bitcoind

