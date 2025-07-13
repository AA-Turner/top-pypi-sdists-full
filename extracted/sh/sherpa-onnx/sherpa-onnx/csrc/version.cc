// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Sat Jul 12 12:08:44 2025";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "27098a0e";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.6";
  return version;
}

}  // namespace sherpa_onnx
