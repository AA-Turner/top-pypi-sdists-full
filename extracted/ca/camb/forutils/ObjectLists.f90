
    module ObjectLists
    ! Implement lists of arbitrary objects
    ! AL Feb 2014
    use FileUtils
    implicit none

    private

    type Object_pointer
        class(*), pointer :: p => null()
        class(*), pointer :: Object => null()
    end type Object_pointer

    type Object_array_pointer
        class(*), pointer :: p(:) => null()
    end type Object_array_pointer

#ifdef SINGLE
    integer, parameter :: list_prec = kind(1.0)
#else
    integer, parameter :: list_prec = kind(1.d0)
#endif

    type, abstract :: TSaveLoadStateObject
    contains
    procedure :: SaveState
    procedure :: LoadState
    end type TSaveLoadStateObject

    type, extends(TSaveLoadStateObject) :: TObjectList
        integer :: Count = 0
        integer :: Delta = 32
        integer :: DeltaScale = 10
        ! expanding expanding Items, expand array by Delta + Count/DeltaScale
        integer :: Capacity = 0
        logical :: OwnsObjects = .true.
        type(Object_pointer), allocatable :: Items(:)
    contains
    procedure :: AddArray
    procedure :: AddArrayPointer
    procedure :: AddItem
    procedure :: AddItemPointer
    procedure :: AddCopy
    procedure :: AssignPointers
    procedure :: DeleteItem
    procedure :: DeleteRange
    procedure :: FreeItem
    procedure :: SetCapacity
    procedure :: ArrayItem
    procedure :: ArrayItemIndex
    procedure :: SaveBinary
    procedure :: ReadBinary
    procedure :: Thin
    procedure :: Sort
    procedure :: SortArr
    procedure :: Swap
    procedure :: Compare
    procedure :: Clear
    procedure :: DeltaSize
    procedure :: QuickSort
    procedure :: QuickSortArr
    procedure :: RemoveDuplicates
    procedure :: CheckIndex
    procedure :: Error
    procedure :: SaveState => TObjectList_SaveState
    procedure :: LoadState => TObjectList_LoadState
    procedure :: Object => TObjectList_Object ! Secondary object associated with index
    final :: finalize
    generic :: Add => AddItem, AddArray
    end type TObjectList

    type, extends(TObjectList) :: TOwnedIntrinsicList
    contains
    procedure :: AddItem => TOwnedIntrinsicList_AddItem
    procedure :: LoadState => TOwnedIntrinsicList_LoadState
    procedure :: SaveState => TOwnedIntrinsicList_SaveState
    end type

    type, extends(TOwnedIntrinsicList) :: TRealCompareList
    contains
    procedure :: Compare => CompareReal
    end type TRealCompareList

    type, extends(TRealCompareList) :: TRealList
    contains
    procedure :: TRealList_Item
    procedure :: AddArrayItems => TRealList_AddArrayItems
    procedure :: AsArray => TRealList_AsArray
    generic :: Item => TRealList_Item
    ! could add read and save state here
    end type TRealList

    type, extends(TRealCompareList) :: TRealArrayList
    contains
    procedure :: Value => TRealArrayList_Value
    procedure :: RealArrItem => TRealArrayList_Item
    generic :: Item => Value, RealArrItem
    end type TRealArrayList

    type, extends(TObjectList) :: TIntegerArrayList
    contains
    procedure :: Value => TIntegerArrayList_Value
    procedure :: IntegerArrItem => TIntegerArrayList_Item
    generic :: Item => Value, IntegerArrItem
    end type TIntegerArrayList

    type, extends(TOwnedIntrinsicList) :: TStringList
    contains
    procedure :: CharAt => TStringList_CharAt
    procedure :: Compare => TStringList_Compare
    procedure :: StringItem => TStringList_Item
    procedure :: SetFromString => TStringList_SetFromString
    procedure :: ReadColumnsGetArray => TStringList_ReadColumnsGetArray
    procedure :: IndexOf => TStringList_IndexOf
    procedure :: ValueOf => TStringList_ValueOf
    procedure :: AddItems
    procedure :: WriteItems
    procedure :: AddFromFile => TStringList_AddFromFile
    generic :: Item => StringItem
    end type TStringList

    public list_prec, TSaveLoadStateObject, TObjectList, TRealArrayList, TRealList, TIntegerArrayList, TStringList

    contains

    subroutine LoadState(this, F)
    class(TSaveLoadStateObject) :: this
    class(TFileStream) :: F

    end subroutine LoadState

    subroutine SaveState(this, F)
    class(TSaveLoadStateObject) :: this
    class(TFileStream) :: F

    end subroutine SaveState

    subroutine Clear(this, itemsOnly)
    class(TObjectList) :: this
    integer i
    logical, intent(in), optional :: itemsOnly
    logical eachItem

    if (allocated(this%Items)) then
        eachItem = .true.
        if (present(itemsOnly)) eachItem = .not. itemsOnly
        if (eachItem) then
            do i = 1, this%Count
                call this%FreeItem(i)
            end do
        end if
        deallocate(this%Items)
    end if
    this%Count = 0
    this%Capacity = 0

    end subroutine Clear

    impure elemental subroutine finalize(this)
    type(TObjectList), intent(inout) :: this
    call this%Clear()

    end subroutine finalize

    subroutine Error(this, msg)
    class(TObjectList) :: this
    character(len=*), intent(in) :: msg

    write(*, *) msg
    Error stop

    end subroutine Error

    subroutine AddItem(this, C, Object)
    class(TObjectList) :: this
    class(*), intent(in), target :: C
    class(*), intent(in), target, optional :: Object
    class(*), pointer :: CP
    class(*), pointer :: ObjectP

    ! This all looks a bit unneccessary, just trying to avoid ifort bugs, c.f.
    ! http://software.intel.com/en-us/forums/topic/390944
    ! This subroutine does *not* help directly, but derived types can use AddItemPointer which is OK.

    CP => C
    if (present(Object)) then
        ObjectP => Object
    else
        nullify(ObjectP)
    end if
    call this%AddItemPointer(CP, ObjectP)

    end subroutine AddItem

    subroutine AddItemPointer(this, C, Object)
    class(TObjectList) :: this
    class(*), intent(in), pointer :: C
    class(*), intent(in), pointer, optional :: Object

    if (this%Count == this%Capacity) call this%SetCapacity(this%Capacity + this%DeltaSize())
    this%Count = this%Count + 1
    this%Items(this%Count)%p => C
    if (present(Object)) this%Items(this%Count)%Object => Object

    end subroutine AddItemPointer

    subroutine AddCopy(this, C, Object)
    class(TObjectList) :: this
    class(*), intent(in) :: C
    class(*), intent(in), optional :: Object
    class(*), pointer :: P
    class(*), pointer :: PO

    nullify(PO)
    if (this%OwnsObjects) then
        allocate(P, source=C)
        if (present(Object)) allocate(PO, source=Object)
    else
        call this%Error('ObjectLists: Cannot add copy to un-owned list')
    end if
    call this%AddItemPointer(P, PO)

    end subroutine AddCopy

    subroutine AssignPointers(this, L2, ixmin, ixmax)
    class(TObjectList) :: this, L2
    integer, intent(in), optional :: ixmin, ixmax
    integer i1, i2

    call this%Clear()
    i1 = 1
    i2 = L2%Count
    if (present(ixmin)) i1 = ixmin
    if (present(ixmax)) i2 = ixmax
    call this%SetCapacity(i2 - i1 + 1)
    this%Items = L2%Items(i1:i2)
    this%Count = i2 - i1 + 1
    this%OwnsObjects = .false.

    end subroutine AssignPointers

    pure integer function DeltaSize(this)
    class(TObjectList), intent(in) :: this

    DeltaSize = this%Delta + this%Count/this%DeltaScale

    end function

    subroutine SetCapacity(this, C)
    class(TObjectList) :: this
    integer C
    type(Object_pointer), dimension(:), allocatable :: TmpItems

    if (this%Count > 0) then
        if (C < this%Count) call this%Error('ObjectLists: SetCapacity: smaller than Count')
        allocate(TmpItems(C))
        TmpItems(:this%Count) = this%Items(:this%Count)
        call move_alloc(TmpItems, this%Items)
    else
        allocate(this%Items(C))
    end if
    this%Capacity = C

    end subroutine SetCapacity

    subroutine FreeItem(this, i)
    class(TObjectList) :: this
    integer, intent(in) :: i
    logical want_Dealloc

    if (associated(this%Items(i)%p)) then
        want_Dealloc = this%OwnsObjects
        select type (point => this%Items(i)%p)
        class is (Object_array_pointer)
            if (this%OwnsObjects .and. associated(point%p)) deallocate(point%p)
            want_Dealloc = .true.
            ! type is (real(kind=list_prec))
            !         want_Dealloc = .false.
        end select
        if (want_Dealloc) deallocate(this%Items(i)%p)
        this%Items(i)%p => null()
    end if

    if (associated(this%Items(i)%Object) .and. this%OwnsObjects) deallocate(this%Items(i)%Object)
    this%Items(i)%Object => null()

    end subroutine FreeItem

    subroutine DeleteItem(this, i)
    class(TObjectList) :: this
    integer, intent(in) :: i

    call this%FreeItem(i)
    if (this%Count > 1) this%Items(i:this%Count - 1) = this%Items(i + 1:this%Count)
    this%Items(this%Count)%p => null()
    this%Items(this%Count)%Object => null()
    this%Count = this%Count - 1

    end subroutine DeleteItem

    subroutine DeleteRange(this, i1, i2)
    class(TObjectList) :: this
    integer, intent(in) :: i1, i2
    integer i, dN

    do i = i1, i2
        call this%FreeItem(i)
    end do
    dN = i2 - i1 + 1
    if (i2 < this%Count) this%Items(i1:this%Count - dN) = this%Items(i2 + 1:this%Count)
    do i = this%Count - dN + 1, this%Count
        this%Items(i)%p => null()
        this%Items(i)%Object => null()
    end do
    this%Count = this%Count - dN

    end subroutine DeleteRange

    subroutine AddArray(this, P)
    class(TObjectList) :: this
    class(*), target, intent(in) :: P(:)
    class(*), pointer :: Pt

    allocate(Object_array_pointer :: Pt)
    call this%AddItemPointer(Pt)
    select type (Pt)
    type is (Object_array_pointer)
        if (this%OwnsObjects) then
            allocate(Pt%p, source=P)
        else
            ! This would work on ifort, but may not be standard and does not with gfortran
            ! Pt%P => P
            call this%Error('Use AddArrayPointer to add array when ownsObjects if false')
        end if
    end select

    end subroutine AddArray

    subroutine AddArrayPointer(this, P)
    class(TObjectList) :: this
    class(*), pointer, intent(in) :: P(:)
    class(*), pointer :: Pt

    allocate(Object_array_pointer :: Pt)
    call this%AddItemPointer(Pt)
    select type (Pt)
    type is (Object_array_pointer)
        if (this%OwnsObjects) then
            allocate(Pt%p, source=P)
        else
            Pt%p => P
        end if
    end select

    end subroutine AddArrayPointer

    subroutine CheckIndex(this, i)
    class(TObjectList) :: this
    integer, intent(in) :: i

    if (i > this%Count .or. i < 1) call this%Error('Item out of range')

    end subroutine CheckIndex

    ! why this crashes in ifort 13 I do not know..
    ! subroutine AddArray(this, P)
    ! Class (TObjectList) :: this
    ! class(*), target, intent(in) :: P(:)
    ! Type(object_array_pointer), pointer :: Pt
    !
    ! allocate(Pt)
    ! call this%AddItem(Pt)
    ! if (this%ownsObjects) then
    !    allocate(Pt%P(1:SIZE(P)), source= P)
    ! else
    !    Pt%P => P
    ! end if
    ! end subroutine AddArray

    function ArrayItem(this, i) result(P)
    class(TObjectList) :: this
    integer, intent(in) :: i
    class(*), pointer :: P(:)

    call this%CheckIndex(i)
    select type (Point => this%Items(i)%p)
    class is (Object_array_pointer)
        P => Point%p
    class default
        call this%Error('ObjectLists: item is not array item')
    end select

    end function ArrayItem

    function ArrayItemIndex(this, i, j) result(P)
    class(TObjectList) :: this
    integer, intent(in) :: i, j
    class(*), pointer :: P
    class(*), pointer :: Arr(:)

    Arr => this%ArrayItem(i)
    P => Arr(j)

    end function ArrayItemIndex

    function TObjectList_Object(this, i)
    class(TObjectList) :: this
    integer, intent(in) :: i
    class(*), pointer :: TObjectList_Object

    call this%CheckIndex(i)
    TObjectList_Object => this%Items(i)%Object

    end function TObjectList_Object

    subroutine SaveBinary(this, fid)
    class(TObjectList) :: this
    integer, intent(in) :: fid
    integer i, k, sz
    class(*), pointer :: P(:)

    write(fid) this%Count
    do i = 1, this%Count
        select type (Item => this%Items(i)%p)
        class is (Object_array_pointer)
            P => this%ArrayItem(i)
            select type (Point => P)
            type is (real)
                k = 1
                write(fid) size(P), k
                write(fid) Point
            type is (double precision)
                k = 2
                write(fid) size(P), k
                write(fid) Point
            type is (integer)
                k = 3
                write(fid) size(P), k
                write(fid) Point
            type is (logical)
                k = 4
                write(fid) size(P), k
                write(fid) Point
            class default
                ! see e.g. https://cosmocoffee.info/viewtopic.php?f=11&t=2827
                call this%Error('TObjectList: Unknown type to save (if gfortran, check 7.3.1 or higher)')
            end select
        type is (character(len=*))
            k = 5
            sz = len(Item) ! len may return kind=8 in latest gfortran
            write(fid) sz, k
            write(fid) Item
        class default
            call this%Error('TObjectList: not implemented non-array save')
        end select
    end do

    end subroutine SaveBinary

    subroutine ReadBinary(this, fid)
    class(TObjectList) :: this
    integer, intent(in) :: fid
    integer num, i, sz, k
    real, pointer :: ArrR(:)
    double precision, pointer :: ArrD(:)
    integer, pointer :: ArrI(:)
    logical, pointer :: ArrL(:)
    class(*), pointer :: St, P(:)

    call this%Clear()
    this%OwnsObjects = .false.
    read(fid) num
    call this%SetCapacity(num)
    do i = 1, num
        read(fid) sz, k
        if (k == 1) then
            allocate(ArrR(sz))
            read(fid) ArrR
            P => ArrR
            call this%AddArrayPointer(P)
        else if (k == 2) then
            allocate(ArrD(sz))
            read(fid) ArrD
            P => ArrD
            call this%AddArrayPointer(P)
        else if (k == 3) then
            allocate(ArrI(sz))
            read(fid) ArrI
            P => ArrI
            call this%AddArrayPointer(P)
        else if (k == 4) then
            allocate(ArrL(sz))
            read(fid) ArrL
            P => ArrL
            call this%AddArrayPointer(P)
        else if (k == 5) then
            allocate(character(sz) :: St)
            select type (St)
            type is (character(len=*))
                read(fid) St
            end select
            call this%AddItemPointer(St)
        else
            call this%Error('TObjectList ReadBinary - unknown object type')
        end if
    end do
    this%Count = num
    this%OwnsObjects = .true.

    end subroutine ReadBinary

    subroutine Thin(this, i)
    class(TObjectList) :: this
    integer, intent(in) :: i
    integer newCount, j
    type(Object_pointer), dimension(:), pointer :: TmpItems

    if (this%Count > 1) then
        newCount = (this%Count - 1)/i + 1
        allocate(TmpItems(newCount))
        TmpItems = this%Items(1:this%Count:i)
        if (this%OwnsObjects) then
            do j = 1, this%Count
                if (mod(j - 1, i) /= 0) call this%FreeItem(j)
            end do
        end if
        deallocate(this%Items)
        this%Capacity = newCount
        allocate(this%Items, source=TmpItems)
        this%Count = newCount
        deallocate(TmpItems)
    end if

    end subroutine Thin

    subroutine Swap(this, i, j)
    class(TObjectList) :: this
    integer, intent(in) :: i, j
    type(Object_pointer) :: temp

    temp = this%Items(i)
    this%Items(i) = this%Items(j)
    this%Items(j) = temp

    end subroutine Swap

    recursive subroutine QuickSortArr(this, Lin, R, index)
    ! Sorts an array of pointers by the value of the index'th entry
    class(TObjectList) :: this
    integer, intent(in) :: Lin, R, index
    integer I, J, L
    class(*), pointer :: P

    L = Lin
    do
        I = L
        J = R
        P => this%ArrayItemIndex((L + R)/2, index)
        do
            do while (this%Compare(this%ArrayItemIndex(I, index), P) < 0)
                I = I + 1
            end do

            do while (this%Compare(this%ArrayItemIndex(J, index), P) > 0)
                J = J - 1
            end do

            if (I <= J) then
                call this%Swap(I, J)
                I = I + 1
                J = J - 1
            end if
            if (I > J) exit

        end do
        if (L < J) call this%QuickSortArr(L, J, index)
        L = I
        if (I >= R) exit
    end do

    end subroutine QuickSortArr

    subroutine SortArr(this, index)
    class(TObjectList) :: this
    integer, intent(in) :: index

    if (this%Count > 1) call this%QuickSortArr(1, this%Count, index)

    end subroutine SortArr

    recursive subroutine QuickSort(this, Lin, R)
    class(TObjectList) :: this
    integer, intent(in) :: Lin, R
    integer I, J, L
    class(*), pointer :: P

    L = Lin
    do
        I = L
        J = R
        P => this%Items((L + R)/2)%p
        do
            do while (this%Compare(this%Items(I)%p, P) < 0)
                I = I + 1
            end do

            do while (this%Compare(this%Items(J)%p, P) > 0)
                J = J - 1
            end do

            if (I <= J) then
                call this%Swap(I, J)
                I = I + 1
                J = J - 1
            end if
            if (I > J) exit
        end do
        if (L < J) call this%QuickSort(L, J)
        L = I
        if (I >= R) exit
    end do

    end subroutine QuickSort

    subroutine Sort(this)
    class(TObjectList) :: this

    if (this%Count > 1) call this%QuickSort(1, this%Count)

    end subroutine Sort

    integer function Compare(this, R1, R2) result(comp)
    class(TObjectList) :: this
    class(*) R1, R2

    comp = 0 ! equality
    call this%Error('TObjectList: Compare must be defined for derived type')

    end function Compare

    subroutine RemoveDuplicates(this)
    class(TObjectList) :: this
    integer i

    do i = this%Count - 1, 1, -1
        if (this%Compare(this%Items(i + 1)%p, this%Items(i)%p) == 0) call this%DeleteItem(i + 1)
    end do

    end subroutine RemoveDuplicates

    subroutine TObjectList_SaveState(this, F)
    class(TObjectList) :: this
    class(TFileStream) :: F
    integer i

    call F%Write(this%Count)
    do i = 1, this%Count
        select type (item => this%Items(i)%p)
        class is (TSaveLoadStateObject)
            call item%SaveState(F)
        class default
            call this%Error('TObjectList_SaveState: List contains non-TSaveLoadStateObject item')
        end select
    end do

    end subroutine TObjectList_SaveState

    subroutine TObjectList_LoadState(this, F)
    class(TObjectList) :: this
    class(TFileStream) :: F
    integer i, count

    if (.not. F%ReadItem(count) .or. count /= this%Count) &
        call this%Error('TObjectList_LoadState count mismatch (objects must exist before load)')
    do i = 1, this%Count
        select type (item => this%Items(i)%p)
        class is (TSaveLoadStateObject)
            call item%LoadState(F)
        class default
            call this%Error('List contains non-TSaveLoadStateObject item')
        end select
    end do

    end subroutine TObjectList_LoadState

    ! TOwnedIntrinsicList

    subroutine TOwnedIntrinsicList_LoadState(this, F)
    class(TOwnedIntrinsicList) :: this
    class(TFileStream) :: F
    call this%ReadBinary(F%unit)

    end subroutine TOwnedIntrinsicList_LoadState

    subroutine TOwnedIntrinsicList_SaveState(this, F)
    class(TOwnedIntrinsicList) :: this
    class(TFileStream) :: F
    call this%SaveBinary(F%unit)

    end subroutine TOwnedIntrinsicList_SaveState

    subroutine TOwnedIntrinsicList_AddItem(this, C, Object)
    class(TOwnedIntrinsicList) :: this
    class(*), intent(in), target :: C
    class(*), intent(in), target, optional :: Object

    call this%TObjectList%AddCopy(C, Object)

    end subroutine TOwnedIntrinsicList_AddItem

    ! TRealCompareList
    integer function CompareReal(this, R1, R2) result(comp)
    class(TRealCompareList) :: this
    class(*) R1, R2
    real(list_prec) R

    select type (RR1 => R1)
    type is (real(list_prec))
        select type (RR2 => R2)
        type is (real(list_prec))
            R = RR1 - RR2
            if (R < 0) then
                comp = -1
            else if (R > 0) then
                comp = 1
            else
                comp = 0
            end if
            return
        end select
    class default
        call this%Error('TRealList: Compare not defined for this type')
    end select

    end function CompareReal

    ! TRealList: List of reals
    function TRealList_Item(this, i) result(R)
    class(TRealList) :: this
    integer, intent(in) :: i
    real(list_prec) R

    call this%CheckIndex(i)
    select type (pt => this%Items(i)%p)
    type is (real(kind=list_prec))
        R = pt
    class default
        call this%Error('TRealList: object of wrong type')
    end select

    end function TRealList_Item

    subroutine TRealList_AddArrayItems(this, A)
    class(TRealList) :: this
    real(kind=list_prec), intent(in) :: A(:)
    integer i

    do i = 1, size(A)
        call this%AddItem(A(i))
    end do

    end subroutine TRealList_AddArrayItems

    function TRealList_AsArray(this) result(A)
    class(TRealList) :: this
    real(kind=list_prec) :: A(this%Count)
    integer i

    do i = 1, size(A)
        A(i) = this%Item(i)
    end do

    end function TRealList_AsArray

    ! TRealArrayList: List of arrays of reals

    function TRealArrayList_Item(this, i) result(P)
    class(TRealArrayList) :: this
    integer, intent(in) :: i
    real(list_prec), pointer :: P(:)
    class(*), pointer :: Item(:)

    Item => this%ArrayItem(i)
    select type (pt => Item)
    type is (real(kind=list_prec))
        P => pt
    class default
        call this%Error('TRealArrayList: object of wrong type')
    end select

    end function TRealArrayList_Item

    function TRealArrayList_Value(this, i, j) result(P)
    class(TRealArrayList) :: this
    integer, intent(in) :: i, j
    real(list_prec) :: P
    class(*), pointer :: C

    C => this%ArrayItemIndex(i, j)
    select type (Arr => C)
    type is (real(list_prec))
        P = Arr
    class default
        call this%Error('TRealArrayList_Value: object of wrong type (eg. ifort 2017.0.4 bug)')
    end select

    end function TRealArrayList_Value

    ! TIntegerArrayList: List of arrays of reals

    function TIntegerArrayList_Item(this, i) result(P)
    class(TIntegerArrayList) :: this
    integer, intent(in) :: i
    integer, pointer :: P(:)
    class(*), pointer :: Item(:)

    Item => this%ArrayItem(i)
    select type (pt => Item)
    type is (integer)
        P => pt
    class default
        call this%Error('TIntegerArrayList: object of wrong type')
    end select

    end function TIntegerArrayList_Item

    function TIntegerArrayList_Value(this, i, j) result(P)
    class(TIntegerArrayList) :: this
    integer, intent(in) :: i, j
    integer :: P
    class(*), pointer :: C

    C => this%ArrayItemIndex(i, j)
    select type (Arr => C)
    type is (integer)
        P = Arr
    end select

    end function TIntegerArrayList_Value

    !!! TStringList

    function TStringList_Item(this, i) result(S)
    class(TStringList) :: this
    integer, intent(in) :: i
    character(len=:), pointer :: S

    call this%CheckIndex(i)
    select type (pt => this%Items(i)%p)
    type is (character(len=*))
        S => pt
    class default
        call this%Error('TStringList: object of wrong type')
    end select

    end function TStringList_Item

    function TStringList_ValueOf(this, key)
    class(TStringList) :: this
    character(len=*), intent(in) :: key
    integer :: i
    character(len=:), pointer :: TStringList_ValueOf

    i = this%IndexOf(key)
    if (i == -1) call this%Error('TStringList_ValueOf key not found:' // key)
    select type (value => this%Items(i)%Object)
    type is (character(len=*))
        TStringList_ValueOf => value
    class default
        call this%Error('TStringList_ValueOf Object is not a string')
    end select

    end function TStringList_ValueOf

    subroutine TStringList_SetFromString(this, S, valid_chars_in)
    class(TStringList) :: this
    character(len=*), intent(in) :: S
    character(len=*), intent(in), optional :: valid_chars_in
    character(len=:), allocatable :: item
    integer i, j
    character(len=:), allocatable :: valid_chars

    if (present(valid_chars_in)) then
        valid_chars = trim(valid_chars_in)
    else
        valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.'
    end if

    call this%Clear()
    allocate(item, source=S)
    j = 0
    do i = 1, len_trim(S)
        if (verify(S(i:i), valid_chars) == 0) then
            j = j + 1
            item(j:j) = S(i:i)
        else
            if (trim(S(i:i)) /= '') then
                write(*, *) 'Invalid character in: ' // trim(S)
            end if
            if (j > 0) call this%Add(item(1:j))
            j = 0
        end if
    end do
    if (j > 0) call this%Add(item(1:j))

    end subroutine TStringList_SetFromString

    subroutine TStringList_ReadColumnsGetArray(this, filename, array)
    class(TStringList) :: this
    character(len=*), intent(in) :: filename
    real(list_prec), intent(out), allocatable :: array(:, :)
    character(len=:), allocatable :: comment

    call File%LoadTxt(filename, array, comment=comment)
    call this%SetFromString(comment)
    if (this%Count /= size(array, 1)) &
        call this%Error('Column header does not match number of columns: ' // trim(filename))

    end subroutine TStringList_ReadColumnsGetArray

    function TStringList_IndexOf(this, S) result(index)
    class(TStringList) :: this
    character(len=*), intent(in) :: S
    integer index, i

    do i = 1, this%Count
        if (this%Item(i) == S) then
            index = i
            return
        end if
    end do
    index = -1

    end function TStringList_IndexOf

    function TStringList_CharAt(this, i, j) result(C)
    class(TStringList) :: this
    integer, intent(in) :: i, j
    character :: C
    character(len=:), pointer :: P

    call this%CheckIndex(i)
    P => this%Item(i)
    C = P(j:j)

    end function TStringList_CharAt

    integer function TStringList_Compare(this, R1, R2) result(comp)
    class(TStringList) :: this
    class(*) R1, R2

    select type (RR1 => R1)
    type is (character(len=*))
        select type (RR2 => R2)
        type is (character(len=*))
            if (RR1 < RR2) then
                comp = -1
            else if (RR1 > RR2) then
                comp = 1
            else
                comp = 0
            end if
            return
        end select
    class default
        call this%Error('TStringList_Compare: not defined for this type')
    end select

    end function TStringList_Compare

    subroutine WriteItems(this, unit)
    use, intrinsic :: iso_fortran_env, only: output_unit
    class(TStringList) :: this
    integer, intent(in), optional :: unit
    integer i, aunit

    if (present(unit)) then
        aunit = unit
    else
        aunit = output_unit
    end if
    do i = 1, this%Count
        write(aunit, *) this%Item(i)
    end do

    end subroutine WriteItems

    subroutine AddItems(this, List, nodups)
    class(TStringList) :: this, List
    logical, intent(in) :: nodups
    integer i

    do i = 1, List%Count
        if (nodups) then
            if (this%IndexOf(List%Item(i)) /= -1) cycle
        end if
        if (associated(List%Items(i)%Object)) then
            call this%Add(List%Items(i)%p, List%Items(i)%Object)
        else
            call this%Add(List%Items(i)%p)
        end if
    end do

    end subroutine AddItems

    subroutine TStringList_AddFromFile(this, fname, nodups)
    class(TStringList) :: this
    character(len=*), intent(in) :: fname
    character(len=:), allocatable :: InLine
    logical, intent(in) :: nodups
    type(TTextFile) :: F

    call F%Open(fname)
    do while (F%ReadLineSkipEmptyAndComments(InLine))
        if (nodups) then
            if (this%IndexOf(InLine) /= -1) cycle
        end if
        call this%Add(InLine)
    end do
    call F%Close()

    end subroutine TStringList_AddFromFile

    end module ObjectLists
