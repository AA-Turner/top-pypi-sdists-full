    module MiscUtils
    implicit none

    interface PresentDefault
    module procedure PresentDefault_S, PresentDefault_L, PresentDefault_I, PresentDefault_R, PresentDefault_D
    end interface PresentDefault

    interface IfThenElse
    module procedure IfThenElse_S, IfThenElse_L, IfThenElse_I, IfThenElse_R, IfThenElse_D
    end interface IfThenElse

    interface IsFloat
    module procedure isFloat0, isFloat1, isFloat2
    end interface IsFloat

    contains

    pure elemental function DefaultFalse(S) result(Sout)
    logical, intent(in), optional :: S
    logical :: Sout

    if (present(S)) then
        Sout = S
    else
        Sout = .false.
    end if

    end function DefaultFalse

    pure elemental function DefaultTrue(S) result(Sout)
    logical, intent(in), optional :: S
    logical :: Sout

    if (present(S)) then
        Sout = S
    else
        Sout = .true.
    end if

    end function DefaultTrue

    function PresentDefault_S(default, S) result(Sout)
    character(len=*), intent(in), target :: default
    character(len=*), intent(in), target, optional :: S
    character(len=:), pointer :: Sout

    if (present(S)) then
        Sout => S
    else
        Sout => default
    end if

    end function PresentDefault_S

    pure elemental function PresentDefault_L(default, S) result(Sout)
    logical, intent(in) :: default
    logical, intent(in), optional :: S
    logical :: Sout

    if (present(S)) then
        Sout = S
    else
        Sout = default
    end if

    end function PresentDefault_L

    pure elemental function PresentDefault_I(default, S) result(Sout)
    integer, intent(in) :: default
    integer, intent(in), optional :: S
    integer :: Sout

    if (present(S)) then
        Sout = S
    else
        Sout = default
    end if

    end function PresentDefault_I

    pure elemental function PresentDefault_R(default, S) result(Sout)
    real, intent(in) :: default
    real, intent(in), optional :: S
    real :: Sout

    if (present(S)) then
        Sout = S
    else
        Sout = default
    end if

    end function PresentDefault_R

    pure elemental function PresentDefault_D(default, S) result(Sout)
    double precision, intent(in) :: default
    double precision, intent(in), optional :: S
    double precision :: Sout

    if (present(S)) then
        Sout = S
    else
        Sout = default
    end if

    end function PresentDefault_D

    function IfThenElse_S(flag, either, or) result(IfThenElse)
    logical, intent(in) :: flag
    character(len=:), pointer :: IfThenElse
    character(len=*), target :: either, or

    if (flag) then
        IfThenElse => either
    else
        IfThenElse => or
    end if

    end function

    pure elemental function IfThenElse_L(flag, either, or) result(IfThenElse)
    logical, intent(in) :: flag, either, or
    logical :: IfThenElse

    if (flag) then
        IfThenElse = either
    else
        IfThenElse = or
    end if

    end function

    pure elemental function IfThenElse_I(flag, either, or) result(IfThenElse)
    logical, intent(in) :: flag
    integer, intent(in) :: either, or
    integer :: IfThenElse

    if (flag) then
        IfThenElse = either
    else
        IfThenElse = or
    end if

    end function

    pure elemental function IfThenElse_R(flag, either, or) result(IfThenElse)
    logical, intent(in) :: flag
    real, intent(in) :: either, or
    real :: IfThenElse

    if (flag) then
        IfThenElse = either
    else
        IfThenElse = or
    end if

    end function

    pure elemental function IfThenElse_D(flag, either, or) result(IfThenElse)
    logical, intent(in) :: flag
    double precision, intent(in) :: either, or
    double precision :: IfThenElse

    if (flag) then
        IfThenElse = either
    else
        IfThenElse = or
    end if

    end function

    pure logical function isFloat0(R)
    class(*), intent(in) :: R

    select type (R)
    type is (real)
        isFloat0 = .true.
    type is (double precision)
        isFloat0 = .true.
    class default
        isFloat0 = .false.
    end select

    end function isFloat0

    pure logical function isFloat1(R)
    class(*), intent(in) :: R(:)

    isFloat1 = isFloat0(R(lbound(R, 1)))

    end function isFloat1

    pure logical function isFloat2(R)
    class(*), intent(in) :: R(:, :)

    isFloat2 = isFloat0(R(lbound(R, 1), lbound(R, 2)))

    end function isFloat2

    end module MiscUtils
