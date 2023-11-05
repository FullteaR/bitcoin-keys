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

#M = conn.getblockcount()
M = 10000

logging.info("Current Height of Bitcoin block chain is {0}".format(M))

dbpath = os.path.join("/db",chain_name+".db") 
results = leveldb.LevelDB(dbpath)

for height in tqdm(range(1, M)):
    if isin(results, height):
        continue
    result = []
    try:
        blockHash = getBlockHash(height, conn)
        transactionIds = getTransactionIds(blockHash, conn)
        for transactionId in transactionIds:
            transactionHex = getTransactionHex(transactionId, conn)
            try:
                result += getSignAndPubkeys(transactionHex)
                time.sleep(0.01)
            except Exception as ex:
                logging.error("The exception happens during getting sign and pubkeys for height {0}".format(height))
                print(ex)
        put(results, height, result)
        time.sleep(0.01)
        if height%1000==1:
            logging.info("{0} / {1} done.".format(height, M))
    except Exception as e:
        logging.error("The exception happens during calculating height {0}".format(height))
        print(e)
        

logging.info("start writing to file...")
file_name = chain_name + ".txt"
with open(os.path.join("/mnt",file_name), "w") as fp:
    for height in range(1, M):
        for result in get(results, height):
            r,s = result[0]
            x,y = result[1]
            fp.write(f"{height},{r},{s},{x},{y}\n")

