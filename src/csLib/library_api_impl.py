from webcligui_api import LibraryAPI, OperationType, Operation, OperationFolder, ParameterData
from webcligui_api import ParameterOptionsToList, ParameterList, ParameterStringValue, ParameterPreference

operationsData = {}

facterDescription = '''
# Facter.cs

A **CS-Lib** for creating and managing BPO's gpg and encryption/decryption.
'''

facterOptions = ParameterOptionsToList(name='-i', description='List of commands for facter')

paramList = ParameterList(name='cmdbSummary');
paramList.parameters.append(ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

paramList = ParameterList(name='csxuFpsToGraphviz');
paramList.parameters.append(ParameterStringValue(name='--csxuFpsBasePath', description='Path to fps'))
paramList.parameters.append(ParameterStringValue(name='--csxuName', description='Name of csxu'))
paramList.parameters.append(ParameterStringValue(name='--pyDictResultPath', description='Path to dict result file'))
paramList.parameters.append(ParameterStringValue(name='--graphvizResultPath', description='Path to graphviz result file'))
facterOptions.options.append(paramList)

paramList = ParameterList(name='csxuFpsToPyDict');
paramList.parameters.append(ParameterStringValue(name='--csxuFpsBasePath', description='Path to fps'))
paramList.parameters.append(ParameterStringValue(name='--csxuName', description='Name of csxu'))
paramList.parameters.append(ParameterStringValue(name='--pyDictResultPath', description='Path to dict result file'))
facterOptions.options.append(paramList)

facterOptions.options.append(ParameterList(name='csxuInSchema'))

facterOptions.options.append(ParameterList(name='examples_csu'))

paramList = ParameterList(name='factName');
paramList.parameters.append(ParameterPreference(name='--cache', description='Apply cache'))
paramList.parameters.append(ParameterStringValue(name='--fromFile', description='Path to the fromFile'))
paramList.parameters.append(ParameterStringValue(name='--perfName', description='Name of the Perf'))
paramList.parameters.append(ParameterStringValue(name='', mandatory=True, description='factName component'))
facterOptions.options.append(paramList)

paramList = ParameterList(name='factNameGetattr');
paramList.parameters.append(ParameterPreference(name='--cache', description='Apply cache'))
paramList.parameters.append(ParameterStringValue(name='--fromFile', description='Path to the fromFile'))
paramList.parameters.append(ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

facterOptions.options.append(ParameterList(name='facterJsonOutputBytes'))

paramList = ParameterList(name='facterJsonOutputBytesToFile');
paramList.parameters.append(ParameterStringValue(name='--fromFile', mandatory=True, description='Path to the fromFile'))
paramList.parameters.append(ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

paramList = ParameterList(name='roCmnd_examples');
paramList.parameters.append(ParameterStringValue(name='--sectionTitle', mandatory=True, description='Title for this section'))
paramList.parameters.append(ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

paramList = ParameterList(name='roInv_examples_csu');
paramList.parameters.append(ParameterStringValue(name='--sectionTitle', mandatory=True, description='Title for this section'))
paramList.parameters.append(ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

paramList = ParameterList(name='roPerf_examples_csu');
paramList.parameters.append(ParameterStringValue(name='--sectionTitle', mandatory=True, description='Title for this section'))
facterOptions.options.append(paramList)

operationsData['facter.cs'] = {'description': facterDescription, 'parameters': facterOptions}


class LibraryAPIImpl(LibraryAPI):
    libraryFolder = OperationFolder(name="csLib")
    libraryFolder.portfolio.append(Operation(name="facter.cs", operation_type=OperationType.PIPX))

    def getOperationHierarchy(self) -> OperationFolder:
        return self.libraryFolder
    
    def getDescription(self, operationBranch: list[str]) -> str:
        operationName = "_".join(operationBranch)
        operationData = operationsData[operationName]
        if operationData is None:
            return None
        return operationData['description']
            
    def getParameters(self, operationBranch: list[str]) -> ParameterData:
        operationName = "_".join(operationBranch)
        operationData = operationsData[operationName]
        if operationData is None:
            return None
        return operationData['parameters']
