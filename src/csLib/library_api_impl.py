from datetime import datetime
import subprocess
from uuid import uuid4
from pathlib import Path

from webcligui_api import LibraryAPI, OperationType, Operation, OperationFolder, OperationStatusStart, ParameterData
from webcligui_api import ParameterOptionsToList, ParameterList, ParameterStringValue, ParameterPreference

BYSTAR_DIRECTORY = '/bxo/usg/bystar'
OPERATION_ROOT_DIRECTORY = f'{BYSTAR_DIRECTORY}/operationTasks'
CSLIB_DIRECTORY = f'{BYSTAR_DIRECTORY}/develop/csLib'

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
    libraryFolder = OperationFolder(name="csLib")
    libraryFolder.portfolio.append(Operation(name="facter.cs", operation_type=OperationType.PIPX))
    libraryFolder.portfolio.append(Operation(name="banna.cs", operation_type=OperationType.PIPX))
    libraryFolder.portfolio.append(Operation(name="soncli.cs", operation_type=OperationType.MODULE))
    libraryFolder.portfolio.append(Operation(name="facterNEW2.cs", operation_type=OperationType.MODULE))
    sonFolder = OperationFolder(name="SON Modules")
    libraryFolder.portfolio.append(sonFolder,)
    sonFolder.portfolio.append(Operation(name="rtsel.py", operation_type=OperationType.MODULE))
    libraryFolder.portfolio.append(Operation(name="fvr_operation.py", operation_type=OperationType.PIPX))

    def getOperationHierarchy(self) -> OperationFolder:
        return self.libraryFolder
    
    def getDescription(self, operationBranch: list[str]) -> str:
        operationName = "_".join(operationBranch)
        if operationName not in operationsData:
            raise Exception(f'{operationName} not found')
        operationData = operationsData[operationName]
        if 'description' not in operationData:
            return 'No description found'
        return operationData['description']
            
    def getParameters(self, operationBranch: list[str]) -> ParameterData:
        operationName = "_".join(operationBranch)
        operationData = operationsData[operationName]
        if operationData is None:
            return None
        return operationData['parameters']

    def submitOperation(self, operationBranch: list[str], command: list[str], servers: list[str]):
        """Execute the operation with the given command and servers."""
        try:
            # Look up the operation to get its type
            operation = self._findOperation(operationBranch)
            if operation is None:
                return {'status': 'error', 'message': f'Operation {operationBranch} not found'}
            
            # Build the full command based on operation type
            fullCommand = self._buildCommand(operation, command)
            
            print(f"submitOperation: operationBranch={operationBranch}, command={command}, servers={servers}")
            print(f"submitOperation: fullCommand={fullCommand}")
            
            # Execute the command
            result = subprocess.run(
                fullCommand,
                check=True,
                capture_output=True,
                text=True
            )
            
            return {
                'status': 'success',
                'message': 'Operation completed successfully',
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        
        except subprocess.CalledProcessError as exc:
            print(f'submitOperation CalledProcessError: {exc}')
            return {
                'status': 'error',
                'message': f'Operation failed with exit code {exc.returncode}',
                'stdout': exc.stdout,
                'stderr': exc.stderr
            }
        except Exception as exc:
            print(f'submitOperation Exception: {exc}')
            return {
                'status': 'error',
                'message': f'Operation failed: {str(exc)}'
            }

    def _findOperation(self, operationBranch: list[str]) -> Operation:
        """Find the Operation object in the library folder by branch."""
        current = self.libraryFolder
        
        for name in operationBranch:
            found = None
            if hasattr(current, 'portfolio'):
                for item in current.portfolio:
                    if item.name == name:
                        found = item
                        break
            
            if found is None:
                return None
            current = found
        
        return current if isinstance(current, Operation) else None

    def _buildCommand(self, operation: Operation, command: list[str]) -> list[str]:
        """Build the full command based on the operation type."""
        if operation.operation_type == OperationType.PIPX:
            return ['pipx', 'run'] + command
        elif operation.operation_type == OperationType.MODULE:
            return ['python', '-m'] + command
        else:
            # Default: just return the command as-is
            return command

    def submitOperation(self, operationBranch: list[str], command: list[str], servers: list[str]) -> OperationStatusStart:
        # Ignore all parameters, just start fvr_operation.py
        uuid = str(uuid4())
        folder = OPERATION_ROOT_DIRECTORY + '/' + uuid
        Path(folder).mkdir()

        with open(f"{folder}/out.log", "a") as out, open(f"{folder}/err.log", "a") as err:
          subprocess.Popen(
              ['python', f'{CSLIB_DIRECTORY}/fvr_operation.py'],
              cwd=folder,
              stdout=out,
              stderr=err,
              stdin=subprocess.DEVNULL,
              start_new_session=True
            )
        start_time = datetime.now()

        startStatus = OperationStatusStart(uuid=uuid, start_time=start_time, folder=folder)
        return startStatus
    