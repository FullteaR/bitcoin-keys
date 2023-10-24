import os
from bitcoinrpc.authproxy import AuthServiceProxy
import bitcoin
from binascii import unhexlify
from ecdsa import VerifyingKey, SECP256k1

def getConn():
    rpc_user = "frt"
    rpc_password = "pass"
    rpc_host = os.environ["RPC_HOST"]
    rpc_port = os.environ["RPC_PORT"]

    rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
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
            sign_len = int(script_sig[:2], 16)*2
            sign = script_sig[2:sign_len+2]
            pubkey_len = int(script_sig[sign_len+2:sign_len+4], 16)*2
            pubkey = script_sig[sign_len+4:sign_len+4+pubkey_len]
            sign = parseSignature(sign)
            results.append((sign, parsePubKey(pubkey)))
        elif len(out_["script"]) == 130 or len(out_["script"]) == 66: #P2PK
            results.append(((), parsepubKey(script_sig)))

    return results

def parseSignature(signature_hex):
    signature = unhexlify(signature_hex)
    
    # 署名が正しくDERエンコードされていることを確認
    if signature[0] != 0x30:
        return 0,0 
    # Rの値の取得
    r_length = signature[3]
    r = int.from_bytes(signature[4:4+r_length], byteorder='big')
    
    # Sの値の取得
    s_length = signature[4+r_length+1]
    s = int.from_bytes(signature[6+r_length:6+r_length+s_length], byteorder='big')
    
    return r, s

def parsePubKey(pubkey_hex):
    pubkey_bytes = unhexlify(pubkey_hex)
    vk = VerifyingKey.from_string(pubkey_bytes, curve=SECP256k1)
    return vk.pubkey.point.x(), vk.pubkey.point.y()

