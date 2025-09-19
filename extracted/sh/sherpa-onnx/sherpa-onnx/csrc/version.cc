// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Thu Sep 18 07:09:10 2025";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "26aa2fa9";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.14";
  return version;
}

}  // namespace sherpa_onnx
