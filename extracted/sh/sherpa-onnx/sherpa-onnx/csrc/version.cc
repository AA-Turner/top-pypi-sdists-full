// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Tue Feb 24 10:48:35 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "174f8684";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.26";
  return version;
}

}  // namespace sherpa_onnx
