    ! Matrix utility routines. Uses BLAS/LAPACK. Mostly wrapper routines.
    ! Generally (but not always) assumes that all matrix arrays are defined at exactly correct size
    ! Not complete
    ! Antony Lewis May 2003-2014
    ! http://cosmologist.info/utils/


    module MatrixUtils
    use MpiUtils
    use FileUtils
    use StringUtils
    implicit none

    logical, parameter :: Matrix_runmsgs = .false.
#ifdef MATRIX_SINGLE
    integer, parameter :: dm = kind(1.0)
#else
    integer, parameter :: dm = kind(1.d0)
#endif
    ! Precision of matrix operators
    ! If changing also need to change prefix on LAPACK routine names
    integer, parameter :: Mat_F90 = 1, Mat_Norm = 2, Mat_DC = 3 ! Normal, basic BLAS/LAPACK or divide and conquer
    integer, parameter :: matrix_method = Mat_DC

    real Matrix_StartTime

    type TMatrixType
        real(dm), dimension(:, :), pointer :: M
    end type TMatrixType

    complex(dm), parameter :: COne = (1._dm, 0._dm), CZero = (0._dm, 0._dm)
    real(dm), parameter :: ROne = 1._dm, RZero = 0._dm
    real, parameter :: SOne = 1., SZero = 0.

    character(len=*), parameter :: Matrix_IO_fmt = '(*(1E17.7))'

    contains

    function GetMatrixTime()
    real GetMatrixTime
    real atime

    call cpu_time(atime)

    GetMatrixTime = atime

    end function GetMatrixTime

    subroutine Matrix_start(Name)
    character(len=*), intent(in) :: Name

    if (Matrix_runmsgs) then
        Matrix_StartTime = GetMatrixTime()
        write(*, *) 'Matrix_' // trim(Name) // ' start'
    end if

    end subroutine Matrix_start

    subroutine Matrix_end(Name)
    character(len=*), intent(in) :: Name

    if (Matrix_runmsgs) then
        write(*, *) 'Matrix_' // trim(Name) // ' end: ', GetMatrixTime() - Matrix_StartTime
    end if

    end subroutine Matrix_end

    subroutine Matrix_WriteFileRow(aunit, vec, n)
    integer, intent(in) :: aunit
    integer, intent(in) :: n
    real(dm) :: vec(n)

    write(aunit, Matrix_IO_fmt) vec(1:n)

    end subroutine Matrix_WriteFileRow

    subroutine Matrix_Write(aname, mat, forcetable, commentline)
    character(len=*), intent(in) :: aname
    character(len=*), intent(in), optional :: commentline
    real(dm), intent(in) :: mat(:, :)
    logical, intent(in), optional :: forcetable
    integer i, k
    integer shp(2)
    logical WriteTab
    type(TTextFile) :: F

    shp = shape(mat)
    WriteTab = shp(2) <= 50
    if (present(forcetable)) then
        if (forcetable) WriteTab = .true.
    end if
    call F%CreateFile(aname)
    if (present(commentline)) then
        call F%Write('#' // commentline)
    end if
    do i = 1, shp(1)
        if (.not. WriteTab) then
            do k = 1, shp(2)
                call F%Write(mat(i, k))
            end do
        else
            write(F%unit, F%RealFormat) mat(i, 1:shp(2))
            ! workaround for ifort 14 bug
            ! call F%Write(mat(i,1:shp(2)))
        end if
    end do
    call F%Close()

    end subroutine Matrix_Write

    subroutine Matrix_Write_double(aname, mat, forcetable)
    character(len=*), intent(in) :: aname
    double precision, intent(in) :: mat(:, :)
    logical, intent(in), optional :: forcetable
    integer i, k
    integer shp(2)
    logical WriteTab
    type(TTextFile) F

    shp = shape(mat)
    WriteTab = shp(2) <= 50
    if (present(forcetable)) then
        if (forcetable) WriteTab = .true.
    end if
    call F%CreateFile(aname)
    do i = 1, shp(1)
        if (.not. WriteTab) then
            do k = 1, shp(2)
                call F%Write(mat(i, k))
            end do
        else
            call F%Write(mat(i, 1:shp(2)))
        end if
    end do
    call F%Close()

    end subroutine Matrix_Write_double

    subroutine Matrix_Write_Binary(aname, mat)
    character(len=*), intent(in) :: aname
    real(dm), intent(in) :: mat(:, :)
    type(TBinaryFile) F

    call F%CreateFile(aname)
    write(F%unit) mat
    call F%Close()

    end subroutine Matrix_Write_Binary

    subroutine MatrixSym_Write_Binary(aname, mat)
    character(len=*), intent(in) :: aname
    real(dm), intent(in) :: mat(:, :)
    integer i
    integer shp(2)
    type(TBinaryFile) F

    shp = shape(mat)
    if (shp(1) /= shp(2)) call MpiStop('MatrixSym_Write_Binary: Not square matrix')
    if (shp(1) == 0) return

    call F%CreateFile(aname)
    do i = 1, shp(1)
        write(F%unit) mat(i:shp(2), i)
    end do
    call F%Close()

    end subroutine MatrixSym_Write_Binary

    subroutine MatrixSym_Write_Binary_Single(aname, mat)
    character(len=*), intent(in) :: aname
    real(dm), intent(in) :: mat(:, :)
    integer i
    integer shp(2)
    type(TBinaryFile) F

    shp = shape(mat)
    if (shp(1) /= shp(2)) call MpiStop('MatrixSym_Write_Binary_Single: Not square matrix')
    if (shp(1) == 0) return

    call F%CreateFile(aname)
    do i = 1, shp(1)
        write(F%unit) real(mat(i:shp(2), i), kind(1.0))
    end do
    call F%Close()

    end subroutine MatrixSym_Write_Binary_Single

    subroutine Matrix_WriteVec(aname, vec)
    character(len=*), intent(in) :: aname
    real(dm), intent(in) :: vec(:)
    integer i
    type(TTextFile) F

    call F%CreateFile(aname)
    do i = 1, size(vec)
        call F%Write(vec(i))
    end do
    call F%Close()

    end subroutine Matrix_WriteVec

    subroutine Matrix_Read_Binary(aname, mat)
    character(len=*), intent(in) :: aname
    real(dm), intent(out) :: mat(:, :)
    type(TBinaryFile) F

    call F%Open(aname)
    read(F%unit) mat
    call F%Close()

    end subroutine Matrix_Read_Binary

    subroutine MatrixSym_Read_Binary(aname, mat)
    character(len=*), intent(in) :: aname
    real(dm), intent(out) :: mat(:, :)
    integer i
    integer shp(2)
    type(TBinaryFile) F

    shp = shape(mat)
    if (shp(1) /= shp(2)) call MpiStop('MatrixSym_Read_Binary: Not square matrix')
    if (shp(1) == 0) return

    call F%Open(aname)
    do i = 1, shp(1)
        read(F%unit) mat(i:shp(1), i)
        mat(i, i:shp(1)) = mat(i:shp(1), i)
    end do
    call F%Close()

    end subroutine MatrixSym_Read_Binary

    subroutine MatrixSym_Read_Binary_Single(aname, mat)
    character(len=*), intent(in) :: aname
    real, intent(out) :: mat(:, :)
    integer i
    integer shp(2)
    type(TBinaryFile) F

    shp = shape(mat)
    if (shp(1) /= shp(2)) call MpiStop('MatrixSym_Read_Binary: Not square matrix')
    if (shp(1) == 0) return

    call F%Open(aname)
    do i = 1, shp(1)
        read(F%unit) mat(i:shp(1), i)
        mat(i, i:shp(1)) = mat(i:shp(1), i)
    end do
    call F%Close()

    end subroutine MatrixSym_Read_Binary_Single

    subroutine Matrix_Read(aname, mat)
    character(len=*), intent(in) :: aname
    real(dm), intent(out) :: mat(:, :)
    integer j, k
    integer shp(2)
    real(dm) tmp
    type(TTextFile) :: F

    shp = shape(mat)

    call F%Open(aname)

    do j = 1, shp(1)
        read(F%unit, *, end=200, err=100) mat(j, 1:shp(2))
    end do
    goto 120

100 rewind(F%unit) ! Try other possible format
    do j = 1, shp(1)
        do k = 1, shp(2)
            read(F%unit, *, end=200) mat(j, k)
        end do
    end do

120 read(F%unit, *, err=150, end=150) tmp
    goto 200

150 call F%Close()
    return

200 call MpiStop('Matrix_Read: file ' // trim(aname) // ' is the wrong size')

    end subroutine Matrix_Read

    subroutine Matrix_ReadSingle(aname, mat)
    character(len=*), intent(in) :: aname
    real, intent(out) :: mat(:, :)
    integer j, k
    integer shp(2)
    real tmp
    type(TTextFile) :: F

    shp = shape(mat)

    call F%Open(aname)

    do j = 1, shp(1)
        read(F%unit, *, end=200, err=100) mat(j, 1:shp(2))
    end do
    goto 120

100 rewind(F%unit) ! Try other possible format
    do j = 1, shp(1)
        do k = 1, shp(2)
            read(F%unit, *, end=200) mat(j, k)
        end do
    end do

120 read(F%unit, *, err=150, end=150) tmp
    goto 200

150 call F%Close()
    return

200 call MpiStop('Matrix_Read:Single file ' // trim(aname) // ' is the wrong size')

    end subroutine Matrix_ReadSingle

    pure function Matrix_Diag(M, n)
    integer, intent(in) :: n
    real(dm), intent(in) :: M(:, :)
    real(dm) Matrix_Diag(n)
    integer i

    do i = 1, n
        Matrix_Diag(i) = M(i, i)
    end do

    end function Matrix_Diag

    function ILAENV_wrap(i, S1, S2, a, b, c, d)
    integer ILAENV_wrap
    integer, intent(in) :: i, a, b, c, d
    character(len=*), intent(in) :: S1, S2
    integer, external :: ILAENV

    ! If you don't have ILAENV in math library, change routine to return some positive integer
    ! that is a guess at the blocksize
#ifdef MATRIX_SINGLE
    ILAENV_wrap = 16
#else
    ILAENV_wrap = ILAENV(i, S1, S2, a, b, c, d)
#endif
    !!!IFC

    end function ILAENV_wrap

    subroutine Matrix_Diagonalize(m, diag, n)
    ! Does m = U diag U^T, returning U in M
    integer, intent(in) :: n
    real(dm), intent(inout) :: m(n, n)
    real(dm), intent(out) :: diag(n)
    integer ierr, tmpsize
    real(dm), allocatable, dimension(:) :: tmp

    call Matrix_start('Diagonalize')
#ifdef MATRIX_SINGLE
    tmpsize = max((ILAENV_wrap(1, 'SSYTRD', 'U', n, n, n, n) + 2)*n, max(1, 3*n - 1)) ! 3*n**2
    allocate(tmp(tmpsize))
    call SSYEV('V', 'U', n, m, n, diag, tmp, tmpsize, ierr) ! evalues and vectors of symmetric matrix
#else
    tmpsize = max((ILAENV_wrap(1, 'DSYTRD', 'U', n, n, n, n) + 2)*n, max(1, 3*n - 1)) ! 3*n**2
    allocate(tmp(tmpsize))
    call DSYEV('V', 'U', n, m, n, diag, tmp, tmpsize, ierr) ! evalues and vectors of symmetric matrix
#endif
    if (ierr /= 0) call MpiStop('Error in Matrix_Diagonalize')
    deallocate(tmp)
    call Matrix_end('Diagonalize')

    end subroutine Matrix_Diagonalize

    subroutine Matrix_Diagonalize_DC(m, diag, n)
    ! Complex version. Does m = U diag U^dag, returning U in M
    integer, intent(in) :: n
    real(dm), intent(inout) :: m(n, n)
    real(dm), intent(out) :: diag(n)
    integer ierr, tmpsize, isize
    real(dm), allocatable, dimension(:) :: tmp
    integer, allocatable, dimension(:) :: iwork

    call Matrix_start('Diagonalize')

    if (matrix_method == Mat_DC) then
        ! Divide and conquer
        tmpsize = 1 + 6*n + 2*n**2
        isize = 3 + 5*n
        allocate(tmp(tmpsize))
        allocate(iwork(isize))
#ifdef MATRIX_SINGLE
        call SSYEVD('V', 'U', n, m, n, diag, tmp, tmpsize, iwork, isize, ierr) ! evalues and vectors of hermitian matrix
#else
        call DSYEVD('V', 'U', n, m, n, diag, tmp, tmpsize, iwork, isize, ierr) ! evalues and vectors of hermitian matrix
#endif
        deallocate(iwork)
        deallocate(tmp)
    else
        call Matrix_Diagonalize(m, diag, n)
    end if

    if (ierr /= 0) call MpiStop('Error in Matrix_Diagonalize')

    call Matrix_end('Diagonalize')

    end subroutine Matrix_Diagonalize_DC

    subroutine Matrix_Root(M, n, pow)
    ! Does M**pow for symmetric M using U D**pow U^T
    ! Not optimized for large matrices
    integer, intent(in) :: n
    real(dm), intent(inout) :: M(n, n)
    real(dm), allocatable :: Tmp(:, :)
    real(dm), intent(in) :: pow

    real(dm), allocatable :: diag(:)
    integer i

    allocate(Tmp(n, n), diag(n))
    call Matrix_Diagonalize(M, diag, n)
    Tmp = M
    diag = diag**pow
    do i = 1, n
        M(:, i) = M(:, i)*diag(i)
    end do
    M = matmul(M, transpose(Tmp))

    end subroutine Matrix_Root

    subroutine Matrix_Diagonalize_Partial(m, diag, n, emin, emax, nfound)
    ! Real version. Does m = U diag U^dag, returning U in M
    ! Assumes up to nfound values will be found. nfound set to true value on exit
    integer, intent(in) :: n
    real(dm), intent(inout) :: m(:, :)
    real(dm), intent(out) :: diag(:)
    real(dm), intent(in) :: emin, emax
    integer, intent(inout) :: nfound
    integer ierr, worksize, LIWork
    real(dm), allocatable, dimension(:) :: work
    real(dm), allocatable, dimension(:, :) :: tmp
    integer, allocatable, dimension(:) :: supp, iwork
    real(dm) wsize(1)
    real(dm) atol
    integer ISize(1)

    atol = 1d-9
    call Matrix_start('Matrix_Diagonalize_Partial')
    allocate(tmp(n, nfound))
    allocate(supp(n))
    ! Query
    worksize = -1
    LIWork = -1
#ifdef MATRIX_SINGLE
    call SSYEVR('V', 'V', 'U', n, m, size(m, dim=1), emin, emax, 0, 0, atol, nfound, diag, tmp, size(tmp, dim=1), &
        supp, wsize, worksize, ISize, LIWork, ierr)
#else
    call DSYEVR('V', 'V', 'U', n, m, size(m, dim=1), emin, emax, 0, 0, atol, nfound, diag, tmp, size(tmp, dim=1), &
        supp, wsize, worksize, ISize, LIWork, ierr)
#endif
    worksize = real(wsize(1))
    LIWork = ISize(1)
    allocate(work(worksize), iwork(LIWork))
#ifdef MATRIX_SINGLE
    call SSYEVR('V', 'V', 'U', n, m, size(m, dim=1), emin, emax, 0, 0, atol, nfound, diag, tmp, size(tmp, dim=1), &
        supp, work, worksize, iwork, LIWork, ierr)
#else
    call DSYEVR('V', 'V', 'U', n, m, size(m, dim=1), emin, emax, 0, 0, atol, nfound, diag, tmp, size(tmp, dim=1), &
        supp, work, worksize, iwork, LIWork, ierr)
#endif
    deallocate(supp, work, iwork)
    if (ierr /= 0) call MpiStop('Matrix_Diagonalize_Partial: Error')
    m(1:n, 1:nfound) = tmp(1:n, 1:nfound) ! nfound now different
    deallocate(tmp)
    call Matrix_end('Matrix_Diagonalize_Partial')

    end subroutine Matrix_Diagonalize_Partial

    subroutine Matrix_CDiagonalize_Partial(m, diag, n, emin, emax, nfound)
    ! Complex version. Does m = U diag U^dag, returning U in M
    ! Assumes up to nfound values will be found. nfound set to true value on exit
    integer, intent(in) :: n
    complex(dm), intent(inout) :: m(:, :)
    real(dm), intent(out) :: diag(:)
    real(dm), intent(in) :: emin, emax
    integer, intent(inout) :: nfound
    integer ierr, worksize, LRWork, LIWork
    real(dm), allocatable, dimension(:) :: Rwork
    complex(dm), allocatable, dimension(:) :: work
    complex(dm), allocatable, dimension(:, :) :: tmp
    integer, allocatable, dimension(:) :: supp, iwork
    complex(dm) wsize(1)
    real(dm) Rsize(1), atol
    integer ISize(1)

    atol = 1d-9
    call Matrix_start('Matrix_CDiagonalize_Partial')
    allocate(tmp(n, nfound))
    allocate(supp(n))
    ! Query
    worksize = -1
    LRWork = -1
    LIWork = -1
#ifdef MATRIX_SINGLE
    call CHEEVR('V', 'V', 'U', n, m, size(m, dim=1), emin, emax, 0, 0, atol, nfound, diag, tmp, size(tmp, dim=1), &
        supp, wsize, worksize, Rsize, LRWork, ISize, LIWork, ierr)
#else
    call ZHEEVR('V', 'V', 'U', n, m, size(m, dim=1), emin, emax, 0, 0, atol, nfound, diag, tmp, size(tmp, dim=1), &
        supp, wsize, worksize, Rsize, LRWork, ISize, LIWork, ierr)
#endif
    worksize = real(wsize(1))
    LRWork = Rsize(1)
    LIWork = ISize(1)
    allocate(work(worksize), Rwork(LRWork), iwork(LIWork))
#ifdef MATRIX_SINGLE
    call CHEEVR('V', 'V', 'U', n, m, size(m, dim=1), emin, emax, 0, 0, atol, nfound, diag, tmp, size(tmp, dim=1), &
        supp, work, worksize, Rwork, LRWork, iwork, LIWork, ierr)
#else
    call ZHEEVR('V', 'V', 'U', n, m, size(m, dim=1), emin, emax, 0, 0, atol, nfound, diag, tmp, size(tmp, dim=1), &
        supp, work, worksize, Rwork, LRWork, iwork, LIWork, ierr)
#endif
    deallocate(supp, work, Rwork, iwork)
    if (ierr /= 0) call MpiStop('Matrix_CDiagonalize_Partial: Error')
    m(1:n, 1:nfound) = tmp(1:n, 1:nfound) ! nfound now different
    deallocate(tmp)
    call Matrix_end('Matrix_CDiagonalize_Partial')

    end subroutine

    subroutine Matrix_CDiagonalize(m, diag, n)
    ! Complex version. Does m = U diag U^dag, returning U in M
    integer, intent(in) :: n
    complex(dm), intent(inout) :: m(n, n)
    real(dm), intent(out) :: diag(n)
    integer ierr, tmpsize, isize, rworksize
    real(dm), allocatable, dimension(:) :: Rwork
    complex(dm), allocatable, dimension(:) :: tmp
    integer, allocatable, dimension(:) :: iwork

    call Matrix_start('CDiagonalize')

    if (matrix_method == Mat_DC) then
        ! Divide and conquer
        tmpsize = 2*n + n**2
        rworksize = 1 + 4*n + 2*n*int(log(real(n))/log(2.) + 1) + 3*n**2
        isize = (2 + 5*n)*4
        allocate(tmp(tmpsize), Rwork(rworksize))
        allocate(iwork(isize))
#ifdef MATRIX_SINGLE
        ! evalues and vectors of hermitian matrix
        call CHEEVD('V', 'U', n, m, n, diag, tmp, tmpsize, Rwork, rworksize, iwork, isize, ierr)
#else
        ! evalues and vectors of hermitian matrix
        call ZHEEVD('V', 'U', n, m, n, diag, tmp, tmpsize, Rwork, rworksize, iwork, isize, ierr)
#endif
        deallocate(iwork)
    else
        rworksize = max(1, 3*n - 2)
#ifdef MATRIX_SINGLE
        tmpsize = max((ILAENV_wrap(1, 'CHETRD', 'U', n, n, n, n) + 1)*n, max(1, 2*n - 1)) ! 3*n**2
        allocate(tmp(tmpsize), Rwork(rworksize))
        call CHEEV('V', 'U', n, m, n, diag, tmp, tmpsize, Rwork, ierr) ! evalues and vectors of hermitian matrix
#else
        tmpsize = max((ILAENV_wrap(1, 'ZHETRD', 'U', n, n, n, n) + 1)*n, max(1, 2*n - 1)) ! 3*n**2
        allocate(tmp(tmpsize), Rwork(rworksize))
        call ZHEEV('V', 'U', n, m, n, diag, tmp, tmpsize, Rwork, ierr) ! evalues and vectors of hermitian matrix
#endif
    end if

    if (ierr /= 0) call MpiStop('Error in Matrix_CDiagonalize')
    deallocate(tmp, Rwork)

    call Matrix_end('CDiagonalize')

    end subroutine Matrix_CDiagonalize

    function Matrix_CTrace(M)
    complex(dm), intent(in) :: M(:, :)
    complex(dm) tmp, Matrix_CTrace
    integer i

    if (size(M, dim=1) /= size(M, dim=2)) call MpiStop('Matrix_CTrace: non-square matrix')
    tmp = 0
    do i = 1, size(M, dim=1)
        tmp = tmp + M(i, i)
    end do
    Matrix_CTrace = tmp

    end function Matrix_CTrace

    function Matrix_Trace(M)
    real(dm), intent(in) :: M(:, :)
    real(dm) tmp, Matrix_Trace
    integer i

    if (size(M, dim=1) /= size(M, dim=2)) call MpiStop('Matrix_Trace: non-square matrix')
    tmp = 0
    do i = 1, size(M, dim=1)
        tmp = tmp + M(i, i)
    end do
    Matrix_Trace = tmp

    end function Matrix_Trace

    function MatrixSym_LogDet(mat) result(logDet)
    real(dm), intent(in) :: mat(:, :)
    real(dm) logDet
    real(dm), allocatable :: Tmp(:, :)
    integer i

    if (size(mat, dim=1) /= size(mat, dim=2)) call MpiStop('MatrixSym_LogDet: non-square matrix')
    allocate(Tmp(size(mat, dim=1), size(mat, dim=1)))
    Tmp = mat
    call Matrix_Cholesky(Tmp)
    logDet = 0
    do i = 1, size(mat, dim=1)
        logDet = logDet + log(Tmp(i, i))
    end do
    logDet = 2._dm*logDet

    end function MatrixSym_LogDet

    subroutine Matrix_CRotateSymm(Mat, U, m, Out, triangular)
    ! Gets U^dag Mat U
    integer, intent(in) :: m
    complex(dm), intent(in) :: Mat(:, :), U(:, :)
    complex(dm) Out(:, :)
    complex(dm), dimension(:, :), allocatable :: C
    integer n
    logical, intent(in), optional :: triangular
    logical :: triang

    call Matrix_start('CRotateSymm')

    if (present(triangular)) then
        triang = triangular
    else
        triang = .false.
    end if

    n = size(Mat, dim=1)
    if (n /= size(Mat, dim=2)) call MpiStop('Matrix_CRotateSymm: Need square matrix')
    if (n /= size(U, dim=1)) call MpiStop('Matrix_CRotateSymm: Matrix size mismatch')
    if (size(Out, dim=1) < m .or. size(Out, dim=2) < m) &
        call MpiStop('Matrix_CRotateSymm: Wrong output size')

    if (matrix_method == Mat_F90) then
        Out = matmul(matmul(transpose(conjg(U(1:n, 1:m))), Mat), U(1:n, 1:m))
    else
#ifdef MATRIX_SINGLE
        if (triang) then
            if (m /= n) call MpiStop('Matrix_CRotateSymm: Matrices must be same size')
            call CHEMM('L', 'U', n, n, COne, Mat, size(Mat, dim=1), U, size(U, dim=1), CZero, Out, size(Out, dim=1))
            call CTRMM('Left', 'Upper', 'Complex-Transpose', 'Not-unit', n, n, COne, U, size(U, dim=1), Out, &
                size(Out, dim=1))
        else
            allocate(C(n, m))
            call CHEMM('L', 'U', n, m, COne, Mat, size(Mat, dim=1), U, size(U, dim=1), CZero, C, n)
            call CGEMM('C', 'N', m, m, n, COne, U, size(U, dim=1), C, n, CZero, Out, size(Out, dim=1))
            deallocate(C)
        end if
#else
        if (triang) then
            if (m /= n) call MpiStop('Matrix_CRotateSymm: Matrices must be same size')
            call ZHEMM('L', 'U', n, n, COne, Mat, size(Mat, dim=1), U, size(U, dim=1), CZero, Out, size(Out, dim=1))
            call ZTRMM('Left', 'Upper', 'Complex-Transpose', 'Not-unit', n, n, COne, U, size(U, dim=1), Out, &
                size(Out, dim=1))
        else
            allocate(C(n, m))
            call ZHEMM('L', 'U', n, m, COne, Mat, size(Mat, dim=1), U, size(U, dim=1), CZero, C, n)
            call ZGEMM('C', 'N', m, m, n, COne, U, size(U, dim=1), C, n, CZero, Out, size(Out, dim=1))
            deallocate(C)
        end if
#endif
    end if
    call Matrix_end('CRotateSymm')

    end subroutine Matrix_CRotateSymm

    subroutine Matrix_RotateSymm(Mat, U, m, Out, triangular)
    ! Gets U^T Mat U
    ! If triangular U = Upper triangular (U^T lower triangular)
    integer, intent(in) :: m
    real(dm), intent(in) :: Mat(:, :), U(:, :)
    real(dm) Out(:, :)
    real(dm), dimension(:, :), allocatable :: C
    logical, intent(in), optional :: triangular
    logical triang
    integer n

    call Matrix_start('RotateSymm')

    if (present(triangular)) then
        triang = triangular
    else
        triang = .false.
    end if

    n = size(Mat, dim=1)
    if (n /= size(Mat, dim=2)) call MpiStop('Matrix_RotateSymm: Need square matrix')
    if (n /= size(U, dim=1)) call MpiStop('Matrix_RotateSymm: Matrix size mismatch')
    if (size(Out, dim=1) < m .or. size(Out, dim=2) < m) &
        call MpiStop('Matrix_RotateSymm: Wrong output size')

    if (matrix_method == Mat_F90) then
        Out = matmul(matmul(transpose(U(1:n, 1:m)), Mat), U(1:n, 1:m))
    else
#ifdef MATRIX_SINGLE
        if (triang) then
            if (m /= n) call MpiStop('Matrix_RotateSymm: Matrices must be same size')
            call SSYMM('L', 'U', n, n, ROne, Mat, size(Mat, dim=1), U, size(U, dim=1), RZero, Out, size(Out, dim=1))
            call STRMM('Left', 'Upper', 'Transpose', 'Not-unit', n, n, ROne, U, size(U, dim=1), Out, size(Out, dim=1))
        else
            allocate(C(n, m))
            call SSYMM('L', 'U', n, m, ROne, Mat, size(Mat, dim=1), U, size(U, dim=1), RZero, C, n)
            call SGEMM('T', 'N', m, m, n, ROne, U, size(U, dim=1), C, n, RZero, Out, size(Out, dim=1))
            deallocate(C)
        end if
#else
        if (triang) then
            if (m /= n) call MpiStop('Matrix_RotateSymm: Matrices must be same size')
            call DSYMM('L', 'U', n, n, ROne, Mat, size(Mat, dim=1), U, size(U, dim=1), RZero, Out, size(Out, dim=1))
            call DTRMM('Left', 'Upper', 'Transpose', 'Not-unit', n, n, ROne, U, size(U, dim=1), Out, size(Out, dim=1))
        else
            allocate(C(n, m))
            call DSYMM('L', 'U', n, m, ROne, Mat, size(Mat, dim=1), U, size(U, dim=1), RZero, C, n)
            call DGEMM('T', 'N', m, m, n, ROne, U, size(U, dim=1), C, n, RZero, Out, size(Out, dim=1))
            deallocate(C)
        end if
#endif
    end if
    call Matrix_end('RotateSymm')

    end subroutine Matrix_RotateSymm

    subroutine Matrix_RotateAntiSymm(Mat, U, m, Out)
    ! Gets U^T Mat U
    ! Where Mat = -Mat^T
    integer, intent(in) :: m
    real(dm), intent(in) :: Mat(:, :), U(:, :)
    real(dm) Out(:, :)
    real(dm), dimension(:, :), allocatable :: C
    integer i, j, n

    call Matrix_start('RotateAntiSymm')

    n = size(Mat, dim=1)
    if (n /= size(Mat, dim=2)) call MpiStop('Matrix_RotateAntiSymm: Need square matrix')
    if (n /= size(U, dim=1)) call MpiStop('Matrix_RotateAntiSymm: Matrix size mismatch')
    if (size(Out, dim=1) < m .or. size(Out, dim=2) < m) &
        call MpiStop('Matrix_RotateAntiSymm: Wrong output size')

    if (matrix_method == Mat_F90) then
        Out = matmul(matmul(transpose(U(1:n, 1:m)), Mat), U(1:n, 1:m))
    else
        allocate(C(n, m))
        C = U(1:n, 1:m)
#ifdef MATRIX_SINGLE
        call STRMM('Left', 'Lower', 'Not-Transpose', 'Not-unit', n, m, ROne, Mat, size(Mat, dim=1), C, size(C, dim=1))
        call SGEMM('T', 'N', m, m, n, ROne, U, size(U, dim=1), C, n, RZero, Out, size(Out, dim=1))
#else
        call DTRMM('Left', 'Lower', 'Not-Transpose', 'Not-unit', n, m, ROne, Mat, size(Mat, dim=1), C, size(C, dim=1))
        call DGEMM('T', 'N', m, m, n, ROne, U, size(U, dim=1), C, n, RZero, Out, size(Out, dim=1))
#endif
        deallocate(C)
    end if

    do i = 1, m
        do j = 1, i
            Out(j, i) = Out(j, i) - Out(i, j)
            Out(i, j) = -Out(j, i)
        end do
    end do

    call Matrix_end('RotateAntiSymm')

    end subroutine Matrix_RotateAntiSymm

    subroutine Matrix_CMult_SymmRight(Mat, U, Out, a, b)
    complex(dm), intent(in) :: Mat(:, :), U(:, :)
    complex(dm) Out(:, :)
    complex(dm), intent(in), optional :: a, b
    complex(dm) mult, beta
    integer n, m

    call Matrix_start('CMult_SymmRight')

    m = size(Mat, dim=1)
    n = size(U, dim=2)
    if (n /= size(Mat, dim=2) .or. n /= size(U, dim=1)) &
        call MpiStop('Matrix_CMult_SymmRight: Size mismatch')
    if (present(a)) then
        mult = a
    else
        mult = COne
    end if
    if (present(b)) then
        beta = b
    else
        beta = CZero
    end if
    if (matrix_method == Mat_F90) then
        if (beta /= CZero) then
            Out = a*matmul(Mat, U) + beta*Out
        else
            Out = matmul(Mat, U)
            if (mult /= COne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call CHEMM('R', 'U', m, n, mult, U, size(U, dim=1), Mat, size(Mat, dim=1), beta, Out, size(Out, dim=1))
#else
        call ZHEMM('R', 'U', m, n, mult, U, size(U, dim=1), Mat, size(Mat, dim=1), beta, Out, size(Out, dim=1))
#endif
    end if

    call Matrix_end('CMult_SymmRight')

    end subroutine Matrix_CMult_SymmRight

    subroutine Matrix_CMult_SymmLeft(Mat, U, Out, a, b)
    complex(dm), intent(in) :: Mat(:, :), U(:, :)
    complex(dm) Out(:, :)
    complex(dm), intent(in), optional :: a, b
    complex(dm) mult, beta
    integer n, m

    call Matrix_start('CMult_SymmLeft')

    m = size(Mat, dim=1)
    n = size(U, dim=2)
    if (m /= size(U, dim=1) .or. m /= size(Mat, dim=2)) &
        call MpiStop('Matrix_CMult_SymmLeft: Size mismatch')
    if (present(a)) then
        mult = a
    else
        mult = COne
    end if
    if (present(b)) then
        beta = b
    else
        beta = CZero
    end if
    if (matrix_method == Mat_F90) then
        if (beta /= CZero) then
            Out = a*matmul(Mat, U) + beta*Out
        else
            Out = matmul(Mat, U)
            if (mult /= COne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call CHEMM('L', 'U', m, n, mult, Mat, size(Mat, dim=1), U, size(U, dim=1), beta, Out, size(Out, dim=1))
#else
        call ZHEMM('L', 'U', m, n, mult, Mat, size(Mat, dim=1), U, size(U, dim=1), beta, Out, size(Out, dim=1))
#endif
    end if

    call Matrix_end('CMult_SymmLeft')

    end subroutine Matrix_CMult_SymmLeft

    subroutine Matrix_CMult(Mat, U, Out, a, b)
    ! Out = a*Mat U + b*out
    complex(dm), intent(in) :: Mat(:, :), U(:, :)
    complex(dm) Out(:, :)
    complex(dm), intent(in), optional :: a, b
    complex(dm) mult, beta
    integer m, n, k

    call Matrix_start('CMult')

    m = size(Mat, dim=1)
    n = size(U, dim=2)
    k = size(Mat, dim=2)
    if (k /= size(U, dim=1)) call MpiStop('Matrix_Mult: Matrix size mismatch')
    if (present(a)) then
        mult = a
    else
        mult = COne
    end if
    if (present(b)) then
        beta = b
    else
        beta = CZero
    end if

    if (matrix_method == Mat_F90) then
        if (beta /= CZero) then
            Out = a*matmul(Mat, U) + beta*Out
        else
            Out = matmul(Mat, U)
            if (mult /= COne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call CGEMM('N', 'N', m, n, k, mult, Mat, m, U, k, beta, Out, size(Out, dim=1))
#else
        call ZGEMM('N', 'N', m, n, k, mult, Mat, m, U, k, beta, Out, size(Out, dim=1))
#endif
    end if
    call Matrix_end('CMult')

    end subroutine Matrix_CMult

    subroutine Matrix_MultSq_RepRight(Mat, U, a)
    ! U = a*Mat*U
    real(dm), intent(in) :: Mat(:, :)
    real(dm), intent(inout) :: U(:, :)
    real(dm), intent(in), optional :: a
    real(dm) aa
    integer m, n
    real(dm), dimension(:, :), allocatable :: tmp

    m = size(Mat, dim=1)
    n = size(Mat, dim=2)
    if (m /= n) call MpiStop('Matrix_MultSq: Matrix size mismatch')
    m = size(U, dim=1)
    n = size(U, dim=2)
    if (m /= n) call MpiStop('Matrix_MultSq: Matrix size mismatch')

    allocate(tmp(n, n))
    if (present(a)) then
        aa = a
    else
        aa = ROne
    end if

    call Matrix_Mult(Mat, U, tmp, aa)
    U = tmp
    deallocate(tmp)

    end subroutine Matrix_MultSq_RepRight

    subroutine Matrix_MultTri(Mat, L, side)
    ! Mat -> L Mat or Mat L where L is lower triangular
    real(dm), intent(inout) :: Mat(:, :)
    real(dm), intent(in) :: L(:, :)
    character(len=*), intent(in) :: side
    integer m, n

    call Matrix_start('Matrix_MultTri')

    m = size(Mat, dim=1)
    n = size(Mat, dim=2)

    if (side(1:1) == 'L') then
        if (size(L, dim=2) /= m) call MpiStop('Matrix_MultTri: Matrix size mismatch')
    else
        if (size(L, dim=1) /= n) call MpiStop('Matrix_MultTri: Matrix size mismatch')
    end if
#ifdef MATRIX_SINGLE
    call STRMM(side, 'Lower', 'Not-Transpose', 'Not-unit', m, n, ROne, L, size(L, dim=1), Mat, size(Mat, dim=1))
#else
    call DTRMM(side, 'Lower', 'Not-Transpose', 'Not-unit', m, n, ROne, L, size(L, dim=1), Mat, size(Mat, dim=1))
#endif
    call Matrix_end('Matrix_MultTri')

    end subroutine Matrix_MultTri

    subroutine Matrix_Mult(Mat, U, Out, a, b)
    ! Out = a*Mat U + b*out
    real(dm), intent(in) :: Mat(:, :), U(:, :)
    real(dm) :: Out(:, :)
    real(dm), intent(in), optional :: a, b
    real(dm) mult, beta
    integer m, n, k

    call Matrix_start('Mult')

    m = size(Mat, dim=1)
    n = size(U, dim=2)
    k = size(Mat, dim=2)
    if (k /= size(U, dim=1)) call MpiStop('Matrix_Mult: Matrix size mismatch')

    if (present(a)) then
        mult = a
    else
        mult = ROne
    end if
    if (present(b)) then
        beta = b
    else
        beta = RZero
    end if

    if (matrix_method == Mat_F90) then
        if (beta /= RZero) then
            Out = a*matmul(Mat, U) + beta*Out
        else
            Out = matmul(Mat, U)
            if (mult /= ROne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call SGEMM('N', 'N', m, n, k, mult, Mat, m, U, k, beta, Out, size(Out, dim=1))
#else
        call DGEMM('N', 'N', m, n, k, mult, Mat, m, U, k, beta, Out, size(Out, dim=1))
#endif
    end if
    call Matrix_end('Mult')

    end subroutine Matrix_Mult

    subroutine Matrix_Mult_SymmLeft(Mat, U, Out, a, b)
    real(dm), intent(in) :: Mat(:, :), U(:, :)
    real(dm) Out(:, :)
    real(dm), intent(in), optional :: a, b
    real(dm) mult, beta
    integer n, m

    call Matrix_start('Mult_SymmLeft')

    m = size(Mat, dim=1)
    n = size(U, dim=2)
    if (m /= size(U, dim=1) .or. m /= size(Mat, dim=2)) &
        call MpiStop('Matrix_Mult_SymmLeft: Size mismatch')
    if (present(a)) then
        mult = a
    else
        mult = ROne
    end if
    if (present(b)) then
        beta = b
    else
        beta = RZero
    end if
    if (matrix_method == Mat_F90) then
        if (beta /= RZero) then
            Out = a*matmul(Mat, U) + beta*Out
        else
            Out = matmul(Mat, U)
            if (mult /= COne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call SSYMM('L', 'U', m, n, mult, Mat, size(Mat, dim=1), U, size(U, dim=1), beta, Out, size(Out, dim=1))
#else
        call DSYMM('L', 'U', m, n, mult, Mat, size(Mat, dim=1), U, size(U, dim=1), beta, Out, size(Out, dim=1))
#endif
    end if

    call Matrix_end('Mult_SymmLeft')

    end subroutine Matrix_Mult_SymmLeft

    subroutine Matrix_Mult_SymmRight(Mat, U, Out, a, b)
    ! Out = a*Mat U + b*out
    real(dm), intent(in) :: Mat(:, :), U(:, :)
    real(dm) Out(:, :)
    real(dm), intent(in), optional :: a, b
    real(dm) mult, beta
    integer n, m

    call Matrix_start('Mult_SymmRight')

    m = size(Mat, dim=1)
    n = size(U, dim=2)
    if (n /= size(Mat, dim=2) .or. n /= size(U, dim=1)) &
        call MpiStop('Matrix_Mult_SymmRight: Size mismatch')
    if (present(a)) then
        mult = a
    else
        mult = ROne
    end if
    if (present(b)) then
        beta = b
    else
        beta = RZero
    end if
    if (matrix_method == Mat_F90) then
        if (beta /= RZero) then
            Out = a*matmul(Mat, U) + beta*Out
        else
            Out = matmul(Mat, U)
            if (mult /= ROne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call SSYMM('R', 'U', m, n, mult, U, size(U, dim=1), Mat, size(Mat, dim=1), beta, Out, size(Out, dim=1))
#else
        call DSYMM('R', 'U', m, n, mult, U, size(U, dim=1), Mat, size(Mat, dim=1), beta, Out, size(Out, dim=1))
#endif
    end if

    call Matrix_end('Mult_SymmRight')

    end subroutine Matrix_Mult_SymmRight

    subroutine Matrix_CMultGen(Mat, m, k, U, n, Out)
    ! out(1:m,1:n) = MatMul(Mat(1:m,1:k),U(1:k,1:n))
    integer, intent(in) :: m, k, n
    complex(dm), intent(in) :: Mat(:, :), U(:, :)
    complex(dm) Out(:, :)

    call Matrix_start('CMultGen')

    if (size(Out, dim=1) < m .or. size(Out, dim=2) < n) call MpiStop('Matrix_CMultGen: bad Out size')

    if (matrix_method == Mat_F90) then
        Out(1:m, 1:n) = matmul(Mat(1:m, 1:k), U(1:k, 1:n))
    else
#ifdef MATRIX_SINGLE
        call CGEMM('N', 'N', m, n, k, COne, Mat, size(Mat, dim=1), U, size(U, dim=1), CZero, Out, size(Out, dim=1))
#else
        call ZGEMM('N', 'N', m, n, k, COne, Mat, size(Mat, dim=1), U, size(U, dim=1), CZero, Out, size(Out, dim=1))
#endif
    end if
    call Matrix_end('CMultGen')

    end subroutine Matrix_CMultGen

    subroutine Matrix_MultGen(Mat, m, k, U, n, Out)
    ! out(1:m,1:n) = MatMul(Mat(1:m,1:k),U(1:k,1:n))
    integer, intent(in) :: m, k, n
    real(dm), intent(in) :: Mat(:, :), U(:, :)
    real(dm) Out(:, :)

    call Matrix_start('MultGen')

    if (size(Out, dim=1) < m .or. size(Out, dim=2) < n) call MpiStop('Matrix_MultGen: bad Out size')

    if (matrix_method == Mat_F90) then
        Out(1:m, 1:n) = matmul(Mat(1:m, 1:k), U(1:k, 1:n))
    else
#ifdef MATRIX_SINGLE
        call SGEMM('N', 'N', m, n, k, ROne, Mat, size(Mat, dim=1), U, size(U, dim=1), RZero, Out, size(Out, dim=1))
#else
        call DGEMM('N', 'N', m, n, k, ROne, Mat, size(Mat, dim=1), U, size(U, dim=1), RZero, Out, size(Out, dim=1))
#endif
    end if
    call Matrix_end('MultGen')

    end subroutine Matrix_MultGen

    subroutine Matrix_CMult_NT(Mat, U, Out, a, b)
    ! Out = a*Mat U^dag + b*out
    complex(dm), intent(in) :: Mat(:, :), U(:, :)
    complex(dm) Out(:, :)
    complex(dm), intent(in), optional :: a, b
    complex(dm) mult, beta
    integer m, n, k

    m = size(Mat, dim=1)
    n = size(U, dim=1)
    k = size(Mat, dim=2)
    if (k /= size(U, dim=2)) call MpiStop('Matrix_CMult_NT: Matrix size mismatch')
    call Matrix_start('CMult_NT')
    if (present(a)) then
        mult = a
    else
        mult = COne
    end if
    if (present(b)) then
        beta = b
    else
        beta = CZero
    end if

    if (matrix_method == Mat_F90) then
        if (beta /= CZero) then
            Out = beta*Out + mult*matmul(Mat, conjg(transpose(U)))
        else
            Out = matmul(Mat, conjg(transpose(U)))
            if (mult /= COne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call CGEMM('N', 'C', m, n, k, mult, Mat, m, U, n, beta, Out, size(Out, dim=1))
#else
        call ZGEMM('N', 'C', m, n, k, mult, Mat, m, U, n, beta, Out, size(Out, dim=1))
#endif
    end if
    call Matrix_end('CMult_NT')

    end subroutine Matrix_CMult_NT

    subroutine Matrix_Mult_NT(Mat, U, Out, a, b)
    ! Out = a*Mat U^T + b*out
    real(dm), intent(in) :: Mat(:, :), U(:, :)
    real(dm) Out(:, :)
    real(dm), intent(in), optional :: a, b
    real(dm) mult, beta
    integer m, n, k

    m = size(Mat, dim=1)
    n = size(U, dim=1)
    k = size(Mat, dim=2)
    if (k /= size(U, dim=2)) call MpiStop('Matrix_Mult_NT: Matrix size mismatch')
    call Matrix_start('Mult_NT')
    if (present(a)) then
        mult = a
    else
        mult = ROne
    end if
    if (present(b)) then
        beta = b
    else
        beta = RZero
    end if

    if (matrix_method == Mat_F90) then
        if (beta /= RZero) then
            Out = beta*Out + mult*matmul(Mat, transpose(U))
        else
            Out = matmul(Mat, transpose(U))
            if (mult /= ROne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call SGEMM('N', 'T', m, n, k, mult, Mat, m, U, n, beta, Out, size(Out, dim=1))
#else
        call DGEMM('N', 'T', m, n, k, mult, Mat, m, U, n, beta, Out, size(Out, dim=1))
#endif
    end if
    call Matrix_end('Mult_NT')

    end subroutine Matrix_Mult_NT

    subroutine Matrix_CMult_TN(Mat, U, Out, a, b)
    ! Out = a*Mat^dag U + b*Out
    complex(dm), intent(in) :: Mat(:, :), U(:, :)
    complex(dm) Out(:, :)
    complex(dm), intent(in), optional :: a, b
    complex(dm) mult, beta
    integer m, n, k

    m = size(Mat, dim=2)
    n = size(U, dim=2)
    k = size(Mat, dim=1)
    if (k /= size(U, dim=1)) call MpiStop('Matrix_CMult_TN: Matrix size mismatch')

    call Matrix_start('CMult_TN')
    if (present(a)) then
        mult = a
    else
        mult = COne
    end if
    if (present(b)) then
        beta = b
    else
        beta = CZero
    end if
    if (matrix_method == Mat_F90) then
        if (beta /= CZero) then
            Out = mult*matmul(conjg(transpose(Mat)), U) + beta*Out
        else
            Out = matmul(conjg(transpose(Mat)), U)
            if (mult /= COne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call CGEMM('C', 'N', m, n, k, mult, Mat, k, U, k, beta, Out, size(Out, dim=1))
#else
        call ZGEMM('C', 'N', m, n, k, mult, Mat, k, U, k, beta, Out, size(Out, dim=1))
#endif
    end if
    call Matrix_end('CMult_TN')

    end subroutine Matrix_CMult_TN

    subroutine Matrix_Mult_TN(Mat, U, Out, a, b)
    ! Out = a*Mat^dag U + b*Out
    real(dm), intent(in) :: Mat(:, :), U(:, :)
    real(dm) Out(:, :)
    real(dm), intent(in), optional :: a, b
    real(dm) mult, beta
    integer m, n, k

    m = size(Mat, dim=2)
    n = size(U, dim=2)
    k = size(Mat, dim=1)
    if (k /= size(U, dim=1)) call MpiStop('Matrix_Mult_TN: Matrix size mismatch')

    call Matrix_start('CMult_TN')
    if (present(a)) then
        mult = a
    else
        mult = ROne
    end if
    if (present(b)) then
        beta = b
    else
        beta = RZero
    end if
    if (matrix_method == Mat_F90) then
        if (beta /= CZero) then
            Out = mult*matmul(transpose(Mat), U) + beta*Out
        else
            Out = matmul(transpose(Mat), U)
            if (mult /= COne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call SGEMM('T', 'N', m, n, k, mult, Mat, k, U, k, beta, Out, size(Out, dim=1))
#else
        call DGEMM('T', 'N', m, n, k, mult, Mat, k, U, k, beta, Out, size(Out, dim=1))
#endif
    end if
    call Matrix_end('Mult_TN')

    end subroutine Matrix_Mult_TN

    subroutine Matrix_Cholesky(M, err, zeroed)
    ! Note upper triangular is not zeroed
    real(dm), intent(inout) :: M(:, :)
    integer n, info
    integer, optional :: err
    logical, intent(in), optional :: zeroed
    integer i

    n = size(M, dim=1)
    if (size(M, dim=2) /= n) call MpiStop('Matrix_Cholesky: non-square matrix')

#ifdef MATRIX_SINGLE
    call spotrf ('L', n, M, n, info)
#else
    call dpotrf ('L', n, M, n, info)
#endif

    if (present(err)) then
        err = info
    else
        if (info /= 0) &
            call MpiStop('Matrix_Cholesky: not positive definite ' // trim(IntToStr(info)))
    end if

    if (info == 0 .and. present(zeroed)) then
        do i = 1, n
            M(1:i - 1, i) = 0
        end do
    end if

    end subroutine Matrix_Cholesky

    subroutine Matrix_CCholesky(M)
    ! M = L L^\dag
    complex(dm), intent(inout) :: M(:, :)
    integer n, info

    n = size(M, dim=1)
    if (size(M, dim=2) /= n) call MpiStop('Matrix_CCholesky: non-square matrix')

#ifdef MATRIX_SINGLE
    call cpotrf ('L', n, M, n, info)
#else
    call zpotrf ('L', n, M, n, info)
#endif

    if (info /= 0) call MpiStop('Matrix_CCholesky: not positive definite ' // trim(IntToStr(info)))

    end subroutine Matrix_CCholesky

    subroutine Matrix_CholeskyRootInverse(M, transpose, error)
    ! M = L L^T and return L^{-1} in M  ( or [L^(-1}]^T )
    real(dm), intent(inout) :: M(:, :)
    integer n, info
    integer i, j
    logical, intent(in), optional :: transpose
    integer, intent(out), optional :: error
    logical trans

    call Matrix_Cholesky(M, info)
    if (info == 0) then
        n = size(M, dim=1)
#ifdef MATRIX_SINGLE
        call STRTRI('L', 'N', n, M, n, info)
#else
        call DTRTRI('L', 'N', n, M, n, info)
#endif
    end if
    if (present(error)) error = info
    if (info /= 0) then
        if (present(error)) return
        call MpiStop('Matrix_CholeskyRootInverse: not positive definite ' // trim(IntToStr(info)))
    end if

    if (present(transpose)) then
        trans = transpose
    else
        trans = .false.
    end if

    if (trans) then
        do i = 1, n
            do j = 1, i - 1
                M(j, i) = M(i, j)
                M(i, j) = 0
            end do
        end do
    else
        do i = 1, n
            do j = 1, i - 1
                M(j, i) = 0
            end do
        end do
    end if

    end subroutine Matrix_CholeskyRootInverse

    subroutine Matrix_CCholeskyRootInverse(M, dagger)
    ! M = L L^\dag and return L^{-1} in M  ( or [L^(-1}]^\dag )
    complex(dm), intent(inout) :: M(:, :)
    integer n, info
    integer i, j
    logical, intent(in), optional :: dagger
    logical trans

    call Matrix_CCholesky(M)
    n = size(M, dim=1)

#ifdef MATRIX_SINGLE
    call CTRTRI('L', 'N', n, M, n, info)
#else
    call ZTRTRI('L', 'N', n, M, n, info)
#endif

    if (info /= 0) call MpiStop('Matrix_CCholeskyRootInverse: not positive definite ' // trim(IntToStr(info)))

    if (present(dagger)) then
        trans = dagger
    else
        trans = .false.
    end if

    if (trans) then
        do i = 1, n
            do j = 1, i - 1
                M(j, i) = conjg(M(i, j))
                M(i, j) = 0
            end do
        end do
    else
        do i = 1, n
            do j = 1, i - 1
                M(j, i) = 0
            end do
        end do
    end if

    end subroutine Matrix_CCholeskyRootInverse

    subroutine Matrix_inverse_chol(M, err)
    ! Inverse of symmetric matrix
    ! This should not be used in real situations, but useful for quick testing
    real(dm), intent(inout) :: M(:, :)
    integer i, j, n
    integer info
    integer, optional :: err

    n = size(M, dim=1)
    if (size(M, dim=2) /= n) call MpiStop('Matrix_Inverse: non-square matrix')
    call Matrix_start('Inverse')
    if (present(err)) then
        call Matrix_Cholesky(M, err)
        if (err /= 0) return
    else
        call Matrix_Cholesky(M)
    end if
#ifdef MATRIX_SINGLE
    call spotri ('L', n, M, n, info)
#else
    call dpotri ('L', n, M, n, info)
#endif
    if (present(err)) then
        err = info
        if (err /= 0) return
    else
        if (info /= 0) call MpiStop('Matrix_inverse: error ' // trim(IntToStr(info)))
    end if
    do i = 1, n
        do j = 1, i - 1
            M(j, i) = M(i, j)
        end do
    end do
    call Matrix_end('Inverse')

    end subroutine Matrix_inverse_chol

    subroutine Matrix_Inverse(M)
    ! Inverse of symmetric positive definite matrix
    real(dm), intent(inout) :: M(:, :)
    integer i, n

    !     real(dm) w(Size(M,DIM=1))
    !     real(dm), dimension(:,:), allocatable :: tmp, tmp2
    !     real(dm), dimension(:), allocatable :: norm

    n = size(M, dim=1)
    do i = 1, size(M, dim=1)
        if (abs(M(i, i)) < 1d-30) call MpiStop('Matrix_Inverse: very small diagonal'  )
    end do

    call Matrix_inverse_chol(M)
    !
    !     allocate(tmp(Size(M,DIM=1),Size(M,DIM=1)))
    !
    !     n = Size(M,DIM=1)
    !     if (n<=1) return
    !     if (Size(M,DIM=2)/=n) call MpiStop('Matrix_Inverse: non-square matrix')
    !     call Matrix_Start('Inverse')
    !
    !
    !     allocate(norm(n))
    !     do i=1, n
    !        norm(i) = sqrt(abs(M(i,i)))
    !        if (norm(i) < 1d-30) &
    !         call MpiStop('Matrix_Inverse: very small diagonal'  )
    !        M(i,:) = M(i,:)/norm(i)
    !        M(:,i) = M(:,i)/norm(i)
    !     end do
    !
    !     call Matrix_Diagonalize(M,w,n)
    !     write (*,*), 'min/max eigenvalues = ', minval(w), maxval(w)
    !     if (any(w<=0)) then
    !          write (*,*), 'min/max eigenvalues = ', minval(w), maxval(w)
    !          call MpiStop('Matrix_Inverse: negative or zero eigenvalues')
    !     end if
    !     do i=1, n
    !        tmp(i,:) = M(:,i)/w(i)
    !     end do
    !     allocate(tmp2(Size(M,DIM=1),Size(M,DIM=1)))
    !     call Matrix_Mult(M,tmp,tmp2)
    !     M = tmp2
    !     do i=1, n
    !        M(i,:) = M(i,:)/norm(i)
    !        M(:,i) = M(:,i)/norm(i)
    !     end do
    !     deallocate(tmp, tmp2)
    !     deallocate(norm)
    !     call Matrix_End('Inverse')

    end subroutine Matrix_Inverse

    function Matrix_GaussianLogLike(Cov, d) result(LogLike)
    ! Returns -Log Likelihood for Gaussian: (d^T Cov^{-1} d + log|Cov|)/2
    ! ** Cov is destroyed by the function** [replaced by choleksy lower triangular]
    real(dm), intent(inout) :: Cov(:, :)
    real(dm), intent(in) :: d(:)
    real(dm), allocatable :: tmp(:)
    real(dm) :: LogLike
    integer info, i, n

    call Matrix_start('GaussianLogLike')
    n = size(Cov, dim=1)
    if (size(Cov, dim=2) /= n) call MpiStop('Matrix_GaussianLogLike: non-square matrix')
    if (size(d) /= n) call MpiStop('Matrix_GaussianLogLike: covariance and d different size')

    call Matrix_Cholesky(Cov)
    LogLike = 0
    ! Log Det term:
    do i = 1, n
        LogLike = LogLike + log(Cov(i, i))
    end do

    ! Solve for Cov^{-1}d [could use faster symmetric method]
    allocate(tmp(n))
    tmp = d
#ifdef MATRIX_SINGLE
    call SPOTRS('L', n, 1, Cov, n, tmp, n, info)
#else
    call DPOTRS('L', n, 1, Cov, n, tmp, n, info)
#endif
    if (info /= 0) call MpiStop('Matrix_GaussianLogLike: error in solving for cov^{-1}d')

    ! Add together
    LogLike = LogLike + dot_product(tmp, d)/2._dm
    deallocate(tmp)

    call Matrix_end('GaussianLogLike')

    end function Matrix_GaussianLogLike

    function Matrix_GaussianLogLikeDouble(Cov, d) result(LogLike)
    ! Returns -Log Likelihood for Gaussian: (d^T Cov^{-1} d + log|Cov|)/2
    ! ** Cov is destroyed by the function** [replaced by choleksy lower triangular]
    double precision, intent(inout) :: Cov(:, :)
    double precision, intent(in) :: d(:)
    double precision, allocatable :: tmp(:)
    double precision :: LogLike
    integer info, i, n

    call Matrix_start('GaussianLogLikeDouble')
    n = size(Cov, dim=1)
    if (size(Cov, dim=2) /= n) call MpiStop('Matrix_GaussianLogLikeDouble: non-square matrix')
    if (size(d) /= n) call MpiStop('Matrix_GaussianLogLikeDouble: covariance and d different size')

    call dpotrf ('L', n, Cov, n, info)
    if (info /= 0) call MpiStop('Matrix_GaussianLogLikeDouble: not positive definite ' // trim(IntToStr(info)))

    LogLike = 0
    ! Log Det term:
    do i = 1, n
        LogLike = LogLike + log(Cov(i, i))
    end do

    ! Solve for Cov^{-1}d [could use faster symmetric method]
    allocate(tmp(n))
    tmp = d
    call DPOTRS('L', n, 1, Cov, n, tmp, n, info)
    if (info /= 0) call MpiStop('Matrix_GaussianLogLikeDouble: error in solving for cov^{-1}d')

    ! Add together
    LogLike = LogLike + dot_product(tmp, d)/2._dm
    deallocate(tmp)

    call Matrix_end('GaussianLogLikeDouble')

    end function Matrix_GaussianLogLikeDouble

    subroutine Matrix_InverseAsymm(M)
    ! This should not be used in real situations, but useful for quick testing
    real(dm), intent(inout) :: M(:, :)
    real(dm) w(size(M, dim=1))
    real(dm), dimension(:, :), allocatable :: tmp, VT
    integer i, n

    n = size(M, dim=1)
    if (size(M, dim=2) /= n) call MpiStop('Matrix_InverseAsymm: non-square matrix')
    if (n == 0) return
    if (n == 1) then
        if (M(1, 1) == 0._dm) call MpiStop('Matrix_InverseAsymm: singular matrix')
        M(1, 1) = 1._dm/M(1, 1)
        return
    end if

    allocate(tmp(n, n), VT(n, n))

    call Matrix_SVD(M, n, n, w, VT)

    do i = 1, n
        tmp(i, :) = M(:, i)/w(i)
    end do

    call Matrix_Mult_TN(VT, tmp, M, 1._dm, 0._dm)
    ! M = matmul(transpose(VT),tmp)   //Changed for HPCF prob Sept 07

    deallocate(tmp, VT)

    end subroutine Matrix_InverseAsymm

    subroutine Matrix_SVD(Mat, m, n, D, VT)
    ! Do singular value decomposition of m x n matrix Mat
    ! Mat = U D V^T
    ! returns U in Mat, vector D of diagonal elements of, orthogonal matrix VT= V^T
    integer, intent(in) :: m, n
    real(dm), intent(inout) :: Mat(m, n)
    real(dm), intent(out) :: D(n), VT(n, n)

    integer WorkSize, ierr
    real(dm), allocatable, dimension(:) :: rv1

    WorkSize = 3*n**2

    allocate(rv1(WorkSize))
    call Matrix_start('SVD')
#ifdef MATRIX_SINGLE
    call SGESVD('O', 'A', m, n, Mat, m, D, Mat, m, VT, n, rv1, WorkSize, ierr)
#else
    call DGESVD('O', 'A', m, n, Mat, m, D, Mat, m, VT, n, rv1, WorkSize, ierr)
#endif
    if (ierr /= 0) call MpiStop('error in Matrix_SVD')
    call Matrix_end('SVD')

    deallocate(rv1)

    end subroutine Matrix_SVD

    subroutine Matrix_SVD_VT(Mat, m, n, D, U)
    ! Do singular value decomposition of m x n matrix Mat
    ! Mat = U D V^dag
    ! returns V^dag in Mat, vector D of diagonal elements of, unitary matrix U
    integer, intent(in) :: m, n
    real(dm), intent(inout) :: Mat(m, n)
    real(dm), intent(out), optional :: U(m, m)
    real(dm), intent(out) :: D(*)

    integer WorkSize, ierr
    integer, allocatable, dimension(:) :: IWork
    real(dm), allocatable, dimension(:) :: rv1
    real(dm) OptWk(1)

    if (n <= m) call MpiStop('Matrix_SVD_VT assumed n>m. ')

    call Matrix_start('SVD_VT')

    if (present(U) .and. matrix_method == Mat_DC) then
        ! Use divide and conquer
        allocate(IWork(8*min(m, n)))
        WorkSize = -1 ! 3*min(M,N)*min(M,N) +max(max(M,N),5*min(M,N)*min(M,N)+4*min(M,N))
#ifdef MATRIX_SINGLE
        call SGESDD('O', m, n, Mat, m, D, U, m, Mat, n, OptWk, WorkSize, IWork, ierr)
#else
        call DGESDD('O', m, n, Mat, m, D, U, m, Mat, n, OptWk, WorkSize, IWork, ierr)
#endif
        WorkSize = nint(OptWk(1))
        allocate(rv1(WorkSize))
#ifdef MATRIX_SINGLE
        call SGESDD('O', m, n, Mat, m, D, U, m, Mat, n, rv1, WorkSize, IWork, ierr)
#else
        call DGESDD('O', m, n, Mat, m, D, U, m, Mat, n, rv1, WorkSize, IWork, ierr)
#endif
        deallocate(IWork)
    else
        call MpiStop('Matrix_SVD_VT Not no-U non-DC case')
    end if

    if (ierr /= 0) call MpiStop('error in Matrix_SVD_VT')
    deallocate(rv1)

    call Matrix_end('SVD_VT')

    end subroutine Matrix_SVD_VT

    subroutine Matrix_CSVD_VT(Mat, m, n, D, U)
    ! Do singular value decomposition of m x n matrix Mat
    ! Mat = U D V^dag
    ! returns V^dag in Mat, vector D of diagonal elements of, unitary matrix U
    integer, intent(in) :: m, n
    complex(dm), intent(inout) :: Mat(m, n)
    complex(dm), intent(out), optional :: U(m, m)
    real(dm), intent(out) :: D(*)

    integer WorkSize, ierr
    integer, allocatable, dimension(:) :: IWork
    complex(dm), allocatable, dimension(:) :: rv1
    real(dm), allocatable, dimension(:) :: rwork

    if (n <= m) call MpiStop('Matrix_CSVD_VT assumed n>m. If equal use SVD_U.')

    call Matrix_start('CSVD_VT')

    if (present(U) .and. matrix_method == Mat_DC) then
        ! Use divide and conquer
        WorkSize = 2*min(m, n)*min(m, n) + 2*min(m, n) + max(m, n) + 5*n ! Add on 5N..
        allocate(rv1(WorkSize))
        allocate(rwork(5*min(m, n)*min(m, n) + 5*min(m, n)))
        allocate(IWork(8*min(m, n)))
#ifdef MATRIX_SINGLE
        call CGESDD('O', m, n, Mat, m, D, U, m, Mat, n, rv1, WorkSize, rwork, IWork, ierr)
#else
        call ZGESDD('O', m, n, Mat, m, D, U, m, Mat, n, rv1, WorkSize, rwork, IWork, ierr)
#endif
        deallocate(IWork)
    else
        allocate(rwork((max(3*min(m, n), 5*min(m, n) - 4))))
        WorkSize = 3*max(m, n)**2
        allocate(rv1(WorkSize), stat=ierr)
        if (ierr /= 0) then
            WorkSize = max(3*min(m, n) + max(m, n), 5*min(m, n))
            allocate(rv1(WorkSize))
        end if
#ifdef MATRIX_SINGLE
        if (present(U)) then
            call CGESVD('S', 'O', m, n, Mat, m, D, U, m, Mat, n, rv1, WorkSize, rwork, ierr)
        else
            call CGESVD('N', 'O', m, n, Mat, m, D, Mat, m, Mat, n, rv1, WorkSize, rwork, ierr)
        end if
#else
        if (present(U)) then
            call ZGESVD('S', 'O', m, n, Mat, m, D, U, m, Mat, n, rv1, WorkSize, rwork, ierr)
        else
            call ZGESVD('N', 'O', m, n, Mat, m, D, Mat, m, Mat, n, rv1, WorkSize, rwork, ierr)
        end if
#endif
    end if

    if (ierr /= 0) call MpiStop('error in Matrix_SVD_VT')
    deallocate(rv1)

    call Matrix_end('SVD_VT')

    end subroutine Matrix_CSVD_VT

    subroutine Matrix_CSVD_U(Mat, m, n, D, VT)
    ! Do singular value decomposition of m x n matrix Mat
    ! Mat = U D VT
    ! returns U in Mat, vector D of diagonal elements of, unitary matrix V
    integer, intent(in) :: m, n
    complex(dm), intent(inout) :: Mat(m, n)
    complex(dm), intent(out), optional :: VT(n, n)
    real(dm), intent(out) :: D(*)
    integer WorkSize, ierr
    integer, allocatable, dimension(:) :: IWork
    complex(dm), allocatable, dimension(:) :: rv1
    real(dm), allocatable, dimension(:) :: rwork

    call Matrix_start('CSVD_U')

    if (m < n) call MpiStop('Matrix_CSVD_U assumed m>=n')

    if (present(VT) .and. matrix_method == Mat_DC) then
        WorkSize = 2*min(m, n)*min(m, n) + 2*min(m, n) + max(m, n) + 5*n ! Add on 5N..
        allocate(rv1(WorkSize))
        allocate(rwork(5*min(m, n)*min(m, n) + 5*min(m, n)))
        allocate(IWork(8*min(m, n)))
#ifdef MATRIX_SINGLE
        call CGESDD('O', m, n, Mat, m, D, Mat, m, VT, n, rv1, WorkSize, rwork, IWork, ierr)
#else
        call ZGESDD('O', m, n, Mat, m, D, Mat, m, VT, n, rv1, WorkSize, rwork, IWork, ierr)
#endif
        deallocate(IWork)
    else
        allocate(rwork((max(3*min(m, n), 5*min(m, n) - 4))))

        WorkSize = 3*max(m, n)**2
        allocate(rv1(WorkSize), stat=ierr)
        if (ierr /= 0) then
            WorkSize = max(3*min(m, n) + max(m, n), 5*min(m, n))
            allocate(rv1(WorkSize))
        end if
#ifdef MATRIX_SINGLE
        if (present(VT)) then
            call CGESVD('O', 'S', m, n, Mat, m, D, Mat, m, VT, n, rv1, WorkSize, rwork, ierr)
        else
            call CGESVD('O', 'N', m, n, Mat, m, D, Mat, m, Mat, n, rv1, WorkSize, rwork, ierr)
        end if
#else
        if (present(VT)) then
            call ZGESVD('O', 'S', m, n, Mat, m, D, Mat, m, VT, n, rv1, WorkSize, rwork, ierr)
        else
            call ZGESVD('O', 'N', m, n, Mat, m, D, Mat, m, Mat, n, rv1, WorkSize, rwork, ierr)
        end if
#endif
    end if
    if (ierr /= 0) call MpiStop('error in Matrix_SVD_U')
    call Matrix_end('CSVD_U')

    deallocate(rv1, rwork)

    end subroutine Matrix_CSVD_U

    subroutine Matrix_CSVD_AllVT(Mat, m, n, D, VT)
    ! n>m
    ! Do singular value decomposition of m x n matrix Mat
    ! Mat = U D V^dag
    ! returns all nxn V^dag in VT, vector D of diagonal elements of
    integer, intent(in) :: m, n
    complex(dm), intent(inout) :: Mat(m, n)
    complex(dm), intent(out) :: VT(n, n)
    real(dm), intent(out) :: D(m)

    integer WorkSize, ierr
    complex(dm), allocatable, dimension(:) :: rv1
    complex(dm), allocatable, dimension(:, :) :: U
    integer, allocatable, dimension(:) :: IWork
    real(dm), allocatable, dimension(:) :: rwork

    call Matrix_start('CSVD_AllVT')

    if (matrix_method == Mat_DC) then
        ! Divide and conquer doesn't seem to provide outputs we want here
        WorkSize = 2*min(m, n)*min(m, n) + 2*min(m, n) + max(m, n) + 5*n ! Add on 5N..
        allocate(rv1(WorkSize))
        allocate(rwork(5*min(m, n)*min(m, n) + 5*min(m, n)))
        allocate(IWork(8*min(m, n)))
        allocate(U(m, m))
#ifdef MATRIX_SINGLE
        call CGESDD('A', m, n, Mat, m, D, U, m, VT, n, rv1, WorkSize, rwork, IWork, ierr)
#else
        call ZGESDD('A', m, n, Mat, m, D, U, m, VT, n, rv1, WorkSize, rwork, IWork, ierr)
#endif
        deallocate(U)
        deallocate(IWork)
    else
        WorkSize = 2*m*n + 2*max(n, m)
        allocate(rwork(5*max(m, n)))
        allocate(rv1(WorkSize), stat=ierr)
        if (ierr /= 0) then
            WorkSize = max(3*min(m, n) + max(m, n), 5*min(m, n))
            allocate(rv1(WorkSize))
        end if
#ifdef MATRIX_SINGLE
        call CGESVD('N', 'A', m, n, Mat, m, D, Mat, m, VT, n, rv1, WorkSize, rwork, ierr)
#else
        call ZGESVD('N', 'A', m, n, Mat, m, D, Mat, m, VT, n, rv1, WorkSize, rwork, ierr)
#endif
    end if

    if (ierr /= 0) call MpiStop('error in Matrix_SVD_AllVT')
    deallocate(rv1, rwork)

    call Matrix_end('CSVD_AllVT')

    end subroutine Matrix_CSVD_AllVT

    subroutine Matrix_DiagPreMul(D, M)
    ! M -> matmul(diag(D),M)
    real(dm), intent(inout) :: M(:, :)
    real(dm), intent(in) :: D(:)
    integer i

    if (size(D) /= size(M, dim=1)) call MpiStop('Matrix_DiagPreMul: Wrong size')
    do i = 1, size(D)
        M(i, :) = M(i, :)*D(i)
    end do

    end subroutine Matrix_DiagPreMul

    subroutine Matrix_SolveSymm(M, a, soln)
    real(dm), intent(out) :: soln(:)
    real(dm), intent(in) :: M(:, :), a(:)
    integer IPIV(size(a)), info
    real(dm), dimension(:, :), allocatable :: tmp
    real(dm), dimension(:), allocatable :: work
    integer n, WorkSize

    n = size(M, dim=1)
    if (size(M, dim=2) /= n) call MpiStop('Matrix_SolveSq: non-square matrix')
    if (n == 0) return
    if (n == 1) then
        if (M(1, 1) == 0._dm) call MpiStop('Matrix_SolveSymm: singular matrix')
        soln(1) = a(1)/M(1, 1)
        return
    end if
    call Matrix_start('SolveSymm')

    WorkSize = n**2
    allocate(work(WorkSize))
    allocate(tmp(n, n))
    tmp = M
#ifdef MATRIX_SINGLE
    call SSYTRF('U', n, tmp, n, IPIV, work, WorkSize, info)
#else
    call DSYTRF('U', n, tmp, n, IPIV, work, WorkSize, info)
#endif
    deallocate(work)
    if (info /= 0) call MpiStop('error in SolveSymm')
    soln(1:n) = a(1:n)
#ifdef MATRIX_SINGLE
    call SSYTRS('U', n, 1, tmp, n, IPIV, soln, n, info)
#else
    call DSYTRS('U', n, 1, tmp, n, IPIV, soln, n, info)
#endif
    if (info /= 0) call MpiStop('error (2) in SolveSymm')
    deallocate(tmp)

    call Matrix_end('SolveSymm')

    end subroutine Matrix_SolveSymm

    subroutine Matrix_SolveASymm(M, a, soln)
    real(dm), intent(out) :: soln(:)
    real(dm), intent(in) :: M(:, :), a(:)
    integer IPIV(size(a)), info
    real(dm), dimension(:, :), allocatable :: tmp
    integer n

    n = size(M, dim=1)
    if (size(M, dim=2) /= n) call MpiStop('Matrix_SolveSq: non-square matrix')
    if (n == 0) return
    if (n == 1) then
        if (M(1, 1) == 0._dm) call MpiStop('Matrix_SolveASymm: singular matrix')
        soln(1) = a(1)/M(1, 1)
        return
    end if

    call Matrix_start('SolveASymm')

    allocate(tmp(n, n))
    tmp = M
#ifdef MATRIX_SINGLE
    call SGETRF(n, n, tmp, n, IPIV, info)
#else
    call DGETRF(n, n, tmp, n, IPIV, info)
#endif
    if (info /= 0) call MpiStop('error in SolveASymm')
    soln(1:n) = a(1:n)
#ifdef MATRIX_SINGLE
    call SGETRS('N', n, 1, tmp, n, IPIV, soln, n, info)
#else
    call DGETRS('N', n, 1, tmp, n, IPIV, soln, n, info)
#endif
    if (info /= 0) call MpiStop('error (2) in SolveASymm')
    deallocate(tmp)

    call Matrix_end('SolveASymm')

    end subroutine Matrix_SolveASymm

    function Matrix_vecdot(vec1, vec2)
    real(dm) vec1(:), vec2(:)
    real(dm) Matrix_vecdot
    integer n
#ifdef MATRIX_SINGLE
    real(dm) sdot
    external sdot
#else
    real(dm) ddot
    external ddot
#endif
    n = size(vec1)
    if (n /= size(vec2)) call MpiStop('Matrix_vecdot: size mismatch')
#ifdef MATRIX_SINGLE
    Matrix_vecdot = sdot(n, vec1, 1, vec2, 1)
#else
    Matrix_vecdot = ddot(n, vec1, 1, vec2, 1)
#endif

    end function Matrix_vecdot

    function Matrix_QuadForm(Mat, vec)
    ! Get vec^T*Mat*vec where Mat is symmetric
    real(dm) Matrix_QuadForm
    real(dm) vec(:)
    real(dm) Mat(:, :)
    real(dm), dimension(:), allocatable :: out
    integer n

    n = size(vec)
    allocate(out(n))
    call Matrix_MulVecSymm(Mat, vec, out)
    Matrix_QuadForm = Matrix_vecdot(vec, out)
    deallocate(out)

    end function Matrix_QuadForm

    subroutine Matrix_MulVec(Mat, vec, Out, a, b)
    ! Out = a*Mat*vec + b*out
    real(dm), intent(in) :: Mat(:, :)
    real(dm) vec(:)
    real(dm) Out(:)
    real(dm), intent(in), optional :: a, b
    real(dm) mult, beta
    integer m, n

    call Matrix_start('MulVec')

    m = size(Mat, dim=1)
    n = size(vec)
    if (size(Mat, dim=2) /= n) call MpiStop('Matrix_MulVec: size mismatch')
    if (present(a)) then
        mult = a
    else
        mult = ROne
    end if
    if (present(b)) then
        beta = b
    else
        beta = RZero
    end if

    if (matrix_method == Mat_F90) then
        if (beta /= RZero) then
            Out = a*matmul(Mat, vec) + beta*Out
        else
            Out = matmul(Mat, vec)
            if (mult /= ROne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call SGEMV('N', m, n, mult, Mat, m, vec, 1, beta, Out, 1)
#else
        call DGEMV('N', m, n, mult, Mat, m, vec, 1, beta, Out, 1)
#endif
    end if
    call Matrix_end('MulVec')

    end subroutine Matrix_MulVec

    subroutine Matrix_MulVecSingle(Mat, vec, Out, a, b)
    ! Out = a*Mat*vec + b*out
    real, intent(in) :: Mat(:, :)
    real vec(:)
    real Out(:)
    real, intent(in), optional :: a, b
    real mult, beta
    integer m, n

    call Matrix_start('MulVecSingle')

    m = size(Mat, dim=1)
    n = size(vec)
    if (size(Mat, dim=2) /= n) call MpiStop('Matrix_MulVecSingle: size mismatch')
    if (present(a)) then
        mult = a
    else
        mult = SOne
    end if
    if (present(b)) then
        beta = b
    else
        beta = SZero
    end if

    if (matrix_method == Mat_F90) then
        if (beta /= SZero) then
            Out = a*matmul(Mat, vec) + beta*Out
        else
            Out = matmul(Mat, vec)
            if (mult /= SOne) Out = Out*mult
        end if
    else
        call SGEMV('N', m, n, mult, Mat, m, vec, 1, beta, Out, 1)
    end if
    call Matrix_end('MulVecSingle')

    end subroutine Matrix_MulVecSingle

    subroutine Matrix_MulVecSymm(Mat, vec, Out, a, b)
    ! Out = a*Mat*vec + b*out
    real(dm), intent(in) :: Mat(:, :)
    real(dm) vec(:)
    real(dm) Out(:)
    real(dm), intent(in), optional :: a, b
    real(dm) mult, beta
    integer m, n

    call Matrix_start('MulVecSymm')

    m = size(Mat, dim=1)
    n = size(vec)
    if (m /= n) call MpiStop('Matrix_MulVecSymm: size mismatch')
    if (present(a)) then
        mult = a
    else
        mult = ROne
    end if
    if (present(b)) then
        beta = b
    else
        beta = RZero
    end if

    if (matrix_method == Mat_F90) then
        if (beta /= RZero) then
            Out = a*matmul(Mat, vec) + beta*Out
        else
            Out = matmul(Mat, vec)
            if (mult /= ROne) Out = Out*mult
        end if
    else
#ifdef MATRIX_SINGLE
        call SSYMV('U', m, mult, Mat, m, vec, 1, beta, Out, 1)
#else
        call DSYMV('U', m, mult, Mat, m, vec, 1, beta, Out, 1)
#endif
    end if
    call Matrix_end('MulVecSymm')

    end subroutine Matrix_MulVecSymm

    subroutine Matrix_MulVecSymmSingle(Mat, vec, Out, a, b)
    ! Out = a*Mat*vec + b*out
    real, intent(in) :: Mat(:, :)
    real vec(:)
    real Out(:)
    real, intent(in), optional :: a, b
    real mult, beta
    integer m, n

    call Matrix_start('MulVecSymm')

    m = size(Mat, dim=1)
    n = size(vec)
    if (m /= n) call MpiStop('Matrix_MulVecSymm: size mismatch')
    if (present(a)) then
        mult = a
    else
        mult = SOne
    end if
    if (present(b)) then
        beta = b
    else
        beta = SZero
    end if

    if (matrix_method == Mat_F90) then
        if (beta /= RZero) then
            Out = a*matmul(Mat, vec) + beta*Out
        else
            Out = matmul(Mat, vec)
            if (mult /= ROne) Out = Out*mult
        end if
    else
        call SSYMV('U', m, mult, Mat, m, vec, 1, beta, Out, 1)
    end if
    call Matrix_end('MulVecSymmSingle')

    end subroutine Matrix_MulVecSymmSingle

    function Matrix_vecdotSingle(vec1, vec2)
    real vec1(:), vec2(:)
    real Matrix_vecdotSingle
    integer n
    real sdot
    external sdot

    n = size(vec1)
    if (n /= size(vec2)) call MpiStop('Matrix_vecdotSingle: size mismatch')
    Matrix_vecdotSingle = sdot(n, vec1, 1, vec2, 1)

    end function Matrix_vecdotSingle

    subroutine Matrix_InverseArrayMPI(Arr, nmat)
    ! Invert array of matrices by sending each to separate CPU
    integer, intent(in) :: nmat
#ifdef __GFORTRAN__
    type(TMatrixType), target :: Arr(:)
#else
    type(TMatrixType), target :: Arr(*)
#endif
    type(TMatrixType), pointer :: AM
    integer n
    integer i, MpiID, MpiSize
    integer sz
#ifdef MPI
    integer j, ierr, sid
    type(TMatrixType), target :: tmp
#endif

    call MpiStat(MpiID, MpiSize)
    if (MpiID == 0) then
        n = nmat
        sz = size(Arr(1)%M, dim=1)
    end if
    !    if (MpiID==0) then
    !     do i=1,nmat
    !      print *,'inverting',i
    !      call Matrix_inverse(Arr(i)%M)
    !     end do
    !    end if
    !    return
#ifdef MPI
    if (MpiID == 0) print *, 'MatrixInverseArray: starting'
    call MPI_BCAST(n, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, ierr)
    call MPI_BCAST(sz, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, ierr)
    if (MpiID /= 0) then
        allocate(tmp%M(sz, sz))
        AM => tmp
    end if
#endif

    do i = 1, n
        if (MpiID == 0) AM => Arr(i)
#ifdef MPI
        if (mod(i, MpiSize) /= MpiID) then
            ! Do nothing
            if (MpiID == 0) then
                j = mod(i, MpiSize)
                call MPI_SEND(AM%M, size(AM%M), MPI_DOUBLE_PRECISION, j, 1, MPI_COMM_WORLD, ierr)
            end if
        else
            if (MpiID /= 0) then
                ! Get from main thread
                call MPI_RECV(AM%M, size(AM%M), MPI_DOUBLE_PRECISION, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE, ierr)
            end if
#endif
            call Matrix_Inverse(AM%M)

#ifdef MPI
            if (MpiID == 0) then
                do j = max(1, i - MpiSize + 1), i - 1
                    sid = mod(j, MpiSize)
                    call MPI_RECV(Arr(j)%M, size(Arr(j)%M), MPI_DOUBLE_PRECISION, sid, 1, MPI_COMM_WORLD, &
                        MPI_STATUS_IGNORE, ierr)
                end do
            else
                call MPI_SEND(AM%M, size(AM%M), MPI_DOUBLE_PRECISION, 0, 1, MPI_COMM_WORLD, ierr)
            end if
        end if
#endif
    end do

#ifdef MPI
    if (MpiID == 0) then
        do j = n - mod(n, MpiSize) + 1, n
            sid = mod(j, MpiSize)
            call MPI_RECV(Arr(j)%M, size(Arr(j)%M), MPI_DOUBLE_PRECISION, sid, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE, &
                ierr)
        end do
    else
        deallocate(tmp%M)
    end if
#endif
    if (MpiID == 0) print *, 'MatrixInverseArray: Done'

    end subroutine Matrix_InverseArrayMPI

    end module MatrixUtils
