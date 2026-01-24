/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

#include "types_structs_macros.h"

// From https://gcc.gnu.org/onlinedocs/cpp/Stringizing.html
#define xstr(a) str(a)
#define str(a) #a

long TANGO_VERSION_HEX;

// Some internal constants were removed from cppTango in 9.4. To support both
// 9.4 and previous versions we must export constants conditionally, skipping
// the ones that are no longer available in cppTango. For each constant that
// could missing we must define a dummy fallback value of the type specified
// below, in the global namespace. This type is later used to detect missing
// constants using a template specialization.
struct PyTangoFallbackConstant {
};

[[maybe_unused]] static const PyTangoFallbackConstant MIN_POLL_PERIOD;
static const PyTangoFallbackConstant DELTA_T;
static const PyTangoFallbackConstant MIN_DELTA_WORK;
static const PyTangoFallbackConstant TIME_HEARTBEAT;
static const PyTangoFallbackConstant POLL_LOOP_NB;
static const PyTangoFallbackConstant ONE_SECOND;
static const PyTangoFallbackConstant DISCARD_THRESHOLD;

static const PyTangoFallbackConstant DELTA_PERIODIC;
static const PyTangoFallbackConstant DELTA_PERIODIC_LONG;

static const PyTangoFallbackConstant RECONNECTION_DELAY;

template <typename T>
static void export_conditionally(py::module &consts_module, const char *name, T value) {
    consts_module.attr(name) = value;
}

template <>
void export_conditionally(py::module & /*consts_module*/, const char * /*name*/, PyTangoFallbackConstant) {
    // Do nothing for missing constants.
}

namespace Tango {
static void export_optional_constants(py::module &consts_module) {
    // This function must be defined in the Tango namespace and all constants
    // must be referenced using unqualified names. They are resolved either to
    // the proper constants provided by cppTango (if exist) or to the fallback
    // values defined in this file.

    //
    // Some general interest define
    //
    export_conditionally(consts_module, "DELTA_T", DELTA_T);
    export_conditionally(consts_module, "DELTA_T", DELTA_T);
    export_conditionally(consts_module, "MIN_DELTA_WORK", MIN_DELTA_WORK);
    export_conditionally(consts_module, "TIME_HEARTBEAT", TIME_HEARTBEAT);
    export_conditionally(consts_module, "POLL_LOOP_NB", POLL_LOOP_NB);
    export_conditionally(consts_module, "ONE_SECOND", ONE_SECOND);
    export_conditionally(consts_module, "DISCARD_THRESHOLD", DISCARD_THRESHOLD);

    //
    // Event related define
    //
    export_conditionally(consts_module, "DELTA_PERIODIC", DELTA_PERIODIC);
    export_conditionally(consts_module, "DELTA_PERIODIC_LONG", DELTA_PERIODIC_LONG);

    //
    // Time to wait before trying to reconnect after
    // a connevtion failure
    //
    export_conditionally(consts_module, "RECONNECTION_DELAY", RECONNECTION_DELAY);
}
} // namespace Tango

void export_constants(py::module &m) {
    PyObject *py_constants_module = PyImport_AddModule("tango.constants");

    if(py_constants_module == nullptr) {
        throw std::runtime_error("Failed to create or access 'tango.constants' module");
    }

    py::module consts_module = py::reinterpret_borrow<py::module>(py_constants_module);
    m.attr("constants") = consts_module;

    consts_module.attr("__doc__") = "module containing several Tango constants.\n\nNew in PyTango 7.0.0";

    consts_module.attr("NUMPY_VERSION") = xstr(PYTANGO_NUMPY_VERSION);

    consts_module.attr("PYBIND11_VERSION_MAJOR") = PYBIND11_VERSION_MAJOR;
    consts_module.attr("PYBIND11_VERSION_MINOR") = PYBIND11_VERSION_MINOR;
    consts_module.attr("PYBIND11_VERSION_PATCH") = xstr(PYBIND11_VERSION_PATCH);

    consts_module.attr("PY_MAJOR_VERSION") = PY_MAJOR_VERSION;
    consts_module.attr("PY_MINOR_VERSION") = PY_MINOR_VERSION;
    consts_module.attr("PY_MICRO_VERSION") = PY_MICRO_VERSION;
    consts_module.attr("PY_VERSION") = PY_VERSION;
    consts_module.attr("PY_VERSION_HEX") = PY_VERSION_HEX;

    //
    // From tango_const.h
    //

    Tango::export_optional_constants(consts_module);

    //
    // Some general interest define
    //
    consts_module.attr("TANGO_VERSION_MAJOR") = TANGO_VERSION_MAJOR;
    consts_module.attr("TANGO_VERSION_MINOR") = TANGO_VERSION_MINOR;
    consts_module.attr("TANGO_VERSION_PATCH") = TANGO_VERSION_PATCH;
    consts_module.attr("TANGO_VERSION_NB") = TANGO_VERSION_NB;
    consts_module.attr("TANGO_VERSION") = Tango::TgLibVers;

    consts_module.attr("TgLibVers") = Tango::TgLibVers;
    consts_module.attr("TgLibMajorVers") = Tango::TgLibMajorVers;
    consts_module.attr("TgLibVersNb") = Tango::TgLibVersNb;
    consts_module.attr("DevVersion") = Tango::DevVersion;
    consts_module.attr("DefaultMaxSeq") = Tango::DefaultMaxSeq;
    consts_module.attr("DefaultBlackBoxDepth") = Tango::DefaultBlackBoxDepth;
    consts_module.attr("DefaultPollRingDepth") = Tango::DefaultPollRingDepth;

    consts_module.attr("InitialOutput") = Tango::InitialOutput;
    consts_module.attr("DSDeviceDomain") = Tango::DSDeviceDomain;
    consts_module.attr("DefaultDocUrl") = Tango::DefaultDocUrl;
    consts_module.attr("EnvVariable") = Tango::EnvVariable;
    consts_module.attr("WindowsEnvVariable") = Tango::WindowsEnvVariable;
    consts_module.attr("DbObjName") = Tango::DbObjName;

    consts_module.attr("NotSet") = Tango::NotSet;
    // Changed in tango 8 from DescNotSet to NotSet. We keep the old constant
    // to try to maintain backward compatibility
    consts_module.attr("DescNotSet") = Tango::NotSet;

    consts_module.attr("ResNotDefined") = Tango::ResNotDefined;
    consts_module.attr("MessBoxTitle") = Tango::MessBoxTitle;
    consts_module.attr("StatusNotSet") = Tango::StatusNotSet;
    consts_module.attr("TangoHostNotSet") = Tango::TangoHostNotSet;
    consts_module.attr("RootAttNotDef") = Tango::RootAttNotDef;

    consts_module.attr("DefaultWritAttrProp") = Tango::DefaultWritAttrProp;
    consts_module.attr("AllAttr") = Tango::AllAttr;
    consts_module.attr("AllAttr_3") = Tango::AllAttr_3;
    consts_module.attr("AllCmd") = Tango::AllCmd;

    consts_module.attr("PollCommand") = Tango::PollCommand;
    consts_module.attr("PollAttribute") = Tango::PollAttribute;

    consts_module.attr("LOCAL_POLL_REQUEST") = Tango::LOCAL_POLL_REQUEST;
    consts_module.attr("LOCAL_REQUEST_STR_SIZE") = Tango::LOCAL_REQUEST_STR_SIZE;

    consts_module.attr("MIN_POLL_PERIOD") = Tango::MIN_POLL_PERIOD;

    consts_module.attr("DEFAULT_TIMEOUT") = Tango::DEFAULT_TIMEOUT;
    consts_module.attr("DEFAULT_POLL_OLD_FACTOR") = Tango::DEFAULT_POLL_OLD_FACTOR;

    consts_module.attr("TG_IMP_MINOR_TO") = Tango::TG_IMP_MINOR_TO;
    consts_module.attr("TG_IMP_MINOR_DEVFAILED") = Tango::TG_IMP_MINOR_DEVFAILED;
    consts_module.attr("TG_IMP_MINOR_NON_DEVFAILED") = Tango::TG_IMP_MINOR_NON_DEVFAILED;

    consts_module.attr("TANGO_PY_MOD_NAME") = Tango::TANGO_PY_MOD_NAME;
    consts_module.attr("DATABASE_CLASS") = Tango::DATABASE_CLASS;

    consts_module.attr("TANGO_FLOAT_PRECISION") = Tango::TANGO_FLOAT_PRECISION;
    consts_module.attr("NoClass") = Tango::NoClass;

    //
    // Event related define
    //

    consts_module.attr("EVENT_HEARTBEAT_PERIOD") = Tango::EVENT_HEARTBEAT_PERIOD;
    consts_module.attr("EVENT_RESUBSCRIBE_PERIOD") = Tango::EVENT_RESUBSCRIBE_PERIOD;
    consts_module.attr("DEFAULT_EVENT_PERIOD") = Tango::DEFAULT_EVENT_PERIOD;
    consts_module.attr("HEARTBEAT") = Tango::HEARTBEAT;

    //
    // ZMQ event system related define
    //
    consts_module.attr("ZMQ_EVENT_PROT_VERSION") = Tango::ZMQ_EVENT_PROT_VERSION;
    consts_module.attr("HEARTBEAT_METHOD_NAME") = Tango::HEARTBEAT_METHOD_NAME;
    consts_module.attr("EVENT_METHOD_NAME") = Tango::EVENT_METHOD_NAME;
    consts_module.attr("HEARTBEAT_EVENT_NAME") = Tango::HEARTBEAT_EVENT_NAME;
    consts_module.attr("CTRL_SOCK_ENDPOINT") = Tango::CTRL_SOCK_ENDPOINT;
    consts_module.attr("MCAST_PROT") = Tango::MCAST_PROT;
    consts_module.attr("MCAST_HOPS") = Tango::MCAST_HOPS;
    consts_module.attr("PGM_RATE") = Tango::PGM_RATE;
    consts_module.attr("PGM_IVL") = Tango::PGM_IVL;
    consts_module.attr("MAX_SOCKET_SUB") = Tango::MAX_SOCKET_SUB;
    consts_module.attr("PUB_HWM") = Tango::PUB_HWM;
    consts_module.attr("SUB_HWM") = Tango::SUB_HWM;
    consts_module.attr("SUB_SEND_HWM") = Tango::SUB_SEND_HWM;

    consts_module.attr("NOTIFD_CHANNEL") = Tango::NOTIFD_CHANNEL;

    //
    // Locking feature related defines
    //

    consts_module.attr("DEFAULT_LOCK_VALIDITY") = Tango::DEFAULT_LOCK_VALIDITY;
    consts_module.attr("DEVICE_UNLOCKED_REASON") = Tango::DEVICE_UNLOCKED_REASON;
    consts_module.attr("MIN_LOCK_VALIDITY") = Tango::MIN_LOCK_VALIDITY;
    consts_module.attr("TG_LOCAL_HOST") = Tango::TG_LOCAL_HOST;

    //
    // Client timeout as defined by omniORB4.0.0
    //

    consts_module.attr("CLNT_TIMEOUT_STR") = Tango::CLNT_TIMEOUT_STR;
    consts_module.attr("CLNT_TIMEOUT") = Tango::CLNT_TIMEOUT;
    consts_module.attr("NARROW_CLNT_TIMEOUT") = Tango::NARROW_CLNT_TIMEOUT;

    //
    // Connection and call timeout for database device
    //

    consts_module.attr("DB_CONNECT_TIMEOUT") = Tango::DB_CONNECT_TIMEOUT;
    consts_module.attr("DB_RECONNECT_TIMEOUT") = Tango::DB_RECONNECT_TIMEOUT;
    consts_module.attr("DB_TIMEOUT") = Tango::DB_TIMEOUT;
    consts_module.attr("DB_START_PHASE_RETRIES") = Tango::DB_START_PHASE_RETRIES;

    //
    // Access Control related defines
    // WARNING: these string are also used within the Db stored procedure
    // introduced in Tango V6.1. If you change it here, don't forget to
    // also update the stored procedure
    //

    consts_module.attr("CONTROL_SYSTEM") = Tango::CONTROL_SYSTEM;
    consts_module.attr("SERVICE_PROP_NAME") = Tango::SERVICE_PROP_NAME;
    consts_module.attr("ACCESS_SERVICE") = Tango::ACCESS_SERVICE;

    //
    // Polling threads pool related defines
    //

    consts_module.attr("DEFAULT_POLLING_THREADS_POOL_SIZE") = Tango::DEFAULT_POLLING_THREADS_POOL_SIZE;

    //
    // Max transfer size 256 MBytes (in byte). Needed by omniORB
    //

    consts_module.attr("MAX_TRANSFER_SIZE") = Tango::MAX_TRANSFER_SIZE;

    //
    // Max GIOP connection per server . Needed by omniORB
    //

    consts_module.attr("MAX_GIOP_PER_SERVER") = Tango::MAX_GIOP_PER_SERVER;

    //
    // Telemetry related defines
    //

#if defined(TANGO_USE_TELEMETRY)
    consts_module.attr("TELEMETRY_SUPPORTED") = true;
#else
    consts_module.attr("TELEMETRY_SUPPORTED") = false;
#endif

    //
    // Tango name length
    //

    consts_module.attr("MaxServerNameLength") = Tango::MaxServerNameLength;
    consts_module.attr("MaxDevPropLength") = Tango::MaxDevPropLength;

    //
    // For forwarded attribute implementation
    //
    consts_module.attr("MIN_IDL_CONF5") = Tango::MIN_IDL_CONF5;
    consts_module.attr("MIN_IDL_DEV_INTR") = Tango::MIN_IDL_DEV_INTR;
    consts_module.attr("ALL_EVENTS") = Tango::ALL_EVENTS;

    // --------------------------------------------------------

    //
    // Files used to retrieve env. variables
    //

    consts_module.attr("USER_ENV_VAR_FILE") = Tango::USER_ENV_VAR_FILE;

    consts_module.attr("kLogTargetConsole") = Tango::kLogTargetConsole;
    consts_module.attr("kLogTargetFile") = Tango::kLogTargetFile;
    consts_module.attr("kLogTargetDevice") = Tango::kLogTargetDevice;
    consts_module.attr("kLogTargetSep") = Tango::kLogTargetSep;

    consts_module.attr("AlrmValueNotSpec") = Tango::AlrmValueNotSpec;
    consts_module.attr("AssocWritNotSpec") = Tango::AssocWritNotSpec;
    consts_module.attr("LabelNotSpec") = Tango::LabelNotSpec;
    consts_module.attr("DescNotSpec") = Tango::DescNotSpec;
    consts_module.attr("UnitNotSpec") = Tango::UnitNotSpec;
    consts_module.attr("StdUnitNotSpec") = Tango::StdUnitNotSpec;
    consts_module.attr("DispUnitNotSpec") = Tango::DispUnitNotSpec;
#ifdef FormatNotSpec
    consts_module.attr("FormatNotSpec") = Tango::FormatNotSpec;
#else
    consts_module.attr("FormatNotSpec") = Tango::FormatNotSpec_FL;
#endif
    consts_module.attr("FormatNotSpec_FL") = Tango::FormatNotSpec_FL;
    consts_module.attr("FormatNotSpec_INT") = Tango::FormatNotSpec_INT;
    consts_module.attr("FormatNotSpec_STR") = Tango::FormatNotSpec_STR;

    consts_module.attr("NotANumber") = Tango::NotANumber;
    consts_module.attr("MemNotUsed") = Tango::MemNotUsed;
    consts_module.attr("MemAttrPropName") = Tango::MemAttrPropName;

    consts_module.attr("API_AttrConfig") = Tango::API_AttrConfig;
    consts_module.attr("API_AttrEventProp") = Tango::API_AttrEventProp;
    consts_module.attr("API_AttrIncorrectDataNumber") = Tango::API_AttrIncorrectDataNumber;
    consts_module.attr("API_AttrNoAlarm") = Tango::API_AttrNoAlarm;
    consts_module.attr("API_AttrNotAllowed") = Tango::API_AttrNotAllowed;
    consts_module.attr("API_AttrNotFound") = Tango::API_AttrNotFound;
    consts_module.attr("API_AttrNotWritable") = Tango::API_AttrNotWritable;
    consts_module.attr("API_AttrOptProp") = Tango::API_AttrOptProp;
    consts_module.attr("API_AttrPropValueNotSet") = Tango::API_AttrPropValueNotSet;
    consts_module.attr("API_AttrValueNotSet") = Tango::API_AttrValueNotSet;
    consts_module.attr("API_AttrWrongDefined") = Tango::API_AttrWrongDefined;
    consts_module.attr("API_AttrWrongMemValue") = Tango::API_AttrWrongMemValue;
    consts_module.attr("API_BadConfigurationProperty") = Tango::API_BadConfigurationProperty;
    consts_module.attr("API_BlackBoxArgument") = Tango::API_BlackBoxArgument;
    consts_module.attr("API_BlackBoxEmpty") = Tango::API_BlackBoxEmpty;
    consts_module.attr("API_CannotCheckAccessControl") = Tango::API_CannotCheckAccessControl;
    consts_module.attr("API_CannotOpenFile") = Tango::API_CannotOpenFile;
    consts_module.attr("API_CantActivatePOAManager") = Tango::API_CantActivatePOAManager;
    consts_module.attr("API_CantCreateClassPoa") = Tango::API_CantCreateClassPoa;
    consts_module.attr("API_CantCreateLockingThread") = Tango::API_CantCreateLockingThread;
    consts_module.attr("API_CantFindLockingThread") = Tango::API_CantFindLockingThread;
    consts_module.attr("API_CantGetClientIdent") = Tango::API_CantGetClientIdent;
    consts_module.attr("API_CantGetDevObjectId") = Tango::API_CantGetDevObjectId;
    consts_module.attr("API_CantInstallSignal") = Tango::API_CantInstallSignal;
    consts_module.attr("API_CantRetrieveClass") = Tango::API_CantRetrieveClass;
    consts_module.attr("API_CantRetrieveClassList") = Tango::API_CantRetrieveClassList;
    consts_module.attr("API_CantStoreDeviceClass") = Tango::API_CantStoreDeviceClass;
    consts_module.attr("API_ClassNotFound") = Tango::API_ClassNotFound;
    consts_module.attr("API_CmdArgumentTypeNotSupported") = Tango::API_CmdArgumentTypeNotSupported;
    consts_module.attr("API_CommandNotAllowed") = Tango::API_CommandNotAllowed;
    consts_module.attr("API_CommandNotFound") = Tango::API_CommandNotFound;
    consts_module.attr("API_CorbaSysException") = Tango::API_CorbaSysException;
    consts_module.attr("API_CorruptedDatabase") = Tango::API_CorruptedDatabase;
    consts_module.attr("API_DatabaseAccess") = Tango::API_DatabaseAccess;
    consts_module.attr("API_DeviceLocked") = Tango::API_DeviceLocked;
    consts_module.attr("API_DeviceNotFound") = Tango::API_DeviceNotFound;
    consts_module.attr("API_DeviceNotLocked") = Tango::API_DeviceNotLocked;
    consts_module.attr("API_DeviceUnlockable") = Tango::API_DeviceUnlockable;
    consts_module.attr("API_DeviceUnlocked") = Tango::API_DeviceUnlocked;
    consts_module.attr("API_EventSupplierNotConstructed") = Tango::API_EventSupplierNotConstructed;
    consts_module.attr("API_IncoherentDbData") = Tango::API_IncoherentDbData;
    consts_module.attr("API_IncoherentDevData") = Tango::API_IncoherentDevData;
    consts_module.attr("API_IncoherentValues") = Tango::API_IncoherentValues;
    consts_module.attr("API_IncompatibleAttrDataType") = Tango::API_IncompatibleAttrDataType;
    consts_module.attr("API_IncompatibleCmdArgumentType") = Tango::API_IncompatibleCmdArgumentType;
    consts_module.attr("API_InitMethodNotFound") = Tango::API_InitMethodNotFound;
    consts_module.attr("API_InitNotPublic") = Tango::API_InitNotPublic;
    consts_module.attr("API_InitThrowsException") = Tango::API_InitThrowsException;
    consts_module.attr("API_JavaRuntimeSecurityException") = Tango::API_JavaRuntimeSecurityException;
    consts_module.attr("API_MemoryAllocation") = Tango::API_MemoryAllocation;
    consts_module.attr("API_MethodArgument") = Tango::API_MethodArgument;
    consts_module.attr("API_MethodNotFound") = Tango::API_MethodNotFound;
    consts_module.attr("API_MissedEvents") = Tango::API_MissedEvents;
    consts_module.attr("API_NotSupportedFeature") = Tango::API_NotSupportedFeature;
    consts_module.attr("API_NtDebugWindowError") = Tango::API_NtDebugWindowError;
    consts_module.attr("API_OverloadingNotSupported") = Tango::API_OverloadingNotSupported;
    consts_module.attr("API_PolledDeviceNotInPoolConf") = Tango::API_PolledDeviceNotInPoolConf;
    consts_module.attr("API_PolledDeviceNotInPoolMap") = Tango::API_PolledDeviceNotInPoolMap;
    consts_module.attr("API_PollingThreadNotFound") = Tango::API_PollingThreadNotFound;
    consts_module.attr("API_ReadOnlyMode") = Tango::API_ReadOnlyMode;
    consts_module.attr("API_SignalOutOfRange") = Tango::API_SignalOutOfRange;
    consts_module.attr("API_SystemCallFailed") = Tango::API_SystemCallFailed;
    consts_module.attr("API_WAttrOutsideLimit") = Tango::API_WAttrOutsideLimit;
    consts_module.attr("API_WizardConfError") = Tango::API_WizardConfError;
    consts_module.attr("API_WrongEventData") = Tango::API_WrongEventData;
    consts_module.attr("API_WrongHistoryDataBuffer") = Tango::API_WrongHistoryDataBuffer;
    consts_module.attr("API_WrongLockingStatus") = Tango::API_WrongLockingStatus;
    consts_module.attr("API_ZmqInitFailed") = Tango::API_ZmqInitFailed;
}
