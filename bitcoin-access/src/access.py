from utils import *
import json
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
db = leveldb.LevelDB(dbpath, create_if_missing=True)

for height in tqdm(range(1, M)):
    if isin(db, height):
        continue
    try:
        result = extractInfosFromHeight(height, conn)
        put(db, height, result)
        if height%1000==1:
            logging.info("{0} / {1} done.".format(height, M))
    except Exception as e:
        print(e)
        logging.error("Exception happens during calculating")
        

logging.info("start writing to file...")
file_name = chain_name + ".json"
results = []
for height in range(1, M):
    for result in get(db, height):
        for txid in result:
            r,s = result[txid][0]
            x,y = result[txid][1]
            d = {
                "height":height,
                "tx":txid,
                "r":r,
                "s":s,
                "x":x,
                "y":y
            }
        results.append(d)

with open(os.path.join("/out",file_name), "w") as fp:
    json.dump(results, fp, indent=4)

