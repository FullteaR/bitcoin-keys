from utils import *
from tqdm.auto import tqdm
import itertools
import os 
import time


time.sleep(30)

conn = getConn()
M = conn.getblockcount()

results = []

for height in tqdm(range(1, M)):
    try:
        blockHash = getBlockHash(height, conn)
        transactionIds = getTransactionIds(blockHash, conn)
        for transactionId in transactionIds:
            transactionHex = getTransactionHex(transactionId, conn)
            try:
                results += getSignAndPubkeys(transactionHex)
            except:
                pass
        time.sleep(0.1)
    except Exception as e:
        print(e)
        

file_name = os.environ["RPC_HOST"]+".txt"
with open(os.path.join("/mnt",file_name), "w") as fp:
    for result in results:
        r,s = result[0]
        x,y = result[1]
        fp.write(f"{r},{s},{x},{y}\n")

