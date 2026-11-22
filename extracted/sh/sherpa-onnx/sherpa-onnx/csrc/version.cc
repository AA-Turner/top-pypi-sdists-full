// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

#include "onnxruntime_c_api.h"  // NOLINT

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Sun Nov 22 10:36:20 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "38016c6e";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "2.0.3";
  return version;
}

const char *GetOnnxruntimeVersionStr() {
  return OrtGetApiBase()->GetVersionString();
}

}  // namespace sherpa_onnx
