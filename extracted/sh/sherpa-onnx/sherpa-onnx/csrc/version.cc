// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Mon Jun 15 07:50:54 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "330609da";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.13.3";
  return version;
}

}  // namespace sherpa_onnx
