    module MiscTests
    use MiscUtils
    implicit none

    contains

    function RunMiscTests() result(fails)
    integer fails
    character(len=:), pointer :: SP
    character(len=5), target :: def, present_val

    fails = 0

    if (DefaultFalse() .or. .not. DefaultFalse(.true.) .or. DefaultFalse(.false.)) then
        fails = fails + 1
        print *, 'Error in DefaultFalse'
    end if
    if (.not. DefaultTrue() .or. DefaultTrue(.false.) .or. .not. DefaultTrue(.true.)) then
        fails = fails + 1
        print *, 'Error in DefaultTrue'
    end if

    if (PresentDefault(5, 7) /= 7 .or. PresentDefault(5) /= 5) then
        fails = fails + 1
        print *, 'Error in PresentDefault (integer)'
    end if
    if (abs(PresentDefault(1.5, 2.5) - 2.5) > 1e-6 .or. abs(PresentDefault(1.5) - 1.5) > 1e-6) then
        fails = fails + 1
        print *, 'Error in PresentDefault (real)'
    end if
    if (abs(PresentDefault(1.5d0, 2.5d0) - 2.5d0) > 1d-10 .or. abs(PresentDefault(1.5d0) - 1.5d0) > 1d-10) then
        fails = fails + 1
        print *, 'Error in PresentDefault (double)'
    end if
    if (.not. PresentDefault(.false., .true.) .or. PresentDefault(.true., .false.) .or. &
        .not. PresentDefault(.true.)) then
        fails = fails + 1
        print *, 'Error in PresentDefault (logical)'
    end if

    def = 'defau'
    present_val = 'prsnt'
    SP => PresentDefault(def, present_val)
    if (SP /= 'prsnt') then
        fails = fails + 1
        print *, 'Error in PresentDefault (string, present)'
    end if
    SP => PresentDefault(def)
    if (SP /= 'defau') then
        fails = fails + 1
        print *, 'Error in PresentDefault (string, default)'
    end if

    if (IfThenElse(.true., 3, 5) /= 3 .or. IfThenElse(.false., 3, 5) /= 5) then
        fails = fails + 1
        print *, 'Error in IfThenElse (integer)'
    end if
    if (abs(IfThenElse(.true., 1.5, 2.5) - 1.5) > 1e-6 .or. abs(IfThenElse(.false., 1.5, 2.5) - 2.5) > 1e-6) then
        fails = fails + 1
        print *, 'Error in IfThenElse (real)'
    end if
    if (abs(IfThenElse(.true., 1.5d0, 2.5d0) - 1.5d0) > 1d-10 .or. &
        abs(IfThenElse(.false., 1.5d0, 2.5d0) - 2.5d0) > 1d-10) then
        fails = fails + 1
        print *, 'Error in IfThenElse (double)'
    end if
    if (.not. IfThenElse(.true., .true., .false.) .or. IfThenElse(.false., .true., .false.)) then
        fails = fails + 1
        print *, 'Error in IfThenElse (logical)'
    end if
    SP => IfThenElse(.true., present_val, def)
    if (SP /= 'prsnt') then
        fails = fails + 1
        print *, 'Error in IfThenElse (string)'
    end if

    block
        real :: r1(3)
        double precision :: d1(3)
        integer :: i1(3)
        r1 = 1.
        d1 = 1.d0
        i1 = 1
        if (.not. IsFloat(1.) .or. .not. IsFloat(1.d0) .or. IsFloat(1)) then
            fails = fails + 1
            print *, 'Error in IsFloat (scalar)'
        end if
        if (.not. IsFloat(r1) .or. .not. IsFloat(d1) .or. IsFloat(i1)) then
            fails = fails + 1
            print *, 'Error in IsFloat (1D array)'
        end if
    end block

    block
        real :: r2(2, 2)
        integer :: i2(2, 2)
        r2 = 1.
        i2 = 1
        if (.not. IsFloat(r2) .or. IsFloat(i2)) then
            fails = fails + 1
            print *, 'Error in IsFloat (2D array)'
        end if
    end block

    if (fails == 0) print *, 'OK misc tests'

    end function

    end module
