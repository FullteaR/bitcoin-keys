from utils import *
from tqdm.auto import tqdm
import itertools
import os 
import time
import logging

logging.info("waiting for 30 seconds to start...")
time.sleep(30)
logging.info("program start")

conn = getConn()
M = conn.getblockcount()

logging.info("Current Height of Bitcoin block chain is {0}".format(M))

results = {}

for height in tqdm(range(1, M)):
    results[height] = []
    try:
        blockHash = getBlockHash(height, conn)
        transactionIds = getTransactionIds(blockHash, conn)
        for transactionId in transactionIds:
            transactionHex = getTransactionHex(transactionId, conn)
            try:
                results[height] += getSignAndPubkeys(transactionHex)
                time.sleep(0.01)
            except Exception as ex:
                logging.error("The exception happens during getting sign and pubkeys for height {0}".format(height))
                print(ex)
                pass
        time.sleep(0.01)
        logging.info("{0} / {1} done.".format(height, M))
    except Exception as e:
        logging.error("The exception happens during calculating height {0}".format(height))
        print(e)
        

logging.info("start writing to file...")
file_name = os.environ["RPC_HOST"]+".txt"
with open(os.path.join("/mnt",file_name), "w") as fp:
    for height in range(1, M):
        for result in results[height]:
            r,s = result[0]
            x,y = result[1]
            fp.write(f"{height},{r},{s},{x},{y}\n")

