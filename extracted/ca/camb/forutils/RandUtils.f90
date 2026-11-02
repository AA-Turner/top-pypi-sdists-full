
    module RandUtils
    ! mostly legacy random functions used by CosmoMC
    use MpiUtils
    implicit none

    integer :: rand_inst = 0
    integer, parameter :: krand = kind(1.d0)
    integer :: Rand_Feedback = 1

    ! State for the RANMAR generator.
    double precision, private, save :: ramar_u(97), ramar_c, ramar_cd, ramar_cm
    integer, private, save :: ramar_i97, ramar_j97

    interface RandRotation
    module procedure RandRotationS, RandRotationD
    end interface

    contains

    ! subroutine init_random_seed()
    ! integer, allocatable :: seed(:)
    ! integer :: i, n, un, istat, dt(8), pid, t(2), s
    ! integer(8) :: count, tms
    !
    ! call random_seed(size = n)
    ! allocate(seed(n))
    !! First try if the OS provides a random number generator
    !! Fallback to XOR:ing the current time and pid. The PID is
    !! useful in case one launches multiple instances of the same
    !! program in parallel.
    ! call system_clock(count)
    ! if (count /= 0) then
    !    t = transfer(count, t)
    ! else
    !    call date_and_time(values=dt)
    !    tms = (dt(1) - 1970) * 365_8 * 24 * 60 * 60 * 1000 &
    !    + dt(2) * 31_8 * 24 * 60 * 60 * 1000 &
    !    + dt(3) * 24 * 60 * 60 * 60 * 1000 &
    !    + dt(5) * 60 * 60 * 1000 &
    !    + dt(6) * 60 * 1000 + dt(7) * 1000 &
    !    + dt(8)
    !    t = transfer(tms, t)
    ! end if
    ! s = ieor(t(1), t(2))
    ! pid = getpid() + 1099279 ! Add a prime
    ! s = ieor(s, pid)
    ! if (n >= 3) then
    !    seed(1) = t(1) + 36269
    !    seed(2) = t(2) + 72551
    !    seed(3) = pid
    !    if (n > 3) then
    !        seed(4:) = s + 37 * (/ (i, i=0, n - 4) /)
    !    end if
    ! else
    !    seed = s + 37 * (/ (i, i=0, n - 1 ) /)
    ! end if
    ! call random_seed(put=seed)
    ! end subroutine init_random_seed

    subroutine initRandom(i, i2)
    implicit none
    integer, intent(in), optional :: i
    integer, intent(in), optional :: i2
    integer seed_in, kl, ij
    character(len=10) :: fred
    real(krand) :: klr

    if (present(i)) then
        seed_in = i
    else
        seed_in = -1
    end if
    if (seed_in /= -1) then
        if (present(i2)) then
            kl = i2
            if (i2 > 30081) call MpiStop('initRandom:second seed too large')
        else
            kl = 9373
        end if
        ij = i
    else
        call system_clock(count=ij)
        ij = mod(ij + rand_inst*100, 31328)
        call date_and_time(time=fred)
        read(fred, '(e10.3)') klr
        kl = mod(int(klr*1000), 30081)
    end if

    if (Rand_Feedback > 0) write(*, '(" Random seeds:",1I6,",",1I6," rand_inst:",1I4)') ij, kl, rand_inst
    call RMARIN(ij, kl)

    end subroutine initRandom

    subroutine RandIndices(indices, nmax, n)
    integer, intent(in) :: nmax, n
    integer indices(n), i, ix
    integer tmp(nmax)

    if (n > nmax) call MpiStop('Error in RandIndices, n > nmax')
    do i = 1, nmax
        tmp(i) = i
    end do
    do i = 1, n
        ix = int(RANMAR()*(nmax + 1 - i)) + 1
        indices(i) = tmp(ix)
        tmp(ix) = tmp(nmax + 1 - i)
    end do

    end subroutine RandIndices

    subroutine RandRotationS(R, N)
    ! this is most certainly not the world's most efficient or robust random rotation generator
    integer, intent(in) :: N
    real R(N, N), vec(N), norm
    integer i, j

    do j = 1, N
        do
            do i = 1, N
                vec(i) = real(GAUSSIAN1())
            end do
            do i = 1, j - 1
                vec = vec - sum(vec*R(i, :))*R(i, :)
            end do
            norm = sum(vec**2)
            if (norm > 1e-3) exit
        end do
        R(j, :) = vec/sqrt(norm)
    end do

    end subroutine RandRotationS

    subroutine RandRotationD(R, N)
    ! this is most certainly not the world's most efficient or robust random rotation generator
    integer, intent(in) :: N
    double precision R(N, N), vec(N), norm
    integer i, j

    do j = 1, N
        do
            do i = 1, N
                vec(i) = GAUSSIAN1()
            end do
            do i = 1, j - 1
                vec = vec - sum(vec*R(i, :))*R(i, :)
            end do
            norm = sum(vec**2)
            if (norm > 1e-3) exit
        end do
        R(j, :) = vec/sqrt(norm)
    end do

    end subroutine RandRotationD

    double precision function GAUSSIAN1()
    implicit none
    double precision R, V1, V2, FAC
    integer, save :: iset = 0
    double precision, save :: gset

    ! Box muller
    if (iset == 0) then
        R = 2
        do while (R >= 1.d0)
            V1 = 2.d0*RANMAR() - 1.d0
            V2 = 2.d0*RANMAR() - 1.d0
            R = V1**2 + V2**2
        end do
        FAC = sqrt(-2.d0*log(R)/R)
        gset = V1*FAC
        GAUSSIAN1 = V2*FAC
        iset = 1
    else
        GAUSSIAN1 = gset
        iset = 0
    end if

    end function GAUSSIAN1

    double precision function CAUCHY1()
    implicit none

    CAUCHY1 = GAUSSIAN1()/max(1d-15, abs(GAUSSIAN1()))

    end function CAUCHY1

    real function RANDEXP1()
    !
    !     Random-number generator for the exponential distribution
    !     Algorithm EA from J. H. Ahrens and U. Dieter,
    !     Communications of the ACM, 31 (1988) 1330--1337.
    !     Coded by K. G. Hamilton, December 1996, with corrections.
    !
    real u, up, g, y

    real, parameter :: alog2 = 0.6931471805599453
    real, parameter :: a = 5.7133631526454228
    real, parameter :: b = 3.4142135623730950
    real, parameter :: c = -1.6734053240284925
    real, parameter :: p = 0.9802581434685472
    real, parameter :: aa = 5.6005707569738080
    real, parameter :: bb = 3.3468106480569850
    real, parameter :: hh = 0.0026106723602095
    real, parameter :: dd = 0.0857864376269050

    u = RANMAR()
    do while (u <= 0) ! Comment out this block
        u = RANMAR() ! if your RNG can never
    end do ! return exact zero
    g = c
    u = u + u
    do while (u < 1.0)
        g = g + alog2
        u = u + u
    end do
    u = u - 1.0
    if (u <= p) then
        RANDEXP1 = g + aa/(bb - u)
        return
    end if
    do
        u = RANMAR()
        y = a/(b - u)
        up = RANMAR()
        if ((up*hh + dd)*(b - u)**2 <= exp(-(y + c))) then
            RANDEXP1 = g + y
            return
        end if
    end do

    end function RANDEXP1

    subroutine RMARIN(ij, kl)
    ! This is the initialization routine for the random number generator RANMAR()
    ! NOTE: The seed variables can have values between:    0 <= IJ <= 31328
    !                                                      0 <= KL <= 30081
    ! The random number sequences created by these two seeds are of sufficient
    ! length to complete an entire calculation with. For example, if sveral
    ! different groups are working on different parts of the same calculation,
    ! each group could be assigned its own IJ seed. This would leave each group
    ! with 30000 choices for the second seed. That is to say, this random
    ! number generator can create 900 million different subsequences -- with
    ! each subsequence having a length of approximately 10^30.
    !
    ! Use IJ = 1802 & KL = 9373 to test the random number generator. The
    ! subroutine RANMAR should be used to generate 20000 random numbers.
    ! Then display the next six random numbers generated multiplied by 4096*4096
    ! If the random number generator is working properly, the random numbers
    !    should be:
    !           6533892.0  14220222.0  7275067.0
    !           6172232.0  8354498.0   10633180.0
    double precision S, T
    integer i, j, k, l, m
    integer ij, kl
    integer ii, jj

    if (ij < 0 .or. ij > 31328 .or. &
        kl < 0 .or. kl > 30081) then
        print '(A)', ' The first random number seed must have a value  between 0 and 31328'
        print '(A)', ' The second seed must have a value between 0 and   30081'
        call MpiStop('Error in RMARIN')
    end if
    i = mod(ij/177, 177) + 2
    j = mod(ij, 177) + 2
    k = mod(kl/169, 178) + 1
    l = mod(kl, 169)
    do ii = 1, 97
        S = 0.0
        T = 0.5
        do jj = 1, 24
            m = mod(mod(i*j, 179)*k, 179)
            i = j
            j = k
            k = m
            l = mod(53*l + 1, 169)
            if (mod(l*m, 64) >= 32) then
                S = S + T
            end if
            T = 0.5*T
        end do
        ramar_u(ii) = S
    end do
    ramar_c = 362436.0/16777216.0
    ramar_cd = 7654321.0/16777216.0
    ramar_cm = 16777213.0/16777216.0
    ramar_i97 = 97
    ramar_j97 = 33

    end subroutine RMARIN

    double precision function RANMAR()
    ! This is the random number generator proposed by George Marsaglia in
    ! Florida State University Report: FSU-SCRI-87-50
    ! It was slightly modified by F. James to produce an array of pseudorandom
    ! numbers.
    double precision uni

    ! INTEGER IVEC
    uni = ramar_u(ramar_i97) - ramar_u(ramar_j97)
    if (uni < 0.d0) uni = uni + 1.d0
    ramar_u(ramar_i97) = uni
    ramar_i97 = ramar_i97 - 1
    if (ramar_i97 == 0) ramar_i97 = 97
    ramar_j97 = ramar_j97 - 1
    if (ramar_j97 == 0) ramar_j97 = 97
    ramar_c = ramar_c - ramar_cd
    if (ramar_c < 0.d0) ramar_c = ramar_c + ramar_cm
    uni = uni - ramar_c
    if (uni < 0.d0) uni = uni + 1.d0
    RANMAR = uni

    end function RANMAR

    end module RandUtils
