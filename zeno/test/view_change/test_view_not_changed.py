from typing import Iterable

from zeno.common.looper import Looper

from zeno.common.util import getMaxFailures
from zeno.test.helper import TestNodeSet, getNonPrimaryReplicas, ppDelay, \
    checkViewNoForNodes, sendReqsToNodesAndVerifySuffReplies
from zeno.test.helper import TestReplica

nodeCount = 7
F = getMaxFailures(nodeCount)


# noinspection PyIncorrectDocstring
def testViewNotChanged(looper: Looper, nodeSet: TestNodeSet, up, client1):
    """
    Test that a view change is not done when the performance of master does
    not go down
    """
    """
    Send multiple requests to the client and delay some requests by all
    backup instances to ensure master instance
    is always faster than backup instances and there is no view change
    """

    # Delay PRE-PREPARE for all backup protocol instances so master performs
    # better
    for i in range(1, F + 1):
        nonPrimReps = getNonPrimaryReplicas(nodeSet, i)
        # type: Iterable[TestReplica]
        for r in nonPrimReps:
            r.node.nodeIbStasher.delay(ppDelay(10, i))

    sendReqsToNodesAndVerifySuffReplies(looper, client1, 5)

    checkViewNoForNodes(nodeSet, 0)
