import sys

from Common.config import *
from Common.LoggingSetup import *
from MerkleTreeHandling.MerkleTreeNode import MerkleTreeNode
from MerkleTreeHandling.MerkleTreeNodeInfo import MerkleTreeNodeInfo


class MerkleTree:
    def __init__(self, txnList):
        self.txnList = txnList
        self.treeRoot = self.generateMerkleTree()
        self.treeHash = self.treeRoot.treeNodeHash
        self.treeNodeCount = self.calculateTreeNodeCount()
        self._treeSize = self.treeNodeCount * sys.getsizeof(self.treeHash)

    def generateMerkleTree(self):
        logger.info("Merkle Tree Generation Called")
        nodesQueue = []
        # Add all the transactions in the queue
        # Handles the leaf nodes
        for transaction in self.txnList:
            tree_node = MerkleTreeNodeInfo(
                MerkleTreeNode([], txn=transaction, isLeafNode=True), 0
            )
            nodesQueue.append(tree_node)

        # We want the root to be there in the children
        while len(nodesQueue) > 1:
            currentLevel = nodesQueue[0].level
            nodesForParentLevel = []

            for i in range(arity):
                if len(nodesQueue) > 0 and nodesQueue[0].level == currentLevel:
                    nodesForParentLevel.append(
                        nodesQueue[0].node
                    )  # YOU ONLY APPEND THE NODE DETAILS not the level info
                    nodesQueue.remove(nodesQueue[0])
            nodesQueue.append(
                MerkleTreeNodeInfo(
                    MerkleTreeNode(nodesForParentLevel, isLeafNode=False),
                    currentLevel + 1,
                )
            )

        # Returns the root of the Merkle Tree generated
        logger.info("Merkle Tree Generation over")
        logger.info("Root is : " + str(nodesQueue[0].node))
        return nodesQueue[0].node

    def calculateTreeNodeCount(self):
        # NOTE : The parent paper of this project checks the behaviour of
        # BITCOIN SYSTEM , wrt to maxMerkleTreeLeadNode possible
        # Hence to make the project consistent with that logic
        # I have added a if - else condition
        if maxMerkleTreeLeafNode is None:
            numOfNodes = len(self.txnList)
        else:
            numOfNodes = maxMerkleTreeLeafNode

        n = numOfNodes
        while n > 1:
            numOfNodes += (n + arity - 1) // arity
            n = (n + arity - 1) // arity
        return numOfNodes

    def getMerkleTreeSystemSize(self):
        return self._treeSize

    def __str__(self):
        printValue = "MerkleTree("
        printValue += " TreeHash : " + str(self.treeHash) + ","
        printValue += " TreeNodeCount: " + str(self.treeNodeCount)
        printValue += ")"
        return printValue
