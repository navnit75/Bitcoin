hashSize = 256
arity = 4

# NOTE : This is author kept number for the leaf nodes when mekle tree size is calculated.
# I am guessing its kept mostly to keep the parameters of experiment similar.
# Hence I am adding an option to change this to `None` in which case it considers the original leaf node
# i.e. nothing but original number of transactions a block has.
maxMerkleTreeLeafNode = 15

nodeCount = 5
walletCountPerNode = 5
incentiveAmount = 1
genesisBlockBitCoin = 1000
sizeOfNonce = 32
probabilityOfTxn = 0.2  # NOTE : out of 1
