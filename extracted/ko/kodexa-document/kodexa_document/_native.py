"""
Native library loading for Go bindings using CFFI.
"""

import logging
import os
import platform
import signal
import sys
from pathlib import Path
from typing import Optional

from cffi import FFI

logger = logging.getLogger(__name__)

# Detect execution environment
logger.info("Detecting environment")
IS_LAMBDA = bool(os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
logger.info(f"Is lambda: {IS_LAMBDA}")

# Configure Go runtime for Lambda/container to prevent threading/signal conflicts
# Go's async preemption (SIGURG) can conflict with Lambda's runtime, causing deadlocks.
# Setting asyncpreemptoff=1 disables this. cgocheck=0 disables CGO pointer checks.
# See: .work/go-python-deadlock-fixes.md for full explanation
if IS_LAMBDA:
    logger.info("Lambda environment detected, configuring Go runtime settings")
    existing_godebug = os.environ.get('GODEBUG', '')
    required_settings = 'asyncpreemptoff=1,cgocheck=0'
    if 'asyncpreemptoff' not in existing_godebug:
        if existing_godebug:
            os.environ['GODEBUG'] = f"{existing_godebug},{required_settings}"
        else:
            os.environ['GODEBUG'] = required_settings
        logger.info(f"Set GODEBUG={os.environ['GODEBUG']}")
    else:
        logger.info(f"GODEBUG already set: {existing_godebug}")

    # Set GOTRACEBACK for debugging deadlocks (shows stack traces on crash)
    if 'GOTRACEBACK' not in os.environ:
        os.environ['GOTRACEBACK'] = 'crash'
        logger.info("Set GOTRACEBACK=crash")
    else:
        logger.info(f"GOTRACEBACK already set: {os.environ['GOTRACEBACK']}")

    # Limit Go to single OS thread to prevent CGO deadlocks
    if 'GOMAXPROCS' not in os.environ:
        os.environ['GOMAXPROCS'] = '1'
        logger.info("Set GOMAXPROCS=1")
    else:
        logger.info(f"GOMAXPROCS already set: {os.environ['GOMAXPROCS']}")

# Create FFI instance
ffi = FFI()

# Declare all C functions from the Go library
ffi.cdef("""
    // Library information
    char* GetLibraryVersion();
    char* GetBuildInfo();
    int IsLambdaEnvironment();
    
    // Document lifecycle
    unsigned long long CreateDocument(const char* jsonInput);
    unsigned long long OpenDocument(const char* path, int detached, int inmemory, int deleteOnClose);
    unsigned long long OpenDocumentFromBytes(const void* data, int size, int inmemory);
    int SaveDocument(unsigned long long handle, const char* path);
    int CloseDocument(unsigned long long handle);
    void FreeHandle(unsigned long long handle);
    
    // Document export
    void* GetDocumentBytes(unsigned long long handle, int* size);
    
    // Document properties
    char* GetDocumentJSON(unsigned long long handle);
    char* GetDocumentUUID(unsigned long long handle);
    char* GetDocumentVersion(unsigned long long handle);
    
    // Document creation utilities
    unsigned long long CreateDocumentFromText(const char* text, const char* separator, int inmemory);
    unsigned long long CreateDocumentFromJSON(const char* jsonData, int inmemory);
    
    // Memory management
    void FreeString(char* str);
    void FreeBytes(void* ptr);
    
    // Error handling
    int KodexaGetLastError();
    char* KodexaGetLastErrorMessage();
    void ClearError();
    
    // Utility functions
    char* GetMemoryStats();
    void ForceGarbageCollection();
    
    // ContentNode operations
    unsigned long long CreateContentNode(unsigned long long docHandle, const char* nodeType, const char* content, int index);
    char* GetNodeType(unsigned long long nodeHandle);
    char* GetNodeContent(unsigned long long nodeHandle);
    int GetNodeIndex(unsigned long long nodeHandle);
    int GetNodeID(unsigned long long nodeHandle);
    int IsNodeVirtual(unsigned long long nodeHandle);
    char* GetNodeUUID(unsigned long long nodeHandle);
    int SetNodeContent(unsigned long long nodeHandle, const char* content);
    int SetNodeIndex(unsigned long long nodeHandle, int index);
    
    // Content Parts Operations
    char* GetNodeContentParts(unsigned long long nodeHandle);
    int SetNodeContentParts(unsigned long long nodeHandle, const char* partsJSON);
    
    // Document-Node integration
    unsigned long long GetDocumentContentNode(unsigned long long docHandle);
    int SetDocumentContentNode(unsigned long long docHandle, unsigned long long nodeHandle);
    unsigned long long DocumentCreateNode(unsigned long long docHandle, const char* nodeType, const char* content);
    unsigned long long DocumentCreateNodeWithOptions(unsigned long long docHandle, const char* nodeType, const char* content, int virtual, unsigned long long parentHandle, int index);
    
    // Tree Navigation
    unsigned long long GetNodeParent(unsigned long long nodeHandle);
    int GetNodeChildCount(unsigned long long nodeHandle);
    unsigned long long GetNodeChild(unsigned long long nodeHandle, int index);
    unsigned long long* GetNodeChildren(unsigned long long nodeHandle, int* count);
    int AddNodeChild(unsigned long long parentHandle, unsigned long long childHandle, int index);
    int RemoveNodeChild(unsigned long long parentHandle, unsigned long long childHandle);
    void FreeHandleArray(unsigned long long* handles);

    // Child Re-parenting Operations
    int ReparentNode(unsigned long long nodeHandle, unsigned long long newParentHandle, int index);
    int AdoptNodeChildren(unsigned long long parentHandle, unsigned long long* childHandles, int childCount, int replace);
    int DeleteNodeChildren(unsigned long long parentHandle, unsigned long long* childHandles, int childCount, unsigned long long* excludeHandles, int excludeCount);

    // Node Hierarchy Queries
    int IsNodeRoot(unsigned long long nodeHandle);
    int IsNodeFirstChild(unsigned long long nodeHandle);
    int IsNodeLastChild(unsigned long long nodeHandle);
    int IsNodeLeaf(unsigned long long nodeHandle);
    int GetNodeDepth(unsigned long long nodeHandle);
    int GetNodePage(unsigned long long nodeHandle);
    unsigned long long GetNodeFirstChild(unsigned long long nodeHandle);
    unsigned long long GetNodeLastChild(unsigned long long nodeHandle);

    // Confidence Operations
    double GetNodeConfidence(unsigned long long nodeHandle);
    int SetNodeConfidence(unsigned long long nodeHandle, double confidence);
    int HasNodeConfidence(unsigned long long nodeHandle);

    // BBox Operations
    int ClearNodeBBox(unsigned long long nodeHandle);
    int SetBboxFromChildren(unsigned long long nodeHandle);

    // Pattern Matching
    int NodeMatches(unsigned long long nodeHandle, const char* pattern);

    // Bulk Tag/Feature Operations
    int RemoveAllNodeTags(unsigned long long nodeHandle);
    int RemoveAllNodeFeatures(unsigned long long nodeHandle);
    
    // Sibling Navigation
    unsigned long long GetNextNode(unsigned long long nodeHandle, const char* nodeTypeRegex, int skipVirtual, int hasNoContent, int traverse);
    unsigned long long GetPreviousNode(unsigned long long nodeHandle, const char* nodeTypeRegex, int skipVirtual, int hasNoContent, int traverse);
    
    // Node Navigation Methods
    unsigned long long* GetNodeSiblings(unsigned long long nodeHandle, int* count);
    unsigned long long* GetNodePath(unsigned long long nodeHandle, int* count);
    char* GetNodeAllContent(unsigned long long nodeHandle, const char* separator, int strip);

    // Node Serialization
    char* NodeToDict(unsigned long long nodeHandle);
    
    // Selector Operations
    unsigned long long* DocumentSelect(unsigned long long docHandle, const char* selector, const char* variablesJSON, int first_only, int* count);
    unsigned long long DocumentSelectFirst(unsigned long long docHandle, const char* selector, const char* variablesJSON);
    unsigned long long* SelectNodes(unsigned long long nodeHandle, const char* selector, const char* variablesJSON, int* count);
    unsigned long long SelectSingleNode(unsigned long long nodeHandle, const char* selector, const char* variablesJSON);
    
    // Document Metadata Operations
    char* GetDocumentMetadata(unsigned long long handle);
    int SetDocumentMetadata(unsigned long long handle, const char* key, const char* value);
    
    // Document Source Metadata Operations
    char* GetDocumentSource(unsigned long long handle);
    int SetDocumentSource(unsigned long long handle, const char* sourceJSON);
    
    // Document ref property
    char* Document_GetRef(unsigned long long docHandle);
    void Document_SetRef(unsigned long long docHandle, char* ref);
    
    // Document delete_on_close property
    int Document_GetDeleteOnClose(unsigned long long docHandle);
    
    // External Data operations
    char* GetExternalData(unsigned long long handle, const char* key);
    int SetExternalData(unsigned long long handle, const char* key, const char* dataJSON);
    char* GetExternalDataKeys(unsigned long long handle);
    
    // Document Statistics
    char* GetDocumentStatistics(unsigned long long handle);
    
    // Document Query Operations
    char* GetDocumentAllTags(unsigned long long handle);
    char* GetNodesByType(unsigned long long handle, const char* nodeType);
    
    // Document Validations Operations
    char* GetValidations(unsigned long long handle);
    int SetDocumentValidationsList(unsigned long long handle, const char* validationsJSON);
    
    // Document Processing Steps Operations
    char* GetDocumentProcessingSteps(unsigned long long handle);
    int SetDocumentProcessingSteps(unsigned long long handle, const char* stepsJSON);

    // Document Knowledge Features Operations
    char* GetDocumentKnowledgeFeatures(unsigned long long handle);
    int SetDocumentKnowledgeFeatures(unsigned long long handle, const char* featuresJSON);

    // Document Knowledge Items Operations
    char* GetKnowledge(unsigned long long handle);
    int SetKnowledge(unsigned long long handle, char* itemsJSON);

    // Document Labels Operations  
    char* GetDocumentLabels(unsigned long long handle);
    int AddDocumentLabel(unsigned long long handle, const char* label);
    int RemoveDocumentLabel(unsigned long long handle, const char* label);
    
    // Document Mixins Operations
    char* GetDocumentMixins(unsigned long long handle);
    int AddDocumentMixin(unsigned long long handle, const char* mixin);
    
    // Document Exceptions Operations
    char* GetDocumentExceptions(unsigned long long handle);
    int AddDocumentException(unsigned long long handle, const char* exceptionJSON);

    // Data Exceptions Operations
    char* GetAllDataExceptions(unsigned long long handle);

    // Feature Management
    char* AddNodeFeature(unsigned long long nodeHandle, const char* featureType, const char* name, const char* valueJSON, int single, int serialized);
    int SetNodeFeature(unsigned long long nodeHandle, const char* featureType, const char* name, const char* valueJSON);
    char* GetNodeFeature(unsigned long long nodeHandle, const char* featureType, const char* name);
    char* GetNodeFeatureValue(unsigned long long nodeHandle, const char* featureType, const char* name);
    int HasNodeFeature(unsigned long long nodeHandle, const char* featureType, const char* name);
    char* GetAllNodeFeatures(unsigned long long nodeHandle);
    int RemoveNodeFeature(unsigned long long nodeHandle, const char* featureType, const char* name);
    char* GetNodeFeaturesOfType(unsigned long long nodeHandle, const char* featureType);
    
    // Tagging System
    int TagNode(unsigned long long nodeHandle, const char* tagName, const char* optionsJSON);
    char* GetNodeTags(unsigned long long nodeHandle);
    char* GetNodeTag(unsigned long long nodeHandle, const char* tagName);
    int RemoveNodeTag(unsigned long long nodeHandle, const char* tagName);
    int UpdateNodeTag(unsigned long long nodeHandle, const char* tagName, const char* valueJSON);
    int HasNodeTag(unsigned long long nodeHandle, const char* tagName);
    
    // Additional Tag and Feature Operations
    int AddTag(unsigned long long nodeHandle, const char* tagJSON);
    char* GetAllTaggedNodes(unsigned long long docHandle);
    char* GetTagsByName(unsigned long long docHandle, const char* tagName);

    // TagInstance Operations (legacy_python parity)
    char* GetTagInstances(unsigned long long docHandle, const char* tagName);
    char* GetTagInstance(unsigned long long docHandle, const char* tagName);
    int AddTagInstance(unsigned long long docHandle, const char* tagName, const char* nodeHandlesJSON);

    // Extraction Engine Operations
    // Taxonomy operations
    unsigned long long LoadTaxonomy(const char* taxonomyJSON);
    unsigned long long LoadTaxonomyFromFile(const char* path);
    char* GetTaxonomyJSON(unsigned long long taxonomyHandle);
    int ValidateTaxonomy(const char* taxonomyJSON);
    void FreeTaxonomy(unsigned long long taxonomyHandle);
    
    // Extraction operations
    unsigned long long CreateExtractionEngine(unsigned long long docHandle, const char* taxonomiesJSON);
    int ProcessAndSaveExtraction(unsigned long long engineHandle);
    char* GetContentExceptions(unsigned long long engineHandle);
    char* GetDocumentTaxonValidations(unsigned long long engineHandle);
    void FreeExtractionEngine(unsigned long long engineHandle);
    
    // ContentNode Lifecycle Operations
    unsigned long long GetNodeByUUID(unsigned long long docHandle, const char* uuid);
    int DeleteContentNode(unsigned long long nodeHandle);
    int SetNodeType(unsigned long long nodeHandle, const char* nodeType);
    int SetNodeVirtual(unsigned long long nodeHandle, int virtual);

    // Document Pretty Print Operations
    char* GetPrettyPage(unsigned long long handle, int pageIndex);
    char* GetPrettyPages(unsigned long long handle);

    // Document Lines Operations
    char* GetDocumentLines(unsigned long long handle);

    // Exception Management Operations
    char* GetOpenExceptions(unsigned long long handle);
    int CloseException(unsigned long long handle, unsigned int excID, const char* closingComment);

    // Native Document Operations
    char* DocumentGetNativeDocuments(unsigned long long handle);
    char* DocumentGetNativeDocumentByID(unsigned long long handle, unsigned int id);
    char* DocumentGetFirstNativeDocument(unsigned long long handle);
    char* DocumentGetNativeDocumentByFilename(unsigned long long handle, const char* filename);
    char* DocumentGetNativeDocumentData(unsigned long long handle, unsigned int id, int* outLen);
    unsigned int DocumentCreateNativeDocument(unsigned long long handle, const char* filename, const char* mimeType, const char* data, int dataLen, const char* checksum);
    int DocumentDeleteNativeDocument(unsigned long long handle, unsigned int id);
    int DocumentDeleteAllNativeDocuments(unsigned long long handle);

    // Data Object Operations
    char* DocumentGetDataObjects(unsigned long long handle);
    char* DocumentGetDataObjectByUUID(unsigned long long handle, const char* uuid);
    char* DocumentGetDataObjectsByGroupUUID(unsigned long long handle, const char* groupUuid);
    char* DocumentCreateDataObject(unsigned long long handle, const char* dataObjectJSON);
    char* DocumentUpdateDataObject(unsigned long long handle, const char* uuid, const char* dataObjectJSON);
    int DocumentDeleteDataObject(unsigned long long handle, unsigned int id);

    // Data Attribute Operations
    char* DocumentGetDataAttributes(unsigned long long handle, unsigned int dataObjectID);
    char* DocumentGetDataAttributeByID(unsigned long long handle, unsigned int attrID);
    char* DocumentGetDataAttributesByDataObjectID(unsigned long long handle, unsigned int dataObjectID);
    unsigned int DocumentCreateDataAttribute(unsigned long long handle, const char* attrJSON);
    int DocumentUpdateDataAttribute(unsigned long long handle, const char* attrJSON);
    int DocumentDeleteDataAttribute(unsigned long long handle, unsigned int attrID);

    // Audit Operations
    char* DocumentListAuditRevisions(unsigned long long handle);
    char* DocumentGetAuditRevision(unsigned long long handle, unsigned int revisionID);
    char* DocumentGetRevisionDetails(unsigned long long handle, unsigned int revisionID);
    char* DocumentGetDataObjectAuditHistory(unsigned long long handle, unsigned int dataObjectID);
    char* DocumentGetDataAttributeAuditHistory(unsigned long long handle, unsigned int dataAttributeID);
    char* DocumentGetTagAuditHistory(unsigned long long handle, unsigned int tagID);
    char* DocumentGetDataObjectAuditsByRevision(unsigned long long handle, unsigned int revisionID);
    char* DocumentGetDataAttributeAuditsByRevision(unsigned long long handle, unsigned int revisionID);
    char* DocumentGetTagAuditsByRevision(unsigned long long handle, unsigned int revisionID);

    // Note Operations
    char* DocumentGetAllNotes(unsigned long long handle);
    char* DocumentGetNotesByDataObjectID(unsigned long long handle, unsigned long long dataObjectID);
    char* DocumentGetNotesByDataAttributeID(unsigned long long handle, unsigned long long dataAttributeID);
    unsigned long long DocumentCreateNote(unsigned long long handle, const char* noteJSON);
    int DocumentUpdateNote(unsigned long long handle, const char* noteJSON);
    int DocumentDeleteNote(unsigned long long handle, unsigned long long noteID);
    char* DocumentGetNoteByUUID(unsigned long long handle, const char* uuid);
    char* DocumentGetNotesByType(unsigned long long handle, const char* noteType);
    char* DocumentGetNotesByGroupUUID(unsigned long long handle, const char* groupUUID);
    char* DocumentGetRootNotes(unsigned long long handle);
    char* DocumentGetChildNotes(unsigned long long handle, unsigned long long parentNoteID);

    // Labelling cache operations
    int PreloadForLabelling(unsigned long long handle);
    int ClearLabellingCache(unsigned long long handle);
    int PreloadBboxesOnly(unsigned long long handle);
    void ClearBboxCache(unsigned long long handle);

    // Line processing operations
    int UpdateDocumentLines(unsigned long long handle, double overlapPercentage);
    int CacheDocument(unsigned long long handle);

    // Transaction operations
    int BeginTransaction(unsigned long long handle);
    int CommitTransaction(unsigned long long handle);
    int RollbackTransaction(unsigned long long handle);

    // Additional Document methods (previously unexposed Go methods)
    unsigned long long* GetTaggedNodesByTagUUID(unsigned long long docHandle, const char* tagUUID, int* outCount);
    unsigned long long GetNodeByNumericID(unsigned long long docHandle, unsigned long long nodeID);
    long long GetNodeCountByTypeName(unsigned long long docHandle, const char* typeName);
    char* GetFeatureTypesWithCounts(unsigned long long docHandle);
    char* GetNodeTypesWithCounts(unsigned long long docHandle);
    int ReplaceAllExceptions(unsigned long long docHandle, const char* exceptionsJSON);
    char* GetTagsByPrefix(unsigned long long docHandle, const char* prefix);
    int CreateDataException(unsigned long long docHandle, const char* exceptionJSON);
    char* GetDataObjectsByParentID(unsigned long long docHandle, unsigned long long parentID);
    char* GetAllFeatures(unsigned long long docHandle);
    char* GetDocumentFilename(unsigned long long docHandle);
    int ClearTagsFromNodesByType(unsigned long long docHandle, const char* typeName);

    // Additional ContentNode methods (previously unexposed Go methods)
    int HasNextNode(unsigned long long nodeHandle, const char* nodeTypeRegex, int skipVirtual);
    int HasPreviousNode(unsigned long long nodeHandle, const char* nodeTypeRegex, int skipVirtual);
    int GetFirstChildIndex(unsigned long long nodeHandle);
    int GetLastChildIndex(unsigned long long nodeHandle);
    unsigned long long GetNodeAtChildIndex(unsigned long long nodeHandle, int index);
    unsigned long long AddChildContent(unsigned long long nodeHandle, const char* nodeType, const char* content, int index);
    unsigned long long* GetNodeAncestors(unsigned long long nodeHandle, int* outCount);
    unsigned long long* GetNodeDescendants(unsigned long long nodeHandle, int* outCount);
""")


def _get_platform_dir() -> str:
    """Get the platform-specific directory name (e.g., 'linux-amd64', 'darwin-arm64')."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Normalize OS names
    if system == "windows":
        os_name = "windows"
    elif system == "darwin":
        os_name = "darwin"
    else:
        os_name = "linux"

    # Normalize architecture names
    if machine in ("x86_64", "amd64"):
        arch_name = "amd64"
    elif machine in ("arm64", "aarch64"):
        arch_name = "arm64"
    elif machine in ("i386", "i686"):
        arch_name = "386"
    else:
        arch_name = machine

    return f"{os_name}-{arch_name}"


def _find_library() -> str:
    """Find the shared library in expected locations."""
    # First, look for bundled library in the package (for wheels)
    package_dir = Path(__file__).parent
    # _native is now inside the kodexa_document package
    native_dir = package_dir / "_native"

    # Library names for different platforms
    system = platform.system()
    machine = platform.machine()

    if system == "Windows":
        lib_names = ["kodexa_go.dll", "libkodexa_go.dll"]
        lib_ext = "dll"
    elif system == "Darwin":
        lib_names = ["libkodexa_go.dylib", "kodexa_go.dylib"]
        lib_ext = "dylib"
    else:  # Linux and others
        if IS_LAMBDA:
            lib_names = ["kodexa_go_lambda.so", "kodexa_go.so", "libkodexa_go.so"]
        else:
            lib_names = ["libkodexa_go.so", "kodexa_go.so"]
        lib_ext = "so"

    # Get platform-specific directory (e.g., "linux-amd64", "darwin-arm64")
    platform_dir = _get_platform_dir()

    # Check platform-specific subdirectory first (for universal wheels)
    platform_native_dir = native_dir / platform_dir
    if platform_native_dir.exists():
        for lib_name in lib_names:
            lib_path = platform_native_dir / lib_name
            if lib_path.exists():
                return str(lib_path)

    # Check bundled native directory directly (legacy layout)
    if native_dir.exists():
        for lib_name in lib_names:
            lib_path = native_dir / lib_name
            if lib_path.exists():
                return str(lib_path)
    
    # Check in the same directory as this module (for development)
    for lib_name in lib_names:
        lib_path = package_dir / lib_name
        if lib_path.exists():
            return str(lib_path)
    
    # Check system library paths
    for lib_name in lib_names:
        # Try to load from system paths (LD_LIBRARY_PATH, etc.)
        try:
            # This will raise an exception if not found
            return lib_name
        except:
            continue
    
    # Build path to the Go lib directory for development
    go_lib_dir = package_dir.parent.parent / "lib" / "go"
    if go_lib_dir.exists():
        for lib_name in lib_names:
            lib_path = go_lib_dir / lib_name
            if lib_path.exists():
                return str(lib_path)
    
    # If we're in development, try the Go build output
    if system == "Linux":
        dev_paths = [
            "../../lib/go/linux_amd64.so",
            "../go/linux_amd64.so",
        ]
    elif system == "Darwin":
        if machine == "arm64":
            dev_paths = [
                "../../lib/go/darwin_arm64.dylib",
                "../go/darwin_arm64.dylib",
            ]
        else:
            dev_paths = [
                "../../lib/go/darwin_amd64.dylib", 
                "../go/darwin_amd64.dylib",
            ]
    else:  # Windows
        dev_paths = [
            "../../lib/go/windows_amd64.dll",
            "../go/windows_amd64.dll",
        ]
    
    for dev_path in dev_paths:
        full_path = package_dir / dev_path
        if full_path.exists():
            return str(full_path.resolve())
    
    # NOTE: lib/python is OUTDATED and should not be used
    # The Go bindings are built to lib/python/_native/
    
    raise RuntimeError(
        f"Kodexa Go native library not found for platform {system} {machine}. "
        f"Searched in: {native_dir}, {package_dir}, and system paths. "
        f"Expected library names: {lib_names}. "
        f"Run 'cd lib/go && make linux' to build the library."
    )


def _load_library():
    """Load the appropriate native library for this platform."""
    lib_path = _find_library()

    # Disable SIGPROF to prevent Go/Python CGO deadlocks.
    # The Go runtime uses SIGPROF for profiling, which can cause deadlocks
    # when the signal arrives on a C/Python thread.
    # See: .work/go-python-deadlock-fixes.md for full explanation
    try:
        # Disable the profiling interval timer to prevent SIGPROF signals
        signal.setitimer(signal.ITIMER_PROF, 0)
        # Block SIGPROF from being delivered
        signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGPROF])
    except (AttributeError, OSError):
        # setitimer/pthread_sigmask not available on all platforms (e.g., Windows)
        pass

    try:
        return ffi.dlopen(lib_path)
    except OSError as e:
        raise RuntimeError(
            f"Failed to load Kodexa Go native library from {lib_path}: {e}. "
            f"Platform: {platform.system()} {platform.machine()}, "
            f"Python: {sys.version}, "
            f"Is Lambda: {IS_LAMBDA}"
        ) from e


# Global library instance
_lib: Optional[object] = None


def get_library():
    """Get the loaded native library instance."""
    global _lib
    if _lib is None:
        _lib = _load_library()

        # Verify the library loaded correctly by calling a simple function
        try:
            version_ptr = _lib.GetLibraryVersion()
            try:
                version = ffi.string(version_ptr).decode('utf-8')
                print(f"Loaded Kodexa Go library version: {version}")
            finally:
                if version_ptr != ffi.NULL:
                    _lib.FreeString(version_ptr)

            # Check if Lambda detection matches
            is_lambda_lib = bool(_lib.IsLambdaEnvironment())
            if is_lambda_lib != IS_LAMBDA:
                print(f"Warning: Lambda detection mismatch - Python: {IS_LAMBDA}, Library: {is_lambda_lib}")

        except Exception as e:
            raise RuntimeError(f"Failed to verify library functionality: {e}") from e

    return _lib


class _LazyLibrary:
    """Lazy proxy for the native library - only loads when first accessed."""

    def __getattr__(self, name):
        return getattr(get_library(), name)


# Export lazy proxy - library only loads when first function is called
lib = _LazyLibrary()