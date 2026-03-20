// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Thu Mar 19 08:01:53 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "6d8c5090";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.30";
  return version;
}

}  // namespace sherpa_onnx
