subroutine doboson3(t,width,gauss,asym,emin,emax,wmin,wmax,np,p,debug,xout,yout,nout) 

  ! *******************************************************************
  ! *                                                                 *
  ! * perform the quantum-mechanical complement to the classical step *
  ! * of the dielectric theory of eels in specular geometry using a   *
  ! * suitable thermodynamical average of the quantized surface       *
  ! * harmonic oscillators                                            *
  ! *                                                                 *
  ! *******************************************************************
  
    implicit none
      
    double precision, intent(in) :: t, width, gauss, asym, emin, emax, wmin
    double precision, intent(in out) :: wmax 
    integer, intent(in) :: np
    double precision, intent(in) :: p(np)
  
    integer, parameter :: mmax = 14, nmax = 2**mmax, nxout=3000
    double precision :: a, a1, a2, alfa, anorm, b, cp2, dwn, fac, fi 
    double precision :: fm, fm0, fm1, fp1, fmpic, fp, fp0, fppic, fr, g1, g2
    double precision :: h, pi, sigma, sp2, test, u
    double precision :: wmpic, wppic, wn, x, x1, x2, x3
    double precision :: func_o1, func_o2, respon 
    integer :: i, imax, imin, istep, j, jmin, jmax, m, n, n_save
    logical :: picm, picp
    logical, intent(in) :: debug
    double precision, allocatable :: p1(:), p2(:)
    double precision :: r1(nmax), r2(nmax)
    double precision, intent(out) :: xout(nxout), yout(nxout)
    integer, intent(out) :: nout
    !double precision, intent(out) :: xout(:), yout(:)
  
    ! debug = .False.
  
  ! remark : the two arrays r1 and r2 are used for fourier
  ! transforming the user-supplied instrumental response of the
  ! spectrometer that has to be coded in the external routine
  ! respon called when the input parameter gauss is < 0 or > 1.
  ! with 0 <= gauss <= 1, r1 and r2 are not used.
  
  ! *** rational approximations for ei(u) * exp(-u) + e1(u) * exp(+u)
  ! *** in the intervals (0, 1.3) and (1.3, infinity) <accuracy : 4.e-04>
  ! *** used for fourier transforming half-lorentzian functions
  
    data fm1 / 0.0 /, fp1 / 0.0 /
    pi = 4.0 * atan(1.0)
  
    dwn = (wmax - wmin) / (np - 1)
  
  ! *** redefine the frequency interval (0, wmax) to be used for the
  ! *** fourier transforms
  
    jmin = int(0.5 + wmin / dwn)
    if ((jmin - 0.5) * dwn < wmin) then
      jmin = jmin + 1
    endif
    fac = ((jmin - 0.5) * dwn - wmin) / dwn
    jmax = int(0.5 + wmax / dwn)
    test = max(1.5 * abs(emin), 1.5 * abs(emax), 6.0 * wmax)
    n_save = np
    n = 2
    do m = 2, mmax
      n = 2 * n
      wmax = n * dwn
      if (wmax >= test) goto 4
    enddo
    m = mmax
    n = nmax
    wmax = n * dwn
    if (debug) write(*,*) ' +++ n has been fixed at', nmax, ' = 2**', mmax, ' +++'
  4 if (debug) write(*,*) ' classical spectrum redefined from 0.0 to', wmax
    if (debug) write(*,*) ' step size =', dwn, ', ', n, ' (= 2**', m, ') points'
  
    allocate (p1(n))
    allocate (p2(n))
    
    do j = 1, n
      p1(j) = 0.0
    enddo
  ! this assignemnt might be saved by using p directly in the interpolation below.
    do j = 1, np
      p2(j) = p(j)
    enddo
  
  ! *** interpolate pcl on a suitable mesh in (0, wmax)
    i = 1
    do j = jmin, min(jmax, n)
      p1(j) = p2(i) + fac * (p2(i + 1) - p2(i))
      i = i + 1
    enddo
    do j = 1, n
      p2(j) = p1(j)
    enddo
  
  ! *** characteristic function f(tau)
  
    call sicot(p1, m, dwn, 1.39 * t)
    call sintr(p2, m, dwn)
    h = (pi + pi) / wmax
    if (gauss < 0 .or. gauss > 1.0) then
  
  ! *** broaden the spectrum by convoluting the characteristic function
  ! *** with a user-supplied response function (arbitrary normalization)
  
      if (debug) write(*,*) '==> switch to a user-supplied instrumental response'
      alfa = amax1(4.0 * dwn, width)
      if (alfa > width) then
        if (debug) write(*,*) ' +++ width has been enlarged to', alfa, ' +++'
      endif
      if (alfa < 10.0 * dwn) then
        if (debug) write(*,*) ' ... poor representation of the response function ...'
        if (debug) write(*,*) 'the step size (', dwn, ') should be reduced'
      endif
  ! make a table of the response function
      r1(1) = respon(0.0_8, alfa)
      r2(1) = r1(1)
      do i = 2, n
        x = (i - 1) * dwn
        r1(i) = respon( x, alfa)
        r2(i) = respon(-x, alfa)
      enddo
  ! fourier transform it
      call rcffi(r1, r2, -m, dwn)
  ! normalization of the response function, and convolution
      anorm = r1(1)
      do i = 1, n
        fac = exp(-p1(i)) / anorm
        cp2 = fac * cos(p2(i))
        sp2 = fac * sin(p2(i))
        p1(i) = r1(i) * cp2 + r2(i) * sp2
        p2(i) = r2(i) * cp2 - r1(i) * sp2
      enddo
      alfa = alfa / 2.0
  
    else
  
  ! *** broaden the spectrum by convoluting the characteristic function by
  ! *** a weighted sum of a lorentzian and a gaussian response functions
  
      alfa = max(1.5 * dwn, width)
      if (alfa > width) then
        if (debug) write(*,*) ' +++ width has been enlarged to', alfa, ' +++'
      endif
      if (alfa > 0.5 * wmax / pi) then
        stop '*** width is too large, nothing done ***'
      endif
      alfa = 0.5 * alfa
      sigma = alfa / 1.66511
      a1 = (1.0 - asym) / 2.0 * (1.0 - gauss)
      a2 = (1.0 + asym) / 2.0 * (1.0 - gauss)
      if (a1 < 0.0 .or. a2 < 0.0) then
        stop '*** invalid input : asym should be in (-1, +1) ***'
      endif
      g1 = (1.0 - asym) * alfa
      g2 = (1.0 + asym) * alfa
      p1(1) = 1.0
      p2(1) = 0.0
      do i = 2, n
        x = (i - 1) * h
        fr = 0.0
        fi = 0.0
        if (a1 /= 0.0) then
          x1 = g1 * x
          if (x1 <= 100.0) then
            fr = a1 * exp(-x1)
          endif
          if (a1 /= a2) then
            if (x1 <= 1.3) then
              fi = a1 * func_o1(x1)
            else
              fi = a1 * func_o2(x1)
            endif
          endif
        endif
        if (a2 /= 0.0) then
          x2 = g2 * x
          if (x2 <= 100.0) then
            fr = fr + a2 * exp(-x2)
          endif
          if (a2 /= a1) then
            if (x2 <= 1.3) then
              fi = fi - a2 * func_o1(x2)
            else
              fi = fi - a2 * func_o2(x2)
            endif
          endif
        endif
        if (gauss /= 0.0) then
          x3 = sigma * x
          if (x3 <= 10.0) then
            fr = fr + gauss * exp(-x3**2)
          endif
        endif
        fi = fi / pi
        fac = exp(-p1(i))
        cp2 = fac * cos(p2(i))
        sp2 = fac * sin(p2(i))
        p1(i) = fr * cp2 + fi * sp2
        p2(i) = fi * cp2 - fr * sp2
      enddo
      if (abs(fi) > 1.0e-03) then
        if (debug) write(*,*) ' ... poor representation of the response function ...'
        if (debug) write(*,*) 'the step size (', dwn, ') should be reduced'
      endif
    endif
  
  ! *** full eels spectrum
  
     call rcffi(p1, p2, m, h)
  
  ! *** output
    istep = max(int(alfa / dwn / 10.0), 1)
    nout = 0
    if (emin > 0.0) goto 18
    imin = n - int(abs(emin) / dwn)
    if ((imin - n) * dwn < emin) then
      imin = imin + 1
    endif
    do i = imin, n
      j = n - i
      if (mod(j, istep) > 0) cycle
      x = -j * dwn
      if (x > emax) goto 20
      nout = nout + 1
      xout(nout) = x
      yout(nout) = p2(j + 1)
    enddo
  18 continue 
    if (emax >= dwn) then
      imax = int(emax / dwn) + 1
      if ((imax - 1) * dwn > emax) then
        imax = imax - 1
      endif
      if (imax >= 2) then
        do i = 2, imax
          if (mod(i - 1, istep) > 0) cycle
          x = (i - 1) * dwn
          if (x < emin) cycle
          nout = nout + 1
          xout(nout) = x
          yout(nout) = p1(i)
        enddo
      endif
    endif
  20 close(unit = 14)
    if (debug) write(*,*) nout, ' values written on disk, step size =', istep * dwn
  
  ! *** analyze the spectrum
    if (.NOT. debug) return  
    if (debug) write(*,*) ' peak location    amplitude'
    wn = 0.0
    fm = p1(1)
    fp = p2(1)
    if (p2(2) < fp .and. p1(2) < fp) then
      if (debug) write(*, '(f13.2, e13.4)') wn, fp
    endif
    fac = 5.0e-06 * fp * dwn
    imax = 2 + int(amax1(abs(emin), abs(emax)) / dwn)
    do i = 2, imax
      fm0 = fm1
      fp0 = fp1
      fm1 = fm
      fp1 = fp
      fm = p2(i)
      fp = p1(i)
      if (i == 2) cycle
      picm = .false.
      picp = .false.
      wn = (i - 1) * dwn
      if ((fm1 >= fm0) .and. (fm1 >= fm)) then
        a = (fm1 - fm0) + (fm1 - fm)
        if (a >= fac) then
          b = 0.5 * ((fm1 - fm0) + 3.0 * (fm1 - fm))
          u = b / a
          wmpic = -wn + u * dwn
          fmpic = fm + 0.5 * b * u
          picm = .true.
        endif
      endif
      if ((fp1 >= fp0) .and. (fp1 >= fp)) then
        a = (fp1 - fp0) + (fp1 - fp)
        if (a >= fac) then
          b = 0.5 * ((fp1 - fp0) + 3.0 * (fp1 - fp))
          u = b / a
          wppic = wn - u * dwn
          fppic = fp + 0.5 * b * u
          picp = .true.
          if (picp) then
            if (picm) then
              if (debug) write(*, '(2(f13.2, e13.4, 5x))') wppic, fppic, wmpic, fmpic
            else
              if (debug) write(*, '(f13.2, e13.4)') wppic, fppic
            endif
          endif
        endif
      endif
      if (picm .and. (.not. picp)) then
        if (debug) write(*, '(33x, f13.2, e13.4)') wmpic, fmpic
      endif
    enddo
    return
  end subroutine doboson3
  ! ##################################################################
  double precision function func_o1(u) 
    implicit none  
    double precision :: u
    func_o1 = -sinh(u) * log(u**2) + u * ((0.03114 * u**2 + 0.41666) * u**2 + 0.84557)
    return
  end function func_o1
  
  double precision function func_o2(u) 
    implicit none 
    double precision :: u
    func_o2 = (((202.91 / u**2 + 932.21) / u**2 + 41.740) / u**2 + 2.0) /  &
            (((540.88 / u**2 + 345.67) / u**2 + 18.961) / u**2 + 1.0) / u
    return
  end function func_o2
  
  
    subroutine sintr(f, msign, h)
  
  ! *******************************************************************
  ! *                                                                 *
  ! * integral sine transform of a real function f(x)                 *
  ! *                                                                 *
  ! * g(y) = integral from zero to infinity of f(x)*sin(x*y) dx       *
  ! * if msign >= 0 or                                                *
  ! * g(y) = y * integral from zero to infinity of f(x)*sin(x*y) dx   *
  ! * if msign < 0                                                    *
  ! *                                                                 *
  ! * f(x) is tabulated on the mesh of points xj = (j-1/2)*h ,        *
  ! * j = 1, 2, ..., n ,  with n = 2**iabs(msig)                      *
  ! * g(y) is computed on the mesh of points yk = k*2pi/(n*h) ,       *
  ! * k = 0, 1, 2, ..., n-1                                           *
  ! *                                                                 *
  ! * input ...                                                       *
  ! * f(j) contains the value of f(xj) , j = 1, 2, ..., n             *
  ! * msign is such that n = 2**iabs(msign)                           *
  ! * h is the step size (must be positive)                           *
  ! *                                                                 *
  ! * output ...                                                      *
  ! * f(k+1) contains g(yk), k = 0, 1, ..., n-1                       *
  ! *                                                                 *
  ! * computing remarks ...                                           *
  ! * f is a real array with dimension n or more                      *
  ! * it is supposed that f(x) is zero for x > n*h                    *
  ! *                                                                 *
  ! *******************************************************************
  
    implicit none
    
    double precision, intent(in out) :: f(*)
    integer, intent(in) :: msign
    double precision, intent(in) :: h
    
    double precision :: a, c, ca, d, e, fnp1, s, sa, ti, ti1, ti2, tr, tr1, tr2
    double precision :: ui, ur, wi, wr
    integer :: i, i2, ip2, j, j2, k, l, le, le1, m2, n, n2, nm1, nv2
  
    if (h <= 0.0) then
      write(*,*) ' *** incorrect step size in <sintr>, h: ', h, ' ***'
      stop
    endif
  
    if (msign == 0) then
      f(1) = 0.0
      return
    endif
  
  ! *** for j and k = 0, 1, 2 ... n/2-1, compute
  ! s1 = sum ( f(2*j+1)*cos(4*pi*k*j/n) - f(2*j+2)*sin(4*pi*k*j/n) )
  ! s2 = sum ( f(2*j+1)*sin(4*pi*k*j/n) + f(2*j+2)*cos(4*pi*k*j/n) )
  ! store s1 in f(2*k+1) and s2 in f(2*k+2)
  ! (adapted from cfft routine, cern library member d704)
  
    m2 = iabs(msign) - 1
    n = 2**m2
    if (n /= 1) then
      nv2 = n / 2
      nm1 = n - 1
      j = 1
      do i = 1, nm1
        if (i < j) then
          i2 = i + i
          j2 = j + j
          ti = f(j2)
          f(j2) = f(i2)
          f(i2) = ti
          i2 = i2 - 1
          j2 = j2 - 1
          tr = f(j2)
          f(j2) = f(i2)
          f(i2) = tr
        endif
        k = nv2
        do while (j > k) 
          j = j - k
          k = k / 2
        enddo
        j = j + k
      enddo
      do i = 1, n, 2
        i2 = i + i
        ti = f(i2 + 2)
        f(i2 + 2) = f(i2) - ti
        f(i2) = f(i2) + ti
        i2 = i2 - 1
        tr = f(i2 + 2)
        f(i2 + 2) = f(i2) - tr
        f(i2) = f(i2) + tr
      enddo
      if (m2 /= 1) then
        c = 0.0
        s = 1.0
        le = 2
        do l = 2, m2
          wr = c
          wi = s
          ur = wr
          ui = wi
          c = sqrt(c * 0.5 + 0.5)
          s = s / (c + c)
          le1 = le
          le = le1 + le1
          do i = 1, n, le
            i2 = i + i
            ip2 = i2 + le
            ti = f(ip2)
            f(ip2) = f(i2) - ti
            f(i2) = f(i2) + ti
            i2 = i2 - 1
            ip2 = ip2 - 1
            tr = f(ip2)
            f(ip2) = f(i2) - tr
            f(i2) = f(i2) + tr
          enddo
          do j = 2, le1
            do i = j, n, le
              i2 = i + i
              ip2 = i2 + le
              tr = f(ip2 - 1) * ur - f(ip2) * ui
              ti = f(ip2) * ur + f(ip2 - 1) * ui
              f(ip2) = f(i2) - ti
              f(i2) = f(i2) + ti
              i2 = i2 - 1
              ip2 = ip2 - 1
              f(ip2) = f(i2) - tr
              f(i2) = f(i2) + tr
            enddo
            tr = ur * wr - ui * wi
            ui = ui * wr + ur * wi
            ur = tr
          enddo
        enddo
      endif
    endif
  
  ! *** for j and k = 0, 1 ... n-1, transform the array f so obtained into
  ! sum f(j+1)*cos(2*pi*k*j/n) and sum f(j+1)*sin(2*pi*k*j/n)
  ! and multiply the results by (1 - cos(2*pi*k/n)) and sin(2*pi*k/n)
  
    fnp1 = 4.0 * (f(1) - f(2))
    a = 3.1415926 / n
    n2 = n + 1
    n = 2 * n
    if (n2 /= 2) then
      c = 1.0
      s = 0.0
      ca = cos(a)
      sa = sin(a)
      k = n + 1
      do j = 3, n2, 2
        k = k - 2
        d = c
        c = d * ca - s * sa
        s = d * sa + s * ca
        tr1 = f(j) + f(k)
        ti1 = f(j + 1) - f(k + 1)
        d = f(j) - f(k)
        e = f(j + 1) + f(k + 1)
        tr2 = d * s + e * c
        ti2 = e * s - d * c
        f(j) = (1.0 - c) * (tr1 + tr2)
        f(j + 1) = s * (ti1 + ti2)
        f(k) = (1.0 + c) * (tr1 - tr2)
        f(k + 1) = s * (ti2 - ti1)
      enddo
      n2 = n2 - 1
      do j = 2, n2
        j2 = j + j
        f(j) = f(j2 - 1) + f(j2)
      enddo
      do j = 2, n2
        f(n + 2 - j) = f(j)
      enddo
      n2 = n2 + 1
    endif 
    f(n2) = fnp1
    if (msign >= 0) then
  
  ! *** normalization
  
      c = 0.0
      a = (a + a) / h
      do j = 2, n
        c = c + a
        f(j) = f(j) / c
      enddo
    endif
    f(1) = 0.0
    return
  end subroutine sintr
  ! #############################################################
  
  subroutine sicot(f, m, h, x0)
  
  ! *******************************************************************
  ! *                                                                 *
  ! * integral transform g(y, x0) of a real function f(x) defined by  *
  ! *                                                                 *
  ! * g(x0, y) = integral of f(x)/tanh(x/x0)*(1-cos(x*y)) dx          *
  ! *                                                                 *
  ! * f(x) is tabulated on the mesh of points xj = (j-1/2)*h ,        *
  ! * j = 1, 2, ..., n ,  with n = 2**m                               *
  ! * g(x0, y) is computed on the mesh of points yk = k*2pi/(n*h) ,   *
  ! * k = 0, 1, 2, ..., n-1                                           *
  ! *                                                                 *
  ! * input ...                                                       *
  ! * f(j) contains the value of f(xj) , j = 1, 2, ..., n             *
  ! * m is such that n = 2**iabs(m)                                   *
  ! * h is the step size (must be positive)                           *
  ! *                                                                 *
  ! * output ...                                                      *
  ! * f(k+1) contains g(x0, yk), k = 0, 1, ..., n-1                   *
  ! *                                                                 *
  ! * computing remarks ...                                           *
  ! * f is a real array with dimension n or more                      *
  ! * it is supposed that f(x) is zero for x > n*h                    *
  ! * external reference : sintr (sine transform of a real function). *
  ! *                                                                 *
  ! *******************************************************************
   
    implicit none
    
    double precision, intent(in out) :: f(*)
    integer, intent(in) :: m
    double precision, intent(in) :: h
    double precision, intent(in) :: x0
    
    double precision :: a, b, c, d, e, s, sa
    integer :: i, j, msign, n
  
    if (m == 0) then
      f(1) = 0.0d0
      return
    endif
  
    if (h <= 0.0) then
      write(*,*) ' *** incorrect step size in <sicot>, h =', h, ' ***'
      stop
    endif
  
    if (x0 < 0.0) then
      write(*,*) ' *** incorrect input in <sicot>, x0 =', x0, ' ***'
      stop
    endif
  
    n = 2**iabs(m)
  
  ! *** evaluate the integral from xj to infinity of f(x)/tanh(x/x0) dx
  ! and store the result in f(j)
  
    c = 0.0
    if (x0 > h / 16.0) then
      c = exp(-h / x0)
    endif
    s = 1.0 - c
    e = c**2
    a = 0.25 * h
    b = 0.25 * x0
    do i = 1, n
      if (i < n) then
        f(i) = f(i) + f(i+1)
      endif
      d = a
      if (s /= 1.0) then
        sa = s
        c = c * e
        s = 1.0 - c
        d = d + b * log(s / sa)
      endif
      f(i) = f(i) * d
    enddo
  
    j = n
    do i = 2, n
      j = j - 1
      f(j) = f(j) + f(j + 1)
    enddo
  ! alternative, but not yet tested:
  !  do j = n - 1, 1, -1
  !    f(j) = f(j) + f(j + 1)
  !  enddo
    msign = -iabs(m)
    call sintr(f, msign, h)
    return
  end subroutine sicot
  ! #############################################################
  
  double precision function respon(w, width)
  
  !*******************************************************************
  !                                                                  *
  ! instrumental response of the spectrometer for the frequency w    *
  ! width is the full width at half maximum of the response function *
  !                                                                  *
  !*******************************************************************
  
    implicit none
    double precision, intent(in) :: w, width
  
    double precision :: a, u
  
    a = 0.8 * width
    u = w / a
    if (u <= -1.0 .or. u >= 2.0) then
       respon = 0.0
    elseif (u > 1.0) then
       respon = 4.0 + 2.0 * sqrt((u - 1.0)**3) - 3.0 * u
    elseif (u > 0.0) then
       respon = 2.0 - 4.0 * sqrt(u**3) + 3.0 * u
    else
       respon = 2.0 * sqrt((u + 1.0)**3)
    endif
    return
  end function respon
  ! ####################################################################
  
  subroutine rcffi(ar, ai, msign, h)
  
  !   ******************************************************************* 
  !   *                                                                 * 
  !   * using a radix-two fast-fourier-transform technique, rcffi       * 
  !   * computes the fourier integral transform of a real function      * 
  !   * f(x) or the inverse fourier transform of a complex function     * 
  !   * such that g(-y) = conj(g(y)).                                   * 
  !   * (adapted from cfft routine, cern library member d704)           * 
  !   *                                                                 * 
  !   * g(y) = integral f(x) * cexp(-i * x * y) dx    (msign < 0)       * 
  !   *                                                                 * 
  !   * f(x) = 1 / (2 * pi) integral g(y) * cexp(+i * y * x) dy  (msign > 0)    * 
  !   *                                                                 * 
  !   * f(x) is tabulated on the meshes of points defined by            * 
  !   * xj = j * hx and -xj = -j * hx,  j = 0, +1, ..., n-2, n-1        * 
  !   * ar(j+1) contains f(+xj) and ai(j+1) contains f(-xj)             * 
  !   * (input when msign < 0 , output when msign >0)                   * 
  !   * ar(1) may be different from ai(1)                               * 
  !   *                                                                 * 
  !   * g(y) is tabulated on the mesh of points defined by              * 
  !   * yk = k * hy  , k = 0, 1, ..., n - 2, n - 1                      * 
  !   * ar(j+1) contains real(g(yk)) and ai(j+1) contains aimag(g(yk))  * 
  !   * (output when msign > 0 , input when msign < 0)                  * 
  !   * remark :  g(-yk) = conj(g(+yk))                                 * 
  !   *                                                                 * 
  !   * n = 2**iabs(msign)  (msign is an input)                         * 
  !   *                                                                 * 
  !   * the step sizes satisfy                                          * 
  !   * hy = (2 * pi) / (n * hx)   or    hx = (2 * pi) / (n * hy)       * 
  !   * h is an input (h = hx if msign < 0 , h = hy if msign > 0)       * 
  !   * h must be positive                                              * 
  !   *                                                                 * 
  !   * ar and ai are two real arrays with dimension n (input and       * 
  !   * output)                                                         * 
  !   *                                                                 * 
  !   ******************************************************************* 
  
    implicit none
  
    double precision, intent(in out) :: ar(*)
    double precision, intent(in out) :: ai(*)
    integer, intent(in)  :: msign
    double precision, intent(in) :: h
    
    double precision :: a, as, c, s, t, ti, tr, ui, ur, wi, wr
    integer :: i, ip, j, k, l, le, le1, m, n, nm1, nv2
  
    as = 0.
    if (msign == 0) then
      return
    endif
  
    if (h <= 0.0) then
      write(*,*) ' *** negative step size in <rcffi>, h = ', h, ' *** '
      stop
    endif
  
  ! *** initialization
  
    m = iabs(msign)
    n = 2**m
    if (msign > 0) then
      ar(1) = 0.5 * ar(1)
    else    
      as = ar(1) - ai(1)
      ar(1) = 0.5 * (ar(1) + ai(1))
      do i = 2, n
        ar(i) = ar(i) + ai(n - i + 2)
      enddo
      do i = 1, n
        ai(i) = 0.0
      enddo
    endif
  ! *** discrete fast-fourier transform
    nv2 = n / 2
    nm1 = n - 1
    j = 1
    do i = 1, nm1
      if (i < j) then
        tr = ar(j)
        ar(j) = ar(i)
        ar(i) = tr
        ti = ai(j)
        ai(j) = ai(i)
        ai(i) = ti
      endif
      k = nv2
      do while (j > k)
        j = j - k
        k = k / 2          
      enddo
      j = j + k
    enddo
    do i = 1, n, 2
      tr = ar(i + 1)
      ar(i + 1) = ar(i) - tr
      ar(i) = ar(i) + tr
      ti = ai(i + 1)
      ai(i + 1) = ai(i) - ti
      ai(i) = ai(i) + ti
    enddo
    if (m == 1) return
    c = 0.0
    s = float(isign(1, msign))
    le = 2
    do l = 2, m
      wr = c
      ur = wr
      wi = s
      ui = wi
      c = sqrt(c * 0.5 + 0.5)
      s = wi / (c + c)
      le1 = le
      le = le1 + le1
      do i = 1, n, le
        ip = i + le1
        tr = ar(ip)
        ar(ip) = ar(i) - tr
        ar(i)  = ar(i) + tr
        ti = ai(ip)
        ai(ip) = ai(i) - ti
        ai(i)  = ai(i) + ti
      enddo
      do j = 2, le1
        do i = j, n, le
          ip = i + le1
          tr = ar(ip) * ur - ai(ip) * ui
          ti = ar(ip) * ui + ai(ip) * ur
          ar(ip) = ar(i) - tr
          ar(i)  = ar(i) + tr
          ai(ip) = ai(i) - ti
          ai(i)  = ai(i) + ti
        enddo
        tr = ur
        ur = tr * wr - ui * wi
        ui = tr * wi + ui * wr
      enddo
    enddo
  
  ! *** correction of the discrete fft, using a trapezoidal approximation
  ! *** for the variations of the input function
  
    c = h
    if (msign >= 0) then
      c = c / 3.1415926
      ai(1) = ar(1)
      do i = 2, n
        ai(i) = ar(n - i + 2)
      enddo
    endif
    ar(1) = c * ar(1)
    ai(1) = c * ai(1)
    a = 3.1415926 / n
    wr = cos(a)
    wi = sin(a)
    t = sqrt(c)
    a = a / t
    c = 0.0
    ur = 1.0
    ui = 0.0
    do i = 2, n
      c = c + a
      tr = ur
      ur = wr * tr - wi * ui
      ui = wi * tr + wr * ui
      ti = ui / c
      tr = ti**2
      ar(i) = ar(i) * tr
      ai(i) = ai(i) * tr
      if (msign <= 0) then
        if (as /= 0.0) then
          ai(i) = ai(i) - as * (t - ur * ti) / (2 * c)
        endif
      endif
    enddo
    return
  end subroutine rcffi
  