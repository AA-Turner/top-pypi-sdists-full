module mod_doeels
  contains
subroutine doeels (e0, theta, phia, phib, wmin, wmax, dw,  &
              layers, neps, nper, name, name_size, thick, epsinf, nos, osc, osc_size,&
              contrl, mode, wn_array, debug, f_array, wn_array_size)

! ******************************************************************
! *                                                                *
! * compute the classical eels spectrum of an arbitrary plane-     *
! * statified medium made from isotropic materials in specular     *
! * geometry using the dielectric theory of eels.                  *
! *              
! * It is based on the work of Lambin'90 and modified for the use  *
! * within python                                                  *
! * (KMS and WFW, Martin-Luther-Universitaet Halle-Wittenberg)      *                                                        *
! ******************************************************************

  implicit none

  integer, parameter :: nt = 5
  
  double precision, intent(in) :: e0, theta, phia, phib, wmin, wmax, dw
  double precision, intent(in) :: thick(name_size), epsinf(name_size), osc(3, osc_size)
  character*10, intent(in) :: name(name_size)
  character*10, intent(in) :: contrl, mode
  integer, intent(in) :: name_size, osc_size, neps
  integer, intent(in) :: wn_array_size
  integer, intent(in) :: layers, nper, nos(name_size)
  double precision, intent(out) :: wn_array(wn_array_size), f_array(wn_array_size)
  logical, intent(in), optional :: debug

  logical :: ration, user
  integer :: i, iw, lstart, nofu, nout, nw, lmax, flag
  double precision :: a, acoef, aerr, alpha, argmin, argmax, b, bcoef, beta,  &
      c1, c2, ccoef, cospsi, dlimf, dx, elleps, ener, epsmac, facru, f, f0,   &
      f1, fpic, pi, prefac, psia, psii, rerr, ru, sinpsi, t,       &
      tanpsi, table, um, widt, wn, wpic, x, xmin, xmax, z, z1, z2
  double complex, dimension(30) :: eps
  dimension table(nt)
  logical debugFirstRun
  common /control/ debugFirstRun

  common / param / acoef, bcoef, ccoef, elleps, cospsi, sinpsi, tanpsi,  &
                   ru, um, dlimf, wn, user, ration
  common / mulayr / argmin, argmax, epsmac, flag

  !if (present(debug)) debug = .True.
  debugFirstRun = .True.

  data aerr / 0.0d0 /, rerr / 1.0d-06 /, f / 0.0d0 /, f1 / 0.0d0 /

! *** machine-dependent constants
! *** epsmac + 1.0 = epsmac , cosh(argmin) = 1.0 , tanh(argmax) = 1.0
  flag = 1

  if (debug) write(*,*) 'doeels:'
  if (debug) write(*,*) 'thick: ',    size(thick)
  if (debug) write(*,*) 'epsinf: ',   size(epsinf), epsinf
  if (debug) write(*,*) 'osc: ',      size(osc), size(osc, 1), size(osc, 2)
  if (debug) write(*,*) 'osc(1,1):',  osc(1,1)
  if (debug) write(*,*) 'nos: ',      size(nos)
  if (debug) write(*,*) 'wn_array: ', size(wn_array)
  if (debug) write(*,*) 'f_array: ',  size(f_array)

  pi = 4.0d0 * atan(1.0d0)
  epsmac = 1.0d0
1 epsmac = epsmac / 2.0d0
  if (1.0d0 + epsmac > 1.0d0) goto 1
  argmin = sqrt(2.0d0  * epsmac)
  argmax = 0.5d0 * log(2.0d0 / epsmac)

  dlimf = 0.0d0
  ration = .false.

! *** read target specifications

  user = layers == 0
  if (user) then

    if (layers == 1) ration = .true.
    lstart = layers - nper + 1
  endif

! *** initialize constants

  lmax = size(thick) 
  nw = size(wn_array)
  ! if (debug) write(*,*) 'lmax: ', lmax
  ! allocate(eps(lmax))
  ! if (debug) write(*,*) 'eps: ', size(eps)
  nout = 1 + nw / 20
  ener = 8.065d+03 * e0
  psia = phia / 180.0d0 * pi
  psii = theta / 180.0d0 * pi
  cospsi = cos(psii)
  sinpsi = sin(psii)
  tanpsi = tan(psii)
  prefac = sqrt(2.555d+05 / e0)/(1.37d+02 * cospsi)
  facru = psia / cospsi * sqrt(0.2624664d0 * e0)
  elleps = (1.0d0 - phia / phib) * (1.0d0 + phia / phib)
  acoef = sinpsi**2 + elleps * cospsi**2
  bcoef = sinpsi * cospsi
  if (dlimf > 0.0d0) then
    ration = .false.
    write(*,*) ' = > electron attracted by an image charge = ', dlimf
! ***    dlimf : half the length unit imposed by the image force
    dlimf = 1.80d0 * dlimf/(e0 * cospsi**2)
  endif
  ! if (debug) write(*,*) 'ration: ', ration
  if (.not. ration) goto 35

! *** set up coefficients for the rational approximation to the integral

  write(*,*) ' = > set up a rational approximation to the integral'
  call quanc8(fun, 0.0d0, pi / 2.0d0, aerr, rerr, alpha, c1, nofu, c2, eps, thick, layers, nper)
  alpha  = (2.0d0 / pi)**2 * alpha
  c1 = 2.0d0 / pi / sqrt(1.0d0 - elleps) * sinpsi * alpha**2
  if (c1 > 0.99d0) goto 30
  c2 = 3.0d0 * alpha**2 / (1.0d0 - c1)
  c1 = c1 * c2
  xmin = wmin / (2.0d0 * ener * psia)
  xmax = wmax / (2.0d0 * ener * psia)
  if (xmin <= 0.0d0) xmin = 0.0d0
  dx = max(0.02d0, (xmax - xmin) / nt)
  z1 = 0.0d0
  z2 = 0.0d0
  do i = 1, nt
    x = xmin + i * dx
    call queels(x, f, aerr, rerr, facru, eps, thick, layers, nper)
    table(i) = f
    f = f * (1.0d0 + alpha * x)**2
    if (abs(c2 * f - c1) < c2 * rerr) cycle
    z = (1.0d0 - f) / (c2 * f - c1)
    if (z <= 0.0d0) cycle
    z1 = z1 + x * z * (x**2 - z)
    z2 = z2 + (x * z)**2
  enddo
  if (z2 == 0.0d0) goto 30
  beta = z1 / z2
  z = 0.0d0
  do i = 1, nt
    x = xmin + i * dx
    z = z + (table(i) - qrat(x,alpha,beta,c1,c2))**2
  enddo
  z = sqrt(z) / nt
  if (z > 5.0d-03) goto 30
  write(*, 109) alpha, c1, c2, beta, z
  goto 35
30 write(*, *) ' ===> cannot do it'
  ration = .false.
  
! *** loop over the energy losses
  
35 if (debug) write(*, 110)
  do iw = 1, nw
    f0 = f1
    f1 = f
    f = 0.0d0
    wn = wmin + (iw - 1) * dw
!    if (debug) write(*,*) 'wn: ', wn
    if (wn < 0.0d0) goto 45
    if (wn == 0.0d0) goto 40
    if (.not. user) call seteps(nos, osc_size, osc, epsinf, wn, name_size, eps)
    !         subroutine seteps(nos, osc_size, osc, epsinf, wn, nLayer, eps)

    x = wn / (2.0d0 * ener * psia)
    if (ration) then
      f = qrat(x,alpha,beta,c1,c2) * aimag(-2.0 / (1.0 + eps(1)))
    else
      call queels(x, f, aerr, rerr, facru, eps, thick, layers, nper)
    endif
    f = prefac * f / wn
40  continue
    wn_array(iw) = wn
    f_array(iw)  = f
! ***    localize a peak using a parabolic interpolation
    if (iw < 3) goto 45
    if (f1 - f0 <= aerr) goto 45
    if (f1 - f <= aerr) goto 45
    a = (f1 - f0) + (f1 - f)
    if (a <= 4.0d0 * rerr * f1) goto 45
    b = 0.5d0 * (f1 - f0 + 3.0d0 * (f1 - f))
    t = b / a
    wpic = wn - t * dw
    fpic = f + 0.5d0 * b * t
    widt = sqrt(8.0d0 * fpic / a) * dw
    if (debug) write(*, 112) wpic, fpic, widt
45  if (mod(iw, nout) == 0) then
      if (debug) write(*, 113) 100.0 * iw / nw, wn, f
    endif
  enddo
  return
109 format(5x, 'alpha = ', f9.4, 4x, 'c1 = ', f9.4, 4x, 'c2 = ', f9.4, 4x,  &
      'beta = ', f9.4/5x, 'accuracy = ', e9.2)
110 format(//' run (%)  wn (cm**-1)  pcl(wn) (cm) |',  &
      ' peak location  amplitude    width')
112 format(40x, f10.2, d12.4, f10.2)
113 format(2x, f5.1, 3x, f11.3, d14.5)
end subroutine doeels
! ####################################################################

double precision function qrat(x, alpha, beta, c1, c2)
  double precision, intent(in) :: x, alpha, beta, c1, c2
  qrat = (1.0d0 + x * (beta + c1 * x)) / ((1.0d0 + x * (beta + c2 * x)) * (1.0d0 + alpha * x)**2)
  return
end function qrat
! ####################################################################

subroutine quanc8(fun, a, b, abserr, relerr, result, errest, nofun, flag, eps, d, layers, nper)

! estimate the integral of fun(x) from a to b
! to a user provided tolerance.
! an automatic adaptive routine based on
! the 8-panel newton-cotes rule (g. forsythe et al, 1977, p. 92)
!
! input ..
!
! fun     the name of the integrand function subprogram fun(x).
! a       the lower limit of integration.
! b       the upper limit of integration.(b may be less than a.)
! relerr  a relative error tolerance. (should be non-negative)
! abserr  an absolute error tolerance. (should be non-negative)
!
! output ..
!
! result  an approximation to the integral hopefully satisfying the
!         least stringent of the two error tolerances.
! errest  an estimate of the magnitude of the actual error.
! nofun   the number of function values used in calculation of result.
! flag    a reliability indicator.  if flag is zero, then result
!         probably satisfies the error tolerance.  if flag is
!         xxx.yyy , then  xxx = the number of intervals which have
!         not converged and 0.yyy = the fraction of the interval
!         left to do when the limit on  nofun  was approached.

  implicit none
  external fun
  double precision :: fun
  double precision, intent(in) :: a
  double precision, intent(in) :: b
  double precision, intent(in out) :: abserr
  double precision, intent(in) :: relerr
  double precision, intent(out) :: result
  double precision, intent(out) :: errest
  integer, intent(out) :: nofun
  double precision, intent(out) :: flag

  double precision, intent(in) :: d(:)
  double complex, intent(in) :: eps(:)
  integer, intent(in) :: layers, nper

  double precision :: w0, w1, w2, w3, w4, area, x0, f0, stone, step, cor11, temp
  double precision :: qprev, qnow, qdiff, qleft, esterr, tolerr
  double precision :: qright(31), f(16), x(16), fsave(8, 30), xsave(8, 30)
  double precision :: dabs, dmax1

  integer :: levmin, levmax, levout, nomax, nofin, lev, nim, i, j

! ***   stage 1 ***   general initialization
! set constants.

!  write (*,*) 'quanc8:'
!  write (*,*) 'd: ', size(d)
!  write (*,*) 'eps: ', size(eps)

  levmin = 1
  levmax = 30
  levout = 6
  nomax = 5000
  nofin = nomax - 8 * (levmax - levout + 2**(levout + 1))

! trouble when nofun reaches nofin

  w0 =   3956.0d0 / 14175.0d0
  w1 =  23552.0d0 / 14175.0d0
  w2 =  -3712.0d0 / 14175.0d0
  w3 =  41984.0d0 / 14175.0d0
  w4 = -18160.0d0 / 14175.0d0

! initialize running sums to zero.

  flag   = 0.0d0
  result = 0.0d0
  cor11  = 0.0d0
  errest = 0.0d0
  area   = 0.0d0
  nofun = 0
  if (a == b) return

! ***   stage 2 ***   initialization for first interval

  lev = 0
  nim = 1
  x0 = a
  x(16) = b
  qprev  = 0.0d0
  f0 = fun(x0, eps, d, layers, nper, size(eps))
  stone = (b - a) / 16.0d0
  x(8)  =  (x0    + x(16)) / 2.0d0
  x(4)  =  (x0    + x(8))  / 2.0d0
  x(12) =  (x(8)  + x(16)) / 2.0d0
  x(2)  =  (x0    + x(4))  / 2.0d0
  x(6)  =  (x(4)  + x(8))  / 2.0d0
  x(10) =  (x(8)  + x(12)) / 2.0d0
  x(14) =  (x(12) + x(16)) / 2.0d0
  do j = 2, 16, 2
    f(j) = fun(x(j), eps, d, layers, nper, size(eps))
  enddo
  nofun = 9

  do

! ***   stage 3 ***   central calculation
! requires qprev, x0, x2, x4, ..., x16, f0, f2, f4, ..., f16.
! calculates x1, x3, ...x15, f1, f3, ...f15, qleft, qright, qnow, qdiff, area.

    x(1) = (x0 + x(2)) / 2.0d0
    f(1) = fun(x(1), eps, d, layers, nper, size(eps))
    do j = 3, 15, 2
      x(j) = (x(j - 1) + x(j + 1)) / 2.0d0
      f(j) = fun(x(j), eps, d, layers, nper, size(eps))
    enddo
    nofun = nofun + 8
    step = (x(16) - x0) / 16.0d0
    qleft  =  (w0 * (f0 + f(8))  + w1 * (f(1) + f(7)) + w2 * (f(2) + f(6))  &
        + w3 * (f(3) + f(5))  +  w4 * f(4)) * step
    qright(lev + 1) = (w0 * (f(8) + f(16)) + w1 * (f(9) + f(15)) + w2 * (f(10) + f(14))  &
        + w3 * (f(11) + f(13)) + w4 * f(12)) * step
    qnow = qleft + qright(lev + 1)
    qdiff = qnow - qprev
    area = area + qdiff

! ***   stage 4 *** interval convergence test

    esterr = dabs(qdiff) / 1023.0d0
    tolerr = dmax1(abserr, relerr * dabs(area)) * (step / stone)
    
    if (lev >= levmin) then
      if (lev >= levmax) then
! current level is levmax.
        flag = flag + 1.0d0
      else
        if (nofun > nofin) then
! ***   stage 6   ***   trouble section
! number of function values is about to exceed limit.
          nofin = 2 * nofin
          levmax = levout
          flag = flag + (b - x0) / (b - a)
        else
          if (esterr > tolerr) then
! ***   stage 5   ***   no convergence
! locate next interval.
            nim = 2 * nim
            lev = lev + 1
! store right hand elements for future use.
            do i = 1, 8
              fsave(i, lev) = f(i + 8)
              xsave(i, lev) = x(i + 8)
            enddo
! assemble left hand elements for immediate use.
            qprev = qleft
            do i = 1, 8
              f(18 - 2 * i) = f(9 - i)
              x(18 - 2 * i) = x(9 - i)
            enddo
            cycle
          endif    
        endif
      endif

! ***   stage 7   ***   interval converged
! add contributions into running sums.
      result = result + qnow
      errest = errest + esterr
      cor11  = cor11  + qdiff / 1023.0d0
! locate next interval.
      do while (nim /= 2 * (nim / 2))
        nim = nim / 2
        lev = lev - 1
      enddo
      nim = nim + 1

      if (lev <= 0) exit

! assemble elements required for the next interval.
      qprev = qright(lev)
      x0 = x(16)
      f0 = f(16)
      do i = 1, 8
        f(2*i) = fsave(i, lev)
        x(2*i) = xsave(i, lev)
      enddo
      cycle
    else
! ***   stage 5   ***   no convergence
! locate next interval.
      nim = 2 * nim
      lev = lev + 1
! store right hand elements for future use.
      do i = 1, 8
        fsave(i, lev) = f(i + 8)
        xsave(i, lev) = x(i + 8)
      enddo
! assemble left hand elements for immediate use.
      qprev = qleft
      do i = 1, 8
        f(18 - 2 * i) = f(9 - i)
        x(18 - 2 * i) = x(9 - i)
      enddo
    endif
     
   enddo

 ! ***   stage 8   ***   finalize and return
  result = result + cor11

! make sure errest not less than roundoff level.
  if (errest /= 0.0d0) then
    temp = dabs(result) + errest
    do while (temp == dabs(result))
      errest = 2 * errest
      temp = dabs(result) + errest
    enddo
  endif
  return
end subroutine quanc8
! ############################################################################

double precision function fun(phi)

! ******************************************************************
! *                                                                *
! * integrand of the expression of the 1st order term in the       *
! * expansion of the eels integral for a homogeneous target.       *
! *                                                                *
! ******************************************************************

  implicit none
  
  double precision, intent(in out) :: phi

  logical :: user, ration
  double precision :: acoef, bcoef, ccoef, cospsi, dlimf, elleps, ru
  double precision :: sinphi, sinpsi, tanpsi, um, wn

  common / param / acoef, bcoef, ccoef, elleps, cospsi, sinpsi, tanpsi,  &
                   ru, um, dlimf, wn, user, ration

  sinphi = sin(phi)
  fun = sqrt((1.0d0 - elleps + elleps * sinphi**2) *   &
             (1.0d0 - sinpsi * sinphi) *               &
             (1.0d0 + sinpsi * sinphi))
  return
end function fun
! ##########################################################################

subroutine queels(x, f, aerr, rerr, facru, eps, d, layers, nper)

! ******************************************************************
! *                                                                *
! * perform q-space integration for computing the eels spectrum of *
! * a isotropic target using polar coordinates.                    *
! *                                                                *
! * x is the dimensionless energy loss hbar*omega/(2*e0*phia)      *
! * aerr and rerr are the desired absolute and relative accuracies *
! * facru*x is the units of wavevectors omega/v_perpendicular      *
! * f is the q-integral multiplied by (2/pi)**2                    *
! *                                                                *
! ******************************************************************

  implicit none
  
  double precision, intent(in) :: x
  double precision, intent(out) :: f
  double precision, intent(in out) :: aerr
  double precision, intent(in out) :: rerr
  double precision, intent(in) :: facru
  
  double precision, intent(in) :: d(:)
  double complex, intent(in) :: eps(:)
  integer, intent(in) :: layers, nper
   
  logical :: ration, user
  double precision :: acoef, bcoef, ccoef, cospsi, dlimf, elleps
  double precision :: error, flag, ru, sinpsi
  double precision :: u1, u2, um, ut, tanpsi, wn, y
  integer :: ie, nofu
  dimension error(3), flag(3)

  common / param / acoef, bcoef, ccoef, elleps, cospsi, sinpsi, tanpsi,  &
      ru, um, dlimf, wn, user, ration

!  write (*,*) 'queels:'
!  write (*,*) 'eps: ', size(eps)
!  write (*,*) 'd: ', size(d)

  f = 0.0d0
  if (x <= 0.0d0) then
    return
  endif
  ru = facru * x
  ccoef = cospsi**2 / x
  ut = ccoef - bcoef
  u1 = abs(ut)
  u2 = ccoef + bcoef
  if (ut > 0.0d0) then
    call quanc8(fint1, 0.0d0, u1, aerr, rerr, y, error(1), nofu, flag(1), eps, d, layers, nper)
    f = y
  else
    flag(1) = 0.0d0
  endif
  if (u2 > u1) then
    call quanc8(fint2, u1, u2, aerr, rerr, y, error(2), nofu, flag(2), eps, d, layers, nper)
    f = f + y
  else
    flag(2) = 0.0d0
  endif
  if (abs(acoef) > x * (1.0d0 - elleps) * bcoef) then
    um = sqrt(ccoef / x / (1.0d0 - elleps) + bcoef**2 / acoef)
    if (um > u2) then
      call quanc8(fint3, u2, um, aerr, rerr, y, error(3), nofu, flag(3), eps, d, layers, nper)
      f = f + y
    endif
    if (um < u1) then
      call quanc8(fint3, um, u1, aerr, rerr, y, error(3), nofu, flag(3), eps, d, layers, nper)
      f = f - y
    endif
  else
    flag(3) = 0.0d0
  endif
  do ie = 1, 3
    if (flag(ie) == 0.0d0) cycle
    write(*,*) ' +++ flag(', ie, ') =', flag(ie), ', error =', error(ie), ' +++'
    if (flag(ie) - aint(flag(ie)) > 0.5d-02) then
      stop '*** execution aborted ***'
    endif
  enddo
  f = (2.0d0 / 3.141592653589793238d0)**2 * f
  return
end subroutine queels
! ###########################################################################

double precision function fint1(u, eps, d, layers, nper, eps_size)

! ******************************************************************
! *                                                                *
! * integration over the azimutal angle from 0.0 to pi             *
! *                                                                *
! ******************************************************************

  implicit none
  
  double precision, intent(in) :: u

  double precision, intent(in) :: d(eps_size)
  double complex, intent(in) :: eps(eps_size)
  integer, intent(in) :: layers, nper, eps_size
   
  logical :: ration, user
  double precision :: acoef, bcoef, ccoef, cospsi, den, dif, dlimf, e, elleps
  double precision :: pi, rom, rop, ru, sinpsi, sum, um, t
  double precision :: tanpsi, wn

  common / param / acoef, bcoef, ccoef, elleps, cospsi, sinpsi, tanpsi,  &
      ru, um, dlimf, wn, user, ration

  data pi / 3.141592653589793238d0 /

!  write (*,*) 'fint1:'
!  write (*,*) 'd: ', size(d)
!  write (*,*) 'eps: ', size(eps)

  if (u == 0.0d0) then
    fint1 = 0.0d0
    return
  endif
  e = tanpsi * u
  rom = (1.0d0 - e)**2 + u**2
  rop = (1.0d0 + e)**2 + u**2
  sum = rop + rom
  rom = sqrt(rom)
  rop = sqrt(rop)
  dif = rop - rom
  den = sqrt((2.0d0 - dif) * (2.0d0 + dif)) * rop * rom
  fint1 = pi * u**2 * (4.0d0 * sum - dif**2 * (sum - rop * rom)) / den**3
  if (ration) then
    return
  endif
  if (user) then
    fint1 = fint1 * usurlo(ru * u, wn)
  else
    fint1 = fint1 * surlos(ru * u, eps, d, layers, nper)
    if (dlimf > 0.0d0) then
      t = ru * u * dlimf
      fint1 = fint1 * (1.d0 + t * log(t / (t + 0.26d0)))**2 / (1.d0 + 1.40d0 * t)
    endif
  endif
  return
end function fint1
! ###################################################

double precision function fint2(u, eps, d, layers, nper, eps_size)

! ******************************************************************
! *                                                                *
! * integration over the azimutal angle from 0.0 to phi < pi       *
! *                                                                *
! ******************************************************************

  implicit none
  
  double precision, intent(in) :: u

  double precision, intent(in) :: d(eps_size)
  double complex, intent(in) :: eps(eps_size)
  integer, intent(in) :: layers, nper, eps_size
   
  logical :: ration, user
  double precision :: a, arg, b, b2, c, ccoef, cospsi, dlimf, elleps, phi
  double precision :: ru, sinpsi, um, t, tanpsi, wn, x
 
  common / param / a, b, ccoef, elleps, cospsi, sinpsi, tanpsi, &
      ru, um, dlimf, wn, user, ration

!  write (*,*) 'fint2:'
!  write (*,*) 'd: ', size(d)
!  write (*,*) 'eps: ', size(eps)

  if (u == 0.0d0) then
    fint2 = 0.0d0
    return
  endif
  b2 = b**2
  c = (1.0d0 - elleps) * (cospsi * u)**2 + (b - ccoef) * (b + ccoef)
  if (abs(a * c) > 1.0d-03 * b2) then
    x = (b - sqrt(b2 - a * c)) / a
  else
    x = a * c / b2
    x = 0.5d0 * c * (1.d0 + 0.25d0 * x * (1.d0 + 0.5d0 * x * (1.d0 + 0.625d0 * x))) / b
  endif
  arg = x / u
  if (abs(arg) > 1.0d0) then
    arg = sign(1.0d0, arg)
  endif
  phi = acos(arg)
  fint2 = phint(phi, tanpsi, u)
  if (ration) then
    return
  endif
  if (user) then
    fint2 = fint2 * usurlo(ru * u, wn)
  else
    fint2 = fint2 * surlos(ru * u, eps, d, layers, nper)
    if (dlimf > 0.0d0) then
      t = ru * u * dlimf
      fint2 = fint2 * (1.d0 + t * log(t / (t + 0.26d0)))**2 / (1.d0 + 1.40d0 * t)
    endif
  endif
  return
end function fint2
! ########################################################################

double precision function fint3(u, eps, d, layers, nper, eps_size)

! ******************************************************************
! *                                                                *
! * integration over the azimutal angle from phi1 > 0 to phi2 < pi *
! *                                                                *
! ******************************************************************

  implicit none
  
  double precision, intent(in) :: u

  double precision, intent(in) :: d(eps_size)
  double complex, intent(in) :: eps(eps_size)
  integer, intent(in) :: layers, nper, eps_size
   
  logical :: ration, user
  double precision :: a, arg, b, ccoef, cospsi, dlimf, elleps, phi1, phi2
  double precision :: sinpsi, rac, ru, um, t, tanpsi, wn

  common / param / a, b, ccoef, elleps, cospsi, sinpsi, tanpsi,  &
      ru, um, dlimf, wn, user, ration


!  write (*,*) 'fint3:'
!  write (*,*) 'd: ', size(d)
!  write (*,*) 'eps: ', size(eps)

  if (u == 0.0d0) then
    fint3 = 0.0d0
    return
  endif
  rac = sign(1.0d0, a) * cospsi * sqrt((1.0d0 - elleps) * a * (um - u) * (um + u))
  arg = (b - rac) / (u * a)
  if (abs(arg) > 1.0d0) arg = sign(1.0d0, arg)
  phi2 = acos(arg)
  fint3 = phint(phi2, tanpsi, u)
  arg = (b + rac) / (u * a)
  if (abs(arg) > 1.0d0) arg = sign(1.0d0, arg)
  phi1 = acos(arg)
  fint3 = fint3 - phint(phi1, tanpsi, u)
  if (ration) return
  if (user) then
    fint3 = fint3 * usurlo(ru * u, wn)
  else
    fint3 = fint3 * surlos(ru * u, eps, d, layers, nper)
    if (dlimf > 0.0d0) then
      t = ru * u * dlimf
      fint3 = fint3 * (1.d0 + t * log(t / (t + 0.26d0)))**2 / (1.d0 + 1.40d0 * t)
    endif
  endif
  return
end function fint3
! ##########################################################################

double precision function usurlo(dq, wn)

! ******************************************************************
! *                                                                *
! * user-supplied dielectric surface loss function aimag(g(dq, wn)) *
! * input arguments :                                              *
! *    dq : modulus of the two-dimensional surface wave vector     *
! *         (angstroem**-1)                                        *
! *    wn : frequency (cm**-1)                                     *
! *                                                                *
! ******************************************************************

  implicit none
  
  double precision, intent(in) :: dq
  double precision, intent(in) :: wn

  if ((wn .GT. 0).AND.(dq.GT.0)) then
    write(*,*) 'hello, here is the user loss function'
  endif
  usurlo = 1.0d0
  return
end function usurlo
! #########################################################################

double precision function surlos(dk, eps, d, layers, nper)

! ******************************************************************
! *                                                                *
! * eels surface loss function for an arbitrary multilayered target*
! *                                                                *
! ******************************************************************

  implicit none
  
  double precision, intent(in) :: dk
  double complex, intent(in) :: eps(30)
  double precision, intent(in) :: d(:)
  integer, intent(in) :: layers, nper

  integer :: lmax, flag
  logical :: static, zero
  integer :: lstart, n
  double precision, allocatable :: arg(:)
  double precision :: argmin, argmax, cn, cnm1, epsmac, sn, snm1, t
  double complex :: a, b, csi, pnm2, pnm1, pn, pp, qnm2, qnm1, qn, qp, z

  common / mulayr / argmin, argmax, epsmac, flag

  zero(z) = (real(z) == 0.0) .and. (aimag(z) == 0.0)

!  write (*,*) 'surlos:'
!  write (*,*) 'd: ', size(d)
!  write (*,*) 'eps: ', size(eps)

  lmax = size(eps)
  allocate (arg(lmax))
  lstart = layers - nper + 1
  static = .true.
  n = 1
1 arg(n) = dk * d(n)
  if (arg(n) > argmax .or. zero(eps(n))) goto 10
  static = .not. (n >= lstart .and. arg(n) > argmin)
  n = n + 1
  if (n <= layers) goto 1

! *** periodic continued fraction, period = nper

  if (nper > 1) goto 2
  csi = eps(layers)
  goto 9
2 if (static) goto 5
  cn = cosh(arg(lstart))
  sn = sinh(arg(lstart))
  pnm1 = 1.0
  pn = cn
  pp = eps(lstart) * sn
  qnm1 = 0.0
  qn = sn / eps(lstart)
  qp = pn
  do  n = lstart + 1, layers
    cnm1 = cn
    snm1 = sn
    cn = cosh(arg(n))
    sn = sinh(arg(n))
    a = eps(n) * sn
    pp = cn * pp + a * pn
    qp = cn * qp + a * qn
    b = (eps(n - 1) / eps(n)) * (sn / snm1)
    a = cnm1 * b + cn
    pnm2 = pnm1
    pnm1 = pn
    qnm2 = qnm1
    qnm1 = qn
    pn = a * pnm1 - b * pnm2
    qn = a * qnm1 - b * qnm2
  enddo
  if (zero(qn)) goto 4
  a = 0.5 * (pn - qp) / qn
  b = sqrt(a**2 + pp / qn)
  pn = a - pn / qn
  if (abs(pn + b) > abs(pn - b)) then
    b = -b
  endif
  csi = a + b
  goto 9
4 a = qp - pn
  if (zero(a)) goto 12
  csi = pp / a
  goto 9

! *** small-dk limit of the periodic tail

5 pn = 0.0
  qn = 0.0
  do  n = lstart, layers
    pn = pn + d(n) * eps(n)
    qn = qn + d(n) / eps(n)
  enddo
  if (zero(qn)) goto 12
  csi = sqrt(pn / qn)
  if (aimag(csi) > 0.0) goto 9
  if ((aimag(csi) < 0.0) .or. (real(qn) < 0.0)) then
    csi = -csi
  endif 
9 n = lstart
  goto 11
10 csi = eps(n)

! *** backward algorithm

11 n = n - 1
  if (n <= 0) goto 15
  if (arg(n) == 0.0d0) goto 11
  t = tanh(arg(n))
  b = eps(n) + csi * t
  if (zero(b)) goto 13
  csi = eps(n) * (csi + t * eps(n)) / b
  goto 11
12 n = lstart
13 if (n <= 1) goto 14
  n = n - 1
  csi = eps(n) / tanh(arg(n))
  goto 11
14 surlos = 0.0d0
  return
15 a = csi + 1.0
  if (zero(a)) then
    surlos = 2.0d0 / epsmac
  else
    surlos = aimag(-2.0 / a)
  endif
  return
end function surlos
! #########################################################################

double precision function phint(phi, a, u)

! ******************************************************************
! *                                                                *
! * evaluate the integral from zero to phi of                      *
! *                                                                *
! *                 u                 2                            *
! *  ( ----------------------------- )  dphi                       *
! *                          2     2                               *
! *    (1 - a * u * cos(phi))  +  u                                *
! *                                                                *
! * for 0 <= phi <= pi , u >= 0 and a >= 0                         *
! *                                                                *
! ******************************************************************

  implicit none
  
  double precision, intent(in out) :: phi
  double precision, intent(in) :: a
  double precision, intent(in) :: u

  double precision :: ai, ar, bi, br, c, cpr, d, e, esr, pi, qr, ri, rm, root
  double precision :: rp, rr, s, spr, tm, tp, u2, x, zeta, zetai, zetar, zr

  pi = 3.141592653589793238d0
  c = cos(phi)
  s = sin(phi)
  u2 = u**2
  e = a*u
  if (u < 1.0d0 .and. e < 1.0d-02 * (1.0d0 + u2)) then
    zr = 1.0d0 + u2
    esr = e / zr
    phint = u2 / zr**2 * ((( (4.0d0 / 3.0d0) * (2.0d0 + c**2) * s * (5.0d0 - 3.0d0 * u2) *  &
            esr + (phi + c * s) * (5.0d0 - u2)) * esr + 4.0d0 * s) * esr + phi)
  else
    rm = sqrt((1.0d0 - e)**2 + u2)
    tm = 0.5d0 * atan2(u, 1.0d0 - e)
    rp = sqrt((1.0d0 + e)**2 + u2)
    tp = 0.5d0 * atan2(u, 1.0d0 + e)
    root = sqrt(rm * rp)
    cpr = cos(tm + tp)
    spr = sin(tm + tp)
    if (c >= 0.0d0) then
      x = s / (1.0d0 + c)
    elseif (abs(s) > 1.0d-07) then
      x = (1.0d0 - c) / s
    endif
    if ((c >= 0.0d0) .or. (abs(s) > 1.0d-07)) then
      zeta = sqrt(rm / rp)
      zetar = -zeta * sin(tm - tp)
      zetai =  zeta * cos(tm - tp)
      br = 0.5d0 * log(((zetar + x)**2 + zetai**2) / ((zetar - x)**2 + zetai**2))
      bi = atan2(zetai, zetar + x) - atan2(zetai, zetar - x)
      rr = -(br * spr - bi * cpr) / root
      ri = -(bi * spr + br * cpr) / root
      d = e * s / ((1.0d0 - e * c)**2 + u2)
      ar = d * (1.0d0 - e * c) - rr + u * ri
      ai = -d * u - ri - u * rr
    else
      rr = -pi / root * cpr
      ri =  pi / root * spr
      ar = -rr + u * ri
      ai = -ri - u * rr
    endif
    qr = (ar * (cpr - spr) * (cpr + spr) + 2.0d0 * ai * cpr * spr) / (rm * rp)
    phint = 0.5d0 * (ri / u - qr)
  endif
  return
end function phint
! ################################################################

subroutine seteps(nos, osc_size, osc, epsinf, wn, nLayer, eps)

  ! ******************************************************************
  ! * set up long-wavelength dielectric functions of the layers for  *
  ! * the present frequency wn (in cm**-1)                           *
  ! ******************************************************************
  
  ! implicit none
  integer, intent(in) :: nLayer
  integer, dimension(nLayer),intent(in) :: nos
  integer, intent(in) :: osc_size
  double precision, dimension(3,osc_size),intent(in) :: osc
  !f2py depend(osc_size) osc
  double precision, dimension(nLayer),intent(in) :: epsinf
  double precision,  intent(in) :: wn
  double complex, dimension(nLayer), intent(out) :: eps
  !f2py depend(nLayer) nos, epsinf, eps
  
  double complex :: nomi, deno, addeps
  double precision :: wn2, b
  integer :: flag
  logical debugFirstRun
  common /control/ debugFirstRun
   
  j = 0
  do l = 1, nLayer      ! loop over different thin film layers
    m = nos(l)/2      ! m number of TO modes = offset to reach the LO mode in the joint TO-LO list
    nomi = dcmplx(1.0d0, 0.0d0)
    deno = dcmplx(1.0d0, 0.0d0)
    addeps = dcmplx(0.0d0, 0.0d0)
    wn2 = wn**2
    do k = 1, m     ! loop over all TO modes
      j = j + 1

      if (osc(1,j) > 0.) then     ! positive TO mode: 'Kurosawa' form: _Multiplicative_ phonon mode
        b = wn/osc(1, j+m)
        nomi = nomi * osc(1, j+m)**2 * (1.0 - b * dcmplx(b, osc(3,j+m)/osc(1, j+m)) )
        deno =deno * (osc(1,j)**2 - wn * dcmplx( wn, osc(3,j) ) )
      
      else if (osc(1,j) < 0.) then! Negative TO mode means: _Additive_ Lorentz oscillator with Q
        addeps = addeps + osc(1,j)**2 * osc(2,j) /dcmplx(osc(1,j)**2 - wn2, -1*wn*osc(3,j))  ! Sign of imaginary part changed (WFW)
      
      else                      ! osc(1,j) = 0   -> it is a Drude term
        addeps = addeps - dcmplx(osc(1,j+m)**2, wn*(osc(3,j)-osc(3,j+m))) /dcmplx(wn2, wn*osc(3,j))
      end if

    enddo
    j = j+m     ! we have already looped over the LO modes, therefore increase the index
    eps(l) = epsinf(l) * (nomi / deno + addeps) ! brackets changed by HHe 230915
  enddo
  debugFirstRun = .false.
  return
end subroutine seteps

end module mod_doeels
