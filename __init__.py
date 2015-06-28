from . import cluster
from . import softSelection


def run():
	result = softSelection.getSelectionWeight()
	cluster.createCluster(result)

