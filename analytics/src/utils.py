import hashlib
import base58
from ecdsa import VerifyingKey, SECP256k1

def pubkey_to_address(x, y):
    # 公開鍵を非圧縮形式のバイト文字列に変換
    pubkey_bytes = b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

    # SHA256ハッシュを計算
    sha256 = hashlib.sha256(pubkey_bytes).digest()

    # RIPEMD-160ハッシュを計算
    ripemd160 = hashlib.new('ripemd160', sha256).digest()

    # ネットワークバイトの追加（0x00: 主要なBitcoinネットワーク）
    versioned_payload = b'\x00' + ripemd160

    # チェックサムの追加
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    address_bytes = versioned_payload + checksum

    # Base58Checkエンコードを行い、Bitcoinアドレスを取得
    address = base58.b58encode(address_bytes).decode('utf-8')
    return address
