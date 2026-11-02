    module ArrayTests
    use ArrayUtils
    implicit none

    contains

    function RunArrayTests() result(fails)
    integer fails
    character(len=:), allocatable :: S, S2
    real, allocatable :: arr(:)
    integer, allocatable :: arrI(:)
    integer :: intarr(5)

    fails = 0

    allocate(arr(3), source=[1., 2., 3.])
    call reallocate(arr, 2)
    call reallocate(arr, 5)
    call reallocate(arrI, 5)
    arrI(3) = 4
    call reallocate(arrI, 8)
    if (arr(2) /= 2. .or. arrI(3) /= 4) then
        fails = fails + 1
        print *, 'Error in realloc'
    end if
    call reallocate(arrI, 0)

    intarr = [3, 7, 1, 7, 5]
    if (IndexOf(7, intarr, 5) /= 2) then
        fails = fails + 1
        print *, 'Error in IndexOf: found value'
    end if
    if (IndexOf(9, intarr, 5) /= 0) then
        fails = fails + 1
        print *, 'Error in IndexOf: missing value'
    end if
    if (IndexOf(3, intarr, 0) /= 0) then
        fails = fails + 1
        print *, 'Error in IndexOf: empty array'
    end if

    if (MaxIndex(real(intarr), 5) /= 2 .or. MinIndex(real(intarr), 5) /= 3) then
        fails = fails + 1
        print *, 'Error in MaxIndex/MinIndex'
    end if

    if (fails == 0) print *, 'OK array tests'

    end function

    end module
