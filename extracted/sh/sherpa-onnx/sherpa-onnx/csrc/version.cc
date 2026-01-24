// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Thu Jan 15 08:07:01 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "7e227a52";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.23";
  return version;
}

}  // namespace sherpa_onnx
