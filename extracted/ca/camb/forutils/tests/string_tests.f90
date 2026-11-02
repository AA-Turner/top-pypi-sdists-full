    module StringTests
    use StringUtils
    implicit none

    contains

    function RunStringTests() result(fails)
    integer fails
    logical, parameter :: F = .false., T = .true.
    character(len=:), allocatable :: S, S2
    fails = 0

    if (UpperCase('Low@er') /= 'LOW@ER' .or. LowerCase('1L oW@eR') /= '1l ow@er') then
        print *, 'Error in uppercase/lowercase'
        fails = fails + 1
    end if

    S = FormatString('Test %d for %f %s', 91, 3.04, 'result')
    if (S /= 'Test 91 for 3.0400 result') then
        fails = fails + 1
        print *, 'Error in FormatString: ', S
    end if

    S2 = Join(',', S, 'XP')
    if (S2 /= S // ',XP') then
        fails = fails + 1
        print *, 'Error in Join: ', S2
    end if

    if (.not. IsWhiteSpace(' ') .or. .not. IsWhiteSpace(char(9)) .or. IsWhiteSpace('a')) then
        fails = fails + 1
        print *, 'Error in IsWhiteSpace'
    end if

    if (.not. StringStarts('Hello World', 'Hello') .or. &
        .not. StringStarts('Hello World', 'World', 7) .or. &
        StringStarts('Hi', 'Hello')) then
        fails = fails + 1
        print *, 'Error in StringStarts'
    end if

    S = 'abc   '
    if (len(StringTrimmed(S, T)) /= 3 .or. len(StringTrimmed(S)) /= 6 .or. len(StringTrimmed(S, F)) /= 6) then
        fails = fails + 1
        print *, 'Error in StringTrimmed'
    end if

    S = 'Hello World'
    call StringReplace('World', 'There', S)
    if (S /= 'Hello There') then
        fails = fails + 1
        print *, 'Error in StringReplace: ', S
    end if
    call StringReplace('xyz', 'abc', S)
    if (S /= 'Hello There') then
        fails = fails + 1
        print *, 'Error in StringReplace (no match): ', S
    end if

    if (StringEscape('a,b,c', ',') /= 'a\,b\,c') then
        fails = fails + 1
        print *, 'Error in StringEscape (default escape)'
    end if
    if (StringEscape('a,b,c', ',', '!') /= 'a!,b!,c') then
        fails = fails + 1
        print *, 'Error in StringEscape (custom escape)'
    end if

    if (IntToStr(42) /= '42' .or. IntToStr(-7) /= '-7' .or. &
        IntToStr(5, 3) /= '005' .or. IntToStr(-5, 4) /= '-0005') then
        fails = fails + 1
        print *, 'Error in IntToStr'
    end if

    if (StrToInt('123') /= 123 .or. StrToInt(' -45 ') /= -45) then
        fails = fails + 1
        print *, 'Error in StrToInt'
    end if

    if (concat('Value: ', 5, ' and ', 3.5d0) /= 'Value: 5 and3.5000') then
        fails = fails + 1
        print *, 'Error in concat: ', concat('Value: ', 5, ' and ', 3.5d0)
    end if
    if (numcat('item', 7) /= 'item7') then
        fails = fails + 1
        print *, 'Error in numcat'
    end if

    if (RealToStr(3.5d0) /= '3.5000' .or. RealToStr(3.5d0, 3) /= '3.5') then
        fails = fails + 1
        print *, 'Error in RealToStr'
    end if

    if (GetParamCount() /= 0 .or. GetParam(1) /= '') then
        fails = fails + 1
        print *, 'Error in GetParamCount/GetParam'
    end if

    block
        logical :: is_present
        S = GetEnvironmentVariable('FORUTILS_TEST_UNDEFINED_VAR_XYZ', is_present)
        if (is_present .or. S /= '') then
            fails = fails + 1
            print *, 'Error in GetEnvironmentVariable'
        end if
    end block

    if (fails == 0) print *, 'OK string tests'

    end function

    end module
