// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Mon Aug 25 03:49:31 2025";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "6b1fbded";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.10";
  return version;
}

}  // namespace sherpa_onnx
