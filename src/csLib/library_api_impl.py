from datetime import datetime
import subprocess
from uuid import uuid4
from pathlib import Path

from webcligui_api import LibraryAPI, OperationType, Operation, OperationFolder, OperationStatusStart, ParameterData
from webcligui_api import ParameterOptionsToList, ParameterList, ParameterStringValue, ParameterPreference

LIBRARY_NAME = "csLib"

BYSTAR_DIRECTORY = Path('/bxo/usg/bystar').resolve()
OPERATION_ROOT_DIRECTORY = (BYSTAR_DIRECTORY / 'operationTasks').resolve()
CSLIB_DIRECTORY = (BYSTAR_DIRECTORY / 'develop' / 'csLib').resolve()

operationsData = {}


'''
========================================================
Facter.cs
========================================================
'''

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

'''
========================================================
fvr_operation.py
========================================================
'''

fvrOperationDescription = '''
# fvr_operation.py

A simple test operation that runs in the background and updating its status
'''
operationsData['fvr_operation.py'] = {'description': fvrOperationDescription, 'parameters': None}


class LibraryAPIImpl(LibraryAPI):
    libraryFolder = OperationFolder(name=LIBRARY_NAME)
    libraryFolder.portfolio.append(Operation(name="facter.cs", operation_type=OperationType.PIPX))
    libraryFolder.portfolio.append(Operation(name="banna.cs", operation_type=OperationType.PIPX))
    libraryFolder.portfolio.append(Operation(name="soncli.cs", operation_type=OperationType.MODULE))
    libraryFolder.portfolio.append(Operation(name="facterNEW2.cs", operation_type=OperationType.MODULE))
    libraryFolder.portfolio.append(Operation(name="rtsel.py", operation_type=OperationType.PYTHON))
    libraryFolder.portfolio.append(Operation(name="fvr_operation.py", operation_type=OperationType.PYTHON))

    def getOperationHierarchy(self) -> OperationFolder:
        return self.libraryFolder
    
    def _getOperationData(self, operationBranch: list[str]):
        if len(operationBranch) != 1:
           raise Exception(f"{LIBRARY_NAME} doesn't accept directories (len(operationBranch) != 1)")
        operationName = operationBranch[0]
        if operationName not in operationsData:
            raise Exception(f'{operationBranch}: operationsData not found')
        return operationsData[operationName]
       
    def getDescription(self, operationBranch: list[str]) -> str:
        operationData = self._getOperationData(operationBranch)
        if 'description' not in operationData:
            raise Exception(f'{operationBranch}: No description found')
        return operationData['description']
            
    def getParameters(self, operationBranch: list[str]) -> ParameterData:
        operationData = self._getOperationData(operationBranch)
        if 'parameters' not in operationData:
            raise Exception(f'{operationBranch}: No parameters found')
        return operationData['parameters']

    def submitOperation(self, operationBranch: list[str], command: list[str], servers: list[str]) -> OperationStatusStart:
        """Execute the operation with the given command and servers."""
        operation = self._findOperation(operationBranch)
        
        # Build the full command based on operation type
        cmd = self._buildCommand(operation, command)
        if cmd['uuid'] is None:
           raise Exception(f'uuid not set for operation {operationBranch}')

        print(f"submitOperation: uuid={cmd['uuid']}")
        print(f"submitOperation: operationBranch={operationBranch}, command={command}, servers={servers}")
        print(f"submitOperation: full_command={cmd['full_command']}")

        run_folder = OPERATION_ROOT_DIRECTORY / cmd['run_folder']
        out_file = run_folder / 'out.log'
        err_file = run_folder / 'err.log'
        with out_file.open("a") as out, err_file.open("a") as err:
          subprocess.Popen(
              cmd['full_command'],
              cwd=run_folder,
              stdout=out,
              stderr=err,
              stdin=subprocess.DEVNULL,
              start_new_session=True
            )
        start_time = datetime.now()

        startStatus = OperationStatusStart(uuid=cmd['uuid'], start_time=start_time, folder=cmd['run_folder'])
        return startStatus

    def _findOperation(self, operationBranch: list[str]):
      if len(operationBranch) != 1:
          raise Exception(f"{LIBRARY_NAME} doesn't accept directories (len(operationBranch) != 1)")
      result = next((x for x in self.libraryFolder.portfolio if x.name == operationBranch[0]), None)
      if result is None:
        raise Exception(f'{operationBranch}: operation not found')
      return result 

    def _buildCommand(self, operation: Operation, command: list[str]):
        """Build the full command based on the operation type."""
        match operation.operation_type:
          case OperationType.PIPX:
            return { 'uuid': None, 'run_folder': None, 'full_command': ['pipx', 'run'] + command }
          case OperationType.MODULE:
            return { 'uuid': None, 'run_folder': None, 'full_command': ['python', '-m'] + command }
          case OperationType.PYTHON:
            uuid = str(uuid4())
            folder = OPERATION_ROOT_DIRECTORY / uuid
            folder.mkdir()
            python_operation = CSLIB_DIRECTORY / command[0]
            command[0] = str(python_operation)
            return { 'uuid': uuid, 'run_folder': uuid, 'full_command': ['python'] + command }
          case _:
            raise Exception(f'Unknown OperationType {operation.operation_type}')
    