// sherpa-onnx/csrc/version.h
//
// Copyright      2025  Xiaomi Corporation

#include "sherpa-onnx/csrc/version.h"

namespace sherpa_onnx {

const char *GetGitDate() {
  static const char *date = "Sun Feb 15 09:33:22 2026";
  return date;
}

const char *GetGitSha1() {
  static const char *sha1 = "f7bcbf3d";
  return sha1;
}

const char *GetVersionStr() {
  static const char *version = "1.12.25";
  return version;
}

}  // namespace sherpa_onnx
