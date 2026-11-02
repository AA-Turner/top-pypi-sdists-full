    module RangesTests
    use RangeUtils
    implicit none

    contains

    function RunRangesTests() result(fails)
    integer fails
    type(TRanges) R
    double precision, allocatable :: tmp(:)
    double precision, pointer :: P(:)

    fails = 0
    ! Combine set of ranges with specified approx maximum spacing in each
    call R%Add(1.d0, 5.d0, 4) ! 1, 2,3, 4, 5
    call R%Add_delta(0.5d0, 2.d0, 0.5d0)
    call R%Add_delta(2.d0, 4.d0, 1.1d0) ! Should be ignored as wider spacing
    call R%GetArray()
    if (any(R%points /= [0.5d0, 1.d0, 1.5d0, 2.d0, 3.d0, 4.d0, 5.d0])) then
        fails = fails + 1
        print *, 'Error in Ranges', R%points
    end if
    ! Check very close points merged
    call R%Add_delta(1.39999d0, 1.800001d0, 0.1d0)
    call R%GetArray()
    if (any(R%points == 1.5d0)) then
        fails = fails + 1
        print *, 'Error in ranges merge', R%points
    end if
    call R%Free()
    call R%Add(1d-3, 10.d0, 4, IsLog=.true.)
    call R%Add_delta(-2.d0, 3.d0, 1.d0)
    call R%GetArray()
    if (R%points(1) /= -2.d0 .or. abs(R%points(4) - 1d-2) > 1d-10) then
        fails = fails + 1
        print *, 'Error in neg range', R%points
    end if
    call R%Free()
    call R%Add(1d-3, 10.d0, 4, IsLog=.true.)
    call R%Add_delta(1.d0, 15.d0, 1.d0)
    call R%GetArray()
    if (abs(R%points(5) - 2.d0) > 1d-10 .or. abs(R%points(2) - 0.01d0) > 1d-10) then
        fails = fails + 1
        print *, 'Error in log range', R%points
    end if
    ! Test ordering invariance (not generally true, but is here)
    call R%Free()
    call R%Add(1d-3, 10.d0, 4, IsLog=.true.)
    call R%Add_delta(0.d0, 3.d0, 1.d0)
    call R%GetArray()
    allocate(tmp, source=R%points)
    call R%Free()
    call R%Add_delta(0.d0, 3.d0, 1.d0)
    call R%Add(1d-3, 10.d0, 4, IsLog=.true.)
    call R%GetArray()
    if (size(tmp) /= size(R%points)) then
        fails = fails + 1
        print *, 'Error in size on range add ordering'
        print *, 'arr 1', tmp
        print *, 'arr 2 ', R%points
    else if (any(abs(tmp - R%points) > 1d-7)) then
        fails = fails + 1
        print *, 'Error in range add ordering'
        print *, 'arr 1', tmp
        print *, 'arr 2 ', R%points
    end if

    call R%Free()
    call R%Add_delta(1.d0, 5.d0, 1.d0)
    call R%Add(1d-3, 4.d0, 4, IsLog=.true.)
    call R%GetArray()
    if (abs(R%points(5) - 1) > 1d-10) then
        fails = fails + 1
        print *, 'error in log left of linear'
        print *, R%points
    end if
    deallocate(tmp)
    allocate(tmp, source=R%Array())
    call R%Free()
    call R%Add(1d-3, 4.d0, 4, IsLog=.true.)
    call R%Add_delta(1.d0, 5.d0, 1.d0)
    if (any(abs(R%Array() - tmp) > 1d-10)) then
        fails = fails + 1
        print *, 'error in linear right of log'
        print *, R%points
    end if
    call R%Free()
    call R%Add(1d-3, 4.d0, 4, IsLog=.true.)
    call R%Add_delta(3.d0, 7.d0, 1.d0)
    call R%Add_delta(2.d0, 4.3d0, 0.1d0)
    P => R%Array()
    if (abs(P(size(P) - 1) - 6.1d0) > 1d-10) then
        fails = fails + 1
        print *, 'error in intersecting arrays'
        print *, R%Array()
    end if

    ! IndexOf/IndexOfOrdered/dArray on a simple evenly-spaced range [1,2,3,4,5]
    call R%Free()
    call R%Add(1.d0, 5.d0, 4)
    if (R%IndexOf(1.d0) /= 1 .or. R%IndexOf(3.d0) /= 3 .or. &
        R%IndexOf(5.d0) /= 5 .or. R%IndexOf(4.5d0) /= 4) then
        fails = fails + 1
        print *, 'Error in IndexOf', R%IndexOf(1.d0), R%IndexOf(3.d0), R%IndexOf(5.d0), R%IndexOf(4.5d0)
    end if

    block
        double precision :: vals(5)
        integer :: indices(5), i
        vals = [1.d0, 2.3d0, 3.d0, 4.5d0, 5.d0]
        call R%IndexOfOrdered(vals, 5, indices)
        do i = 1, 5
            if (indices(i) /= R%IndexOf(vals(i))) then
                fails = fails + 1
                print *, 'Error in IndexOfOrdered (ascending)', i, indices(i), R%IndexOf(vals(i))
            end if
        end do
        ! descending order should give the same per-value result
        vals = [5.d0, 4.5d0, 3.d0, 2.3d0, 1.d0]
        call R%IndexOfOrdered(vals, 5, indices)
        do i = 1, 5
            if (indices(i) /= R%IndexOf(vals(i))) then
                fails = fails + 1
                print *, 'Error in IndexOfOrdered (descending)', i, indices(i), R%IndexOf(vals(i))
            end if
        end do
    end block

    ! Getdpoints must also materialize points when called directly after Add.
    call R%Getdpoints()
    if (.not. allocated(R%points) .or. &
        any(abs(R%dpoints - [0.5d0, 1.d0, 1.d0, 1.d0, 0.5d0]) > 1d-10)) then
        fails = fails + 1
        print *, 'Error in direct Getdpoints', R%dpoints
    end if
    if (any(abs(R%dArray() - [0.5d0, 1.d0, 1.d0, 1.d0, 0.5d0]) > 1d-10)) then
        fails = fails + 1
        print *, 'Error in dArray', R%dArray()
    end if

    if (fails == 0) print *, 'Ranges OK'

    end function

    end module
