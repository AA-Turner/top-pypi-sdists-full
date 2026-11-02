    module MatrixTests
    use MatrixUtils
    implicit none

    contains

    function RunMatrixTests() result(fails)
    integer fails
    real(dm) :: A(3, 3), B(3, 2), C(3, 2), v(3), outv(3), soln(3), diag(3), Ainv(3, 3), Id(3, 3)
    real(dm), parameter :: tol = 1d-8
    integer :: i, j

    fails = 0

    ! Symmetric tridiagonal matrix
    A = reshape([4.d0, 1.d0, 0.d0, 1.d0, 3.d0, 1.d0, 0.d0, 1.d0, 2.d0], [3, 3])
    B = reshape([1.d0, 0.d0, 1.d0, 0.d0, 1.d0, 1.d0], [3, 2])
    v = [1.d0, 2.d0, 3.d0]

    if (abs(Matrix_Trace(A) - 9.d0) > tol) then
        fails = fails + 1
        print *, 'Error in Matrix_Trace', Matrix_Trace(A)
    end if

    call Matrix_Mult(A, B, C)
    if (any(abs(C - reshape([4.d0, 2.d0, 2.d0, 1.d0, 4.d0, 3.d0], [3, 2])) > tol)) then
        fails = fails + 1
        print *, 'Error in Matrix_Mult', C
    end if

    call Matrix_MulVec(A, v, outv)
    if (any(abs(outv - [6.d0, 10.d0, 8.d0]) > tol)) then
        fails = fails + 1
        print *, 'Error in Matrix_MulVec', outv
    end if

    if (abs(Matrix_vecdot(v, v) - 14.d0) > tol) then
        fails = fails + 1
        print *, 'Error in Matrix_vecdot', Matrix_vecdot(v, v)
    end if

    if (abs(Matrix_QuadForm(A, v) - 50.d0) > tol) then
        fails = fails + 1
        print *, 'Error in Matrix_QuadForm', Matrix_QuadForm(A, v)
    end if

    call Matrix_SolveSymm(A, v, soln)
    if (any(abs(matmul(A, soln) - v) > tol)) then
        fails = fails + 1
        print *, 'Error in Matrix_SolveSymm', soln
    end if

    Ainv = A
    call Matrix_Inverse(Ainv)
    Id = matmul(A, Ainv)
    do i = 1, 3
        do j = 1, 3
            if (abs(Id(i, j) - merge(1.d0, 0.d0, i == j)) > tol) then
                fails = fails + 1
                print *, 'Error in Matrix_Inverse', Id
            end if
        end do
    end do

    block
        real(dm) :: M(3, 3)
        M = A
        call Matrix_Diagonalize(M, diag, 3)
        if (any(abs(diag - [1.2679491924311228d0, 3.d0, 4.7320508075688785d0]) > 1d-6)) then
            fails = fails + 1
            print *, 'Error in Matrix_Diagonalize', diag
        end if
    end block

    block
        real(dm) :: M1(1, 1), rhs1(1), x1(1)

        M1 = reshape([4.d0], [1, 1])
        rhs1 = [12.d0]
        call Matrix_SolveSymm(M1, rhs1, x1)
        if (abs(x1(1) - 3.d0) > tol) then
            fails = fails + 1
            print *, 'Error in 1x1 Matrix_SolveSymm', x1
        end if

        M1 = reshape([4.d0], [1, 1])
        call Matrix_SolveASymm(M1, rhs1, x1)
        if (abs(x1(1) - 3.d0) > tol) then
            fails = fails + 1
            print *, 'Error in 1x1 Matrix_SolveASymm', x1
        end if

        M1 = reshape([4.d0], [1, 1])
        call Matrix_InverseAsymm(M1)
        if (abs(M1(1, 1) - 0.25d0) > tol) then
            fails = fails + 1
            print *, 'Error in 1x1 Matrix_InverseAsymm', M1
        end if
    end block

    if (fails == 0) print *, 'OK matrix tests'

    end function

    end module
