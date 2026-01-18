from webcligui_api import OperationType, Operation, OperationFolder, LibraryAPI

class LibraryAPIImpl(LibraryAPI):
    def getOperationHierarchy(self) -> OperationFolder:
        libraryFolder = OperationFolder(folder_name="csLib")
        libraryFolder.portfolio.append(Operation(operation_type=OperationType.PIPX, operation_name="facter"))

        return libraryFolder
    