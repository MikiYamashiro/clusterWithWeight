from maya.OpenMaya import *
from maya import cmds


def _single(point):
    return "[%s]" % (point)


def _double(point):
    return "[%s][%s]" % (point[0], point[1])


def _triple(point):
    return "[%s][%s][%s]" % (point[0], point[1], point[2])


def _getConvertedData(dag_path, point_weight_list, target_point_weight):
    object_name = dag_path.fullPathName()
    if dag_path.hasFn(MFn.kMesh) == True:
        for point, weight in point_weight_list:
            target_point_weight.update({'%s.vtx%s' % (object_name,
                                                      _single(point)): weight})
    elif dag_path.hasFn(MFn.kNurbsCurve) == True:
        for point, weight in point_weight_list:
            target_point_weight.update({'%s.cv%s' % (object_name,
                                                     _single(point)): weight})
    elif dag_path.hasFn(MFn.kNurbsSurface) == True:
        for point, weight in point_weight_list:
            target_point_weight.update({'%s.cv%s' % (object_name,
                                                     _double(point)): weight})
    elif dag_path.hasFn(MFn.kLattice) == True:
        for point, weight in point_weight_list:
            target_point_weight.update({'%s.pt%s' % (object_name,
                                                     _triple(point)): weight})


def createCluster(selection_list):
    target_point_weight = {}
    for dag_path, point_weight_list in selection_list.items():
        _getConvertedData(dag_path, point_weight_list, target_point_weight)
    cmds.softSelect(e=True, sse=False)
    cmds.select(target_point_weight.keys())
    cluster_node = cmds.cluster()
    for point, weight in target_point_weight.items():
        cmds.percent(cluster_node[0], point, v=weight)