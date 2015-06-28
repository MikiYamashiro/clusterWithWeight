from maya.OpenMaya import *


class Component():
    def _getWeight(self, index):
        return self.weight(index).influence()

    def getIndexWeights(self):
        return_list = []
        for i, index in enumerate(self._getIndice()):
            return_list.append((index, self._getWeight(i)))
        return return_list


class SingleComponent(Component, MFnSingleIndexedComponent):
    def __init__(self, object):
        super(SingleComponent, self).__init__(object)

    def _getIndice(self):
        int_array = MIntArray()
        self.getElements(int_array)
        return int_array


class DoubleComponent(Component, MFnDoubleIndexedComponent):
    def __init__(self, object):
        super(DoubleComponent, self).__init__(object)

    def _getIndice(self):
        u_array = MIntArray()
        v_array = MIntArray()
        self.getElements(u_array, v_array)
        return zip(u_array, v_array)


class TripleComponent(Component, MFnTripleIndexedComponent):
    def __init__(self, object):
        super(TripleComponent, self).__init__(object)

    def _getIndice(self):
        s_array = MIntArray()
        t_array = MIntArray()
        u_array = MIntArray()
        self.getElements(s_array, t_array, u_array)
        return zip(s_array, t_array, u_array)


def _getMFnComponentClass(component):
    if component.hasFn(MFn.kSingleIndexedComponent) == True:
        return SingleComponent(component)
    elif component.hasFn(MFn.kDoubleIndexedComponent) == True:
        return DoubleComponent(component)
    elif component.hasFn(MFn.kTripleIndexedComponent) == True:
        return TripleComponent(component)


def _hasSelection():
    selection = MSelectionList()
    MGlobal.getActiveSelectionList(selection)
    return True if selection.isEmpty() == False else True


def _getDagPathByIndex(selection, index):
    dag = MDagPath()
    obj = MObject()
    selection.getDagPath(index, dag, obj)
    return (dag, obj)


def _getCurrentSoftSelection():
    ### define variables
    dag_component = {}
    ### check has selection
    if _hasSelection() == True:
        ### define variables
        rich_selection = MRichSelection()
        selection = MSelectionList()
        ### get rich selection
        MGlobal.getRichSelection(rich_selection)
        ### rich selection to selection list
        rich_selection.getSelection(selection)
        for index in range(selection.length()):
            dag_comp = _getDagPathByIndex(selection, index)
            dag_component.update({dag_comp[0]: dag_comp[1]})
    return dag_component


def getSelectionWeight():
    ### define
    dag_index_weight = {}
    ### get selection
    dag_component = _getCurrentSoftSelection()
    ### get index, weight
    # return dag_component
    for dag, component in dag_component.items():
        ### Mfn class check
        comp_class = _getMFnComponentClass(component)
        if comp_class != None:
            dag_index_weight.update({dag: comp_class.getIndexWeights()})
    return dag_index_weight
