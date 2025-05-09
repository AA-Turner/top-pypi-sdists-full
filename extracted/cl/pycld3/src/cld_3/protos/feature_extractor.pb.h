// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: feature_extractor.proto

#ifndef PROTOBUF_feature_5fextractor_2eproto__INCLUDED
#define PROTOBUF_feature_5fextractor_2eproto__INCLUDED

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 3000000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 3000000 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/message_lite.h>
#include <google/protobuf/repeated_field.h>
#include <google/protobuf/extension_set.h>
// @@protoc_insertion_point(includes)

namespace chrome_lang_id {

// Internal implementation detail -- do not call these.
void protobuf_AddDesc_feature_5fextractor_2eproto();
void protobuf_AssignDesc_feature_5fextractor_2eproto();
void protobuf_ShutdownFile_feature_5fextractor_2eproto();

class FeatureExtractorDescriptor;
class FeatureFunctionDescriptor;
class Parameter;

// ===================================================================

class Parameter : public ::google::protobuf::MessageLite /* @@protoc_insertion_point(class_definition:chrome_lang_id.Parameter) */ {
 public:
  Parameter();
  virtual ~Parameter();

  Parameter(const Parameter& from);

  inline Parameter& operator=(const Parameter& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::std::string& unknown_fields() const {
    return _unknown_fields_.GetNoArena(
        &::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }

  inline ::std::string* mutable_unknown_fields() {
    return _unknown_fields_.MutableNoArena(
        &::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }

  static const Parameter& default_instance();

  #ifdef GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER
  // Returns the internal default instance pointer. This function can
  // return NULL thus should not be used by the user. This is intended
  // for Protobuf internal code. Please use default_instance() declared
  // above instead.
  static inline const Parameter* internal_default_instance() {
    return default_instance_;
  }
  #endif

  void Swap(Parameter* other);

  // implements Message ----------------------------------------------

  inline Parameter* New() const { return New(NULL); }

  Parameter* New(::google::protobuf::Arena* arena) const;
  void CheckTypeAndMergeFrom(const ::google::protobuf::MessageLite& from);
  void CopyFrom(const Parameter& from);
  void MergeFrom(const Parameter& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  void DiscardUnknownFields();
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  void InternalSwap(Parameter* other);
  private:
  inline ::google::protobuf::Arena* GetArenaNoVirtual() const {
    return _arena_ptr_;
  }
  inline ::google::protobuf::Arena* MaybeArenaPtr() const {
    return _arena_ptr_;
  }
  public:

  ::std::string GetTypeName() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // optional string name = 1;
  bool has_name() const;
  void clear_name();
  static const int kNameFieldNumber = 1;
  const ::std::string& name() const;
  void set_name(const ::std::string& value);
  void set_name(const char* value);
  void set_name(const char* value, size_t size);
  ::std::string* mutable_name();
  ::std::string* release_name();
  void set_allocated_name(::std::string* name);

  // optional string value = 2;
  bool has_value() const;
  void clear_value();
  static const int kValueFieldNumber = 2;
  const ::std::string& value() const;
  void set_value(const ::std::string& value);
  void set_value(const char* value);
  void set_value(const char* value, size_t size);
  ::std::string* mutable_value();
  ::std::string* release_value();
  void set_allocated_value(::std::string* value);

  // @@protoc_insertion_point(class_scope:chrome_lang_id.Parameter)
 private:
  inline void set_has_name();
  inline void clear_has_name();
  inline void set_has_value();
  inline void clear_has_value();

  ::google::protobuf::internal::ArenaStringPtr _unknown_fields_;
  ::google::protobuf::Arena* _arena_ptr_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::internal::ArenaStringPtr name_;
  ::google::protobuf::internal::ArenaStringPtr value_;
  #ifdef GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER
  friend void  protobuf_AddDesc_feature_5fextractor_2eproto_impl();
  #else
  friend void  protobuf_AddDesc_feature_5fextractor_2eproto();
  #endif
  friend void protobuf_AssignDesc_feature_5fextractor_2eproto();
  friend void protobuf_ShutdownFile_feature_5fextractor_2eproto();

  void InitAsDefaultInstance();
  static Parameter* default_instance_;
};
// -------------------------------------------------------------------

class FeatureFunctionDescriptor : public ::google::protobuf::MessageLite /* @@protoc_insertion_point(class_definition:chrome_lang_id.FeatureFunctionDescriptor) */ {
 public:
  FeatureFunctionDescriptor();
  virtual ~FeatureFunctionDescriptor();

  FeatureFunctionDescriptor(const FeatureFunctionDescriptor& from);

  inline FeatureFunctionDescriptor& operator=(const FeatureFunctionDescriptor& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::std::string& unknown_fields() const {
    return _unknown_fields_.GetNoArena(
        &::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }

  inline ::std::string* mutable_unknown_fields() {
    return _unknown_fields_.MutableNoArena(
        &::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }

  static const FeatureFunctionDescriptor& default_instance();

  #ifdef GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER
  // Returns the internal default instance pointer. This function can
  // return NULL thus should not be used by the user. This is intended
  // for Protobuf internal code. Please use default_instance() declared
  // above instead.
  static inline const FeatureFunctionDescriptor* internal_default_instance() {
    return default_instance_;
  }
  #endif

  void Swap(FeatureFunctionDescriptor* other);

  // implements Message ----------------------------------------------

  inline FeatureFunctionDescriptor* New() const { return New(NULL); }

  FeatureFunctionDescriptor* New(::google::protobuf::Arena* arena) const;
  void CheckTypeAndMergeFrom(const ::google::protobuf::MessageLite& from);
  void CopyFrom(const FeatureFunctionDescriptor& from);
  void MergeFrom(const FeatureFunctionDescriptor& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  void DiscardUnknownFields();
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  void InternalSwap(FeatureFunctionDescriptor* other);
  private:
  inline ::google::protobuf::Arena* GetArenaNoVirtual() const {
    return _arena_ptr_;
  }
  inline ::google::protobuf::Arena* MaybeArenaPtr() const {
    return _arena_ptr_;
  }
  public:

  ::std::string GetTypeName() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // required string type = 1;
  bool has_type() const;
  void clear_type();
  static const int kTypeFieldNumber = 1;
  const ::std::string& type() const;
  void set_type(const ::std::string& value);
  void set_type(const char* value);
  void set_type(const char* value, size_t size);
  ::std::string* mutable_type();
  ::std::string* release_type();
  void set_allocated_type(::std::string* type);

  // optional string name = 2;
  bool has_name() const;
  void clear_name();
  static const int kNameFieldNumber = 2;
  const ::std::string& name() const;
  void set_name(const ::std::string& value);
  void set_name(const char* value);
  void set_name(const char* value, size_t size);
  ::std::string* mutable_name();
  ::std::string* release_name();
  void set_allocated_name(::std::string* name);

  // optional int32 argument = 3 [default = 0];
  bool has_argument() const;
  void clear_argument();
  static const int kArgumentFieldNumber = 3;
  ::google::protobuf::int32 argument() const;
  void set_argument(::google::protobuf::int32 value);

  // repeated .chrome_lang_id.Parameter parameter = 4;
  int parameter_size() const;
  void clear_parameter();
  static const int kParameterFieldNumber = 4;
  const ::chrome_lang_id::Parameter& parameter(int index) const;
  ::chrome_lang_id::Parameter* mutable_parameter(int index);
  ::chrome_lang_id::Parameter* add_parameter();
  ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::Parameter >*
      mutable_parameter();
  const ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::Parameter >&
      parameter() const;

  // repeated .chrome_lang_id.FeatureFunctionDescriptor feature = 7;
  int feature_size() const;
  void clear_feature();
  static const int kFeatureFieldNumber = 7;
  const ::chrome_lang_id::FeatureFunctionDescriptor& feature(int index) const;
  ::chrome_lang_id::FeatureFunctionDescriptor* mutable_feature(int index);
  ::chrome_lang_id::FeatureFunctionDescriptor* add_feature();
  ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor >*
      mutable_feature();
  const ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor >&
      feature() const;

  // @@protoc_insertion_point(class_scope:chrome_lang_id.FeatureFunctionDescriptor)
 private:
  inline void set_has_type();
  inline void clear_has_type();
  inline void set_has_name();
  inline void clear_has_name();
  inline void set_has_argument();
  inline void clear_has_argument();

  ::google::protobuf::internal::ArenaStringPtr _unknown_fields_;
  ::google::protobuf::Arena* _arena_ptr_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::internal::ArenaStringPtr type_;
  ::google::protobuf::internal::ArenaStringPtr name_;
  ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::Parameter > parameter_;
  ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor > feature_;
  ::google::protobuf::int32 argument_;
  #ifdef GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER
  friend void  protobuf_AddDesc_feature_5fextractor_2eproto_impl();
  #else
  friend void  protobuf_AddDesc_feature_5fextractor_2eproto();
  #endif
  friend void protobuf_AssignDesc_feature_5fextractor_2eproto();
  friend void protobuf_ShutdownFile_feature_5fextractor_2eproto();

  void InitAsDefaultInstance();
  static FeatureFunctionDescriptor* default_instance_;
};
// -------------------------------------------------------------------

class FeatureExtractorDescriptor : public ::google::protobuf::MessageLite /* @@protoc_insertion_point(class_definition:chrome_lang_id.FeatureExtractorDescriptor) */ {
 public:
  FeatureExtractorDescriptor();
  virtual ~FeatureExtractorDescriptor();

  FeatureExtractorDescriptor(const FeatureExtractorDescriptor& from);

  inline FeatureExtractorDescriptor& operator=(const FeatureExtractorDescriptor& from) {
    CopyFrom(from);
    return *this;
  }

  inline const ::std::string& unknown_fields() const {
    return _unknown_fields_.GetNoArena(
        &::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }

  inline ::std::string* mutable_unknown_fields() {
    return _unknown_fields_.MutableNoArena(
        &::google::protobuf::internal::GetEmptyStringAlreadyInited());
  }

  static const FeatureExtractorDescriptor& default_instance();

  #ifdef GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER
  // Returns the internal default instance pointer. This function can
  // return NULL thus should not be used by the user. This is intended
  // for Protobuf internal code. Please use default_instance() declared
  // above instead.
  static inline const FeatureExtractorDescriptor* internal_default_instance() {
    return default_instance_;
  }
  #endif

  void Swap(FeatureExtractorDescriptor* other);

  // implements Message ----------------------------------------------

  inline FeatureExtractorDescriptor* New() const { return New(NULL); }

  FeatureExtractorDescriptor* New(::google::protobuf::Arena* arena) const;
  void CheckTypeAndMergeFrom(const ::google::protobuf::MessageLite& from);
  void CopyFrom(const FeatureExtractorDescriptor& from);
  void MergeFrom(const FeatureExtractorDescriptor& from);
  void Clear();
  bool IsInitialized() const;

  int ByteSize() const;
  bool MergePartialFromCodedStream(
      ::google::protobuf::io::CodedInputStream* input);
  void SerializeWithCachedSizes(
      ::google::protobuf::io::CodedOutputStream* output) const;
  void DiscardUnknownFields();
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const;
  void InternalSwap(FeatureExtractorDescriptor* other);
  private:
  inline ::google::protobuf::Arena* GetArenaNoVirtual() const {
    return _arena_ptr_;
  }
  inline ::google::protobuf::Arena* MaybeArenaPtr() const {
    return _arena_ptr_;
  }
  public:

  ::std::string GetTypeName() const;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  // repeated .chrome_lang_id.FeatureFunctionDescriptor feature = 1;
  int feature_size() const;
  void clear_feature();
  static const int kFeatureFieldNumber = 1;
  const ::chrome_lang_id::FeatureFunctionDescriptor& feature(int index) const;
  ::chrome_lang_id::FeatureFunctionDescriptor* mutable_feature(int index);
  ::chrome_lang_id::FeatureFunctionDescriptor* add_feature();
  ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor >*
      mutable_feature();
  const ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor >&
      feature() const;

  // @@protoc_insertion_point(class_scope:chrome_lang_id.FeatureExtractorDescriptor)
 private:

  ::google::protobuf::internal::ArenaStringPtr _unknown_fields_;
  ::google::protobuf::Arena* _arena_ptr_;

  ::google::protobuf::uint32 _has_bits_[1];
  mutable int _cached_size_;
  ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor > feature_;
  #ifdef GOOGLE_PROTOBUF_NO_STATIC_INITIALIZER
  friend void  protobuf_AddDesc_feature_5fextractor_2eproto_impl();
  #else
  friend void  protobuf_AddDesc_feature_5fextractor_2eproto();
  #endif
  friend void protobuf_AssignDesc_feature_5fextractor_2eproto();
  friend void protobuf_ShutdownFile_feature_5fextractor_2eproto();

  void InitAsDefaultInstance();
  static FeatureExtractorDescriptor* default_instance_;
};
// ===================================================================


// ===================================================================

#if !PROTOBUF_INLINE_NOT_IN_HEADERS
// Parameter

// optional string name = 1;
inline bool Parameter::has_name() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void Parameter::set_has_name() {
  _has_bits_[0] |= 0x00000001u;
}
inline void Parameter::clear_has_name() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void Parameter::clear_name() {
  name_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  clear_has_name();
}
inline const ::std::string& Parameter::name() const {
  // @@protoc_insertion_point(field_get:chrome_lang_id.Parameter.name)
  return name_.GetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void Parameter::set_name(const ::std::string& value) {
  set_has_name();
  name_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:chrome_lang_id.Parameter.name)
}
inline void Parameter::set_name(const char* value) {
  set_has_name();
  name_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:chrome_lang_id.Parameter.name)
}
inline void Parameter::set_name(const char* value, size_t size) {
  set_has_name();
  name_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:chrome_lang_id.Parameter.name)
}
inline ::std::string* Parameter::mutable_name() {
  set_has_name();
  // @@protoc_insertion_point(field_mutable:chrome_lang_id.Parameter.name)
  return name_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* Parameter::release_name() {
  // @@protoc_insertion_point(field_release:chrome_lang_id.Parameter.name)
  clear_has_name();
  return name_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void Parameter::set_allocated_name(::std::string* name) {
  if (name != NULL) {
    set_has_name();
  } else {
    clear_has_name();
  }
  name_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), name);
  // @@protoc_insertion_point(field_set_allocated:chrome_lang_id.Parameter.name)
}

// optional string value = 2;
inline bool Parameter::has_value() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void Parameter::set_has_value() {
  _has_bits_[0] |= 0x00000002u;
}
inline void Parameter::clear_has_value() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void Parameter::clear_value() {
  value_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  clear_has_value();
}
inline const ::std::string& Parameter::value() const {
  // @@protoc_insertion_point(field_get:chrome_lang_id.Parameter.value)
  return value_.GetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void Parameter::set_value(const ::std::string& value) {
  set_has_value();
  value_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:chrome_lang_id.Parameter.value)
}
inline void Parameter::set_value(const char* value) {
  set_has_value();
  value_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:chrome_lang_id.Parameter.value)
}
inline void Parameter::set_value(const char* value, size_t size) {
  set_has_value();
  value_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:chrome_lang_id.Parameter.value)
}
inline ::std::string* Parameter::mutable_value() {
  set_has_value();
  // @@protoc_insertion_point(field_mutable:chrome_lang_id.Parameter.value)
  return value_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* Parameter::release_value() {
  // @@protoc_insertion_point(field_release:chrome_lang_id.Parameter.value)
  clear_has_value();
  return value_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void Parameter::set_allocated_value(::std::string* value) {
  if (value != NULL) {
    set_has_value();
  } else {
    clear_has_value();
  }
  value_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set_allocated:chrome_lang_id.Parameter.value)
}

// -------------------------------------------------------------------

// FeatureFunctionDescriptor

// required string type = 1;
inline bool FeatureFunctionDescriptor::has_type() const {
  return (_has_bits_[0] & 0x00000001u) != 0;
}
inline void FeatureFunctionDescriptor::set_has_type() {
  _has_bits_[0] |= 0x00000001u;
}
inline void FeatureFunctionDescriptor::clear_has_type() {
  _has_bits_[0] &= ~0x00000001u;
}
inline void FeatureFunctionDescriptor::clear_type() {
  type_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  clear_has_type();
}
inline const ::std::string& FeatureFunctionDescriptor::type() const {
  // @@protoc_insertion_point(field_get:chrome_lang_id.FeatureFunctionDescriptor.type)
  return type_.GetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void FeatureFunctionDescriptor::set_type(const ::std::string& value) {
  set_has_type();
  type_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:chrome_lang_id.FeatureFunctionDescriptor.type)
}
inline void FeatureFunctionDescriptor::set_type(const char* value) {
  set_has_type();
  type_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:chrome_lang_id.FeatureFunctionDescriptor.type)
}
inline void FeatureFunctionDescriptor::set_type(const char* value, size_t size) {
  set_has_type();
  type_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:chrome_lang_id.FeatureFunctionDescriptor.type)
}
inline ::std::string* FeatureFunctionDescriptor::mutable_type() {
  set_has_type();
  // @@protoc_insertion_point(field_mutable:chrome_lang_id.FeatureFunctionDescriptor.type)
  return type_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* FeatureFunctionDescriptor::release_type() {
  // @@protoc_insertion_point(field_release:chrome_lang_id.FeatureFunctionDescriptor.type)
  clear_has_type();
  return type_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void FeatureFunctionDescriptor::set_allocated_type(::std::string* type) {
  if (type != NULL) {
    set_has_type();
  } else {
    clear_has_type();
  }
  type_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), type);
  // @@protoc_insertion_point(field_set_allocated:chrome_lang_id.FeatureFunctionDescriptor.type)
}

// optional string name = 2;
inline bool FeatureFunctionDescriptor::has_name() const {
  return (_has_bits_[0] & 0x00000002u) != 0;
}
inline void FeatureFunctionDescriptor::set_has_name() {
  _has_bits_[0] |= 0x00000002u;
}
inline void FeatureFunctionDescriptor::clear_has_name() {
  _has_bits_[0] &= ~0x00000002u;
}
inline void FeatureFunctionDescriptor::clear_name() {
  name_.ClearToEmptyNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
  clear_has_name();
}
inline const ::std::string& FeatureFunctionDescriptor::name() const {
  // @@protoc_insertion_point(field_get:chrome_lang_id.FeatureFunctionDescriptor.name)
  return name_.GetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void FeatureFunctionDescriptor::set_name(const ::std::string& value) {
  set_has_name();
  name_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), value);
  // @@protoc_insertion_point(field_set:chrome_lang_id.FeatureFunctionDescriptor.name)
}
inline void FeatureFunctionDescriptor::set_name(const char* value) {
  set_has_name();
  name_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), ::std::string(value));
  // @@protoc_insertion_point(field_set_char:chrome_lang_id.FeatureFunctionDescriptor.name)
}
inline void FeatureFunctionDescriptor::set_name(const char* value, size_t size) {
  set_has_name();
  name_.SetNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(),
      ::std::string(reinterpret_cast<const char*>(value), size));
  // @@protoc_insertion_point(field_set_pointer:chrome_lang_id.FeatureFunctionDescriptor.name)
}
inline ::std::string* FeatureFunctionDescriptor::mutable_name() {
  set_has_name();
  // @@protoc_insertion_point(field_mutable:chrome_lang_id.FeatureFunctionDescriptor.name)
  return name_.MutableNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline ::std::string* FeatureFunctionDescriptor::release_name() {
  // @@protoc_insertion_point(field_release:chrome_lang_id.FeatureFunctionDescriptor.name)
  clear_has_name();
  return name_.ReleaseNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited());
}
inline void FeatureFunctionDescriptor::set_allocated_name(::std::string* name) {
  if (name != NULL) {
    set_has_name();
  } else {
    clear_has_name();
  }
  name_.SetAllocatedNoArena(&::google::protobuf::internal::GetEmptyStringAlreadyInited(), name);
  // @@protoc_insertion_point(field_set_allocated:chrome_lang_id.FeatureFunctionDescriptor.name)
}

// optional int32 argument = 3 [default = 0];
inline bool FeatureFunctionDescriptor::has_argument() const {
  return (_has_bits_[0] & 0x00000004u) != 0;
}
inline void FeatureFunctionDescriptor::set_has_argument() {
  _has_bits_[0] |= 0x00000004u;
}
inline void FeatureFunctionDescriptor::clear_has_argument() {
  _has_bits_[0] &= ~0x00000004u;
}
inline void FeatureFunctionDescriptor::clear_argument() {
  argument_ = 0;
  clear_has_argument();
}
inline ::google::protobuf::int32 FeatureFunctionDescriptor::argument() const {
  // @@protoc_insertion_point(field_get:chrome_lang_id.FeatureFunctionDescriptor.argument)
  return argument_;
}
inline void FeatureFunctionDescriptor::set_argument(::google::protobuf::int32 value) {
  set_has_argument();
  argument_ = value;
  // @@protoc_insertion_point(field_set:chrome_lang_id.FeatureFunctionDescriptor.argument)
}

// repeated .chrome_lang_id.Parameter parameter = 4;
inline int FeatureFunctionDescriptor::parameter_size() const {
  return parameter_.size();
}
inline void FeatureFunctionDescriptor::clear_parameter() {
  parameter_.Clear();
}
inline const ::chrome_lang_id::Parameter& FeatureFunctionDescriptor::parameter(int index) const {
  // @@protoc_insertion_point(field_get:chrome_lang_id.FeatureFunctionDescriptor.parameter)
  return parameter_.Get(index);
}
inline ::chrome_lang_id::Parameter* FeatureFunctionDescriptor::mutable_parameter(int index) {
  // @@protoc_insertion_point(field_mutable:chrome_lang_id.FeatureFunctionDescriptor.parameter)
  return parameter_.Mutable(index);
}
inline ::chrome_lang_id::Parameter* FeatureFunctionDescriptor::add_parameter() {
  // @@protoc_insertion_point(field_add:chrome_lang_id.FeatureFunctionDescriptor.parameter)
  return parameter_.Add();
}
inline ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::Parameter >*
FeatureFunctionDescriptor::mutable_parameter() {
  // @@protoc_insertion_point(field_mutable_list:chrome_lang_id.FeatureFunctionDescriptor.parameter)
  return &parameter_;
}
inline const ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::Parameter >&
FeatureFunctionDescriptor::parameter() const {
  // @@protoc_insertion_point(field_list:chrome_lang_id.FeatureFunctionDescriptor.parameter)
  return parameter_;
}

// repeated .chrome_lang_id.FeatureFunctionDescriptor feature = 7;
inline int FeatureFunctionDescriptor::feature_size() const {
  return feature_.size();
}
inline void FeatureFunctionDescriptor::clear_feature() {
  feature_.Clear();
}
inline const ::chrome_lang_id::FeatureFunctionDescriptor& FeatureFunctionDescriptor::feature(int index) const {
  // @@protoc_insertion_point(field_get:chrome_lang_id.FeatureFunctionDescriptor.feature)
  return feature_.Get(index);
}
inline ::chrome_lang_id::FeatureFunctionDescriptor* FeatureFunctionDescriptor::mutable_feature(int index) {
  // @@protoc_insertion_point(field_mutable:chrome_lang_id.FeatureFunctionDescriptor.feature)
  return feature_.Mutable(index);
}
inline ::chrome_lang_id::FeatureFunctionDescriptor* FeatureFunctionDescriptor::add_feature() {
  // @@protoc_insertion_point(field_add:chrome_lang_id.FeatureFunctionDescriptor.feature)
  return feature_.Add();
}
inline ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor >*
FeatureFunctionDescriptor::mutable_feature() {
  // @@protoc_insertion_point(field_mutable_list:chrome_lang_id.FeatureFunctionDescriptor.feature)
  return &feature_;
}
inline const ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor >&
FeatureFunctionDescriptor::feature() const {
  // @@protoc_insertion_point(field_list:chrome_lang_id.FeatureFunctionDescriptor.feature)
  return feature_;
}

// -------------------------------------------------------------------

// FeatureExtractorDescriptor

// repeated .chrome_lang_id.FeatureFunctionDescriptor feature = 1;
inline int FeatureExtractorDescriptor::feature_size() const {
  return feature_.size();
}
inline void FeatureExtractorDescriptor::clear_feature() {
  feature_.Clear();
}
inline const ::chrome_lang_id::FeatureFunctionDescriptor& FeatureExtractorDescriptor::feature(int index) const {
  // @@protoc_insertion_point(field_get:chrome_lang_id.FeatureExtractorDescriptor.feature)
  return feature_.Get(index);
}
inline ::chrome_lang_id::FeatureFunctionDescriptor* FeatureExtractorDescriptor::mutable_feature(int index) {
  // @@protoc_insertion_point(field_mutable:chrome_lang_id.FeatureExtractorDescriptor.feature)
  return feature_.Mutable(index);
}
inline ::chrome_lang_id::FeatureFunctionDescriptor* FeatureExtractorDescriptor::add_feature() {
  // @@protoc_insertion_point(field_add:chrome_lang_id.FeatureExtractorDescriptor.feature)
  return feature_.Add();
}
inline ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor >*
FeatureExtractorDescriptor::mutable_feature() {
  // @@protoc_insertion_point(field_mutable_list:chrome_lang_id.FeatureExtractorDescriptor.feature)
  return &feature_;
}
inline const ::google::protobuf::RepeatedPtrField< ::chrome_lang_id::FeatureFunctionDescriptor >&
FeatureExtractorDescriptor::feature() const {
  // @@protoc_insertion_point(field_list:chrome_lang_id.FeatureExtractorDescriptor.feature)
  return feature_;
}

#endif  // !PROTOBUF_INLINE_NOT_IN_HEADERS
// -------------------------------------------------------------------

// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace chrome_lang_id

// @@protoc_insertion_point(global_scope)

#endif  // PROTOBUF_feature_5fextractor_2eproto__INCLUDED
