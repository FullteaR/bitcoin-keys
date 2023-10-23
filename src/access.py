from utils import *
from tqdm.auto import tqdm
import itertools
import os 

conn = getConn()
M = conn.getblockcount()

results = []

for height in tqdm(range(1, M)):
    try:
        blockHash = getBlockHash(height)
        transactionIds = getTransactionIds(blockHash)
        for transactionId in transactionIds:
            transactionHex = getTransactionHex(transactionId)
            try:
                results += getSignAndPubkeys(transactionHex)
            except:
                pass
    except:
        pass

file_name = os.environ["RPC_HOST"]+".txt"
with open(os.path.join("/mnt",file_name), "w") as fp:
    for result in results:
        r,s = result[0]
        x,y = result[1]
        fp.write(f"{r},{s},{x},{y}\n")

