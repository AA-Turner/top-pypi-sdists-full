// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Fri Apr 24 10:33:15 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "d795ccd1";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.40";
  return version;
}

}  // namespace sherpa_onnx
