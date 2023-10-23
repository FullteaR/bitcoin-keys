from utils import *
from tqdm.auto import tqdm
import itertools
from multiprocessing import Pool, cpu_count

retval = {}
M = 2426743	
#M = 20000

def wrap(height):
    conn = get_conn()
    hashes = get_hashes(height, conn)
    retval = {}
    for tx_hash in hashes:
        try:
            for key, sig in get_keys_and_sigs(tx_hash, conn):
                tmp = retval.get(key, set())
                tmp.add(sig)
                retval[key] = tmp
        except Exception as e:
            pass
    return retval

if __name__ == "__main__":
    with Pool(48) as p:
        imap = p.imap(wrap, range(1,M))
        calcs = list(tqdm(imap, total=M-1))
    for calc in calcs:
        for k, v in calc.items():
            tmp = retval.get(k, set())
            tmp = tmp.union(v)
            retval[k] = tmp


for key in retval.keys():
    for sig1, sig2 in itertools.combinations(retval[key], 2):
        r1, s1, h1 = sig1
        r2, s2, h2 = sig2
        if h1==h2:
            continue
        h1 = int(h1, 16)
        h2 = int(h2, 16)
        if (h1-h2)%(s1-s2)==0:
            k = (h1-h2)//(s1-s2)
            d = ((s1*k)-h1)//r1
            print(d,k)
        

