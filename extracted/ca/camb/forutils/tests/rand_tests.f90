    module RandTests
    use RandUtils
    implicit none

    contains

    function RunRandTests() result(fails)
    integer fails
    double precision :: r, expected(6)
    integer :: i
    real :: e
    double precision :: c

    fails = 0

    ! RANMAR is documented to give these six values (x 4096*4096) after
    ! seeding with IJ=1802, KL=9373 and discarding 20000 draws.
    expected = [6533892.d0, 14220222.d0, 7275067.d0, 6172232.d0, 8354498.d0, 10633180.d0]
    call RMARIN(1802, 9373)
    do i = 1, 20000
        r = RANMAR()
    end do
    do i = 1, 6
        r = RANMAR()
        if (abs(r*4096.d0*4096.d0 - expected(i)) > 1d-6) then
            fails = fails + 1
            print *, 'Error in RANMAR reference sequence', i, r*4096.d0*4096.d0, expected(i)
        end if
    end do

    block
        integer :: idx(5), j, k
        call RMARIN(1802, 9373)
        call RandIndices(idx, 10, 5)
        do j = 1, 5
            if (idx(j) < 1 .or. idx(j) > 10) then
                fails = fails + 1
                print *, 'Error in RandIndices: out of range', idx
            end if
            do k = j + 1, 5
                if (idx(j) == idx(k)) then
                    fails = fails + 1
                    print *, 'Error in RandIndices: duplicate', idx
                end if
            end do
        end do
    end block

    ! Statistical sanity check on GAUSSIAN1 (mean~0, variance~1)
    block
        integer, parameter :: n = 200000
        double precision :: s, s2, mean, var
        s = 0
        s2 = 0
        call RMARIN(1802, 9373)
        do i = 1, n
            r = GAUSSIAN1()
            s = s + r
            s2 = s2 + r*r
        end do
        mean = s/n
        var = s2/n - mean**2
        if (abs(mean) > 0.02d0 .or. abs(var - 1.d0) > 0.05d0) then
            fails = fails + 1
            print *, 'Error in GAUSSIAN1 statistics', mean, var
        end if
    end block

    e = RANDEXP1()
    if (e < 0) then
        fails = fails + 1
        print *, 'Error in RANDEXP1: negative value', e
    end if

    c = CAUCHY1()
    if (c /= c) then ! NaN check
        fails = fails + 1
        print *, 'Error in CAUCHY1: NaN'
    end if

    ! RandRotation should produce an orthogonal matrix: R^T R = I
    block
        integer, parameter :: N = 4
        double precision :: R(N, N), prod(N, N)
        integer :: j, k
        double precision :: err
        call RMARIN(1802, 9373)
        call RandRotation(R, N)
        prod = matmul(transpose(R), R)
        err = 0
        do j = 1, N
            do k = 1, N
                if (j == k) then
                    err = max(err, abs(prod(j, k) - 1.d0))
                else
                    err = max(err, abs(prod(j, k)))
                end if
            end do
        end do
        if (err > 1d-8) then
            fails = fails + 1
            print *, 'Error in RandRotation: not orthogonal', err
        end if
    end block

    if (fails == 0) print *, 'OK rand tests'

    end function

    end module
