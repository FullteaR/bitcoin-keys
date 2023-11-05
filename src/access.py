from utils import *
import itertools
import os 
import time
import logging
from tqdm.auto import tqdm
from dbutils import *
import leveldb

logging.basicConfig(level=logging.INFO)

logging.info("waiting for 30 seconds to start...")
time.sleep(30)
logging.info("program start")

conn = getConn()
chain_name = "bitcoin-" + conn.getblockchaininfo()["chain"]
logging.info("Running on chain {0}".format(chain_name))

M = conn.getblockcount()

logging.info("Current Height of Bitcoin block chain is {0}".format(M))

dbpath = os.path.join("/db",chain_name+".db") 
results = leveldb.LevelDB(dbpath, create_if_missing=True)

for height in tqdm(range(1, M)):
    if isin(results, height):
        continue
    try:
        result = extractInfosFromHeight(height, conn)
        put(results, height, result)
        if height%1000==1:
            logging.info("{0} / {1} done.".format(height, M))
    except:
        logging.error("Exception happens during calculating")
        

logging.info("start writing to file...")
file_name = chain_name + ".txt"
with open(os.path.join("/mnt",file_name), "w") as fp:
    for height in range(1, M):
        for result in get(results, height):
            r,s = result[0]
            x,y = result[1]
            fp.write(f"{height},{r},{s},{x},{y}\n")

