from utils import *
import json
import os 
import time
import logging
from tqdm.auto import tqdm
from leveldictionary import LevelDict

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
db = LevelDict(dbpath)

for height in tqdm(range(1, M)):
    if height in db:
        continue
    try:
        result = extractInfosFromHeight(height, conn)
        db[height] = result
        if height%1000==1:
            logging.info("{0} / {1} done.".format(height, M))
    except Exception as e:
        logging.error(e)
        logging.error("Exception happens during calculating")

