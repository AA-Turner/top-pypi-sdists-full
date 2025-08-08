// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Thu Aug 7 14:19:11 2025";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "bfbd6033";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.7";
  return version;
}

}  // namespace sherpa_onnx
