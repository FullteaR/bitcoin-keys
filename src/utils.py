import os
from bitcoinrpc.authproxy import AuthServiceProxy
import bitcoin
from binascii import unhexlify
from ecdsa import VerifyingKey, SECP256k1
import logging
from retry import retry

def getConn():
    rpc_user = "frt"
    rpc_password = "pass"
    rpc_host = os.environ["RPC_HOST"]
    rpc_port = os.environ["RPC_PORT"]

    rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
    logging.info("connection ready: {0}".format(rpc_url))
    return AuthServiceProxy(rpc_url)


def getBlockHash(height, conn):
    return conn.getblockhash(height)


def getTransactionIds(blockHash, conn):
    return conn.getblock(blockHash)["tx"]


def getTransactionHex(transactionId, conn):
    return conn.getrawtransaction(transactionId)


def getSignAndPubkeys(transactionHex):
    tx = bitcoin.deserialize(transactionHex)
    results = []
    for in_, out_ in zip(tx["ins"], tx["outs"]):
        script_sig = in_["script"]
        if out_["script"].startswith('76a914') and out_["script"].endswith('88ac'): #P2PKH
            logging.debug("P2PKH key found. script:{0}".format(script_sig))
            script_sig = unhexlify(script_sig)
            sign_len = int(script_sig[0])
            logging.debug("sign len: {0}".format(sign_len))
            sign = script_sig[1:sign_len+1]
            logging.debug("sign: {0}".format(sign))
            pubkey_len = int(script_sig[sign_len+1])
            logging.debug("pubkey len: {0}".format(pubkey_len))
            pubkey = script_sig[sign_len+2:sign_len+2+pubkey_len]
            logging.debug("pubkey: {0}".format(pubkey))
            sign = parseSignature(sign)
            pubkey = parsePubKey(pubkey)
            results.append((sign, pubkey))
        elif len(out_["script"]) == 130 or len(out_["script"]) == 66: #P2PK
            logging.debug("P2PK found")
            results.append(((0,0), parsepubKey(unhexlify(script_sig))))
        else:
            logging.warn("Unknown format. skipped.")
            logging.warn("In: {0}".format(script_sig))
            logging.warn("Out: {0}".format(out_["script"]))
            pass

    return results



def parseSignature(signature):
    
    # 署名が正しくDERエンコードされていることを確認
    if signature[0] != 0x30:
        logging.warn("No DER Format! signature: {0}".format(signature))
        return 0,0 
    # Rの値の取得
    r_length = signature[3]
    r = int.from_bytes(signature[4:4+r_length], byteorder='big')
    
    # Sの値の取得
    s_length = signature[4+r_length+1]
    s = int.from_bytes(signature[6+r_length:6+r_length+s_length], byteorder='big')
    
    return r, s

def parsePubKey(pubkey):
    vk = VerifyingKey.from_string(pubkey, curve=SECP256k1)
    return vk.pubkey.point.x(), vk.pubkey.point.y()

@retry(ConnectionError, tries=5, delay=2)
def extractInfosFromHeight(height, conn):
    result = []
    blockHash = getBlockHash(height, conn)
    transactionIds = getTransactionIds(blockHash, conn)
    for transactionId in transactionIds:
        transactionHex = getTransactionHex(transactionId, conn)
        try:
            result += getSignAndPubkeys(transactionHex)
        except:
            logging.error("The exception happens during parsing sign and pubkeys for height {0}".format(height))
    return result