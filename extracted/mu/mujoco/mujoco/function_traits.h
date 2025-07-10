// Copyright 2022 DeepMind Technologies Limited
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef MUJOCO_PYTHON_CODEGEN_FUNCTION_TRAITS_H_
#define MUJOCO_PYTHON_CODEGEN_FUNCTION_TRAITS_H_

#include <tuple>

#include <mujoco/mujoco.h>
#include "util/crossplatform.h"

namespace mujoco::python_traits {

struct mj_defaultVFS {
  static constexpr char name[] = "mj_defaultVFS";
  static constexpr char doc[] = "Initialize an empty VFS, mj_deleteVFS must be called to deallocate the VFS.";
  using type = void (mjVFS *);
  static constexpr auto param_names = std::make_tuple("vfs");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_defaultVFS;
  }
};

struct mj_addFileVFS {
  static constexpr char name[] = "mj_addFileVFS";
  static constexpr char doc[] = "Add file to VFS, return 0: success, 2: repeated name, -1: failed to load.";
  using type = int (mjVFS *, const char *, const char *);
  static constexpr auto param_names = std::make_tuple("vfs", "directory", "filename");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_addFileVFS;
  }
};

struct mj_addBufferVFS {
  static constexpr char name[] = "mj_addBufferVFS";
  static constexpr char doc[] = "Add file to VFS from buffer, return 0: success, 2: repeated name, -1: failed to load.";
  using type = int (mjVFS *, const char *, const void *, int);
  static constexpr auto param_names = std::make_tuple("vfs", "name", "buffer", "nbuffer");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_addBufferVFS;
  }
};

struct mj_deleteFileVFS {
  static constexpr char name[] = "mj_deleteFileVFS";
  static constexpr char doc[] = "Delete file from VFS, return 0: success, -1: not found in VFS.";
  using type = int (mjVFS *, const char *);
  static constexpr auto param_names = std::make_tuple("vfs", "filename");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_deleteFileVFS;
  }
};

struct mj_deleteVFS {
  static constexpr char name[] = "mj_deleteVFS";
  static constexpr char doc[] = "Delete all files from VFS and deallocates VFS internal memory.";
  using type = void (mjVFS *);
  static constexpr auto param_names = std::make_tuple("vfs");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_deleteVFS;
  }
};

struct mj_loadXML {
  static constexpr char name[] = "mj_loadXML";
  static constexpr char doc[] = "Parse XML file in MJCF or URDF format, compile it, return low-level model. If vfs is not NULL, look up files in vfs before reading from disk. If error is not NULL, it must have size error_sz.";
  using type = mjModel * (const char *, const mjVFS *, char *, int);
  static constexpr auto param_names = std::make_tuple("filename", "vfs", "error", "error_sz");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_loadXML;
  }
};

struct mj_parseXML {
  static constexpr char name[] = "mj_parseXML";
  static constexpr char doc[] = "Parse spec from XML file.";
  using type = mjSpec * (const char *, const mjVFS *, char *, int);
  static constexpr auto param_names = std::make_tuple("filename", "vfs", "error", "error_sz");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_parseXML;
  }
};

struct mj_parseXMLString {
  static constexpr char name[] = "mj_parseXMLString";
  static constexpr char doc[] = "Parse spec from XML string.";
  using type = mjSpec * (const char *, const mjVFS *, char *, int);
  static constexpr auto param_names = std::make_tuple("xml", "vfs", "error", "error_sz");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_parseXMLString;
  }
};

struct mj_compile {
  static constexpr char name[] = "mj_compile";
  static constexpr char doc[] = "Compile spec to model.";
  using type = mjModel * (mjSpec *, const mjVFS *);
  static constexpr auto param_names = std::make_tuple("s", "vfs");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_compile;
  }
};

struct mj_copyBack {
  static constexpr char name[] = "mj_copyBack";
  static constexpr char doc[] = "Copy real-valued arrays from model to spec, returns 1 on success.";
  using type = int (mjSpec *, const mjModel *);
  static constexpr auto param_names = std::make_tuple("s", "m");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_copyBack;
  }
};

struct mj_recompile {
  static constexpr char name[] = "mj_recompile";
  static constexpr char doc[] = "Recompile spec to model, preserving the state, return 0 on success.";
  using type = int (mjSpec *, const mjVFS *, mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("s", "vfs", "m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_recompile;
  }
};

struct mj_saveLastXML {
  static constexpr char name[] = "mj_saveLastXML";
  static constexpr char doc[] = "Update XML data structures with info from low-level model created with mj_loadXML, save as MJCF. If error is not NULL, it must have size error_sz.";
  using type = int (const char *, const mjModel *, char *, int);
  static constexpr auto param_names = std::make_tuple("filename", "m", "error", "error_sz");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_saveLastXML;
  }
};

struct mj_freeLastXML {
  static constexpr char name[] = "mj_freeLastXML";
  static constexpr char doc[] = "Free last XML model if loaded. Called internally at each load.";
  using type = void ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_freeLastXML;
  }
};

struct mj_saveXMLString {
  static constexpr char name[] = "mj_saveXMLString";
  static constexpr char doc[] = "Save spec to XML string, return 0 on success, -1 on failure. If length of the output buffer is too small, returns the required size.";
  using type = int (const mjSpec *, char *, int, char *, int);
  static constexpr auto param_names = std::make_tuple("s", "xml", "xml_sz", "error", "error_sz");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_saveXMLString;
  }
};

struct mj_saveXML {
  static constexpr char name[] = "mj_saveXML";
  static constexpr char doc[] = "Save spec to XML file, return 0 on success, -1 otherwise.";
  using type = int (const mjSpec *, const char *, char *, int);
  static constexpr auto param_names = std::make_tuple("s", "filename", "error", "error_sz");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_saveXML;
  }
};

struct mj_step {
  static constexpr char name[] = "mj_step";
  static constexpr char doc[] = "Advance simulation, use control callback to obtain external force and control.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_step;
  }
};

struct mj_step1 {
  static constexpr char name[] = "mj_step1";
  static constexpr char doc[] = "Advance simulation in two steps: before external force and control is set by user.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_step1;
  }
};

struct mj_step2 {
  static constexpr char name[] = "mj_step2";
  static constexpr char doc[] = "Advance simulation in two steps: after external force and control is set by user.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_step2;
  }
};

struct mj_forward {
  static constexpr char name[] = "mj_forward";
  static constexpr char doc[] = "Forward dynamics: same as mj_step but do not integrate in time.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_forward;
  }
};

struct mj_inverse {
  static constexpr char name[] = "mj_inverse";
  static constexpr char doc[] = "Inverse dynamics: qacc must be set before calling.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_inverse;
  }
};

struct mj_forwardSkip {
  static constexpr char name[] = "mj_forwardSkip";
  static constexpr char doc[] = "Forward dynamics with skip; skipstage is mjtStage.";
  using type = void (const mjModel *, mjData *, int, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "skipstage", "skipsensor");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_forwardSkip;
  }
};

struct mj_inverseSkip {
  static constexpr char name[] = "mj_inverseSkip";
  static constexpr char doc[] = "Inverse dynamics with skip; skipstage is mjtStage.";
  using type = void (const mjModel *, mjData *, int, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "skipstage", "skipsensor");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_inverseSkip;
  }
};

struct mj_defaultLROpt {
  static constexpr char name[] = "mj_defaultLROpt";
  static constexpr char doc[] = "Set default options for length range computation.";
  using type = void (mjLROpt *);
  static constexpr auto param_names = std::make_tuple("opt");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_defaultLROpt;
  }
};

struct mj_defaultSolRefImp {
  static constexpr char name[] = "mj_defaultSolRefImp";
  static constexpr char doc[] = "Set solver parameters to default values.";
  using type = void (mjtNum *, mjtNum *);
  static constexpr auto param_names = std::make_tuple("solref", "solimp");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_defaultSolRefImp;
  }
};

struct mj_defaultOption {
  static constexpr char name[] = "mj_defaultOption";
  static constexpr char doc[] = "Set physics options to default values.";
  using type = void (mjOption *);
  static constexpr auto param_names = std::make_tuple("opt");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_defaultOption;
  }
};

struct mj_defaultVisual {
  static constexpr char name[] = "mj_defaultVisual";
  static constexpr char doc[] = "Set visual options to default values.";
  using type = void (mjVisual *);
  static constexpr auto param_names = std::make_tuple("vis");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_defaultVisual;
  }
};

struct mj_copyModel {
  static constexpr char name[] = "mj_copyModel";
  static constexpr char doc[] = "Copy mjModel, allocate new if dest is NULL.";
  using type = mjModel * (mjModel *, const mjModel *);
  static constexpr auto param_names = std::make_tuple("dest", "src");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_copyModel;
  }
};

struct mj_saveModel {
  static constexpr char name[] = "mj_saveModel";
  static constexpr char doc[] = "Save model to binary MJB file or memory buffer; buffer has precedence when given.";
  using type = void (const mjModel *, const char *, void *, int);
  static constexpr auto param_names = std::make_tuple("m", "filename", "buffer", "buffer_sz");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_saveModel;
  }
};

struct mj_loadModel {
  static constexpr char name[] = "mj_loadModel";
  static constexpr char doc[] = "Load model from binary MJB file. If vfs is not NULL, look up file in vfs before reading from disk.";
  using type = mjModel * (const char *, const mjVFS *);
  static constexpr auto param_names = std::make_tuple("filename", "vfs");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_loadModel;
  }
};

struct mj_deleteModel {
  static constexpr char name[] = "mj_deleteModel";
  static constexpr char doc[] = "Free memory allocation in model.";
  using type = void (mjModel *);
  static constexpr auto param_names = std::make_tuple("m");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_deleteModel;
  }
};

struct mj_sizeModel {
  static constexpr char name[] = "mj_sizeModel";
  static constexpr char doc[] = "Return size of buffer needed to hold model.";
  using type = int (const mjModel *);
  static constexpr auto param_names = std::make_tuple("m");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_sizeModel;
  }
};

struct mj_makeData {
  static constexpr char name[] = "mj_makeData";
  static constexpr char doc[] = "Allocate mjData corresponding to given model. If the model buffer is unallocated the initial configuration will not be set.";
  using type = mjData * (const mjModel *);
  static constexpr auto param_names = std::make_tuple("m");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_makeData;
  }
};

struct mj_copyData {
  static constexpr char name[] = "mj_copyData";
  static constexpr char doc[] = "Copy mjData. m is only required to contain the size fields from MJMODEL_INTS.";
  using type = mjData * (mjData *, const mjModel *, const mjData *);
  static constexpr auto param_names = std::make_tuple("dest", "m", "src");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_copyData;
  }
};

struct mjv_copyData {
  static constexpr char name[] = "mjv_copyData";
  static constexpr char doc[] = "Copy mjData, skip large arrays not required for visualization.";
  using type = mjData * (mjData *, const mjModel *, const mjData *);
  static constexpr auto param_names = std::make_tuple("dest", "m", "src");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_copyData;
  }
};

struct mj_resetData {
  static constexpr char name[] = "mj_resetData";
  static constexpr char doc[] = "Reset data to defaults.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_resetData;
  }
};

struct mj_resetDataDebug {
  static constexpr char name[] = "mj_resetDataDebug";
  static constexpr char doc[] = "Reset data to defaults, fill everything else with debug_value.";
  using type = void (const mjModel *, mjData *, unsigned char);
  static constexpr auto param_names = std::make_tuple("m", "d", "debug_value");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_resetDataDebug;
  }
};

struct mj_resetDataKeyframe {
  static constexpr char name[] = "mj_resetDataKeyframe";
  static constexpr char doc[] = "Reset data. If 0 <= key < nkey, set fields from specified keyframe.";
  using type = void (const mjModel *, mjData *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "key");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_resetDataKeyframe;
  }
};

struct mj_markStack {
  static constexpr char name[] = "mj_markStack";
  static constexpr char doc[] = "Mark a new frame on the mjData stack.";
  using type = void (mjData *);
  static constexpr auto param_names = std::make_tuple("d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_markStack;
  }
};

struct mj_freeStack {
  static constexpr char name[] = "mj_freeStack";
  static constexpr char doc[] = "Free the current mjData stack frame. All pointers returned by mj_stackAlloc since the last call to mj_markStack must no longer be used afterwards.";
  using type = void (mjData *);
  static constexpr auto param_names = std::make_tuple("d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_freeStack;
  }
};

struct mj_stackAllocByte {
  static constexpr char name[] = "mj_stackAllocByte";
  static constexpr char doc[] = "Allocate a number of bytes on mjData stack at a specific alignment. Call mju_error on stack overflow.";
  using type = void * (mjData *, size_t, size_t);
  static constexpr auto param_names = std::make_tuple("d", "bytes", "alignment");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_stackAllocByte;
  }
};

struct mj_stackAllocNum {
  static constexpr char name[] = "mj_stackAllocNum";
  static constexpr char doc[] = "Allocate array of mjtNums on mjData stack. Call mju_error on stack overflow.";
  using type = mjtNum * (mjData *, size_t);
  static constexpr auto param_names = std::make_tuple("d", "size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_stackAllocNum;
  }
};

struct mj_stackAllocInt {
  static constexpr char name[] = "mj_stackAllocInt";
  static constexpr char doc[] = "Allocate array of ints on mjData stack. Call mju_error on stack overflow.";
  using type = int * (mjData *, size_t);
  static constexpr auto param_names = std::make_tuple("d", "size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_stackAllocInt;
  }
};

struct mj_deleteData {
  static constexpr char name[] = "mj_deleteData";
  static constexpr char doc[] = "Free memory allocation in mjData.";
  using type = void (mjData *);
  static constexpr auto param_names = std::make_tuple("d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_deleteData;
  }
};

struct mj_resetCallbacks {
  static constexpr char name[] = "mj_resetCallbacks";
  static constexpr char doc[] = "Reset all callbacks to NULL pointers (NULL is the default).";
  using type = void ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_resetCallbacks;
  }
};

struct mj_setConst {
  static constexpr char name[] = "mj_setConst";
  static constexpr char doc[] = "Set constant fields of mjModel, corresponding to qpos0 configuration.";
  using type = void (mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_setConst;
  }
};

struct mj_setLengthRange {
  static constexpr char name[] = "mj_setLengthRange";
  static constexpr char doc[] = "Set actuator_lengthrange for specified actuator; return 1 if ok, 0 if error.";
  using type = int (mjModel *, mjData *, int, const mjLROpt *, char *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "index", "opt", "error", "error_sz");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_setLengthRange;
  }
};

struct mj_makeSpec {
  static constexpr char name[] = "mj_makeSpec";
  static constexpr char doc[] = "Create empty spec.";
  using type = mjSpec * ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_makeSpec;
  }
};

struct mj_copySpec {
  static constexpr char name[] = "mj_copySpec";
  static constexpr char doc[] = "Copy spec.";
  using type = mjSpec * (const mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_copySpec;
  }
};

struct mj_deleteSpec {
  static constexpr char name[] = "mj_deleteSpec";
  static constexpr char doc[] = "Free memory allocation in mjSpec.";
  using type = void (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_deleteSpec;
  }
};

struct mjs_activatePlugin {
  static constexpr char name[] = "mjs_activatePlugin";
  static constexpr char doc[] = "Activate plugin. Returns 0 on success.";
  using type = int (mjSpec *, const char *);
  static constexpr auto param_names = std::make_tuple("s", "name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_activatePlugin;
  }
};

struct mjs_setDeepCopy {
  static constexpr char name[] = "mjs_setDeepCopy";
  static constexpr char doc[] = "Turn deep copy on or off attach. Returns 0 on success.";
  using type = int (mjSpec *, int);
  static constexpr auto param_names = std::make_tuple("s", "deepcopy");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setDeepCopy;
  }
};

struct mj_printFormattedModel {
  static constexpr char name[] = "mj_printFormattedModel";
  static constexpr char doc[] = "Print mjModel to text file, specifying format. float_format must be a valid printf-style format string for a single float value.";
  using type = void (const mjModel *, const char *, const char *);
  static constexpr auto param_names = std::make_tuple("m", "filename", "float_format");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_printFormattedModel;
  }
};

struct mj_printModel {
  static constexpr char name[] = "mj_printModel";
  static constexpr char doc[] = "Print model to text file.";
  using type = void (const mjModel *, const char *);
  static constexpr auto param_names = std::make_tuple("m", "filename");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_printModel;
  }
};

struct mj_printFormattedData {
  static constexpr char name[] = "mj_printFormattedData";
  static constexpr char doc[] = "Print mjData to text file, specifying format. float_format must be a valid printf-style format string for a single float value";
  using type = void (const mjModel *, const mjData *, const char *, const char *);
  static constexpr auto param_names = std::make_tuple("m", "d", "filename", "float_format");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_printFormattedData;
  }
};

struct mj_printData {
  static constexpr char name[] = "mj_printData";
  static constexpr char doc[] = "Print data to text file.";
  using type = void (const mjModel *, const mjData *, const char *);
  static constexpr auto param_names = std::make_tuple("m", "d", "filename");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_printData;
  }
};

struct mju_printMat {
  static constexpr char name[] = "mju_printMat";
  static constexpr char doc[] = "Print matrix to screen.";
  using type = void (const mjtNum *, int, int);
  static constexpr auto param_names = std::make_tuple("mat", "nr", "nc");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_printMat;
  }
};

struct mju_printMatSparse {
  static constexpr char name[] = "mju_printMatSparse";
  static constexpr char doc[] = "Print sparse matrix to screen.";
  using type = void (const mjtNum *, int, const int *, const int *, const int *);
  static constexpr auto param_names = std::make_tuple("mat", "nr", "rownnz", "rowadr", "colind");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_printMatSparse;
  }
};

struct mj_printSchema {
  static constexpr char name[] = "mj_printSchema";
  static constexpr char doc[] = "Print internal XML schema as plain text or HTML, with style-padding or &nbsp;.";
  using type = int (const char *, char *, int, int, int);
  static constexpr auto param_names = std::make_tuple("filename", "buffer", "buffer_sz", "flg_html", "flg_pad");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_printSchema;
  }
};

struct mj_fwdPosition {
  static constexpr char name[] = "mj_fwdPosition";
  static constexpr char doc[] = "Run position-dependent computations.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_fwdPosition;
  }
};

struct mj_fwdVelocity {
  static constexpr char name[] = "mj_fwdVelocity";
  static constexpr char doc[] = "Run velocity-dependent computations.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_fwdVelocity;
  }
};

struct mj_fwdActuation {
  static constexpr char name[] = "mj_fwdActuation";
  static constexpr char doc[] = "Compute actuator force qfrc_actuator.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_fwdActuation;
  }
};

struct mj_fwdAcceleration {
  static constexpr char name[] = "mj_fwdAcceleration";
  static constexpr char doc[] = "Add up all non-constraint forces, compute qacc_smooth.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_fwdAcceleration;
  }
};

struct mj_fwdConstraint {
  static constexpr char name[] = "mj_fwdConstraint";
  static constexpr char doc[] = "Run selected constraint solver.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_fwdConstraint;
  }
};

struct mj_Euler {
  static constexpr char name[] = "mj_Euler";
  static constexpr char doc[] = "Euler integrator, semi-implicit in velocity.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_Euler;
  }
};

struct mj_RungeKutta {
  static constexpr char name[] = "mj_RungeKutta";
  static constexpr char doc[] = "Runge-Kutta explicit order-N integrator.";
  using type = void (const mjModel *, mjData *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "N");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_RungeKutta;
  }
};

struct mj_implicit {
  static constexpr char name[] = "mj_implicit";
  static constexpr char doc[] = "Implicit-in-velocity integrators.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_implicit;
  }
};

struct mj_invPosition {
  static constexpr char name[] = "mj_invPosition";
  static constexpr char doc[] = "Run position-dependent computations in inverse dynamics.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_invPosition;
  }
};

struct mj_invVelocity {
  static constexpr char name[] = "mj_invVelocity";
  static constexpr char doc[] = "Run velocity-dependent computations in inverse dynamics.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_invVelocity;
  }
};

struct mj_invConstraint {
  static constexpr char name[] = "mj_invConstraint";
  static constexpr char doc[] = "Apply the analytical formula for inverse constraint dynamics.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_invConstraint;
  }
};

struct mj_compareFwdInv {
  static constexpr char name[] = "mj_compareFwdInv";
  static constexpr char doc[] = "Compare forward and inverse dynamics, save results in fwdinv.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_compareFwdInv;
  }
};

struct mj_sensorPos {
  static constexpr char name[] = "mj_sensorPos";
  static constexpr char doc[] = "Evaluate position-dependent sensors.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_sensorPos;
  }
};

struct mj_sensorVel {
  static constexpr char name[] = "mj_sensorVel";
  static constexpr char doc[] = "Evaluate velocity-dependent sensors.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_sensorVel;
  }
};

struct mj_sensorAcc {
  static constexpr char name[] = "mj_sensorAcc";
  static constexpr char doc[] = "Evaluate acceleration and force-dependent sensors.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_sensorAcc;
  }
};

struct mj_energyPos {
  static constexpr char name[] = "mj_energyPos";
  static constexpr char doc[] = "Evaluate position-dependent energy (potential).";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_energyPos;
  }
};

struct mj_energyVel {
  static constexpr char name[] = "mj_energyVel";
  static constexpr char doc[] = "Evaluate velocity-dependent energy (kinetic).";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_energyVel;
  }
};

struct mj_checkPos {
  static constexpr char name[] = "mj_checkPos";
  static constexpr char doc[] = "Check qpos, reset if any element is too big or nan.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_checkPos;
  }
};

struct mj_checkVel {
  static constexpr char name[] = "mj_checkVel";
  static constexpr char doc[] = "Check qvel, reset if any element is too big or nan.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_checkVel;
  }
};

struct mj_checkAcc {
  static constexpr char name[] = "mj_checkAcc";
  static constexpr char doc[] = "Check qacc, reset if any element is too big or nan.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_checkAcc;
  }
};

struct mj_kinematics {
  static constexpr char name[] = "mj_kinematics";
  static constexpr char doc[] = "Run forward kinematics.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_kinematics;
  }
};

struct mj_comPos {
  static constexpr char name[] = "mj_comPos";
  static constexpr char doc[] = "Map inertias and motion dofs to global frame centered at CoM.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_comPos;
  }
};

struct mj_camlight {
  static constexpr char name[] = "mj_camlight";
  static constexpr char doc[] = "Compute camera and light positions and orientations.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_camlight;
  }
};

struct mj_flex {
  static constexpr char name[] = "mj_flex";
  static constexpr char doc[] = "Compute flex-related quantities.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_flex;
  }
};

struct mj_tendon {
  static constexpr char name[] = "mj_tendon";
  static constexpr char doc[] = "Compute tendon lengths, velocities and moment arms.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_tendon;
  }
};

struct mj_transmission {
  static constexpr char name[] = "mj_transmission";
  static constexpr char doc[] = "Compute actuator transmission lengths and moments.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_transmission;
  }
};

struct mj_crb {
  static constexpr char name[] = "mj_crb";
  static constexpr char doc[] = "Run composite rigid body inertia algorithm (CRB).";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_crb;
  }
};

struct mj_makeM {
  static constexpr char name[] = "mj_makeM";
  static constexpr char doc[] = "Make inertia matrix.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_makeM;
  }
};

struct mj_factorM {
  static constexpr char name[] = "mj_factorM";
  static constexpr char doc[] = "Compute sparse L'*D*L factorizaton of inertia matrix.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_factorM;
  }
};

struct mj_solveM {
  static constexpr char name[] = "mj_solveM";
  static constexpr char doc[] = "Solve linear system M * x = y using factorization:  x = inv(L'*D*L)*y";
  using type = void (const mjModel *, mjData *, mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "x", "y", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_solveM;
  }
};

struct mj_solveM2 {
  static constexpr char name[] = "mj_solveM2";
  static constexpr char doc[] = "Half of linear solve:  x = sqrt(inv(D))*inv(L')*y";
  using type = void (const mjModel *, mjData *, mjtNum *, const mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "x", "y", "sqrtInvD", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_solveM2;
  }
};

struct mj_comVel {
  static constexpr char name[] = "mj_comVel";
  static constexpr char doc[] = "Compute cvel, cdof_dot.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_comVel;
  }
};

struct mj_passive {
  static constexpr char name[] = "mj_passive";
  static constexpr char doc[] = "Compute qfrc_passive from spring-dampers, gravity compensation and fluid forces.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_passive;
  }
};

struct mj_subtreeVel {
  static constexpr char name[] = "mj_subtreeVel";
  static constexpr char doc[] = "Sub-tree linear velocity and angular momentum: compute subtree_linvel, subtree_angmom.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_subtreeVel;
  }
};

struct mj_rne {
  static constexpr char name[] = "mj_rne";
  static constexpr char doc[] = "RNE: compute M(qpos)*qacc + C(qpos,qvel); flg_acc=0 removes inertial term.";
  using type = void (const mjModel *, mjData *, int, mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "d", "flg_acc", "result");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_rne;
  }
};

struct mj_rnePostConstraint {
  static constexpr char name[] = "mj_rnePostConstraint";
  static constexpr char doc[] = "RNE with complete data: compute cacc, cfrc_ext, cfrc_int.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_rnePostConstraint;
  }
};

struct mj_collision {
  static constexpr char name[] = "mj_collision";
  static constexpr char doc[] = "Run collision detection.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_collision;
  }
};

struct mj_makeConstraint {
  static constexpr char name[] = "mj_makeConstraint";
  static constexpr char doc[] = "Construct constraints.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_makeConstraint;
  }
};

struct mj_island {
  static constexpr char name[] = "mj_island";
  static constexpr char doc[] = "Find constraint islands.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_island;
  }
};

struct mj_projectConstraint {
  static constexpr char name[] = "mj_projectConstraint";
  static constexpr char doc[] = "Compute inverse constraint inertia efc_AR.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_projectConstraint;
  }
};

struct mj_referenceConstraint {
  static constexpr char name[] = "mj_referenceConstraint";
  static constexpr char doc[] = "Compute efc_vel, efc_aref.";
  using type = void (const mjModel *, mjData *);
  static constexpr auto param_names = std::make_tuple("m", "d");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_referenceConstraint;
  }
};

struct mj_constraintUpdate {
  static constexpr char name[] = "mj_constraintUpdate";
  static constexpr char doc[] = "Compute efc_state, efc_force, qfrc_constraint, and (optionally) cone Hessians. If cost is not NULL, set *cost = s(jar) where jar = Jac*qacc-aref.";
  using type = void (const mjModel *, mjData *, const mjtNum *, mjtNum (*)[1], int);
  static constexpr auto param_names = std::make_tuple("m", "d", "jar", "cost", "flg_coneHessian");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_constraintUpdate);
  }
};

struct mj_stateSize {
  static constexpr char name[] = "mj_stateSize";
  static constexpr char doc[] = "Return size of state specification.";
  using type = int (const mjModel *, unsigned int);
  static constexpr auto param_names = std::make_tuple("m", "spec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_stateSize;
  }
};

struct mj_getState {
  static constexpr char name[] = "mj_getState";
  static constexpr char doc[] = "Get state.";
  using type = void (const mjModel *, const mjData *, mjtNum *, unsigned int);
  static constexpr auto param_names = std::make_tuple("m", "d", "state", "spec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_getState;
  }
};

struct mj_setState {
  static constexpr char name[] = "mj_setState";
  static constexpr char doc[] = "Set state.";
  using type = void (const mjModel *, mjData *, const mjtNum *, unsigned int);
  static constexpr auto param_names = std::make_tuple("m", "d", "state", "spec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_setState;
  }
};

struct mj_setKeyframe {
  static constexpr char name[] = "mj_setKeyframe";
  static constexpr char doc[] = "Copy current state to the k-th model keyframe.";
  using type = void (mjModel *, const mjData *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "k");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_setKeyframe;
  }
};

struct mj_addContact {
  static constexpr char name[] = "mj_addContact";
  static constexpr char doc[] = "Add contact to d->contact list; return 0 if success; 1 if buffer full.";
  using type = int (const mjModel *, mjData *, const mjContact *);
  static constexpr auto param_names = std::make_tuple("m", "d", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_addContact;
  }
};

struct mj_isPyramidal {
  static constexpr char name[] = "mj_isPyramidal";
  static constexpr char doc[] = "Determine type of friction cone.";
  using type = int (const mjModel *);
  static constexpr auto param_names = std::make_tuple("m");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_isPyramidal;
  }
};

struct mj_isSparse {
  static constexpr char name[] = "mj_isSparse";
  static constexpr char doc[] = "Determine type of constraint Jacobian.";
  using type = int (const mjModel *);
  static constexpr auto param_names = std::make_tuple("m");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_isSparse;
  }
};

struct mj_isDual {
  static constexpr char name[] = "mj_isDual";
  static constexpr char doc[] = "Determine type of solver (PGS is dual, CG and Newton are primal).";
  using type = int (const mjModel *);
  static constexpr auto param_names = std::make_tuple("m");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_isDual;
  }
};

struct mj_mulJacVec {
  static constexpr char name[] = "mj_mulJacVec";
  static constexpr char doc[] = "Multiply dense or sparse constraint Jacobian by vector.";
  using type = void (const mjModel *, const mjData *, mjtNum *, const mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "d", "res", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_mulJacVec;
  }
};

struct mj_mulJacTVec {
  static constexpr char name[] = "mj_mulJacTVec";
  static constexpr char doc[] = "Multiply dense or sparse constraint Jacobian transpose by vector.";
  using type = void (const mjModel *, const mjData *, mjtNum *, const mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "d", "res", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_mulJacTVec;
  }
};

struct mj_jac {
  static constexpr char name[] = "mj_jac";
  static constexpr char doc[] = "Compute 3/6-by-nv end-effector Jacobian of global point attached to given body.";
  using type = void (const mjModel *, const mjData *, mjtNum *, mjtNum *, const mjtNum (*)[3], int);
  static constexpr auto param_names = std::make_tuple("m", "d", "jacp", "jacr", "point", "body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_jac);
  }
};

struct mj_jacBody {
  static constexpr char name[] = "mj_jacBody";
  static constexpr char doc[] = "Compute body frame end-effector Jacobian.";
  using type = void (const mjModel *, const mjData *, mjtNum *, mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "jacp", "jacr", "body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_jacBody;
  }
};

struct mj_jacBodyCom {
  static constexpr char name[] = "mj_jacBodyCom";
  static constexpr char doc[] = "Compute body center-of-mass end-effector Jacobian.";
  using type = void (const mjModel *, const mjData *, mjtNum *, mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "jacp", "jacr", "body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_jacBodyCom;
  }
};

struct mj_jacSubtreeCom {
  static constexpr char name[] = "mj_jacSubtreeCom";
  static constexpr char doc[] = "Compute subtree center-of-mass end-effector Jacobian.";
  using type = void (const mjModel *, mjData *, mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "jacp", "body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_jacSubtreeCom;
  }
};

struct mj_jacGeom {
  static constexpr char name[] = "mj_jacGeom";
  static constexpr char doc[] = "Compute geom end-effector Jacobian.";
  using type = void (const mjModel *, const mjData *, mjtNum *, mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "jacp", "jacr", "geom");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_jacGeom;
  }
};

struct mj_jacSite {
  static constexpr char name[] = "mj_jacSite";
  static constexpr char doc[] = "Compute site end-effector Jacobian.";
  using type = void (const mjModel *, const mjData *, mjtNum *, mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "jacp", "jacr", "site");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_jacSite;
  }
};

struct mj_jacPointAxis {
  static constexpr char name[] = "mj_jacPointAxis";
  static constexpr char doc[] = "Compute translation end-effector Jacobian of point, and rotation Jacobian of axis.";
  using type = void (const mjModel *, mjData *, mjtNum *, mjtNum *, const mjtNum (*)[3], const mjtNum (*)[3], int);
  static constexpr auto param_names = std::make_tuple("m", "d", "jacPoint", "jacAxis", "point", "axis", "body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_jacPointAxis);
  }
};

struct mj_jacDot {
  static constexpr char name[] = "mj_jacDot";
  static constexpr char doc[] = "Compute 3/6-by-nv Jacobian time derivative of global point attached to given body.";
  using type = void (const mjModel *, const mjData *, mjtNum *, mjtNum *, const mjtNum (*)[3], int);
  static constexpr auto param_names = std::make_tuple("m", "d", "jacp", "jacr", "point", "body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_jacDot);
  }
};

struct mj_angmomMat {
  static constexpr char name[] = "mj_angmomMat";
  static constexpr char doc[] = "Compute subtree angular momentum matrix.";
  using type = void (const mjModel *, mjData *, mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "mat", "body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_angmomMat;
  }
};

struct mj_name2id {
  static constexpr char name[] = "mj_name2id";
  static constexpr char doc[] = "Get id of object with the specified mjtObj type and name, returns -1 if id not found.";
  using type = int (const mjModel *, int, const char *);
  static constexpr auto param_names = std::make_tuple("m", "type", "name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_name2id;
  }
};

struct mj_id2name {
  static constexpr char name[] = "mj_id2name";
  static constexpr char doc[] = "Get name of object with the specified mjtObj type and id, returns NULL if name not found.";
  using type = const char * (const mjModel *, int, int);
  static constexpr auto param_names = std::make_tuple("m", "type", "id");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_id2name;
  }
};

struct mj_fullM {
  static constexpr char name[] = "mj_fullM";
  static constexpr char doc[] = "Convert sparse inertia matrix M into full (i.e. dense) matrix.";
  using type = void (const mjModel *, mjtNum *, const mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "dst", "M");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_fullM;
  }
};

struct mj_mulM {
  static constexpr char name[] = "mj_mulM";
  static constexpr char doc[] = "Multiply vector by inertia matrix.";
  using type = void (const mjModel *, const mjData *, mjtNum *, const mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "d", "res", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_mulM;
  }
};

struct mj_mulM2 {
  static constexpr char name[] = "mj_mulM2";
  static constexpr char doc[] = "Multiply vector by (inertia matrix)^(1/2).";
  using type = void (const mjModel *, const mjData *, mjtNum *, const mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "d", "res", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_mulM2;
  }
};

struct mj_addM {
  static constexpr char name[] = "mj_addM";
  static constexpr char doc[] = "Add inertia matrix to destination matrix. Destination can be sparse or dense when all int* are NULL.";
  using type = void (const mjModel *, mjData *, mjtNum *, int *, int *, int *);
  static constexpr auto param_names = std::make_tuple("m", "d", "dst", "rownnz", "rowadr", "colind");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_addM;
  }
};

struct mj_applyFT {
  static constexpr char name[] = "mj_applyFT";
  static constexpr char doc[] = "Apply Cartesian force and torque (outside xfrc_applied mechanism).";
  using type = void (const mjModel *, mjData *, const mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[3], int, mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "d", "force", "torque", "point", "body", "qfrc_target");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_applyFT);
  }
};

struct mj_objectVelocity {
  static constexpr char name[] = "mj_objectVelocity";
  static constexpr char doc[] = "Compute object 6D velocity (rot:lin) in object-centered frame, world/local orientation.";
  using type = void (const mjModel *, const mjData *, int, int, mjtNum (*)[6], int);
  static constexpr auto param_names = std::make_tuple("m", "d", "objtype", "objid", "res", "flg_local");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_objectVelocity);
  }
};

struct mj_objectAcceleration {
  static constexpr char name[] = "mj_objectAcceleration";
  static constexpr char doc[] = "Compute object 6D acceleration (rot:lin) in object-centered frame, world/local orientation.";
  using type = void (const mjModel *, const mjData *, int, int, mjtNum (*)[6], int);
  static constexpr auto param_names = std::make_tuple("m", "d", "objtype", "objid", "res", "flg_local");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_objectAcceleration);
  }
};

struct mj_geomDistance {
  static constexpr char name[] = "mj_geomDistance";
  static constexpr char doc[] = "Returns smallest signed distance between two geoms and optionally segment from geom1 to geom2.";
  using type = mjtNum (const mjModel *, const mjData *, int, int, mjtNum, mjtNum (*)[6]);
  static constexpr auto param_names = std::make_tuple("m", "d", "geom1", "geom2", "distmax", "fromto");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_geomDistance);
  }
};

struct mj_contactForce {
  static constexpr char name[] = "mj_contactForce";
  static constexpr char doc[] = "Extract 6D force:torque given contact id, in the contact frame.";
  using type = void (const mjModel *, const mjData *, int, mjtNum (*)[6]);
  static constexpr auto param_names = std::make_tuple("m", "d", "id", "result");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_contactForce);
  }
};

struct mj_differentiatePos {
  static constexpr char name[] = "mj_differentiatePos";
  static constexpr char doc[] = "Compute velocity by finite-differencing two positions.";
  using type = void (const mjModel *, mjtNum *, mjtNum, const mjtNum *, const mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "qvel", "dt", "qpos1", "qpos2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_differentiatePos;
  }
};

struct mj_integratePos {
  static constexpr char name[] = "mj_integratePos";
  static constexpr char doc[] = "Integrate position with given velocity.";
  using type = void (const mjModel *, mjtNum *, const mjtNum *, mjtNum);
  static constexpr auto param_names = std::make_tuple("m", "qpos", "qvel", "dt");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_integratePos;
  }
};

struct mj_normalizeQuat {
  static constexpr char name[] = "mj_normalizeQuat";
  static constexpr char doc[] = "Normalize all quaternions in qpos-type vector.";
  using type = void (const mjModel *, mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "qpos");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_normalizeQuat;
  }
};

struct mj_local2Global {
  static constexpr char name[] = "mj_local2Global";
  static constexpr char doc[] = "Map from body local to global Cartesian coordinates, sameframe takes values from mjtSameFrame.";
  using type = void (mjData *, mjtNum (*)[3], mjtNum (*)[9], const mjtNum (*)[3], const mjtNum (*)[4], int, mjtByte);
  static constexpr auto param_names = std::make_tuple("d", "xpos", "xmat", "pos", "quat", "body", "sameframe");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_local2Global);
  }
};

struct mj_getTotalmass {
  static constexpr char name[] = "mj_getTotalmass";
  static constexpr char doc[] = "Sum all body masses.";
  using type = mjtNum (const mjModel *);
  static constexpr auto param_names = std::make_tuple("m");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_getTotalmass;
  }
};

struct mj_setTotalmass {
  static constexpr char name[] = "mj_setTotalmass";
  static constexpr char doc[] = "Scale body masses and inertias to achieve specified total mass.";
  using type = void (mjModel *, mjtNum);
  static constexpr auto param_names = std::make_tuple("m", "newmass");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_setTotalmass;
  }
};

struct mj_getPluginConfig {
  static constexpr char name[] = "mj_getPluginConfig";
  static constexpr char doc[] = "Return a config attribute value of a plugin instance; NULL: invalid plugin instance ID or attribute name";
  using type = const char * (const mjModel *, int, const char *);
  static constexpr auto param_names = std::make_tuple("m", "plugin_id", "attrib");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_getPluginConfig;
  }
};

struct mj_loadPluginLibrary {
  static constexpr char name[] = "mj_loadPluginLibrary";
  static constexpr char doc[] = "Load a dynamic library. The dynamic library is assumed to register one or more plugins.";
  using type = void (const char *);
  static constexpr auto param_names = std::make_tuple("path");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_loadPluginLibrary;
  }
};

struct mj_loadAllPluginLibraries {
  static constexpr char name[] = "mj_loadAllPluginLibraries";
  static constexpr char doc[] = "Scan a directory and load all dynamic libraries. Dynamic libraries in the specified directory are assumed to register one or more plugins. Optionally, if a callback is specified, it is called for each dynamic library encountered that registers plugins.";
  using type = void (const char *, mjfPluginLibraryLoadCallback);
  static constexpr auto param_names = std::make_tuple("directory", "callback");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_loadAllPluginLibraries;
  }
};

struct mj_version {
  static constexpr char name[] = "mj_version";
  static constexpr char doc[] = "Return version number: 1.0.2 is encoded as 102.";
  using type = int ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_version;
  }
};

struct mj_versionString {
  static constexpr char name[] = "mj_versionString";
  static constexpr char doc[] = "Return the current version of MuJoCo as a null-terminated string.";
  using type = const char * ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_versionString;
  }
};

struct mj_multiRay {
  static constexpr char name[] = "mj_multiRay";
  static constexpr char doc[] = "Intersect multiple rays emanating from a single point. Similar semantics to mj_ray, but vec is an array of (nray x 3) directions.";
  using type = void (const mjModel *, mjData *, const mjtNum (*)[3], const mjtNum *, const mjtByte *, mjtByte, int, int *, mjtNum *, int, mjtNum);
  static constexpr auto param_names = std::make_tuple("m", "d", "pnt", "vec", "geomgroup", "flg_static", "bodyexclude", "geomid", "dist", "nray", "cutoff");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_multiRay);
  }
};

struct mj_ray {
  static constexpr char name[] = "mj_ray";
  static constexpr char doc[] = "Intersect ray (pnt+x*vec, x>=0) with visible geoms, except geoms in bodyexclude. Return distance (x) to nearest surface, or -1 if no intersection and output geomid. geomgroup, flg_static are as in mjvOption; geomgroup==NULL skips group exclusion.";
  using type = mjtNum (const mjModel *, const mjData *, const mjtNum (*)[3], const mjtNum (*)[3], const mjtByte *, mjtByte, int, int (*)[1]);
  static constexpr auto param_names = std::make_tuple("m", "d", "pnt", "vec", "geomgroup", "flg_static", "bodyexclude", "geomid");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_ray);
  }
};

struct mj_rayHfield {
  static constexpr char name[] = "mj_rayHfield";
  static constexpr char doc[] = "Intersect ray with hfield, return nearest distance or -1 if no intersection.";
  using type = mjtNum (const mjModel *, const mjData *, int, const mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("m", "d", "geomid", "pnt", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_rayHfield);
  }
};

struct mj_rayMesh {
  static constexpr char name[] = "mj_rayMesh";
  static constexpr char doc[] = "Intersect ray with mesh, return nearest distance or -1 if no intersection.";
  using type = mjtNum (const mjModel *, const mjData *, int, const mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("m", "d", "geomid", "pnt", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mj_rayMesh);
  }
};

struct mju_rayGeom {
  static constexpr char name[] = "mju_rayGeom";
  static constexpr char doc[] = "Intersect ray with pure geom, return nearest distance or -1 if no intersection.";
  using type = mjtNum (const mjtNum (*)[3], const mjtNum (*)[9], const mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[3], int);
  static constexpr auto param_names = std::make_tuple("pos", "mat", "size", "pnt", "vec", "geomtype");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_rayGeom);
  }
};

struct mju_rayFlex {
  static constexpr char name[] = "mju_rayFlex";
  static constexpr char doc[] = "Intersect ray with flex, return nearest distance or -1 if no intersection, and also output nearest vertex id.";
  using type = mjtNum (const mjModel *, const mjData *, int, mjtByte, mjtByte, mjtByte, mjtByte, int, const mjtNum *, const mjtNum *, int (*)[1]);
  static constexpr auto param_names = std::make_tuple("m", "d", "flex_layer", "flg_vert", "flg_edge", "flg_face", "flg_skin", "flexid", "pnt", "vec", "vertid");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_rayFlex);
  }
};

struct mju_raySkin {
  static constexpr char name[] = "mju_raySkin";
  static constexpr char doc[] = "Intersect ray with skin, return nearest distance or -1 if no intersection, and also output nearest vertex id.";
  using type = mjtNum (int, int, const int *, const float *, const mjtNum (*)[3], const mjtNum (*)[3], int (*)[1]);
  static constexpr auto param_names = std::make_tuple("nface", "nvert", "face", "vert", "pnt", "vec", "vertid");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_raySkin);
  }
};

struct mjv_defaultCamera {
  static constexpr char name[] = "mjv_defaultCamera";
  static constexpr char doc[] = "Set default camera.";
  using type = void (mjvCamera *);
  static constexpr auto param_names = std::make_tuple("cam");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_defaultCamera;
  }
};

struct mjv_defaultFreeCamera {
  static constexpr char name[] = "mjv_defaultFreeCamera";
  static constexpr char doc[] = "Set default free camera.";
  using type = void (const mjModel *, mjvCamera *);
  static constexpr auto param_names = std::make_tuple("m", "cam");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_defaultFreeCamera;
  }
};

struct mjv_defaultPerturb {
  static constexpr char name[] = "mjv_defaultPerturb";
  static constexpr char doc[] = "Set default perturbation.";
  using type = void (mjvPerturb *);
  static constexpr auto param_names = std::make_tuple("pert");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_defaultPerturb;
  }
};

struct mjv_room2model {
  static constexpr char name[] = "mjv_room2model";
  static constexpr char doc[] = "Transform pose from room to model space.";
  using type = void (mjtNum (*)[3], mjtNum (*)[4], const mjtNum (*)[3], const mjtNum (*)[4], const mjvScene *);
  static constexpr auto param_names = std::make_tuple("modelpos", "modelquat", "roompos", "roomquat", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjv_room2model);
  }
};

struct mjv_model2room {
  static constexpr char name[] = "mjv_model2room";
  static constexpr char doc[] = "Transform pose from model to room space.";
  using type = void (mjtNum (*)[3], mjtNum (*)[4], const mjtNum (*)[3], const mjtNum (*)[4], const mjvScene *);
  static constexpr auto param_names = std::make_tuple("roompos", "roomquat", "modelpos", "modelquat", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjv_model2room);
  }
};

struct mjv_cameraInModel {
  static constexpr char name[] = "mjv_cameraInModel";
  static constexpr char doc[] = "Get camera info in model space; average left and right OpenGL cameras.";
  using type = void (mjtNum (*)[3], mjtNum (*)[3], mjtNum (*)[3], const mjvScene *);
  static constexpr auto param_names = std::make_tuple("headpos", "forward", "up", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjv_cameraInModel);
  }
};

struct mjv_cameraInRoom {
  static constexpr char name[] = "mjv_cameraInRoom";
  static constexpr char doc[] = "Get camera info in room space; average left and right OpenGL cameras.";
  using type = void (mjtNum (*)[3], mjtNum (*)[3], mjtNum (*)[3], const mjvScene *);
  static constexpr auto param_names = std::make_tuple("headpos", "forward", "up", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjv_cameraInRoom);
  }
};

struct mjv_frustumHeight {
  static constexpr char name[] = "mjv_frustumHeight";
  static constexpr char doc[] = "Get frustum height at unit distance from camera; average left and right OpenGL cameras.";
  using type = mjtNum (const mjvScene *);
  static constexpr auto param_names = std::make_tuple("scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_frustumHeight;
  }
};

struct mjv_alignToCamera {
  static constexpr char name[] = "mjv_alignToCamera";
  static constexpr char doc[] = "Rotate 3D vec in horizontal plane by angle between (0,1) and (forward_x,forward_y).";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "vec", "forward");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjv_alignToCamera);
  }
};

struct mjv_moveCamera {
  static constexpr char name[] = "mjv_moveCamera";
  static constexpr char doc[] = "Move camera with mouse; action is mjtMouse.";
  using type = void (const mjModel *, int, mjtNum, mjtNum, const mjvScene *, mjvCamera *);
  static constexpr auto param_names = std::make_tuple("m", "action", "reldx", "reldy", "scn", "cam");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_moveCamera;
  }
};

struct mjv_movePerturb {
  static constexpr char name[] = "mjv_movePerturb";
  static constexpr char doc[] = "Move perturb object with mouse; action is mjtMouse.";
  using type = void (const mjModel *, const mjData *, int, mjtNum, mjtNum, const mjvScene *, mjvPerturb *);
  static constexpr auto param_names = std::make_tuple("m", "d", "action", "reldx", "reldy", "scn", "pert");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_movePerturb;
  }
};

struct mjv_moveModel {
  static constexpr char name[] = "mjv_moveModel";
  static constexpr char doc[] = "Move model with mouse; action is mjtMouse.";
  using type = void (const mjModel *, int, mjtNum, mjtNum, const mjtNum (*)[3], mjvScene *);
  static constexpr auto param_names = std::make_tuple("m", "action", "reldx", "reldy", "roomup", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjv_moveModel);
  }
};

struct mjv_initPerturb {
  static constexpr char name[] = "mjv_initPerturb";
  static constexpr char doc[] = "Copy perturb pos,quat from selected body; set scale for perturbation.";
  using type = void (const mjModel *, mjData *, const mjvScene *, mjvPerturb *);
  static constexpr auto param_names = std::make_tuple("m", "d", "scn", "pert");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_initPerturb;
  }
};

struct mjv_applyPerturbPose {
  static constexpr char name[] = "mjv_applyPerturbPose";
  static constexpr char doc[] = "Set perturb pos,quat in d->mocap when selected body is mocap, and in d->qpos otherwise. Write d->qpos only if flg_paused and subtree root for selected body has free joint.";
  using type = void (const mjModel *, mjData *, const mjvPerturb *, int);
  static constexpr auto param_names = std::make_tuple("m", "d", "pert", "flg_paused");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_applyPerturbPose;
  }
};

struct mjv_applyPerturbForce {
  static constexpr char name[] = "mjv_applyPerturbForce";
  static constexpr char doc[] = "Set perturb force,torque in d->xfrc_applied, if selected body is dynamic.";
  using type = void (const mjModel *, mjData *, const mjvPerturb *);
  static constexpr auto param_names = std::make_tuple("m", "d", "pert");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_applyPerturbForce;
  }
};

struct mjv_averageCamera {
  static constexpr char name[] = "mjv_averageCamera";
  static constexpr char doc[] = "Return the average of two OpenGL cameras.";
  using type = mjvGLCamera (const mjvGLCamera *, const mjvGLCamera *);
  static constexpr auto param_names = std::make_tuple("cam1", "cam2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_averageCamera;
  }
};

struct mjv_select {
  static constexpr char name[] = "mjv_select";
  static constexpr char doc[] = "Select geom, flex or skin with mouse, return bodyid; -1: none selected.";
  using type = int (const mjModel *, const mjData *, const mjvOption *, mjtNum, mjtNum, mjtNum, const mjvScene *, mjtNum (*)[3], int (*)[1], int (*)[1], int (*)[1]);
  static constexpr auto param_names = std::make_tuple("m", "d", "vopt", "aspectratio", "relx", "rely", "scn", "selpnt", "geomid", "flexid", "skinid");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjv_select);
  }
};

struct mjv_defaultOption {
  static constexpr char name[] = "mjv_defaultOption";
  static constexpr char doc[] = "Set default visualization options.";
  using type = void (mjvOption *);
  static constexpr auto param_names = std::make_tuple("opt");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_defaultOption;
  }
};

struct mjv_defaultFigure {
  static constexpr char name[] = "mjv_defaultFigure";
  static constexpr char doc[] = "Set default figure.";
  using type = void (mjvFigure *);
  static constexpr auto param_names = std::make_tuple("fig");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_defaultFigure;
  }
};

struct mjv_initGeom {
  static constexpr char name[] = "mjv_initGeom";
  static constexpr char doc[] = "Initialize given geom fields when not NULL, set the rest to their default values.";
  using type = void (mjvGeom *, int, const mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[9], const float (*)[4]);
  static constexpr auto param_names = std::make_tuple("geom", "type", "size", "pos", "mat", "rgba");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjv_initGeom);
  }
};

struct mjv_connector {
  static constexpr char name[] = "mjv_connector";
  static constexpr char doc[] = "Set (type, size, pos, mat) for connector-type geom between given points. Assume that mjv_initGeom was already called to set all other properties. Width of mjGEOM_LINE is denominated in pixels.";
  using type = void (mjvGeom *, int, mjtNum, const mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("geom", "type", "width", "from_", "to");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjv_connector);
  }
};

struct mjv_defaultScene {
  static constexpr char name[] = "mjv_defaultScene";
  static constexpr char doc[] = "Set default abstract scene.";
  using type = void (mjvScene *);
  static constexpr auto param_names = std::make_tuple("scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_defaultScene;
  }
};

struct mjv_makeScene {
  static constexpr char name[] = "mjv_makeScene";
  static constexpr char doc[] = "Allocate resources in abstract scene.";
  using type = void (const mjModel *, mjvScene *, int);
  static constexpr auto param_names = std::make_tuple("m", "scn", "maxgeom");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_makeScene;
  }
};

struct mjv_freeScene {
  static constexpr char name[] = "mjv_freeScene";
  static constexpr char doc[] = "Free abstract scene.";
  using type = void (mjvScene *);
  static constexpr auto param_names = std::make_tuple("scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_freeScene;
  }
};

struct mjv_updateScene {
  static constexpr char name[] = "mjv_updateScene";
  static constexpr char doc[] = "Update entire scene given model state.";
  using type = void (const mjModel *, mjData *, const mjvOption *, const mjvPerturb *, mjvCamera *, int, mjvScene *);
  static constexpr auto param_names = std::make_tuple("m", "d", "opt", "pert", "cam", "catmask", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_updateScene;
  }
};

struct mjv_copyModel {
  static constexpr char name[] = "mjv_copyModel";
  static constexpr char doc[] = "Copy mjModel, skip large arrays not required for abstract visualization.";
  using type = void (mjModel *, const mjModel *);
  static constexpr auto param_names = std::make_tuple("dest", "src");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_copyModel;
  }
};

struct mjv_addGeoms {
  static constexpr char name[] = "mjv_addGeoms";
  static constexpr char doc[] = "Add geoms from selected categories.";
  using type = void (const mjModel *, mjData *, const mjvOption *, const mjvPerturb *, int, mjvScene *);
  static constexpr auto param_names = std::make_tuple("m", "d", "opt", "pert", "catmask", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_addGeoms;
  }
};

struct mjv_makeLights {
  static constexpr char name[] = "mjv_makeLights";
  static constexpr char doc[] = "Make list of lights.";
  using type = void (const mjModel *, const mjData *, mjvScene *);
  static constexpr auto param_names = std::make_tuple("m", "d", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_makeLights;
  }
};

struct mjv_updateCamera {
  static constexpr char name[] = "mjv_updateCamera";
  static constexpr char doc[] = "Update camera.";
  using type = void (const mjModel *, const mjData *, mjvCamera *, mjvScene *);
  static constexpr auto param_names = std::make_tuple("m", "d", "cam", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_updateCamera;
  }
};

struct mjv_updateSkin {
  static constexpr char name[] = "mjv_updateSkin";
  static constexpr char doc[] = "Update skins.";
  using type = void (const mjModel *, const mjData *, mjvScene *);
  static constexpr auto param_names = std::make_tuple("m", "d", "scn");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjv_updateSkin;
  }
};

struct mjr_defaultContext {
  static constexpr char name[] = "mjr_defaultContext";
  static constexpr char doc[] = "Set default mjrContext.";
  using type = void (mjrContext *);
  static constexpr auto param_names = std::make_tuple("con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_defaultContext;
  }
};

struct mjr_makeContext {
  static constexpr char name[] = "mjr_makeContext";
  static constexpr char doc[] = "Allocate resources in custom OpenGL context; fontscale is mjtFontScale.";
  using type = void (const mjModel *, mjrContext *, int);
  static constexpr auto param_names = std::make_tuple("m", "con", "fontscale");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_makeContext;
  }
};

struct mjr_changeFont {
  static constexpr char name[] = "mjr_changeFont";
  static constexpr char doc[] = "Change font of existing context.";
  using type = void (int, mjrContext *);
  static constexpr auto param_names = std::make_tuple("fontscale", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_changeFont;
  }
};

struct mjr_addAux {
  static constexpr char name[] = "mjr_addAux";
  static constexpr char doc[] = "Add Aux buffer with given index to context; free previous Aux buffer.";
  using type = void (int, int, int, int, mjrContext *);
  static constexpr auto param_names = std::make_tuple("index", "width", "height", "samples", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_addAux;
  }
};

struct mjr_freeContext {
  static constexpr char name[] = "mjr_freeContext";
  static constexpr char doc[] = "Free resources in custom OpenGL context, set to default.";
  using type = void (mjrContext *);
  static constexpr auto param_names = std::make_tuple("con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_freeContext;
  }
};

struct mjr_resizeOffscreen {
  static constexpr char name[] = "mjr_resizeOffscreen";
  static constexpr char doc[] = "Resize offscreen buffers.";
  using type = void (int, int, mjrContext *);
  static constexpr auto param_names = std::make_tuple("width", "height", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_resizeOffscreen;
  }
};

struct mjr_uploadTexture {
  static constexpr char name[] = "mjr_uploadTexture";
  static constexpr char doc[] = "Upload texture to GPU, overwriting previous upload if any.";
  using type = void (const mjModel *, const mjrContext *, int);
  static constexpr auto param_names = std::make_tuple("m", "con", "texid");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_uploadTexture;
  }
};

struct mjr_uploadMesh {
  static constexpr char name[] = "mjr_uploadMesh";
  static constexpr char doc[] = "Upload mesh to GPU, overwriting previous upload if any.";
  using type = void (const mjModel *, const mjrContext *, int);
  static constexpr auto param_names = std::make_tuple("m", "con", "meshid");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_uploadMesh;
  }
};

struct mjr_uploadHField {
  static constexpr char name[] = "mjr_uploadHField";
  static constexpr char doc[] = "Upload height field to GPU, overwriting previous upload if any.";
  using type = void (const mjModel *, const mjrContext *, int);
  static constexpr auto param_names = std::make_tuple("m", "con", "hfieldid");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_uploadHField;
  }
};

struct mjr_restoreBuffer {
  static constexpr char name[] = "mjr_restoreBuffer";
  static constexpr char doc[] = "Make con->currentBuffer current again.";
  using type = void (const mjrContext *);
  static constexpr auto param_names = std::make_tuple("con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_restoreBuffer;
  }
};

struct mjr_setBuffer {
  static constexpr char name[] = "mjr_setBuffer";
  static constexpr char doc[] = "Set OpenGL framebuffer for rendering: mjFB_WINDOW or mjFB_OFFSCREEN. If only one buffer is available, set that buffer and ignore framebuffer argument.";
  using type = void (int, mjrContext *);
  static constexpr auto param_names = std::make_tuple("framebuffer", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_setBuffer;
  }
};

struct mjr_readPixels {
  static constexpr char name[] = "mjr_readPixels";
  static constexpr char doc[] = "Read pixels from current OpenGL framebuffer to client buffer. Viewport is in OpenGL framebuffer; client buffer starts at (0,0).";
  using type = void (unsigned char *, float *, mjrRect, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("rgb", "depth", "viewport", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_readPixels;
  }
};

struct mjr_drawPixels {
  static constexpr char name[] = "mjr_drawPixels";
  static constexpr char doc[] = "Draw pixels from client buffer to current OpenGL framebuffer. Viewport is in OpenGL framebuffer; client buffer starts at (0,0).";
  using type = void (const unsigned char *, const float *, mjrRect, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("rgb", "depth", "viewport", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_drawPixels;
  }
};

struct mjr_blitBuffer {
  static constexpr char name[] = "mjr_blitBuffer";
  static constexpr char doc[] = "Blit from src viewpoint in current framebuffer to dst viewport in other framebuffer. If src, dst have different size and flg_depth==0, color is interpolated with GL_LINEAR.";
  using type = void (mjrRect, mjrRect, int, int, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("src", "dst", "flg_color", "flg_depth", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_blitBuffer;
  }
};

struct mjr_setAux {
  static constexpr char name[] = "mjr_setAux";
  static constexpr char doc[] = "Set Aux buffer for custom OpenGL rendering (call restoreBuffer when done).";
  using type = void (int, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("index", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_setAux;
  }
};

struct mjr_blitAux {
  static constexpr char name[] = "mjr_blitAux";
  static constexpr char doc[] = "Blit from Aux buffer to con->currentBuffer.";
  using type = void (int, mjrRect, int, int, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("index", "src", "left", "bottom", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_blitAux;
  }
};

struct mjr_text {
  static constexpr char name[] = "mjr_text";
  static constexpr char doc[] = "Draw text at (x,y) in relative coordinates; font is mjtFont.";
  using type = void (int, const char *, const mjrContext *, float, float, float, float, float);
  static constexpr auto param_names = std::make_tuple("font", "txt", "con", "x", "y", "r", "g", "b");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_text;
  }
};

struct mjr_overlay {
  static constexpr char name[] = "mjr_overlay";
  static constexpr char doc[] = "Draw text overlay; font is mjtFont; gridpos is mjtGridPos.";
  using type = void (int, int, mjrRect, const char *, const char *, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("font", "gridpos", "viewport", "overlay", "overlay2", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_overlay;
  }
};

struct mjr_maxViewport {
  static constexpr char name[] = "mjr_maxViewport";
  static constexpr char doc[] = "Get maximum viewport for active buffer.";
  using type = mjrRect (const mjrContext *);
  static constexpr auto param_names = std::make_tuple("con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_maxViewport;
  }
};

struct mjr_rectangle {
  static constexpr char name[] = "mjr_rectangle";
  static constexpr char doc[] = "Draw rectangle.";
  using type = void (mjrRect, float, float, float, float);
  static constexpr auto param_names = std::make_tuple("viewport", "r", "g", "b", "a");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_rectangle;
  }
};

struct mjr_label {
  static constexpr char name[] = "mjr_label";
  static constexpr char doc[] = "Draw rectangle with centered text.";
  using type = void (mjrRect, int, const char *, float, float, float, float, float, float, float, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("viewport", "font", "txt", "r", "g", "b", "a", "rt", "gt", "bt", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_label;
  }
};

struct mjr_figure {
  static constexpr char name[] = "mjr_figure";
  static constexpr char doc[] = "Draw 2D figure.";
  using type = void (mjrRect, mjvFigure *, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("viewport", "fig", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_figure;
  }
};

struct mjr_render {
  static constexpr char name[] = "mjr_render";
  static constexpr char doc[] = "Render 3D scene.";
  using type = void (mjrRect, mjvScene *, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("viewport", "scn", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_render;
  }
};

struct mjr_finish {
  static constexpr char name[] = "mjr_finish";
  static constexpr char doc[] = "Call glFinish.";
  using type = void ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_finish;
  }
};

struct mjr_getError {
  static constexpr char name[] = "mjr_getError";
  static constexpr char doc[] = "Call glGetError and return result.";
  using type = int ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_getError;
  }
};

struct mjr_findRect {
  static constexpr char name[] = "mjr_findRect";
  static constexpr char doc[] = "Find first rectangle containing mouse, -1: not found.";
  using type = int (int, int, int, const mjrRect *);
  static constexpr auto param_names = std::make_tuple("x", "y", "nrect", "rect");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjr_findRect;
  }
};

struct mjui_themeSpacing {
  static constexpr char name[] = "mjui_themeSpacing";
  static constexpr char doc[] = "Get builtin UI theme spacing (ind: 0-1).";
  using type = mjuiThemeSpacing (int);
  static constexpr auto param_names = std::make_tuple("ind");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjui_themeSpacing;
  }
};

struct mjui_themeColor {
  static constexpr char name[] = "mjui_themeColor";
  static constexpr char doc[] = "Get builtin UI theme color (ind: 0-3).";
  using type = mjuiThemeColor (int);
  static constexpr auto param_names = std::make_tuple("ind");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjui_themeColor;
  }
};

struct mjui_add {
  static constexpr char name[] = "mjui_add";
  static constexpr char doc[] = "Add definitions to UI.";
  using type = void (mjUI *, const mjuiDef *);
  static constexpr auto param_names = std::make_tuple("ui", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjui_add;
  }
};

struct mjui_addToSection {
  static constexpr char name[] = "mjui_addToSection";
  static constexpr char doc[] = "Add definitions to UI section.";
  using type = void (mjUI *, int, const mjuiDef *);
  static constexpr auto param_names = std::make_tuple("ui", "sect", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjui_addToSection;
  }
};

struct mjui_resize {
  static constexpr char name[] = "mjui_resize";
  static constexpr char doc[] = "Compute UI sizes.";
  using type = void (mjUI *, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("ui", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjui_resize;
  }
};

struct mjui_update {
  static constexpr char name[] = "mjui_update";
  static constexpr char doc[] = "Update specific section/item; -1: update all.";
  using type = void (int, int, const mjUI *, const mjuiState *, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("section", "item", "ui", "state", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjui_update;
  }
};

struct mjui_event {
  static constexpr char name[] = "mjui_event";
  static constexpr char doc[] = "Handle UI event, return pointer to changed item, NULL if no change.";
  using type = mjuiItem * (mjUI *, mjuiState *, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("ui", "state", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjui_event;
  }
};

struct mjui_render {
  static constexpr char name[] = "mjui_render";
  static constexpr char doc[] = "Copy UI image to current buffer.";
  using type = void (mjUI *, const mjuiState *, const mjrContext *);
  static constexpr auto param_names = std::make_tuple("ui", "state", "con");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjui_render;
  }
};

struct mju_warning_i {
  static constexpr char name[] = "mju_warning_i";
  static constexpr char doc[] = "Deprecated: use mju_warning.";
  using type = void (const char *, int);
  static constexpr auto param_names = std::make_tuple("msg", "i");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_warning_i;
  }
};

struct mju_warning_s {
  static constexpr char name[] = "mju_warning_s";
  static constexpr char doc[] = "Deprecated: use mju_warning.";
  using type = void (const char *, const char *);
  static constexpr auto param_names = std::make_tuple("msg", "text");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_warning_s;
  }
};

struct mju_clearHandlers {
  static constexpr char name[] = "mju_clearHandlers";
  static constexpr char doc[] = "Clear user error and memory handlers.";
  using type = void ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_clearHandlers;
  }
};

struct mju_malloc {
  static constexpr char name[] = "mju_malloc";
  static constexpr char doc[] = "Allocate memory; byte-align on 64; pad size to multiple of 64.";
  using type = void * (size_t);
  static constexpr auto param_names = std::make_tuple("size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_malloc;
  }
};

struct mju_free {
  static constexpr char name[] = "mju_free";
  static constexpr char doc[] = "Free memory, using free() by default.";
  using type = void (void *);
  static constexpr auto param_names = std::make_tuple("ptr");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_free;
  }
};

struct mj_warning {
  static constexpr char name[] = "mj_warning";
  static constexpr char doc[] = "High-level warning function: count warnings in mjData, print only the first.";
  using type = void (mjData *, int, int);
  static constexpr auto param_names = std::make_tuple("d", "warning", "info");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mj_warning;
  }
};

struct mju_writeLog {
  static constexpr char name[] = "mju_writeLog";
  static constexpr char doc[] = "Write [datetime, type: message] to MUJOCO_LOG.TXT.";
  using type = void (const char *, const char *);
  static constexpr auto param_names = std::make_tuple("type", "msg");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_writeLog;
  }
};

struct mjs_getError {
  static constexpr char name[] = "mjs_getError";
  static constexpr char doc[] = "Get compiler error message from spec.";
  using type = const char * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getError;
  }
};

struct mjs_isWarning {
  static constexpr char name[] = "mjs_isWarning";
  static constexpr char doc[] = "Return 1 if compiler error is a warning.";
  using type = int (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_isWarning;
  }
};

struct mju_zero3 {
  static constexpr char name[] = "mju_zero3";
  static constexpr char doc[] = "Set res = 0.";
  using type = void (mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_zero3);
  }
};

struct mju_copy3 {
  static constexpr char name[] = "mju_copy3";
  static constexpr char doc[] = "Set res = vec.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "data");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_copy3);
  }
};

struct mju_scl3 {
  static constexpr char name[] = "mju_scl3";
  static constexpr char doc[] = "Set res = vec*scl.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3], mjtNum);
  static constexpr auto param_names = std::make_tuple("res", "vec", "scl");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_scl3);
  }
};

struct mju_add3 {
  static constexpr char name[] = "mju_add3";
  static constexpr char doc[] = "Set res = vec1 + vec2.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "vec1", "vec2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_add3);
  }
};

struct mju_sub3 {
  static constexpr char name[] = "mju_sub3";
  static constexpr char doc[] = "Set res = vec1 - vec2.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "vec1", "vec2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_sub3);
  }
};

struct mju_addTo3 {
  static constexpr char name[] = "mju_addTo3";
  static constexpr char doc[] = "Set res = res + vec.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_addTo3);
  }
};

struct mju_subFrom3 {
  static constexpr char name[] = "mju_subFrom3";
  static constexpr char doc[] = "Set res = res - vec.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_subFrom3);
  }
};

struct mju_addToScl3 {
  static constexpr char name[] = "mju_addToScl3";
  static constexpr char doc[] = "Set res = res + vec*scl.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3], mjtNum);
  static constexpr auto param_names = std::make_tuple("res", "vec", "scl");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_addToScl3);
  }
};

struct mju_addScl3 {
  static constexpr char name[] = "mju_addScl3";
  static constexpr char doc[] = "Set res = vec1 + vec2*scl.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[3], mjtNum);
  static constexpr auto param_names = std::make_tuple("res", "vec1", "vec2", "scl");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_addScl3);
  }
};

struct mju_normalize3 {
  static constexpr char name[] = "mju_normalize3";
  static constexpr char doc[] = "Normalize vector, return length before normalization.";
  using type = mjtNum (mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_normalize3);
  }
};

struct mju_norm3 {
  static constexpr char name[] = "mju_norm3";
  static constexpr char doc[] = "Return vector length (without normalizing the vector).";
  using type = mjtNum (const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_norm3);
  }
};

struct mju_dot3 {
  static constexpr char name[] = "mju_dot3";
  static constexpr char doc[] = "Return dot-product of vec1 and vec2.";
  using type = mjtNum (const mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("vec1", "vec2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_dot3);
  }
};

struct mju_dist3 {
  static constexpr char name[] = "mju_dist3";
  static constexpr char doc[] = "Return Cartesian distance between 3D vectors pos1 and pos2.";
  using type = mjtNum (const mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("pos1", "pos2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_dist3);
  }
};

struct mju_mulMatVec3 {
  static constexpr char name[] = "mju_mulMatVec3";
  static constexpr char doc[] = "Multiply 3-by-3 matrix by vector: res = mat * vec.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[9], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "mat", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_mulMatVec3);
  }
};

struct mju_mulMatTVec3 {
  static constexpr char name[] = "mju_mulMatTVec3";
  static constexpr char doc[] = "Multiply transposed 3-by-3 matrix by vector: res = mat' * vec.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[9], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "mat", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_mulMatTVec3);
  }
};

struct mju_cross {
  static constexpr char name[] = "mju_cross";
  static constexpr char doc[] = "Compute cross-product: res = cross(a, b).";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "a", "b");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_cross);
  }
};

struct mju_zero4 {
  static constexpr char name[] = "mju_zero4";
  static constexpr char doc[] = "Set res = 0.";
  using type = void (mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("res");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_zero4);
  }
};

struct mju_unit4 {
  static constexpr char name[] = "mju_unit4";
  static constexpr char doc[] = "Set res = (1,0,0,0).";
  using type = void (mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("res");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_unit4);
  }
};

struct mju_copy4 {
  static constexpr char name[] = "mju_copy4";
  static constexpr char doc[] = "Set res = vec.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("res", "data");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_copy4);
  }
};

struct mju_normalize4 {
  static constexpr char name[] = "mju_normalize4";
  static constexpr char doc[] = "Normalize vector, return length before normalization.";
  using type = mjtNum (mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_normalize4);
  }
};

struct mju_zero {
  static constexpr char name[] = "mju_zero";
  static constexpr char doc[] = "Set res = 0.";
  using type = void (mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_zero;
  }
};

struct mju_fill {
  static constexpr char name[] = "mju_fill";
  static constexpr char doc[] = "Set res = val.";
  using type = void (mjtNum *, mjtNum, int);
  static constexpr auto param_names = std::make_tuple("res", "val", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_fill;
  }
};

struct mju_copy {
  static constexpr char name[] = "mju_copy";
  static constexpr char doc[] = "Set res = vec.";
  using type = void (mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_copy;
  }
};

struct mju_sum {
  static constexpr char name[] = "mju_sum";
  static constexpr char doc[] = "Return sum(vec).";
  using type = mjtNum (const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_sum;
  }
};

struct mju_L1 {
  static constexpr char name[] = "mju_L1";
  static constexpr char doc[] = "Return L1 norm: sum(abs(vec)).";
  using type = mjtNum (const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_L1;
  }
};

struct mju_scl {
  static constexpr char name[] = "mju_scl";
  static constexpr char doc[] = "Set res = vec*scl.";
  using type = void (mjtNum *, const mjtNum *, mjtNum, int);
  static constexpr auto param_names = std::make_tuple("res", "vec", "scl", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_scl;
  }
};

struct mju_add {
  static constexpr char name[] = "mju_add";
  static constexpr char doc[] = "Set res = vec1 + vec2.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "vec1", "vec2", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_add;
  }
};

struct mju_sub {
  static constexpr char name[] = "mju_sub";
  static constexpr char doc[] = "Set res = vec1 - vec2.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "vec1", "vec2", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_sub;
  }
};

struct mju_addTo {
  static constexpr char name[] = "mju_addTo";
  static constexpr char doc[] = "Set res = res + vec.";
  using type = void (mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_addTo;
  }
};

struct mju_subFrom {
  static constexpr char name[] = "mju_subFrom";
  static constexpr char doc[] = "Set res = res - vec.";
  using type = void (mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_subFrom;
  }
};

struct mju_addToScl {
  static constexpr char name[] = "mju_addToScl";
  static constexpr char doc[] = "Set res = res + vec*scl.";
  using type = void (mjtNum *, const mjtNum *, mjtNum, int);
  static constexpr auto param_names = std::make_tuple("res", "vec", "scl", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_addToScl;
  }
};

struct mju_addScl {
  static constexpr char name[] = "mju_addScl";
  static constexpr char doc[] = "Set res = vec1 + vec2*scl.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, mjtNum, int);
  static constexpr auto param_names = std::make_tuple("res", "vec1", "vec2", "scl", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_addScl;
  }
};

struct mju_normalize {
  static constexpr char name[] = "mju_normalize";
  static constexpr char doc[] = "Normalize vector, return length before normalization.";
  using type = mjtNum (mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_normalize;
  }
};

struct mju_norm {
  static constexpr char name[] = "mju_norm";
  static constexpr char doc[] = "Return vector length (without normalizing vector).";
  using type = mjtNum (const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_norm;
  }
};

struct mju_dot {
  static constexpr char name[] = "mju_dot";
  static constexpr char doc[] = "Return dot-product of vec1 and vec2.";
  using type = mjtNum (const mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("vec1", "vec2", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_dot;
  }
};

struct mju_mulMatVec {
  static constexpr char name[] = "mju_mulMatVec";
  static constexpr char doc[] = "Multiply matrix and vector: res = mat * vec.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int, int);
  static constexpr auto param_names = std::make_tuple("res", "mat", "vec", "nr", "nc");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_mulMatVec;
  }
};

struct mju_mulMatTVec {
  static constexpr char name[] = "mju_mulMatTVec";
  static constexpr char doc[] = "Multiply transposed matrix and vector: res = mat' * vec.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int, int);
  static constexpr auto param_names = std::make_tuple("res", "mat", "vec", "nr", "nc");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_mulMatTVec;
  }
};

struct mju_mulVecMatVec {
  static constexpr char name[] = "mju_mulVecMatVec";
  static constexpr char doc[] = "Multiply square matrix with vectors on both sides: returns vec1' * mat * vec2.";
  using type = mjtNum (const mjtNum *, const mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("vec1", "mat", "vec2", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_mulVecMatVec;
  }
};

struct mju_transpose {
  static constexpr char name[] = "mju_transpose";
  static constexpr char doc[] = "Transpose matrix: res = mat'.";
  using type = void (mjtNum *, const mjtNum *, int, int);
  static constexpr auto param_names = std::make_tuple("res", "mat", "nr", "nc");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_transpose;
  }
};

struct mju_symmetrize {
  static constexpr char name[] = "mju_symmetrize";
  static constexpr char doc[] = "Symmetrize square matrix res = (mat + mat')/2.";
  using type = void (mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "mat", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_symmetrize;
  }
};

struct mju_eye {
  static constexpr char name[] = "mju_eye";
  static constexpr char doc[] = "Set mat to the identity matrix.";
  using type = void (mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("mat", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_eye;
  }
};

struct mju_mulMatMat {
  static constexpr char name[] = "mju_mulMatMat";
  static constexpr char doc[] = "Multiply matrices: res = mat1 * mat2.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int, int, int);
  static constexpr auto param_names = std::make_tuple("res", "mat1", "mat2", "r1", "c1", "c2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_mulMatMat;
  }
};

struct mju_mulMatMatT {
  static constexpr char name[] = "mju_mulMatMatT";
  static constexpr char doc[] = "Multiply matrices, second argument transposed: res = mat1 * mat2'.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int, int, int);
  static constexpr auto param_names = std::make_tuple("res", "mat1", "mat2", "r1", "c1", "r2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_mulMatMatT;
  }
};

struct mju_mulMatTMat {
  static constexpr char name[] = "mju_mulMatTMat";
  static constexpr char doc[] = "Multiply matrices, first argument transposed: res = mat1' * mat2.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int, int, int);
  static constexpr auto param_names = std::make_tuple("res", "mat1", "mat2", "r1", "c1", "c2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_mulMatTMat;
  }
};

struct mju_sqrMatTD {
  static constexpr char name[] = "mju_sqrMatTD";
  static constexpr char doc[] = "Set res = mat' * diag * mat if diag is not NULL, and res = mat' * mat otherwise.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int, int);
  static constexpr auto param_names = std::make_tuple("res", "mat", "diag", "nr", "nc");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_sqrMatTD;
  }
};

struct mju_transformSpatial {
  static constexpr char name[] = "mju_transformSpatial";
  static constexpr char doc[] = "Coordinate transform of 6D motion or force vector in rotation:translation format. rotnew2old is 3-by-3, NULL means no rotation; flg_force specifies force or motion type.";
  using type = void (mjtNum (*)[6], const mjtNum (*)[6], int, const mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[9]);
  static constexpr auto param_names = std::make_tuple("res", "vec", "flg_force", "newpos", "oldpos", "rotnew2old");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_transformSpatial);
  }
};

struct mju_dense2sparse {
  static constexpr char name[] = "mju_dense2sparse";
  static constexpr char doc[] = "Convert matrix from dense to sparse.  nnz is size of res and colind, return 1 if too small, 0 otherwise.";
  using type = int (mjtNum *, const mjtNum *, int, int, int *, int *, int *, int);
  static constexpr auto param_names = std::make_tuple("res", "mat", "nr", "nc", "rownnz", "rowadr", "colind", "nnz");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_dense2sparse;
  }
};

struct mju_sparse2dense {
  static constexpr char name[] = "mju_sparse2dense";
  static constexpr char doc[] = "Convert matrix from sparse to dense.";
  using type = void (mjtNum *, const mjtNum *, int, int, const int *, const int *, const int *);
  static constexpr auto param_names = std::make_tuple("res", "mat", "nr", "nc", "rownnz", "rowadr", "colind");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_sparse2dense;
  }
};

struct mju_rotVecQuat {
  static constexpr char name[] = "mju_rotVecQuat";
  static constexpr char doc[] = "Rotate vector by quaternion.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("res", "vec", "quat");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_rotVecQuat);
  }
};

struct mju_negQuat {
  static constexpr char name[] = "mju_negQuat";
  static constexpr char doc[] = "Conjugate quaternion, corresponding to opposite rotation.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("res", "quat");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_negQuat);
  }
};

struct mju_mulQuat {
  static constexpr char name[] = "mju_mulQuat";
  static constexpr char doc[] = "Multiply quaternions.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[4], const mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("res", "quat1", "quat2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_mulQuat);
  }
};

struct mju_mulQuatAxis {
  static constexpr char name[] = "mju_mulQuatAxis";
  static constexpr char doc[] = "Multiply quaternion and axis.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[4], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "quat", "axis");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_mulQuatAxis);
  }
};

struct mju_axisAngle2Quat {
  static constexpr char name[] = "mju_axisAngle2Quat";
  static constexpr char doc[] = "Convert axisAngle to quaternion.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[3], mjtNum);
  static constexpr auto param_names = std::make_tuple("res", "axis", "angle");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_axisAngle2Quat);
  }
};

struct mju_quat2Vel {
  static constexpr char name[] = "mju_quat2Vel";
  static constexpr char doc[] = "Convert quaternion (corresponding to orientation difference) to 3D velocity.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[4], mjtNum);
  static constexpr auto param_names = std::make_tuple("res", "quat", "dt");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_quat2Vel);
  }
};

struct mju_subQuat {
  static constexpr char name[] = "mju_subQuat";
  static constexpr char doc[] = "Subtract quaternions, express as 3D velocity: qb*quat(res) = qa.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[4], const mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("res", "qa", "qb");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_subQuat);
  }
};

struct mju_quat2Mat {
  static constexpr char name[] = "mju_quat2Mat";
  static constexpr char doc[] = "Convert quaternion to 3D rotation matrix.";
  using type = void (mjtNum (*)[9], const mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("res", "quat");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_quat2Mat);
  }
};

struct mju_mat2Quat {
  static constexpr char name[] = "mju_mat2Quat";
  static constexpr char doc[] = "Convert 3D rotation matrix to quaternion.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[9]);
  static constexpr auto param_names = std::make_tuple("quat", "mat");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_mat2Quat);
  }
};

struct mju_derivQuat {
  static constexpr char name[] = "mju_derivQuat";
  static constexpr char doc[] = "Compute time-derivative of quaternion, given 3D rotational velocity.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[4], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "quat", "vel");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_derivQuat);
  }
};

struct mju_quatIntegrate {
  static constexpr char name[] = "mju_quatIntegrate";
  static constexpr char doc[] = "Integrate quaternion given 3D angular velocity.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[3], mjtNum);
  static constexpr auto param_names = std::make_tuple("quat", "vel", "scale");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_quatIntegrate);
  }
};

struct mju_quatZ2Vec {
  static constexpr char name[] = "mju_quatZ2Vec";
  static constexpr char doc[] = "Construct quaternion performing rotation from z-axis to given vector.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("quat", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_quatZ2Vec);
  }
};

struct mju_mat2Rot {
  static constexpr char name[] = "mju_mat2Rot";
  static constexpr char doc[] = "Extract 3D rotation from an arbitrary 3x3 matrix by refining the input quaternion. Returns the number of iterations required to converge";
  using type = int (mjtNum (*)[4], const mjtNum (*)[9]);
  static constexpr auto param_names = std::make_tuple("quat", "mat");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_mat2Rot);
  }
};

struct mju_euler2Quat {
  static constexpr char name[] = "mju_euler2Quat";
  static constexpr char doc[] = "Convert sequence of Euler angles (radians) to quaternion. seq[0,1,2] must be in 'xyzXYZ', lower/upper-case mean intrinsic/extrinsic rotations.";
  using type = void (mjtNum (*)[4], const mjtNum (*)[3], const char *);
  static constexpr auto param_names = std::make_tuple("quat", "euler", "seq");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_euler2Quat);
  }
};

struct mju_mulPose {
  static constexpr char name[] = "mju_mulPose";
  static constexpr char doc[] = "Multiply two poses.";
  using type = void (mjtNum (*)[3], mjtNum (*)[4], const mjtNum (*)[3], const mjtNum (*)[4], const mjtNum (*)[3], const mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("posres", "quatres", "pos1", "quat1", "pos2", "quat2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_mulPose);
  }
};

struct mju_negPose {
  static constexpr char name[] = "mju_negPose";
  static constexpr char doc[] = "Conjugate pose, corresponding to the opposite spatial transformation.";
  using type = void (mjtNum (*)[3], mjtNum (*)[4], const mjtNum (*)[3], const mjtNum (*)[4]);
  static constexpr auto param_names = std::make_tuple("posres", "quatres", "pos", "quat");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_negPose);
  }
};

struct mju_trnVecPose {
  static constexpr char name[] = "mju_trnVecPose";
  static constexpr char doc[] = "Transform vector by pose.";
  using type = void (mjtNum (*)[3], const mjtNum (*)[3], const mjtNum (*)[4], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("res", "pos", "quat", "vec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_trnVecPose);
  }
};

struct mju_cholFactor {
  static constexpr char name[] = "mju_cholFactor";
  static constexpr char doc[] = "Cholesky decomposition: mat = L*L'; return rank, decomposition performed in-place into mat.";
  using type = int (mjtNum *, int, mjtNum);
  static constexpr auto param_names = std::make_tuple("mat", "n", "mindiag");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_cholFactor;
  }
};

struct mju_cholSolve {
  static constexpr char name[] = "mju_cholSolve";
  static constexpr char doc[] = "Solve (mat*mat') * res = vec, where mat is a Cholesky factor.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "mat", "vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_cholSolve;
  }
};

struct mju_cholUpdate {
  static constexpr char name[] = "mju_cholUpdate";
  static constexpr char doc[] = "Cholesky rank-one update: L*L' +/- x*x'; return rank.";
  using type = int (mjtNum *, mjtNum *, int, int);
  static constexpr auto param_names = std::make_tuple("mat", "x", "n", "flg_plus");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_cholUpdate;
  }
};

struct mju_cholFactorBand {
  static constexpr char name[] = "mju_cholFactorBand";
  static constexpr char doc[] = "Band-dense Cholesky decomposition.  Returns minimum value in the factorized diagonal, or 0 if rank-deficient.  mat has (ntotal-ndense) x nband + ndense x ntotal elements.  The first (ntotal-ndense) x nband store the band part, left of diagonal, inclusive.  The second ndense x ntotal store the band part as entire dense rows.  Add diagadd+diagmul*mat_ii to diagonal before factorization.";
  using type = mjtNum (mjtNum *, int, int, int, mjtNum, mjtNum);
  static constexpr auto param_names = std::make_tuple("mat", "ntotal", "nband", "ndense", "diagadd", "diagmul");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_cholFactorBand;
  }
};

struct mju_cholSolveBand {
  static constexpr char name[] = "mju_cholSolveBand";
  static constexpr char doc[] = "Solve (mat*mat')*res = vec where mat is a band-dense Cholesky factor.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int, int, int);
  static constexpr auto param_names = std::make_tuple("res", "mat", "vec", "ntotal", "nband", "ndense");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_cholSolveBand;
  }
};

struct mju_band2Dense {
  static constexpr char name[] = "mju_band2Dense";
  static constexpr char doc[] = "Convert banded matrix to dense matrix, fill upper triangle if flg_sym>0.";
  using type = void (mjtNum *, const mjtNum *, int, int, int, mjtByte);
  static constexpr auto param_names = std::make_tuple("res", "mat", "ntotal", "nband", "ndense", "flg_sym");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_band2Dense;
  }
};

struct mju_dense2Band {
  static constexpr char name[] = "mju_dense2Band";
  static constexpr char doc[] = "Convert dense matrix to banded matrix.";
  using type = void (mjtNum *, const mjtNum *, int, int, int);
  static constexpr auto param_names = std::make_tuple("res", "mat", "ntotal", "nband", "ndense");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_dense2Band;
  }
};

struct mju_bandMulMatVec {
  static constexpr char name[] = "mju_bandMulMatVec";
  static constexpr char doc[] = "Multiply band-diagonal matrix with nvec vectors, include upper triangle if flg_sym>0.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int, int, int, int, mjtByte);
  static constexpr auto param_names = std::make_tuple("res", "mat", "vec", "ntotal", "nband", "ndense", "nvec", "flg_sym");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_bandMulMatVec;
  }
};

struct mju_bandDiag {
  static constexpr char name[] = "mju_bandDiag";
  static constexpr char doc[] = "Address of diagonal element i in band-dense matrix representation.";
  using type = int (int, int, int, int);
  static constexpr auto param_names = std::make_tuple("i", "ntotal", "nband", "ndense");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_bandDiag;
  }
};

struct mju_eig3 {
  static constexpr char name[] = "mju_eig3";
  static constexpr char doc[] = "Eigenvalue decomposition of symmetric 3x3 matrix, mat = eigvec * diag(eigval) * eigvec'.";
  using type = int (mjtNum (*)[3], mjtNum (*)[9], mjtNum (*)[4], const mjtNum (*)[9]);
  static constexpr auto param_names = std::make_tuple("eigval", "eigvec", "quat", "mat");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_eig3);
  }
};

struct mju_boxQP {
  static constexpr char name[] = "mju_boxQP";
  static constexpr char doc[] = "minimize 0.5*x'*H*x + x'*g  s.t. lower <= x <= upper, return rank or -1 if failed   inputs:     n           - problem dimension     H           - SPD matrix                n*n     g           - bias vector               n     lower       - lower bounds              n     upper       - upper bounds              n     res         - solution warmstart        n   return value:     nfree <= n  - rank of unconstrained subspace, -1 if failure   outputs (required):     res         - solution                  n     R           - subspace Cholesky factor  nfree*nfree    allocated: n*(n+7)   outputs (optional):     index       - set of free dimensions    nfree          allocated: n   notes:     the initial value of res is used to warmstart the solver     R must have allocatd size n*(n+7), but only nfree*nfree values are used in output     index (if given) must have allocated size n, but only nfree values are used in output     only the lower triangles of H and R and are read from and written to, respectively     the convenience function mju_boxQPmalloc allocates the required data structures";
  using type = int (mjtNum *, mjtNum *, int *, const mjtNum *, const mjtNum *, int, const mjtNum *, const mjtNum *);
  static constexpr auto param_names = std::make_tuple("res", "R", "index", "H", "g", "n", "lower", "upper");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_boxQP;
  }
};

struct mju_boxQPmalloc {
  static constexpr char name[] = "mju_boxQPmalloc";
  static constexpr char doc[] = "allocate heap memory for box-constrained Quadratic Program   as in mju_boxQP, index, lower, and upper are optional   free all pointers with mju_free()";
  using type = void (mjtNum * *, mjtNum * *, int * *, mjtNum * *, mjtNum * *, int, mjtNum * *, mjtNum * *);
  static constexpr auto param_names = std::make_tuple("res", "R", "index", "H", "g", "n", "lower", "upper");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_boxQPmalloc;
  }
};

struct mju_muscleGain {
  static constexpr char name[] = "mju_muscleGain";
  static constexpr char doc[] = "Muscle active force, prm = (range[2], force, scale, lmin, lmax, vmax, fpmax, fvmax).";
  using type = mjtNum (mjtNum, mjtNum, const mjtNum (*)[2], mjtNum, const mjtNum (*)[9]);
  static constexpr auto param_names = std::make_tuple("len", "vel", "lengthrange", "acc0", "prm");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_muscleGain);
  }
};

struct mju_muscleBias {
  static constexpr char name[] = "mju_muscleBias";
  static constexpr char doc[] = "Muscle passive force, prm = (range[2], force, scale, lmin, lmax, vmax, fpmax, fvmax).";
  using type = mjtNum (mjtNum, const mjtNum (*)[2], mjtNum, const mjtNum (*)[9]);
  static constexpr auto param_names = std::make_tuple("len", "lengthrange", "acc0", "prm");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_muscleBias);
  }
};

struct mju_muscleDynamics {
  static constexpr char name[] = "mju_muscleDynamics";
  static constexpr char doc[] = "Muscle activation dynamics, prm = (tau_act, tau_deact, smoothing_width).";
  using type = mjtNum (mjtNum, mjtNum, const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("ctrl", "act", "prm");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mju_muscleDynamics);
  }
};

struct mju_encodePyramid {
  static constexpr char name[] = "mju_encodePyramid";
  static constexpr char doc[] = "Convert contact force to pyramid representation.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("pyramid", "force", "mu", "dim");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_encodePyramid;
  }
};

struct mju_decodePyramid {
  static constexpr char name[] = "mju_decodePyramid";
  static constexpr char doc[] = "Convert pyramid representation to contact force.";
  using type = void (mjtNum *, const mjtNum *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("force", "pyramid", "mu", "dim");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_decodePyramid;
  }
};

struct mju_springDamper {
  static constexpr char name[] = "mju_springDamper";
  static constexpr char doc[] = "Integrate spring-damper analytically, return pos(dt).";
  using type = mjtNum (mjtNum, mjtNum, mjtNum, mjtNum, mjtNum);
  static constexpr auto param_names = std::make_tuple("pos0", "vel0", "Kp", "Kv", "dt");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_springDamper;
  }
};

struct mju_min {
  static constexpr char name[] = "mju_min";
  static constexpr char doc[] = "Return min(a,b) with single evaluation of a and b.";
  using type = mjtNum (mjtNum, mjtNum);
  static constexpr auto param_names = std::make_tuple("a", "b");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_min;
  }
};

struct mju_max {
  static constexpr char name[] = "mju_max";
  static constexpr char doc[] = "Return max(a,b) with single evaluation of a and b.";
  using type = mjtNum (mjtNum, mjtNum);
  static constexpr auto param_names = std::make_tuple("a", "b");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_max;
  }
};

struct mju_clip {
  static constexpr char name[] = "mju_clip";
  static constexpr char doc[] = "Clip x to the range [min, max].";
  using type = mjtNum (mjtNum, mjtNum, mjtNum);
  static constexpr auto param_names = std::make_tuple("x", "min", "max");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_clip;
  }
};

struct mju_sign {
  static constexpr char name[] = "mju_sign";
  static constexpr char doc[] = "Return sign of x: +1, -1 or 0.";
  using type = mjtNum (mjtNum);
  static constexpr auto param_names = std::make_tuple("x");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_sign;
  }
};

struct mju_round {
  static constexpr char name[] = "mju_round";
  static constexpr char doc[] = "Round x to nearest integer.";
  using type = int (mjtNum);
  static constexpr auto param_names = std::make_tuple("x");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_round;
  }
};

struct mju_type2Str {
  static constexpr char name[] = "mju_type2Str";
  static constexpr char doc[] = "Convert type id (mjtObj) to type name.";
  using type = const char * (int);
  static constexpr auto param_names = std::make_tuple("type");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_type2Str;
  }
};

struct mju_str2Type {
  static constexpr char name[] = "mju_str2Type";
  static constexpr char doc[] = "Convert type name to type id (mjtObj).";
  using type = int (const char *);
  static constexpr auto param_names = std::make_tuple("str");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_str2Type;
  }
};

struct mju_writeNumBytes {
  static constexpr char name[] = "mju_writeNumBytes";
  static constexpr char doc[] = "Return human readable number of bytes using standard letter suffix.";
  using type = const char * (size_t);
  static constexpr auto param_names = std::make_tuple("nbytes");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_writeNumBytes;
  }
};

struct mju_warningText {
  static constexpr char name[] = "mju_warningText";
  static constexpr char doc[] = "Construct a warning message given the warning type and info.";
  using type = const char * (int, size_t);
  static constexpr auto param_names = std::make_tuple("warning", "info");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_warningText;
  }
};

struct mju_isBad {
  static constexpr char name[] = "mju_isBad";
  static constexpr char doc[] = "Return 1 if nan or abs(x)>mjMAXVAL, 0 otherwise. Used by check functions.";
  using type = int (mjtNum);
  static constexpr auto param_names = std::make_tuple("x");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_isBad;
  }
};

struct mju_isZero {
  static constexpr char name[] = "mju_isZero";
  static constexpr char doc[] = "Return 1 if all elements are 0.";
  using type = int (mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_isZero;
  }
};

struct mju_standardNormal {
  static constexpr char name[] = "mju_standardNormal";
  static constexpr char doc[] = "Standard normal random number generator (optional second number).";
  using type = mjtNum (mjtNum *);
  static constexpr auto param_names = std::make_tuple("num2");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_standardNormal;
  }
};

struct mju_f2n {
  static constexpr char name[] = "mju_f2n";
  static constexpr char doc[] = "Convert from float to mjtNum.";
  using type = void (mjtNum *, const float *, int);
  static constexpr auto param_names = std::make_tuple("res", "vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_f2n;
  }
};

struct mju_n2f {
  static constexpr char name[] = "mju_n2f";
  static constexpr char doc[] = "Convert from mjtNum to float.";
  using type = void (float *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_n2f;
  }
};

struct mju_d2n {
  static constexpr char name[] = "mju_d2n";
  static constexpr char doc[] = "Convert from double to mjtNum.";
  using type = void (mjtNum *, const double *, int);
  static constexpr auto param_names = std::make_tuple("res", "vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_d2n;
  }
};

struct mju_n2d {
  static constexpr char name[] = "mju_n2d";
  static constexpr char doc[] = "Convert from mjtNum to double.";
  using type = void (double *, const mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("res", "vec", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_n2d;
  }
};

struct mju_insertionSort {
  static constexpr char name[] = "mju_insertionSort";
  static constexpr char doc[] = "Insertion sort, resulting list is in increasing order.";
  using type = void (mjtNum *, int);
  static constexpr auto param_names = std::make_tuple("list", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_insertionSort;
  }
};

struct mju_insertionSortInt {
  static constexpr char name[] = "mju_insertionSortInt";
  static constexpr char doc[] = "Integer insertion sort, resulting list is in increasing order.";
  using type = void (int *, int);
  static constexpr auto param_names = std::make_tuple("list", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_insertionSortInt;
  }
};

struct mju_Halton {
  static constexpr char name[] = "mju_Halton";
  static constexpr char doc[] = "Generate Halton sequence.";
  using type = mjtNum (int, int);
  static constexpr auto param_names = std::make_tuple("index", "base");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_Halton;
  }
};

struct mju_strncpy {
  static constexpr char name[] = "mju_strncpy";
  static constexpr char doc[] = "Call strncpy, then set dst[n-1] = 0.";
  using type = char * (char *, const char *, int);
  static constexpr auto param_names = std::make_tuple("dst", "src", "n");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_strncpy;
  }
};

struct mju_sigmoid {
  static constexpr char name[] = "mju_sigmoid";
  static constexpr char doc[] = "Sigmoid function over 0<=x<=1 using quintic polynomial.";
  using type = mjtNum (mjtNum);
  static constexpr auto param_names = std::make_tuple("x");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_sigmoid;
  }
};

struct mjc_getSDF {
  static constexpr char name[] = "mjc_getSDF";
  static constexpr char doc[] = "get sdf from geom id";
  using type = const mjpPlugin * (const mjModel *, int);
  static constexpr auto param_names = std::make_tuple("m", "id");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjc_getSDF;
  }
};

struct mjc_distance {
  static constexpr char name[] = "mjc_distance";
  static constexpr char doc[] = "signed distance function";
  using type = mjtNum (const mjModel *, const mjData *, const mjSDF *, const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("m", "d", "s", "x");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjc_distance);
  }
};

struct mjc_gradient {
  static constexpr char name[] = "mjc_gradient";
  static constexpr char doc[] = "gradient of sdf";
  using type = void (const mjModel *, const mjData *, const mjSDF *, mjtNum (*)[3], const mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("m", "d", "s", "gradient", "x");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjc_gradient);
  }
};

struct mjd_transitionFD {
  static constexpr char name[] = "mjd_transitionFD";
  static constexpr char doc[] = "Finite differenced transition matrices (control theory notation)   d(x_next) = A*dx + B*du   d(sensor) = C*dx + D*du   required output matrix dimensions:      A: (2*nv+na x 2*nv+na)      B: (2*nv+na x nu)      D: (nsensordata x 2*nv+na)      C: (nsensordata x nu)";
  using type = void (const mjModel *, mjData *, mjtNum, mjtByte, mjtNum *, mjtNum *, mjtNum *, mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "d", "eps", "flg_centered", "A", "B", "C", "D");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjd_transitionFD;
  }
};

struct mjd_inverseFD {
  static constexpr char name[] = "mjd_inverseFD";
  static constexpr char doc[] = "Finite differenced Jacobians of (force, sensors) = mj_inverse(state, acceleration)   All outputs are optional. Output dimensions (transposed w.r.t Control Theory convention):     DfDq: (nv x nv)     DfDv: (nv x nv)     DfDa: (nv x nv)     DsDq: (nv x nsensordata)     DsDv: (nv x nsensordata)     DsDa: (nv x nsensordata)     DmDq: (nv x nM)   single-letter shortcuts:     inputs: q=qpos, v=qvel, a=qacc     outputs: f=qfrc_inverse, s=sensordata, m=qM   notes:     optionally computes mass matrix Jacobian DmDq     flg_actuation specifies whether to subtract qfrc_actuator from qfrc_inverse";
  using type = void (const mjModel *, mjData *, mjtNum, mjtByte, mjtNum *, mjtNum *, mjtNum *, mjtNum *, mjtNum *, mjtNum *, mjtNum *);
  static constexpr auto param_names = std::make_tuple("m", "d", "eps", "flg_actuation", "DfDq", "DfDv", "DfDa", "DsDq", "DsDv", "DsDa", "DmDq");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjd_inverseFD;
  }
};

struct mjd_subQuat {
  static constexpr char name[] = "mjd_subQuat";
  static constexpr char doc[] = "Derivatives of mju_subQuat.";
  using type = void (const mjtNum (*)[4], const mjtNum (*)[4], mjtNum (*)[9], mjtNum (*)[9]);
  static constexpr auto param_names = std::make_tuple("qa", "qb", "Da", "Db");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjd_subQuat);
  }
};

struct mjd_quatIntegrate {
  static constexpr char name[] = "mjd_quatIntegrate";
  static constexpr char doc[] = "Derivatives of mju_quatIntegrate.";
  using type = void (const mjtNum (*)[3], mjtNum, mjtNum (*)[9], mjtNum (*)[9], mjtNum (*)[3]);
  static constexpr auto param_names = std::make_tuple("vel", "scale", "Dquat", "Dvel", "Dscale");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjd_quatIntegrate);
  }
};

struct mjp_defaultPlugin {
  static constexpr char name[] = "mjp_defaultPlugin";
  static constexpr char doc[] = "Set default plugin definition.";
  using type = void (mjpPlugin *);
  static constexpr auto param_names = std::make_tuple("plugin");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_defaultPlugin;
  }
};

struct mjp_registerPlugin {
  static constexpr char name[] = "mjp_registerPlugin";
  static constexpr char doc[] = "Globally register a plugin. This function is thread-safe. If an identical mjpPlugin is already registered, this function does nothing. If a non-identical mjpPlugin with the same name is already registered, an mju_error is raised. Two mjpPlugins are considered identical if all member function pointers and numbers are equal, and the name and attribute strings are all identical, however the char pointers to the strings need not be the same.";
  using type = int (const mjpPlugin *);
  static constexpr auto param_names = std::make_tuple("plugin");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_registerPlugin;
  }
};

struct mjp_pluginCount {
  static constexpr char name[] = "mjp_pluginCount";
  static constexpr char doc[] = "Return the number of globally registered plugins.";
  using type = int ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_pluginCount;
  }
};

struct mjp_getPlugin {
  static constexpr char name[] = "mjp_getPlugin";
  static constexpr char doc[] = "Look up a plugin by name. If slot is not NULL, also write its registered slot number into it.";
  using type = const mjpPlugin * (const char *, int *);
  static constexpr auto param_names = std::make_tuple("name", "slot");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_getPlugin;
  }
};

struct mjp_getPluginAtSlot {
  static constexpr char name[] = "mjp_getPluginAtSlot";
  static constexpr char doc[] = "Look up a plugin by the registered slot number that was returned by mjp_registerPlugin.";
  using type = const mjpPlugin * (int);
  static constexpr auto param_names = std::make_tuple("slot");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_getPluginAtSlot;
  }
};

struct mjp_defaultResourceProvider {
  static constexpr char name[] = "mjp_defaultResourceProvider";
  static constexpr char doc[] = "Set default resource provider definition.";
  using type = void (mjpResourceProvider *);
  static constexpr auto param_names = std::make_tuple("provider");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_defaultResourceProvider;
  }
};

struct mjp_registerResourceProvider {
  static constexpr char name[] = "mjp_registerResourceProvider";
  static constexpr char doc[] = "Globally register a resource provider in a thread-safe manner. The provider must have a prefix that is not a sub-prefix or super-prefix of any current registered providers.  This function returns a slot number > 0 on success.";
  using type = int (const mjpResourceProvider *);
  static constexpr auto param_names = std::make_tuple("provider");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_registerResourceProvider;
  }
};

struct mjp_resourceProviderCount {
  static constexpr char name[] = "mjp_resourceProviderCount";
  static constexpr char doc[] = "Return the number of globally registered resource providers.";
  using type = int ();
  static constexpr auto param_names = std::make_tuple();

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_resourceProviderCount;
  }
};

struct mjp_getResourceProvider {
  static constexpr char name[] = "mjp_getResourceProvider";
  static constexpr char doc[] = "Return the resource provider with the prefix that matches against the resource name. If no match, return NULL.";
  using type = const mjpResourceProvider * (const char *);
  static constexpr auto param_names = std::make_tuple("resource_name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_getResourceProvider;
  }
};

struct mjp_getResourceProviderAtSlot {
  static constexpr char name[] = "mjp_getResourceProviderAtSlot";
  static constexpr char doc[] = "Look up a resource provider by slot number returned by mjp_registerResourceProvider. If invalid slot number, return NULL.";
  using type = const mjpResourceProvider * (int);
  static constexpr auto param_names = std::make_tuple("slot");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjp_getResourceProviderAtSlot;
  }
};

struct mju_threadPoolCreate {
  static constexpr char name[] = "mju_threadPoolCreate";
  static constexpr char doc[] = "Create a thread pool with the specified number of threads running.";
  using type = mjThreadPool * (size_t);
  static constexpr auto param_names = std::make_tuple("number_of_threads");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_threadPoolCreate;
  }
};

struct mju_bindThreadPool {
  static constexpr char name[] = "mju_bindThreadPool";
  static constexpr char doc[] = "Adds a thread pool to mjData and configures it for multi-threaded use.";
  using type = void (mjData *, void *);
  static constexpr auto param_names = std::make_tuple("d", "thread_pool");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_bindThreadPool;
  }
};

struct mju_threadPoolEnqueue {
  static constexpr char name[] = "mju_threadPoolEnqueue";
  static constexpr char doc[] = "Enqueue a task in a thread pool.";
  using type = void (mjThreadPool *, mjTask *);
  static constexpr auto param_names = std::make_tuple("thread_pool", "task");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_threadPoolEnqueue;
  }
};

struct mju_threadPoolDestroy {
  static constexpr char name[] = "mju_threadPoolDestroy";
  static constexpr char doc[] = "Destroy a thread pool.";
  using type = void (mjThreadPool *);
  static constexpr auto param_names = std::make_tuple("thread_pool");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_threadPoolDestroy;
  }
};

struct mju_defaultTask {
  static constexpr char name[] = "mju_defaultTask";
  static constexpr char doc[] = "Initialize an mjTask.";
  using type = void (mjTask *);
  static constexpr auto param_names = std::make_tuple("task");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_defaultTask;
  }
};

struct mju_taskJoin {
  static constexpr char name[] = "mju_taskJoin";
  static constexpr char doc[] = "Wait for a task to complete.";
  using type = void (mjTask *);
  static constexpr auto param_names = std::make_tuple("task");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mju_taskJoin;
  }
};

struct mjs_attach {
  static constexpr char name[] = "mjs_attach";
  static constexpr char doc[] = "Attach child to a parent, return the attached element if success or NULL otherwise.";
  using type = mjsElement * (mjsElement *, const mjsElement *, const char *, const char *);
  static constexpr auto param_names = std::make_tuple("parent", "child", "prefix", "suffix");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_attach;
  }
};

struct mjs_addBody {
  static constexpr char name[] = "mjs_addBody";
  static constexpr char doc[] = "Add child body to body, return child.";
  using type = mjsBody * (mjsBody *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("body", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addBody;
  }
};

struct mjs_addSite {
  static constexpr char name[] = "mjs_addSite";
  static constexpr char doc[] = "Add site to body, return site spec.";
  using type = mjsSite * (mjsBody *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("body", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addSite;
  }
};

struct mjs_addJoint {
  static constexpr char name[] = "mjs_addJoint";
  static constexpr char doc[] = "Add joint to body.";
  using type = mjsJoint * (mjsBody *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("body", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addJoint;
  }
};

struct mjs_addFreeJoint {
  static constexpr char name[] = "mjs_addFreeJoint";
  static constexpr char doc[] = "Add freejoint to body.";
  using type = mjsJoint * (mjsBody *);
  static constexpr auto param_names = std::make_tuple("body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addFreeJoint;
  }
};

struct mjs_addGeom {
  static constexpr char name[] = "mjs_addGeom";
  static constexpr char doc[] = "Add geom to body.";
  using type = mjsGeom * (mjsBody *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("body", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addGeom;
  }
};

struct mjs_addCamera {
  static constexpr char name[] = "mjs_addCamera";
  static constexpr char doc[] = "Add camera to body.";
  using type = mjsCamera * (mjsBody *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("body", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addCamera;
  }
};

struct mjs_addLight {
  static constexpr char name[] = "mjs_addLight";
  static constexpr char doc[] = "Add light to body.";
  using type = mjsLight * (mjsBody *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("body", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addLight;
  }
};

struct mjs_addFrame {
  static constexpr char name[] = "mjs_addFrame";
  static constexpr char doc[] = "Add frame to body.";
  using type = mjsFrame * (mjsBody *, mjsFrame *);
  static constexpr auto param_names = std::make_tuple("body", "parentframe");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addFrame;
  }
};

struct mjs_delete {
  static constexpr char name[] = "mjs_delete";
  static constexpr char doc[] = "Remove object corresponding to the given element, return 0 on success.";
  using type = int (mjSpec *, mjsElement *);
  static constexpr auto param_names = std::make_tuple("spec", "element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_delete;
  }
};

struct mjs_addActuator {
  static constexpr char name[] = "mjs_addActuator";
  static constexpr char doc[] = "Add actuator.";
  using type = mjsActuator * (mjSpec *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("s", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addActuator;
  }
};

struct mjs_addSensor {
  static constexpr char name[] = "mjs_addSensor";
  static constexpr char doc[] = "Add sensor.";
  using type = mjsSensor * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addSensor;
  }
};

struct mjs_addFlex {
  static constexpr char name[] = "mjs_addFlex";
  static constexpr char doc[] = "Add flex.";
  using type = mjsFlex * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addFlex;
  }
};

struct mjs_addPair {
  static constexpr char name[] = "mjs_addPair";
  static constexpr char doc[] = "Add contact pair.";
  using type = mjsPair * (mjSpec *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("s", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addPair;
  }
};

struct mjs_addExclude {
  static constexpr char name[] = "mjs_addExclude";
  static constexpr char doc[] = "Add excluded body pair.";
  using type = mjsExclude * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addExclude;
  }
};

struct mjs_addEquality {
  static constexpr char name[] = "mjs_addEquality";
  static constexpr char doc[] = "Add equality.";
  using type = mjsEquality * (mjSpec *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("s", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addEquality;
  }
};

struct mjs_addTendon {
  static constexpr char name[] = "mjs_addTendon";
  static constexpr char doc[] = "Add tendon.";
  using type = mjsTendon * (mjSpec *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("s", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addTendon;
  }
};

struct mjs_wrapSite {
  static constexpr char name[] = "mjs_wrapSite";
  static constexpr char doc[] = "Wrap site using tendon.";
  using type = mjsWrap * (mjsTendon *, const char *);
  static constexpr auto param_names = std::make_tuple("tendon", "name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_wrapSite;
  }
};

struct mjs_wrapGeom {
  static constexpr char name[] = "mjs_wrapGeom";
  static constexpr char doc[] = "Wrap geom using tendon.";
  using type = mjsWrap * (mjsTendon *, const char *, const char *);
  static constexpr auto param_names = std::make_tuple("tendon", "name", "sidesite");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_wrapGeom;
  }
};

struct mjs_wrapJoint {
  static constexpr char name[] = "mjs_wrapJoint";
  static constexpr char doc[] = "Wrap joint using tendon.";
  using type = mjsWrap * (mjsTendon *, const char *, double);
  static constexpr auto param_names = std::make_tuple("tendon", "name", "coef");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_wrapJoint;
  }
};

struct mjs_wrapPulley {
  static constexpr char name[] = "mjs_wrapPulley";
  static constexpr char doc[] = "Wrap pulley using tendon.";
  using type = mjsWrap * (mjsTendon *, double);
  static constexpr auto param_names = std::make_tuple("tendon", "divisor");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_wrapPulley;
  }
};

struct mjs_addNumeric {
  static constexpr char name[] = "mjs_addNumeric";
  static constexpr char doc[] = "Add numeric.";
  using type = mjsNumeric * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addNumeric;
  }
};

struct mjs_addText {
  static constexpr char name[] = "mjs_addText";
  static constexpr char doc[] = "Add text.";
  using type = mjsText * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addText;
  }
};

struct mjs_addTuple {
  static constexpr char name[] = "mjs_addTuple";
  static constexpr char doc[] = "Add tuple.";
  using type = mjsTuple * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addTuple;
  }
};

struct mjs_addKey {
  static constexpr char name[] = "mjs_addKey";
  static constexpr char doc[] = "Add keyframe.";
  using type = mjsKey * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addKey;
  }
};

struct mjs_addPlugin {
  static constexpr char name[] = "mjs_addPlugin";
  static constexpr char doc[] = "Add plugin.";
  using type = mjsPlugin * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addPlugin;
  }
};

struct mjs_addDefault {
  static constexpr char name[] = "mjs_addDefault";
  static constexpr char doc[] = "Add default.";
  using type = mjsDefault * (mjSpec *, const char *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("s", "classname", "parent");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addDefault;
  }
};

struct mjs_setToMotor {
  static constexpr char name[] = "mjs_setToMotor";
  static constexpr char doc[] = "Set actuator to motor, return error if any.";
  using type = const char * (mjsActuator *);
  static constexpr auto param_names = std::make_tuple("actuator");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setToMotor;
  }
};

struct mjs_setToPosition {
  static constexpr char name[] = "mjs_setToPosition";
  static constexpr char doc[] = "Set actuator to position, return error if any.";
  using type = const char * (mjsActuator *, double, double (*)[1], double (*)[1], double (*)[1], double);
  static constexpr auto param_names = std::make_tuple("actuator", "kp", "kv", "dampratio", "timeconst", "inheritrange");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjs_setToPosition);
  }
};

struct mjs_setToIntVelocity {
  static constexpr char name[] = "mjs_setToIntVelocity";
  static constexpr char doc[] = "Set actuator to integrated velocity, return error if any.";
  using type = const char * (mjsActuator *, double, double (*)[1], double (*)[1], double (*)[1], double);
  static constexpr auto param_names = std::make_tuple("actuator", "kp", "kv", "dampratio", "timeconst", "inheritrange");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjs_setToIntVelocity);
  }
};

struct mjs_setToVelocity {
  static constexpr char name[] = "mjs_setToVelocity";
  static constexpr char doc[] = "Set actuator to velocity servo, return error if any.";
  using type = const char * (mjsActuator *, double);
  static constexpr auto param_names = std::make_tuple("actuator", "kv");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setToVelocity;
  }
};

struct mjs_setToDamper {
  static constexpr char name[] = "mjs_setToDamper";
  static constexpr char doc[] = "Set actuator to activate damper, return error if any.";
  using type = const char * (mjsActuator *, double);
  static constexpr auto param_names = std::make_tuple("actuator", "kv");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setToDamper;
  }
};

struct mjs_setToCylinder {
  static constexpr char name[] = "mjs_setToCylinder";
  static constexpr char doc[] = "Set actuator to hydraulic or pneumatic cylinder, return error if any.";
  using type = const char * (mjsActuator *, double, double, double, double);
  static constexpr auto param_names = std::make_tuple("actuator", "timeconst", "bias", "area", "diameter");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setToCylinder;
  }
};

struct mjs_setToMuscle {
  static constexpr char name[] = "mjs_setToMuscle";
  static constexpr char doc[] = "Set actuator to muscle, return error if any.a";
  using type = const char * (mjsActuator *, double (*)[2], double, double (*)[2], double, double, double, double, double, double, double);
  static constexpr auto param_names = std::make_tuple("actuator", "timeconst", "tausmooth", "range", "force", "scale", "lmin", "lmax", "vmax", "fpmax", "fvmax");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjs_setToMuscle);
  }
};

struct mjs_setToAdhesion {
  static constexpr char name[] = "mjs_setToAdhesion";
  static constexpr char doc[] = "Set actuator to active adhesion, return error if any.";
  using type = const char * (mjsActuator *, double);
  static constexpr auto param_names = std::make_tuple("actuator", "gain");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setToAdhesion;
  }
};

struct mjs_addMesh {
  static constexpr char name[] = "mjs_addMesh";
  static constexpr char doc[] = "Add mesh.";
  using type = mjsMesh * (mjSpec *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("s", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addMesh;
  }
};

struct mjs_addHField {
  static constexpr char name[] = "mjs_addHField";
  static constexpr char doc[] = "Add height field.";
  using type = mjsHField * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addHField;
  }
};

struct mjs_addSkin {
  static constexpr char name[] = "mjs_addSkin";
  static constexpr char doc[] = "Add skin.";
  using type = mjsSkin * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addSkin;
  }
};

struct mjs_addTexture {
  static constexpr char name[] = "mjs_addTexture";
  static constexpr char doc[] = "Add texture.";
  using type = mjsTexture * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addTexture;
  }
};

struct mjs_addMaterial {
  static constexpr char name[] = "mjs_addMaterial";
  static constexpr char doc[] = "Add material.";
  using type = mjsMaterial * (mjSpec *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("s", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_addMaterial;
  }
};

struct mjs_getSpec {
  static constexpr char name[] = "mjs_getSpec";
  static constexpr char doc[] = "Get spec from body.";
  using type = mjSpec * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getSpec;
  }
};

struct mjs_findSpec {
  static constexpr char name[] = "mjs_findSpec";
  static constexpr char doc[] = "Find spec (model asset) by name.";
  using type = mjSpec * (mjSpec *, const char *);
  static constexpr auto param_names = std::make_tuple("spec", "name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_findSpec;
  }
};

struct mjs_findBody {
  static constexpr char name[] = "mjs_findBody";
  static constexpr char doc[] = "Find body in spec by name.";
  using type = mjsBody * (mjSpec *, const char *);
  static constexpr auto param_names = std::make_tuple("s", "name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_findBody;
  }
};

struct mjs_findElement {
  static constexpr char name[] = "mjs_findElement";
  static constexpr char doc[] = "Find element in spec by name.";
  using type = mjsElement * (mjSpec *, mjtObj, const char *);
  static constexpr auto param_names = std::make_tuple("s", "type", "name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_findElement;
  }
};

struct mjs_findChild {
  static constexpr char name[] = "mjs_findChild";
  static constexpr char doc[] = "Find child body by name.";
  using type = mjsBody * (mjsBody *, const char *);
  static constexpr auto param_names = std::make_tuple("body", "name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_findChild;
  }
};

struct mjs_getParent {
  static constexpr char name[] = "mjs_getParent";
  static constexpr char doc[] = "Get parent body.";
  using type = mjsBody * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getParent;
  }
};

struct mjs_getFrame {
  static constexpr char name[] = "mjs_getFrame";
  static constexpr char doc[] = "Get parent frame.";
  using type = mjsFrame * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getFrame;
  }
};

struct mjs_findFrame {
  static constexpr char name[] = "mjs_findFrame";
  static constexpr char doc[] = "Find frame by name.";
  using type = mjsFrame * (mjSpec *, const char *);
  static constexpr auto param_names = std::make_tuple("s", "name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_findFrame;
  }
};

struct mjs_getDefault {
  static constexpr char name[] = "mjs_getDefault";
  static constexpr char doc[] = "Get default corresponding to an element.";
  using type = mjsDefault * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getDefault;
  }
};

struct mjs_findDefault {
  static constexpr char name[] = "mjs_findDefault";
  static constexpr char doc[] = "Find default in model by class name.";
  using type = mjsDefault * (mjSpec *, const char *);
  static constexpr auto param_names = std::make_tuple("s", "classname");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_findDefault;
  }
};

struct mjs_getSpecDefault {
  static constexpr char name[] = "mjs_getSpecDefault";
  static constexpr char doc[] = "Get global default from model.";
  using type = mjsDefault * (mjSpec *);
  static constexpr auto param_names = std::make_tuple("s");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getSpecDefault;
  }
};

struct mjs_getId {
  static constexpr char name[] = "mjs_getId";
  static constexpr char doc[] = "Get element id.";
  using type = int (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getId;
  }
};

struct mjs_firstChild {
  static constexpr char name[] = "mjs_firstChild";
  static constexpr char doc[] = "Return body's first child of given type. If recurse is nonzero, also search the body's subtree.";
  using type = mjsElement * (mjsBody *, mjtObj, int);
  static constexpr auto param_names = std::make_tuple("body", "type", "recurse");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_firstChild;
  }
};

struct mjs_nextChild {
  static constexpr char name[] = "mjs_nextChild";
  static constexpr char doc[] = "Return body's next child of the same type; return NULL if child is last. If recurse is nonzero, also search the body's subtree.";
  using type = mjsElement * (mjsBody *, mjsElement *, int);
  static constexpr auto param_names = std::make_tuple("body", "child", "recurse");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_nextChild;
  }
};

struct mjs_firstElement {
  static constexpr char name[] = "mjs_firstElement";
  static constexpr char doc[] = "Return spec's first element of selected type.";
  using type = mjsElement * (mjSpec *, mjtObj);
  static constexpr auto param_names = std::make_tuple("s", "type");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_firstElement;
  }
};

struct mjs_nextElement {
  static constexpr char name[] = "mjs_nextElement";
  static constexpr char doc[] = "Return spec's next element; return NULL if element is last.";
  using type = mjsElement * (mjSpec *, mjsElement *);
  static constexpr auto param_names = std::make_tuple("s", "element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_nextElement;
  }
};

struct mjs_setName {
  static constexpr char name[] = "mjs_setName";
  static constexpr char doc[] = "Set element's name, return 0 on success.";
  using type = int (mjsElement *, const char *);
  static constexpr auto param_names = std::make_tuple("element", "name");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setName;
  }
};

struct mjs_setBuffer {
  static constexpr char name[] = "mjs_setBuffer";
  static constexpr char doc[] = "Copy buffer.";
  using type = void (mjByteVec *, const void *, int);
  static constexpr auto param_names = std::make_tuple("dest", "array", "size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setBuffer;
  }
};

struct mjs_setString {
  static constexpr char name[] = "mjs_setString";
  static constexpr char doc[] = "Copy text to string.";
  using type = void (mjString *, const char *);
  static constexpr auto param_names = std::make_tuple("dest", "text");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setString;
  }
};

struct mjs_setStringVec {
  static constexpr char name[] = "mjs_setStringVec";
  static constexpr char doc[] = "Split text to entries and copy to string vector.";
  using type = void (mjStringVec *, const char *);
  static constexpr auto param_names = std::make_tuple("dest", "text");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setStringVec;
  }
};

struct mjs_setInStringVec {
  static constexpr char name[] = "mjs_setInStringVec";
  static constexpr char doc[] = "Set entry in string vector.";
  using type = mjtByte (mjStringVec *, int, const char *);
  static constexpr auto param_names = std::make_tuple("dest", "i", "text");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setInStringVec;
  }
};

struct mjs_appendString {
  static constexpr char name[] = "mjs_appendString";
  static constexpr char doc[] = "Append text entry to string vector.";
  using type = void (mjStringVec *, const char *);
  static constexpr auto param_names = std::make_tuple("dest", "text");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_appendString;
  }
};

struct mjs_setInt {
  static constexpr char name[] = "mjs_setInt";
  static constexpr char doc[] = "Copy int array to vector.";
  using type = void (mjIntVec *, const int *, int);
  static constexpr auto param_names = std::make_tuple("dest", "array", "size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setInt;
  }
};

struct mjs_appendIntVec {
  static constexpr char name[] = "mjs_appendIntVec";
  static constexpr char doc[] = "Append int array to vector of arrays.";
  using type = void (mjIntVecVec *, const int *, int);
  static constexpr auto param_names = std::make_tuple("dest", "array", "size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_appendIntVec;
  }
};

struct mjs_setFloat {
  static constexpr char name[] = "mjs_setFloat";
  static constexpr char doc[] = "Copy float array to vector.";
  using type = void (mjFloatVec *, const float *, int);
  static constexpr auto param_names = std::make_tuple("dest", "array", "size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setFloat;
  }
};

struct mjs_appendFloatVec {
  static constexpr char name[] = "mjs_appendFloatVec";
  static constexpr char doc[] = "Append float array to vector of arrays.";
  using type = void (mjFloatVecVec *, const float *, int);
  static constexpr auto param_names = std::make_tuple("dest", "array", "size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_appendFloatVec;
  }
};

struct mjs_setDouble {
  static constexpr char name[] = "mjs_setDouble";
  static constexpr char doc[] = "Copy double array to vector.";
  using type = void (mjDoubleVec *, const double *, int);
  static constexpr auto param_names = std::make_tuple("dest", "array", "size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setDouble;
  }
};

struct mjs_setPluginAttributes {
  static constexpr char name[] = "mjs_setPluginAttributes";
  static constexpr char doc[] = "Set plugin attributes.";
  using type = void (mjsPlugin *, void *);
  static constexpr auto param_names = std::make_tuple("plugin", "attributes");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setPluginAttributes;
  }
};

struct mjs_getName {
  static constexpr char name[] = "mjs_getName";
  static constexpr char doc[] = "Get element's name.";
  using type = mjString * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getName;
  }
};

struct mjs_getString {
  static constexpr char name[] = "mjs_getString";
  static constexpr char doc[] = "Get string contents.";
  using type = const char * (const mjString *);
  static constexpr auto param_names = std::make_tuple("source");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getString;
  }
};

struct mjs_getDouble {
  static constexpr char name[] = "mjs_getDouble";
  static constexpr char doc[] = "Get double array contents and optionally its size.";
  using type = const double * (const mjDoubleVec *, int *);
  static constexpr auto param_names = std::make_tuple("source", "size");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getDouble;
  }
};

struct mjs_getPluginAttributes {
  static constexpr char name[] = "mjs_getPluginAttributes";
  static constexpr char doc[] = "Get plugin attributes.";
  using type = const void * (const mjsPlugin *);
  static constexpr auto param_names = std::make_tuple("plugin");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getPluginAttributes;
  }
};

struct mjs_setDefault {
  static constexpr char name[] = "mjs_setDefault";
  static constexpr char doc[] = "Set element's default.";
  using type = void (mjsElement *, const mjsDefault *);
  static constexpr auto param_names = std::make_tuple("element", "def_");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setDefault;
  }
};

struct mjs_setFrame {
  static constexpr char name[] = "mjs_setFrame";
  static constexpr char doc[] = "Set element's enclosing frame, return 0 on success.";
  using type = int (mjsElement *, mjsFrame *);
  static constexpr auto param_names = std::make_tuple("dest", "frame");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setFrame;
  }
};

struct mjs_resolveOrientation {
  static constexpr char name[] = "mjs_resolveOrientation";
  static constexpr char doc[] = "Resolve alternative orientations to quat, return error if any.";
  using type = const char * (double (*)[4], mjtByte, const char *, const mjsOrientation *);
  static constexpr auto param_names = std::make_tuple("quat", "degree", "sequence", "orientation");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return *reinterpret_cast<type*>(&::mjs_resolveOrientation);
  }
};

struct mjs_bodyToFrame {
  static constexpr char name[] = "mjs_bodyToFrame";
  static constexpr char doc[] = "Transform body into a frame.";
  using type = mjsFrame * (mjsBody * *);
  static constexpr auto param_names = std::make_tuple("body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_bodyToFrame;
  }
};

struct mjs_setUserValue {
  static constexpr char name[] = "mjs_setUserValue";
  static constexpr char doc[] = "Set user payload, overriding the existing value for the specified key if present.";
  using type = void (mjsElement *, const char *, const void *);
  static constexpr auto param_names = std::make_tuple("element", "key", "data");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_setUserValue;
  }
};

struct mjs_getUserValue {
  static constexpr char name[] = "mjs_getUserValue";
  static constexpr char doc[] = "Return user payload or NULL if none found.";
  using type = const void * (mjsElement *, const char *);
  static constexpr auto param_names = std::make_tuple("element", "key");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_getUserValue;
  }
};

struct mjs_deleteUserValue {
  static constexpr char name[] = "mjs_deleteUserValue";
  static constexpr char doc[] = "Delete user payload.";
  using type = void (mjsElement *, const char *);
  static constexpr auto param_names = std::make_tuple("element", "key");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_deleteUserValue;
  }
};

struct mjs_defaultSpec {
  static constexpr char name[] = "mjs_defaultSpec";
  static constexpr char doc[] = "Default spec attributes.";
  using type = void (mjSpec *);
  static constexpr auto param_names = std::make_tuple("spec");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultSpec;
  }
};

struct mjs_defaultOrientation {
  static constexpr char name[] = "mjs_defaultOrientation";
  static constexpr char doc[] = "Default orientation attributes.";
  using type = void (mjsOrientation *);
  static constexpr auto param_names = std::make_tuple("orient");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultOrientation;
  }
};

struct mjs_defaultBody {
  static constexpr char name[] = "mjs_defaultBody";
  static constexpr char doc[] = "Default body attributes.";
  using type = void (mjsBody *);
  static constexpr auto param_names = std::make_tuple("body");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultBody;
  }
};

struct mjs_defaultFrame {
  static constexpr char name[] = "mjs_defaultFrame";
  static constexpr char doc[] = "Default frame attributes.";
  using type = void (mjsFrame *);
  static constexpr auto param_names = std::make_tuple("frame");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultFrame;
  }
};

struct mjs_defaultJoint {
  static constexpr char name[] = "mjs_defaultJoint";
  static constexpr char doc[] = "Default joint attributes.";
  using type = void (mjsJoint *);
  static constexpr auto param_names = std::make_tuple("joint");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultJoint;
  }
};

struct mjs_defaultGeom {
  static constexpr char name[] = "mjs_defaultGeom";
  static constexpr char doc[] = "Default geom attributes.";
  using type = void (mjsGeom *);
  static constexpr auto param_names = std::make_tuple("geom");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultGeom;
  }
};

struct mjs_defaultSite {
  static constexpr char name[] = "mjs_defaultSite";
  static constexpr char doc[] = "Default site attributes.";
  using type = void (mjsSite *);
  static constexpr auto param_names = std::make_tuple("site");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultSite;
  }
};

struct mjs_defaultCamera {
  static constexpr char name[] = "mjs_defaultCamera";
  static constexpr char doc[] = "Default camera attributes.";
  using type = void (mjsCamera *);
  static constexpr auto param_names = std::make_tuple("camera");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultCamera;
  }
};

struct mjs_defaultLight {
  static constexpr char name[] = "mjs_defaultLight";
  static constexpr char doc[] = "Default light attributes.";
  using type = void (mjsLight *);
  static constexpr auto param_names = std::make_tuple("light");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultLight;
  }
};

struct mjs_defaultFlex {
  static constexpr char name[] = "mjs_defaultFlex";
  static constexpr char doc[] = "Default flex attributes.";
  using type = void (mjsFlex *);
  static constexpr auto param_names = std::make_tuple("flex");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultFlex;
  }
};

struct mjs_defaultMesh {
  static constexpr char name[] = "mjs_defaultMesh";
  static constexpr char doc[] = "Default mesh attributes.";
  using type = void (mjsMesh *);
  static constexpr auto param_names = std::make_tuple("mesh");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultMesh;
  }
};

struct mjs_defaultHField {
  static constexpr char name[] = "mjs_defaultHField";
  static constexpr char doc[] = "Default height field attributes.";
  using type = void (mjsHField *);
  static constexpr auto param_names = std::make_tuple("hfield");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultHField;
  }
};

struct mjs_defaultSkin {
  static constexpr char name[] = "mjs_defaultSkin";
  static constexpr char doc[] = "Default skin attributes.";
  using type = void (mjsSkin *);
  static constexpr auto param_names = std::make_tuple("skin");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultSkin;
  }
};

struct mjs_defaultTexture {
  static constexpr char name[] = "mjs_defaultTexture";
  static constexpr char doc[] = "Default texture attributes.";
  using type = void (mjsTexture *);
  static constexpr auto param_names = std::make_tuple("texture");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultTexture;
  }
};

struct mjs_defaultMaterial {
  static constexpr char name[] = "mjs_defaultMaterial";
  static constexpr char doc[] = "Default material attributes.";
  using type = void (mjsMaterial *);
  static constexpr auto param_names = std::make_tuple("material");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultMaterial;
  }
};

struct mjs_defaultPair {
  static constexpr char name[] = "mjs_defaultPair";
  static constexpr char doc[] = "Default pair attributes.";
  using type = void (mjsPair *);
  static constexpr auto param_names = std::make_tuple("pair");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultPair;
  }
};

struct mjs_defaultEquality {
  static constexpr char name[] = "mjs_defaultEquality";
  static constexpr char doc[] = "Default equality attributes.";
  using type = void (mjsEquality *);
  static constexpr auto param_names = std::make_tuple("equality");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultEquality;
  }
};

struct mjs_defaultTendon {
  static constexpr char name[] = "mjs_defaultTendon";
  static constexpr char doc[] = "Default tendon attributes.";
  using type = void (mjsTendon *);
  static constexpr auto param_names = std::make_tuple("tendon");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultTendon;
  }
};

struct mjs_defaultActuator {
  static constexpr char name[] = "mjs_defaultActuator";
  static constexpr char doc[] = "Default actuator attributes.";
  using type = void (mjsActuator *);
  static constexpr auto param_names = std::make_tuple("actuator");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultActuator;
  }
};

struct mjs_defaultSensor {
  static constexpr char name[] = "mjs_defaultSensor";
  static constexpr char doc[] = "Default sensor attributes.";
  using type = void (mjsSensor *);
  static constexpr auto param_names = std::make_tuple("sensor");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultSensor;
  }
};

struct mjs_defaultNumeric {
  static constexpr char name[] = "mjs_defaultNumeric";
  static constexpr char doc[] = "Default numeric attributes.";
  using type = void (mjsNumeric *);
  static constexpr auto param_names = std::make_tuple("numeric");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultNumeric;
  }
};

struct mjs_defaultText {
  static constexpr char name[] = "mjs_defaultText";
  static constexpr char doc[] = "Default text attributes.";
  using type = void (mjsText *);
  static constexpr auto param_names = std::make_tuple("text");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultText;
  }
};

struct mjs_defaultTuple {
  static constexpr char name[] = "mjs_defaultTuple";
  static constexpr char doc[] = "Default tuple attributes.";
  using type = void (mjsTuple *);
  static constexpr auto param_names = std::make_tuple("tuple");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultTuple;
  }
};

struct mjs_defaultKey {
  static constexpr char name[] = "mjs_defaultKey";
  static constexpr char doc[] = "Default keyframe attributes.";
  using type = void (mjsKey *);
  static constexpr auto param_names = std::make_tuple("key");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultKey;
  }
};

struct mjs_defaultPlugin {
  static constexpr char name[] = "mjs_defaultPlugin";
  static constexpr char doc[] = "Default plugin attributes.";
  using type = void (mjsPlugin *);
  static constexpr auto param_names = std::make_tuple("plugin");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_defaultPlugin;
  }
};

struct mjs_asBody {
  static constexpr char name[] = "mjs_asBody";
  static constexpr char doc[] = "Safely cast an element as mjsBody, or return NULL if the element is not an mjsBody.";
  using type = mjsBody * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asBody;
  }
};

struct mjs_asGeom {
  static constexpr char name[] = "mjs_asGeom";
  static constexpr char doc[] = "Safely cast an element as mjsGeom, or return NULL if the element is not an mjsGeom.";
  using type = mjsGeom * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asGeom;
  }
};

struct mjs_asJoint {
  static constexpr char name[] = "mjs_asJoint";
  static constexpr char doc[] = "Safely cast an element as mjsJoint, or return NULL if the element is not an mjsJoint.";
  using type = mjsJoint * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asJoint;
  }
};

struct mjs_asSite {
  static constexpr char name[] = "mjs_asSite";
  static constexpr char doc[] = "Safely cast an element as mjsSite, or return NULL if the element is not an mjsSite.";
  using type = mjsSite * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asSite;
  }
};

struct mjs_asCamera {
  static constexpr char name[] = "mjs_asCamera";
  static constexpr char doc[] = "Safely cast an element as mjsCamera, or return NULL if the element is not an mjsCamera.";
  using type = mjsCamera * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asCamera;
  }
};

struct mjs_asLight {
  static constexpr char name[] = "mjs_asLight";
  static constexpr char doc[] = "Safely cast an element as mjsLight, or return NULL if the element is not an mjsLight.";
  using type = mjsLight * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asLight;
  }
};

struct mjs_asFrame {
  static constexpr char name[] = "mjs_asFrame";
  static constexpr char doc[] = "Safely cast an element as mjsFrame, or return NULL if the element is not an mjsFrame.";
  using type = mjsFrame * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asFrame;
  }
};

struct mjs_asActuator {
  static constexpr char name[] = "mjs_asActuator";
  static constexpr char doc[] = "Safely cast an element as mjsActuator, or return NULL if the element is not an mjsActuator.";
  using type = mjsActuator * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asActuator;
  }
};

struct mjs_asSensor {
  static constexpr char name[] = "mjs_asSensor";
  static constexpr char doc[] = "Safely cast an element as mjsSensor, or return NULL if the element is not an mjsSensor.";
  using type = mjsSensor * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asSensor;
  }
};

struct mjs_asFlex {
  static constexpr char name[] = "mjs_asFlex";
  static constexpr char doc[] = "Safely cast an element as mjsFlex, or return NULL if the element is not an mjsFlex.";
  using type = mjsFlex * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asFlex;
  }
};

struct mjs_asPair {
  static constexpr char name[] = "mjs_asPair";
  static constexpr char doc[] = "Safely cast an element as mjsPair, or return NULL if the element is not an mjsPair.";
  using type = mjsPair * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asPair;
  }
};

struct mjs_asEquality {
  static constexpr char name[] = "mjs_asEquality";
  static constexpr char doc[] = "Safely cast an element as mjsEquality, or return NULL if the element is not an mjsEquality.";
  using type = mjsEquality * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asEquality;
  }
};

struct mjs_asExclude {
  static constexpr char name[] = "mjs_asExclude";
  static constexpr char doc[] = "Safely cast an element as mjsExclude, or return NULL if the element is not an mjsExclude.";
  using type = mjsExclude * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asExclude;
  }
};

struct mjs_asTendon {
  static constexpr char name[] = "mjs_asTendon";
  static constexpr char doc[] = "Safely cast an element as mjsTendon, or return NULL if the element is not an mjsTendon.";
  using type = mjsTendon * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asTendon;
  }
};

struct mjs_asNumeric {
  static constexpr char name[] = "mjs_asNumeric";
  static constexpr char doc[] = "Safely cast an element as mjsNumeric, or return NULL if the element is not an mjsNumeric.";
  using type = mjsNumeric * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asNumeric;
  }
};

struct mjs_asText {
  static constexpr char name[] = "mjs_asText";
  static constexpr char doc[] = "Safely cast an element as mjsText, or return NULL if the element is not an mjsText.";
  using type = mjsText * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asText;
  }
};

struct mjs_asTuple {
  static constexpr char name[] = "mjs_asTuple";
  static constexpr char doc[] = "Safely cast an element as mjsTuple, or return NULL if the element is not an mjsTuple.";
  using type = mjsTuple * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asTuple;
  }
};

struct mjs_asKey {
  static constexpr char name[] = "mjs_asKey";
  static constexpr char doc[] = "Safely cast an element as mjsKey, or return NULL if the element is not an mjsKey.";
  using type = mjsKey * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asKey;
  }
};

struct mjs_asMesh {
  static constexpr char name[] = "mjs_asMesh";
  static constexpr char doc[] = "Safely cast an element as mjsMesh, or return NULL if the element is not an mjsMesh.";
  using type = mjsMesh * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asMesh;
  }
};

struct mjs_asHField {
  static constexpr char name[] = "mjs_asHField";
  static constexpr char doc[] = "Safely cast an element as mjsHField, or return NULL if the element is not an mjsHField.";
  using type = mjsHField * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asHField;
  }
};

struct mjs_asSkin {
  static constexpr char name[] = "mjs_asSkin";
  static constexpr char doc[] = "Safely cast an element as mjsSkin, or return NULL if the element is not an mjsSkin.";
  using type = mjsSkin * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asSkin;
  }
};

struct mjs_asTexture {
  static constexpr char name[] = "mjs_asTexture";
  static constexpr char doc[] = "Safely cast an element as mjsTexture, or return NULL if the element is not an mjsTexture.";
  using type = mjsTexture * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asTexture;
  }
};

struct mjs_asMaterial {
  static constexpr char name[] = "mjs_asMaterial";
  static constexpr char doc[] = "Safely cast an element as mjsMaterial, or return NULL if the element is not an mjsMaterial.";
  using type = mjsMaterial * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asMaterial;
  }
};

struct mjs_asPlugin {
  static constexpr char name[] = "mjs_asPlugin";
  static constexpr char doc[] = "Safely cast an element as mjsPlugin, or return NULL if the element is not an mjsPlugin.";
  using type = mjsPlugin * (mjsElement *);
  static constexpr auto param_names = std::make_tuple("element");

  MUJOCO_ALWAYS_INLINE static type& GetFunc() {
    return ::mjs_asPlugin;
  }
};

}  // namespace mujoco::python_traits

#endif  // MUJOCO_PYTHON_CODEGEN_FUNCTION_TRAITS_H_

