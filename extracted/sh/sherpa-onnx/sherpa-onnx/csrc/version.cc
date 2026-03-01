// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Sat Feb 28 07:59:52 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "86d3d00e";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.28";
  return version;
}

}  // namespace sherpa_onnx
