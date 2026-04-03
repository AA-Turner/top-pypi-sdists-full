// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Fri Apr 3 03:44:41 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "21473b6b";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.35";
  return version;
}

}  // namespace sherpa_onnx
