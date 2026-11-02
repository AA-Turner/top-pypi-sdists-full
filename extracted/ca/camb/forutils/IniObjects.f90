    ! Module to read in name/value pairs from a file, with each line of the form line 'name = value'
    ! Should correctly interpret FITS headers
    ! Antony Lewis (http://cosmologist.info/). Released to the public domain.
    ! 2014 using Fortran 2003/2008

    module IniObjects
    use FileUtils
    use StringUtils
    use MiscUtils
    implicit none
    private

    character(len=0), target :: Empty_String = ''
    integer, parameter :: Ini_Enumeration_Len = 64

    type TNameValue
        character(len=:), allocatable :: Name
        character(len=:), allocatable :: Value
    end type TNameValue

    type TNameValue_pointer
        type(TNameValue), pointer :: P
    end type TNameValue_pointer

    type TNameValueList
        integer :: Count = 0
        integer :: Delta = 128
        integer :: Capacity = 0
        logical :: ignoreDuplicates = .false.
        logical :: AllowDuplicateKeys = .false.
        ! Use pointer so arrays can be moved around quickly without deep copies
        type(TNameValue_pointer), dimension(:), allocatable :: Items
    contains
    procedure :: Init => TNameValueList_Init
    procedure :: Clear => TNameValueList_Clear
    procedure :: ValueOf => TNameValueList_ValueOf
    procedure :: IndexOf => TNameValueList_IndexOf
    procedure :: HasKey => TNameValueList_HasKey
    procedure :: SetCapacity => TNameValueList_SetCapacity
    procedure :: Delete => TNameValueList_Delete
    procedure :: Error => TNameValueList_Error
    procedure :: FailStop => TNameValueList_FailStop
    procedure :: AddString => TNameValueList_Add
    procedure :: Name => TNameValueList_Name
    procedure :: Value => TNameValueList_Value
    procedure :: Override => TNameValueList_Override
    procedure :: TNameValueList_AddDouble
    procedure :: TNameValueList_AddReal
    procedure :: TNameValueList_AddInt
    procedure :: TNameValueList_AddLogical
    generic :: Add => AddString, TNameValueList_AddDouble, &
        TNameValueList_AddReal, TNameValueList_AddInt, &
        TNameValueList_AddLogical
    final :: TNameValueList_Free
    end type TNameValueList

    type, extends(TNameValueList) :: TIniFile
        logical :: SlashComments = .false.
        logical :: Echo_Read = .false.
        logical :: Fail_on_not_found = .false.
        logical :: ExpandEnvironmentVariables = .true.
        character(len=:), allocatable :: Original_filename
        type(TNameValueList) :: ReadValues
    contains
    procedure :: Open => Ini_Open
    procedure :: Open_Fromlines => Ini_Open_Fromlines
    procedure :: Close => Ini_Close
    procedure :: Read_String => Ini_Read_String
    procedure :: Read_String_Default => Ini_Read_String_Default
    procedure :: Read_String_Array => Ini_Read_String_Array
    procedure :: Read_Int_Array => Ini_Read_Int_Array
    procedure :: Read_Int => Ini_Read_Int
    procedure :: Read_Double => Ini_Read_Double
    procedure :: Read_Double_Array => Ini_Read_Double_Array
    procedure :: Read_Real => Ini_Read_Real
    procedure :: Read_Real_Array => Ini_Read_Real_Array
    procedure :: Read_Logical => Ini_Read_Logical
    procedure :: Read_Enumeration => Ini_Read_Enumeration
    procedure :: Read_Enumeration_List => Ini_Read_Enumeration_List
    procedure :: TestEqual => Ini_TestEqual
    procedure :: SaveReadValues => Ini_SaveReadValues
    procedure :: Key_To_Arraykey => Ini_Key_To_Arraykey
    procedure :: EnumerationValue => Ini_EnumerationValue
    procedure :: ResolveLinkedFile => Ini_ResolveLinkedFile
    procedure :: ExpandEnvironment => Ini_ExpandEnvironment
    procedure, private :: NameValue_AddLine => Ini_NameValue_AddLine
    procedure, private :: EmptyCheckDefault => Ini_EmptyCheckDefault
    procedure, private :: Ini_Read_Real_Change
    procedure, private :: Ini_Read_Double_Change
    procedure, private :: Ini_Read_Int_Change
    procedure, private :: Ini_Read_Logical_Change
    procedure, private :: Ini_Read_String_Change
    generic :: Read => Ini_Read_Real_Change, Ini_Read_Double_Change, Ini_Read_Int_Change, &
        Ini_Read_Logical_Change, Ini_Read_String_Change
    end type TIniFile

    public TNameValueList, TIniFile, Ini_Enumeration_Len

    contains

    subroutine TNameValueList_Init(this, ignoreDuplicates)
    class(TNameValueList) :: this
    logical, intent(in), optional :: ignoreDuplicates

    this%Count = 0
    this%Capacity = 0
    this%Delta = 128
    this%ignoreDuplicates = DefaultFalse(ignoreDuplicates)

    end subroutine TNameValueList_Init

    subroutine TNameValueList_Clear(this)
    class(TNameValueList) :: this
    integer i, status

    do i = this%Count, 1, -1
        deallocate(this%Items(i)%P, stat=status)
    end do
    deallocate(this%Items, stat=status)
    call this%Init()

    end subroutine TNameValueList_Clear

    impure elemental subroutine TNameValueList_Free(this)
    type(TNameValueList), intent(inout) :: this
    call this%Clear()

    end subroutine TNameValueList_Free

    function TNameValueList_ValueOf(this, AName) result(AValue)
    class(TNameValueList), intent(in) :: this
    character(len=*), intent(in) :: AName
    character(len=:), pointer :: AValue
    integer i

    i = this%IndexOf(AName)
    if (i /= -1) then
        AValue => this%Items(i)%P%Value
    else
        AValue => Empty_String
    end if

    end function TNameValueList_ValueOf

    function TNameValueList_Name(this, i) result(Name)
    class(TNameValueList), intent(in) :: this
    integer i
    character(len=:), pointer :: Name

    Name => this%Items(i)%P%Name

    end function TNameValueList_Name

    function TNameValueList_Value(this, i) result(Value)
    class(TNameValueList), intent(in) :: this
    integer i
    character(len=:), pointer :: Value

    Value => this%Items(i)%P%Value

    end function TNameValueList_Value

    function TNameValueList_IndexOf(this, AName) result(AValue)
    class(TNameValueList), intent(in) :: this
    character(len=*), intent(in) :: AName
    integer :: AValue
    integer i

    do i = 1, this%Count
        if (this%Items(i)%P%Name == AName) then
            AValue = i
            return
        end if
    end do
    AValue = -1

    end function TNameValueList_IndexOf

    function TNameValueList_HasKey(this, AName) result(AValue)
    class(TNameValueList), intent(in) :: this
    character(len=*), intent(in) :: AName
    logical :: AValue

    AValue = this%IndexOf(AName) /= -1

    end function TNameValueList_HasKey

    subroutine TNameValueList_Override(this, Settings, only_if_exists)
    class(TNameValueList) :: this
    class(TNameValueList), intent(in) :: Settings
    logical, intent(in), optional :: only_if_exists
    integer i, ix
    character(len=:), pointer :: name

    do i = 1, Settings%Count
        name => Settings%Name(i)
        ix = this%IndexOf(name)
        if (ix /= -1) then
            this%Items(ix)%P%Value = Settings%Value(i)
        else if (.not. DefaultFalse(only_if_exists)) then
            call this%Add(name, Settings%Value(i))
        end if
    end do

    end subroutine TNameValueList_Override

    subroutine TNameValueList_Add(this, AName, AValue, only_if_undefined)
    class(TNameValueList) :: this
    character(len=*), intent(in) :: AName, AValue
    logical, intent(in), optional :: only_if_undefined
    logical isDefault

    isDefault = DefaultTrue(only_if_undefined)

    if ((.not. this%AllowDuplicateKeys .or. isDefault) .and. this%HasKey(AName)) then
        if (this%ignoreDuplicates .or. isDefault) return
        call this%Error('duplicate key name', AName)
    end if
    if (this%Count == this%Capacity) call this%SetCapacity(this%Capacity + this%Delta)
    this%Count = this%Count + 1
    allocate(this%Items(this%Count)%P)
    this%Items(this%Count)%P%Name = trim(adjustl(AName))
    this%Items(this%Count)%P%Value = trim(adjustl(AValue))

    end subroutine TNameValueList_Add

    subroutine TNameValueList_AddReal(this, AName, AValue)
    class(TNameValueList) :: this
    character(len=*), intent(in) :: AName
    real, intent(in) :: AValue
    character(len=32) tmp

    write(tmp, *) AValue
    call this%AddString(AName, tmp)

    end subroutine TNameValueList_AddReal

    subroutine TNameValueList_AddDouble(this, AName, AValue)
    class(TNameValueList) :: this
    character(len=*), intent(in) :: AName
    double precision, intent(in) :: AValue
    character(len=32) tmp

    write(tmp, *) AValue
    call this%AddString(AName, tmp)

    end subroutine TNameValueList_AddDouble

    subroutine TNameValueList_AddInt(this, AName, AValue)
    class(TNameValueList) :: this
    character(len=*), intent(in) :: AName
    integer, intent(in) :: AValue
    character(len=32) tmp

    write(tmp, *) AValue
    call this%AddString(AName, tmp)

    end subroutine TNameValueList_AddInt

    subroutine TNameValueList_AddLogical(this, AName, AValue)
    class(TNameValueList) :: this
    character(len=*), intent(in) :: AName
    logical, intent(in) :: AValue
    character(len=32) tmp

    write(tmp, *) AValue
    call this%AddString(AName, tmp)

    end subroutine TNameValueList_AddLogical

    subroutine TNameValueList_SetCapacity(this, C)
    class(TNameValueList) :: this
    integer C
    type(TNameValue_pointer), dimension(:), allocatable :: TmpItems

    if (this%Count > 0) then
        if (C < this%Count) call this%Error('TNameValueList_SetCapacity, smaller than Count')
        allocate(TmpItems(C))
        TmpItems(:this%Count) = this%Items(:this%Count)
        call move_alloc(TmpItems, this%Items)
    else
        allocate(this%Items(C))
    end if
    this%Capacity = C

    end subroutine TNameValueList_SetCapacity

    subroutine TNameValueList_Delete(this, i)
    class(TNameValueList) :: this
    integer, intent(in) :: i

    deallocate(this%Items(i)%P)
    if (this%Count > 1) this%Items(i:this%Count - 1) = this%Items(i + 1:this%Count)
    this%Count = this%Count - 1

    end subroutine TNameValueList_Delete

    subroutine TNameValueList_FailStop(this)
    class(TNameValueList) :: this

    error stop

    end subroutine TNameValueList_FailStop

    subroutine TNameValueList_Error(this, Msg, Key)
    class(TNameValueList) :: this
    character(len=*) :: Msg
    character(len=*), optional :: Key

    if (present(Key)) then
        write(*, *) 'Error for key "' // trim(Key) // '" : ' // Msg
    else
        write(*, *) 'Error :' // Msg
    end if
    call this%FailStop()

    end subroutine TNameValueList_Error

    subroutine Ini_EmptyCheckDefault(this, Key, Default)
    class(TIniFile) :: this
    character(len=*), intent(in) :: Key
    class(*), intent(in), optional :: Default

    if (.not. present(Default)) call this%Error('missing key', Key)

    end subroutine Ini_EmptyCheckDefault

    function Ini_ExpandEnvironment(this, InValue) result(res)
    ! expand $(PLACEHOLDER) with environment variables, as Makefile
    class(TIniFile) :: this
    character(len=:), allocatable, intent(in) :: InValue
    character(len=:), allocatable :: res, S
    integer i

    i = index(InValue, '$(')
    if (i > 0) then
        res = InValue(:i - 1)
        S = InValue(i:)
        i = 1
        do while (i <= len(S))
            if (S(i:i) == '$') then
                if (S(i + 1:i + 1) == '$') then
                    res = res // '$'
                    i = i + 1
                else if (S(i + 1:i + 1) == '(') then
                    S = S(i + 2:)
                    i = index(S, ')')
                    if (i == 0) then
                        call this%Error('bad environment placeholder: ' // InValue)
                    end if
                    res = res // GetEnvironmentVariable(S(:i - 1))
                end if
            else
                res = res // S(i:i)
            end if
            i = i + 1
        end do
    else
        res = InValue
    end if

    end function Ini_ExpandEnvironment

    subroutine Ini_NameValue_AddLine(this, AInLine, only_if_undefined)
    class(TIniFile) :: this
    character (len=*), intent(in) :: AInLine
    integer EqPos, slashpos, lastpos
    logical, intent(in), optional :: only_if_undefined
    logical isDefault
    character (len=len(AInLine)) :: AName, InLine
    character(len=:), allocatable :: val

    isDefault = DefaultFalse(only_if_undefined)

    InLine = trim(adjustl(AInLine))
    EqPos = scan(InLine, '=')
    if (EqPos /= 0 .and. InLine(1:1) /= '#' .and. .not. StringStarts(InLine, 'COMMENT')) then
        AName = trim(InLine(1:EqPos - 1))

        val = adjustl(InLine(EqPos + 1:))
        if (this%SlashComments) then
            slashpos = scan(val, '/')
            if (slashpos /= 0) then
                val = val(1:slashpos - 1)
            end if
        end if
        if (this%ExpandEnvironmentVariables) then
            val = this%ExpandEnvironment(val)
        end if
        lastpos = len_trim(val)
        if (lastpos > 1) then
            if (val(1:1) == '''' .and. val(lastpos:lastpos) == '''') then
                val = val(2:lastpos - 1)
            end if
        end if
        call this%Add(AName, val, only_if_undefined=isDefault)
    end if

    end subroutine Ini_NameValue_AddLine

    function Ini_ResolveLinkedFile(this, name, thisfilename) result(IncludeFile)
    class(TIniFile) :: this
    character(len=*), intent(in) :: name, thisfilename
    character(len=:), allocatable :: IncludeFile

    if (.not. File%IsFullPath(name)) then
        IncludeFile = File%ExtractPath(thisfilename) // trim(name)
        if (File%Exists(IncludeFile)) then
            if (File%Exists(name) .and. name /= IncludeFile) &
                call this%Error(trim(thisfilename) // &
                ' , ambiguous multiple matches to include file: ' // trim(name))
        else
            IncludeFile = name
        end if
    else
        IncludeFile = name
    end if
    if (.not. File%Exists(IncludeFile)) then
        call this%Error(trim(thisfilename) // ' , include file not found: ' // trim(name))
    end if

    end function Ini_ResolveLinkedFile

    recursive subroutine Ini_Open(this, filename, error, slash_comments, append, only_if_undefined)
    class(TIniFile) :: this
    character (len=*), intent(in) :: filename
    logical, intent(out), optional :: error
    logical, intent(in), optional :: slash_comments
    logical, intent(in), optional :: append, only_if_undefined
    character (len=:), allocatable :: IncludeFile
    character(len=:), allocatable :: InLine
    integer lastpos, i, status
    type(TNameValueList) IncudeFiles, DefaultValueFiles
    logical isDefault
    type(TTextFile) :: F

    isDefault = DefaultFalse(only_if_undefined)

    if (.not. DefaultFalse(append)) then
        call this%TNameValueList%Init()
        call this%ReadValues%Init(.true.)
        this%Original_filename = filename
    end if

    this%SlashComments = DefaultFalse(slash_comments)

    call F%Open(filename, status=status)
    if (status /= 0) then
        if (present(error)) then
            error = .true.
            return
        else
            call this%Error('Ini_Open, file not found: ' // trim(filename))
        end if
    end if

    call IncudeFiles%Init()
    call DefaultValueFiles%Init()

    do
        if (.not. F%ReadLineSkipEmptyAndComments(InLine)) exit
        if (InLine == 'END') exit
        if (StringStarts(InLine, 'INCLUDE(')) then
            lastpos = scan(InLine, ')')
            if (lastpos /= 0) then
                call IncudeFiles%Add(InLine(9:lastpos - 1), '')
            else
                call this%Error('Ini_Open, error in INCLUDE line: ' // trim(filename))
            end if
        else if (StringStarts(InLine, 'DEFAULT(')) then
            ! Settings to read in as defaults, overridden by subsequent re-definitions
            lastpos = scan(InLine, ')')
            if (lastpos /= 0) then
                call DefaultValueFiles%Add(InLine(9:lastpos - 1), '')
            else
                call this%Error('Ini_Open, error in DEFAULT line: ' // trim(filename))
            end if
        else if (InLine /= '') then
            call this%NameValue_AddLine(InLine, only_if_undefined=isDefault)
        end if
    end do

    call F%Close()
    if (present(error)) error = .false.

    do i = 1, IncudeFiles%Count
        if (DefaultFalse(error)) exit
        IncludeFile = this%ResolveLinkedFile(IncudeFiles%Items(i)%P%Name, filename)
        call this%Open(IncludeFile, error, slash_comments, append=.true., only_if_undefined=isDefault)
    end do
    do i = 1, DefaultValueFiles%Count
        if (DefaultFalse(error)) exit
        IncludeFile = this%ResolveLinkedFile(DefaultValueFiles%Items(i)%P%Name, filename)
        call this%Open(IncludeFile, error, slash_comments, append=.true., only_if_undefined=.true.)
    end do
    call IncudeFiles%Clear()
    call DefaultValueFiles%Clear()

    end subroutine Ini_Open

    subroutine Ini_Open_Fromlines(this, Lines, NumLines, slash_comments)
    class(TIniFile) :: this
    integer, intent(in) :: NumLines
    character (len=*), dimension(NumLines), intent(in) :: Lines
    logical, intent(in), optional :: slash_comments
    integer i

    call this%TNameValueList%Init()
    call this%ReadValues%Init(.true.)

    if (present(slash_comments)) then
        this%SlashComments = slash_comments
    end if

    do i = 1, NumLines
        call this%NameValue_AddLine(Lines(i))
    end do

    end subroutine Ini_Open_Fromlines

    subroutine Ini_Close(this)
    class(TIniFile) :: this

    call this%TNameValueList%Clear()
    call this%ReadValues%Clear()

    end subroutine Ini_Close

    function Ini_Read_String(this, Key, NotFoundFail) result(AValue)
    class(TIniFile) :: this
    character (len=*), intent(in) :: Key
    logical, intent(in), optional :: NotFoundFail
    character(len=:), pointer :: AValue

    AValue => this%ValueOf(Key)

    if (AValue /= '') then
        call this%ReadValues%Add(Key, AValue)
        if (this%Echo_Read) write(*, *) trim(Key) // ' = ', trim(AValue)
        return
    end if
    if (PresentDefault(this%Fail_on_not_found, NotFoundFail)) then
        call this%Error('key not found', Key)
    end if

    end function Ini_Read_String

    function Ini_Read_String_Default(this, Key, Default, AllowBlank, EnvDefault) result(AValue)
    ! Returns from this first; if not found tries environment variable if EnvDefault is true,
    ! If not found returns Default (unless not present, in which case gives error)
    ! AllBlank specifies whether an empty string counts as a valid result to give instead of Default
    class(TIniFile) :: this
    character (len=*), intent(in) :: Key
    character (len=*), intent(in), optional :: Default
    logical, intent(in), optional :: AllowBlank
    logical, intent(in), optional :: EnvDefault
    character(len=:), allocatable :: AValue
    logical is_present

    if (this%HasKey(Key)) then
        AValue = this%Read_String(Key, .false.)
        if (AValue /= '' .or. DefaultFalse(AllowBlank)) return
    else
        AValue = ''
    end if
    if (DefaultFalse(EnvDefault)) then
        AValue = GetEnvironmentVariable(Key, is_present)
        if (DefaultFalse(AllowBlank) .and. is_present) return
    end if
    if (AValue == '') then
        if (.not. present(Default)) call this%Error('key not found', Key)
        AValue = Default
    end if
    call this%ReadValues%Add(Key, AValue)
    if (this%Echo_Read) write(*, *) trim(Key) // ' = ', trim(AValue)

    end function Ini_Read_String_Default

    function Ini_TestEqual(this, Key, value, EmptyOK) result(OK)
    class(TIniFile) :: this
    character (len=*), intent(in) :: Key, value
    logical, intent(in), optional :: EmptyOK
    character(len=:), pointer :: val
    logical :: OK

    val => this%ValueOf(Key)
    OK = val == value
    if (.not. OK .and. present(EmptyOK)) then
        OK = EmptyOK .and. val == ''
    end if

    end function Ini_TestEqual

    function Ini_Key_To_Arraykey(this, Key, index)  result(AValue)
    class(TIniFile), intent(in) :: this
    character (len=*), intent(in) :: Key
    integer, intent(in) :: index
    character(len=:), allocatable :: AValue
    character(len=32) :: numstr

    write(numstr, *) index
    numstr = adjustl(numstr)
    AValue = trim(Key) // '(' // trim(numstr) // ')'

    end function Ini_Key_To_Arraykey

    function Ini_Read_String_Array(this, Key, index, NotFoundFail) result(AValue)
    class(TIniFile) :: this
    integer, intent(in) :: index
    character (len=*), intent(in) :: Key
    logical, intent(in), optional :: NotFoundFail
    character(len=:), pointer :: AValue
    character(len=:), allocatable :: ArrayKey

    ArrayKey = this%Key_To_Arraykey(Key, index)
    AValue => this%Read_String(ArrayKey, NotFoundFail)

    end function Ini_Read_String_Array

    function Ini_Read_Int_Array(this, Key, index, Default)
    ! Reads Key(1), Key(2), etc.
    class(TIniFile) :: this
    integer Ini_Read_Int_Array
    integer, intent(in), optional :: Default
    integer, intent(in) :: index
    character(len=*), intent(in) :: Key
    character(len=:), allocatable :: ArrayKey

    ArrayKey = this%Key_To_Arraykey(Key, index)
    Ini_Read_Int_Array = this%Read_Int(ArrayKey, Default)

    end function Ini_Read_Int_Array

    function Ini_Read_Int(this, Key, Default, min, max, OK)
    class(TIniFile) :: this
    integer Ini_Read_Int
    integer, intent(in), optional :: Default, min, max
    logical, intent(out), optional :: OK
    character(len=*), intent(in) :: Key
    character(len=:), pointer :: S
    integer status

    S => this%Read_String(Key, .not. present(Default))
    if (S == '') then
        call this%EmptyCheckDefault(Key, Default)
        Ini_Read_Int = Default
        call this%ReadValues%Add(Key, Default)
    else
        if (verify(trim(S), '-+0123456789') /= 0) then
            status = 1
            if (present(OK)) then
                Ini_Read_Int = -1
                OK = .false.
                return
            end if
        else
            read(S, *, iostat=status) Ini_Read_Int
        end if
        if (status /= 0) call this%Error('error reading integer', Key)
        if (present(max)) then
            if (Ini_Read_Int > max) call this%Error('value > max', Key)
        end if
        if (present(min)) then
            if (Ini_Read_Int < min) call this%Error('value < min', Key)
        end if
    end if
    if (present(OK)) OK = .true.

    end function Ini_Read_Int

    integer function Ini_EnumerationValue(this, S, Names)
    class(TIniFile) :: this
    character(len=*) :: S
    character(len=Ini_Enumeration_Len), intent(in) :: Names(:)
    integer i

    do i = 1, size(Names)
        if (S == Names(i)) then
            Ini_EnumerationValue = i
            return
        end if
    end do
    Ini_EnumerationValue = -1

    end function Ini_EnumerationValue

    function Ini_Read_Enumeration(this, Key, Names, Default)
    class(TIniFile) :: this
    character(len=*), intent(in) :: Key
    character(len=Ini_Enumeration_Len), intent(in) :: Names(:)
    integer, intent(in), optional :: Default
    integer Ini_Read_Enumeration
    character(len=:), pointer :: S
    logical OK

    Ini_Read_Enumeration = this%Read_Int(Key, Default, OK=OK)
    if (OK) then
        if (Ini_Read_Enumeration < 1 .or. Ini_Read_Enumeration > size(Names)) &
            call this%Error('enumeration value not valid', Key)
    else
        S => this%ValueOf(Key)
        Ini_Read_Enumeration = this%EnumerationValue(S, Names)
        if (Ini_Read_Enumeration < 0) call this%Error('"' // S // '" enumeration name not recognised', Key)
    end if

    end function Ini_Read_Enumeration

    subroutine Ini_Read_Enumeration_List(this, Key, Names, Enums, nvalues, max_enums, Default)
    class(TIniFile) :: this
    character(len=*), intent(in) :: Key
    character(len=Ini_Enumeration_Len), intent(in) :: Names(:)
    integer, allocatable, intent(out) :: Enums(:)
    character(len=*), intent(in), optional :: Default
    integer, intent(in), optional :: nvalues, max_enums
    integer, parameter :: defmax = 128
    integer :: maxvalues
    integer, allocatable :: Values(:)
    character(len=Ini_Enumeration_Len + 8) part
    character(len=:), allocatable :: InLine
    integer i, slen, pos, n, status

    InLine = this%Read_String_Default(Key, Default)
    pos = 1
    slen = len_trim(InLine)
    n = 0
    maxvalues = PresentDefault(PresentDefault(defmax, max_enums), nvalues)
    allocate(Values(maxvalues))
    do
        do while (pos <= slen)
            if (IsWhiteSpace(InLine(pos:pos))) then
                pos = pos + 1
            else
                exit
            end if
        end do
        read(InLine(pos:), *, iostat=status) part
        if (status /= 0) exit
        pos = pos + len_trim(part)
        i = this%EnumerationValue(part, Names)
        if (i < 0) call this%Error('"' // part // '" enumeration name not recognised', Key)
        n = n + 1
        if (n > defmax) call this%Error('More than maximum enumeration values', Key)
        Values(n) = i
        if (n == maxvalues) exit
    end do
    if (present(nvalues)) then
        if (n == 1) then
            ! Fill whole array with same value
            allocate(Enums(nvalues), source=Values(1))
            return
        else if (n /= nvalues) then
            call this%Error('Wrong number of enumeration values', Key)
        end if
    end if
    allocate(Enums, source=Values(:n))

    end subroutine Ini_Read_Enumeration_List

    function Ini_Read_Double(this, Key, Default, min, max)
    class(TIniFile) :: this
    double precision Ini_Read_Double
    double precision, intent(in), optional :: Default, min, max
    character (len=*), intent(in) :: Key
    character(len=:), pointer :: S
    integer status

    S => this%Read_String(Key, .not. present(Default))
    if (S == '') then
        call this%EmptyCheckDefault(Key, Default)
        Ini_Read_Double = Default
        call this%ReadValues%Add(Key, Default)
    else
        read(S, *, iostat=status) Ini_Read_Double
        if (status /= 0) call this%Error('error reading double', Key)
    end if
    if (present(max)) then
        if (Ini_Read_Double > max) call this%Error('value > max', Key)
    end if
    if (present(min)) then
        if (Ini_Read_Double < min) call this%Error('value < min', Key)
    end if

    end function Ini_Read_Double

    function Ini_Read_Double_Array(this, Key, index, Default, min, max)
    ! Reads Key(1), Key(2), etc.
    class(TIniFile) :: this
    double precision Ini_Read_Double_Array
    double precision, intent(in), optional :: Default, min, max
    integer, intent(in) :: index
    character(len=*), intent(in) :: Key
    character(len=:), allocatable :: ArrayKey

    ArrayKey = this%Key_To_Arraykey(Key, index)
    Ini_Read_Double_Array = this%Read_Double(ArrayKey, Default, min, max)

    end function Ini_Read_Double_Array

    function Ini_Read_Real(this, Key, Default, min, max)
    class(TIniFile) :: this
    real Ini_Read_Real
    real, intent(in), optional :: Default, min, max
    character(len=*), intent(in) :: Key
    character(len=:), pointer :: S
    integer status

    S => this%Read_String(Key, .not. present(Default))
    if (S == '') then
        call this%EmptyCheckDefault(Key, Default)
        Ini_Read_Real = Default
        call this%ReadValues%Add(Key, Default)
    else
        read(S, *, iostat=status) Ini_Read_Real
        if (status /= 0) call this%Error('error reading real', Key)
    end if
    if (present(max)) then
        if (Ini_Read_Real > max) call this%Error('value > max', Key)
    end if
    if (present(min)) then
        if (Ini_Read_Real < min) call this%Error('value < min', Key)
    end if

    end function Ini_Read_Real

    function Ini_Read_Real_Array(this, Key, index, Default, min, max)
    ! Reads Key(1), Key(2), etc.
    class(TIniFile) :: this
    real Ini_Read_Real_Array
    real, intent(in), optional :: Default, min, max
    integer, intent(in) :: index
    character(len=*), intent(in) :: Key
    character(len=:), allocatable :: ArrayKey

    ArrayKey = this%Key_To_Arraykey(Key, index)
    Ini_Read_Real_Array = this%Read_Real(ArrayKey, Default, min, max)

    end function Ini_Read_Real_Array

    function Ini_Read_Logical(this, Key, Default)
    class(TIniFile) :: this
    logical Ini_Read_Logical
    logical, intent(in), optional :: Default
    character(len=*), intent(in) :: Key
    character(len=:), pointer :: S
    integer status

    S => this%Read_String(Key, .not. present(Default))
    if (S == '') then
        call this%EmptyCheckDefault(Key, Default)
        Ini_Read_Logical = Default
        call this%ReadValues%Add(Key, Default)
    else
        if (verify(trim(S), '10TF') /= 0) then
            status = 1
        else
            read(S, *, iostat=status) Ini_Read_Logical
        end if
        if (status /= 0) call this%Error('error reading logical', Key)
    end if

    end function Ini_Read_Logical

    subroutine Ini_SaveReadValues(this, afile)
    class(TIniFile) :: this
    character(len=*), intent(in) :: afile
    integer i
    type(TTextFile) :: F

    call F%CreateFile(afile)

    do i = 1, this%ReadValues%Count
        call F%Write(this%ReadValues%Items(i)%P%Name, ' = ', this%ReadValues%Items(i)%P%Value)
    end do

    call F%Close()

    end subroutine Ini_SaveReadValues

    subroutine Ini_Read_Int_Change(this, Key, Current, min, max)
    class(TIniFile) :: this
    character(len=*), intent(in) :: Key
    integer, intent(inout) :: Current
    integer, intent(in), optional :: min, max
    Current = this%Read_Int(Key, Current, min, max)

    end subroutine Ini_Read_Int_Change

    subroutine Ini_Read_Double_Change(this, Key, Current, min, max)
    class(TIniFile) :: this
    character(len=*), intent(in) :: Key
    double precision, intent(inout) :: Current
    double precision, intent(in), optional :: min, max
    Current = this%Read_Double(Key, Current, min, max)

    end subroutine Ini_Read_Double_Change

    subroutine Ini_Read_Real_Change(this, Key, Current, min, max)
    class(TIniFile) :: this
    character(len=*), intent(in) :: Key
    real, intent(inout) :: Current
    real, intent(in), optional :: min, max
    Current = this%Read_Real(Key, Current, min, max)

    end subroutine Ini_Read_Real_Change

    subroutine Ini_Read_Logical_Change(this, Key, Current)
    class(TIniFile) :: this
    character(len=*), intent(in) :: Key
    logical, intent(inout) :: Current
    Current = this%Read_Logical(Key, Current)

    end subroutine Ini_Read_Logical_Change

    subroutine Ini_Read_String_Change(this, Key, Current)
    class(TIniFile) :: this
    character(len=*), intent(in) :: Key
    character(len=:), allocatable, intent(inout) :: Current

    Current = this%Read_String_Default(Key, Current)

    end subroutine Ini_Read_String_Change

    end module IniObjects
