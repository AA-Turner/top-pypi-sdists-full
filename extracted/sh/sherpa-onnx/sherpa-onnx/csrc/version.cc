// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

#include "onnxruntime_c_api.h"  // NOLINT

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Tue Aug 11 06:43:30 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "3dc7c569";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.13.5";
  return version;
}

const char *GetOnnxruntimeVersionStr() {
  return OrtGetApiBase()->GetVersionString();
}

}  // namespace sherpa_onnx
