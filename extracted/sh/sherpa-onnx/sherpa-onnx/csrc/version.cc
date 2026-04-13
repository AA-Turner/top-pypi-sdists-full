// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Sun Apr 12 13:50:06 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "aacfe96f";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.38";
  return version;
}

}  // namespace sherpa_onnx
