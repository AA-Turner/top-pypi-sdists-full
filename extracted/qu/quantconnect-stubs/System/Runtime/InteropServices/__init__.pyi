from typing import overload
from enum import IntEnum
import abc
import typing
import warnings

import Microsoft.Win32.SafeHandles
import System
import System.Collections
import System.Collections.Generic
import System.Collections.Immutable
import System.Globalization
import System.Numerics
import System.Reflection
import System.Runtime.ConstrainedExecution
import System.Runtime.InteropServices
import System.Runtime.InteropServices.ComTypes
import System.Security

System_Runtime_InteropServices_CULong = typing.Any
System_Runtime_InteropServices_WeakGCHandle = typing.Any
System_Runtime_InteropServices_NFloat = typing.Any
System_Runtime_InteropServices_PinnedGCHandle = typing.Any
System_Runtime_InteropServices_GCHandle = typing.Any
System_Runtime_InteropServices_CLong = typing.Any
System_Runtime_InteropServices_ArrayWithOffset = typing.Any
System_Runtime_InteropServices_OSPlatform = typing.Any

System_Runtime_InteropServices_WeakGCHandle_T = typing.TypeVar("System_Runtime_InteropServices_WeakGCHandle_T")
System_Runtime_InteropServices_TypeMapAttribute_TTypeMapGroup = typing.TypeVar("System_Runtime_InteropServices_TypeMapAttribute_TTypeMapGroup")
System_Runtime_InteropServices_PinnedGCHandle_T = typing.TypeVar("System_Runtime_InteropServices_PinnedGCHandle_T")
System_Runtime_InteropServices_GCHandle_T = typing.TypeVar("System_Runtime_InteropServices_GCHandle_T")
System_Runtime_InteropServices_TypeMapAssociationAttribute_TTypeMapGroup = typing.TypeVar("System_Runtime_InteropServices_TypeMapAssociationAttribute_TTypeMapGroup")
System_Runtime_InteropServices_TypeMapAssemblyTargetAttribute_TTypeMapGroup = typing.TypeVar("System_Runtime_InteropServices_TypeMapAssemblyTargetAttribute_TTypeMapGroup")
System_Runtime_InteropServices_TypeMapping_GetOrCreateExternalTypeMapping_TTypeMapGroup = typing.TypeVar("System_Runtime_InteropServices_TypeMapping_GetOrCreateExternalTypeMapping_TTypeMapGroup")
System_Runtime_InteropServices_TypeMapping_GetOrCreateProxyTypeMapping_TTypeMapGroup = typing.TypeVar("System_Runtime_InteropServices_TypeMapping_GetOrCreateProxyTypeMapping_TTypeMapGroup")
System_Runtime_InteropServices_Marshal_CreateAggregatedObject_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_CreateAggregatedObject_T")
System_Runtime_InteropServices_Marshal_CreateWrapperOfType_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_CreateWrapperOfType_T")
System_Runtime_InteropServices_Marshal_CreateWrapperOfType_TWrapper = typing.TypeVar("System_Runtime_InteropServices_Marshal_CreateWrapperOfType_TWrapper")
System_Runtime_InteropServices_Marshal_GetComInterfaceForObject_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_GetComInterfaceForObject_T")
System_Runtime_InteropServices_Marshal_GetNativeVariantForObject_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_GetNativeVariantForObject_T")
System_Runtime_InteropServices_Marshal_GetObjectForNativeVariant_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_GetObjectForNativeVariant_T")
System_Runtime_InteropServices_Marshal_GetObjectsForNativeVariants_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_GetObjectsForNativeVariants_T")
System_Runtime_InteropServices_Marshal_SizeOf_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_SizeOf_T")
System_Runtime_InteropServices_Marshal_UnsafeAddrOfPinnedArrayElement_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_UnsafeAddrOfPinnedArrayElement_T")
System_Runtime_InteropServices_Marshal_OffsetOf_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_OffsetOf_T")
System_Runtime_InteropServices_Marshal_StructureToPtr_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_StructureToPtr_T")
System_Runtime_InteropServices_Marshal_PtrToStructure_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_PtrToStructure_T")
System_Runtime_InteropServices_Marshal_DestroyStructure_T = typing.TypeVar("System_Runtime_InteropServices_Marshal_DestroyStructure_T")
System_Runtime_InteropServices_Marshal_GetDelegateForFunctionPointer_TDelegate = typing.TypeVar("System_Runtime_InteropServices_Marshal_GetDelegateForFunctionPointer_TDelegate")
System_Runtime_InteropServices_Marshal_GetFunctionPointerForDelegate_TDelegate = typing.TypeVar("System_Runtime_InteropServices_Marshal_GetFunctionPointerForDelegate_TDelegate")
System_Runtime_InteropServices_NFloat_ConvertToInteger_TInteger = typing.TypeVar("System_Runtime_InteropServices_NFloat_ConvertToInteger_TInteger")
System_Runtime_InteropServices_NFloat_ConvertToIntegerNative_TInteger = typing.TypeVar("System_Runtime_InteropServices_NFloat_ConvertToIntegerNative_TInteger")
System_Runtime_InteropServices_NFloat_CreateChecked_TOther = typing.TypeVar("System_Runtime_InteropServices_NFloat_CreateChecked_TOther")
System_Runtime_InteropServices_NFloat_CreateSaturating_TOther = typing.TypeVar("System_Runtime_InteropServices_NFloat_CreateSaturating_TOther")
System_Runtime_InteropServices_NFloat_CreateTruncating_TOther = typing.TypeVar("System_Runtime_InteropServices_NFloat_CreateTruncating_TOther")
System_Runtime_InteropServices_MemoryMarshal_AsBytes_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_AsBytes_T")
System_Runtime_InteropServices_MemoryMarshal_AsMemory_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_AsMemory_T")
System_Runtime_InteropServices_MemoryMarshal_GetReference_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_GetReference_T")
System_Runtime_InteropServices_MemoryMarshal_Cast_TFrom = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_Cast_TFrom")
System_Runtime_InteropServices_MemoryMarshal_Cast_TTo = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_Cast_TTo")
System_Runtime_InteropServices_MemoryMarshal_CreateSpan_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_CreateSpan_T")
System_Runtime_InteropServices_MemoryMarshal_CreateReadOnlySpan_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_CreateReadOnlySpan_T")
System_Runtime_InteropServices_MemoryMarshal_TryGetArray_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_TryGetArray_T")
System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_T")
System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_TManager = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_TManager")
System_Runtime_InteropServices_MemoryMarshal_ToEnumerable_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_ToEnumerable_T")
System_Runtime_InteropServices_MemoryMarshal_Read_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_Read_T")
System_Runtime_InteropServices_MemoryMarshal_TryRead_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_TryRead_T")
System_Runtime_InteropServices_MemoryMarshal_Write_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_Write_T")
System_Runtime_InteropServices_MemoryMarshal_TryWrite_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_TryWrite_T")
System_Runtime_InteropServices_MemoryMarshal_AsRef_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_AsRef_T")
System_Runtime_InteropServices_MemoryMarshal_CreateFromPinnedArray_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_CreateFromPinnedArray_T")
System_Runtime_InteropServices_MemoryMarshal_GetArrayDataReference_T = typing.TypeVar("System_Runtime_InteropServices_MemoryMarshal_GetArrayDataReference_T")
System_Runtime_InteropServices_ComWrappers_GetInstance_ComInterfaceDispatch_T = typing.TypeVar("System_Runtime_InteropServices_ComWrappers_GetInstance_ComInterfaceDispatch_T")
System_Runtime_InteropServices_GCHandleExtensions_GetAddressOfArrayData_T = typing.TypeVar("System_Runtime_InteropServices_GCHandleExtensions_GetAddressOfArrayData_T")
System_Runtime_InteropServices_SafeBuffer_Initialize_T = typing.TypeVar("System_Runtime_InteropServices_SafeBuffer_Initialize_T")
System_Runtime_InteropServices_SafeBuffer_Read_T = typing.TypeVar("System_Runtime_InteropServices_SafeBuffer_Read_T")
System_Runtime_InteropServices_SafeBuffer_ReadArray_T = typing.TypeVar("System_Runtime_InteropServices_SafeBuffer_ReadArray_T")
System_Runtime_InteropServices_SafeBuffer_ReadSpan_T = typing.TypeVar("System_Runtime_InteropServices_SafeBuffer_ReadSpan_T")
System_Runtime_InteropServices_SafeBuffer_Write_T = typing.TypeVar("System_Runtime_InteropServices_SafeBuffer_Write_T")
System_Runtime_InteropServices_SafeBuffer_WriteArray_T = typing.TypeVar("System_Runtime_InteropServices_SafeBuffer_WriteArray_T")
System_Runtime_InteropServices_SafeBuffer_WriteSpan_T = typing.TypeVar("System_Runtime_InteropServices_SafeBuffer_WriteSpan_T")
System_Runtime_InteropServices_CollectionsMarshal_AsSpan_T = typing.TypeVar("System_Runtime_InteropServices_CollectionsMarshal_AsSpan_T")
System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TKey = typing.TypeVar("System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TKey")
System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TAlternateKey = typing.TypeVar("System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TAlternateKey")
System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TValue = typing.TypeVar("System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TValue")
System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TKey = typing.TypeVar("System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TKey")
System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TAlternateKey = typing.TypeVar("System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TAlternateKey")
System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TValue = typing.TypeVar("System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TValue")
System_Runtime_InteropServices_CollectionsMarshal_SetCount_T = typing.TypeVar("System_Runtime_InteropServices_CollectionsMarshal_SetCount_T")
System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsImmutableArray_T = typing.TypeVar("System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsImmutableArray_T")
System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsArray_T = typing.TypeVar("System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsArray_T")
System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsMemory_T = typing.TypeVar("System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsMemory_T")


class Architecture(IntEnum):
    """This class has no documentation."""

    X_86 = 0

    X_64 = 1

    ARM = 2

    ARM_64 = 3

    WASM = 4

    S_390X = 5

    LOONG_ARCH_64 = 6

    ARMV_6 = 7

    PPC_64_LE = 8

    RISC_V_64 = 9


class OSPlatform(System.IEquatable[System_Runtime_InteropServices_OSPlatform]):
    """This class has no documentation."""

    FREE_BSD: System.Runtime.InteropServices.OSPlatform

    LINUX: System.Runtime.InteropServices.OSPlatform

    OSX: System.Runtime.InteropServices.OSPlatform

    WINDOWS: System.Runtime.InteropServices.OSPlatform

    def __eq__(self, right: System.Runtime.InteropServices.OSPlatform) -> bool:
        ...

    def __ne__(self, right: System.Runtime.InteropServices.OSPlatform) -> bool:
        ...

    @staticmethod
    def create(os_platform: str) -> System.Runtime.InteropServices.OSPlatform:
        ...

    @overload
    def equals(self, other: System.Runtime.InteropServices.OSPlatform) -> bool:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    def get_hash_code(self) -> int:
        ...

    def to_string(self) -> str:
        ...


class RuntimeInformation(System.Object):
    """This class has no documentation."""

    OS_DESCRIPTION: str

    OS_ARCHITECTURE: System.Runtime.InteropServices.Architecture

    RUNTIME_IDENTIFIER: str

    process_architecture: System.Runtime.InteropServices.Architecture

    @staticmethod
    def is_os_platform(os_platform: System.Runtime.InteropServices.OSPlatform) -> bool:
        ...


class CULong(System.IEquatable[System_Runtime_InteropServices_CULong]):
    """This class has no documentation."""

    @property
    def value(self) -> System.UIntPtr:
        ...

    @overload
    def __init__(self, value: int) -> None:
        ...

    @overload
    def __init__(self, value: System.UIntPtr) -> None:
        ...

    @overload
    def equals(self, o: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Runtime.InteropServices.CULong) -> bool:
        ...

    def get_hash_code(self) -> int:
        ...

    def to_string(self) -> str:
        ...


class ComEventInterfaceAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def source_interface(self) -> typing.Type:
        ...

    @property
    def event_provider(self) -> typing.Type:
        ...

    def __init__(self, source_interface: typing.Type, event_provider: typing.Type) -> None:
        ...


class OptionalAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class StandardOleMarshalObject(System.MarshalByRefObject, System.Runtime.InteropServices.IMarshal):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class _Typed_TypeMapping_GetOrCreateExternalTypeMapping(typing.Generic[System_Runtime_InteropServices_TypeMapping_GetOrCreateExternalTypeMapping_TTypeMapGroup]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Generic.IReadOnlyDictionary[str, typing.Type]:
        ...


class _TypeMapping_GetOrCreateExternalTypeMapping:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_TypeMapping_GetOrCreateExternalTypeMapping_TTypeMapGroup]) -> System.Runtime.InteropServices._Typed_TypeMapping_GetOrCreateExternalTypeMapping[System_Runtime_InteropServices_TypeMapping_GetOrCreateExternalTypeMapping_TTypeMapGroup]:
        ...


class _Typed_TypeMapping_GetOrCreateProxyTypeMapping(typing.Generic[System_Runtime_InteropServices_TypeMapping_GetOrCreateProxyTypeMapping_TTypeMapGroup]):
    """"""

    @overload
    def __call__(self) -> System.Collections.Generic.IReadOnlyDictionary[typing.Type, typing.Type]:
        ...


class _TypeMapping_GetOrCreateProxyTypeMapping:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_TypeMapping_GetOrCreateProxyTypeMapping_TTypeMapGroup]) -> System.Runtime.InteropServices._Typed_TypeMapping_GetOrCreateProxyTypeMapping[System_Runtime_InteropServices_TypeMapping_GetOrCreateProxyTypeMapping_TTypeMapGroup]:
        ...


class TypeMapping(System.Object):
    """This class has no documentation."""

    get_or_create_external_type_mapping: System.Runtime.InteropServices._TypeMapping_GetOrCreateExternalTypeMapping

    get_or_create_proxy_type_mapping: System.Runtime.InteropServices._TypeMapping_GetOrCreateProxyTypeMapping


class CurrencyWrapper(System.Object):
    """This class has no documentation."""

    @property
    def wrapped_object(self) -> float:
        ...

    @overload
    def __init__(self, obj: float) -> None:
        ...

    @overload
    def __init__(self, obj: typing.Any) -> None:
        ...


class GCHandleType(IntEnum):
    """This class has no documentation."""

    WEAK = 0

    WEAK_TRACK_RESURRECTION = 1

    NORMAL = 2

    PINNED = 3


class ComEventsHelper(System.Object):
    """This class has no documentation."""

    @staticmethod
    def combine(rcw: typing.Any, iid: System.Guid, dispid: int, d: System.Delegate) -> None:
        ...

    @staticmethod
    def remove(rcw: typing.Any, iid: System.Guid, dispid: int, d: System.Delegate) -> System.Delegate:
        ...


class ICustomFactory(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def create_instance(self, server_type: typing.Type) -> System.MarshalByRefObject:
        ...


class _Typed_Marshal_CreateAggregatedObject(typing.Generic[System_Runtime_InteropServices_Marshal_CreateAggregatedObject_T]):
    """"""

    @overload
    def __call__(self, p_outer: System.IntPtr, o: System_Runtime_InteropServices_Marshal_CreateAggregatedObject_T) -> System.IntPtr:
        ...


class _Marshal_CreateAggregatedObject:
    """"""

    @overload
    def __call__(self, p_outer: System.IntPtr, o: typing.Any) -> System.IntPtr:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_CreateAggregatedObject_T]) -> System.Runtime.InteropServices._Typed_Marshal_CreateAggregatedObject[System_Runtime_InteropServices_Marshal_CreateAggregatedObject_T]:
        ...


class _Typed_Marshal_CreateWrapperOfType(typing.Generic[System_Runtime_InteropServices_Marshal_CreateWrapperOfType_T]):
    """"""

    @overload
    def __call__(self, o: System_Runtime_InteropServices_Marshal_CreateWrapperOfType_T) -> System_Runtime_InteropServices_Marshal_CreateWrapperOfType_TWrapper:
        ...


class _Marshal_CreateWrapperOfType:
    """"""

    @overload
    def __call__(self, o: typing.Any, t: typing.Type) -> System.Object:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_CreateWrapperOfType_T]) -> System.Runtime.InteropServices._Typed_Marshal_CreateWrapperOfType[System_Runtime_InteropServices_Marshal_CreateWrapperOfType_T]:
        ...


class CustomQueryInterfaceMode(IntEnum):
    """This class has no documentation."""

    IGNORE = 0

    ALLOW = 1


class _Typed_Marshal_GetComInterfaceForObject(typing.Generic[System_Runtime_InteropServices_Marshal_GetComInterfaceForObject_T]):
    """"""

    @overload
    def __call__(self, o: System_Runtime_InteropServices_Marshal_GetComInterfaceForObject_T) -> System.IntPtr:
        ...


class _Marshal_GetComInterfaceForObject:
    """"""

    @overload
    def __call__(self, o: typing.Any, t: typing.Type) -> System.IntPtr:
        ...

    @overload
    def __call__(self, o: typing.Any, t: typing.Type, mode: System.Runtime.InteropServices.CustomQueryInterfaceMode) -> System.IntPtr:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_GetComInterfaceForObject_T]) -> System.Runtime.InteropServices._Typed_Marshal_GetComInterfaceForObject[System_Runtime_InteropServices_Marshal_GetComInterfaceForObject_T]:
        ...


class _Typed_Marshal_GetNativeVariantForObject(typing.Generic[System_Runtime_InteropServices_Marshal_GetNativeVariantForObject_T]):
    """"""

    @overload
    def __call__(self, obj: System_Runtime_InteropServices_Marshal_GetNativeVariantForObject_T, p_dst_native_variant: System.IntPtr) -> None:
        ...


class _Marshal_GetNativeVariantForObject:
    """"""

    @overload
    def __call__(self, obj: typing.Any, p_dst_native_variant: System.IntPtr) -> None:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_GetNativeVariantForObject_T]) -> System.Runtime.InteropServices._Typed_Marshal_GetNativeVariantForObject[System_Runtime_InteropServices_Marshal_GetNativeVariantForObject_T]:
        ...


class _Typed_Marshal_GetObjectForNativeVariant(typing.Generic[System_Runtime_InteropServices_Marshal_GetObjectForNativeVariant_T]):
    """"""

    @overload
    def __call__(self, p_src_native_variant: System.IntPtr) -> System_Runtime_InteropServices_Marshal_GetObjectForNativeVariant_T:
        ...


class _Marshal_GetObjectForNativeVariant:
    """"""

    @overload
    def __call__(self, p_src_native_variant: System.IntPtr) -> System.Object:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_GetObjectForNativeVariant_T]) -> System.Runtime.InteropServices._Typed_Marshal_GetObjectForNativeVariant[System_Runtime_InteropServices_Marshal_GetObjectForNativeVariant_T]:
        ...


class _Typed_Marshal_GetObjectsForNativeVariants(typing.Generic[System_Runtime_InteropServices_Marshal_GetObjectsForNativeVariants_T]):
    """"""

    @overload
    def __call__(self, a_src_native_variant: System.IntPtr, c_vars: int) -> typing.List[System_Runtime_InteropServices_Marshal_GetObjectsForNativeVariants_T]:
        ...


class _Marshal_GetObjectsForNativeVariants:
    """"""

    @overload
    def __call__(self, a_src_native_variant: System.IntPtr, c_vars: int) -> typing.List[System.Object]:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_GetObjectsForNativeVariants_T]) -> System.Runtime.InteropServices._Typed_Marshal_GetObjectsForNativeVariants[System_Runtime_InteropServices_Marshal_GetObjectsForNativeVariants_T]:
        ...


class _Typed_Marshal_SizeOf(typing.Generic[System_Runtime_InteropServices_Marshal_SizeOf_T]):
    """"""

    @overload
    def __call__(self, structure: System_Runtime_InteropServices_Marshal_SizeOf_T) -> int:
        ...

    @overload
    def __call__(self) -> int:
        ...


class _Marshal_SizeOf:
    """"""

    @overload
    def __call__(self, structure: typing.Any) -> int:
        ...

    @overload
    def __call__(self, t: typing.Type) -> int:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_SizeOf_T]) -> System.Runtime.InteropServices._Typed_Marshal_SizeOf[System_Runtime_InteropServices_Marshal_SizeOf_T]:
        ...


class _Typed_Marshal_UnsafeAddrOfPinnedArrayElement(typing.Generic[System_Runtime_InteropServices_Marshal_UnsafeAddrOfPinnedArrayElement_T]):
    """"""

    @overload
    def __call__(self, arr: typing.List[System_Runtime_InteropServices_Marshal_UnsafeAddrOfPinnedArrayElement_T], index: int) -> System.IntPtr:
        ...


class _Marshal_UnsafeAddrOfPinnedArrayElement:
    """"""

    @overload
    def __call__(self, arr: System.Array, index: int) -> System.IntPtr:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_UnsafeAddrOfPinnedArrayElement_T]) -> System.Runtime.InteropServices._Typed_Marshal_UnsafeAddrOfPinnedArrayElement[System_Runtime_InteropServices_Marshal_UnsafeAddrOfPinnedArrayElement_T]:
        ...


class _Typed_Marshal_OffsetOf(typing.Generic[System_Runtime_InteropServices_Marshal_OffsetOf_T]):
    """"""

    @overload
    def __call__(self, field_name: str) -> System.IntPtr:
        ...


class _Marshal_OffsetOf:
    """"""

    @overload
    def __call__(self, t: typing.Type, field_name: str) -> System.IntPtr:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_OffsetOf_T]) -> System.Runtime.InteropServices._Typed_Marshal_OffsetOf[System_Runtime_InteropServices_Marshal_OffsetOf_T]:
        ...


class _Typed_Marshal_StructureToPtr(typing.Generic[System_Runtime_InteropServices_Marshal_StructureToPtr_T]):
    """"""

    @overload
    def __call__(self, structure: System_Runtime_InteropServices_Marshal_StructureToPtr_T, ptr: System.IntPtr, f_delete_old: bool) -> None:
        ...


class _Marshal_StructureToPtr:
    """"""

    @overload
    def __call__(self, structure: typing.Any, ptr: System.IntPtr, f_delete_old: bool) -> None:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_StructureToPtr_T]) -> System.Runtime.InteropServices._Typed_Marshal_StructureToPtr[System_Runtime_InteropServices_Marshal_StructureToPtr_T]:
        ...


class _Typed_Marshal_PtrToStructure(typing.Generic[System_Runtime_InteropServices_Marshal_PtrToStructure_T]):
    """"""

    @overload
    def __call__(self, ptr: System.IntPtr, structure: System_Runtime_InteropServices_Marshal_PtrToStructure_T) -> None:
        ...

    @overload
    def __call__(self, ptr: System.IntPtr) -> System_Runtime_InteropServices_Marshal_PtrToStructure_T:
        ...


class _Marshal_PtrToStructure:
    """"""

    @overload
    def __call__(self, ptr: System.IntPtr, structure_type: typing.Type) -> System.Object:
        ...

    @overload
    def __call__(self, ptr: System.IntPtr, structure: typing.Any) -> None:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_PtrToStructure_T]) -> System.Runtime.InteropServices._Typed_Marshal_PtrToStructure[System_Runtime_InteropServices_Marshal_PtrToStructure_T]:
        ...


class _Typed_Marshal_DestroyStructure(typing.Generic[System_Runtime_InteropServices_Marshal_DestroyStructure_T]):
    """"""

    @overload
    def __call__(self, ptr: System.IntPtr) -> None:
        ...


class _Marshal_DestroyStructure:
    """"""

    @overload
    def __call__(self, ptr: System.IntPtr, structuretype: typing.Type) -> None:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_DestroyStructure_T]) -> System.Runtime.InteropServices._Typed_Marshal_DestroyStructure[System_Runtime_InteropServices_Marshal_DestroyStructure_T]:
        ...


class _Typed_Marshal_GetDelegateForFunctionPointer(typing.Generic[System_Runtime_InteropServices_Marshal_GetDelegateForFunctionPointer_TDelegate]):
    """"""

    @overload
    def __call__(self, ptr: System.IntPtr) -> System_Runtime_InteropServices_Marshal_GetDelegateForFunctionPointer_TDelegate:
        ...


class _Marshal_GetDelegateForFunctionPointer:
    """"""

    @overload
    def __call__(self, ptr: System.IntPtr, t: typing.Type) -> System.Delegate:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_GetDelegateForFunctionPointer_TDelegate]) -> System.Runtime.InteropServices._Typed_Marshal_GetDelegateForFunctionPointer[System_Runtime_InteropServices_Marshal_GetDelegateForFunctionPointer_TDelegate]:
        ...


class _Typed_Marshal_GetFunctionPointerForDelegate(typing.Generic[System_Runtime_InteropServices_Marshal_GetFunctionPointerForDelegate_TDelegate]):
    """"""

    @overload
    def __call__(self, d: System_Runtime_InteropServices_Marshal_GetFunctionPointerForDelegate_TDelegate) -> System.IntPtr:
        ...


class _Marshal_GetFunctionPointerForDelegate:
    """"""

    @overload
    def __call__(self, d: System.Delegate) -> System.IntPtr:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_Marshal_GetFunctionPointerForDelegate_TDelegate]) -> System.Runtime.InteropServices._Typed_Marshal_GetFunctionPointerForDelegate[System_Runtime_InteropServices_Marshal_GetFunctionPointerForDelegate_TDelegate]:
        ...


class SafeHandle(System.Runtime.ConstrainedExecution.CriticalFinalizerObject, System.IDisposable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def handle(self) -> System.IntPtr:
        ...

    @handle.setter
    def handle(self, value: System.IntPtr) -> None:
        ...

    @property
    def is_closed(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def is_invalid(self) -> bool:
        ...

    def __init__(self, invalid_handle_value: System.IntPtr, owns_handle: bool) -> None:
        ...

    def close(self) -> None:
        ...

    def dangerous_add_ref(self, success: bool) -> None:
        ...

    def dangerous_get_handle(self) -> System.IntPtr:
        ...

    def dangerous_release(self) -> None:
        ...

    @overload
    def dispose(self) -> None:
        ...

    @overload
    def dispose(self, disposing: bool) -> None:
        ...

    def release_handle(self) -> bool:
        ...

    def set_handle_as_invalid(self) -> None:
        ...


class Marshal(System.Object):
    """This class has no documentation."""

    SYSTEM_DEFAULT_CHAR_SIZE: int = 2

    SYSTEM_MAX_DBCS_CHAR_SIZE: int = ...

    create_aggregated_object: System.Runtime.InteropServices._Marshal_CreateAggregatedObject

    create_wrapper_of_type: System.Runtime.InteropServices._Marshal_CreateWrapperOfType

    get_com_interface_for_object: System.Runtime.InteropServices._Marshal_GetComInterfaceForObject

    get_native_variant_for_object: System.Runtime.InteropServices._Marshal_GetNativeVariantForObject

    get_object_for_native_variant: System.Runtime.InteropServices._Marshal_GetObjectForNativeVariant

    get_objects_for_native_variants: System.Runtime.InteropServices._Marshal_GetObjectsForNativeVariants

    size_of: System.Runtime.InteropServices._Marshal_SizeOf

    unsafe_addr_of_pinned_array_element: System.Runtime.InteropServices._Marshal_UnsafeAddrOfPinnedArrayElement

    offset_of: System.Runtime.InteropServices._Marshal_OffsetOf

    structure_to_ptr: System.Runtime.InteropServices._Marshal_StructureToPtr

    ptr_to_structure: System.Runtime.InteropServices._Marshal_PtrToStructure

    destroy_structure: System.Runtime.InteropServices._Marshal_DestroyStructure

    get_delegate_for_function_pointer: System.Runtime.InteropServices._Marshal_GetDelegateForFunctionPointer

    get_function_pointer_for_delegate: System.Runtime.InteropServices._Marshal_GetFunctionPointerForDelegate

    @staticmethod
    def add_ref(p_unk: System.IntPtr) -> int:
        ...

    @staticmethod
    def alloc_co_task_mem(cb: int) -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def alloc_h_global(cb: System.IntPtr) -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def alloc_h_global(cb: int) -> System.IntPtr:
        ...

    @staticmethod
    def are_com_objects_available_for_cleanup() -> bool:
        ...

    @staticmethod
    def bind_to_moniker(moniker_name: str) -> System.Object:
        ...

    @staticmethod
    def change_wrapper_handle_strength(otp: typing.Any, f_is_weak: bool) -> None:
        ...

    @staticmethod
    def cleanup_unused_objects_in_current_context() -> None:
        ...

    @staticmethod
    @overload
    def copy(source: typing.List[int], start_index: int, destination: System.IntPtr, length: int) -> None:
        ...

    @staticmethod
    @overload
    def copy(source: typing.List[str], start_index: int, destination: System.IntPtr, length: int) -> None:
        ...

    @staticmethod
    @overload
    def copy(source: typing.List[float], start_index: int, destination: System.IntPtr, length: int) -> None:
        ...

    @staticmethod
    @overload
    def copy(source: typing.List[System.IntPtr], start_index: int, destination: System.IntPtr, length: int) -> None:
        ...

    @staticmethod
    @overload
    def copy(source: System.IntPtr, destination: typing.List[int], start_index: int, length: int) -> None:
        ...

    @staticmethod
    @overload
    def copy(source: System.IntPtr, destination: typing.List[str], start_index: int, length: int) -> None:
        ...

    @staticmethod
    @overload
    def copy(source: System.IntPtr, destination: typing.List[float], start_index: int, length: int) -> None:
        ...

    @staticmethod
    @overload
    def copy(source: System.IntPtr, destination: typing.List[System.IntPtr], start_index: int, length: int) -> None:
        ...

    @staticmethod
    def final_release_com_object(o: typing.Any) -> int:
        ...

    @staticmethod
    def free_bstr(ptr: System.IntPtr) -> None:
        ...

    @staticmethod
    def free_co_task_mem(ptr: System.IntPtr) -> None:
        ...

    @staticmethod
    def free_h_global(hglobal: System.IntPtr) -> None:
        ...

    @staticmethod
    def generate_guid_for_type(type: typing.Type) -> System.Guid:
        ...

    @staticmethod
    def generate_prog_id_for_type(type: typing.Type) -> str:
        ...

    @staticmethod
    def get_com_object_data(obj: typing.Any, key: typing.Any) -> System.Object:
        ...

    @staticmethod
    def get_end_com_slot(t: typing.Type) -> int:
        ...

    @staticmethod
    def get_exception_code() -> int:
        warnings.warn("GetExceptionCode() may be unavailable in future releases.", DeprecationWarning)

    @staticmethod
    @overload
    def get_exception_for_hr(error_code: int) -> System.Exception:
        ...

    @staticmethod
    @overload
    def get_exception_for_hr(error_code: int, error_info: System.IntPtr) -> System.Exception:
        ...

    @staticmethod
    @overload
    def get_exception_for_hr(error_code: int, iid: System.Guid, p_unk: System.IntPtr) -> System.Exception:
        ...

    @staticmethod
    def get_exception_pointers() -> System.IntPtr:
        ...

    @staticmethod
    def get_hinstance(m: System.Reflection.Module) -> System.IntPtr:
        ...

    @staticmethod
    def get_hr_for_exception(e: System.Exception) -> int:
        ...

    @staticmethod
    def get_hr_for_last_win_32_error() -> int:
        ...

    @staticmethod
    def get_i_dispatch_for_object(o: typing.Any) -> System.IntPtr:
        ...

    @staticmethod
    def get_i_unknown_for_object(o: typing.Any) -> System.IntPtr:
        ...

    @staticmethod
    def get_last_p_invoke_error() -> int:
        ...

    @staticmethod
    def get_last_p_invoke_error_message() -> str:
        ...

    @staticmethod
    def get_last_system_error() -> int:
        ...

    @staticmethod
    def get_last_win_32_error() -> int:
        ...

    @staticmethod
    def get_object_for_i_unknown(p_unk: System.IntPtr) -> System.Object:
        ...

    @staticmethod
    def get_p_invoke_error_message(error: int) -> str:
        ...

    @staticmethod
    def get_start_com_slot(t: typing.Type) -> int:
        ...

    @staticmethod
    def get_typed_object_for_i_unknown(p_unk: System.IntPtr, t: typing.Type) -> System.Object:
        ...

    @staticmethod
    def get_type_from_clsid(clsid: System.Guid) -> typing.Type:
        ...

    @staticmethod
    def get_type_info_name(type_info: System.Runtime.InteropServices.ComTypes.ITypeInfo) -> str:
        ...

    @staticmethod
    def get_unique_object_for_i_unknown(unknown: System.IntPtr) -> System.Object:
        ...

    @staticmethod
    def init_handle(safe_handle: System.Runtime.InteropServices.SafeHandle, handle: System.IntPtr) -> None:
        ...

    @staticmethod
    def is_com_object(o: typing.Any) -> bool:
        ...

    @staticmethod
    def is_type_visible_from_com(t: typing.Type) -> bool:
        ...

    @staticmethod
    def prelink(m: System.Reflection.MethodInfo) -> None:
        ...

    @staticmethod
    def prelink_all(c: typing.Type) -> None:
        ...

    @staticmethod
    @overload
    def ptr_to_string_ansi(ptr: System.IntPtr) -> str:
        ...

    @staticmethod
    @overload
    def ptr_to_string_ansi(ptr: System.IntPtr, len: int) -> str:
        ...

    @staticmethod
    @overload
    def ptr_to_string_auto(ptr: System.IntPtr, len: int) -> str:
        ...

    @staticmethod
    @overload
    def ptr_to_string_auto(ptr: System.IntPtr) -> str:
        ...

    @staticmethod
    def ptr_to_string_bstr(ptr: System.IntPtr) -> str:
        ...

    @staticmethod
    @overload
    def ptr_to_string_uni(ptr: System.IntPtr) -> str:
        ...

    @staticmethod
    @overload
    def ptr_to_string_uni(ptr: System.IntPtr, len: int) -> str:
        ...

    @staticmethod
    @overload
    def ptr_to_string_utf_8(ptr: System.IntPtr) -> str:
        ...

    @staticmethod
    @overload
    def ptr_to_string_utf_8(ptr: System.IntPtr, byte_len: int) -> str:
        ...

    @staticmethod
    def query_interface(p_unk: System.IntPtr, iid: System.Guid, ppv: typing.Optional[System.IntPtr]) -> typing.Tuple[int, System.IntPtr]:
        ...

    @staticmethod
    @overload
    def read_byte(ptr: System.IntPtr, ofs: int) -> int:
        ...

    @staticmethod
    @overload
    def read_byte(ptr: System.IntPtr) -> int:
        ...

    @staticmethod
    @overload
    def read_int_16(ptr: System.IntPtr, ofs: int) -> int:
        ...

    @staticmethod
    @overload
    def read_int_16(ptr: System.IntPtr) -> int:
        ...

    @staticmethod
    @overload
    def read_int_32(ptr: System.IntPtr, ofs: int) -> int:
        ...

    @staticmethod
    @overload
    def read_int_32(ptr: System.IntPtr) -> int:
        ...

    @staticmethod
    @overload
    def read_int_64(ptr: System.IntPtr, ofs: int) -> int:
        ...

    @staticmethod
    @overload
    def read_int_64(ptr: System.IntPtr) -> int:
        ...

    @staticmethod
    @overload
    def read_int_ptr(ptr: System.IntPtr, ofs: int) -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def read_int_ptr(ptr: System.IntPtr) -> System.IntPtr:
        ...

    @staticmethod
    def re_alloc_co_task_mem(pv: System.IntPtr, cb: int) -> System.IntPtr:
        ...

    @staticmethod
    def re_alloc_h_global(pv: System.IntPtr, cb: System.IntPtr) -> System.IntPtr:
        ...

    @staticmethod
    def release(p_unk: System.IntPtr) -> int:
        ...

    @staticmethod
    def release_com_object(o: typing.Any) -> int:
        ...

    @staticmethod
    def secure_string_to_bstr(s: System.Security.SecureString) -> System.IntPtr:
        ...

    @staticmethod
    def secure_string_to_co_task_mem_ansi(s: System.Security.SecureString) -> System.IntPtr:
        ...

    @staticmethod
    def secure_string_to_co_task_mem_unicode(s: System.Security.SecureString) -> System.IntPtr:
        ...

    @staticmethod
    def secure_string_to_global_alloc_ansi(s: System.Security.SecureString) -> System.IntPtr:
        ...

    @staticmethod
    def secure_string_to_global_alloc_unicode(s: System.Security.SecureString) -> System.IntPtr:
        ...

    @staticmethod
    def set_com_object_data(obj: typing.Any, key: typing.Any, data: typing.Any) -> bool:
        ...

    @staticmethod
    def set_last_p_invoke_error(error: int) -> None:
        ...

    @staticmethod
    def set_last_system_error(error: int) -> None:
        ...

    @staticmethod
    def string_to_bstr(s: str) -> System.IntPtr:
        ...

    @staticmethod
    def string_to_co_task_mem_ansi(s: str) -> System.IntPtr:
        ...

    @staticmethod
    def string_to_co_task_mem_auto(s: str) -> System.IntPtr:
        ...

    @staticmethod
    def string_to_co_task_mem_uni(s: str) -> System.IntPtr:
        ...

    @staticmethod
    def string_to_co_task_mem_utf_8(s: str) -> System.IntPtr:
        ...

    @staticmethod
    def string_to_h_global_ansi(s: str) -> System.IntPtr:
        ...

    @staticmethod
    def string_to_h_global_auto(s: str) -> System.IntPtr:
        ...

    @staticmethod
    def string_to_h_global_uni(s: str) -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def throw_exception_for_hr(error_code: int) -> None:
        ...

    @staticmethod
    @overload
    def throw_exception_for_hr(error_code: int, error_info: System.IntPtr) -> None:
        ...

    @staticmethod
    @overload
    def throw_exception_for_hr(error_code: int, iid: System.Guid, p_unk: System.IntPtr) -> None:
        ...

    @staticmethod
    @overload
    def write_byte(ptr: System.IntPtr, ofs: int, val: int) -> None:
        ...

    @staticmethod
    @overload
    def write_byte(ptr: System.IntPtr, val: int) -> None:
        ...

    @staticmethod
    @overload
    def write_int_16(ptr: System.IntPtr, ofs: int, val: int) -> None:
        ...

    @staticmethod
    @overload
    def write_int_16(ptr: System.IntPtr, val: int) -> None:
        ...

    @staticmethod
    @overload
    def write_int_16(ptr: System.IntPtr, ofs: int, val: str) -> None:
        ...

    @staticmethod
    @overload
    def write_int_16(ptr: System.IntPtr, val: str) -> None:
        ...

    @staticmethod
    @overload
    def write_int_32(ptr: System.IntPtr, ofs: int, val: int) -> None:
        ...

    @staticmethod
    @overload
    def write_int_32(ptr: System.IntPtr, val: int) -> None:
        ...

    @staticmethod
    @overload
    def write_int_64(ptr: System.IntPtr, ofs: int, val: int) -> None:
        ...

    @staticmethod
    @overload
    def write_int_64(ptr: System.IntPtr, val: int) -> None:
        ...

    @staticmethod
    @overload
    def write_int_ptr(ptr: System.IntPtr, ofs: int, val: System.IntPtr) -> None:
        ...

    @staticmethod
    @overload
    def write_int_ptr(ptr: System.IntPtr, val: System.IntPtr) -> None:
        ...

    @staticmethod
    def zero_free_bstr(s: System.IntPtr) -> None:
        ...

    @staticmethod
    def zero_free_co_task_mem_ansi(s: System.IntPtr) -> None:
        ...

    @staticmethod
    def zero_free_co_task_mem_unicode(s: System.IntPtr) -> None:
        ...

    @staticmethod
    def zero_free_co_task_mem_utf_8(s: System.IntPtr) -> None:
        ...

    @staticmethod
    def zero_free_global_alloc_ansi(s: System.IntPtr) -> None:
        ...

    @staticmethod
    def zero_free_global_alloc_unicode(s: System.IntPtr) -> None:
        ...


class WeakGCHandle(typing.Generic[System_Runtime_InteropServices_WeakGCHandle_T], System.IEquatable[System_Runtime_InteropServices_WeakGCHandle], System.IDisposable):
    """This class has no documentation."""

    @property
    def is_allocated(self) -> bool:
        ...

    def __init__(self, target: System_Runtime_InteropServices_WeakGCHandle_T, track_resurrection: bool = False) -> None:
        ...

    def dispose(self) -> None:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Runtime.InteropServices.WeakGCHandle[System_Runtime_InteropServices_WeakGCHandle_T]) -> bool:
        ...

    @staticmethod
    def from_int_ptr(value: System.IntPtr) -> System.Runtime.InteropServices.WeakGCHandle[System_Runtime_InteropServices_WeakGCHandle_T]:
        ...

    def get_hash_code(self) -> int:
        ...

    def set_target(self, target: System_Runtime_InteropServices_WeakGCHandle_T) -> None:
        ...

    @staticmethod
    def to_int_ptr(value: System.Runtime.InteropServices.WeakGCHandle[System_Runtime_InteropServices_WeakGCHandle_T]) -> System.IntPtr:
        ...

    def try_get_target(self, target: typing.Optional[System_Runtime_InteropServices_WeakGCHandle_T]) -> typing.Tuple[bool, System_Runtime_InteropServices_WeakGCHandle_T]:
        ...


class StringMarshalling(IntEnum):
    """This class has no documentation."""

    CUSTOM = 0

    UTF_8 = 1

    UTF_16 = 2


class DllImportSearchPath(IntEnum):
    """This class has no documentation."""

    USE_DLL_DIRECTORY_FOR_DEPENDENCIES = ...

    APPLICATION_DIRECTORY = ...

    USER_DIRECTORIES = ...

    SYSTEM_32 = ...

    SAFE_DIRECTORIES = ...

    ASSEMBLY_DIRECTORY = ...

    LEGACY_BEHAVIOR = ...


class NativeLibrary(System.Object):
    """This class has no documentation."""

    @staticmethod
    def free(handle: System.IntPtr) -> None:
        ...

    @staticmethod
    def get_export(handle: System.IntPtr, name: str) -> System.IntPtr:
        ...

    @staticmethod
    def get_main_program_handle() -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def load(library_path: str) -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def load(library_name: str, assembly: System.Reflection.Assembly, search_path: typing.Optional[System.Runtime.InteropServices.DllImportSearchPath]) -> System.IntPtr:
        ...

    @staticmethod
    def set_dll_import_resolver(assembly: System.Reflection.Assembly, resolver: typing.Callable[[str, System.Reflection.Assembly, typing.Optional[System.Runtime.InteropServices.DllImportSearchPath]], System.IntPtr]) -> None:
        ...

    @staticmethod
    def try_get_export(handle: System.IntPtr, name: str, address: typing.Optional[System.IntPtr]) -> typing.Tuple[bool, System.IntPtr]:
        ...

    @staticmethod
    @overload
    def try_load(library_path: str, handle: typing.Optional[System.IntPtr]) -> typing.Tuple[bool, System.IntPtr]:
        ...

    @staticmethod
    @overload
    def try_load(library_name: str, assembly: System.Reflection.Assembly, search_path: typing.Optional[System.Runtime.InteropServices.DllImportSearchPath], handle: typing.Optional[System.IntPtr]) -> typing.Tuple[bool, System.IntPtr]:
        ...


class NativeMemory(System.Object):
    """This class has no documentation."""

    @staticmethod
    def aligned_alloc(byte_count: System.UIntPtr, alignment: System.UIntPtr) -> typing.Any:
        ...

    @staticmethod
    def aligned_free(ptr: typing.Any) -> None:
        ...

    @staticmethod
    def aligned_realloc(ptr: typing.Any, byte_count: System.UIntPtr, alignment: System.UIntPtr) -> typing.Any:
        ...

    @staticmethod
    @overload
    def alloc(element_count: System.UIntPtr, element_size: System.UIntPtr) -> typing.Any:
        ...

    @staticmethod
    @overload
    def alloc(byte_count: System.UIntPtr) -> typing.Any:
        ...

    @staticmethod
    @overload
    def alloc_zeroed(byte_count: System.UIntPtr) -> typing.Any:
        ...

    @staticmethod
    @overload
    def alloc_zeroed(element_count: System.UIntPtr, element_size: System.UIntPtr) -> typing.Any:
        ...

    @staticmethod
    def clear(ptr: typing.Any, byte_count: System.UIntPtr) -> None:
        ...

    @staticmethod
    def copy(source: typing.Any, destination: typing.Any, byte_count: System.UIntPtr) -> None:
        ...

    @staticmethod
    def fill(ptr: typing.Any, byte_count: System.UIntPtr, value: int) -> None:
        ...

    @staticmethod
    def free(ptr: typing.Any) -> None:
        ...

    @staticmethod
    def realloc(ptr: typing.Any, byte_count: System.UIntPtr) -> typing.Any:
        ...


class UnmanagedType(IntEnum):
    """This class has no documentation."""

    BOOL = ...

    I_1 = ...

    U_1 = ...

    I_2 = ...

    U_2 = ...

    I_4 = ...

    U_4 = ...

    I_8 = ...

    U_8 = ...

    R_4 = ...

    R_8 = ...

    CURRENCY = ...

    B_STR = ...

    LP_STR = ...

    LPW_STR = ...

    LPT_STR = ...

    BY_VAL_T_STR = ...

    I_UNKNOWN = ...

    I_DISPATCH = ...

    STRUCT = ...

    INTERFACE = ...

    SAFE_ARRAY = ...

    BY_VAL_ARRAY = ...

    SYS_INT = ...

    SYS_U_INT = ...

    VB_BY_REF_STR = ...

    ANSI_B_STR = ...

    TB_STR = ...

    VARIANT_BOOL = ...

    FUNCTION_PTR = ...

    AS_ANY = ...

    LP_ARRAY = ...

    LP_STRUCT = ...

    CUSTOM_MARSHALER = ...

    ERROR = ...

    I_INSPECTABLE = ...

    H_STRING = ...

    LPUTF_8_STR = ...


class VarEnum(IntEnum):
    """This class has no documentation."""

    VT_EMPTY = 0

    VT_NULL = 1

    VT_I_2 = 2

    VT_I_4 = 3

    VT_R_4 = 4

    VT_R_8 = 5

    VT_CY = 6

    VT_DATE = 7

    VT_BSTR = 8

    VT_DISPATCH = 9

    VT_ERROR = 10

    VT_BOOL = 11

    VT_VARIANT = 12

    VT_UNKNOWN = 13

    VT_DECIMAL = 14

    VT_I_1 = 16

    VT_UI_1 = 17

    VT_UI_2 = 18

    VT_UI_4 = 19

    VT_I_8 = 20

    VT_UI_8 = 21

    VT_INT = 22

    VT_UINT = 23

    VT_VOID = 24

    VT_HRESULT = 25

    VT_PTR = 26

    VT_SAFEARRAY = 27

    VT_CARRAY = 28

    VT_USERDEFINED = 29

    VT_LPSTR = 30

    VT_LPWSTR = 31

    VT_RECORD = 36

    VT_FILETIME = 64

    VT_BLOB = 65

    VT_STREAM = 66

    VT_STORAGE = 67

    VT_STREAMED_OBJECT = 68

    VT_STORED_OBJECT = 69

    VT_BLOB_OBJECT = 70

    VT_CF = 71

    VT_CLSID = 72

    VT_VECTOR = ...

    VT_ARRAY = ...

    VT_BYREF = ...


class MarshalAsAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> System.Runtime.InteropServices.UnmanagedType:
        ...

    @property
    def safe_array_sub_type(self) -> System.Runtime.InteropServices.VarEnum:
        ...

    @safe_array_sub_type.setter
    def safe_array_sub_type(self, value: System.Runtime.InteropServices.VarEnum) -> None:
        ...

    @property
    def safe_array_user_defined_sub_type(self) -> typing.Type:
        ...

    @safe_array_user_defined_sub_type.setter
    def safe_array_user_defined_sub_type(self, value: typing.Type) -> None:
        ...

    @property
    def iid_parameter_index(self) -> int:
        ...

    @iid_parameter_index.setter
    def iid_parameter_index(self, value: int) -> None:
        ...

    @property
    def array_sub_type(self) -> System.Runtime.InteropServices.UnmanagedType:
        ...

    @array_sub_type.setter
    def array_sub_type(self, value: System.Runtime.InteropServices.UnmanagedType) -> None:
        ...

    @property
    def size_param_index(self) -> int:
        ...

    @size_param_index.setter
    def size_param_index(self, value: int) -> None:
        ...

    @property
    def size_const(self) -> int:
        ...

    @size_const.setter
    def size_const(self, value: int) -> None:
        ...

    @property
    def marshal_type(self) -> str:
        ...

    @marshal_type.setter
    def marshal_type(self, value: str) -> None:
        ...

    @property
    def marshal_type_ref(self) -> typing.Type:
        ...

    @marshal_type_ref.setter
    def marshal_type_ref(self, value: typing.Type) -> None:
        ...

    @property
    def marshal_cookie(self) -> str:
        ...

    @marshal_cookie.setter
    def marshal_cookie(self, value: str) -> None:
        ...

    @overload
    def __init__(self, unmanaged_type: System.Runtime.InteropServices.UnmanagedType) -> None:
        ...

    @overload
    def __init__(self, unmanaged_type: int) -> None:
        ...


class TypeMapAttribute(typing.Generic[System_Runtime_InteropServices_TypeMapAttribute_TTypeMapGroup], System.Attribute):
    """This class has no documentation."""

    @overload
    def __init__(self, value: str, target: typing.Type) -> None:
        ...

    @overload
    def __init__(self, value: str, target: typing.Type, trim_target: typing.Type) -> None:
        ...


class ComImportAttribute(System.Attribute):
    """This class has no documentation."""


class _Typed_NFloat_ConvertToInteger(typing.Generic[System_Runtime_InteropServices_NFloat_ConvertToInteger_TInteger]):
    """"""

    @overload
    def __call__(self, value: System.Runtime.InteropServices.NFloat) -> System_Runtime_InteropServices_NFloat_ConvertToInteger_TInteger:
        ...


class _NFloat_ConvertToInteger:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_NFloat_ConvertToInteger_TInteger]) -> System.Runtime.InteropServices._Typed_NFloat_ConvertToInteger[System_Runtime_InteropServices_NFloat_ConvertToInteger_TInteger]:
        ...


class _Typed_NFloat_ConvertToIntegerNative(typing.Generic[System_Runtime_InteropServices_NFloat_ConvertToIntegerNative_TInteger]):
    """"""

    @overload
    def __call__(self, value: System.Runtime.InteropServices.NFloat) -> System_Runtime_InteropServices_NFloat_ConvertToIntegerNative_TInteger:
        ...


class _NFloat_ConvertToIntegerNative:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_NFloat_ConvertToIntegerNative_TInteger]) -> System.Runtime.InteropServices._Typed_NFloat_ConvertToIntegerNative[System_Runtime_InteropServices_NFloat_ConvertToIntegerNative_TInteger]:
        ...


class _Typed_NFloat_CreateChecked(typing.Generic[System_Runtime_InteropServices_NFloat_CreateChecked_TOther]):
    """"""

    @overload
    def __call__(self, value: System_Runtime_InteropServices_NFloat_CreateChecked_TOther) -> System.Runtime.InteropServices.NFloat:
        ...


class _NFloat_CreateChecked:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_NFloat_CreateChecked_TOther]) -> System.Runtime.InteropServices._Typed_NFloat_CreateChecked[System_Runtime_InteropServices_NFloat_CreateChecked_TOther]:
        ...


class _Typed_NFloat_CreateSaturating(typing.Generic[System_Runtime_InteropServices_NFloat_CreateSaturating_TOther]):
    """"""

    @overload
    def __call__(self, value: System_Runtime_InteropServices_NFloat_CreateSaturating_TOther) -> System.Runtime.InteropServices.NFloat:
        ...


class _NFloat_CreateSaturating:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_NFloat_CreateSaturating_TOther]) -> System.Runtime.InteropServices._Typed_NFloat_CreateSaturating[System_Runtime_InteropServices_NFloat_CreateSaturating_TOther]:
        ...


class _Typed_NFloat_CreateTruncating(typing.Generic[System_Runtime_InteropServices_NFloat_CreateTruncating_TOther]):
    """"""

    @overload
    def __call__(self, value: System_Runtime_InteropServices_NFloat_CreateTruncating_TOther) -> System.Runtime.InteropServices.NFloat:
        ...


class _NFloat_CreateTruncating:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_NFloat_CreateTruncating_TOther]) -> System.Runtime.InteropServices._Typed_NFloat_CreateTruncating[System_Runtime_InteropServices_NFloat_CreateTruncating_TOther]:
        ...


class NFloat(System.Numerics.IBinaryFloatingPointIeee754[System_Runtime_InteropServices_NFloat], System.Numerics.IMinMaxValue[System_Runtime_InteropServices_NFloat], System.IUtf8SpanFormattable):
    """This class has no documentation."""

    EPSILON: System.Runtime.InteropServices.NFloat

    MAX_VALUE: System.Runtime.InteropServices.NFloat

    MIN_VALUE: System.Runtime.InteropServices.NFloat

    NA_N: System.Runtime.InteropServices.NFloat

    NEGATIVE_INFINITY: System.Runtime.InteropServices.NFloat

    POSITIVE_INFINITY: System.Runtime.InteropServices.NFloat

    SIZE: int

    @property
    def value(self) -> float:
        ...

    E: System.Runtime.InteropServices.NFloat

    PI: System.Runtime.InteropServices.NFloat

    TAU: System.Runtime.InteropServices.NFloat

    NEGATIVE_ZERO: System.Runtime.InteropServices.NFloat

    convert_to_integer: System.Runtime.InteropServices._NFloat_ConvertToInteger

    convert_to_integer_native: System.Runtime.InteropServices._NFloat_ConvertToIntegerNative

    create_checked: System.Runtime.InteropServices._NFloat_CreateChecked

    create_saturating: System.Runtime.InteropServices._NFloat_CreateSaturating

    create_truncating: System.Runtime.InteropServices._NFloat_CreateTruncating

    def __add__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    def __eq__(self, right: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @overload
    def __ge__(self, right: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @overload
    def __ge__(self, other: typing.Any) -> bool:
        ...

    @overload
    def __ge__(self, other: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @overload
    def __gt__(self, right: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @overload
    def __gt__(self, other: typing.Any) -> bool:
        ...

    @overload
    def __gt__(self, other: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    def __iadd__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    def __imod__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    def __imul__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    def __init__(self, value: float) -> None:
        ...

    def __isub__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    def __itruediv__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @overload
    def __le__(self, right: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @overload
    def __le__(self, other: typing.Any) -> bool:
        ...

    @overload
    def __le__(self, other: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @overload
    def __lt__(self, right: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @overload
    def __lt__(self, other: typing.Any) -> bool:
        ...

    @overload
    def __lt__(self, other: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    def __mod__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    def __mul__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    def __ne__(self, right: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    def __neg__(self) -> System.Runtime.InteropServices.NFloat:
        ...

    def __pos__(self) -> System.Runtime.InteropServices.NFloat:
        ...

    def __sub__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    def __truediv__(self, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def abs(value: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def acos(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def acosh(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def acos_pi(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def asin(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def asinh(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def asin_pi(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def atan(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def atan_2(y: System.Runtime.InteropServices.NFloat, x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def atan_2_pi(y: System.Runtime.InteropServices.NFloat, x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def atanh(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def atan_pi(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def bit_decrement(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def bit_increment(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def cbrt(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def ceiling(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def clamp(value: System.Runtime.InteropServices.NFloat, min: System.Runtime.InteropServices.NFloat, max: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def clamp_native(value: System.Runtime.InteropServices.NFloat, min: System.Runtime.InteropServices.NFloat, max: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @overload
    def compare_to(self, obj: typing.Any) -> int:
        ...

    @overload
    def compare_to(self, other: System.Runtime.InteropServices.NFloat) -> int:
        ...

    @staticmethod
    def copy_sign(value: System.Runtime.InteropServices.NFloat, sign: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def cos(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def cosh(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def cos_pi(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def degrees_to_radians(degrees: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def exp(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def exp_10(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def exp_10_m_1(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def exp_2(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def exp_2_m_1(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def exp_m_1(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def floor(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def fused_multiply_add(left: System.Runtime.InteropServices.NFloat, right: System.Runtime.InteropServices.NFloat, addend: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    def get_hash_code(self) -> int:
        ...

    @staticmethod
    def hypot(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def ieee_754_remainder(left: System.Runtime.InteropServices.NFloat, right: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def i_log_b(x: System.Runtime.InteropServices.NFloat) -> int:
        ...

    @staticmethod
    def is_even_integer(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_finite(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_infinity(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_integer(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_na_n(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_negative(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_negative_infinity(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_normal(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_odd_integer(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_positive(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_positive_infinity(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_pow_2(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_real_number(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def is_subnormal(value: System.Runtime.InteropServices.NFloat) -> bool:
        ...

    @staticmethod
    def lerp(value_1: System.Runtime.InteropServices.NFloat, value_2: System.Runtime.InteropServices.NFloat, amount: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def log(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def log(x: System.Runtime.InteropServices.NFloat, new_base: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def log_10(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def log_10_p_1(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def log_2(value: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def log_2_p_1(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def log_p_1(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def max(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def max_magnitude(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def max_magnitude_number(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def max_native(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def max_number(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def min(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def min_magnitude(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def min_magnitude_number(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def min_native(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def min_number(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def multiply_add_estimate(left: System.Runtime.InteropServices.NFloat, right: System.Runtime.InteropServices.NFloat, addend: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def parse(s: str) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def parse(s: str, style: System.Globalization.NumberStyles) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def parse(s: str, provider: System.IFormatProvider) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def parse(s: str, style: System.Globalization.NumberStyles, provider: System.IFormatProvider) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def parse(s: System.ReadOnlySpan[str], style: System.Globalization.NumberStyles = ..., provider: System.IFormatProvider = None) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def parse(s: System.ReadOnlySpan[str], provider: System.IFormatProvider) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def parse(utf_8_text: System.ReadOnlySpan[int], style: System.Globalization.NumberStyles = ..., provider: System.IFormatProvider = None) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def parse(utf_8_text: System.ReadOnlySpan[int], provider: System.IFormatProvider) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def pow(x: System.Runtime.InteropServices.NFloat, y: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def radians_to_degrees(radians: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def reciprocal_estimate(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def reciprocal_sqrt_estimate(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def root_n(x: System.Runtime.InteropServices.NFloat, n: int) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def round(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def round(x: System.Runtime.InteropServices.NFloat, digits: int) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def round(x: System.Runtime.InteropServices.NFloat, mode: System.MidpointRounding) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    @overload
    def round(x: System.Runtime.InteropServices.NFloat, digits: int, mode: System.MidpointRounding) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def scale_b(x: System.Runtime.InteropServices.NFloat, n: int) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def sign(value: System.Runtime.InteropServices.NFloat) -> int:
        ...

    @staticmethod
    def sin(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def sin_cos(x: System.Runtime.InteropServices.NFloat) -> System.ValueTuple[System.Runtime.InteropServices.NFloat, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    def sin_cos_pi(x: System.Runtime.InteropServices.NFloat) -> System.ValueTuple[System.Runtime.InteropServices.NFloat, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    def sinh(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def sin_pi(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def sqrt(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def tan(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def tanh(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @staticmethod
    def tan_pi(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @overload
    def to_string(self) -> str:
        ...

    @overload
    def to_string(self, format: str) -> str:
        ...

    @overload
    def to_string(self, provider: System.IFormatProvider) -> str:
        ...

    @overload
    def to_string(self, format: str, provider: System.IFormatProvider) -> str:
        ...

    @staticmethod
    def truncate(x: System.Runtime.InteropServices.NFloat) -> System.Runtime.InteropServices.NFloat:
        ...

    @overload
    def try_format(self, destination: System.Span[str], chars_written: typing.Optional[int], format: System.ReadOnlySpan[str] = ..., provider: System.IFormatProvider = None) -> typing.Tuple[bool, int]:
        ...

    @overload
    def try_format(self, utf_8_destination: System.Span[int], bytes_written: typing.Optional[int], format: System.ReadOnlySpan[str] = ..., provider: System.IFormatProvider = None) -> typing.Tuple[bool, int]:
        ...

    @staticmethod
    @overload
    def try_parse(s: str, result: typing.Optional[System.Runtime.InteropServices.NFloat]) -> typing.Tuple[bool, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    @overload
    def try_parse(s: System.ReadOnlySpan[str], result: typing.Optional[System.Runtime.InteropServices.NFloat]) -> typing.Tuple[bool, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    @overload
    def try_parse(utf_8_text: System.ReadOnlySpan[int], result: typing.Optional[System.Runtime.InteropServices.NFloat]) -> typing.Tuple[bool, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    @overload
    def try_parse(s: str, style: System.Globalization.NumberStyles, provider: System.IFormatProvider, result: typing.Optional[System.Runtime.InteropServices.NFloat]) -> typing.Tuple[bool, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    @overload
    def try_parse(s: System.ReadOnlySpan[str], style: System.Globalization.NumberStyles, provider: System.IFormatProvider, result: typing.Optional[System.Runtime.InteropServices.NFloat]) -> typing.Tuple[bool, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    @overload
    def try_parse(s: str, provider: System.IFormatProvider, result: typing.Optional[System.Runtime.InteropServices.NFloat]) -> typing.Tuple[bool, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    @overload
    def try_parse(s: System.ReadOnlySpan[str], provider: System.IFormatProvider, result: typing.Optional[System.Runtime.InteropServices.NFloat]) -> typing.Tuple[bool, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    @overload
    def try_parse(utf_8_text: System.ReadOnlySpan[int], style: System.Globalization.NumberStyles, provider: System.IFormatProvider, result: typing.Optional[System.Runtime.InteropServices.NFloat]) -> typing.Tuple[bool, System.Runtime.InteropServices.NFloat]:
        ...

    @staticmethod
    @overload
    def try_parse(utf_8_text: System.ReadOnlySpan[int], provider: System.IFormatProvider, result: typing.Optional[System.Runtime.InteropServices.NFloat]) -> typing.Tuple[bool, System.Runtime.InteropServices.NFloat]:
        ...


class InvalidComObjectException(System.SystemException):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...


class ClassInterfaceType(IntEnum):
    """This class has no documentation."""

    NONE = 0

    AUTO_DISPATCH = 1

    AUTO_DUAL = 2


class CreatedWrapperFlags(IntEnum):
    """This class has no documentation."""

    NONE = 0

    TRACKER_OBJECT = 1

    NON_WRAPPING = ...


class CustomQueryInterfaceResult(IntEnum):
    """This class has no documentation."""

    HANDLED = 0

    NOT_HANDLED = 1

    FAILED = 2


class PinnedGCHandle(typing.Generic[System_Runtime_InteropServices_PinnedGCHandle_T], System.IEquatable[System_Runtime_InteropServices_PinnedGCHandle], System.IDisposable):
    """This class has no documentation."""

    @property
    def is_allocated(self) -> bool:
        ...

    @property
    def target(self) -> System_Runtime_InteropServices_PinnedGCHandle_T:
        ...

    @target.setter
    def target(self, value: System_Runtime_InteropServices_PinnedGCHandle_T) -> None:
        ...

    def __init__(self, target: System_Runtime_InteropServices_PinnedGCHandle_T) -> None:
        ...

    def dispose(self) -> None:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Runtime.InteropServices.PinnedGCHandle[System_Runtime_InteropServices_PinnedGCHandle_T]) -> bool:
        ...

    @staticmethod
    def from_int_ptr(value: System.IntPtr) -> System.Runtime.InteropServices.PinnedGCHandle[System_Runtime_InteropServices_PinnedGCHandle_T]:
        ...

    def get_address_of_object_data(self) -> typing.Any:
        ...

    def get_hash_code(self) -> int:
        ...

    @staticmethod
    def to_int_ptr(value: System.Runtime.InteropServices.PinnedGCHandle[System_Runtime_InteropServices_PinnedGCHandle_T]) -> System.IntPtr:
        ...


class DispatchWrapper(System.Object):
    """This class has no documentation."""

    @property
    def wrapped_object(self) -> System.Object:
        ...

    def __init__(self, obj: typing.Any) -> None:
        ...


class GCHandle(typing.Generic[System_Runtime_InteropServices_GCHandle_T], System.IEquatable[System_Runtime_InteropServices_GCHandle], System.IDisposable):
    """This class has no documentation."""

    @property
    def is_allocated(self) -> bool:
        ...

    @property
    def target(self) -> System_Runtime_InteropServices_GCHandle_T:
        ...

    @target.setter
    def target(self, value: System_Runtime_InteropServices_GCHandle_T) -> None:
        ...

    def __eq__(self, b: System.Runtime.InteropServices.GCHandle) -> bool:
        ...

    def __init__(self, target: System_Runtime_InteropServices_GCHandle_T) -> None:
        ...

    def __ne__(self, b: System.Runtime.InteropServices.GCHandle) -> bool:
        ...

    def addr_of_pinned_object(self) -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def alloc(value: typing.Any) -> System.Runtime.InteropServices.GCHandle:
        ...

    @staticmethod
    @overload
    def alloc(value: typing.Any, type: System.Runtime.InteropServices.GCHandleType) -> System.Runtime.InteropServices.GCHandle:
        ...

    def dispose(self) -> None:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Runtime.InteropServices.GCHandle[System_Runtime_InteropServices_GCHandle_T]) -> bool:
        ...

    @overload
    def equals(self, o: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Runtime.InteropServices.GCHandle) -> bool:
        ...

    def free(self) -> None:
        ...

    @staticmethod
    def from_int_ptr(value: System.IntPtr) -> System.Runtime.InteropServices.GCHandle[System_Runtime_InteropServices_GCHandle_T]:
        ...

    def get_hash_code(self) -> int:
        ...

    @staticmethod
    @overload
    def to_int_ptr(value: System.Runtime.InteropServices.GCHandle[System_Runtime_InteropServices_GCHandle_T]) -> System.IntPtr:
        ...

    @staticmethod
    @overload
    def to_int_ptr(value: System.Runtime.InteropServices.GCHandle) -> System.IntPtr:
        ...


class LibraryImportAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def library_name(self) -> str:
        ...

    @property
    def entry_point(self) -> str:
        ...

    @entry_point.setter
    def entry_point(self, value: str) -> None:
        ...

    @property
    def string_marshalling(self) -> System.Runtime.InteropServices.StringMarshalling:
        ...

    @string_marshalling.setter
    def string_marshalling(self, value: System.Runtime.InteropServices.StringMarshalling) -> None:
        ...

    @property
    def string_marshalling_custom_type(self) -> typing.Type:
        ...

    @string_marshalling_custom_type.setter
    def string_marshalling_custom_type(self, value: typing.Type) -> None:
        ...

    @property
    def set_last_error(self) -> bool:
        ...

    @set_last_error.setter
    def set_last_error(self, value: bool) -> None:
        ...

    def __init__(self, library_name: str) -> None:
        ...


class TypeMapAssociationAttribute(typing.Generic[System_Runtime_InteropServices_TypeMapAssociationAttribute_TTypeMapGroup], System.Attribute):
    """This class has no documentation."""

    def __init__(self, source: typing.Type, proxy: typing.Type) -> None:
        ...


class InvalidOleVariantTypeException(System.SystemException):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...


class CLong(System.IEquatable[System_Runtime_InteropServices_CLong]):
    """This class has no documentation."""

    @property
    def value(self) -> System.IntPtr:
        ...

    @overload
    def __init__(self, value: int) -> None:
        ...

    @overload
    def __init__(self, value: System.IntPtr) -> None:
        ...

    @overload
    def equals(self, o: typing.Any) -> bool:
        ...

    @overload
    def equals(self, other: System.Runtime.InteropServices.CLong) -> bool:
        ...

    def get_hash_code(self) -> int:
        ...

    def to_string(self) -> str:
        ...


class ICustomMarshaler(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def clean_up_managed_data(self, managed_obj: typing.Any) -> None:
        ...

    def clean_up_native_data(self, p_native_data: System.IntPtr) -> None:
        ...

    def get_native_data_size(self) -> int:
        ...

    def marshal_managed_to_native(self, managed_obj: typing.Any) -> System.IntPtr:
        ...

    def marshal_native_to_managed(self, p_native_data: System.IntPtr) -> System.Object:
        ...


class ComSourceInterfacesAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> str:
        ...

    @overload
    def __init__(self, source_interfaces: str) -> None:
        ...

    @overload
    def __init__(self, source_interface: typing.Type) -> None:
        ...

    @overload
    def __init__(self, source_interface_1: typing.Type, source_interface_2: typing.Type) -> None:
        ...

    @overload
    def __init__(self, source_interface_1: typing.Type, source_interface_2: typing.Type, source_interface_3: typing.Type) -> None:
        ...

    @overload
    def __init__(self, source_interface_1: typing.Type, source_interface_2: typing.Type, source_interface_3: typing.Type, source_interface_4: typing.Type) -> None:
        ...


class TypeIdentifierAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def scope(self) -> str:
        ...

    @property
    def identifier(self) -> str:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, scope: str, identifier: str) -> None:
        ...


class SafeArrayTypeMismatchException(System.SystemException):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...


class PosixSignal(IntEnum):
    """This class has no documentation."""

    SIGHUP = -1

    SIGINT = -2

    SIGQUIT = -3

    SIGTERM = -4

    SIGCHLD = -5

    SIGCONT = -6

    SIGWINCH = -7

    SIGTTIN = -8

    SIGTTOU = -9

    SIGTSTP = -10

    SIGKILL = -11


class PosixSignalContext(System.Object):
    """This class has no documentation."""

    @property
    def signal(self) -> System.Runtime.InteropServices.PosixSignal:
        ...

    @property
    def cancel(self) -> bool:
        ...

    @cancel.setter
    def cancel(self, value: bool) -> None:
        ...

    def __init__(self, signal: System.Runtime.InteropServices.PosixSignal) -> None:
        ...


class PosixSignalRegistration(System.Object, System.IDisposable):
    """This class has no documentation."""

    @staticmethod
    def create(signal: System.Runtime.InteropServices.PosixSignal, handler: typing.Callable[[System.Runtime.InteropServices.PosixSignalContext], typing.Any]) -> System.Runtime.InteropServices.PosixSignalRegistration:
        ...

    def dispose(self) -> None:
        ...


class CharSet(IntEnum):
    """This class has no documentation."""

    NONE = 1

    ANSI = 2

    UNICODE = 3

    AUTO = 4


class CallingConvention(IntEnum):
    """This class has no documentation."""

    WINAPI = 1

    CDECL = 2

    STD_CALL = 3

    THIS_CALL = 4

    FAST_CALL = 5


class DllImportAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> str:
        ...

    @property
    def entry_point(self) -> str:
        ...

    @entry_point.setter
    def entry_point(self, value: str) -> None:
        ...

    @property
    def char_set(self) -> System.Runtime.InteropServices.CharSet:
        ...

    @char_set.setter
    def char_set(self, value: System.Runtime.InteropServices.CharSet) -> None:
        ...

    @property
    def set_last_error(self) -> bool:
        ...

    @set_last_error.setter
    def set_last_error(self, value: bool) -> None:
        ...

    @property
    def exact_spelling(self) -> bool:
        ...

    @exact_spelling.setter
    def exact_spelling(self, value: bool) -> None:
        ...

    @property
    def calling_convention(self) -> System.Runtime.InteropServices.CallingConvention:
        ...

    @calling_convention.setter
    def calling_convention(self, value: System.Runtime.InteropServices.CallingConvention) -> None:
        ...

    @property
    def best_fit_mapping(self) -> bool:
        ...

    @best_fit_mapping.setter
    def best_fit_mapping(self, value: bool) -> None:
        ...

    @property
    def preserve_sig(self) -> bool:
        ...

    @preserve_sig.setter
    def preserve_sig(self, value: bool) -> None:
        ...

    @property
    def throw_on_unmappable_char(self) -> bool:
        ...

    @throw_on_unmappable_char.setter
    def throw_on_unmappable_char(self, value: bool) -> None:
        ...

    def __init__(self, dll_name: str) -> None:
        ...


class LCIDConversionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> int:
        ...

    def __init__(self, lcid: int) -> None:
        ...


class CriticalHandle(System.Runtime.ConstrainedExecution.CriticalFinalizerObject, System.IDisposable, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def handle(self) -> System.IntPtr:
        ...

    @handle.setter
    def handle(self, value: System.IntPtr) -> None:
        ...

    @property
    def is_closed(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def is_invalid(self) -> bool:
        ...

    def __init__(self, invalid_handle_value: System.IntPtr) -> None:
        ...

    def close(self) -> None:
        ...

    @overload
    def dispose(self) -> None:
        ...

    @overload
    def dispose(self, disposing: bool) -> None:
        ...

    def release_handle(self) -> bool:
        ...

    def set_handle(self, handle: System.IntPtr) -> None:
        ...

    def set_handle_as_invalid(self) -> None:
        ...


class ArrayWithOffset(System.IEquatable[System_Runtime_InteropServices_ArrayWithOffset]):
    """This class has no documentation."""

    def __eq__(self, b: System.Runtime.InteropServices.ArrayWithOffset) -> bool:
        ...

    def __init__(self, array: typing.Any, offset: int) -> None:
        ...

    def __ne__(self, b: System.Runtime.InteropServices.ArrayWithOffset) -> bool:
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        ...

    @overload
    def equals(self, obj: System.Runtime.InteropServices.ArrayWithOffset) -> bool:
        ...

    def get_array(self) -> System.Object:
        ...

    def get_hash_code(self) -> int:
        ...

    def get_offset(self) -> int:
        ...


class ExternalException(System.SystemException):
    """This class has no documentation."""

    @property
    def error_code(self) -> int:
        ...

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...

    @overload
    def __init__(self, message: str, error_code: int) -> None:
        ...

    def to_string(self) -> str:
        ...


class COMException(System.Runtime.InteropServices.ExternalException):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...

    @overload
    def __init__(self, message: str, error_code: int) -> None:
        ...

    def to_string(self) -> str:
        ...


class MarshalDirectiveException(System.SystemException):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...


class DispIdAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> int:
        ...

    def __init__(self, disp_id: int) -> None:
        ...


class ComInterfaceType(IntEnum):
    """This class has no documentation."""

    INTERFACE_IS_DUAL = 0

    INTERFACE_IS_I_UNKNOWN = 1

    INTERFACE_IS_I_DISPATCH = 2

    INTERFACE_IS_I_INSPECTABLE = 3


class ExtendedLayoutKind(IntEnum):
    """This class has no documentation."""

    C_STRUCT = 0

    C_UNION = 1


class SEHException(System.Runtime.InteropServices.ExternalException):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...

    def can_resume(self) -> bool:
        ...


class TypeMapAssemblyTargetAttribute(typing.Generic[System_Runtime_InteropServices_TypeMapAssemblyTargetAttribute_TTypeMapGroup], System.Attribute):
    """This class has no documentation."""

    def __init__(self, assembly_name: str) -> None:
        ...


class BestFitMappingAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def best_fit_mapping(self) -> bool:
        ...

    @property
    def throw_on_unmappable_char(self) -> bool:
        ...

    @throw_on_unmappable_char.setter
    def throw_on_unmappable_char(self, value: bool) -> None:
        ...

    def __init__(self, best_fit_mapping: bool) -> None:
        ...


class _Typed_MemoryMarshal_AsBytes(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_AsBytes_T]):
    """"""

    @overload
    def __call__(self, span: System.Span[System_Runtime_InteropServices_MemoryMarshal_AsBytes_T]) -> System.Span[int]:
        ...

    @overload
    def __call__(self, span: System.ReadOnlySpan[System_Runtime_InteropServices_MemoryMarshal_AsBytes_T]) -> System.ReadOnlySpan[int]:
        ...


class _MemoryMarshal_AsBytes:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_AsBytes_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_AsBytes[System_Runtime_InteropServices_MemoryMarshal_AsBytes_T]:
        ...


class _Typed_MemoryMarshal_AsMemory(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_AsMemory_T]):
    """"""

    @overload
    def __call__(self, memory: System.ReadOnlyMemory[System_Runtime_InteropServices_MemoryMarshal_AsMemory_T]) -> System.Memory[System_Runtime_InteropServices_MemoryMarshal_AsMemory_T]:
        ...


class _MemoryMarshal_AsMemory:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_AsMemory_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_AsMemory[System_Runtime_InteropServices_MemoryMarshal_AsMemory_T]:
        ...


class _Typed_MemoryMarshal_GetReference(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_GetReference_T]):
    """"""

    @overload
    def __call__(self, span: System.Span[System_Runtime_InteropServices_MemoryMarshal_GetReference_T]) -> typing.Any:
        ...

    @overload
    def __call__(self, span: System.ReadOnlySpan[System_Runtime_InteropServices_MemoryMarshal_GetReference_T]) -> typing.Any:
        ...


class _MemoryMarshal_GetReference:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_GetReference_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_GetReference[System_Runtime_InteropServices_MemoryMarshal_GetReference_T]:
        ...


class _Typed_MemoryMarshal_Cast(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_Cast_TFrom]):
    """"""

    @overload
    def __call__(self, span: System.Span[System_Runtime_InteropServices_MemoryMarshal_Cast_TFrom]) -> System.Span[System_Runtime_InteropServices_MemoryMarshal_Cast_TTo]:
        ...

    @overload
    def __call__(self, span: System.ReadOnlySpan[System_Runtime_InteropServices_MemoryMarshal_Cast_TFrom]) -> System.ReadOnlySpan[System_Runtime_InteropServices_MemoryMarshal_Cast_TTo]:
        ...


class _MemoryMarshal_Cast:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_Cast_TFrom]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_Cast[System_Runtime_InteropServices_MemoryMarshal_Cast_TFrom]:
        ...


class _Typed_MemoryMarshal_CreateSpan(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_CreateSpan_T]):
    """"""

    @overload
    def __call__(self, reference: System_Runtime_InteropServices_MemoryMarshal_CreateSpan_T, length: int) -> System.Span[System_Runtime_InteropServices_MemoryMarshal_CreateSpan_T]:
        ...


class _MemoryMarshal_CreateSpan:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_CreateSpan_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_CreateSpan[System_Runtime_InteropServices_MemoryMarshal_CreateSpan_T]:
        ...


class _Typed_MemoryMarshal_CreateReadOnlySpan(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_CreateReadOnlySpan_T]):
    """"""

    @overload
    def __call__(self, reference: System_Runtime_InteropServices_MemoryMarshal_CreateReadOnlySpan_T, length: int) -> System.ReadOnlySpan[System_Runtime_InteropServices_MemoryMarshal_CreateReadOnlySpan_T]:
        ...


class _MemoryMarshal_CreateReadOnlySpan:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_CreateReadOnlySpan_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_CreateReadOnlySpan[System_Runtime_InteropServices_MemoryMarshal_CreateReadOnlySpan_T]:
        ...


class _Typed_MemoryMarshal_TryGetArray(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_TryGetArray_T]):
    """"""

    @overload
    def __call__(self, memory: System.ReadOnlyMemory[System_Runtime_InteropServices_MemoryMarshal_TryGetArray_T], segment: typing.Optional[System.ArraySegment[System_Runtime_InteropServices_MemoryMarshal_TryGetArray_T]]) -> typing.Tuple[bool, System.ArraySegment[System_Runtime_InteropServices_MemoryMarshal_TryGetArray_T]]:
        ...


class _MemoryMarshal_TryGetArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_TryGetArray_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_TryGetArray[System_Runtime_InteropServices_MemoryMarshal_TryGetArray_T]:
        ...


class _Typed_MemoryMarshal_TryGetMemoryManager(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_T]):
    """"""

    @overload
    def __call__(self, memory: System.ReadOnlyMemory[System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_T], manager: typing.Optional[System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_TManager]) -> typing.Tuple[bool, System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_TManager]:
        ...

    @overload
    def __call__(self, memory: System.ReadOnlyMemory[System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_T], manager: typing.Optional[System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_TManager], start: typing.Optional[int], length: typing.Optional[int]) -> typing.Tuple[bool, System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_TManager, int, int]:
        ...


class _MemoryMarshal_TryGetMemoryManager:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_TryGetMemoryManager[System_Runtime_InteropServices_MemoryMarshal_TryGetMemoryManager_T]:
        ...


class _Typed_MemoryMarshal_ToEnumerable(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_ToEnumerable_T]):
    """"""

    @overload
    def __call__(self, memory: System.ReadOnlyMemory[System_Runtime_InteropServices_MemoryMarshal_ToEnumerable_T]) -> System.Collections.Generic.IEnumerable[System_Runtime_InteropServices_MemoryMarshal_ToEnumerable_T]:
        ...


class _MemoryMarshal_ToEnumerable:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_ToEnumerable_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_ToEnumerable[System_Runtime_InteropServices_MemoryMarshal_ToEnumerable_T]:
        ...


class _Typed_MemoryMarshal_Read(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_Read_T]):
    """"""

    @overload
    def __call__(self, source: System.ReadOnlySpan[int]) -> System_Runtime_InteropServices_MemoryMarshal_Read_T:
        ...


class _MemoryMarshal_Read:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_Read_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_Read[System_Runtime_InteropServices_MemoryMarshal_Read_T]:
        ...


class _Typed_MemoryMarshal_TryRead(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_TryRead_T]):
    """"""

    @overload
    def __call__(self, source: System.ReadOnlySpan[int], value: typing.Optional[System_Runtime_InteropServices_MemoryMarshal_TryRead_T]) -> typing.Tuple[bool, System_Runtime_InteropServices_MemoryMarshal_TryRead_T]:
        ...


class _MemoryMarshal_TryRead:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_TryRead_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_TryRead[System_Runtime_InteropServices_MemoryMarshal_TryRead_T]:
        ...


class _Typed_MemoryMarshal_Write(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_Write_T]):
    """"""

    @overload
    def __call__(self, destination: System.Span[int], value: System_Runtime_InteropServices_MemoryMarshal_Write_T) -> None:
        ...


class _MemoryMarshal_Write:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_Write_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_Write[System_Runtime_InteropServices_MemoryMarshal_Write_T]:
        ...


class _Typed_MemoryMarshal_TryWrite(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_TryWrite_T]):
    """"""

    @overload
    def __call__(self, destination: System.Span[int], value: System_Runtime_InteropServices_MemoryMarshal_TryWrite_T) -> bool:
        ...


class _MemoryMarshal_TryWrite:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_TryWrite_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_TryWrite[System_Runtime_InteropServices_MemoryMarshal_TryWrite_T]:
        ...


class _Typed_MemoryMarshal_AsRef(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_AsRef_T]):
    """"""

    @overload
    def __call__(self, span: System.Span[int]) -> typing.Any:
        ...

    @overload
    def __call__(self, span: System.ReadOnlySpan[int]) -> typing.Any:
        ...


class _MemoryMarshal_AsRef:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_AsRef_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_AsRef[System_Runtime_InteropServices_MemoryMarshal_AsRef_T]:
        ...


class _Typed_MemoryMarshal_CreateFromPinnedArray(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_CreateFromPinnedArray_T]):
    """"""

    @overload
    def __call__(self, array: typing.List[System_Runtime_InteropServices_MemoryMarshal_CreateFromPinnedArray_T], start: int, length: int) -> System.Memory[System_Runtime_InteropServices_MemoryMarshal_CreateFromPinnedArray_T]:
        ...


class _MemoryMarshal_CreateFromPinnedArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_CreateFromPinnedArray_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_CreateFromPinnedArray[System_Runtime_InteropServices_MemoryMarshal_CreateFromPinnedArray_T]:
        ...


class _Typed_MemoryMarshal_GetArrayDataReference(typing.Generic[System_Runtime_InteropServices_MemoryMarshal_GetArrayDataReference_T]):
    """"""

    @overload
    def __call__(self, array: typing.List[System_Runtime_InteropServices_MemoryMarshal_GetArrayDataReference_T]) -> typing.Any:
        ...


class _MemoryMarshal_GetArrayDataReference:
    """"""

    @overload
    def __call__(self, array: System.Array) -> typing.Any:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_MemoryMarshal_GetArrayDataReference_T]) -> System.Runtime.InteropServices._Typed_MemoryMarshal_GetArrayDataReference[System_Runtime_InteropServices_MemoryMarshal_GetArrayDataReference_T]:
        ...


class MemoryMarshal(System.Object):
    """This class has no documentation."""

    as_bytes: System.Runtime.InteropServices._MemoryMarshal_AsBytes

    as_memory: System.Runtime.InteropServices._MemoryMarshal_AsMemory

    get_reference: System.Runtime.InteropServices._MemoryMarshal_GetReference

    cast: System.Runtime.InteropServices._MemoryMarshal_Cast

    create_span: System.Runtime.InteropServices._MemoryMarshal_CreateSpan

    create_read_only_span: System.Runtime.InteropServices._MemoryMarshal_CreateReadOnlySpan

    try_get_array: System.Runtime.InteropServices._MemoryMarshal_TryGetArray

    try_get_memory_manager: System.Runtime.InteropServices._MemoryMarshal_TryGetMemoryManager

    to_enumerable: System.Runtime.InteropServices._MemoryMarshal_ToEnumerable

    read: System.Runtime.InteropServices._MemoryMarshal_Read

    try_read: System.Runtime.InteropServices._MemoryMarshal_TryRead

    write: System.Runtime.InteropServices._MemoryMarshal_Write

    try_write: System.Runtime.InteropServices._MemoryMarshal_TryWrite

    as_ref: System.Runtime.InteropServices._MemoryMarshal_AsRef

    create_from_pinned_array: System.Runtime.InteropServices._MemoryMarshal_CreateFromPinnedArray

    get_array_data_reference: System.Runtime.InteropServices._MemoryMarshal_GetArrayDataReference

    @staticmethod
    def create_read_only_span_from_null_terminated(value: typing.Any) -> System.ReadOnlySpan[str]:
        ...

    @staticmethod
    def try_get_string(memory: System.ReadOnlyMemory[str], text: typing.Optional[str], start: typing.Optional[int], length: typing.Optional[int]) -> typing.Tuple[bool, str, int, int]:
        ...


class DefaultDllImportSearchPathsAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def paths(self) -> System.Runtime.InteropServices.DllImportSearchPath:
        ...

    def __init__(self, paths: System.Runtime.InteropServices.DllImportSearchPath) -> None:
        ...


class UnmanagedCallersOnlyAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def call_convs(self) -> typing.List[typing.Type]:
        ...

    @call_convs.setter
    def call_convs(self, value: typing.List[typing.Type]) -> None:
        ...

    @property
    def entry_point(self) -> str:
        ...

    @entry_point.setter
    def entry_point(self, value: str) -> None:
        ...

    def __init__(self) -> None:
        ...


class UnmanagedCallConvAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def call_convs(self) -> typing.List[typing.Type]:
        ...

    @call_convs.setter
    def call_convs(self, value: typing.List[typing.Type]) -> None:
        ...

    def __init__(self) -> None:
        ...


class InAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CreateComInterfaceFlags(IntEnum):
    """This class has no documentation."""

    NONE = 0

    CALLER_DEFINED_I_UNKNOWN = 1

    TRACKER_SUPPORT = 2


class CreateObjectFlags(IntEnum):
    """This class has no documentation."""

    NONE = 0

    TRACKER_OBJECT = 1

    UNIQUE_INSTANCE = 2

    AGGREGATION = 4

    UNWRAP = 8


class ComWrappers(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    class ComInterfaceEntry:
        """This class has no documentation."""

        @property
        def iid(self) -> System.Guid:
            ...

        @iid.setter
        def iid(self, value: System.Guid) -> None:
            ...

        @property
        def vtable(self) -> System.IntPtr:
            ...

        @vtable.setter
        def vtable(self, value: System.IntPtr) -> None:
            ...

        @property
        def iid(self) -> System.Guid:
            ...

        @iid.setter
        def iid(self, value: System.Guid) -> None:
            ...

        @property
        def vtable(self) -> System.IntPtr:
            ...

        @vtable.setter
        def vtable(self, value: System.IntPtr) -> None:
            ...

    class ComInterfaceDispatch:
        """This class has no documentation."""

        @property
        def vtable(self) -> System.IntPtr:
            ...

        @vtable.setter
        def vtable(self, value: System.IntPtr) -> None:
            ...

        @property
        def vtable(self) -> System.IntPtr:
            ...

        @vtable.setter
        def vtable(self, value: System.IntPtr) -> None:
            ...

        get_instance: System.Runtime.InteropServices._ComWrappers.ComInterfaceDispatch_GetInstance

    def compute_vtables(self, obj: typing.Any, flags: System.Runtime.InteropServices.CreateComInterfaceFlags, count: typing.Optional[int]) -> typing.Tuple[typing.Any, int]:
        ...

    @overload
    def create_object(self, external_com_object: System.IntPtr, flags: System.Runtime.InteropServices.CreateObjectFlags) -> System.Object:
        ...

    @overload
    def create_object(self, external_com_object: System.IntPtr, flags: System.Runtime.InteropServices.CreateObjectFlags, user_state: typing.Any, wrapper_flags: typing.Optional[System.Runtime.InteropServices.CreatedWrapperFlags]) -> typing.Tuple[System.Object, System.Runtime.InteropServices.CreatedWrapperFlags]:
        ...

    @staticmethod
    def get_i_unknown_impl(fp_query_interface: typing.Optional[System.IntPtr], fp_add_ref: typing.Optional[System.IntPtr], fp_release: typing.Optional[System.IntPtr]) -> typing.Tuple[None, System.IntPtr, System.IntPtr, System.IntPtr]:
        ...

    def get_or_create_com_interface_for_object(self, instance: typing.Any, flags: System.Runtime.InteropServices.CreateComInterfaceFlags) -> System.IntPtr:
        ...

    @overload
    def get_or_create_object_for_com_instance(self, external_com_object: System.IntPtr, flags: System.Runtime.InteropServices.CreateObjectFlags) -> System.Object:
        ...

    @overload
    def get_or_create_object_for_com_instance(self, external_com_object: System.IntPtr, flags: System.Runtime.InteropServices.CreateObjectFlags, user_state: typing.Any) -> System.Object:
        ...

    @overload
    def get_or_register_object_for_com_instance(self, external_com_object: System.IntPtr, flags: System.Runtime.InteropServices.CreateObjectFlags, wrapper: typing.Any) -> System.Object:
        ...

    @overload
    def get_or_register_object_for_com_instance(self, external_com_object: System.IntPtr, flags: System.Runtime.InteropServices.CreateObjectFlags, wrapper: typing.Any, inner: System.IntPtr) -> System.Object:
        ...

    @staticmethod
    def register_for_marshalling(instance: System.Runtime.InteropServices.ComWrappers) -> None:
        ...

    @staticmethod
    def register_for_tracker_support(instance: System.Runtime.InteropServices.ComWrappers) -> None:
        ...

    @staticmethod
    def try_get_com_instance(obj: typing.Any, unknown: typing.Optional[System.IntPtr]) -> typing.Tuple[bool, System.IntPtr]:
        ...

    @staticmethod
    def try_get_object(unknown: System.IntPtr, obj: typing.Optional[typing.Any]) -> typing.Tuple[bool, typing.Any]:
        ...


class ErrorWrapper(System.Object):
    """This class has no documentation."""

    @property
    def error_code(self) -> int:
        ...

    @overload
    def __init__(self, error_code: int) -> None:
        ...

    @overload
    def __init__(self, error_code: typing.Any) -> None:
        ...

    @overload
    def __init__(self, e: System.Exception) -> None:
        ...


class ComMemberType(IntEnum):
    """This class has no documentation."""

    METHOD = 0

    PROP_GET = 1

    PROP_SET = 2


class FieldOffsetAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> int:
        ...

    def __init__(self, offset: int) -> None:
        ...


class _Typed_GCHandleExtensions_GetAddressOfArrayData(typing.Generic[System_Runtime_InteropServices_GCHandleExtensions_GetAddressOfArrayData_T]):
    """"""

    @overload
    def __call__(self, handle: System.Runtime.InteropServices.PinnedGCHandle[typing.List[System_Runtime_InteropServices_GCHandleExtensions_GetAddressOfArrayData_T]]) -> typing.Any:
        ...


class _GCHandleExtensions_GetAddressOfArrayData:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_GCHandleExtensions_GetAddressOfArrayData_T]) -> System.Runtime.InteropServices._Typed_GCHandleExtensions_GetAddressOfArrayData[System_Runtime_InteropServices_GCHandleExtensions_GetAddressOfArrayData_T]:
        ...


class GCHandleExtensions(System.Object):
    """This class has no documentation."""

    get_address_of_array_data: System.Runtime.InteropServices._GCHandleExtensions_GetAddressOfArrayData

    @staticmethod
    def get_address_of_string_data(handle: System.Runtime.InteropServices.PinnedGCHandle[str]) -> typing.Any:
        ...


class LayoutKind(IntEnum):
    """This class has no documentation."""

    SEQUENTIAL = 0

    EXTENDED = 1

    EXPLICIT = 2

    AUTO = 3


class HandleRef:
    """This class has no documentation."""

    @property
    def wrapper(self) -> System.Object:
        ...

    @property
    def handle(self) -> System.IntPtr:
        ...

    def __init__(self, wrapper: typing.Any, handle: System.IntPtr) -> None:
        ...

    @staticmethod
    def to_int_ptr(value: System.Runtime.InteropServices.HandleRef) -> System.IntPtr:
        ...


class InterfaceTypeAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> System.Runtime.InteropServices.ComInterfaceType:
        ...

    @overload
    def __init__(self, interface_type: System.Runtime.InteropServices.ComInterfaceType) -> None:
        ...

    @overload
    def __init__(self, interface_type: int) -> None:
        ...


class UnknownWrapper(System.Object):
    """This class has no documentation."""

    @property
    def wrapped_object(self) -> System.Object:
        ...

    def __init__(self, obj: typing.Any) -> None:
        ...


class ClassInterfaceAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> System.Runtime.InteropServices.ClassInterfaceType:
        ...

    @overload
    def __init__(self, class_interface_type: System.Runtime.InteropServices.ClassInterfaceType) -> None:
        ...

    @overload
    def __init__(self, class_interface_type: int) -> None:
        ...


class DefaultCharSetAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def char_set(self) -> System.Runtime.InteropServices.CharSet:
        ...

    def __init__(self, char_set: System.Runtime.InteropServices.CharSet) -> None:
        ...


class _Typed_SafeBuffer_Initialize(typing.Generic[System_Runtime_InteropServices_SafeBuffer_Initialize_T]):
    """"""

    @overload
    def __call__(self, num_elements: int) -> None:
        ...


class _SafeBuffer_Initialize:
    """"""

    @overload
    def __call__(self, num_bytes: int) -> None:
        ...

    @overload
    def __call__(self, num_elements: int, size_of_each_element: int) -> None:
        ...

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_SafeBuffer_Initialize_T]) -> System.Runtime.InteropServices._Typed_SafeBuffer_Initialize[System_Runtime_InteropServices_SafeBuffer_Initialize_T]:
        ...


class _Typed_SafeBuffer_Read(typing.Generic[System_Runtime_InteropServices_SafeBuffer_Read_T]):
    """"""

    @overload
    def __call__(self, byte_offset: int) -> System_Runtime_InteropServices_SafeBuffer_Read_T:
        ...


class _SafeBuffer_Read:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_SafeBuffer_Read_T]) -> System.Runtime.InteropServices._Typed_SafeBuffer_Read[System_Runtime_InteropServices_SafeBuffer_Read_T]:
        ...


class _Typed_SafeBuffer_ReadArray(typing.Generic[System_Runtime_InteropServices_SafeBuffer_ReadArray_T]):
    """"""

    @overload
    def __call__(self, byte_offset: int, array: typing.List[System_Runtime_InteropServices_SafeBuffer_ReadArray_T], index: int, count: int) -> None:
        ...


class _SafeBuffer_ReadArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_SafeBuffer_ReadArray_T]) -> System.Runtime.InteropServices._Typed_SafeBuffer_ReadArray[System_Runtime_InteropServices_SafeBuffer_ReadArray_T]:
        ...


class _Typed_SafeBuffer_ReadSpan(typing.Generic[System_Runtime_InteropServices_SafeBuffer_ReadSpan_T]):
    """"""

    @overload
    def __call__(self, byte_offset: int, buffer: System.Span[System_Runtime_InteropServices_SafeBuffer_ReadSpan_T]) -> None:
        ...


class _SafeBuffer_ReadSpan:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_SafeBuffer_ReadSpan_T]) -> System.Runtime.InteropServices._Typed_SafeBuffer_ReadSpan[System_Runtime_InteropServices_SafeBuffer_ReadSpan_T]:
        ...


class _Typed_SafeBuffer_Write(typing.Generic[System_Runtime_InteropServices_SafeBuffer_Write_T]):
    """"""

    @overload
    def __call__(self, byte_offset: int, value: System_Runtime_InteropServices_SafeBuffer_Write_T) -> None:
        ...


class _SafeBuffer_Write:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_SafeBuffer_Write_T]) -> System.Runtime.InteropServices._Typed_SafeBuffer_Write[System_Runtime_InteropServices_SafeBuffer_Write_T]:
        ...


class _Typed_SafeBuffer_WriteArray(typing.Generic[System_Runtime_InteropServices_SafeBuffer_WriteArray_T]):
    """"""

    @overload
    def __call__(self, byte_offset: int, array: typing.List[System_Runtime_InteropServices_SafeBuffer_WriteArray_T], index: int, count: int) -> None:
        ...


class _SafeBuffer_WriteArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_SafeBuffer_WriteArray_T]) -> System.Runtime.InteropServices._Typed_SafeBuffer_WriteArray[System_Runtime_InteropServices_SafeBuffer_WriteArray_T]:
        ...


class _Typed_SafeBuffer_WriteSpan(typing.Generic[System_Runtime_InteropServices_SafeBuffer_WriteSpan_T]):
    """"""

    @overload
    def __call__(self, byte_offset: int, data: System.ReadOnlySpan[System_Runtime_InteropServices_SafeBuffer_WriteSpan_T]) -> None:
        ...


class _SafeBuffer_WriteSpan:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_SafeBuffer_WriteSpan_T]) -> System.Runtime.InteropServices._Typed_SafeBuffer_WriteSpan[System_Runtime_InteropServices_SafeBuffer_WriteSpan_T]:
        ...


class SafeBuffer(Microsoft.Win32.SafeHandles.SafeHandleZeroOrMinusOneIsInvalid, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    @property
    def byte_length(self) -> int:
        ...

    @property
    def initialize(self) -> System.Runtime.InteropServices._SafeBuffer_Initialize:
        ...

    @property
    def read(self) -> System.Runtime.InteropServices._SafeBuffer_Read:
        ...

    @property
    def read_array(self) -> System.Runtime.InteropServices._SafeBuffer_ReadArray:
        ...

    @property
    def read_span(self) -> System.Runtime.InteropServices._SafeBuffer_ReadSpan:
        ...

    @property
    def write(self) -> System.Runtime.InteropServices._SafeBuffer_Write:
        ...

    @property
    def write_array(self) -> System.Runtime.InteropServices._SafeBuffer_WriteArray:
        ...

    @property
    def write_span(self) -> System.Runtime.InteropServices._SafeBuffer_WriteSpan:
        ...

    def __init__(self, owns_handle: bool) -> None:
        ...

    def acquire_pointer(self, pointer: typing.Any) -> None:
        ...

    def release_pointer(self) -> None:
        ...


class ProgIdAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> str:
        ...

    def __init__(self, prog_id: str) -> None:
        ...


class OutAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class ComVisibleAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> bool:
        ...

    def __init__(self, visibility: bool) -> None:
        ...


class ExtendedLayoutAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self, layout_kind: System.Runtime.InteropServices.ExtendedLayoutKind) -> None:
        ...


class ComDefaultInterfaceAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> typing.Type:
        ...

    def __init__(self, default_interface: typing.Type) -> None:
        ...


class ICustomAdapter(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def get_underlying_object(self) -> System.Object:
        ...


class ICustomQueryInterface(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def get_interface(self, iid: System.Guid, ppv: typing.Optional[System.IntPtr]) -> typing.Tuple[System.Runtime.InteropServices.CustomQueryInterfaceResult, System.IntPtr]:
        ...


class VariantWrapper(System.Object):
    """This class has no documentation."""

    @property
    def wrapped_object(self) -> System.Object:
        ...

    def __init__(self, obj: typing.Any) -> None:
        ...


class _Typed_CollectionsMarshal_AsSpan(typing.Generic[System_Runtime_InteropServices_CollectionsMarshal_AsSpan_T]):
    """"""

    @overload
    def __call__(self, list: System.Collections.Generic.List[System_Runtime_InteropServices_CollectionsMarshal_AsSpan_T]) -> System.Span[System_Runtime_InteropServices_CollectionsMarshal_AsSpan_T]:
        ...


class _CollectionsMarshal_AsSpan:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_CollectionsMarshal_AsSpan_T]) -> System.Runtime.InteropServices._Typed_CollectionsMarshal_AsSpan[System_Runtime_InteropServices_CollectionsMarshal_AsSpan_T]:
        ...


class _Typed_CollectionsMarshal_GetValueRefOrNullRef(typing.Generic[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TKey]):
    """"""

    @overload
    def __call__(self, dictionary: System.Collections.Generic.Dictionary[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TKey, System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TValue], key: System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TKey) -> typing.Any:
        ...

    @overload
    def __call__(self, dictionary: System.Collections.Generic.Dictionary.AlternateLookup[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TAlternateKey], key: System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TAlternateKey) -> typing.Any:
        ...


class _CollectionsMarshal_GetValueRefOrNullRef:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TKey]) -> System.Runtime.InteropServices._Typed_CollectionsMarshal_GetValueRefOrNullRef[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrNullRef_TKey]:
        ...


class _Typed_CollectionsMarshal_GetValueRefOrAddDefault(typing.Generic[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TKey]):
    """"""

    @overload
    def __call__(self, dictionary: System.Collections.Generic.Dictionary[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TKey, System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TValue], key: System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TKey, exists: typing.Optional[bool]) -> typing.Tuple[typing.Any, bool]:
        ...

    @overload
    def __call__(self, dictionary: System.Collections.Generic.Dictionary.AlternateLookup[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TAlternateKey], key: System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TAlternateKey, exists: typing.Optional[bool]) -> typing.Tuple[typing.Any, bool]:
        ...


class _CollectionsMarshal_GetValueRefOrAddDefault:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TKey]) -> System.Runtime.InteropServices._Typed_CollectionsMarshal_GetValueRefOrAddDefault[System_Runtime_InteropServices_CollectionsMarshal_GetValueRefOrAddDefault_TKey]:
        ...


class _Typed_CollectionsMarshal_SetCount(typing.Generic[System_Runtime_InteropServices_CollectionsMarshal_SetCount_T]):
    """"""

    @overload
    def __call__(self, list: System.Collections.Generic.List[System_Runtime_InteropServices_CollectionsMarshal_SetCount_T], count: int) -> None:
        ...


class _CollectionsMarshal_SetCount:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_CollectionsMarshal_SetCount_T]) -> System.Runtime.InteropServices._Typed_CollectionsMarshal_SetCount[System_Runtime_InteropServices_CollectionsMarshal_SetCount_T]:
        ...


class CollectionsMarshal(System.Object):
    """This class has no documentation."""

    as_span: System.Runtime.InteropServices._CollectionsMarshal_AsSpan

    get_value_ref_or_null_ref: System.Runtime.InteropServices._CollectionsMarshal_GetValueRefOrNullRef

    get_value_ref_or_add_default: System.Runtime.InteropServices._CollectionsMarshal_GetValueRefOrAddDefault

    set_count: System.Runtime.InteropServices._CollectionsMarshal_SetCount

    @staticmethod
    def as_bytes(array: System.Collections.BitArray) -> System.Span[int]:
        ...


class UnmanagedFunctionPointerAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def calling_convention(self) -> System.Runtime.InteropServices.CallingConvention:
        ...

    @property
    def best_fit_mapping(self) -> bool:
        ...

    @best_fit_mapping.setter
    def best_fit_mapping(self, value: bool) -> None:
        ...

    @property
    def set_last_error(self) -> bool:
        ...

    @set_last_error.setter
    def set_last_error(self, value: bool) -> None:
        ...

    @property
    def throw_on_unmappable_char(self) -> bool:
        ...

    @throw_on_unmappable_char.setter
    def throw_on_unmappable_char(self, value: bool) -> None:
        ...

    @property
    def char_set(self) -> System.Runtime.InteropServices.CharSet:
        ...

    @char_set.setter
    def char_set(self, value: System.Runtime.InteropServices.CharSet) -> None:
        ...

    def __init__(self, calling_convention: System.Runtime.InteropServices.CallingConvention) -> None:
        ...


class DefaultParameterValueAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> System.Object:
        ...

    def __init__(self, value: typing.Any) -> None:
        ...


class GuidAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> str:
        ...

    def __init__(self, guid: str) -> None:
        ...


class AllowReversePInvokeCallsAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class StructLayoutAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def value(self) -> System.Runtime.InteropServices.LayoutKind:
        ...

    @property
    def pack(self) -> int:
        ...

    @pack.setter
    def pack(self, value: int) -> None:
        ...

    @property
    def size(self) -> int:
        ...

    @size.setter
    def size(self, value: int) -> None:
        ...

    @property
    def char_set(self) -> System.Runtime.InteropServices.CharSet:
        ...

    @char_set.setter
    def char_set(self, value: System.Runtime.InteropServices.CharSet) -> None:
        ...

    @overload
    def __init__(self, layout_kind: System.Runtime.InteropServices.LayoutKind) -> None:
        ...

    @overload
    def __init__(self, layout_kind: int) -> None:
        ...


class BStrWrapper(System.Object):
    """This class has no documentation."""

    @property
    def wrapped_object(self) -> str:
        ...

    @overload
    def __init__(self, value: str) -> None:
        ...

    @overload
    def __init__(self, value: typing.Any) -> None:
        ...


class IDynamicInterfaceCastable(metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def get_interface_implementation(self, interface_type: System.RuntimeTypeHandle) -> System.RuntimeTypeHandle:
        ...

    def is_interface_implemented(self, interface_type: System.RuntimeTypeHandle, throw_if_not_implemented: bool) -> bool:
        ...


class DynamicInterfaceCastableImplementationAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CoClassAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def co_class(self) -> typing.Type:
        ...

    def __init__(self, co_class: typing.Type) -> None:
        ...


class SafeArrayRankMismatchException(System.SystemException):
    """This class has no documentation."""

    @overload
    def __init__(self) -> None:
        ...

    @overload
    def __init__(self, message: str) -> None:
        ...

    @overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        ...


class PreserveSigAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class WasmImportLinkageAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class _Typed_ImmutableCollectionsMarshal_AsImmutableArray(typing.Generic[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsImmutableArray_T]):
    """"""

    @overload
    def __call__(self, array: typing.List[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsImmutableArray_T]) -> System.Collections.Immutable.ImmutableArray[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsImmutableArray_T]:
        ...


class _ImmutableCollectionsMarshal_AsImmutableArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsImmutableArray_T]) -> System.Runtime.InteropServices._Typed_ImmutableCollectionsMarshal_AsImmutableArray[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsImmutableArray_T]:
        ...


class _Typed_ImmutableCollectionsMarshal_AsArray(typing.Generic[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsArray_T]):
    """"""

    @overload
    def __call__(self, array: System.Collections.Immutable.ImmutableArray[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsArray_T]) -> typing.List[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsArray_T]:
        ...


class _ImmutableCollectionsMarshal_AsArray:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsArray_T]) -> System.Runtime.InteropServices._Typed_ImmutableCollectionsMarshal_AsArray[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsArray_T]:
        ...


class _Typed_ImmutableCollectionsMarshal_AsMemory(typing.Generic[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsMemory_T]):
    """"""

    @overload
    def __call__(self, builder: System.Collections.Immutable.ImmutableArray.Builder) -> System.Memory[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsMemory_T]:
        ...


class _ImmutableCollectionsMarshal_AsMemory:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsMemory_T]) -> System.Runtime.InteropServices._Typed_ImmutableCollectionsMarshal_AsMemory[System_Runtime_InteropServices_ImmutableCollectionsMarshal_AsMemory_T]:
        ...


class ImmutableCollectionsMarshal(System.Object):
    """This class has no documentation."""

    as_immutable_array: System.Runtime.InteropServices._ImmutableCollectionsMarshal_AsImmutableArray

    as_array: System.Runtime.InteropServices._ImmutableCollectionsMarshal_AsArray

    as_memory: System.Runtime.InteropServices._ImmutableCollectionsMarshal_AsMemory


class ComInterfaceDispatch_GetInstance:
    """"""

    def __getitem__(self, type: typing.Type[System_Runtime_InteropServices_ComWrappers_GetInstance_ComInterfaceDispatch_T]) -> System.Runtime.InteropServices._Typed_ComWrappers.ComInterfaceDispatch_GetInstance[System_Runtime_InteropServices_ComWrappers_GetInstance_ComInterfaceDispatch_T]:
        ...


class ComInterfaceDispatch_GetInstance(typing.Generic[System_Runtime_InteropServices_ComWrappers_GetInstance_ComInterfaceDispatch_T]):
    """"""

    @overload
    def __call__(self, dispatch_ptr: typing.Any) -> System_Runtime_InteropServices_ComWrappers_GetInstance_ComInterfaceDispatch_T:
        ...

    @overload
    def __call__(self, dispatch_ptr: typing.Any) -> System_Runtime_InteropServices_ComWrappers_GetInstance_ComInterfaceDispatch_T:
        ...


