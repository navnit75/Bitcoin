from Common.config import *
from Common.HashAlgo import *


class MerkleTreeNode:
    # NOTE: The logic behind the isLeafNode is that, if a node is a leav node the childrenTreeNodes will be null
    # But the it will have txns in the txnList
    # But if a node of tree is non leaf - it will not contain txn list
    # NOTE: to remove the ambiguity in naming of a node vs merkle tree node, I am naming all the merkle Tree Node based account into
    def __init__(self, childrenTreeNodes, txn=None, isLeafNode=False):
        self.txn = txn
        self.isLeafNode = isLeafNode
        self.childrenTreeNodes = childrenTreeNodes
        self.treeNodeHash = (
            self.txn.getTransactionHash()
            if self.isLeafNode
            else self.calculateTreeNodeHash()
        )

    # NOTE: This function main job is to calculate the nodeHash of a non leaf node
    def calculateTreeNodeHash(self):
        localTreeNodeHash = ""
        for childTreeNode in self.childrenTreeNodes:
            localTreeNodeHash += childTreeNode.treeNodeHash

        # If the num of child is less than arity,
        # Then add the last child hash as pad value
        # NOTE: Merkle tree rules suggests that if there are
        diffInArity = arity - len(self.childrenTreeNodes)
        if diffInArity > 0:
            lastIndexTreeNodeHash = self.childrenTreeNodes[-1]
            localTreeNodeHash += lastIndexTreeNodeHash.treeNodeHash * diffInArity

        localTreeNodeHash = generateHash(localTreeNodeHash)
        return localTreeNodeHash

    def __str__(self):
        printString = "MerkleTree( leafNode = " + str(self.isLeafNode)
        if self.isLeafNode is True:
            printString += ", txn = " + str(self.txn.getTransactionHash())
        else:
            printString += ", countChildrenNode = " + str(len(self.childrenTreeNodes))
        printString += ")"
        return printString
