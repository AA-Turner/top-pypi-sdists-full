// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Wed Apr 8 12:52:31 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "90f3020f";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.36";
  return version;
}

}  // namespace sherpa_onnx
