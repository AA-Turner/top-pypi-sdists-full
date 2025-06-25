// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Tue Jun 24 16:37:55 2025";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "056da052";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.2";
  return version;
}

}  // namespace sherpa_onnx
