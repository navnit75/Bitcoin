import hashlib

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme

# NOTE: This validation is done for a prevTxn , which has reached to a new txn, who is trying to add this prevTxn to its input
# - senderScript : In this case would be the senderScript details are taken from the request , sent by sender to create a new transaction
# - receiverScript : In this case the receiverScript details is obtained from the sender's previousTxn's receiver which is sender itself
def validateTxnHash(senderHashesObj, receiverHashesObj, txnHash):
    senderSignature = senderHashesObj.senderSignature
    senderPublicKey = senderHashesObj.senderPublicKey

    receiverLockedTxnHash = receiverHashesObj.lockedTxnHash

    genSenderUnlockingHash = SHA256.new(
        hashlib.sha256(senderPublicKey).hexdigest().encode()
    )
    genSenderUnlockingHash.update(txnHash.encode())

    if genSenderUnlockingHash.hexdigest() != receiverLockedTxnHash.hexdigest():
        return False  # NOTE: Basically means the receiver is not the right receiver

    verifier = PKCS115_SigScheme(RSA.importKey(senderPublicKey))
    try:
        verifier.verify(receiverLockedTxnHash, senderSignature)
    except:
        return False
    return True
