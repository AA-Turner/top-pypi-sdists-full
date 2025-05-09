use core::{
    ffi::{c_int, c_void, CStr},
    mem,
    ptr::{self, null_mut as NULL},
};
use pyo3_ffi::*;
use std::{path::PathBuf, time::SystemTime};

use crate::common::*;

// For benchmarking, all modules are public. The crate itself isn't distributed as a library,
// but is only meant to be accessed through its Python API.
pub mod common;
pub mod date;
pub mod date_delta;
pub mod datetime_delta;
pub mod round;
#[rustfmt::skip] // this module is autogenerated. No need to format it.
pub mod docstrings;
pub mod instant;
pub mod monthday;
pub mod offset_datetime;
pub mod plain_datetime;
pub mod system_datetime;
pub mod time;
pub mod time_delta;
pub mod tz;
pub mod yearmonth;
pub mod zoned_datetime;

use common::math::*;
use date::unpickle as _unpkl_date;
use date_delta::unpickle as _unpkl_ddelta;
use date_delta::{days, months, weeks, years};
use datetime_delta::unpickle as _unpkl_dtdelta;
use docstrings as doc;
use instant::{unpickle as _unpkl_inst, unpickle_v07 as _unpkl_utc, Instant};
use monthday::unpickle as _unpkl_md;
use offset_datetime::unpickle as _unpkl_offset;
use plain_datetime::unpickle as _unpkl_local;
use system_datetime::unpickle as _unpkl_system;
use time::unpickle as _unpkl_time;
use time_delta::unpickle as _unpkl_tdelta;
use time_delta::{hours, microseconds, milliseconds, minutes, nanoseconds, seconds};
use tz::cache::TZifCache;
use yearmonth::unpickle as _unpkl_ym;
use zoned_datetime::unpickle as _unpkl_zoned;

#[allow(static_mut_refs)]
static mut MODULE_DEF: PyModuleDef = PyModuleDef {
    m_base: PyModuleDef_HEAD_INIT,
    m_name: c"whenever".as_ptr(),
    m_doc: c"Modern datetime library for Python".as_ptr(),
    m_size: mem::size_of::<State>() as _,
    m_methods: unsafe { METHODS.as_ptr() as *mut _ },
    m_slots: unsafe { MODULE_SLOTS.as_ptr() as *mut _ },
    m_traverse: Some(module_traverse),
    m_clear: Some(module_clear),
    m_free: Some(module_free),
};

static mut METHODS: &[PyMethodDef] = &[
    method!(_unpkl_date, c"", METH_O),
    method!(_unpkl_ym, c"", METH_O),
    method!(_unpkl_md, c"", METH_O),
    method!(_unpkl_time, c"", METH_O),
    method_vararg!(_unpkl_ddelta, c""),
    method!(_unpkl_tdelta, c"", METH_O),
    method_vararg!(_unpkl_dtdelta, c""),
    method!(_unpkl_local, c"", METH_O),
    method!(_unpkl_inst, c"", METH_O),
    method!(_unpkl_utc, c"", METH_O), // for backwards compatibility
    method!(_unpkl_offset, c"", METH_O),
    method_vararg!(_unpkl_zoned, c""),
    method!(_unpkl_system, c"", METH_O),
    // FUTURE: set __module__ on these
    method!(years, doc::YEARS, METH_O),
    method!(months, doc::MONTHS, METH_O),
    method!(weeks, doc::WEEKS, METH_O),
    method!(days, doc::DAYS, METH_O),
    method!(hours, doc::HOURS, METH_O),
    method!(minutes, doc::MINUTES, METH_O),
    method!(seconds, doc::SECONDS, METH_O),
    method!(milliseconds, doc::MILLISECONDS, METH_O),
    method!(microseconds, doc::MICROSECONDS, METH_O),
    method!(nanoseconds, doc::NANOSECONDS, METH_O),
    method!(_patch_time_frozen, c"", METH_O),
    method!(_patch_time_keep_ticking, c"", METH_O),
    method!(_unpatch_time, c""),
    method!(_set_tzpath, c"", METH_O),
    method!(_clear_tz_cache, c""),
    method!(_clear_tz_cache_by_keys, c"", METH_O),
    PyMethodDef::zeroed(),
];

unsafe fn _patch_time_frozen(module: *mut PyObject, arg: *mut PyObject) -> PyReturn {
    _patch_time(module, arg, true)
}

unsafe fn _patch_time_keep_ticking(module: *mut PyObject, arg: *mut PyObject) -> PyReturn {
    _patch_time(module, arg, false)
}

unsafe fn _patch_time(module: *mut PyObject, arg: *mut PyObject, freeze: bool) -> PyReturn {
    let state: &mut State = PyModule_GetState(module).cast::<State>().as_mut().unwrap();
    if Py_TYPE(arg) != state.instant_type {
        raise_type_err("Expected an Instant")?
    }
    let instant = Instant::extract(arg);
    let pos_epoch = u64::try_from(instant.epoch.get())
        .ok()
        .ok_or_type_err("Can only set time after 1970")?;

    state.time_patch = if freeze {
        TimePatch::Frozen(instant)
    } else {
        TimePatch::KeepTicking {
            pin: std::time::Duration::new(pos_epoch, instant.subsec.get() as _),
            at: SystemTime::now()
                .duration_since(SystemTime::UNIX_EPOCH)
                .ok()
                .ok_or_type_err("System time before 1970")?,
        }
    };
    Py_None().as_result()
}

unsafe fn _unpatch_time(module: *mut PyObject, _: *mut PyObject) -> PyReturn {
    let state: &mut State = PyModule_GetState(module).cast::<State>().as_mut().unwrap();
    state.time_patch = TimePatch::Unset;
    Py_None().as_result()
}

pub(crate) unsafe fn _set_tzpath(module: *mut PyObject, to: *mut PyObject) -> PyReturn {
    let state = State::for_mod_mut(module);

    if PyTuple_CheckExact(to) == 0 {
        raise_type_err("Argument must be a tuple")?;
    }
    let size = PyTuple_GET_SIZE(to);
    let mut result = Vec::with_capacity(size as _);

    for i in 0..size {
        let path = PyTuple_GET_ITEM(to, i);
        result.push(PathBuf::from(
            path.to_str()?.ok_or_type_err("Path must be a string")?,
        ))
    }
    state.tz_cache.paths = result;
    Py_None().as_result()
}

pub(crate) unsafe fn _clear_tz_cache(module: *mut PyObject, _: *mut PyObject) -> PyReturn {
    let state = State::for_mod_mut(module);
    state.tz_cache.clear_all();
    Py_None().as_result()
}

pub(crate) unsafe fn _clear_tz_cache_by_keys(
    module: *mut PyObject,
    keys_obj: *mut PyObject,
) -> PyReturn {
    let state = State::for_mod_mut(module);
    if PyTuple_CheckExact(keys_obj) == 0 {
        raise_type_err("Argument must be a tuple")?;
    }
    let size = PyTuple_GET_SIZE(keys_obj);
    let mut keys = Vec::with_capacity(size as _);
    for i in 0..size {
        let path = PyTuple_GET_ITEM(keys_obj, i);
        keys.push(path.to_str()?.ok_or_type_err("Path must be a string")?)
    }
    state.tz_cache.clear_only(&keys);
    Py_None().as_result()
}

#[allow(non_upper_case_globals)]
#[allow(dead_code)]
const Py_mod_gil: c_int = 4;
#[allow(non_upper_case_globals)]
#[allow(dead_code)]
const Py_MOD_GIL_NOT_USED: *mut c_void = 1 as *mut c_void;

static mut MODULE_SLOTS: &[PyModuleDef_Slot] = &[
    PyModuleDef_Slot {
        slot: Py_mod_exec,
        value: module_exec as *mut c_void,
    },
    #[cfg(Py_3_13)]
    PyModuleDef_Slot {
        slot: Py_mod_multiple_interpreters,
        // awaiting https://github.com/python/cpython/pull/102995
        value: Py_MOD_PER_INTERPRETER_GIL_SUPPORTED,
    },
    // FUTURE: set this once we've ensured that:
    // - tz cache is threadsafe
    // - we safely handle non-threadsafe modules: datetime, zoneinfo
    // #[cfg(Py_3_13)]
    // PyModuleDef_Slot {
    //     slot: Py_mod_gil,
    //     value: Py_MOD_GIL_NOT_USED,
    // },
    PyModuleDef_Slot {
        slot: 0,
        value: NULL(),
    },
];

unsafe fn create_enum(name: &CStr, members: &[(&CStr, i32)]) -> PyReturn {
    let members_dict = PyDict_New().as_result()?;
    defer_decref!(members_dict);
    for &(key, value) in members {
        if PyDict_SetItemString(members_dict, key.as_ptr(), steal!(value.to_py()?)) == -1 {
            return Err(PyErrOccurred());
        }
    }
    let enum_module = PyImport_ImportModule(c"enum".as_ptr()).as_result()?;
    defer_decref!(enum_module);
    PyObject_CallMethod(
        enum_module,
        c"Enum".as_ptr(),
        c"sO".as_ptr(),
        name.as_ptr(),
        members_dict,
    )
    .as_result()
}

unsafe fn new_exc(
    module: *mut PyObject,
    name: &CStr,
    doc: &CStr,
    base: *mut PyObject,
) -> *mut PyObject {
    let e = PyErr_NewExceptionWithDoc(name.as_ptr(), doc.as_ptr(), base, NULL());
    if e.is_null() || PyModule_AddType(module, e.cast()) != 0 {
        return NULL();
    }
    e
}

// Return the new type and the unpickler function
unsafe fn new_type<T: PyWrapped>(
    module: *mut PyObject,
    module_nameobj: *mut PyObject,
    spec: *mut PyType_Spec,
    unpickle_name: &CStr,
    singletons: &[(&CStr, T)],
    type_ptr: *mut *mut PyTypeObject,
    unpickle_ptr: *mut *mut PyObject,
) -> bool {
    let cls: *mut PyTypeObject = PyType_FromModuleAndSpec(module, spec, ptr::null_mut()).cast();
    if cls.is_null() || PyModule_AddType(module, cls) != 0 {
        return false;
    }

    let unpickler = PyObject_GetAttrString(module, unpickle_name.as_ptr());
    defer_decref!(unpickler);
    if PyObject_SetAttrString(unpickler, c"__module__".as_ptr(), module_nameobj) != 0 {
        return false;
    }

    for (name, value) in singletons {
        let Some(pyvalue) = value.to_obj(cls).ok() else {
            return false;
        };
        defer_decref!(pyvalue);
        if PyDict_SetItemString((*cls).tp_dict, name.as_ptr(), pyvalue) != 0 {
            return false;
        }
    }
    (*type_ptr) = cls;
    (*unpickle_ptr) = unpickler;
    true
}

macro_rules! unwrap_or_errcode {
    ($expr:expr) => {
        match $expr {
            Ok(v) => v,
            Err(_) => return -1,
        }
    };
}

// Sets __module__ on <module>.<attrname> to <module_name>
unsafe fn patch_dunder_module(
    module: *mut PyObject,
    module_name: *mut PyObject,
    attrname: &CStr,
) -> bool {
    let obj = PyObject_GetAttrString(module, attrname.as_ptr());
    if obj.is_null() {
        return false;
    }
    defer_decref!(obj);
    if PyObject_SetAttrString(module, c"__module__".as_ptr(), module_name) != 0 {
        return false;
    }
    true
}

#[cold]
unsafe extern "C" fn module_exec(module: *mut PyObject) -> c_int {
    let state: &mut State = PyModule_GetState(module).cast::<State>().as_mut().unwrap();
    let module_name = unwrap_or_errcode!("whenever".to_py());
    defer_decref!(module_name);

    if !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(date::SPEC),
        c"_unpkl_date",
        date::SINGLETONS,
        ptr::addr_of_mut!(state.date_type),
        ptr::addr_of_mut!(state.unpickle_date),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(yearmonth::SPEC),
        c"_unpkl_ym",
        yearmonth::SINGLETONS,
        ptr::addr_of_mut!(state.yearmonth_type),
        ptr::addr_of_mut!(state.unpickle_yearmonth),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(monthday::SPEC),
        c"_unpkl_md",
        monthday::SINGLETONS,
        ptr::addr_of_mut!(state.monthday_type),
        ptr::addr_of_mut!(state.unpickle_monthday),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(time::SPEC),
        c"_unpkl_time",
        time::SINGLETONS,
        ptr::addr_of_mut!(state.time_type),
        ptr::addr_of_mut!(state.unpickle_time),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(date_delta::SPEC),
        c"_unpkl_ddelta",
        date_delta::SINGLETONS,
        ptr::addr_of_mut!(state.date_delta_type),
        ptr::addr_of_mut!(state.unpickle_date_delta),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(time_delta::SPEC),
        c"_unpkl_tdelta",
        time_delta::SINGLETONS,
        ptr::addr_of_mut!(state.time_delta_type),
        ptr::addr_of_mut!(state.unpickle_time_delta),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(datetime_delta::SPEC),
        c"_unpkl_dtdelta",
        datetime_delta::SINGLETONS,
        ptr::addr_of_mut!(state.datetime_delta_type),
        ptr::addr_of_mut!(state.unpickle_datetime_delta),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(plain_datetime::SPEC),
        c"_unpkl_local",
        plain_datetime::SINGLETONS,
        ptr::addr_of_mut!(state.plain_datetime_type),
        ptr::addr_of_mut!(state.unpickle_plain_datetime),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(instant::SPEC),
        c"_unpkl_inst",
        instant::SINGLETONS,
        ptr::addr_of_mut!(state.instant_type),
        ptr::addr_of_mut!(state.unpickle_instant),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(offset_datetime::SPEC),
        c"_unpkl_offset",
        offset_datetime::SINGLETONS,
        ptr::addr_of_mut!(state.offset_datetime_type),
        ptr::addr_of_mut!(state.unpickle_offset_datetime),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(zoned_datetime::SPEC),
        c"_unpkl_zoned",
        zoned_datetime::SINGLETONS,
        ptr::addr_of_mut!(state.zoned_datetime_type),
        ptr::addr_of_mut!(state.unpickle_zoned_datetime),
    ) || !new_type(
        module,
        module_name,
        ptr::addr_of_mut!(system_datetime::SPEC),
        c"_unpkl_system",
        system_datetime::SINGLETONS,
        ptr::addr_of_mut!(state.system_datetime_type),
        ptr::addr_of_mut!(state.unpickle_system_datetime),
    ) || !patch_dunder_module(module, module_name, c"_unpkl_utc")
    {
        return -1;
    }

    PyDateTime_IMPORT();
    state.py_api = match PyDateTimeAPI().as_ref() {
        Some(api) => api,
        None => return -1,
    };

    let datetime_module = PyImport_ImportModule(c"datetime".as_ptr());
    defer_decref!(datetime_module);
    state.strptime = PyObject_GetAttrString(
        steal!(PyObject_GetAttrString(
            datetime_module,
            c"datetime".as_ptr()
        )),
        c"strptime".as_ptr(),
    );
    state.timezone_type = PyObject_GetAttrString(datetime_module, c"timezone".as_ptr()).cast();

    state.time_ns = unwrap_or_errcode!(import_from(c"time", c"time_ns"));

    let weekday_enum = unwrap_or_errcode!(create_enum(
        c"Weekday",
        &[
            (c"MONDAY", 1),
            (c"TUESDAY", 2),
            (c"WEDNESDAY", 3),
            (c"THURSDAY", 4),
            (c"FRIDAY", 5),
            (c"SATURDAY", 6),
            (c"SUNDAY", 7),
        ],
    )) as *mut _;
    defer_decref!(weekday_enum);
    if PyModule_AddType(module, weekday_enum.cast()) != 0 {
        return -1;
    }

    state.weekday_enum_members = [
        PyObject_GetAttrString(weekday_enum, c"MONDAY".as_ptr()),
        PyObject_GetAttrString(weekday_enum, c"TUESDAY".as_ptr()),
        PyObject_GetAttrString(weekday_enum, c"WEDNESDAY".as_ptr()),
        PyObject_GetAttrString(weekday_enum, c"THURSDAY".as_ptr()),
        PyObject_GetAttrString(weekday_enum, c"FRIDAY".as_ptr()),
        PyObject_GetAttrString(weekday_enum, c"SATURDAY".as_ptr()),
        PyObject_GetAttrString(weekday_enum, c"SUNDAY".as_ptr()),
    ];

    state.str_years = PyUnicode_InternFromString(c"years".as_ptr());
    state.str_months = PyUnicode_InternFromString(c"months".as_ptr());
    state.str_weeks = PyUnicode_InternFromString(c"weeks".as_ptr());
    state.str_days = PyUnicode_InternFromString(c"days".as_ptr());
    state.str_hours = PyUnicode_InternFromString(c"hours".as_ptr());
    state.str_minutes = PyUnicode_InternFromString(c"minutes".as_ptr());
    state.str_seconds = PyUnicode_InternFromString(c"seconds".as_ptr());
    state.str_milliseconds = PyUnicode_InternFromString(c"milliseconds".as_ptr());
    state.str_microseconds = PyUnicode_InternFromString(c"microseconds".as_ptr());
    state.str_nanoseconds = PyUnicode_InternFromString(c"nanoseconds".as_ptr());
    state.str_year = PyUnicode_InternFromString(c"year".as_ptr());
    state.str_month = PyUnicode_InternFromString(c"month".as_ptr());
    state.str_day = PyUnicode_InternFromString(c"day".as_ptr());
    state.str_hour = PyUnicode_InternFromString(c"hour".as_ptr());
    state.str_minute = PyUnicode_InternFromString(c"minute".as_ptr());
    state.str_second = PyUnicode_InternFromString(c"second".as_ptr());
    state.str_millisecond = PyUnicode_InternFromString(c"millisecond".as_ptr());
    state.str_microsecond = PyUnicode_InternFromString(c"microsecond".as_ptr());
    state.str_nanosecond = PyUnicode_InternFromString(c"nanosecond".as_ptr());
    state.str_compatible = PyUnicode_InternFromString(c"compatible".as_ptr());
    state.str_raise = PyUnicode_InternFromString(c"raise".as_ptr());
    state.str_earlier = PyUnicode_InternFromString(c"earlier".as_ptr());
    state.str_later = PyUnicode_InternFromString(c"later".as_ptr());
    state.str_tz = PyUnicode_InternFromString(c"tz".as_ptr());
    state.str_disambiguate = PyUnicode_InternFromString(c"disambiguate".as_ptr());
    state.str_offset = PyUnicode_InternFromString(c"offset".as_ptr());
    state.str_ignore_dst = PyUnicode_InternFromString(c"ignore_dst".as_ptr());
    state.str_unit = PyUnicode_InternFromString(c"unit".as_ptr());
    state.str_increment = PyUnicode_InternFromString(c"increment".as_ptr());
    state.str_mode = PyUnicode_InternFromString(c"mode".as_ptr());
    state.str_floor = PyUnicode_InternFromString(c"floor".as_ptr());
    state.str_ceil = PyUnicode_InternFromString(c"ceil".as_ptr());
    state.str_half_floor = PyUnicode_InternFromString(c"half_floor".as_ptr());
    state.str_half_ceil = PyUnicode_InternFromString(c"half_ceil".as_ptr());
    state.str_half_even = PyUnicode_InternFromString(c"half_even".as_ptr());
    state.str_format = PyUnicode_InternFromString(c"format".as_ptr());

    state.exc_repeated = new_exc(
        module,
        c"whenever.RepeatedTime",
        doc::REPEATEDTIME,
        PyExc_ValueError,
    );
    state.exc_skipped = new_exc(
        module,
        c"whenever.SkippedTime",
        doc::SKIPPEDTIME,
        PyExc_ValueError,
    );
    state.exc_invalid_offset = new_exc(
        module,
        c"whenever.InvalidOffsetError",
        doc::INVALIDOFFSETERROR,
        PyExc_ValueError,
    );
    state.exc_implicitly_ignoring_dst = new_exc(
        module,
        c"whenever.ImplicitlyIgnoringDST",
        doc::IMPLICITLYIGNORINGDST,
        PyExc_TypeError,
    );
    state.exc_tz_notfound = new_exc(
        module,
        c"whenever.TimeZoneNotFoundError",
        doc::TIMEZONENOTFOUNDERROR,
        PyExc_ValueError,
    );

    // Making time patcheable results in a performance hit.
    // Only enable it if the time_machine module is available.
    state.time_machine_exists = unwrap_or_errcode!(time_machine_installed());
    state.time_patch = TimePatch::Unset;

    // We write these fields manually, to avoid triggering a "drop" of the previous value
    // which isn't there, since Python just allocated this memory for us.
    // std::ptr::write(
    (&raw mut state.tz_cache).write(TZifCache::new(unwrap_or_errcode!(get_tzdata_path())));
    (&raw mut state.zoneinfo_type).write(LazyImport::new(c"zoneinfo", c"ZoneInfo"));
    0
}

unsafe fn time_machine_installed() -> PyResult<bool> {
    // Important: we don't import `time_machine` here,
    // because that would be slower. We only need to check its existence.
    let find_spec = import_from(c"importlib.util", c"find_spec")?;
    defer_decref!(find_spec);
    let spec = call1(find_spec, steal!("time_machine".to_py()?))?;
    defer_decref!(spec);
    Ok(!is_none(spec))
}

fn get_tzdata_path() -> PyResult<Option<PathBuf>> {
    Ok(Some(PathBuf::from(unsafe {
        let __path__ = match import_from(c"tzdata.zoneinfo", c"__path__") {
            Ok(obj) => Ok(obj),
            _ if PyErr_ExceptionMatches(PyExc_ImportError) == 1 => {
                PyErr_Clear();
                return Ok(None);
            }
            e => e,
        }?;
        defer_decref!(__path__);
        // __path__ is a list of paths. It will only have one element,
        // unless somebody is doing something strange.
        (PyObject_GetItem(__path__, steal!((0).to_py()?)).as_result()? as *mut PyObject)
            .to_str()?
            .ok_or_type_err("tzdata module path must be a string")?
            .to_owned()
    })))
}

unsafe fn traverse(target: *mut PyObject, visit: visitproc, arg: *mut c_void) {
    if !target.is_null() {
        (visit)(target, arg);
    }
}
unsafe fn traverse_type(
    target: *mut PyTypeObject,
    visit: visitproc,
    arg: *mut c_void,
    num_singletons: usize,
) {
    if !target.is_null() {
        // XXX: This trick SEEMS to let us avoid adding GC support to our types.
        // Since our types are atomic and immutable this should be allowed...
        // ...BUT there is a reference cycle between the class and the
        // singleton instances (e.g. the Date.MAX instance and Date class itself)
        // Visiting the type once for each singleton should make GC aware of this.
        for _ in 0..(num_singletons + 1) {
            (visit)(target.cast(), arg);
        }
    }
}

unsafe extern "C" fn module_traverse(
    module: *mut PyObject,
    visit: visitproc,
    arg: *mut c_void,
) -> c_int {
    let state = State::for_mod(module);
    // types
    traverse_type(state.date_type, visit, arg, date::SINGLETONS.len());
    traverse_type(
        state.yearmonth_type,
        visit,
        arg,
        yearmonth::SINGLETONS.len(),
    );
    traverse_type(state.monthday_type, visit, arg, monthday::SINGLETONS.len());
    traverse_type(state.time_type, visit, arg, time::SINGLETONS.len());
    traverse_type(
        state.date_delta_type,
        visit,
        arg,
        date_delta::SINGLETONS.len(),
    );
    traverse_type(
        state.time_delta_type,
        visit,
        arg,
        time_delta::SINGLETONS.len(),
    );
    traverse_type(
        state.datetime_delta_type,
        visit,
        arg,
        datetime_delta::SINGLETONS.len(),
    );
    traverse_type(
        state.plain_datetime_type,
        visit,
        arg,
        plain_datetime::SINGLETONS.len(),
    );
    traverse_type(state.instant_type, visit, arg, instant::SINGLETONS.len());
    traverse_type(
        state.offset_datetime_type,
        visit,
        arg,
        offset_datetime::SINGLETONS.len(),
    );
    traverse_type(
        state.zoned_datetime_type,
        visit,
        arg,
        zoned_datetime::SINGLETONS.len(),
    );
    traverse_type(
        state.system_datetime_type,
        visit,
        arg,
        system_datetime::SINGLETONS.len(),
    );

    // enum members
    for &member in state.weekday_enum_members.iter() {
        traverse(member, visit, arg);
    }

    // exceptions
    traverse(state.exc_repeated, visit, arg);
    traverse(state.exc_skipped, visit, arg);
    traverse(state.exc_invalid_offset, visit, arg);
    traverse(state.exc_implicitly_ignoring_dst, visit, arg);
    traverse(state.exc_tz_notfound, visit, arg);

    // Imported modules
    traverse(state.timezone_type, visit, arg);
    traverse(state.strptime, visit, arg);
    traverse(state.time_ns, visit, arg);
    state.zoneinfo_type.traverse(visit, arg);

    0
}

#[cold]
unsafe extern "C" fn module_clear(module: *mut PyObject) -> c_int {
    let state = PyModule_GetState(module).cast::<State>().as_mut().unwrap();
    // types
    Py_CLEAR(ptr::addr_of_mut!(state.date_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.yearmonth_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.monthday_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.time_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.date_delta_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.time_delta_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.datetime_delta_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.plain_datetime_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.instant_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.offset_datetime_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.zoned_datetime_type).cast());
    Py_CLEAR(ptr::addr_of_mut!(state.system_datetime_type).cast());

    // enum members
    Py_CLEAR(ptr::addr_of_mut!(state.weekday_enum_members[0]));
    Py_CLEAR(ptr::addr_of_mut!(state.weekday_enum_members[1]));
    Py_CLEAR(ptr::addr_of_mut!(state.weekday_enum_members[2]));
    Py_CLEAR(ptr::addr_of_mut!(state.weekday_enum_members[3]));
    Py_CLEAR(ptr::addr_of_mut!(state.weekday_enum_members[4]));
    Py_CLEAR(ptr::addr_of_mut!(state.weekday_enum_members[5]));
    Py_CLEAR(ptr::addr_of_mut!(state.weekday_enum_members[6]));

    // interned strings
    Py_CLEAR(ptr::addr_of_mut!(state.str_years));
    Py_CLEAR(ptr::addr_of_mut!(state.str_months));
    Py_CLEAR(ptr::addr_of_mut!(state.str_weeks));
    Py_CLEAR(ptr::addr_of_mut!(state.str_days));
    Py_CLEAR(ptr::addr_of_mut!(state.str_hours));
    Py_CLEAR(ptr::addr_of_mut!(state.str_minutes));
    Py_CLEAR(ptr::addr_of_mut!(state.str_seconds));
    Py_CLEAR(ptr::addr_of_mut!(state.str_milliseconds));
    Py_CLEAR(ptr::addr_of_mut!(state.str_microseconds));
    Py_CLEAR(ptr::addr_of_mut!(state.str_nanoseconds));
    Py_CLEAR(ptr::addr_of_mut!(state.str_year));
    Py_CLEAR(ptr::addr_of_mut!(state.str_month));
    Py_CLEAR(ptr::addr_of_mut!(state.str_day));
    Py_CLEAR(ptr::addr_of_mut!(state.str_hour));
    Py_CLEAR(ptr::addr_of_mut!(state.str_minute));
    Py_CLEAR(ptr::addr_of_mut!(state.str_second));
    Py_CLEAR(ptr::addr_of_mut!(state.str_millisecond));
    Py_CLEAR(ptr::addr_of_mut!(state.str_microsecond));
    Py_CLEAR(ptr::addr_of_mut!(state.str_nanosecond));
    Py_CLEAR(ptr::addr_of_mut!(state.str_compatible));
    Py_CLEAR(ptr::addr_of_mut!(state.str_raise));
    Py_CLEAR(ptr::addr_of_mut!(state.str_earlier));
    Py_CLEAR(ptr::addr_of_mut!(state.str_later));
    Py_CLEAR(ptr::addr_of_mut!(state.str_tz));
    Py_CLEAR(ptr::addr_of_mut!(state.str_disambiguate));
    Py_CLEAR(ptr::addr_of_mut!(state.str_offset));
    Py_CLEAR(ptr::addr_of_mut!(state.str_ignore_dst));
    Py_CLEAR(ptr::addr_of_mut!(state.str_unit));
    Py_CLEAR(ptr::addr_of_mut!(state.str_increment));
    Py_CLEAR(ptr::addr_of_mut!(state.str_mode));
    Py_CLEAR(ptr::addr_of_mut!(state.str_floor));
    Py_CLEAR(ptr::addr_of_mut!(state.str_ceil));
    Py_CLEAR(ptr::addr_of_mut!(state.str_half_floor));
    Py_CLEAR(ptr::addr_of_mut!(state.str_half_ceil));
    Py_CLEAR(ptr::addr_of_mut!(state.str_half_even));
    Py_CLEAR(ptr::addr_of_mut!(state.str_format));

    // exceptions
    Py_CLEAR(ptr::addr_of_mut!(state.exc_repeated));
    Py_CLEAR(ptr::addr_of_mut!(state.exc_skipped));
    Py_CLEAR(ptr::addr_of_mut!(state.exc_invalid_offset));
    Py_CLEAR(ptr::addr_of_mut!(state.exc_implicitly_ignoring_dst));
    Py_CLEAR(ptr::addr_of_mut!(state.exc_tz_notfound));

    // imported stuff
    Py_CLEAR(ptr::addr_of_mut!(state.timezone_type));
    Py_CLEAR(ptr::addr_of_mut!(state.strptime));
    Py_CLEAR(ptr::addr_of_mut!(state.time_ns));

    0
}

#[cold]
unsafe extern "C" fn module_free(module: *mut c_void) {
    let state = PyModule_GetState(module.cast())
        .cast::<State>()
        .as_mut()
        .unwrap();
    // We clean up heap allocated stuff here because module_clear is
    // not *guaranteed* to be called
    std::ptr::drop_in_place(&mut state.tz_cache);
    std::ptr::drop_in_place(&mut state.zoneinfo_type);
}

pub(crate) struct State {
    // types
    date_type: *mut PyTypeObject,
    yearmonth_type: *mut PyTypeObject,
    monthday_type: *mut PyTypeObject,
    time_type: *mut PyTypeObject,
    date_delta_type: *mut PyTypeObject,
    time_delta_type: *mut PyTypeObject,
    datetime_delta_type: *mut PyTypeObject,
    plain_datetime_type: *mut PyTypeObject,
    instant_type: *mut PyTypeObject,
    offset_datetime_type: *mut PyTypeObject,
    zoned_datetime_type: *mut PyTypeObject,
    system_datetime_type: *mut PyTypeObject,

    // weekday enum
    weekday_enum_members: [*mut PyObject; 7],

    // exceptions
    exc_repeated: *mut PyObject,
    exc_skipped: *mut PyObject,
    exc_invalid_offset: *mut PyObject,
    exc_implicitly_ignoring_dst: *mut PyObject,
    exc_tz_notfound: *mut PyObject,

    // unpickling functions
    unpickle_date: *mut PyObject,
    unpickle_yearmonth: *mut PyObject,
    unpickle_monthday: *mut PyObject,
    unpickle_time: *mut PyObject,
    unpickle_date_delta: *mut PyObject,
    unpickle_time_delta: *mut PyObject,
    unpickle_datetime_delta: *mut PyObject,
    unpickle_plain_datetime: *mut PyObject,
    unpickle_instant: *mut PyObject,
    unpickle_offset_datetime: *mut PyObject,
    unpickle_zoned_datetime: *mut PyObject,
    unpickle_system_datetime: *mut PyObject,

    py_api: &'static PyDateTime_CAPI,

    // imported stuff
    timezone_type: *mut PyObject,
    strptime: *mut PyObject,
    time_ns: *mut PyObject,
    zoneinfo_type: LazyImport,

    // strings
    str_years: *mut PyObject,
    str_months: *mut PyObject,
    str_weeks: *mut PyObject,
    str_days: *mut PyObject,
    str_hours: *mut PyObject,
    str_minutes: *mut PyObject,
    str_seconds: *mut PyObject,
    str_milliseconds: *mut PyObject,
    str_microseconds: *mut PyObject,
    str_nanoseconds: *mut PyObject,
    str_year: *mut PyObject,
    str_month: *mut PyObject,
    str_day: *mut PyObject,
    str_hour: *mut PyObject,
    str_minute: *mut PyObject,
    str_second: *mut PyObject,
    str_millisecond: *mut PyObject,
    str_microsecond: *mut PyObject,
    str_nanosecond: *mut PyObject,
    str_compatible: *mut PyObject,
    str_raise: *mut PyObject,
    str_earlier: *mut PyObject,
    str_later: *mut PyObject,
    str_tz: *mut PyObject,
    str_disambiguate: *mut PyObject,
    str_offset: *mut PyObject,
    str_ignore_dst: *mut PyObject,
    str_unit: *mut PyObject,
    str_increment: *mut PyObject,
    str_mode: *mut PyObject,
    str_floor: *mut PyObject,
    str_ceil: *mut PyObject,
    str_half_floor: *mut PyObject,
    str_half_ceil: *mut PyObject,
    str_half_even: *mut PyObject,
    str_format: *mut PyObject,

    time_patch: TimePatch,
    time_machine_exists: bool,

    tz_cache: TZifCache,
}

enum TimePatch {
    Unset,
    Frozen(Instant),
    KeepTicking {
        pin: std::time::Duration,
        at: std::time::Duration,
    },
}

impl Instant {
    fn from_duration_since_epoch(d: std::time::Duration) -> Option<Self> {
        Some(Instant {
            epoch: EpochSecs::new(d.as_secs() as _)?,
            // Safe: subsec on Duration is always in range
            subsec: SubSecNanos::new_unchecked(d.subsec_nanos() as _),
        })
    }

    fn from_nanos_i64(ns: i64) -> Option<Self> {
        Some(Instant {
            epoch: EpochSecs::new(ns / 1_000_000_000)?,
            subsec: SubSecNanos::from_remainder(ns),
        })
    }
}

impl State {
    unsafe fn for_type<'a>(tp: *mut PyTypeObject) -> &'a Self {
        PyType_GetModuleState(tp).cast::<Self>().as_ref().unwrap()
    }

    unsafe fn for_type_mut<'a>(tp: *mut PyTypeObject) -> &'a mut Self {
        PyType_GetModuleState(tp).cast::<Self>().as_mut().unwrap()
    }

    unsafe fn for_mod<'a>(module: *mut PyObject) -> &'a Self {
        PyModule_GetState(module).cast::<Self>().as_ref().unwrap()
    }

    unsafe fn for_mod_mut<'a>(module: *mut PyObject) -> &'a mut Self {
        PyModule_GetState(module).cast::<Self>().as_mut().unwrap()
    }

    unsafe fn for_obj<'a>(obj: *mut PyObject) -> &'a Self {
        PyType_GetModuleState(Py_TYPE(obj))
            .cast::<Self>()
            .as_ref()
            .unwrap()
    }

    unsafe fn for_obj_mut<'a>(obj: *mut PyObject) -> &'a mut Self {
        PyType_GetModuleState(Py_TYPE(obj))
            .cast::<Self>()
            .as_mut()
            .unwrap()
    }

    unsafe fn time_ns(&self) -> PyResult<Instant> {
        match self.time_patch {
            TimePatch::Unset => {
                if self.time_machine_exists {
                    self.time_ns_py()
                } else {
                    self.time_ns_rust()
                }
            }
            TimePatch::Frozen(e) => Ok(e),
            TimePatch::KeepTicking { pin, at } => {
                let dur = pin
                    + SystemTime::now()
                        .duration_since(SystemTime::UNIX_EPOCH)
                        .ok()
                        .ok_or_raise(PyExc_OSError, "System time out of range")?
                    - at;
                Instant::from_duration_since_epoch(dur)
                    .ok_or_raise(PyExc_OSError, "System time out of range")
            }
        }
    }

    unsafe fn time_ns_py(&self) -> PyResult<Instant> {
        let ts = PyObject_CallNoArgs(self.time_ns).as_result()?;
        defer_decref!(ts);
        let ns = (ts as *mut PyObject)
            // FUTURE: this will break in the year 2262. Fix it before then.
            .to_i64()?
            .ok_or_raise(PyExc_RuntimeError, "time_ns() returned a non-integer")?;
        Instant::from_nanos_i64(ns).ok_or_raise(PyExc_OSError, "System time out of range")
    }

    unsafe fn time_ns_rust(&self) -> PyResult<Instant> {
        SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .ok()
            .and_then(Instant::from_duration_since_epoch)
            .ok_or_raise(PyExc_OSError, "System time out of range")
    }
}

#[allow(clippy::missing_safety_doc)]
#[allow(non_snake_case)]
#[no_mangle]
#[cold]
pub unsafe extern "C" fn PyInit__whenever() -> *mut PyObject {
    PyModuleDef_Init(ptr::addr_of_mut!(MODULE_DEF))
}
