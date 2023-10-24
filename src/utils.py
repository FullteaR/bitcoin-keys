import os
from bitcoinrpc.authproxy import AuthServiceProxy
import bitcoin
from binascii import unhexlify
from ecdsa import VerifyingKey, SECP256k1

def getConn():
    rpc_user = "frt"
    rpc_password = "pass"
    #rpc_host = os.environ["RPC_HOST"]
    #rpc_port = os.environ["RPC_PORT"]
    rpc_host = "bitcoin-server"
    rpc_port = "8332"

    rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
    return AuthServiceProxy(rpc_url)


def getBlockHash(height):
    conn = getConn()
    return conn.getblockhash(height)


def getTransactionIds(blockHash):
    conn = getConn()
    return conn.getblock(blockHash)["tx"]


def getTransactionHex(transactionId):
    conn = getConn()
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

#id_ = "5a4216acfb7b8619b4455925e77d789867cea06b74c77f09be41037fcddc062c"
#transactionHex = getTransactionHex(id_)
#assert transactionHex=="01000000015975479e8161302eca4b69ad687418655dfc6d960da3c642542d712193bc6127010000006b48304502210094ea6b6cce6b1224047c39fd5da6ce932d0a5091a5d20f4e1dd4d2e1a6c04733022065d606a3e210650c1ad857d99a1eadd12ab7f08d5def1913766117124be0cec7012102a166ea841c7344b2d3a9a1f9e890d8b2144b5b975cb0ed87d68f12065df89ea7ffffffff0258c90900000000001976a9141eca25f20d936a6e176701b6fe2953d358d9add788ac86022b00000000001976a9144edc3518c2b5eb0a35535d0c47f164b7b5423a0a88ac00000000"

#signAndPubkeys = getSignAndPubkeys(transactionHex)
#assert len(signAndPubkeys)==1
