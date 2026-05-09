// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Sat May 9 02:16:21 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "a2637814";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.13.1";
  return version;
}

}  // namespace sherpa_onnx
