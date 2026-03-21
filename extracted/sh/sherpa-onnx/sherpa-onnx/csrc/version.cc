// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Fri Mar 20 11:16:04 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "e0ab4a8b";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.31";
  return version;
}

}  // namespace sherpa_onnx
