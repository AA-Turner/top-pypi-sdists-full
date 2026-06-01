!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
! _       ___________________________                          _______| 
!| |     / / ____  / ______/___  ___/_______________   _____  / ___  /|
!| |    / / /   / / /         / /  / ___  / ___  / /  / ___/ / /  /_/ |
!| |   / / /   / / /___      / /  / /  / / /  / / /  / /__  / /____   |
!| |  / / /   / / ____/     / /  / /  / / /  / / /  /__  / /  __  /   |
!| |_/ / /___/ / /         / /  / /__/ / /__/ / /_____/ / /  /_/ /    |
!|____/_______/_/         /_/  /______/______/____/____/ /______/     |
!                                                                     |
!                                                                     | 
!        A package of FORTRAN subroutines with analytical and         | 
!         geometrical tools for VOF methods in general grids          | 
!                       and Cartesian geometry                        | 
!                                                                     | 
!                    Copyright (C) 2025 J. Lopez                      | 
!                                                                     | 
!   Dpto. Ingenieria Mecanica, Materiales y Fabricacion, UPCT. 30202, | 
!   Cartagena, Spain.                                                 | 
!                                                                     | 
!   For more information, please contact: joaquin.lopez@upct.es       | 
!---------------------------------------------------------------------| 
! This program is free software: you can redistribute it and/or modify|
! it under the terms of the GNU General Public License as published by|
! the Free Software Foundation, either version 3 of the License, or   |
! (at your option) any later version.                                 |
!                                                                     |
! This program is distributed in the hope that it will be useful,     |
! but WITHOUT ANY WARRANTY; without even the implied warranty of      |
! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       |
! GNU General Public License for more details.                        |
!                                                                     |
! You should have received a copy of the GNU General Public License   |
! along with this program.  If not, see <http://www.gnu.org/licenses/>|
!---------------------------------------------------------------------| 
! List of subroutines:                                                | 
!=====================                                                | 
!                                                                     | 
! 3D subroutines:                                                     | 
!---------------                                                      | 
! ENFORV3D ----> solve the local volume enforcement problem in 3D     | 
!                using the CIBRAVE method                             | 
! ENFORV3DSZ --> solve the local volume enforcement problem for       | 
!                rectangular parallelepiped cells using the method    | 
!                of Scardovelli and Zaleski [Journal of Computational | 
!                Physics, 164 (2000) 228-237]                         | 
! ENFORV3DYJ --> solve the local volume enforcement problem for       | 
!                tetrahedral cells using the method of Yang and James | 
!                [Journal of Computational Physics, 214 (2006) 41-54] | 
! ENFORVPPA ---> shift the paraboloid to enforce discrete volume      |
!                conservation                                         | 
! INTE3D   ----> obtain the polyhedron truncated by a plane           | 
! TOOLV3D  ----> compute the volume of a polyhedron                   | 
! CPPOL3D  ----> copy a polyhedron into a new one                     | 
! RESTORE3D----> restore the structure of a polyhedron                | 
! DIST3D   ----> compute the distance from a point to a polygon       | 
! INITF3D  ----> initialize the material volume fraction in a cell    | 
! POLOUT3D ----> write in an external VTK-format file the geometry of | 
!                a polyhedron                                         | 
! INTV3D   ----> compute the volume of the region resulting from the  | 
!                intersection between a polyhedron and a half space   | 
! INTPV3DPA ---> compute the volume of the polyhedral approximation   |
!                of the region of intersection between a paraboloid   | 
!                and an arbitrary polyhedron                          |
! INTC3D   ----> compute the geometric center of the set of vertices  | 
!                resulting from the intersection between the polyhe-  | 
!                dron edges and a half-space interface                | 
! BOX3D    ----> compute the maximum and minimum coordinates of the   | 
!                minimum-size rectangular parallelepiped that         | 
!                contains a set of points                             | 
! INTE3DFACE---> compute the intersection between a 3D planar face,   | 
!                either convex or non-convex, an a half-space         | 
! AREAFACE ----> compute the area of a 3D polygonal face              | 
! PVFIT    ----> obtain a paraboloid from a Polygonal-set Volumetric  |
!                Fit                                                  | 
! SYSTRA   ----> obtain the coordinates of a point in a new           |
!                orthonormal basis                                    |
! VOFTOOLS_DIM3D get NS and NV parameters for dimensioning arrays in  |  
!                non-Fortran 3D programs                              | 
! DEFPOL3D ----> construct a polyhedron                               | 
!                                                                     | 
! 2D subroutines:                                                     | 
!---------------                                                      | 
! ENFORV2D ----> solve the local volume enforcement problem in 2D     | 
!                using the CIBRAVE method                             | 
! ENFORV2DSZ---> solve the local volume enforcement problem for       | 
!                rectangular cells using the method of Scardovelli    | 
!                and Zaleski [Journal of Computational Physics, 164   | 
!                (2000) 228-237]                                      | 
! NEWPOL2D ----> vertex indices arrangement of the truncated          | 
!                polygon                                              | 
! INTE2D   ----> obtain the polygon truncated by a line               | 
! TOOLV2D  ----> compute the area of a polygon                        | 
! CPPOL2D  ----> copy a polygon into a new one                        | 
! RESTORE2D----> restore the structure of a polygon                   | 
! DIST2D   ----> compute the distance from a point to a segment       | 
! INITF2D  ----> initialize the material area fraction in a cell      | 
! POLOUT2D ----> write in an external file the vertex coordinatex x   | 
!                and y of a polygon in two columns format             | 
! VOFTOOLS_DIM2D get NV parameter for dimensioning arrays in          |  
!                non-Fortran 2D programs                              | 
! DEFPOL2D ----> construct a polygon                                  | 
!                                                                     | 
! Auxiliary subroutines:                                              | 
!----------------------                                               | 
! VOFTOOLSLOGO > print on screen the VOFTools logo                    | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
MODULE VOFTOOLS_MOD 
  ! .. USE Statements ..                                                  
  USE, INTRINSIC :: ISO_C_BINDING, ONLY: W_P => C_DOUBLE,I_P => C_INT,  &
       I_P2 => C_SHORT                                
  ! .. Implicit None Statement ..                                         
  IMPLICIT NONE 
  ! .. Accessibility Statements ..                                        
  PUBLIC 
  PRIVATE :: W_P,I_P,I_P2 
  ! .. Include Lines ..                                                   
#include "dimpol.h" 
  ! .. Interface Blocks ..                                                
  ABSTRACT INTERFACE 
     FUNCTION VOFTOOLS_FUNC2D(A, B) BIND(C) 
       ! .. Import Statements ..                                               
       IMPORT :: W_P 
       ! .. Function Return Value ..                                           
       REAL (W_P) :: VOFTOOLS_FUNC2D 
       ! .. Scalar Arguments ..                                                
       REAL (W_P), INTENT (IN) :: A, B 
     END FUNCTION VOFTOOLS_FUNC2D
     FUNCTION VOFTOOLS_FUNC3D(A, B, C) BIND(C) 
       ! .. Import Statements ..                                               
       IMPORT :: W_P 
       ! .. Function Return Value ..                                           
       REAL (W_P) :: VOFTOOLS_FUNC3D 
       ! .. Scalar Arguments ..                                                
       REAL (W_P), INTENT (IN) :: A, B, C 
     END FUNCTION VOFTOOLS_FUNC3D
  END INTERFACE
CONTAINS 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                               ENFORV3D                              | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index (note that if the polyhedron    | 
!            is not previously truncated, then NTP=NTV)               | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! V        = liquid volume                                            | 
! VT       = total volume of the polyhedron                           | 
! VERTP    = vertex coordinates of the polyhedron                     | 
! XNS, ... = unit-lenght normals to the faces of the polyhedron       | 
! XNC, ... = unit-lenght normal to the new face boundaries on         | 
!            \Gamma_c                                                 | 
! On return:                                                          | 
!===========                                                          | 
! C        = solution of the problem                                  | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE ENFORV3D(C,IPV,NIPV,NTP,NTS,NTV,V,VT,VERTP,XNC,XNS,YNC,YNS,&
       ZNC,ZNS) BIND(C)                                 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(OUT) :: C 
    REAL(W_P), INTENT(IN) :: V, VT 
    REAL(W_P), INTENT(IN) :: XNC, YNC, ZNC 
    INTEGER(I_P), INTENT(IN) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS, NV), NIPV(NS) 
    !.. Local Scalars                                                       
    REAL(W_P) :: C0, C1, C2, C3, CAUX, CIS, CMAX, CMAX2, CMIN, CMIN2,   &
         COEF, CTR, DNMAX, ERRV, PHIINT, SV, TOLC, VAUX, VMAX, VMAXL,   &
         VMIN, VMINL,VMINLL, XE1, XE2, XNCOR, XNCT, XV, XV1, XV2, YE1,  &
         YE2, YNCOR, YNCT, YV, YV1, YV2, ZE1, ZE2, ZNCOR, ZNCT, ZV,     &
         ZV1, ZV2 
    INTEGER(I_P) :: I, IH, II, IMAX, IMAXL, IMAXLOLD, IMIN, IMINL,      &
         INVERT, IP, IP1, IP2, IPF, IPI, IPREF, IPROJ, IS, IS1,         &
         ISC, ISOL, IV, IV1, NTP0, NTS0, NTS00, NTV0         
    !.. Local Arrays                                                        
    REAL(W_P) :: BETXE(NS, NV), BETYE(NS, NV), BETZE(NS, NV), CS(NS),   &
         CS0(NS), PHIV(NV), SUMK(NS), SUML(NS), SUMM(NS),               &
         VERTP0(NV, 3), X0(NS, NV), XNS0(NS), Y0(NS, NV), YNS0(NS),     &
         Z0(NS, NV), ZNS0(NS)                                         
    INTEGER(I_P) :: IA(NV), IPIA0(NV), IPIA1(NV), IPV0(NS, NV),         &
         ISCUT(NS), LISTV(NV), MARKIS(NS), NIPV0(NS)                  
    ! .. Intrinsic Procedures ..                                            
    INTRINSIC :: ABS, INT, REAL 
                                                                        
    IF(VT.LE.0.0_W_P) THEN 
       WRITE(6,*) 'THE POLYHEDRON HAS NULL OR NEGATIVE VOLUME.' 
       RETURN 
    END IF
    IF(NTP.GT.NTV) THEN
       WRITE(6,*) 'NTP>NTV. THE POLYHEDRON MUST BE RESTORED.'
       RETURN
    END IF
    !.. To execute in quad precision may be convinient to use a lower value 
    !.. for TOLC such as, for example, 1.0D-20                              
    TOLC=1.0E-12_W_P 
    DO IS=1,NTS 
       IP=IPV(IS,1) 
       CS(IS)=-XNS(IS)*VERTP(IP,1)-YNS(IS)*VERTP(IP,2)-ZNS(IS)*         &
            VERTP(IP,3)  
    END DO
    VAUX=V 
    LISTV(1)=1 
    DO IV=1,NTV 
       PHIV(IV)=XNC*VERTP(IV,1)+YNC*VERTP(IV,2)+ZNC*VERTP(IV,3) 
       !* Ordered list of global vertex indices                                
       DO I=1,IV-1 
          IF(PHIV(IV).GT.PHIV(LISTV(I))) THEN 
             DO II=IV,I+1,-1 
                LISTV(II)=LISTV(II-1) 
             END DO
             LISTV(I)=IV 
             GOTO 10 
          END IF
       END DO
       LISTV(IV)=IV 
10     CONTINUE 
    END DO
                                                                        
    INVERT=0 
    XNCOR=XNC 
    YNCOR=YNC 
    ZNCOR=ZNC 
    IMIN=1 
    IMAX=NTP 
    VMIN=0.0_W_P 
    VMAX=VT 
    
    !* Obtain the tentative solution bracketing by interpolation            
    IMAXLOLD=NTP+1 
22  CONTINUE 
    PHIINT=PHIV(LISTV(IMIN))-(PHIV(LISTV(IMIN))-PHIV(LISTV(IMAX)))*     &
         (V-VMIN)/(VMAX-VMIN)                                         
    IMAXL=0 
    IMINL=0 
    DO IP=IMIN+1,IMAX 
       I=IP 
       IF(PHIV(LISTV(IP)).LT.PHIINT) THEN 
          IMAXL=IP 
          IMINL=IP-1 
          GOTO 11 
       END IF
    END DO
    IF(IMAXL.EQ.0.AND.IMINL.EQ.0) THEN 
       C=-PHIINT 
       RETURN 
    END IF
11  CONTINUE 
    
    CMAX=PHIV(LISTV(IMINL)) 
    CMIN=PHIV(LISTV(IMAXL)) 
    
    IF((NTP-IMAXL).LT.(IMINL-1)) THEN 
       INVERT=1 
       CAUX=CMIN 
       CMIN=-CMAX 
       CMAX=-CAUX 
       VAUX=VT-V 
       XNCT=-XNCOR 
       YNCT=-YNCOR 
       ZNCT=-ZNCOR 
       IPREF=LISTV(IMAXL) 
    ELSE 
       INVERT=0 
       VAUX=V 
       XNCT=XNCOR 
       YNCT=YNCOR 
       ZNCT=ZNCOR 
       IPREF=LISTV(IMINL) 
    END IF
    DO I=1,NTP 
       IF(I.LE.IMINL) THEN 
          IA(LISTV(I))=1-INVERT 
       ELSE 
          IA(LISTV(I))=INVERT 
       END IF
    END DO
    !. Traslacion:                                                          
    CALL TRPOL3D(CS0,CS,IPREF,IPV0,IPV,MARKIS,NIPV0,NIPV,NTP0,NTP,      &
         NTS0,NTS,NTV0,NTV,VERTP0,VERTP,XNS0,XNS,YNS0,YNS,ZNS0,ZNS)   
    CTR=XNCT*VERTP(IPREF,1)+YNCT*VERTP(IPREF,2)+ZNCT*VERTP(IPREF,3) 
    CMIN=CMIN-CTR 
    CMAX=CMAX-CTR 
    !* End of procedure SETIA                                               
    !* Construction of the new polyhedron                                   
    NTS00=NTS0 
    CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,ISCUT,NIPV0,NTP0,NTS0,NTV0,XNCT,  &
         XNS0,YNCT,YNS0,ZNCT,ZNS0)            
    ! disjoint regions may produce this situation
    IF(NTS0.LE.NTS00) THEN 
       IF((IMAX-IMAXL).GT.(IMINL-IMIN)) THEN 
          IMAXL=IMAXL+1 
          IMINL=IMAXL-1 
       ELSE 
          IMINL=IMINL-1 
          IMAXL=IMINL+1 
       END IF
       GOTO 11 
    END IF
    !* Contributions of the new faces \Gamma_c                              
    DO IS=NTS00+1,NTS0 
       DO IV=1,NIPV0(IS) 
          IPI=IPV0(IS,IV) 
          IPF=IPIA1(IPI) 
          IP=IPIA0(IPI) 
          XV=VERTP0(IPF,1)-VERTP0(IP,1) 
          YV=VERTP0(IPF,2)-VERTP0(IP,2) 
          ZV=VERTP0(IPF,3)-VERTP0(IP,3) 
          CIS=XNS0(IS)*XV+YNS0(IS)*YV+ZNS0(IS)*ZV 
          !cut edge and \Gamma_c normal are perpendic
          IF(CIS.EQ.0.0) THEN 
             BETXE(IS,IV)=0.0_W_P 
             BETYE(IS,IV)=0.0_W_P 
             BETZE(IS,IV)=0.0_W_P 
          ELSE 
             BETXE(IS,IV)=-XV/CIS 
             BETYE(IS,IV)=-YV/CIS 
             BETZE(IS,IV)=-ZV/CIS 
          END IF
          COEF=XNS0(IS)*VERTP0(IPF,1)+YNS0(IS)*VERTP0(IPF,2)+ZNS0(IS)*  &
               VERTP0(IPF,3)                             
          X0(IS,IV)=VERTP0(IPF,1)+BETXE(IS,IV)*COEF 
          Y0(IS,IV)=VERTP0(IPF,2)+BETYE(IS,IV)*COEF 
          Z0(IS,IV)=VERTP0(IPF,3)+BETZE(IS,IV)*COEF 
       END DO
    END DO
    !* Contributions of the rest of faces                                   
    DO IS=1,NTS00 
       IF(MARKIS(IS).EQ.0) THEN 
          DO IV=1,NIPV0(IS) 
             IP=IPV0(IS,IV) 
             IF(IA(IP).EQ.1) THEN 
                X0(IS,IV)=VERTP0(IP,1) 
                Y0(IS,IV)=VERTP0(IP,2) 
                Z0(IS,IV)=VERTP0(IP,3) 
                BETXE(IS,IV)=0.0_W_P 
                BETYE(IS,IV)=0.0_W_P 
                BETZE(IS,IV)=0.0_W_P 
             ELSE
                ISC=NTS00+1
                IV1=1
                DO IS1=NTS00+1,NTS0 
                   ISC=IS1 
                   DO IV1=1,NIPV0(IS1) 
                      IP1=IPV0(IS1,IV1) 
                      IF(IP1.EQ.IP) GOTO 100 
                   END DO
                END DO
100             CONTINUE 
                BETXE(IS,IV)=BETXE(ISC,IV1) 
                BETYE(IS,IV)=BETYE(ISC,IV1) 
                BETZE(IS,IV)=BETZE(ISC,IV1) 
                X0(IS,IV)=X0(ISC,IV1) 
                Y0(IS,IV)=Y0(ISC,IV1) 
                Z0(IS,IV)=Z0(ISC,IV1) 
             END IF
          END DO
       END IF
    END DO
    !** Vectors K,L and M                                                   
    DO IS=NTS00+1,NTS0 
       ISCUT(IS)=1 
       MARKIS(IS)=0 
    END DO
    DO IS=1,NTS0 
       IF(MARKIS(IS).EQ.0) THEN 
          SUMK(IS)=0.0_W_P 
          SUML(IS)=0.0_W_P 
          SUMM(IS)=0.0_W_P 
          IF(ABS(YNS0(IS)).GE.ABS(XNS0(IS)).AND.ABS(YNS0(IS)).GE.       &
               ABS(ZNS0(IS))) THEN                                      
             IPROJ=2 
             DNMAX=YNS0(IS) 
          ELSEIF(ABS(ZNS0(IS)).GE.ABS(XNS0(IS)).AND.ABS(ZNS0(IS))       &
               .GE.ABS(YNS0(IS))) THEN  
             IPROJ=3 
             DNMAX=ZNS0(IS) 
          ELSE 
             IPROJ=1 
             DNMAX=XNS0(IS) 
          END IF
          IH=INT((NIPV0(IS)-2)/2) 
          DO I=2,IH+1 
             IP=2*I 
             IP1=IP-1 
             IP2=IP-2 
             IF(IPROJ.EQ.1) THEN 
                YV1=Y0(IS,IP1)-Y0(IS,1) 
                ZV1=Z0(IS,IP1)-Z0(IS,1) 
                YV2=Y0(IS,IP)-Y0(IS,IP2) 
                ZV2=Z0(IS,IP)-Z0(IS,IP2) 
                YE1=BETYE(IS,IP1)-BETYE(IS,1) 
                ZE1=BETZE(IS,IP1)-BETZE(IS,1) 
                YE2=BETYE(IS,IP)-BETYE(IS,IP2) 
                ZE2=BETZE(IS,IP)-BETZE(IS,IP2) 
                SUMK(IS)=SUMK(IS)+YV1*ZV2-ZV1*YV2 
                SUML(IS)=SUML(IS)+YV1*ZE2-ZV1*YE2-(YV2*ZE1-ZV2*YE1) 
                SUMM(IS)=SUMM(IS)+YE1*ZE2-ZE1*YE2 
             ELSEIF(IPROJ.EQ.2) THEN 
                XV1=X0(IS,IP1)-X0(IS,1) 
                ZV1=Z0(IS,IP1)-Z0(IS,1) 
                XV2=X0(IS,IP)-X0(IS,IP2) 
                ZV2=Z0(IS,IP)-Z0(IS,IP2) 
                XE1=BETXE(IS,IP1)-BETXE(IS,1) 
                ZE1=BETZE(IS,IP1)-BETZE(IS,1) 
                XE2=BETXE(IS,IP)-BETXE(IS,IP2) 
                ZE2=BETZE(IS,IP)-BETZE(IS,IP2) 
                SUMK(IS)=SUMK(IS)+ZV1*XV2-XV1*ZV2 
                SUML(IS)=SUML(IS)+ZV1*XE2-XV1*ZE2-(ZV2*XE1-XV2*ZE1) 
                SUMM(IS)=SUMM(IS)+ZE1*XE2-XE1*ZE2 
             ELSE 
                XV1=X0(IS,IP1)-X0(IS,1) 
                YV1=Y0(IS,IP1)-Y0(IS,1) 
                XV2=X0(IS,IP)-X0(IS,IP2) 
                YV2=Y0(IS,IP)-Y0(IS,IP2) 
                XE1=BETXE(IS,IP1)-BETXE(IS,1) 
                YE1=BETYE(IS,IP1)-BETYE(IS,1) 
                XE2=BETXE(IS,IP)-BETXE(IS,IP2) 
                YE2=BETYE(IS,IP)-BETYE(IS,IP2) 
                SUMK(IS)=SUMK(IS)+XV1*YV2-YV1*XV2 
                SUML(IS)=SUML(IS)+XV1*YE2-YV1*XE2-(XV2*YE1-YV2*XE1) 
                SUMM(IS)=SUMM(IS)+XE1*YE2-YE1*XE2 
             END IF
          END DO
          IF(2*(IH+1).LT.NIPV0(IS)) THEN 
             IF(IPROJ.EQ.1) THEN 
                YV1=Y0(IS,NIPV0(IS))-Y0(IS,1) 
                ZV1=Z0(IS,NIPV0(IS))-Z0(IS,1) 
                YV2=Y0(IS,1)-Y0(IS,NIPV0(IS)-1) 
                ZV2=Z0(IS,1)-Z0(IS,NIPV0(IS)-1) 
                YE1=BETYE(IS,NIPV0(IS))-BETYE(IS,1) 
                ZE1=BETZE(IS,NIPV0(IS))-BETZE(IS,1) 
                YE2=BETYE(IS,1)-BETYE(IS,NIPV0(IS)-1) 
                ZE2=BETZE(IS,1)-BETZE(IS,NIPV0(IS)-1) 
                SUMK(IS)=SUMK(IS)+YV1*ZV2-ZV1*YV2 
                SUML(IS)=SUML(IS)+YV1*ZE2-ZV1*YE2-(YV2*ZE1-ZV2*YE1) 
                SUMM(IS)=SUMM(IS)+YE1*ZE2-ZE1*YE2 
             ELSEIF(IPROJ.EQ.2) THEN 
                XV1=X0(IS,NIPV0(IS))-X0(IS,1) 
                ZV1=Z0(IS,NIPV0(IS))-Z0(IS,1) 
                XV2=X0(IS,1)-X0(IS,NIPV0(IS)-1) 
                ZV2=Z0(IS,1)-Z0(IS,NIPV0(IS)-1) 
                XE1=BETXE(IS,NIPV0(IS))-BETXE(IS,1) 
                ZE1=BETZE(IS,NIPV0(IS))-BETZE(IS,1) 
                XE2=BETXE(IS,1)-BETXE(IS,NIPV0(IS)-1) 
                ZE2=BETZE(IS,1)-BETZE(IS,NIPV0(IS)-1) 
                SUMK(IS)=SUMK(IS)+ZV1*XV2-XV1*ZV2 
                SUML(IS)=SUML(IS)+ZV1*XE2-XV1*ZE2-(ZV2*XE1-XV2*ZE1) 
                SUMM(IS)=SUMM(IS)+ZE1*XE2-XE1*ZE2 
             ELSE 
                XV1=X0(IS,NIPV0(IS))-X0(IS,1) 
                YV1=Y0(IS,NIPV0(IS))-Y0(IS,1) 
                XV2=X0(IS,1)-X0(IS,NIPV0(IS)-1) 
                YV2=Y0(IS,1)-Y0(IS,NIPV0(IS)-1) 
                XE1=BETXE(IS,NIPV0(IS))-BETXE(IS,1) 
                YE1=BETYE(IS,NIPV0(IS))-BETYE(IS,1) 
                XE2=BETXE(IS,1)-BETXE(IS,NIPV0(IS)-1) 
                YE2=BETYE(IS,1)-BETYE(IS,NIPV0(IS)-1) 
                SUMK(IS)=SUMK(IS)+XV1*YV2-YV1*XV2 
                SUML(IS)=SUML(IS)+XV1*YE2-YV1*XE2-(XV2*YE1-YV2*XE1) 
                SUMM(IS)=SUMM(IS)+XE1*YE2-YE1*XE2 
             END IF
          END IF
          SUMK(IS)=SUMK(IS)/DNMAX 
          SUML(IS)=SUML(IS)/DNMAX 
          SUMM(IS)=SUMM(IS)/DNMAX 
       END IF
    END DO
    !** Coefficients of the analytical equation: C3·x^3+C2·x^2+C1·x+C0=0 
    C3=0.0_W_P 
    C2=0.0_W_P 
    C1=0.0_W_P 
    DO IS=NTS00+1,NTS0 
       C3=C3+SUMM(IS) 
       C2=C2+SUML(IS) 
       C1=C1+SUMK(IS) 
    END DO
    C0=6.0_W_P*VAUX 
    DO IS=1,NTS00 
       IF(MARKIS(IS).EQ.0) THEN 
          C2=C2+SUMM(IS)*CS0(IS) 
          C1=C1+SUML(IS)*CS0(IS) 
          C0=C0+SUMK(IS)*CS0(IS) 
       END IF
    END DO
    !. The problem to be solved can be expressed as y(x)=V, and taking into 
    !. account the considerations in [Lopez et al., J. Comput. Phys. 392    
    !. (2019) 666-693], the curve y(x) could be defined as                  
    !. y(x)=(c3/6)*x^3-(c2/6)*x^2+(c1/6)*x+(vaux-c0/6)                      
    VMAXL=VAUX-(C3*CMIN*CMIN*CMIN+C2*CMIN*CMIN+C1*CMIN+C0)/6.0_W_P
    VMINL=VAUX-(C3*CMAX*CMAX*CMAX+C2*CMAX*CMAX+C1*CMAX+C0)/6.0_W_P
    IF(INVERT.EQ.1) THEN 
       VMINLL=VT-VMAXL 
       VMAXL=VT-VMINL 
       VMINL=VMINLL 
    END IF
    SV=(VMINL-V)*(VMAXL-V) 
    IF(SV.GT.0.0_W_P.AND.(IMAX-IMIN).GT.1.AND.IMAXLOLD.NE.IMAXL) THEN 
       IF(VMAXL.GT.V) THEN 
          VMAX=VMINL 
          IMAX=IMINL 
       ELSE 
          VMIN=VMAXL 
          IMIN=IMAXL 
       END IF
       IMAXLOLD=IMAXL 
       GOTO 22 
    END IF
    CALL EQSOL3D(C0,C1,C2,C3,CMIN,CMAX,C) 
    ERRV=C3*C*C*C+C2*C*C+C1*C+C0 
    IF(ABS(ERRV).GT.TOLC)CALL NEWTON3D(C0,C1,C2,C3,CMIN,CMAX,C,ISOL)  
    IF(INVERT.EQ.0) THEN 
       C=-C 
       CMAX2=-CMIN 
       CMIN2=-CMAX 
    ELSE 
       CMAX2=CMAX 
       CMIN2=CMIN 
    END IF
    !. DETRANSLATE                                                          
    IF(INVERT.EQ.1) THEN 
       C=C+CTR 
    ELSE 
       C=C-CTR 
    END IF
    RETURN 
  END SUBROUTINE ENFORV3D
!-----------------------   END OF ENFORV3D  --------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              TRPOL3D                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CS0      = constants of the planes containing the faces of the      | 
!            original polyhedron                                      | 
! IPREF    = reference point                                          | 
! XNS0, ...= unit-lenght normals to the faces of the original pol.    | 
! IPV0     = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NIPV0    = number of vertices of each face                          | 
! NTP0     = last global vertex index                                 | 
! NTS0     = total number of faces                                    | 
! NTV0     = total number of vertices                                 | 
! VERTI0   = vertex coordinates of the original polyhedron            | 
! On return:                                                          | 
!===========                                                          | 
! CS       = constants of the planes containing the faces of the      | 
!            copied polyhedron                                        | 
! XNS,  ...= unit-lenght normals to the faces of the copied pol.      | 
! IPV      = array containing the global indices of the copied pol.   | 
!            vertices                                                 | 
! MARKIS   = 1 if IPREF belongs to the face, 0 otherwise              | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTI    = vertex coordinates of the copied polyhedron              | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE TRPOL3D(CS,CS0,IPREF,IPV,IPV0,MARKIS,NIPV,NIPV0,NTP,NTP0,  &
       NTS,NTS0,NTV,NTV0,VERTI,VERTI0,XNS,XNS0,YNS,YNS0,ZNS,ZNS0)
    !* Scalar Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPREF,NTP0,NTS0,NTV0 
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !* Array Arguments                                                      
    INTEGER(I_P), INTENT(IN) :: IPV0(NS,NV),NIPV0(NS) 
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),MARKIS(NS),NIPV(NS) 
    REAL(W_P), INTENT(IN) :: CS0(NS),VERTI0(NV,3),XNS0(NS),YNS0(NS),    &
         ZNS0(NS)                                                     
    REAL(W_P), INTENT(OUT) :: CS(NS),VERTI(NV,3),XNS(NS),YNS(NS),       &
         ZNS(NS)                                                      
    !* Local Scalars         
    INTEGER(I_P) :: I,IP,J 
    NTS=NTS0 
    NTV=NTV0 
    NTP=NTP0 
    DO IP=1,NTP0 
       DO J=1,3 
          VERTI(IP,J)=VERTI0(IP,J)-VERTI0(IPREF,J) 
       END DO
    END DO
    DO I=1,NTS0 
       MARKIS(I)=0 
       XNS(I)=XNS0(I) 
       YNS(I)=YNS0(I) 
       ZNS(I)=ZNS0(I) 
       NIPV(I)=NIPV0(I) 
       CS(I)=CS0(I)+XNS0(I)*VERTI0(IPREF,1)+YNS0(I)*VERTI0(IPREF,2)     &
            +ZNS0(I)*VERTI0(IPREF,3)                                   
       DO  J=1,NIPV0(I) 
          IPV(I,J)=IPV0(I,J) 
          IF(IPREF.EQ.IPV0(I,J)) MARKIS(I)=1 
       END DO
    END DO
    RETURN 
  END SUBROUTINE TRPOL3D
!-------------------------- END OF TRPOL3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          ENFORV3DSZ                                 | 
!... Scardovelli and Zaleski version for rectangular parallelepiped   | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! DX, ...  = side lengths of the rectangular parallelepiped           | 
! VERTP    = vertex coordinates of the polyhedron                     | 
! XNC, ... = unit-lenght normal to the new face \Gamma_c              | 
! V        = liquid volume                                            | 
! On return:                                                          | 
!===========                                                          | 
! C        = solution of the problem                                  | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE ENFORV3DSZ(C,DX,DY,DZ,V,VERTP,XNC,YNC,ZNC) BIND(C) 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: DX,DY,DZ,XNC,YNC,ZNC 
    REAL(W_P), INTENT(INOUT) :: V 
    REAL(W_P), INTENT(OUT) :: C 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,3) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,I2,IMAX,IMIN 
    REAL(W_P) :: A0,A1,A2,A3,ALPHA,ARG,CI,CMAX,CMIN,M1,M12,M2,M3,MAUX,  &
         P0,Q0,SN,THETA,TOLE,VBACK,V1,V2,V3,VT,XM,XMI,YM,YMI,ZM,ZMI   
    !.. Local Arrays                                                        
    REAL(W_P) :: M(3) 
    !.. Intrinsic Procedures                                                
    INTRINSIC :: ABS, ACOS, COS, MAX, REAL, SIN 
    TOLE=1.0E-09_W_P 
    CMIN=1.0E+14_W_P 
    CMAX=-1.0E+14_W_P 
    VT=DX*DY*DZ 
    VBACK=V 
    V=V/VT
    A0=0.0_W_P
    A1=0.0_W_P
    !.. The vertex indices of the rectangular parallelepiped are supposed   
    !.. to be listed from 1 to 8.                                           
    DO I=1,8 
       CI=-(VERTP(I,1)*XNC+VERTP(I,2)*YNC+VERTP(I,3)*ZNC) 
       IF(CI.LE.CMIN) THEN 
          CMIN=CI 
          IMIN=I 
       END IF
       IF(CI.GE.CMAX) THEN 
          CMAX=CI 
          IMAX=I 
       END IF
    END DO
    !.. If the liquid volume fraction is higher than 0.5, solve the inverse 
    IF((VBACK/VT).LE.(1.0_W_P/2.0_W_P)) THEN 
       CI=CMIN 
       I=IMIN 
    ELSE 
       CI=CMAX 
       I=IMAX 
       V=1.0_W_P-V 
    END IF
    !.. Normalize the plane equation                                        
    SN=ABS(XNC)+ABS(YNC)+ABS(ZNC) 
    XM=XNC/SN 
    YM=YNC/SN 
    ZM=ZNC/SN 
    XMI=XM*DX 
    YMI=YM*DY 
    ZMI=ZM*DZ 
    SN=ABS(XMI)+ABS(YMI)+ABS(ZMI) 
    XM=ABS(XMI)/SN 
    YM=ABS(YMI)/SN 
    ZM=ABS(ZMI)/SN 
    !.. Region limits                                                       
    M(1)=XM 
    M(2)=YM 
    M(3)=ZM 
    DO I=1,2 
       I2=I+1 
       IF(M(I2).LT.M(I)) THEN 
          MAUX=M(I) 
          M(I)=M(I2) 
          M(I2)=MAUX 
       END IF
    END DO
    IF(M(2).LT.M(1)) THEN 
       MAUX=M(1) 
       M(1)=M(2) 
       M(2)=MAUX 
    END IF
    M1=M(1) 
    M2=M(2) 
    M3=M(3) 
    M12=M1+M2 
    V1=(M1*M1)/DMAX1(6.0_W_P*M2*M3,TOLE) 
    V2=V1+(M2-M1)/(2.0_W_P*M3) 
    IF(M3.LT.M12) THEN 
       V3=((3.0_W_P*M12-M3)*(M3*M3)+(M1-3.0_W_P*M3)*(M1*M1)+(M2-        &
            3.0_W_P*M3)*(M2*M2))/(6.0_W_P*M1*M2*M3)               
    ELSE 
       V3=M12/(2.0_W_P*M3) 
    END IF
    IF(V.GE.V2.AND.V.LT.V3) THEN 
       A3=-1.0_W_P 
       A2=3.0_W_P*M12/A3 
       A1=-3.0_W_P*(M1*M1+M2*M2)/A3 
       A0=(M1*M1*M1+M2*M2*M2-(6.0_W_P*M1*M2*M3*V))/A3 
       A3=1.0_W_P 
    ELSE 
       IF(V.GE.V3.AND.V.LE.(1.0_W_P/2.0_W_P).AND.M3.LT.M12) THEN 
          A3=-2.0_W_P 
          A2=3.0_W_P/A3 
          A1=-3.0_W_P*(M1*M1+M2*M2+M3*M3)/A3 
          A0=(M1*M1*M1+M2*M2*M2+M3*M3*M3-(6.0_W_P*M1*M2*M3*V))/A3 
          A3=1.0_W_P 
       END IF
    END IF
    !.. Solution of the inverse problem                                     
    IF(V.GE.0.0_W_P.AND.V.LT.V1) THEN 
       ALPHA=(6.0_W_P*M1*M2*M3*V)**(1.0_W_P/3.0_W_P) 
       GOTO 20 
    END IF
    IF(V.GE.V1.AND.V.LT.V2) THEN 
       ALPHA=(1.0_W_P/2.0_W_P)*(M1+(M1*M1+8.0_W_P*M2*M3*(V-V1))**(      &
            1.0_W_P/2.0_W_P))                                         
       GOTO 20 
    END IF
    IF((V.GE.V2.AND.V.LT.V3).OR.(V.GE.V3.AND.V.LE.(1.0_W_P/2.0_W_P)     &
         .AND.M3.LT.M12)) THEN                                         
       P0=(A1/3.0_W_P)-((A2*A2)/9.0_W_P) 
       Q0=((A1*A2-3.0_W_P*A0)/6.0_W_P)-(A2*A2*A2)/27.0_W_P 
       ARG=Q0/((-1.0_W_P*P0*P0*P0)**(1.0_W_P/2.0_W_P)) 
       IF(ABS(ARG).GT.1.0_W_P) THEN 
          IF(ARG.LT.0.0) THEN 
             ARG=-1.0_W_P
          ELSE 
             ARG=1.0_W_P 
          END IF
       END IF
       THETA=ACOS(ARG)/3.0_W_P 
       ALPHA=((-1.0_W_P*P0)**(1.0_W_P/2.0_W_P))*(SIN(THETA)*(           &
            3.0_W_P**(1.0_W_P/2.0_W_P))-COS(THETA))-(A2/3.0_W_P)     
    ELSE 
       ALPHA=M3*V+M12/2.0_W_P 
    END IF
20  CONTINUE 
    IF((VBACK/VT).LE.(1.0_W_P/2.0_W_P)) THEN 
       C=CMIN+ALPHA*ABS(CMAX-CMIN) 
    ELSE 
       C=CMAX-ALPHA*ABS(CMAX-CMIN) 
    END IF
    V=VBACK 
    RETURN 
  END SUBROUTINE ENFORV3DSZ
!---------------------   END OF ENFORV3DSZ   -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              ENFORV3DYJ                             | 
! Method proposed by [Yang, James, J. Comput. Phy. 214 (2006) 41-54]  | 
! for tetrahedral grid cells                                          | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! V        = liquid volume                                            | 
! VT       = total volume of the tetrahedron                          | 
! VERTP    = vertex coordinates of the tetrahedron                    | 
! XNC, ... = unit-lenght normal to the new face boundary on \Gamma_c  | 
! On return:                                                          | 
!===========                                                          | 
! C        = solution of the problem                                  | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE ENFORV3DYJ(C,V,VT,VERTP,XNC,YNC,ZNC) BIND(C) 
    !.. Scalar arguments                                                    
    REAL(W_P), INTENT(IN) :: V,VT,XNC,YNC,ZNC 
    REAL(W_P), INTENT(OUT) :: C 
    !.. Array arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,3) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,II,IP1,IP2,IP3,IP4,IV 
    REAL(W_P) :: A,ALPHA,B,COEF,COEF2,D,EX,F,FB,FC,P,PA,PB,PC,PD,       &
         PHIVREF,Q,THETA,X,XNCA,Y,YNCA,Z,ZNCA                         
    !.. Local Arrays                                                        
    INTEGER(I_P) :: LISTV(NV) 
    REAL(W_P) :: PHIV(NV) 
    
    IF(VT.LE.0.0_W_P) THEN 
       WRITE(6,*) 'THE POLYHEDRON HAS NULL OR NEGATIVE VOLUME.' 
       RETURN 
    END IF
    
    !. Unit normal vector of the interface, which points away from fluid    
    XNCA=-XNC 
    YNCA=-YNC 
    ZNCA=-ZNC 
    
    F=V/VT 
    LISTV(1)=1 
    DO IV=1,4 
       PHIV(IV)=XNCA*VERTP(IV,1)+YNCA*VERTP(IV,2)+ZNCA*VERTP(IV,3) 
       !* Ordered list of global vertex indices                                
       DO I=1,IV-1 
          IF(PHIV(IV).LT.PHIV(LISTV(I))) THEN 
             DO II=IV,I+1,-1 
                LISTV(II)=LISTV(II-1) 
             END DO
             LISTV(I)=IV 
             GOTO 10 
          END IF
       END DO
       LISTV(IV)=IV 
10     CONTINUE 
    END DO
    PHIVREF=PHIV(LISTV(1)) 
    DO I=1,4 
       PHIV(LISTV(I))=PHIV(LISTV(I))-PHIVREF 
    END DO
    PA=PHIV(LISTV(2)) 
    PB=PHIV(LISTV(2)) 
    PC=PHIV(LISTV(3)) 
    PD=PHIV(LISTV(4)) 
    !. Regime classification                                                
    IF(PB.EQ.PA.AND.PC.EQ.PA) THEN 
       FC=1.0_W_P 
       FB=0.0_W_P
    ELSEIF(PC.EQ.PB.AND.PD.EQ.PB) THEN 
       FB=1.0_W_P
       FC=0.0_W_P
    ELSE 
       FB=((PB/PC)*(PB/PC))*(PC/PD) 
       COEF=(PD-PC)/(PD-PB) 
       FC=(COEF*COEF)*((PD-PB)/PD) 
    END IF
    IF(F.LE.FB) THEN 
       !. Regime I                                                             
       IP1=LISTV(1) 
       IP2=LISTV(2) 
       EX=1.0_W_P/3.0_W_P 
       X=VERTP(IP1,1)+(VERTP(IP2,1)-VERTP(IP1,1))*(F/FB)**EX 
       Y=VERTP(IP1,2)+(VERTP(IP2,2)-VERTP(IP1,2))*(F/FB)**EX 
       Z=VERTP(IP1,3)+(VERTP(IP2,3)-VERTP(IP1,3))*(F/FB)**EX 
       C=XNCA*X+YNCA*Y+ZNCA*Z 
    ELSEIF(F.GE.(1.0_W_P-FC)) THEN 
       !. Regime III                                                           
       IP4=LISTV(4) 
       IP3=LISTV(3) 
       EX=1.0_W_P/3.0_W_P 
       X=VERTP(IP4,1)+(VERTP(IP3,1)-VERTP(IP4,1))*((1.0_W_P-F)/FC)**EX 
       Y=VERTP(IP4,2)+(VERTP(IP3,2)-VERTP(IP4,2))*((1.0_W_P-F)/FC)**EX 
       Z=VERTP(IP4,3)+(VERTP(IP3,3)-VERTP(IP4,3))*((1.0_W_P-F)/FC)**EX 
       C=XNCA*X+YNCA*Y+ZNCA*Z 
    ELSE 
       !. Regime II                                                            
       COEF=PC-PB 
       A=-((COEF*COEF)/PD)*(1.0_W_P/PC+1.0_W_P/(PD-PB)) 
       B=3.0_W_P*(COEF*COEF)/(PD*PC) 
       C=3.0_W_P*PB*COEF/(PD*PC) 
       D=PB*PB/(PD*PC)-F 
       P=C/A-B*B/(3.0_W_P*A*A) 
       Q=D/A+(2.0_W_P*B*B*B)/(27.0_W_P*A*A*A)-(B*C)/(3.0_W_P*A*A) 
       COEF2=P/3D0 
       THETA=ACOS(-Q/(2.0_W_P*SQRT(-COEF2*COEF2*COEF2)))/3.0_W_P 
       ALPHA=SQRT(-COEF2)*(SQRT(3.0_W_P)*SIN(THETA)-COS(THETA))-B/(     &
            3.0_W_P*A) 
       C=ALPHA*(PC-PB)+PB+PHIVREF 
    END IF
    RETURN 
  END SUBROUTINE ENFORV3DYJ
!----------------------   END OF ENFORV3DYJ  -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              ENFORVPPAOLD                              | 
! The paraboloid is shifted to enforce discrete volume conservation   | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NC       = number of sub-cells along each coordinate axis of the    | 
!            superimposed Cartesian grid                              | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! V        = liquid volume                                            | 
! VT       = total volume of the polyhedron                           | 
! VERTP    = vertex coordinates of the polyhedron                     | 
! XNS, ... = unit-lenght normals to the faces of the polyhedron       | 
! On return:                                                          | 
!===========                                                          | 
! C        = solution of the problem                                  | 
! IE       = 0, if the root is found; 1, otherwise                    | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE ENFORVPPAOLD(C,CPARAB,IE,IPV,NC,NIPV,NTP,NTS,V,VT,VERTP,      &
       XNS,YNS,ZNS) BIND(C)        
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(OUT) :: C 
    REAL(W_P), INTENT(IN) :: V, VT 
    INTEGER(I_P), INTENT(OUT) :: IE 
    INTEGER(I_P), INTENT(IN) :: NC,NTP,NTS
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: CPARAB(12),VERTP(NV,3),XNS(NS),YNS(NS),    &
         ZNS(NS) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS)
    !.. Local Scalars
    INTEGER(I_P) :: I,II,IP,ITER,NITER,NTV
    REAL(W_P) :: C0,C1,CI,CIQ,DMOD,D,D0,D1,DD,DVF,FL,P,Q,R,S,T,TOLC,    &
         TOLF,UL,VL,VF,VF0,VF1,VFI,VFIQ,VFREF,X,XMAX,XMIN,Y,YMAX,YMIN,  &
         Z,ZMAX,ZMIN
    !.. Local Arrays      
    INTEGER(I_P) :: LISTV(NV) !list of ordered vertices
    REAL(W_P) :: CPARABL(12),PHI(NV),VN(9)
    IE=0
    NITER=100 ! Maximum number of Brent's iterations
    NTV=NTP !it's suppossed that the polyhedron hasn't been truncated
    TOLF=1.0E-10_W_P ! volume of fluid fraction tolerance
    TOLC=1.0E-16_W_P ! paraboloid location tolerance
    VFREF=V/VT
    ! Initial guess
    CALL INTPV3DPA(CPARAB,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF,XNS,YNS,     &
         ZNS)
    C0=CPARAB(1)
    VF0=VF/VT
    IF(ABS(VF0-VFREF).LT.TOLF) THEN
       C=C0
       RETURN
    END IF
    !Paraboloid orthonormal basis
    VN(1)=CPARAB(7) ! x-component of the shift vector
    VN(2)=CPARAB(8) ! y-component of the shift vector
    VN(3)=CPARAB(9) ! z-component of the shift vector
    VN(4)=VN(2)
    VN(5)=-VN(1)
    VN(6)=0.0_W_P
    DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
    IF(DMOD.NE.0.0_W_P) THEN
       VN(4)=VN(4)/DMOD
       VN(5)=VN(5)/DMOD
    ELSE
       VN(4)=VN(3)
       VN(5)=0.0_W_P
       VN(6)=-VN(1)
       DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
       VN(4)=VN(4)/DMOD
       VN(6)=VN(6)/DMOD
    END IF
    VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
    VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
    VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
    LISTV(1)=1
    XMAX=0.0_W_P
    XMIN=1.0E+20_W_P
    YMAX=0.0_W_P
    YMIN=1.0E+20_W_P
    ZMAX=0.0_W_P
    ZMIN=1.0E+20_W_P
    DO IP=1,NTP
       X=VERTP(IP,1)
       Y=VERTP(IP,2)
       Z=VERTP(IP,3)
       XMAX=MAX(XMAX,X)
       XMIN=MIN(XMIN,X)
       YMAX=MAX(YMAX,Y)
       YMIN=MIN(YMIN,Y)
       ZMAX=MAX(ZMAX,Z)
       ZMIN=MIN(ZMIN,Z)
       CALL PFUNC3D(PHI(IP),CPARAB,VN,X,Y,Z)
       !* Ordered list of global vertex indices                                
       DO I=1,IP-1 
          IF(PHI(IP).GT.PHI(LISTV(I))) THEN 
             DO II=IP,I+1,-1 
                LISTV(II)=LISTV(II-1) 
             END DO
             LISTV(I)=IP 
             GOTO 10 
          END IF
       END DO
       LISTV(IP)=IP
10     CONTINUE 
    END DO
    ! Solution bracketting.
    ! LISTV(1) --> gives the vertex IP through which the shifted
    !              paraboloid passes and truncates zero fluid volume
    ! LISTV(NTP)-> gives the vertex IP through which the shifted
    !              paraboloid passes and truncates the complete polyhedron
    CPARABL(2:12)=CPARAB(2:12)
    IF(VF0.GT.VFREF) THEN 
       DO I=NTP,1,-1
          IP=LISTV(I)
          IF(PHI(IP).GT.0.0_W_P) THEN
             X=VERTP(IP,1)-CPARAB(10)
             Y=VERTP(IP,2)-CPARAB(11)
             Z=VERTP(IP,3)-CPARAB(12)
             FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
             UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
             VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
             CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)*   &
                  UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
             CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF1,  &
                  XNS,YNS,ZNS)
             VF1=VF1/VT
             IF(ABS(VF1-VFREF).LT.TOLF) THEN
                C=CPARABL(1)
                RETURN
             END IF
             IF(VF1.LE.VFREF) THEN ! solution bracketted
                C1=CPARABL(1)
                GOTO 20
             END IF
          END IF
       END DO
    ELSE
       DO I=1,NTP
          IP=LISTV(I)
          IF(PHI(IP).LT.0.0_W_P) THEN
             X=VERTP(IP,1)-CPARAB(10)
             Y=VERTP(IP,2)-CPARAB(11)
             Z=VERTP(IP,3)-CPARAB(12)
             FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
             UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
             VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
             CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)*   &
                  UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
             CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF1,  &
                  XNS,YNS,ZNS)
             VF1=VF1/VT
             IF(ABS(VF1-VFREF).LT.TOLF) THEN
                C=CPARABL(1)
                RETURN
             END IF
             IF(VF1.GE.VFREF) THEN ! solution bracketted
                C1=CPARABL(1)
                GOTO 20
             END IF
          END IF
       END DO
    END IF
    DD=MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN)
    IF(VF0.GT.VFREF) THEN
       CPARABL(1)=CPARAB(1)+DD
    ELSE
       CPARABL(1)=CPARAB(1)-DD
    END IF
    CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF1,XNS,YNS,   &
         ZNS)
    VF1=VF1/VT
    IF(ABS(VF1-VFREF).LT.TOLF) THEN
       C=CPARABL(1)
       RETURN
    END IF
    IF((VF0-VFREF)*(VF1-VFREF).LT.0.0_W_P) THEN
       C1=CPARABL(1)
       GOTO 20
    END IF
    IE=1 ! the solution can not be bracketted
    RETURN
20  CONTINUE
    !IF(ABS(VF1-VFREF).LT.TOLF) THEN
    !   C=C1
    !   RETURN
    !END IF
    ! Init Brent's iteration
    DO ITER=1,NITER
       IF(ABS(C1-C0).LT.TOLC) THEN
          C=(C0+C1)/2.0_W_P
          RETURN
       END IF
       ! Secant interpolation
       DVF=-(VF0-VFREF)/(VF1-VF0)
       CI=C0*(1.0_W_P-DVF)+C1*DVF
       CPARABL(1)=CI
       CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFI,XNS,    &
            YNS,ZNS)
       VFI=VFI/VT
       IF(ABS(VFI-VFREF).LT.TOLF) THEN
          C=CI
          RETURN
       END IF
       IF((VFI-VFREF)/(VF0-VFREF).GT.1.0_W_P.OR.(VFI-VFREF)/(VF0-       &
            VFREF).GT.1.0_W_P) THEN
          ! Bisection
          CI=(C0+C1)/2.0_W_P
          CPARABL(1)=CI
          CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFI,     &
               XNS,YNS,ZNS)
          VFI=VFI/VT
          IF(ABS(VFI-VFREF).LT.TOLF) THEN
             C=CI
             RETURN
          END IF
       END IF
       ! Inverse-quadratic interpolation
       R=(VFI-VFREF)/(VF1-VFREF)
       S=(VFI-VFREF)/(VF0-VFREF)
       T=(VF0-VFREF)/(VF1-VFREF)
       Q=(T-1.0_W_P)*(R-1.0_W_P)*(S-1.0_W_P)
       IF(Q.EQ.0.0_W_P) THEN
          !. Bisection
          CI=(C0+C1)/2.0_W_P
          CPARABL(1)=CI
          CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFI,     &
               XNS,YNS,ZNS)
          VFI=VFI/VT
          IF(ABS(VFI-VFREF).LT.TOLF) THEN
             C=CPARABL(1)
             RETURN
          END IF
       ELSE
          P=S*(T*(R-T)*(C1-CI)-(1.0_W_P-R)*(CI-C0))
          CIQ=CI+P/Q
          CPARABL(1)=CIQ
          CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFIQ,    &
               XNS,YNS,ZNS)
          VFIQ=VFIQ/VT
          IF(ABS(VFIQ-VFREF).LT.TOLF) THEN
             C=CPARABL(1)
             RETURN
          END IF
          ! Check bracket
          D0=ABS(C0-CIQ)
          D1=ABS(C1-CIQ)
          D=ABS(C0-C1)
          IF(MAX(D0,D1).LT.(D*(1.0_W_P-1.0E-1_W_P))) THEN
             CI=CIQ
             VFI=VFIQ
          ELSE
             !. Bisection
             CI=(C0+C1)/2.0_W_P
             CPARABL(1)=CI
             CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFI,  &
                  XNS,YNS,ZNS)
             VFI=VFI/VT
             IF(ABS(VFI-VFREF).LT.TOLF) THEN
                C=CPARABL(1)
                RETURN
             END IF
          END IF
       END IF
!       IF(ABS(VFI-VFREF).LT.TOLF) THEN
!          C=CI
!          RETURN
!       END IF
       IF((VFI-VFREF)*(VF1-VFREF).GT.0.0_W_P) THEN
          C1=CI
          VF1=VFI
       ELSE
          C0=CI
          VF0=VFI
       END IF
    END DO
    IE=1 ! the solution is not found
    RETURN
  END SUBROUTINE ENFORVPPAOLD
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------|       
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              ENFORVPPAJCP                              | 
! The paraboloid is shifted to enforce discrete volume conservation   |
! VERSION DEL JCP  
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NC       = number of sub-cells along each coordinate axis of the    | 
!            superimposed Cartesian grid                              | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! V        = liquid volume                                            | 
! VT       = total volume of the polyhedron                           | 
! VERTP    = vertex coordinates of the polyhedron                     | 
! XNS, ... = unit-lenght normals to the faces of the polyhedron       | 
! On return:                                                          | 
!===========                                                          | 
! C        = solution of the problem                                  | 
! IE       = 0, if the root is found; 1, otherwise                    | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE ENFORVPPAJCP(C,CPARAB,IE,IPV,NC,NIPV,NTP,NTS,V,VT,VERTP,      &
       XNS,YNS,ZNS) BIND(C)        
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(OUT) :: C 
    REAL(W_P), INTENT(IN) :: V, VT 
    INTEGER(I_P), INTENT(OUT) :: IE 
    INTEGER(I_P), INTENT(IN) :: NC,NTP,NTS
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: CPARAB(12),VERTP(NV,3),XNS(NS),YNS(NS),    &
         ZNS(NS) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS)
    !.. Local Scalars
    INTEGER(I_P) :: I,II,IP,ITER,NITER,NTV
    REAL(W_P) :: C0,C1,CI,CIQ,DMOD,D,D0,D1,DD,DVF,FL,P,Q,R,S,T,TOLC,    &
         TOLF,UL,VL,VF,VF0,VF1,VFI,VFIQ,VFREF,X,XMAX,XMIN,Y,YMAX,YMIN,  &
         Z,ZMAX,ZMIN
    !.. Local Arrays      
    INTEGER(I_P) :: LISTV(NV) !list of ordered vertices
    REAL(W_P) :: CPARABL(12),PHI(NV),VN(9)
    IE=0
    NITER=100 ! Maximum number of Brent's iterations
    NTV=NTP !it's suppossed that the polyhedron hasn't been truncated
    TOLF=1.0E-10_W_P ! volume of fluid fraction tolerance
    TOLC=1.0E-16_W_P ! paraboloid location tolerance
    VFREF=V/VT
    ! Initial guess
    CALL INTPV3DPA(CPARAB,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF,XNS,YNS,     &
         ZNS)
    C0=CPARAB(1)
    VF0=VF/VT
    IF(ABS(VF0-VFREF).LT.TOLF) THEN
       C=C0
       RETURN
    END IF
    !Paraboloid orthonormal basis
    VN(1)=CPARAB(7) ! x-component of the shift vector
    VN(2)=CPARAB(8) ! y-component of the shift vector
    VN(3)=CPARAB(9) ! z-component of the shift vector
    VN(4)=VN(2)
    VN(5)=-VN(1)
    VN(6)=0.0_W_P
    DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
    IF(DMOD.NE.0.0_W_P) THEN
       VN(4)=VN(4)/DMOD
       VN(5)=VN(5)/DMOD
    ELSE
       VN(4)=VN(3)
       VN(5)=0.0_W_P
       VN(6)=-VN(1)
       DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
       VN(4)=VN(4)/DMOD
       VN(6)=VN(6)/DMOD
    END IF
    VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
    VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
    VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
    LISTV(1)=1
    XMAX=0.0_W_P
    XMIN=1.0E+20_W_P
    YMAX=0.0_W_P
    YMIN=1.0E+20_W_P
    ZMAX=0.0_W_P
    ZMIN=1.0E+20_W_P
    DO IP=1,NTP
       X=VERTP(IP,1)
       Y=VERTP(IP,2)
       Z=VERTP(IP,3)
       XMAX=MAX(XMAX,X)
       XMIN=MIN(XMIN,X)
       YMAX=MAX(YMAX,Y)
       YMIN=MIN(YMIN,Y)
       ZMAX=MAX(ZMAX,Z)
       ZMIN=MIN(ZMIN,Z)
       CALL PFUNC3D(PHI(IP),CPARAB,VN,X,Y,Z)
       !* Ordered list of global vertex indices                                
       DO I=1,IP-1 
          IF(PHI(IP).GT.PHI(LISTV(I))) THEN 
             DO II=IP,I+1,-1 
                LISTV(II)=LISTV(II-1) 
             END DO
             LISTV(I)=IP 
             GOTO 10 
          END IF
       END DO
       LISTV(IP)=IP
10     CONTINUE 
    END DO
    ! Solution bracketting.
    ! LISTV(1) --> gives the vertex IP through which the shifted
    !              paraboloid passes and truncates zero fluid volume
    ! LISTV(NTP)-> gives the vertex IP through which the shifted
    !              paraboloid passes and truncates the complete polyhedron
    CPARABL(2:12)=CPARAB(2:12)
    IF(VF0.GT.VFREF) THEN 
       DO I=NTP,1,-1
          IP=LISTV(I)
          IF(PHI(IP).GT.0.0_W_P) THEN
             X=VERTP(IP,1)-CPARAB(10)
             Y=VERTP(IP,2)-CPARAB(11)
             Z=VERTP(IP,3)-CPARAB(12)
             FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
             UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
             VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
             CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)*   &
                  UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
             CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF1,  &
                  XNS,YNS,ZNS)
             VF1=VF1/VT
             IF(VF1.LE.VFREF) THEN ! solution bracketted
                C1=CPARABL(1)
                GOTO 20
             END IF
          END IF
       END DO
    ELSE
       DO I=1,NTP
          IP=LISTV(I)
          IF(PHI(IP).LT.0.0_W_P) THEN
             X=VERTP(IP,1)-CPARAB(10)
             Y=VERTP(IP,2)-CPARAB(11)
             Z=VERTP(IP,3)-CPARAB(12)
             FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
             UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
             VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
             CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)*   &
                  UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
             CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF1,  &
                  XNS,YNS,ZNS)
             VF1=VF1/VT
             IF(VF1.GE.VFREF) THEN ! solution bracketted
                C1=CPARABL(1)
                GOTO 20
             END IF
          END IF
       END DO
    END IF
    DD=MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN)
    IF(VF0.GT.VFREF) THEN
       CPARABL(1)=CPARAB(1)+DD
    ELSE
       CPARABL(1)=CPARAB(1)-DD
    END IF
    CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF1,XNS,YNS,   &
         ZNS)
    VF1=VF1/VT
    IF((VF0-VFREF)*(VF1-VFREF).LT.0.0_W_P) THEN
       C1=CPARABL(1)
       GOTO 20
    END IF
    IE=1 ! the solution can not be bracketted
    RETURN
20  CONTINUE
    IF(ABS(VF1-VFREF).LT.TOLF) THEN
       C=C1
       RETURN
    END IF
    ! Init Brent's iteration
    DO ITER=1,NITER
       IF(ABS(C1-C0).LT.TOLC) THEN
          C=(C0+C1)/2.0_W_P
          RETURN
       END IF
       ! Secant interpolation
       DVF=-(VF0-VFREF)/(VF1-VF0)
       CI=C0*(1.0_W_P-DVF)+C1*DVF
       CPARABL(1)=CI
       CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFI,XNS,    &
            YNS,ZNS)
       VFI=VFI/VT
       IF(ABS(VFI-VFREF).LT.TOLF) THEN
          C=CI
          RETURN
       END IF
       IF((VFI-VFREF)/(VF0-VFREF).GT.1.0_W_P.OR.(VFI-VFREF)/(VF0-       &
            VFREF).GT.1.0_W_P) THEN
          ! Bisection
          CI=(C0+C1)/2.0_W_P
          CPARABL(1)=CI
          CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFI,     &
               XNS,YNS,ZNS)
          VFI=VFI/VT
          IF(ABS(VFI-VFREF).LT.TOLF) THEN
             C=CI
             RETURN
          END IF
       END IF
       ! Inverse-quadratic interpolation
       R=(VFI-VFREF)/(VF1-VFREF)
       S=(VFI-VFREF)/(VF0-VFREF)
       T=(VF0-VFREF)/(VF1-VFREF)
       Q=(T-1.0_W_P)*(R-1.0_W_P)*(S-1.0_W_P)
       IF(Q.EQ.0.0_W_P) THEN
          !. Bisection
          CI=(C0+C1)/2.0_W_P
          CPARABL(1)=CI
          CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFI,     &
               XNS,YNS,ZNS)
          VFI=VFI/VT
       ELSE
          P=S*(T*(R-T)*(C1-CI)-(1.0_W_P-R)*(CI-C0))
          CIQ=CI+P/Q
          CPARABL(1)=CIQ
          CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFIQ,    &
               XNS,YNS,ZNS)
          VFIQ=VFIQ/VT
          ! Check bracket
          D0=ABS(C0-CIQ)
          D1=ABS(C1-CIQ)
          D=ABS(C0-C1)
          IF(MAX(D0,D1).LT.(D*(1.0_W_P-1.0E-1_W_P))) THEN
             CI=CIQ
             VFI=VFIQ
          ELSE
             !. Bisection
             CI=(C0+C1)/2.0_W_P
             CPARABL(1)=CI
             CALL INTPV3DPA(CPARABL,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VFI,  &
                  XNS,YNS,ZNS)
             VFI=VFI/VT
          END IF
       END IF
       IF(ABS(VFI-VFREF).LT.TOLF) THEN
          C=CI
          RETURN
       END IF
       IF((VFI-VFREF)*(VF1-VFREF).GT.0.0_W_P) THEN
          C1=CI
          VF1=VFI
       ELSE
          C0=CI
          VF0=VFI
       END IF
    END DO
    IE=1 ! the solution is not found
    RETURN
  END SUBROUTINE ENFORVPPAJCP
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------|       
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              ENFORVPPA                              | 
! The paraboloid is shifted to enforce discrete volume conservation   | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NC       = number of sub-cells along each coordinate axis of the    | 
!            superimposed Cartesian grid                              | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! V        = liquid volume                                            | 
! VT       = total volume of the polyhedron                           | 
! VERTP    = vertex coordinates of the polyhedron                     | 
! XNS, ... = unit-lenght normals to the faces of the polyhedron       | 
! On return:                                                          | 
!===========                                                          | 
! C        = solution of the problem                                  | 
! IE       = 0, if the root is found; 1, otherwise                    | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE ENFORVPPAbrentold(C,CPARAB,IE,IPV,NC,NIPV,NTP,NTS,V,VT,VERTP,      &
       XNS,YNS,ZNS) BIND(C)        
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(OUT) :: C 
    REAL(W_P), INTENT(IN) :: V, VT 
    INTEGER(I_P), INTENT(OUT) :: IE 
    INTEGER(I_P), INTENT(IN) :: NC,NTP,NTS
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: CPARAB(12),VERTP(NV,3),XNS(NS),YNS(NS),    &
         ZNS(NS) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS)
    !.. Local Scalars
    INTEGER(I_P) :: I,IC,II,IP,ITER,JC,KC,NITER,NTV
    REAL(W_P) :: C0,C1,CI,CIQ,DMOD,D,D0,D1,DD,DVF,FL,P,Q,R,S,T,TOLC,    &
         TOLF,UL,VL,VF,VF0,VF1,VFI,VFIQ,VFREF,X,XMAX,XMIN,Y,YMAX,YMIN,  &
         Z,ZMAX,ZMIN
    !.. Local Arrays      
    INTEGER(I_P) :: LISTV(NV) !list of ordered vertices
    INTEGER(I_P) :: ITAGSC(NC,NC,NC),ITAGSC0(NC,NC,NC),ITAGSC1(NC,NC,NC)&
         ,ITAGSCI(NC,NC,NC)
                    !subcell tags:
                    !0, possibly intersected during iteration
                    !1, full
                    !2, empty
    REAL(W_P) :: CPARABL(12),PHI(NV),VN(9),VSC(NC,NC,NC),VSC0(NC,NC,NC),&
         VSC1(NC,NC,NC),VSCI(NC,NC,NC)
    IE=0
    NITER=100 ! Maximum number of Brent's iterations
    NTV=NTP !it's suppossed that the polyhedron hasn't been truncated
    TOLF=1.0E-10_W_P ! volume of fluid fraction tolerance
    TOLC=1.0E-16_W_P ! paraboloid location tolerance
    VFREF=V/VT
    ITAGSC(:,:,:)=0
    ITAGSC0(:,:,:)=0
    ITAGSC1(:,:,:)=0
    VSC(:,:,:)=0.0_W_P
    VSC0(:,:,:)=0.0_W_P
    VSC1(:,:,:)=0.0_W_P
    ! Initial guess
    CALL INTPPASC(CPARAB,IPV,ITAGSC0,NC,NIPV,NTP,NTS,NTV,VERTP,VF,VSC0, &
         XNS,YNS,ZNS)
    C0=CPARAB(1)
    VF0=VF/VT
    IF(ABS(VF0-VFREF).LT.TOLF) THEN
       C=C0
       RETURN
    END IF
    !Paraboloid orthonormal basis
    VN(1)=CPARAB(7) ! x-component of the shift vector
    VN(2)=CPARAB(8) ! y-component of the shift vector
    VN(3)=CPARAB(9) ! z-component of the shift vector
    VN(4)=VN(2)
    VN(5)=-VN(1)
    VN(6)=0.0_W_P
    DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
    IF(DMOD.NE.0.0_W_P) THEN
       VN(4)=VN(4)/DMOD
       VN(5)=VN(5)/DMOD
    ELSE
       VN(4)=VN(3)
       VN(5)=0.0_W_P
       VN(6)=-VN(1)
       DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
       VN(4)=VN(4)/DMOD
       VN(6)=VN(6)/DMOD
    END IF
    VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
    VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
    VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
    LISTV(1)=1
    XMAX=0.0_W_P
    XMIN=1.0E+20_W_P
    YMAX=0.0_W_P
    YMIN=1.0E+20_W_P
    ZMAX=0.0_W_P
    ZMIN=1.0E+20_W_P
    DO IP=1,NTP
       X=VERTP(IP,1)
       Y=VERTP(IP,2)
       Z=VERTP(IP,3)
       XMAX=MAX(XMAX,X)
       XMIN=MIN(XMIN,X)
       YMAX=MAX(YMAX,Y)
       YMIN=MIN(YMIN,Y)
       ZMAX=MAX(ZMAX,Z)
       ZMIN=MIN(ZMIN,Z)
       CALL PFUNC3D(PHI(IP),CPARAB,VN,X,Y,Z)
       !* Ordered list of global vertex indices                                
       DO I=1,IP-1 
          IF(PHI(IP).GT.PHI(LISTV(I))) THEN 
             DO II=IP,I+1,-1 
                LISTV(II)=LISTV(II-1) 
             END DO
             LISTV(I)=IP 
             GOTO 10 
          END IF
       END DO
       LISTV(IP)=IP
10     CONTINUE 
    END DO
    ! Solution bracketting.
    ! LISTV(1) --> gives the vertex IP through which the shifted
    !              paraboloid passes and truncates zero fluid volume
    ! LISTV(NTP)-> gives the vertex IP through which the shifted
    !              paraboloid passes and truncates the complete polyhedron
    CPARABL(2:12)=CPARAB(2:12)
    IF(VF0.GT.VFREF) THEN !initial paraboloid above the solution
       DO I=NTP,1,-1
          IP=LISTV(I)
          IF(PHI(IP).GT.0.0_W_P) THEN !begin at the first vertex just
                                      !below the initial paraboloid
             X=VERTP(IP,1)-CPARAB(10)
             Y=VERTP(IP,2)-CPARAB(11)
             Z=VERTP(IP,3)-CPARAB(12)
             FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
             UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
             VL=X*VN(7)+Y*VN(8)+Z*VN(9)
             CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)*   &
                  UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
             ITAGSC1(:,:,:)=0
             VSC1(:,:,:)=0.0_W_P
             CALL INTPPASC(CPARABL,IPV,ITAGSC1,NC,NIPV,NTP,NTS,NTV,     &
                  VERTP,VF1,VSC1,XNS,YNS,ZNS)
             VF1=VF1/VT
             IF(ABS(VF1-VFREF).LT.TOLF) THEN
                C=CPARABL(1)
                RETURN
             END IF
             IF(VF1.LE.VFREF) THEN ! solution bracketted
                C1=CPARABL(1)
                GOTO 20
             END IF
          END IF
       END DO
    ELSE !initial paraboloid below the solution
       DO I=1,NTP
          IP=LISTV(I)
          IF(PHI(IP).LT.0.0_W_P) THEN !begin at the first vertex just
                                      !above the initial paraboloid
             X=VERTP(IP,1)-CPARAB(10)
             Y=VERTP(IP,2)-CPARAB(11)
             Z=VERTP(IP,3)-CPARAB(12)
             FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
             UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
             VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
             CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)*   &
                  UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
             ITAGSC1(:,:,:)=0
             VSC1(:,:,:)=0.0_W_P
             CALL INTPPASC(CPARABL,IPV,ITAGSC1,NC,NIPV,NTP,NTS,NTV,     &
                  VERTP,VF1,VSC1,XNS,YNS,ZNS)
             VF1=VF1/VT
             IF(ABS(VF1-VFREF).LT.TOLF) THEN
                C=CPARABL(1)
                RETURN
             END IF
             IF(VF1.GE.VFREF) THEN ! solution bracketted
                C1=CPARABL(1)
                GOTO 20
             END IF
          END IF
       END DO
    END IF
    DD=MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN)
    IF(VF0.GT.VFREF) THEN
       CPARABL(1)=CPARAB(1)+DD
    ELSE
       CPARABL(1)=CPARAB(1)-DD
    END IF
    CALL INTPPASC(CPARABL,IPV,ITAGSC1,NC,NIPV,NTP,NTS,NTV,VERTP,VF1,    &
         VSC1,XNS,YNS,ZNS)
    VF1=VF1/VT
    IF(ABS(VF1-VFREF).LT.TOLF) THEN
       C=CPARABL(1)
       RETURN
    END IF
    IF((VF0-VFREF)*(VF1-VFREF).LT.0.0_W_P) THEN
       C1=CPARABL(1)
       GOTO 20
    END IF
    IE=1 ! the solution can not be bracketted
    RETURN
20  CONTINUE
!    IF(ABS(VF1-VFREF).LT.TOLF) THEN
!       C=C1
!       RETURN
!    END IF
    ! Init Brent's iteration
    DO ITER=1,NITER
       !update tags and volumes

       DO IC=1,NC
          DO JC=1,NC
             DO KC=1,NC
                IF(ITAGSC0(IC,JC,KC).EQ.ITAGSC1(IC,JC,KC)) THEN             
                   ITAGSC(IC,JC,KC)=ITAGSC0(IC,JC,KC)
                   VSC(IC,JC,KC)=VSC0(IC,JC,KC)
                END IF
             END DO
          END DO
       END DO
       IF(ABS(C1-C0).LT.TOLC) THEN
          C=(C0+C1)/2.0_W_P
          RETURN
       END IF
       ! Secant interpolation
       DVF=-(VF0-VFREF)/(VF1-VF0)
       CI=C0*(1.0_W_P-DVF)+C1*DVF
       CPARABL(1)=CI
       VSCI=VSC
       ITAGSCI=ITAGSC
       CALL INTPPASC(CPARABL,IPV,ITAGSCI,NC,NIPV,NTP,NTS,NTV,VERTP,VFI, &
            VSCI,XNS,YNS,ZNS)
       VFI=VFI/VT
       IF(ABS(VFI-VFREF).LT.TOLF) THEN
          C=CI
          RETURN
       END IF
       IF((VFI-VFREF)/(VF0-VFREF).GT.1.0_W_P.OR.(VFI-VFREF)/(VF0-       &
            VFREF).GT.1.0_W_P) THEN
          ! Bisection
          CI=(C0+C1)/2.0_W_P
          CPARABL(1)=CI
          VSCI=VSC
          ITAGSCI=ITAGSC
          CALL INTPPASC(CPARABL,IPV,ITAGSCI,NC,NIPV,NTP,NTS,NTV,VERTP,  &
               VFI,VSCI,XNS,YNS,ZNS)
          VFI=VFI/VT
          IF(ABS(VFI-VFREF).LT.TOLF) THEN
             C=CI
             RETURN
          END IF
       END IF
       ! Inverse-quadratic interpolation
       R=(VFI-VFREF)/(VF1-VFREF)
       S=(VFI-VFREF)/(VF0-VFREF)
       T=(VF0-VFREF)/(VF1-VFREF)
       Q=(T-1.0_W_P)*(R-1.0_W_P)*(S-1.0_W_P)
       IF(Q.EQ.0.0_W_P) THEN
          !. Bisection
          CI=(C0+C1)/2.0_W_P
          CPARABL(1)=CI
          VSCI=VSC
          ITAGSCI=ITAGSC
          CALL INTPPASC(CPARABL,IPV,ITAGSCI,NC,NIPV,NTP,NTS,NTV,VERTP,  &
               VFI,VSCI,XNS,YNS,ZNS)
          VFI=VFI/VT
          IF(ABS(VFI-VFREF).LT.TOLF) THEN
             C=CPARABL(1)
             RETURN
          END IF
       ELSE
          P=S*(T*(R-T)*(C1-CI)-(1.0_W_P-R)*(CI-C0))
          CIQ=CI+P/Q
          CPARABL(1)=CIQ
          VSCI=VSC
          ITAGSCI=ITAGSC
          CALL INTPPASC(CPARABL,IPV,ITAGSCI,NC,NIPV,NTP,NTS,NTV,VERTP,  &
               VFIQ,VSCI,XNS,YNS,ZNS)
          VFIQ=VFIQ/VT
          IF(ABS(VFIQ-VFREF).LT.TOLF) THEN
             C=CPARABL(1)
             RETURN
          END IF
          ! Check bracket
          D0=ABS(C0-CIQ)
          D1=ABS(C1-CIQ)
          D=ABS(C0-C1)
          IF(MAX(D0,D1).LT.(D*(1.0_W_P-1.0E-1_W_P))) THEN
             CI=CIQ
             VFI=VFIQ
          ELSE
             !. Bisection
             CI=(C0+C1)/2.0_W_P
             CPARABL(1)=CI
             VSCI=VSC
             ITAGSCI=ITAGSC
             CALL INTPPASC(CPARABL,IPV,ITAGSCI,NC,NIPV,NTP,NTS,NTV,     &
                  VERTP,VFI,VSCI,XNS,YNS,ZNS)
             VFI=VFI/VT
             IF(ABS(VFI-VFREF).LT.TOLF) THEN
                C=CPARABL(1)
                RETURN
             END IF
          END IF
       END IF
!       IF(ABS(VFI-VFREF).LT.TOLF) THEN
!          C=CI
!          RETURN
!       END IF
       IF((VFI-VFREF)*(VF1-VFREF).GT.0.0_W_P) THEN
          C1=CI
          VF1=VFI
          VSC1=VSCI
          ITAGSC1=ITAGSCI
       ELSE
          C0=CI
          VF0=VFI
          VSC0=VSCI
          ITAGSC0=ITAGSCI
       END IF
    END DO
    IE=1 ! the solution is not found
    RETURN
  END SUBROUTINE ENFORVPPAbrentold
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------|
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              ENFORVPPA                              | 
! The paraboloid is shifted to enforce discrete volume conservation   | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NC       = number of sub-cells along each coordinate axis of the    | 
!            superimposed Cartesian grid                              | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! V        = liquid volume                                            | 
! VT       = total volume of the polyhedron                           | 
! VERTP    = vertex coordinates of the polyhedron                     | 
! XNS, ... = unit-lenght normals to the faces of the polyhedron       | 
! On return:                                                          | 
!===========                                                          | 
! C        = solution of the problem                                  | 
! IE       = 0, if the root is found; 1, otherwise                    | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE ENFORVPPA(C,CPARAB,IE,IPV,NC,NIPV,NTP,NTS,V,VT,VERTP,      &
       XNS,YNS,ZNS) BIND(C)        
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(OUT) :: C 
    REAL(W_P), INTENT(IN) :: V, VT 
    INTEGER(I_P), INTENT(OUT) :: IE 
    INTEGER(I_P), INTENT(IN) :: NC,NTP,NTS
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: CPARAB(12),VERTP(NV,3),XNS(NS),YNS(NS),    &
         ZNS(NS) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS)
    !.. Local Scalars
    INTEGER(I_P) :: I,IC,II,IP,ITER,JC,KC,NITER,NTV
    REAL(W_P) :: C0,C1,CA,CB,CC,CD,CE,CI,DMOD,DD,EPS,FCA,FCB,FCC,FL,P,Q,&
         R,S,TOL,TOL1,TOLC,TOLF,UL,VL,VF,VF0,VF1,VFI,VFREF,X,XM,XMAX,   &
         XMIN,Y,YMAX,YMIN,Z,ZMAX,ZMIN
    !.. Local Arrays      
    INTEGER(I_P) :: LISTV(NV) !list of ordered vertices
    INTEGER(I_P) :: ITAGSC(NC,NC,NC),ITAGSC0(NC,NC,NC),ITAGSC1(NC,NC,NC)
                    !subcell tags:
                    !0, possibly intersected during iteration
                    !1, full
                    !2, empty
    REAL(W_P) :: CPARABL(12),PHI(NV),VN(9),VSC(NC,NC,NC),VSC0(NC,NC,NC),&
         VSC1(NC,NC,NC)
    IE=0
    NITER=100 ! Maximum number of Brent's iterations
    NTV=NTP !it's suppossed that the polyhedron hasn't been truncated
    TOLF=1.0E-10_W_P ! volume of fluid fraction tolerance
    TOLC=1.0E-16_W_P ! paraboloid location tolerance
    VFREF=V/VT
    ITAGSC(:,:,:)=0
    ITAGSC0(:,:,:)=0
    ITAGSC1(:,:,:)=0
    VSC(:,:,:)=0.0_W_P
    VSC0(:,:,:)=0.0_W_P
    VSC1(:,:,:)=0.0_W_P
    ! Initial guess
    CALL INTPPASC(CPARAB,IPV,ITAGSC0,NC,NIPV,NTP,NTS,NTV,VERTP,VF,VSC0, &
         XNS,YNS,ZNS)
    C0=CPARAB(1)
    VF0=VF/VT
    IF(ABS(VF0-VFREF).LT.TOLF) THEN !force exit
       C=C0
       RETURN
    END IF
    !Paraboloid orthonormal basis
    VN(1)=CPARAB(7) ! x-component of the shift vector
    VN(2)=CPARAB(8) ! y-component of the shift vector
    VN(3)=CPARAB(9) ! z-component of the shift vector
    VN(4)=VN(2)
    VN(5)=-VN(1)
    VN(6)=0.0_W_P
    DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
    IF(DMOD.NE.0.0_W_P) THEN
       VN(4)=VN(4)/DMOD
       VN(5)=VN(5)/DMOD
    ELSE
       VN(4)=VN(3)
       VN(5)=0.0_W_P
       VN(6)=-VN(1)
       DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
       VN(4)=VN(4)/DMOD
       VN(6)=VN(6)/DMOD
    END IF
    VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
    VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
    VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
    LISTV(1)=1
    XMAX=0.0_W_P
    XMIN=1.0E+20_W_P
    YMAX=0.0_W_P
    YMIN=1.0E+20_W_P
    ZMAX=0.0_W_P
    ZMIN=1.0E+20_W_P
    DO IP=1,NTP
       X=VERTP(IP,1)
       Y=VERTP(IP,2)
       Z=VERTP(IP,3)
       XMAX=MAX(XMAX,X)
       XMIN=MIN(XMIN,X)
       YMAX=MAX(YMAX,Y)
       YMIN=MIN(YMIN,Y)
       ZMAX=MAX(ZMAX,Z)
       ZMIN=MIN(ZMIN,Z)
       CALL PFUNC3D(PHI(IP),CPARAB,VN,X,Y,Z)
       !* Ordered list of global vertex indices                                
       DO I=1,IP-1 
          IF(PHI(IP).GT.PHI(LISTV(I))) THEN 
             DO II=IP,I+1,-1 
                LISTV(II)=LISTV(II-1) 
             END DO
             LISTV(I)=IP 
             GOTO 10 
          END IF
       END DO
       LISTV(IP)=IP
10     CONTINUE 
    END DO
    ! Solution bracketting.
    ! LISTV(1) --> gives the vertex IP through which the shifted
    !              paraboloid passes and truncates zero fluid volume
    ! LISTV(NTP)-> gives the vertex IP through which the shifted
    !              paraboloid passes and truncates the complete polyhedron
    CPARABL(2:12)=CPARAB(2:12)
    IF(VF0.GT.VFREF) THEN !initial paraboloid above the solution
       DO I=NTP,1,-1
          IP=LISTV(I)
          IF(PHI(IP).GT.0.0_W_P) THEN !begin at the first vertex just
                                      !below the initial paraboloid
             X=VERTP(IP,1)-CPARAB(10)
             Y=VERTP(IP,2)-CPARAB(11)
             Z=VERTP(IP,3)-CPARAB(12)
             FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
             UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
             VL=X*VN(7)+Y*VN(8)+Z*VN(9)
             CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)*   &
                  UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
             ITAGSC1(:,:,:)=0
             VSC1(:,:,:)=0.0_W_P
             !update tags and volumes
             DO IC=1,NC
                DO JC=1,NC
                   DO KC=1,NC
                      IF(ITAGSC0(IC,JC,KC).EQ.2) THEN
                         ITAGSC1(IC,JC,KC)=ITAGSC0(IC,JC,KC)
                         VSC1(IC,JC,KC)=VSC0(IC,JC,KC)
                      END IF
                   END DO
                END DO
             END DO
             CALL INTPPASC(CPARABL,IPV,ITAGSC1,NC,NIPV,NTP,NTS,NTV,     &
                  VERTP,VF1,VSC1,XNS,YNS,ZNS)
             VF1=VF1/VT
             IF(ABS(VF1-VFREF).LT.TOLF) THEN
                C=CPARABL(1)
                RETURN
             END IF
             IF(VF1.LE.VFREF) THEN ! solution bracketted
                C1=CPARABL(1)
                GOTO 20
             END IF
          END IF
       END DO
    ELSE !initial paraboloid below the solution
       DO I=1,NTP
          IP=LISTV(I)
          IF(PHI(IP).LT.0.0_W_P) THEN !begin at the first vertex just
                                      !above the initial paraboloid
             X=VERTP(IP,1)-CPARAB(10)
             Y=VERTP(IP,2)-CPARAB(11)
             Z=VERTP(IP,3)-CPARAB(12)
             FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
             UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
             VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
             CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)*   &
                  UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
             ITAGSC1(:,:,:)=0
             VSC1(:,:,:)=0.0_W_P
             !update tags and volumes
             DO IC=1,NC
                DO JC=1,NC
                   DO KC=1,NC
                      IF(ITAGSC0(IC,JC,KC).EQ.1) THEN
                         ITAGSC1(IC,JC,KC)=ITAGSC0(IC,JC,KC)
                         VSC1(IC,JC,KC)=VSC0(IC,JC,KC)
                      END IF
                   END DO
                END DO
             END DO
             CALL INTPPASC(CPARABL,IPV,ITAGSC1,NC,NIPV,NTP,NTS,NTV,     &
                  VERTP,VF1,VSC1,XNS,YNS,ZNS)
             VF1=VF1/VT
             IF(ABS(VF1-VFREF).LT.TOLF) THEN !force exit
                C=CPARABL(1)
                RETURN
             END IF
             IF(VF1.GE.VFREF) THEN ! solution bracketted
                C1=CPARABL(1)
                GOTO 20
             END IF
          END IF
       END DO
    END IF
    DD=MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN)
    ITAGSC1(:,:,:)=0
    VSC1(:,:,:)=0.0_W_P
    IF(VF0.GT.VFREF) THEN
       CPARABL(1)=CPARAB(1)+DD
       !update tags and volumes
       DO IC=1,NC
          DO JC=1,NC
             DO KC=1,NC
                IF(ITAGSC0(IC,JC,KC).EQ.2) THEN
                   ITAGSC1(IC,JC,KC)=ITAGSC0(IC,JC,KC)
                   VSC1(IC,JC,KC)=VSC0(IC,JC,KC)
                END IF
             END DO
          END DO
       END DO
    ELSE
       CPARABL(1)=CPARAB(1)-DD
       !update tags and volumes
       DO IC=1,NC
          DO JC=1,NC
             DO KC=1,NC
                IF(ITAGSC0(IC,JC,KC).EQ.1) THEN
                   ITAGSC1(IC,JC,KC)=ITAGSC0(IC,JC,KC)
                   VSC1(IC,JC,KC)=VSC0(IC,JC,KC)
                END IF
             END DO
          END DO
       END DO
    END IF
    CALL INTPPASC(CPARABL,IPV,ITAGSC1,NC,NIPV,NTP,NTS,NTV,VERTP,VF1,    &
         VSC1,XNS,YNS,ZNS)
    VF1=VF1/VT
    IF(ABS(VF1-VFREF).LT.TOLF) THEN
       C=CPARABL(1)
       RETURN
    END IF
    IF((VF0-VFREF)*(VF1-VFREF).LT.0.0_W_P) THEN
       C1=CPARABL(1)
       GOTO 20
    END IF
    IE=1 ! the solution can not be bracketted
    RETURN
20  CONTINUE
!------
    IF(ABS(VF0-VFREF).LT.ABS(VF1-VFREF)) THEN
       VFI=VF0
       VF0=VF1
       VF1=VFI
       CI=C0
       C0=C1
       C1=CI
!       ITAGSCI=ITAGSC0
!       ITAGSC0=ITAGSC1
!       ITAGSC1=ITAGSCI
!       VSCI=VSC0
!       VSC0=VSC1
!       VSC1=VSCI
    END IF
!------    
    EPS=EPSILON(C0)
    TOL=1.0E-12_W_P
    CA=C0
    CB=C1
    FCA=VF0-VFREF
    FCB=VF1-VFREF
    CC=CB
    FCC=FCB
    !update tags and volumes
    DO IC=1,NC
       DO JC=1,NC
          DO KC=1,NC
             IF(ITAGSC0(IC,JC,KC).EQ.ITAGSC1(IC,JC,KC)) THEN
                ITAGSC(IC,JC,KC)=ITAGSC0(IC,JC,KC)
                VSC(IC,JC,KC)=VSC0(IC,JC,KC)
             END IF
          END DO
       END DO
    END DO
    DO ITER=1,NITER
       IF(ABS(CA-CB).LT.TOLC) THEN !forze exit
          C=(CA+CB)/2.0_W_P
          RETURN
       END IF
       
       IF((FCB.GT.0.0_W_P.AND.FCC.GT.0.0_W_P).OR.(FCB.LT.0.0_W_P.AND.   &
            FCC.LT.0.0_W_P)) THEN
          CC=CA
          FCC=FCA
          CD=CB-CA
          CE=CD
       END IF
       IF(ABS(FCC).LT.ABS(FCB)) THEN
          CA=CB
          CB=CC
          CC=CA
          FCA=FCB
          FCB=FCC
          FCC=FCA
!          ITAGSCI=ITAGSC0
!          ITAGSC0=ITAGSC1
!          ITAGSC1=ITAGSCI
!          VSCI=VSC0
!          VSC0=VSC1
!          VSC1=VSCI
       END IF
       
       TOL1=2.0_W_P*EPS*ABS(CB)+0.5_W_P*TOL
       !write(6,*)'tol1:',tol1
       XM=0.5_W_P*(CC-CB)
       IF(ABS(XM).LE.TOL1.OR.FCB.EQ.0.0_W_P) THEN
        C=CB
        RETURN
     END IF
     IF(ABS(CE).GE.TOL1.AND.ABS(FCA).GT.ABS(FCB)) THEN
        S=FCB/FCA
        IF (CA.EQ.CC) THEN
           P=2.0_W_P*XM*S
           Q=1.0_W_P-S
        ELSE
           Q=FCA/FCC
           R=FCB/FCC
           P=S*(2.0_W_P*XM*Q*(Q-R)-(CB-CA)*(R-1.0_W_P))
           Q=(Q-1.0_W_P)*(R-1.0_W_P)*(S-1.0_W_P)
        END IF
        IF (P.GT.0.0_W_P) Q=-Q
        P=ABS(P)
        IF (2.0_W_P*P.LT.MIN(3.0_W_P*XM*Q-ABS(TOL1*Q),ABS(CE*Q))) THEN
           CE=CD
           CD=P/Q
        ELSE
           CD=XM
           CE=CD
        END IF
     ELSE
        CD=XM
        CE=CD
     END IF
     CA=CB
     FCA=FCB
     CB=CB+MERGE(CD,SIGN(TOL1,XM),ABS(CD).GT.TOL1)
     !FCB=func(CB)
     CPARABL(1)=CB
     VSC1=VSC
     ITAGSC1=ITAGSC
     CALL INTPPASC(CPARABL,IPV,ITAGSC1,NC,NIPV,NTP,NTS,NTV,VERTP,VF1,    &
          VSC1,XNS,YNS,ZNS)
     FCB=VF1/VT-VFREF
  END DO
  WRITE(6,*)'BRENTSOL: EXCEEDED MAXIMUM ITERATIONS'
  C=CB
  IE=1 ! the solution is not found
  RETURN
END SUBROUTINE ENFORVPPA
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------|
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                             INTPPASC                                | 
! Volume of the polyhedral approximation of the region of intersection|
! between a paraboloid and an arbitrary polyhedron                    |
! This version uses tagged subcells with previous computed volumes    |  
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! IPV      = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! ITAGSC   = subcell pre-tags:                                        |
!            0, possibly intersected during iteration                 |
!            1, full                                                  |
!            2, empty                                                 |
! NC       = number of sub-cells along each coordinate axis of the    | 
!            superimposed Cartesian grid                              | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = vertex coordinates of the original polyhedron            | 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  | 
! On return:                                                          | 
!===========                                                          | 
! VF       = volume of intersection                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INTPPASC(CPARAB,IPV,ITAGSC,NC,NIPV,NTP,NTS,NTV,VERTP,VF,   &
       VSC,XNS,YNS,ZNS) BIND(C)                                         
    !.. Scalar Arguments                                                    
    REAL (W_P), INTENT(IN) :: CPARAB(12)
    REAL(W_P), INTENT(OUT) :: VF 
    INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS)
    INTEGER(I_P), INTENT(INOUT) :: ITAGSC(NC,NC,NC)
    REAL(W_P), INTENT(INOUT) :: VSC(NC,NC,NC)
    !.. Local Scalars                                                       
    REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DMOD,DVP,DVPMAX,DVPMIN,DX,DY,DZ,&
         SUMX,SUMY,SUMZ,TOLPHI,VOLF,X,XM,XMAX,XMAX2,XMIN,XMIN2,XP,   &
         XV1,XV2,Y,YM,YMAX,YMAX2,YMIN,YMIN2,YP,YV1,YV2,Z,ZM,ZMAX, &
         ZMAX2,ZMIN,ZMIN2,ZP,ZV1,ZV2
    INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IEBRACKET,IP,                    &
         IP0,IP1,IS,IS2,ISINI,IV,IV2,JC,KC,                             &
         NCL,NTP0,NTP1,NTP2,NTPT,                                       &
         NTS0,NTS1,NTS2,NTST,NTSINI,NTV0,NTV1,NTV2,NTVT                
    !LOGICAL :: ICONVEX
    !.. Local Arrays                                                        
    REAL(W_P) :: CI1(NC),CI2(NC),CJ1(NC),CJ2(NC),CK1(NC),CK2(NC),       &
         CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC),CX2(NC),        &
         CY1(NC),CY2(NC),CZ1(NC),CZ2(NC),PHIV(NV),PHIVMIN(NS),V(8,3),   &
         V0(3),V1(3),VI(3),VNI(3),VNJ(3),VNK(3),VERTP0(NV,3),           &
         VERTP1(NV,3),VERTP2(NV,3),VERTPT(NV,3),VN(9),XNS0(NS),         &
         XNS1(NS),XNS2(NS),XNST(NS),YNS0(NS),YNS1(NS),YNS2(NS),         &
         YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),ZNST(NS)         
    INTEGER(I_P) :: IA(NV),ICHECK(NV),ICTAG(NC),IJKCLIM(6),IPIA0(NV),             &
         IPIA1(NV),IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),     &
         ISCONTN(NS),ISCONTP(NS),ISCUT(NS),ITAGP(NC,NC,NC),ITAGP2(NC,NC,NC),JCTAG(NC,NC),NIPV0(NS),   &
         NIPV1(NS),NIPV2(NS),NIPVT(NS)
    !REAL(W_P) :: DC,DCMAX,DCMIN,DCP,DF,DVF,DVFMAX,DVFMIN,R,XC,YC,ZC
    TOLPHI=1.0E-16_W_P
    !.. Coordinate extremes of the cell and vertex tagging                  
    NCL=NC 
    VF=0.0_W_P 
    XMIN=1.0E+20_W_P 
    XMAX=-1.0E+20_W_P 
    YMIN=1.0E+20_W_P 
    YMAX=-1.0E+20_W_P 
    ZMIN=1.0E+20_W_P 
    ZMAX=-1.0E+20_W_P 
    ICONTP=0 
    ICONTN=0 
    V0(1)=0.0_W_P 
    V0(2)=0.0_W_P 
    V0(3)=0.0_W_P 
    DO IP=1,NTP 
       ICHECK(IP)=0 
    END DO
    !Paraboloid orthonormal basis
    VN(1)=CPARAB(7) 
    VN(2)=CPARAB(8) 
    VN(3)=CPARAB(9) 
    VN(4)=VN(2)
    VN(5)=-VN(1)
    VN(6)=0.0_W_P
    DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
    IF(DMOD.NE.0.0_W_P) THEN
       VN(4)=VN(4)/DMOD
       VN(5)=VN(5)/DMOD
    ELSE
       VN(4)=VN(3)
       VN(5)=0.0_W_P
       VN(6)=-VN(1)
       DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
       VN(4)=VN(4)/DMOD
       VN(6)=VN(6)/DMOD
    END IF
    VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
    VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
    VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
    
    DO IS=1,NTS
       ISCONTP(IS)=0
       ISCONTN(IS)=0
       PHIVMIN(IS)=1.0E+20_W_P
       CS(IS)=-XNS(IS)*VERTP(IPV(IS,1),1)-YNS(IS)*VERTP(IPV(IS,1),2)    &
            -ZNS(IS)*VERTP(IPV(IS,1),3)
       DO IV=1,NIPV(IS) 
          IP=IPV(IS,IV) 
          IF(ICHECK(IP).EQ.0) THEN 
             ICHECK(IP)=1 
             XP=VERTP(IP,1) 
             YP=VERTP(IP,2) 
             ZP=VERTP(IP,3) 
             XMIN=DMIN1(XMIN,XP) 
             XMAX=DMAX1(XMAX,XP) 
             YMIN=DMIN1(YMIN,YP) 
             YMAX=DMAX1(YMAX,YP) 
             ZMIN=DMIN1(ZMIN,ZP) 
             ZMAX=DMAX1(ZMAX,ZP)
             IF(NC.EQ.1) THEN
                CALL PFUNC3D(PHIV(IP),CPARAB,VN,XP,YP,ZP)
                IF(PHIV(IP).GT.0.0_W_P) THEN 
                   IA(IP)=1 
                   ICONTP=ICONTP+1 
                ELSE 
                   IA(IP)=0 
                   ICONTN=ICONTN+1 
                END IF
             END IF
          END IF
       END DO
    END DO
    !.. initialization                                                      
    DX=XMAX-XMIN 
    DY=YMAX-YMIN 
    DZ=ZMAX-ZMIN 
    DD=0.01*MIN(DX,DY,DZ)
    IF(DD.LT.1.0E-20_W_P) THEN
       VF=0.0_W_P 
       RETURN 
    END IF
    CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,NTS,NTVT,     &
         NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)
    DDX=DX/REAL(NCL,KIND=W_P) 
    DDY=DY/REAL(NCL,KIND=W_P) 
    DDZ=DZ/REAL(NCL,KIND=W_P) 
    DO I=1,NCL 
       IF(I.EQ.1) THEN 
          CX1(I)=-XMIN 
       ELSE 
          CX1(I)=CX1(I-1)-DDX 
       END IF
       CX2(I)=-CX1(I)+DDX 
    END DO
    DO I=1,NCL 
       IF(I.EQ.1) THEN 
          CY1(I)=-YMIN 
       ELSE 
          CY1(I)=CY1(I-1)-DDY 
       END IF
       CY2(I)=-CY1(I)+DDY 
    END DO
    DO I=1,NCL 
       IF(I.EQ.1) THEN 
          CZ1(I)=-ZMIN 
       ELSE 
          CZ1(I)=CZ1(I-1)-DDZ 
       END IF
       CZ2(I)=-CZ1(I)+DDZ 
    END DO
    IJKCLIM(1)=1
    IJKCLIM(2)=NCL
    IJKCLIM(3)=1
    IJKCLIM(4)=NCL
    IJKCLIM(5)=1
    IJKCLIM(6)=NCL
    VNI(:)=[1.0_W_P,0.0_W_P,0.0_W_P]
    VNJ(:)=[0.0_W_P,1.0_W_P,0.0_W_P]
    VNK(:)=[0.0_W_P,0.0_W_P,1.0_W_P]
    CI1(:)=CX1(:)
    CI2(:)=CX2(:)
    CJ1(:)=CY1(:)
    CJ2(:)=CY2(:)
    CK1(:)=CZ1(:)
    CK2(:)=CZ2(:)

    !sub-cell tagging:
    ITAGP(IJKCLIM(1):IJKCLIM(2),IJKCLIM(3):IJKCLIM(4),IJKCLIM(5):       &
         IJKCLIM(6))=0
    ITAGP2(IJKCLIM(1):IJKCLIM(2),IJKCLIM(3):IJKCLIM(4),IJKCLIM(5):       &
         IJKCLIM(6))=0
!    R=0.866025403784_W_P*MAX(DDX,DDY,DDZ) !circunscrit ball radius (smallest
!                                          !sphere that contains all the Pijk
!                                          !vertices)
!    DO IC=IJKCLIM(1),IJKCLIM(2) 
!       DO JC=IJKCLIM(3),IJKCLIM(4) 
!          DO KC=IJKCLIM(5),IJKCLIM(6)
!             !circunscrit ball center
!             XC=XMIN+DDX*(REAL(IC,KIND=W_P)-0.5_W_P)
!             YC=YMIN+DDY*(REAL(JC,KIND=W_P)-0.5_W_P)
!             ZC=ZMIN+DDZ*(REAL(KC,KIND=W_P)-0.5_W_P)
!             CALL PFUNC3D(DC,CPARAB,VN,XC,YC,ZC)
!             DCMIN=1.0E+20_W_P
!             DO IS=1,NTS
!                DF=XNS(IS)*XC+YNS(IS)*YC+ZNS(IS)*ZC+CS(IS)
!                !                   IF(ICONVEX.AND.DF.GE.R) THEN
!                !                      ITAGP(IC,JC,KC)=2
!                !                      GOTO 10
!                !                   END IF
!                DCMIN=MIN(DCMIN,DF)
!             END DO
!             IF(DC.GE.R.AND.DCMIN.GE.R) THEN
!                ITAGP(IC,JC,KC)=1
!                GOTO 10
!             END IF
!             IF(DC.LE.-R.AND.DCMIN.GE.R) THEN
!                ITAGP(IC,JC,KC)=2
!                GOTO 10
!             END IF
!10           CONTINUE
!          END DO
!       END DO
!    END DO

    !assign subcell pre-tags:
    ITAGP=ITAGSC
    DO IC=IJKCLIM(1),IJKCLIM(2) 
       DO JC=IJKCLIM(3),IJKCLIM(4) 
          DO KC=IJKCLIM(5),IJKCLIM(6)
             IF(ITAGP(IC,JC,KC).EQ.0) THEN
                V(1,:)=[XMAX+DDX*REAL(IC-NCL,KIND=W_P),YMIN+DDY*REAL(JC-1, &
                     KIND=W_P),ZMAX+DDZ*REAL(KC-NCL,KIND=W_P)]
                V(2,:)=[XMAX+DDX*REAL(IC-NCL,KIND=W_P),YMIN+DDY*REAL(JC-1, &
                     KIND=W_P),ZMIN+DDZ*REAL(KC-1,KIND=W_P)]
                V(3,:)=[XMAX+DDX*REAL(IC-NCL,KIND=W_P),YMAX+DDY*REAL(JC-NCL&
                     ,KIND=W_P),ZMIN+DDZ*REAL(KC-1,KIND=W_P)]
                V(4,:)=[XMAX+DDX*REAL(IC-NCL,KIND=W_P),YMAX+DDY*REAL(JC-NCL&
                     ,KIND=W_P),ZMAX+DDZ*REAL(KC-NCL,KIND=W_P)]
                V(5,:)=[XMIN+DDX*REAL(IC-1,KIND=W_P),YMIN+DDY*REAL(JC-1,   &
                     KIND=W_P),ZMAX+DDZ*REAL(KC-NCL,KIND=W_P)]
                V(6,:)=[XMIN+DDX*REAL(IC-1,KIND=W_P),YMIN+DDY*REAL(JC-1,   &
                     KIND=W_P),ZMIN+DDZ*REAL(KC-1,KIND=W_P)]
                V(7,:)=[XMIN+DDX*REAL(IC-1,KIND=W_P),YMAX+DDY*REAL(JC-NCL, &
                     KIND=W_P),ZMIN+DDZ*REAL(KC-1,KIND=W_P)]
                V(8,:)=[XMIN+DDX*REAL(IC-1,KIND=W_P),YMAX+DDY*REAL(JC-NCL, &
                     KIND=W_P),ZMAX+DDZ*REAL(KC-NCL,KIND=W_P)]
                DVPMIN=1.0E+20_W_P
                DVPMAX=-1.0E+20_W_P
                DO IV=1,8
                   CALL PFUNC3D(DVP,CPARAB,VN,V(IV,1),V(IV,2),V(IV,3))
                   DVPMAX=MAX(DVPMAX,DVP)
                   DVPMIN=MIN(DVPMIN,DVP)
                END DO
                IF(DVPMAX.LE.0.0_W_P) THEN
                   ITAGP(IC,JC,KC)=2
                   ITAGSC(IC,JC,KC)=2
                ELSEIF(DVPMIN.GE.0.0_W_P) THEN
                   ITAGP2(IC,JC,KC)=1
                   ITAGSC(IC,JC,KC)=1
                   DO IV=1,8
                      DO IS=1,NTS
                         IF((XNS(IS)*V(IV,1)+YNS(IS)*V(IV,2)+ZNS(IS)*      &
                              V(IV,3)+CS(IS)).GT.0.0_W_P) GOTO 20
                      END DO
                   END DO
                   ITAGP(IC,JC,KC)=1
                   VSC(IC,JC,KC)=DDX*DDY*DDZ
20                 CONTINUE
                END IF
             END IF
          END DO
       END DO
    END DO
    ICTAG(:)=0
    JCTAG(:,:)=0
    DO IC=IJKCLIM(1),IJKCLIM(2)
       IF(PRODUCT(ITAGP(IC,:,:)).NE.0) THEN
          IF(SUM(ITAGP(IC,:,:)).EQ.NCL*NCL) THEN
             !DO JC=IJKCLIM(3),IJKCLIM(4)
             !   DO KC=IJKCLIM(5),IJKCLIM(6)
             !      IF(ITAGSC(IC,JC,KC).EQ.0) THEN
             !         VSC(IC,JC,KC)=DDX*DDY*DDZ
             !         ITAGSC(IC,JC,KC)=1
             !      END IF
             !   END DO
             !END DO
             ICTAG(IC)=1
             GOTO 25
          END IF
          IF(SUM(ITAGP(IC,:,:)).EQ.2*NCL*NCL) THEN
             ICTAG(IC)=2
             !ITAGSC(IC,:,:)=2
             GOTO 25
          END IF
       END IF
       DO JC=IJKCLIM(3),IJKCLIM(4) 
          IF(PRODUCT(ITAGP(IC,JC,:)).NE.0) THEN
             IF(SUM(ITAGP(IC,JC,:)).EQ.NCL) THEN
                JCTAG(IC,JC)=1
                !DO KC=IJKCLIM(5),IJKCLIM(6)
                !   IF(ITAGSC(IC,JC,KC).EQ.0) THEN
                !      VSC(IC,JC,KC)=DDX*DDY*DDZ
                !      ITAGSC(IC,JC,KC)=1
                !   END IF
                !END DO
             ELSEIF(SUM(ITAGP(IC,JC,:)).EQ.2*NCL) THEN
                JCTAG(IC,JC)=2
                !ITAGSC(IC,JC,:)=2
             END IF
          END IF
       END DO
25     CONTINUE
    END DO             
    !check subcell tags and update VF
    DO IC=IJKCLIM(1),IJKCLIM(2)
       DO JC=IJKCLIM(3),IJKCLIM(4)
          DO KC=IJKCLIM(5),IJKCLIM(6)
             IF(ITAGP(IC,JC,KC).EQ.1) VF=VF+VSC(IC,JC,KC)
          END DO
       END DO
    END DO
    
    DO IC=IJKCLIM(1),IJKCLIM(2)
       IF(ICTAG(IC).NE.0) GOTO 30
       IF(NCL.EQ.1) THEN 
          CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,    &
               NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,        &
               ZNS0,ZNST)                                                  
       ELSE 
          CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,    &
               NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,        &
               ZNS2,ZNST)                                                  
       END IF
       IF(IC.GT.1) CALL INTE3D(CI1(IC),ICONTN,ICONTP,IPV2,NIPV2,        &
            NTP2,NTS2,NTV2,VERTP2,VNI(1),XNS2,VNI(2),YNS2,VNI(3),ZNS2)        
       IF(IC.LT.NCL) CALL INTE3D(CI2(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
            NTS2,NTV2,VERTP2,-VNI(1),XNS2,-VNI(2),YNS2,-VNI(3),ZNS2)  
       DO JC=IJKCLIM(3),IJKCLIM(4)
          IF(JCTAG(IC,JC).NE.0) GOTO 40
          IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,      &
               NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,        &
               XNS2,YNS1,YNS2,ZNS1,ZNS2)                                   
          IF(JC.GT.1) CALL INTE3D(CJ1(JC),ICONTN,ICONTP,IPV1,NIPV1,NTP1,&
               NTS1,NTV1,VERTP1,VNJ(1),XNS1,VNJ(2),YNS1,VNJ(3),ZNS1)
          IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
             IF(JC.LT.NCL) CALL INTE3D(CJ2(JC),ICONTN,ICONTP,IPV1,      &
                  NIPV1,NTP1,NTS1,NTV1,VERTP1,-VNJ(1),XNS1,-VNJ(2),     &
                  YNS1,-VNJ(3),ZNS1)                                         
             IF(ICONTP.NE.0) THEN 
                DO KC=IJKCLIM(5),IJKCLIM(6)                 
!                   IF(ITAGP(IC,JC,KC).NE.0) THEN
                   IF(ITAGP(IC,JC,KC).EQ.1) GOTO 50
                   IF(ITAGP(IC,JC,KC).EQ.2)  GOTO 50
                   IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0,   &
                        NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,     &
                        VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                   IF(KC.GT.1) CALL INTE3D(CK1(KC),ICONTN,ICONTP,IPV0,  &
                        NIPV0,NTP0,NTS0,NTV0,VERTP0,VNK(1),XNS0,        &
                        VNK(2),YNS0,VNK(3),ZNS0)                              
                   IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                      IF(KC.LT.NCL) CALL INTE3D(CK2(KC),ICONTN,ICONTP,  &
                           IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,-VNK(1),    &
                           XNS0,-VNK(2),YNS0,-VNK(3),ZNS0)               
                      IF(ICONTP.NE.0) THEN 
                         !..   Subcell determination by truncation  
!                         IF(NCL.GT.1.and.itagp2(ic,jc,kc).eq.0) THEN 
                         IF(NCL.GT.1) THEN 
                            ICONTP=0 
                            ICONTN=0 
                            DO IP=1,NTP0 
                               ICHECK(IP)=0 
                            END DO
                            DO IS=1,NTS0 
                               DO IV=1,NIPV0(IS) 
                                  IP=IPV0(IS,IV) 
                                  IF(ICHECK(IP).EQ.0) THEN 
                                     ICHECK(IP)=1 
                                     X=VERTP0(IP,1) 
                                     Y=VERTP0(IP,2) 
                                     Z=VERTP0(IP,3) 
                                     CALL PFUNC3D(PHIV(IP),CPARAB,VN,   &
                                          X,Y,Z)
                                     IF(PHIV(IP).GT.0.0_W_P) THEN 
                                        IA(IP)=1 
                                        ICONTP=ICONTP+1 
                                     ELSE 
                                        IA(IP)=0 
                                        ICONTN=ICONTN+1 
                                     END IF
                                  END IF
                               END DO
                            END DO
                         END IF
!                         IF(ICONTN.EQ.0.or.itagp2(ic,jc,kc).eq.1) THEN 
                         IF(ICONTN.EQ.0) THEN 
                            CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,        &
                                 VOLF,XNS0,YNS0,ZNS0)                 
                            VF=VF+VOLF
                            IF(ITAGP2(IC,JC,KC).EQ.1) THEN
!                               ITAGSC(IC,JC,KC)=1
                               VSC(IC,JC,KC)=VOLF
                            END IF
                         ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                            NTSINI=NTS0
                            CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,ISCUT,    &
                                 NIPV0,NTP0,NTS0,NTV0,1.0_W_P,XNS0,     &
                                 0.0_W_P,YNS0,0.0_W_P,ZNS0)
                            !.. Location of the new intersection points   
                            IF(NTS0.GT.NTSINI) THEN 
                               IS=NTS0 
                               IS2=NTS0
                               XMAX2=CX2(IC)
                               XMIN2=-CX1(IC)
                               YMAX2=CY2(JC)
                               YMIN2=-CY1(JC)
                               ZMAX2=CZ2(KC)
                               ZMIN2=-CZ1(KC)
                               DO IS=NTSINI+1,NTS0
                                  SUMX=0.0_W_P
                                  SUMY=0.0_W_P
                                  SUMZ=0.0_W_P
                                  DO IV=1,NIPV0(IS) 
                                     IP=IPV0(IS,IV) 
                                     IP0=IPIA0(IP) 
                                     IP1=IPIA1(IP) 
                                     V0(1)=VERTP0(IP0,1) 
                                     V0(2)=VERTP0(IP0,2) 
                                     V0(3)=VERTP0(IP0,3) 
                                     V1(1)=VERTP0(IP1,1) 
                                     V1(2)=VERTP0(IP1,2) 
                                     V1(3)=VERTP0(IP1,3)
                                     CALL INTEPFUNC3D(CPARAB,VN,V0,V1,  &
                                          VI)
                                     VERTP0(IP,1)=VI(1) 
                                     VERTP0(IP,2)=VI(2) 
                                     VERTP0(IP,3)=VI(3) 
                                     SUMX=SUMX+VERTP0(IP,1)
                                     SUMY=SUMY+VERTP0(IP,2)
                                     SUMZ=SUMZ+VERTP0(IP,3)
                                  END DO
                                  NTP0=NTP0+1
                                  VERTP0(NTP0,1)=SUMX/NIPV0(IS)
                                  VERTP0(NTP0,2)=SUMY/NIPV0(IS)
                                  VERTP0(NTP0,3)=SUMZ/NIPV0(IS)
                                  V0(1)=VERTP0(NTP0,1)
                                  V0(2)=VERTP0(NTP0,2)
                                  V0(3)=VERTP0(NTP0,3)
                                  CALL FINDBRACKETP(CPARAB,VN,DD/REAL(  &
                                       NCL,KIND=W_P),IEBRACKET,V0,V1)
                                  IF(IEBRACKET.EQ.2) THEN 
                                     VI=V1 
                                  ELSEIF(IEBRACKET.EQ.1) THEN
                                     CALL INTEPFUNC3D(CPARAB,VN,V0,V1,  &
                                          VI)
                                  ELSE
                                     VI=V0
                                  END IF
                                  VERTP0(NTP0,1)=VI(1) 
                                  VERTP0(NTP0,2)=VI(2) 
                                  VERTP0(NTP0,3)=VI(3)
                                  ISINI=IS2+1
                                  DO IV=1,NIPV0(IS)
                                     IS2=IS2+1
                                     IV2=IV+1
                                     IF(IV2.GT.NIPV0(IS)) IV2=1
                                     NIPV0(IS2)=3
                                     IPV0(IS2,1)=NTP0
                                     IPV0(IS2,2)=IPV0(IS,IV)
                                     IPV0(IS2,3)=IPV0(IS,IV2)
                                     XV1=VERTP0(IPV0(IS2,2),1)-         &
                                          VERTP0(IPV0(IS2,1),1)
                                     YV1=VERTP0(IPV0(IS2,2),2)-         &
                                          VERTP0(IPV0(IS2,1),2)
                                     ZV1=VERTP0(IPV0(IS2,2),3)-         &
                                          VERTP0(IPV0(IS2,1),3)
                                     XV2=VERTP0(IPV0(IS2,3),1)-         &
                                          VERTP0(IPV0(IS2,2),1)
                                     YV2=VERTP0(IPV0(IS2,3),2)-         &
                                          VERTP0(IPV0(IS2,2),2)
                                     ZV2=VERTP0(IPV0(IS2,3),3)-         &
                                          VERTP0(IPV0(IS2,2),3)
                                     XM=YV1*ZV2-ZV1*YV2
                                     YM=ZV1*XV2-XV1*ZV2
                                     ZM=XV1*YV2-YV1*XV2
                                     AMOD=(XM**2+YM**2+ZM**2)**0.5_W_P
                                     IF(AMOD.NE.0.0_W_P) THEN
                                        XNS0(IS2)=XM/AMOD
                                        YNS0(IS2)=YM/AMOD
                                        ZNS0(IS2)=ZM/AMOD
                                     ELSE
                                        XNS0(IS2)=XM
                                        YNS0(IS2)=YM
                                        ZNS0(IS2)=ZM
                                     END IF
                                  END DO
                                  !* Cancel the IS face
                                  IF(IS2.GT.IS) NIPV0(IS)=0
                               END DO
                               NTS0=IS2
                            END IF
                            CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,VOLF,   &
                                 XNS0,YNS0,ZNS0)
                            VF=VF+VOLF 
                         END IF
                      END IF
                   END IF
50                 CONTINUE
                END DO ! do kc
             END IF
          END IF
40        CONTINUE
       END DO ! do jc
30     CONTINUE
    END DO ! do ic
    RETURN 
  END SUBROUTINE INTPPASC
!------------------------- END OF INTPPASC ---------------------------| 
!---------------------------------------------------------------------|   
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            NEWPOL3D                                 | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! IA       = 0 if \Gamma_c points out of the vertex, 1 otherwise      | 
! IPV0     = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NIPV0    = number of vertices of each face                          | 
! NTP0     = last global vertex index                                 | 
! NTS0     = total number of faces                                    | 
! NTV0     = total number of vertices                                 | 
! XNS0, ...= unit-lenght normals to the faces of the original polyh.  | 
! XNC, ... = unit-lenght normal to the new face \Gamma_c              | 
! On return:                                                          | 
!===========                                                          | 
! IA       = 0 if \Gamma_c points out of the vertex, 1 otherwise      | 
! IPIA0    = global vertex index of the original polihedron with IA=0 | 
!            and which is in the edge containing the intersection     | 
!            point                                                    | 
! IPIA1    = global vertex index of the original polihedron with IA=1 | 
!            and which is in the edge containing the intersection     | 
!            point                                                    | 
! IPV0     = array containing the global indices of the truncat. pol. | 
!            vertices                                                 | 
! ISCUT    = 1 if the faces is truncated. 0 if the faces is not       | 
!            truncated                                                | 
! NIPV0    = number of vertices of each face                          | 
! NTP0     = last global vertex index                                 | 
! NTS0     = total number of faces                                    | 
! NTV0     = total number of vertices                                 | 
! XNS0, ...= unit-lenght normals to the faces of the truncated pol.   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE NEWPOL3D(IA,IPIA0,IPIA1,IPV0,ISCUT,NIPV0,NTP0,NTS0,NTV0,   &
       XNC,XNS0,YNC,YNS0,ZNC,ZNS0) BIND(C)                     
    !.. Scalar Arguments                                                    
    REAL (W_P), INTENT(IN) :: XNC,YNC,ZNC 
    INTEGER(I_P), INTENT(INOUT) :: NTP0,NTS0,NTV0 
    !.. Array Arguments                                                     
    REAL (W_P), INTENT(INOUT) :: XNS0(NS),YNS0(NS),ZNS0(NS) 
    INTEGER(I_P), INTENT(INOUT) :: IA(NV),IPV0(NS, NV),NIPV0(NS) 
    INTEGER(I_P), INTENT(OUT) :: IPIA0(NV),IPIA1(NV),ISCUT(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IP0I,IP1,IP1I,IPINI,IPNEW,IS,ISI,ISNEW,ITYPE,    &
         IV,IV1,IVNEW,IVNEWT,NINT,NIPNEW,NISCUT,NISMIX,NIV,NIVNEW,      &
         NTPMAX,NTSMAX                     
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IPISE(NV,2),IPMARK(NV),IPV1(NS,NV),ISMIX(NS),       &
         IVISE(NS,NV),NIPV1(NS)                 
    INTEGER(I_P2) :: IPE(NV,NV) 
    !* Determination of the cut faces                                       
    NISCUT=0 
    NISMIX=0 
    DO IS=1,NTS0 
       IF(NIPV0(IS).GT.0) THEN 
          ISCUT(IS)=0 
          DO IV=1,NIPV0(IS) 
             IP=IPV0(IS,IV) 
             IV1=IV+1 
             IF(IV.EQ.NIPV0(IS)) IV1=1 
             IP1=IPV0(IS,IV1) 
             IF(IA(IP).NE.IA(IP1)) THEN 
                IPE(IP,IP1)=0 
                ISCUT(IS)=1 
                NISCUT=NISCUT+1 
             END IF
          END DO
          IF(ISCUT(IS).EQ.0) THEN 
             IF(IA(IPV0(IS,1)).EQ.0) NIPV0(IS)=-NIPV0(IS) 
          ELSE 
             NISMIX=NISMIX+1 
             ISMIX(NISMIX)=IS 
          END IF
       END IF
    END DO
    !* Disjoint regions may produce NISCUT=0 and both ICONTP and ICONTN \NEQ
    !.. Cuando el polihedro es no convexo, puede ocurrir que despues de vari
    !.. intersecciones sucesivas, aparezcan varios polihedros individuales. 
    !.. un nuevo plano de corte pasa entre ellos, no aparecera ninguna cara 
    !.. cortada (NISCUT=0) aunque ICONTP y ICONTN sean ambos distintos de 0.
    IF(NISCUT.EQ.0) THEN 
       NIPNEW=0 
       NIVNEW=0 
       ISNEW=0 
       GOTO 50 
    END IF
    !* Construction of the cut faces                                        
    NIPNEW=NTP0 
    DO ISI=1,NISMIX 
       IS=ISMIX(ISI) 
       NIV=0 
       NINT=0 
       DO IV=1,NIPV0(IS) 
          IP=IPV0(IS,IV) 
          IV1=IV+1 
          IF(IV1.GT.NIPV0(IS))IV1=1 
          IP1=IPV0(IS,IV1) 
          IF(IA(IP).EQ.1) THEN 
             NIV=NIV+1 
             IPV1(IS,NIV)=IPV0(IS,IV) 
          END IF
          IF(IA(IP).NE.IA(IP1)) THEN 
             NINT=NINT+1 
             NIV=NIV+1 
             IF(IA(IP).EQ.1) THEN 
                IP1I=IP 
                IP0I=IP1 
                ITYPE=2 
             ELSE 
                IP1I=IP1 
                IP0I=IP 
                ITYPE=1 
             END IF
             IF(IPE(IP1,IP).NE.0) THEN 
                IPNEW=IPE(IP1,IP) 
                IPV1(IS,NIV)=IPNEW 
                IVISE(IS,IPNEW)=NIV 
                IPISE(IPNEW,ITYPE)=IS 
                GOTO 10 
             END IF
             NIPNEW=NIPNEW+1 
             IA(NIPNEW)=0 
             IPE(IP,IP1)=INT(NIPNEW,KIND=I_P2) 
             IPIA0(NIPNEW)=IP0I 
             IPIA1(NIPNEW)=IP1I 
             IPV1(IS,NIV)=NIPNEW 
             IVISE(IS,NIPNEW)=NIV 
             IPISE(NIPNEW,ITYPE)=IS 
          END IF
10        CONTINUE 
       END DO
       NIPV1(IS)=NIV 
    END DO
    !* Construction of the new faces                                        
    NIVNEW=NIPNEW-NTP0 
    ISNEW=NTS0 
    DO IP=NTP0+1,NIPNEW 
       IPMARK(IP)=0 
    END DO
    IVNEWT=0 
    IPNEW=NTP0+1 
    !* First point                                                          
40  CONTINUE 
    IVNEW=1 
    IVNEWT=IVNEWT+1 
    ISNEW=ISNEW+1 
    IPINI=IPNEW 
    IPV0(ISNEW,IVNEW)=IPNEW 
    IPMARK(IPNEW)=1 
20  CONTINUE 
    IS=IPISE(IPNEW,1) 
    IV=IVISE(IS,IPNEW) 
    IV1=IV-1 
    IF(IV1.EQ.0) IV1=NIPV1(IS) 
    IPNEW=IPV1(IS,IV1) 
    IF(IPNEW.NE.IPINI) THEN 
       IVNEW=IVNEW+1 
       IVNEWT=IVNEWT+1 
       IPV0(ISNEW,IVNEW)=IPNEW 
       IPMARK(IPNEW)=1 
       IF(IVNEWT.EQ.NIVNEW) GOTO 30 
       GOTO 20 
    END IF
    NIPV0(ISNEW)=IVNEW 
    DO IPNEW=NTP0+2,NIPNEW 
       IF(IPMARK(IPNEW).EQ.0) GOTO 40 
    END DO
30  CONTINUE 
    NIPV0(ISNEW)=IVNEW 
    !* Assign the vertices of the new truncated polyhedron                  
50  CONTINUE 
    NIV=NIVNEW 
    NTPMAX=NIPNEW 
    NTSMAX=ISNEW 
    DO IS=1,NTS0 
       IF(NIPV0(IS).GT.0) THEN 
          IF(ISCUT(IS).EQ.1) THEN 
             NIPV0(IS)=NIPV1(IS) 
             DO IV=1,NIPV1(IS) 
                IPV0(IS,IV)=IPV1(IS,IV) 
                IF(IA(IPV1(IS,IV)).EQ.1) THEN 
                   NIV=NIV+1 
                   IA(IPV1(IS,IV))=-1 
                END IF
             END DO
          ELSE 
             IF(ISCUT(IS).EQ.0.AND.NIPV0(IS).LT.0) NIPV0(IS)=0 
             DO IV=1,NIPV0(IS) 
                NTSMAX=MAX0(NTSMAX,IS) 
                IF(IA(IPV0(IS,IV)).EQ.1) THEN 
                   NTPMAX=MAX0(NTPMAX,IPV0(IS,IV)) 
                   NIV=NIV+1 
                   IA(IPV0(IS,IV))=-1 
                END IF
             END DO
          END IF
       END IF
    END DO
    DO IP=1,NTP0 
       IF(IA(IP).EQ.-1) IA(IP)=1 
    END DO
    DO IS=NTS0+1,ISNEW 
       XNS0(IS)=-1.0_W_P*XNC 
       YNS0(IS)=-1.0_W_P*YNC 
       ZNS0(IS)=-1.0_W_P*ZNC 
    END DO
    NTV0=NIV 
    NTP0=NTPMAX 
    NTS0=NTSMAX 
    RETURN 
  END SUBROUTINE NEWPOL3D
!-------------------------- END OF NEWPOL3D --------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            NEWPOLCF3D                               | 
! This version of NEWPOL3D returns the clipped face index, IS,        |
! associated to each new intersection point                           | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! IA       = 0 if \Gamma_c points out of the vertex, 1 otherwise      | 
! IPV0     = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NIPV0    = number of vertices of each face                          | 
! NTP0     = last global vertex index                                 | 
! NTS0     = total number of faces                                    | 
! NTV0     = total number of vertices                                 | 
! On return:                                                          | 
!===========                                                          | 
! IA       = 0 if \Gamma_c points out of the vertex, 1 otherwise      | 
! IPIA0    = global vertex index of the original polihedron with IA=0 | 
!            and which is in the edge containing the intersection     | 
!            point                                                    | 
! IPIA1    = global vertex index of the original polihedron with IA=1 | 
!            and which is in the edge containing the intersection     | 
!            point                                                    | 
! IPV0     = array containing the global indices of the truncat. pol. | 
!            vertices                                                 | 
! ISCFIP   = array containing the index of the clipped face           |
!            associated to each new intersection point                | 
! NIPV0    = number of vertices of each face                          | 
! NTP0     = last global vertex index                                 | 
! NTS0     = total number of faces                                    | 
! NTV0     = total number of vertices                                 | 
! XNS0, ...= unit-lenght normals to the faces of the truncated pol.   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE NEWPOLCF3D(IA,IPIA0,IPIA1,IPV0,ISCFIP,NIPV0,NTP0,NTS0,     &
       NTV0) BIND(C)                     
    !.. Scalar Arguments      
    INTEGER(I_P), INTENT(INOUT) :: NTP0,NTS0,NTV0 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(INOUT) :: IA(NV),IPV0(NS, NV),NIPV0(NS) 
    INTEGER(I_P), INTENT(OUT) :: IPIA0(NV),IPIA1(NV),ISCFIP(NV) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IP0I,IP1,IP1I,IPINI,IPNEW,IS,ISI,ISNEW,ITYPE,    &
         IV,IV1,IVNEW,IVNEWT,NINT,NIPNEW,NISCUT,NISMIX,NIV,NIVNEW,      &
         NTPMAX,NTSMAX                     
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IPISE(NV,2),IPMARK(NV),IPV1(NS,NV),ISCUT(NS),       &
         ISMIX(NS),IVISE(NS,NV),NIPV1(NS)                 
    INTEGER(I_P2) :: IPE(NV,NV) 
    !* Determination of the cut faces                                       
    NISCUT=0 
    NISMIX=0 
    DO IS=1,NTS0 
       IF(NIPV0(IS).GT.0) THEN 
          ISCUT(IS)=0 
          DO IV=1,NIPV0(IS) 
             IP=IPV0(IS,IV) 
             IV1=IV+1 
             IF(IV.EQ.NIPV0(IS)) IV1=1 
             IP1=IPV0(IS,IV1) 
             IF(IA(IP).NE.IA(IP1)) THEN 
                IPE(IP,IP1)=0 
                ISCUT(IS)=1 
                NISCUT=NISCUT+1 
             END IF
          END DO
          IF(ISCUT(IS).EQ.0) THEN 
             IF(IA(IPV0(IS,1)).EQ.0) NIPV0(IS)=-NIPV0(IS) 
          ELSE 
             NISMIX=NISMIX+1 
             ISMIX(NISMIX)=IS 
          END IF
       END IF
    END DO
    !* Disjoint regions may produce NISCUT=0 and both ICONTP and ICONTN \NEQ
    !.. Cuando el polihedro es no convexo, puede ocurrir que despues de vari
    !.. intersecciones sucesivas, aparezcan varios polihedros individuales. 
    !.. un nuevo plano de corte pasa entre ellos, no aparecera ninguna cara 
    !.. cortada (NISCUT=0) aunque ICONTP y ICONTN sean ambos distintos de 0.
    IF(NISCUT.EQ.0) THEN 
       NIPNEW=0 
       NIVNEW=0 
       ISNEW=0 
       GOTO 50 
    END IF
    !* Construction of the cut faces                                        
    NIPNEW=NTP0 
    DO ISI=1,NISMIX 
       IS=ISMIX(ISI) 
       NIV=0 
       NINT=0 
       DO IV=1,NIPV0(IS) 
          IP=IPV0(IS,IV) 
          IV1=IV+1 
          IF(IV1.GT.NIPV0(IS))IV1=1 
          IP1=IPV0(IS,IV1) 
          IF(IA(IP).EQ.1) THEN 
             NIV=NIV+1 
             IPV1(IS,NIV)=IPV0(IS,IV) 
          END IF
          IF(IA(IP).NE.IA(IP1)) THEN 
             NINT=NINT+1 
             NIV=NIV+1 
             IF(IA(IP).EQ.1) THEN 
                IP1I=IP 
                IP0I=IP1 
                ITYPE=2 
             ELSE 
                IP1I=IP1 
                IP0I=IP 
                ITYPE=1 
             END IF
             IF(IPE(IP1,IP).NE.0) THEN 
                IPNEW=IPE(IP1,IP) 
                IPV1(IS,NIV)=IPNEW 
                IVISE(IS,IPNEW)=NIV 
                IPISE(IPNEW,ITYPE)=IS 
                GOTO 10 
             END IF
             NIPNEW=NIPNEW+1 
             IA(NIPNEW)=0 
             IPE(IP,IP1)=INT(NIPNEW,KIND=I_P2) 
             IPIA0(NIPNEW)=IP0I 
             IPIA1(NIPNEW)=IP1I 
             IPV1(IS,NIV)=NIPNEW 
             IVISE(IS,NIPNEW)=NIV 
             IPISE(NIPNEW,ITYPE)=IS 
          END IF
10        CONTINUE 
       END DO
       NIPV1(IS)=NIV 
    END DO
    !* Construction of the new faces                                        
    NIVNEW=NIPNEW-NTP0 
    ISNEW=NTS0 
    DO IP=NTP0+1,NIPNEW 
       IPMARK(IP)=0
       ISCFIP(IP)=IPISE(IP,1)
    END DO
    IVNEWT=0 
    IPNEW=NTP0+1 
    !* First point                                                          
40  CONTINUE 
    IVNEW=1 
    IVNEWT=IVNEWT+1 
    ISNEW=ISNEW+1
    IPINI=IPNEW 
    IPV0(ISNEW,IVNEW)=IPNEW 
    IPMARK(IPNEW)=1 
20  CONTINUE 
    IS=IPISE(IPNEW,1) 
    IV=IVISE(IS,IPNEW) 
    IV1=IV-1 
    IF(IV1.EQ.0) IV1=NIPV1(IS) 
    IPNEW=IPV1(IS,IV1) 
    IF(IPNEW.NE.IPINI) THEN 
       IVNEW=IVNEW+1 
       IVNEWT=IVNEWT+1 
       IPV0(ISNEW,IVNEW)=IPNEW 
       IPMARK(IPNEW)=1 
       IF(IVNEWT.EQ.NIVNEW) GOTO 30 
       GOTO 20 
    END IF
    NIPV0(ISNEW)=IVNEW 
    DO IPNEW=NTP0+2,NIPNEW 
       IF(IPMARK(IPNEW).EQ.0) GOTO 40 
    END DO
30  CONTINUE 
    NIPV0(ISNEW)=IVNEW 
    !* Assign the vertices of the new truncated polyhedron                  
50  CONTINUE 
    NIV=NIVNEW 
    NTPMAX=NIPNEW 
    NTSMAX=ISNEW 
    DO IS=1,NTS0 
       IF(NIPV0(IS).GT.0) THEN 
          IF(ISCUT(IS).EQ.1) THEN 
             NIPV0(IS)=NIPV1(IS) 
             DO IV=1,NIPV1(IS) 
                IPV0(IS,IV)=IPV1(IS,IV) 
                IF(IA(IPV1(IS,IV)).EQ.1) THEN 
                   NIV=NIV+1 
                   IA(IPV1(IS,IV))=-1 
                END IF
             END DO
          ELSE 
             IF(ISCUT(IS).EQ.0.AND.NIPV0(IS).LT.0) NIPV0(IS)=0 
             DO IV=1,NIPV0(IS) 
                NTSMAX=MAX0(NTSMAX,IS) 
                IF(IA(IPV0(IS,IV)).EQ.1) THEN 
                   NTPMAX=MAX0(NTPMAX,IPV0(IS,IV)) 
                   NIV=NIV+1 
                   IA(IPV0(IS,IV))=-1 
                END IF
             END DO
          END IF
       END IF
    END DO
    DO IP=1,NTP0 
       IF(IA(IP).EQ.-1) IA(IP)=1 
    END DO
    NTV0=NIV 
    NTP0=NTPMAX 
    NTS0=NTSMAX 
    RETURN 
  END SUBROUTINE NEWPOLCF3D
!------------------------- END OF NEWPOLCF3D -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              EQSOL3D                                | 
!---------------------------------------------------------------------| 
!        This routine solves analyticaly a cubic equation             | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! Coefficients of the equation C3·x^3+C2·x^2+C1·x+C0=0                |
! CMIN,CMAX = brackets of the solution                                | 
! On return:                                                          | 
!===========                                                          | 
! CSOL      = solution of the cubic equation bracketed by CMIN and    | 
!             CMAX                                                    | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE EQSOL3D(C0,C1,C2,C3,CMIN,CMAX,CSOL) 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: C0,C1,C2,C3,CMAX,CMIN 
    REAL(W_P), INTENT(OUT) :: CSOL 
    !.. Local Scalars                                                       
    REAL(W_P) :: A,B,C,CSOL_1,CSOL_2,CSOL_3,D,DSOL_1,DSOL_2,DSOL_3,     &
         E,E2,E3,F,FSIGN,G,P,PI,Q,Q3,R,R2,T,THETA,TOLC,TOLC1            
    
    TOLC=1.0E-12_W_P 
    TOLC1=1.0E-12_W_P 
    PI=.31415926535897932384626433832795E+01_W_P 
    FSIGN=1.0_W_P 
    !* Eq. D*X^3+C*X^2+B*X+A=0                                              
    D=C3 
    C=C2 
    B=C1 
    A=C0 
    IF(ABS(D).LE.TOLC.AND.ABS(C).LE.TOLC) THEN 
       CSOL=-A/B 
       GOTO 10 
    END IF
    IF(ABS(D).LE.TOLC1) THEN 
       !* Eq. C*X^2+B*X+A=0                                                    
       E=B*B-4.0_W_P*C*A 
       IF(E.LT.0.0_W_P) THEN 
          Q=-(1.0_W_P/2.0_W_P)*B 
       ELSE 
          Q=-(1.0_W_P/2.0_W_P)*(B+SIGN(FSIGN,B)*SQRT(E)) 
       END IF
       CSOL_1=Q/C 
       CSOL_2=A/Q 
       DSOL_1=ABS(CSOL_1-CMIN)+ABS(CSOL_1-CMAX) 
       DSOL_2=ABS(CSOL_2-CMIN)+ABS(CSOL_2-CMAX) 
       IF(DSOL_1.LT.DSOL_2) THEN 
          CSOL=CSOL_1 
       ELSE 
          CSOL=CSOL_2 
       END IF
       GOTO 10 
    END IF
    E=C/D 
    F=B/D 
    G=A/D 
    E2=E*E 
    !* Eq. X^3+E*X^2+F*X+G=0                                                
    Q=(E2-3.0_W_P*F)/9.0_W_P 
    R=(2.0_W_P*E2*E-9.0_W_P*E*F+27.0_W_P*G)/54.0_W_P 
    R2=R*R 
    Q3=Q*Q*Q 
    E3=E/3.0_W_P 
    IF((R2).LT.(Q3)) THEN 
       THETA=ACOS(R/SQRT(Q3)) 
       CSOL_1=-2.0_W_P*(SQRT(Q))*COS(THETA/3.0_W_P)-(E3)
       CSOL_2=-2.0_W_P*(SQRT(Q))*COS((THETA+2.0_W_P*PI)/3.0_W_P)-       &
            (E3)                                         
       CSOL_3=-2.0_W_P*(SQRT(Q))*COS((THETA-2.0_W_P*PI)/3.0_W_P)-       &
            (E3)
       DSOL_1=ABS(CSOL_1-CMIN)+ABS(CSOL_1-CMAX) 
       DSOL_2=ABS(CSOL_2-CMIN)+ABS(CSOL_2-CMAX) 
       DSOL_3=ABS(CSOL_3-CMIN)+ABS(CSOL_3-CMAX) 
       IF(DSOL_1.LT.DSOL_2.AND.DSOL_1.LT.DSOL_3) THEN 
          CSOL=CSOL_1 
       ELSEIF(DSOL_2.LT.DSOL_1.AND.DSOL_2.LT.DSOL_3) THEN 
          CSOL=CSOL_2 
       ELSE 
          CSOL=CSOL_3 
       END IF
    ELSEIF((R2).EQ.(Q3)) THEN 
       IF(R.GT.0.0_W_P) THEN 
          CSOL_1=-2.0_W_P*SQRT(Q)-E3 
          CSOL_2=SQRT(Q)-E3 
          DSOL_1=ABS(CSOL_1-CMIN)+ABS(CSOL_1-CMAX) 
          DSOL_2=ABS(CSOL_2-CMIN)+ABS(CSOL_2-CMAX) 
          IF(DSOL_1.LT.DSOL_2) THEN 
             CSOL=CSOL_1 
          ELSE 
             CSOL=CSOL_2 
          END IF
       ELSEIF(R.LT.0.0_W_P) THEN 
          CSOL_1=2.0_W_P*SQRT(Q)-E3 
          CSOL_2=-SQRT(Q)-E3 
          DSOL_1=ABS(CSOL_1-CMIN)+ABS(CSOL_1-CMAX) 
          DSOL_2=ABS(CSOL_2-CMIN)+ABS(CSOL_2-CMAX) 
          IF(DSOL_1.LT.DSOL_2) THEN 
             CSOL=CSOL_1 
          ELSE 
             CSOL=CSOL_2 
          END IF
       ELSE 
          CSOL=-E3 
       END IF
    ELSE 
       P=-SIGN(FSIGN,R)*(ABS(R)+SQRT(R2-Q3))**(1.0_W_P/3.0_W_P)
       IF(ABS(P).LE.TOLC) THEN 
          T=0.0_W_P 
       ELSE 
          T=Q/P 
       END IF
       CSOL=(P+T)-(E3) 
    END IF
10  CONTINUE 
    RETURN 
  END SUBROUTINE EQSOL3D
!-------------------------- END OF EQSOL3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              NEWTON3D                               | 
!---------------------------------------------------------------------| 
!   This routine solves a cubic eq. using the Newton-Raphson method   | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! Coefficients of the equation D·x^3+C·x^2+B·x+A=0                    |
! CMIN,CMAX = brackets of the solution                                | 
! On return:                                                          | 
!===========                                                          | 
! CSOL      = solution of the cubic equation bracketed by CMIN and    | 
!             CMAX                                                    | 
! ISOL      = 0 si la solucion se encuentra entre CMIN y CMAX,        | 
!            -1 si una posible sol se encuentra a la izda del bracket,| 
!            +1 si una posible sol se encuentra a la dcha del bracket.| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE NEWTON3D(A,B,C,D,CMIN,CMAX,CSOL,ISOL) 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: A,B,C,CMAX,CMIN,D 
    REAL(W_P), INTENT(OUT) :: CSOL 
    INTEGER(I_P), INTENT(OUT) :: ISOL 
    !.. Local Scalars                                                       
    REAL(W_P) :: CH,CL,CMAX2,CMIN2,COLD,CSOL2,DCSOL,DFUNC,FUNC,         &
         FUNCMAX,FUNCMIN,TOLC,TOLD                                    
    INTEGER(I_P) :: ITEMAX,JITER 
    
    ITEMAX=100 
    ISOL=0 
    TOLC=1.0E-14_W_P 
    TOLD=1.0E-20_W_P 
    CSOL=(CMIN+CMAX)/2.0_W_P 
    CL=CMIN 
    CH=CMAX 
    COLD=CSOL 
    CSOL2=CSOL*CSOL 
    CMIN2=CMIN*CMIN 
    CMAX2=CMAX*CMAX 
    FUNC=D*CSOL2*CSOL+C*CSOL2+B*CSOL+A 
    DFUNC=3.0_W_P*D*CSOL2+2.0_W_P*C*CSOL+B 
    FUNCMIN=D*CMIN2*CMIN+C*CMIN2+B*CMIN+A 
    FUNCMAX=D*CMAX2*CMAX+C*CMAX2+B*CMAX+A 
    IF(FUNCMIN*FUNCMAX.GT.0.0_W_P) THEN 
       IF(DFUNC*FUNCMIN.GT.0.0_W_P) THEN 
          ISOL=-1 
          CSOL=CMIN 
       ELSE 
          ISOL=+1 
          CSOL=CMAX 
       ENDIF
       RETURN 
    ENDIF
    DO JITER=1,ITEMAX
       DCSOL=0.0_W_P
       IF(ABS(DFUNC).GT.TOLD) DCSOL=FUNC/DFUNC 
       !* Use a simple bisection when the Newton-Raphson iteration sends the   
       !* solution out of bounds or when DFUNC=0.0                             
       IF(ABS(DFUNC).LE.TOLD.OR.(CL-CSOL+DCSOL)*(CSOL-DCSOL-CH)         &
            .LT.0.0_W_P) THEN                                          
          DCSOL=(CH-CL)/2.0_W_P 
          CSOL=CL+DCSOL 
          IF(ABS(CSOL-COLD).LT.TOLC.AND.JITER.GT.1) then 
             RETURN 
          END IF
       ELSE 
          CSOL=CSOL-DCSOL 
          IF(ABS(DCSOL).LT.TOLC) RETURN 
       END IF
       CSOL2=CSOL*CSOL 
       FUNC=D*CSOL2*CSOL+C*CSOL2+B*CSOL+A 
       DFUNC=3.0_W_P*D*CSOL2+2.0_W_P*C*CSOL+B 
       IF(FUNC*FUNCMIN.GT.0.0_W_P) THEN 
          CL=CSOL 
       ELSE 
          CH=CSOL 
       END IF
       COLD=CSOL 
    END DO
    RETURN 
  END SUBROUTINE NEWTON3D
!-------------------------- END OF NEWTON3D --------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                               INTE3D                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! XNC, ... = unit-lenght normal to the new face \Gamma_c              | 
! C        = constant of the plane containing the new face \Gamma_c   | 
! XNS0, ...= unit-lenght normals to the faces of the original pol.    | 
! IPV0     = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NIPV0    = number of vertices of each face                          | 
! NTS0     = total number of faces                                    | 
! NTP0     = last global vertex index                                 | 
! NTV0     = total number of vertices                                 | 
! VERTP0   = vertex coordinates of the original polyhedron            | 
! On return:                                                          | 
!===========                                                          | 
! XNS0, ...= unit-lenght normals to the faces of the truncated pol.   | 
! IPV0     = array containing the global indices of the truncat. pol. | 
!            vertices                                                 | 
! NIPV0    = number of vertices of each face                          | 
! NTS0     = total number of faces                                    | 
! NTP0     = last global vertex index                                 | 
! NTV0     = total number of vertices                                 | 
! ICONTN   = num. of vertices of the original region that are outside | 
!            the truncated region                                     | 
! ICONTP   = num. of vertices of the original region that remain in   | 
!            the truncated region                                     | 
! VERTP0   = vertex coordinates of the truncated polyhedron           | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INTE3D(C,ICONTN,ICONTP,IPV0,NIPV0,NTP0,NTS0,NTV0,          &
       VERTP0,XNC,XNS0,YNC,YNS0,ZNC,ZNS0) BIND(C)                   
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: C,XNC,YNC,ZNC 
    INTEGER(I_P), INTENT(INOUT) :: NTP0,NTS0,NTV0 
    INTEGER(I_P), INTENT(OUT) :: ICONTN,ICONTP 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(INOUT) :: VERTP0(NV,3),XNS0(NS),YNS0(NS),         &
         ZNS0(NS)                                                     
    INTEGER(I_P), INTENT(INOUT) :: IPV0(NS,NV),NIPV0(NS) 
    !.. Local Scalars                 
    INTEGER(I_P) :: IP,IP0,IP1,IS,IV,NTS00 
    !.. Local Arrays                                                        
    REAL(W_P) :: PHIV(NV) 
    INTEGER(I_P) :: IA(NV),IPIA0(NV),IPIA1(NV),ISCUT(NS) 
    
    ICONTP=0 
    ICONTN=0 
    DO IP=1,NTP0 
       IA(IP)=-1 
    END DO
    !* Distance function and values of IA                                   
    DO IS=1,NTS0 
       DO IV=1,NIPV0(IS) 
          IP=IPV0(IS,IV) 
          IF(IA(IP).EQ.(-1)) THEN 
             PHIV(IP)=XNC*VERTP0(IP,1)+YNC*VERTP0(IP,2)+ZNC*            &
                  VERTP0(IP,3)+C
             IF(PHIV(IP).GT.0.0_W_P) THEN 
                IA(IP)=1 
                ICONTP=ICONTP+1 
             ELSE 
                IA(IP)=0 
                ICONTN=ICONTN+1 
             END IF
          END IF
       END DO
    END DO
    IF(ICONTP.NE.0.AND.ICONTN.NE.0) THEN 
       !* Construction of the new polyhedron                                   
       NTS00=NTS0 
       CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,ISCUT,NIPV0,NTP0,NTS0,         &
            NTV0,XNC,XNS0,YNC,YNS0,ZNC,ZNS0)                          
       !* Position of the new vertices                                         
       DO IS=NTS00+1,NTS0 
          DO IV=1,NIPV0(IS) 
             IP=IPV0(IS,IV) 
             IP0=IPIA0(Ip) 
             IP1=IPIA1(Ip) 
             VERTP0(IP,1)=VERTP0(IP0,1)-PHIV(IP0)*(VERTP0(IP1,1)-       &
                  VERTP0(IP0,1))/(PHIV(IP1)-PHIV(IP0))                   
             VERTP0(IP,2)=VERTP0(IP0,2)-PHIV(IP0)*(VERTP0(IP1,2)-       &
                  VERTP0(IP0,2))/(PHIV(IP1)-PHIV(IP0))                   
             VERTP0(IP,3)=VERTP0(IP0,3)-PHIV(IP0)*(VERTP0(IP1,3)-       &
                  VERTP0(IP0,3))/(PHIV(IP1)-PHIV(IP0))                   
          END DO
          !. Faces with less than 3 vertices are supressed.
          IF(NIPV0(IS).LT.3) NIPV0(IS)=0 
       END DO
    END IF
    RETURN 
  END SUBROUTINE INTE3D
!--------------------------- END OF INTE3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              INITF3D                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! FUNC3D   = external user-supplied function where the interface      | 
!            shape is analytically defined                            | 
! IPV      = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NC       = number of sub-cells along each coordinate axis of the    | 
!            superimposed Cartesian grid                              | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! TOL      = prescribed positive tolerance for the distance to the    | 
!            interface                                                | 
! VERTP    = vertex coordinates of the original polyhedron            | 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  | 
! On return:                                                          | 
!===========                                                          | 
! VF       = material volume fraction                                 | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INITF3D(FUNC3D,IPV,NC,NIPV,NTP,NTS,NTV,TOL,VERTP,VF,       &
       XNS,YNS,ZNS) BIND(C)                                         
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: TOL 
    REAL(W_P), INTENT(OUT) :: VF 
    INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
    !.. Procedure Arguments                                                 
    PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
    !.. Local Scalars                                                       
    REAL(W_P) :: AMOD,CX1,CX2,CY1,CY2,CZ1,CZ2,DDX,DDY,DDZ,DX,           &
         DY,DZ,PHIMIN,SUMX,SUMY,SUMZ,VOLF,VOLT,X,XC,XM,XMAX,XMIN,       &
         XP,XV1,XV2,Y,YC,YM,YMAX,YMIN,YP,YV1,YV2,Z,ZC,ZM,ZMAX,          &
         ZMIN,ZP,ZV1,ZV2                                              
    INTEGER(I_P) :: IC,ICONTN,ICONTP,IP,IP0,IP1,IPHI,IS,IS2,IV,         &
         IV2,JC,KC,NTP0,NTP1,NTP2,NTS0,NTS1,NTS2,NTSINI,NTV0,NTV1,      &
         NTV2                                                         
    !.. Local Arrays                                           
    REAL(W_P) :: CS(NS),CS0(NS),CS1(NS),CS2(NS),PHIV(NV),               &
         VERTP0(NV,3),VERTP1(NV,3),VERTP2(NV,3),XNS0(NS),XNS1(NS),      &
         XNS2(NS),YNS0(NS),YNS1(NS),YNS2(NS),ZNS0(NS),ZNS1(NS),         &
         ZNS2(NS)            
    INTEGER(I_P) :: IA(NV),ICHECK(NV),IPIA0(NV),IPIA1(NV),              &
         IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),ISCUT(NS),NIPV0(NS),       &
         NIPV1(NS),NIPV2(NS)                                          
    !.. Coordinate extremes of the cell and vertex tagging 
    XMIN=1.0E+20_W_P 
    XMAX=-1.0E+20_W_P 
    YMIN=1.0E+20_W_P 
    YMAX=-1.0E+20_W_P 
    ZMIN=1.0E+20_W_P 
    ZMAX=-1.0E+20_W_P 
    ICONTP=0 
    ICONTN=0 
    DO IP=1,NTP 
       ICHECK(IP)=0 
    END DO
    DO IS=1,NTS 
       DO IV=1,NIPV(IS) 
          IP=IPV(IS,IV) 
          IF(ICHECK(IP).EQ.0) THEN 
             ICHECK(IP)=1 
             XP=VERTP(IP,1) 
             YP=VERTP(IP,2) 
             ZP=VERTP(IP,3) 
             XMIN=DMIN1(XMIN,XP) 
             XMAX=DMAX1(XMAX,XP) 
             YMIN=DMIN1(YMIN,YP) 
             YMAX=DMAX1(YMAX,YP) 
             ZMIN=DMIN1(ZMIN,ZP) 
             ZMAX=DMAX1(ZMAX,ZP) 
             PHIV(IP)=FUNC3D(XP,YP,ZP) 
             IF(PHIV(IP).GE.0.0_W_P) THEN 
                IA(IP)=1 
                ICONTP=ICONTP+1 
             ELSE 
                IA(IP)=0 
                ICONTN=ICONTN+1 
             END IF
          END IF
       END DO
    END DO
    DX=XMAX-XMIN 
    DY=YMAX-YMIN 
    DZ=ZMAX-ZMIN 
    !.. initialization                                                      
    IPHI=0 
    PHIMIN=10.0_W_P*MAX(DX,DY,DZ) 
    DO IS=1,NTS 
       DO IV=1,NIPV(IS) 
          IP=IPV(IS,IV) 
          PHIMIN=MIN(PHIMIN,ABS(PHIV(IP))) 
       END DO
    END DO
    IF(PHIMIN.LT.TOL*DX) IPHI=1 
    IF(IPHI.EQ.0) THEN 
       IF(ICONTP.EQ.NTV) THEN 
          VF=1.0_W_P 
          RETURN 
       END IF
       IF(ICONTN.EQ.NTV) THEN 
          VF=0.0_W_P
          RETURN 
       END IF
    END IF
    !.. compute the volume VOLT of the original polyhedron                  
    CALL TOOLV3D(IPV,NIPV,NTS,VERTP,VOLT,XNS,YNS,ZNS) 
    DDX=DX/NC 
    DDY=DY/NC 
    DDZ=DZ/NC 
    VF=0.0_W_P
    DO IC=1,NC
       XC=XMIN+(REAL(IC,KIND=W_P)-1.0_W_P)*DDX 
       CALL CPPOL3D(CS2,CS,IPV2,IPV,NIPV2,NIPV,NTP2,NTP,NTS2,           &
            NTS,NTV2,NTV,VERTP2,VERTP,XNS2,XNS,YNS2,YNS,ZNS2,ZNS)     
       CX1=-XC 
       IF(IC.GT.1) CALL INTE3D(CX1,ICONTN,ICONTP,IPV2,NIPV2,NTP2,       &
            NTS2,NTV2,VERTP2,1.0D0,XNS2,0.0_W_P,YNS2,0.0_W_P,ZNS2) 
       CX2=XC+DDX 
       IF(IC.LT.NC) CALL INTE3D(CX2,ICONTN,ICONTP,IPV2,NIPV2,NTP2,      &
            NTS2,NTV2,VERTP2,-1.0_W_P,XNS2,0.0_W_P,YNS2,0.0D0,ZNS2)       
       DO JC=1,NC 
          YC=YMIN+(REAL(JC,KIND=W_P)-1.0_W_P)*DDY 
          CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,NTP1,NTP2,         &
               NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,XNS2,YNS1,        &
               YNS2,ZNS1,ZNS2)                                        
          CY1=-YC 
          IF(JC.GT.1) CALL INTE3D(CY1,ICONTN,ICONTP,IPV1,NIPV1,NTP1,    &
               NTS1,NTV1,VERTP1,0.0_W_P,XNS1,1.0_W_P,YNS1,0.0_W_P,      &
               ZNS1)     
          IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
             CY2=YC+DDY 
             IF(JC.LT.NC) CALL INTE3D(CY2,ICONTN,ICONTP,IPV1,NIPV1,     &
                  NTP1,NTS1,NTV1,VERTP1,0.0_W_P,XNS1,-1.0_W_P,YNS1,     &
                  0.0_W_P,ZNS1)                                               
             IF(ICONTP.NE.0) THEN 
                DO KC=1,NC 
                   ZC=ZMIN+(REAL(KC,KIND=W_P)-1.0_W_P)*DDZ 
                   CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0,NIPV1,          &
                        NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,           &
                        VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                   CZ1=-ZC 
                   IF(KC.GT.1) CALL INTE3D(CZ1,ICONTN,ICONTP,IPV0,      &
                        NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0_W_P,XNS0,       &
                        0.0_W_P,YNS0,1.0_W_P,ZNS0)  
                   IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                      CZ2=ZC+DDZ 
                      IF(KC.LT.NC) CALL INTE3D(CZ2,ICONTN,ICONTP,       &
                           IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0_W_P,    &
                           XNS0,0.0_W_P,YNS0,-1.0_W_P,ZNS0)                    
                      IF(ICONTP.NE.0) THEN 
                         !..   Subcell determination by truncation   
                         ICONTP=0 
                         ICONTN=0 
                         DO IP=1,NTP0 
                            ICHECK(IP)=0 
                         END DO
                         DO IS=1,NTS0 
                            DO IV=1,NIPV0(IS) 
                               IP=IPV0(IS,IV) 
                               IF(ICHECK(IP).EQ.0) THEN 
                                  ICHECK(IP)=1 
                                  X=VERTP0(IP,1) 
                                  Y=VERTP0(IP,2) 
                                  Z=VERTP0(IP,3) 
                                  PHIV(IP)=FUNC3D(X,Y,Z) 
                                  IF(PHIV(IP).GE.0.0_W_P) THEN 
                                     IA(IP)=1 
                                     ICONTP=ICONTP+1 
                                  ELSE 
                                     IA(IP)=0 
                                     ICONTN=ICONTN+1 
                                  END IF
                               END IF
                            END DO
                         END DO
                         IF(ICONTN.EQ.0) THEN 
                            CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,        &
                                 VOLF,XNS0,YNS0,ZNS0)                 
                            VF=VF+VOLF 
                         ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                            NTSINI=NTS0 
                            CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,          &
                                 ISCUT,NIPV0,NTP0,NTS0,NTV0,            &
                                 1.0_W_P,XNS0,0.0_W_P,YNS0,0.0_W_P,     &
                                 ZNS0)                                
                            !.. Location of the new intersection points 
                            IF(NTS0.GT.NTSINI) THEN 
                               IS=NTS0 
                               IS2=NTS0 
                               DO IS=NTSINI+1,NTS0 
                                  SUMX=0.0_W_P 
                                  SUMY=0.0_W_P 
                                  SUMZ=0.0_W_P 
                                  DO IV=1,NIPV0(IS) 
                                     IP=IPV0(IS,IV) 
                                     IP0=IPIA0(IP) 
                                     IP1=IPIA1(IP) 
                                     VERTP0(IP,1)=VERTP0(IP0,1)-        &
                                          PHIV(IP0)*(VERTP0(IP1,        &
                                          1)-VERTP0(IP0,1))/(           &
                                          PHIV(IP1)-PHIV(IP0))        
                                     VERTP0(IP,2)=VERTP0(IP0,2)-        &
                                          PHIV(IP0)*(VERTP0(IP1,        &
                                          2)-VERTP0(IP0,2))/(           &
                                          PHIV(IP1)-PHIV(IP0))        
                                     VERTP0(IP,3)=VERTP0(IP0,3)-        &
                                          PHIV(IP0)*(VERTP0(IP1,        &
                                          3)-VERTP0(IP0,3))/(           &
                                          PHIV(IP1)-PHIV(IP0))        
                                     SUMX=SUMX+VERTP0(IP,1) 
                                     SUMY=SUMY+VERTP0(IP,2) 
                                     SUMZ=SUMZ+VERTP0(IP,3) 
                                  END DO
                                  NTP0=NTP0+1 
                                  VERTP0(NTP0,1)=SUMX/NIPV0(IS) 
                                  VERTP0(NTP0,2)=SUMY/NIPV0(IS) 
                                  VERTP0(NTP0,3)=SUMZ/NIPV0(IS) 
                                  !. The new face IS is replaced by
                                  !. NIPV(IS) triangular faces        
                                  DO IV=1,NIPV0(IS) 
                                     IS2=IS2+1 
                                     IV2=IV+1 
                                     IF(IV2.GT.NIPV0(IS)) IV2=1            
                                     NIPV0(IS2)=3 
                                     IPV0(IS2,1)=NTP0 
                                     IPV0(IS2,2)=IPV0(IS,IV) 
                                     IPV0(IS2,3)=IPV0(IS,IV2) 
                                     XV1=VERTP0(IPV0(IS2,2),1)-         &
                                          VERTP0(IPV0(IS2,1),1)       
                                     YV1=VERTP0(IPV0(IS2,2),2)-         &
                                          VERTP0(IPV0(IS2,1),2)       
                                     ZV1=VERTP0(IPV0(IS2,2),3)-         &
                                          VERTP0(IPV0(IS2,1),3)       
                                     XV2=VERTP0(IPV0(IS2,3),1)-         &
                                          VERTP0(IPV0(IS2,2),1)       
                                     YV2=VERTP0(IPV0(IS2,3),2)-         &
                                          VERTP0(IPV0(IS2,2),2)       
                                     ZV2=VERTP0(IPV0(IS2,3),3)-         &
                                          VERTP0(IPV0(IS2,2),3)       
                                     XM=YV1*ZV2-ZV1*YV2 
                                     YM=ZV1*XV2-XV1*ZV2 
                                     ZM=XV1*YV2-YV1*XV2 
                                     AMOD=(XM**2+YM**2+ZM**2)**0.5_W_P
                                     IF(AMOD.NE.0.0_W_P) THEN 
                                        XNS0(IS2)=XM/AMOD 
                                        YNS0(IS2)=YM/AMOD 
                                        ZNS0(IS2)=ZM/AMOD 
                                     ELSE 
                                        NIPV0(IS2)=0 
                                     END IF
                                  END DO
                                  !* Cancel the IS face   
                                  IF(IS2.GT.IS) NIPV0(IS)=0 
                               END DO
                               NTS0=IS2 
                            END IF
                            CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,        &
                                 VOLF,XNS0,YNS0,ZNS0)                 
                            VF=VF+VOLF 
                         END IF
                      END IF
                   END IF
                END DO
             END IF
          END IF
       END DO
    END DO
    VF=VF/VOLT 
    RETURN 
  END SUBROUTINE INITF3D
!--------------------------- END OF INITF3D --------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                               PFUNC3D                               | 
! Signed distance from point to paraboloid                            |
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! VN       = paraboloid orthonormal basis                             |
! X,Y,Z    = coordinates of the point where VALUE is computed         | 
! On return:                                                          | 
!===========                                                          | 
! A        = value of the multi-implicit interface shape functions:   | 
!            > 0 (inside the interface), < 0 (outside the             | 
!            interface); = 0 (on the interface)                       | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE PFUNC3D(A,CPARAB,VN,X,Y,Z) BIND(C) 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: X,Y,Z 
    REAL(W_P), INTENT(OUT) :: A 
    !.. Array Arguments                                                     
    REAL (W_P), INTENT(IN) :: CPARAB(12)
    REAL (W_P), INTENT(IN) :: VN(9)
    !.. Local Scalars             
    REAL(W_P) :: F,U,V,XT,YT,ZT      
    !. System transformation. From global (X,Y,Z) to local (F,U,V)
    ! where F is the main axis of paraboloid construction
    XT=X-CPARAB(10)
    YT=Y-CPARAB(11) 
    ZT=Z-CPARAB(12) 
    F=XT*VN(1)+YT*VN(2)+ZT*VN(3) 
    U=XT*VN(4)+YT*VN(5)+ZT*VN(6) 
    V=XT*VN(7)+YT*VN(8)+ZT*VN(9) 
    !. Signed distance function
    A=F-(CPARAB(1)+CPARAB(2)*U+CPARAB(3)*V+CPARAB(4)*U**2               &
         +CPARAB(5)*U*V+CPARAB(6)*V**2)
    RETURN 
  END SUBROUTINE PFUNC3D
!--------------------------- END OF PFUNC3D --------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              INTPV3DPAOLD                              | 
! Volume of the polyhedral approximation of the region of intersection|
! between a paraboloid and an arbitrary polyhedron                    |
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! IPV      = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NC       = number of sub-cells along each coordinate axis of the    | 
!            superimposed Cartesian grid                              | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = vertex coordinates of the original polyhedron            | 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  | 
! On return:                                                          | 
!===========                                                          | 
! VF       = volume of intersection                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INTPV3DPAOLD(CPARAB,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF,XNS,     &
       YNS,ZNS) BIND(C)                                         
    !.. Scalar Arguments                                                    
    REAL (W_P), INTENT(IN) :: CPARAB(12)
    REAL(W_P), INTENT(OUT) :: VF 
    INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
    !.. Local Scalars                                                       
    REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DMOD,DX,DY,DZ,                     &
         SUMX,SUMY,SUMZ,TOLPHI,VOLF,X,                                  &
         XM,XMAX,XMAX2,XMIN,XMIN2,XP,XV1,XV2,Y,YM,YMAX,YMAX2,YMIN,      &
         YMIN2,YP,YV1,YV2,Z,ZM,ZMAX,ZMAX2,ZMIN,ZMIN2,ZP,ZV1,ZV2
    INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IEBRACKET,IP,                    &
         IP0,IP1,IS,IS2,ISINI,IV,IV2,JC,KC,                             &
         NCL,NTP0,NTP1,NTP2,NTPT,                                       &
         NTS0,NTS1,NTS2,NTST,NTSINI,NTV0,NTV1,NTV2,NTVT                
         
    !.. Local Arrays                                                        
    REAL(W_P) :: CI1(NC),CI2(NC),CJ1(NC),CJ2(NC),CK1(NC),CK2(NC),       &
         CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC),CX2(NC),        &
         CY1(NC),CY2(NC),CZ1(NC),CZ2(NC),PHIV(NV),PHIVMIN(NS),V0(3),    &
         V1(3),VI(3),VNI(3),VNJ(3),VNK(3),VERTP0(NV,3),                 &
         VERTP1(NV,3),VERTP2(NV,3),VERTPT(NV,3),VN(9),XNS0(NS),         &
         XNS1(NS),XNS2(NS),XNST(NS),YNS0(NS),YNS1(NS),YNS2(NS),         &
         YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),ZNST(NS)         
    INTEGER(I_P) :: IA(NV),ICHECK(NV),IJKCLIM(6),IPIA0(NV),             &
         IPIA1(NV),IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),     &
         ISCONTN(NS),ISCONTP(NS),ISCUT(NS),NIPV0(NS),                   &
         NIPV1(NS),NIPV2(NS),NIPVT(NS)
    TOLPHI=1.0E-16_W_P
    !.. Coordinate extremes of the cell and vertex tagging                  
    NCL=NC 
    VF=0.0_W_P 
    XMIN=1.0E+20_W_P 
    XMAX=-1.0E+20_W_P 
    YMIN=1.0E+20_W_P 
    YMAX=-1.0E+20_W_P 
    ZMIN=1.0E+20_W_P 
    ZMAX=-1.0E+20_W_P 
    ICONTP=0 
    ICONTN=0 
    V0(1)=0.0_W_P 
    V0(2)=0.0_W_P 
    V0(3)=0.0_W_P 
    DO IP=1,NTP 
       ICHECK(IP)=0 
    END DO
    !Paraboloid orthonormal basis
    VN(1)=CPARAB(7) 
    VN(2)=CPARAB(8) 
    VN(3)=CPARAB(9) 
    VN(4)=VN(2)
    VN(5)=-VN(1)
    VN(6)=0.0_W_P
    DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
    IF(DMOD.NE.0.0_W_P) THEN
       VN(4)=VN(4)/DMOD
       VN(5)=VN(5)/DMOD
    ELSE
       VN(4)=VN(3)
       VN(5)=0.0_W_P
       VN(6)=-VN(1)
       DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
       VN(4)=VN(4)/DMOD
       VN(6)=VN(6)/DMOD
    END IF
    VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
    VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
    VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
    
    DO IS=1,NTS
       ISCONTP(IS)=0
       ISCONTN(IS)=0
       PHIVMIN(IS)=1.0E+20_W_P
       CS(IS)=-XNS(IS)*VERTP(IPV(IS,1),1)-YNS(IS)*VERTP(IPV(IS,1),2)    &
            -ZNS(IS)*VERTP(IPV(IS,1),3)
       DO IV=1,NIPV(IS) 
          IP=IPV(IS,IV) 
          IF(ICHECK(IP).EQ.0) THEN 
             ICHECK(IP)=1 
             XP=VERTP(IP,1) 
             YP=VERTP(IP,2) 
             ZP=VERTP(IP,3) 
             XMIN=DMIN1(XMIN,XP) 
             XMAX=DMAX1(XMAX,XP) 
             YMIN=DMIN1(YMIN,YP) 
             YMAX=DMAX1(YMAX,YP) 
             ZMIN=DMIN1(ZMIN,ZP) 
             ZMAX=DMAX1(ZMAX,ZP)
             IF(NC.EQ.1) THEN
                CALL PFUNC3D(PHIV(IP),CPARAB,VN,XP,YP,ZP)
                IF(PHIV(IP).GT.0.0_W_P) THEN 
                   IA(IP)=1 
                   ICONTP=ICONTP+1 
                ELSE 
                   IA(IP)=0 
                   ICONTN=ICONTN+1 
                END IF
             END IF
          END IF
       END DO
    END DO
    !.. initialization                                                      
    DX=XMAX-XMIN 
    DY=YMAX-YMIN 
    DZ=ZMAX-ZMIN 
    DD=0.01*MIN(DX,DY,DZ)
    IF(DD.LT.1.0E-20_W_P) THEN
       VF=0.0_W_P 
       RETURN 
    END IF
    CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,NTS,NTVT,     &
         NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)
    DDX=DX/REAL(NCL,KIND=W_P) 
    DDY=DY/REAL(NCL,KIND=W_P) 
    DDZ=DZ/REAL(NCL,KIND=W_P) 
    DO I=1,NCL 
       IF(I.EQ.1) THEN 
          CX1(I)=-XMIN 
       ELSE 
          CX1(I)=CX1(I-1)-DDX 
       END IF
       CX2(I)=-CX1(I)+DDX 
    END DO
    DO I=1,NCL 
       IF(I.EQ.1) THEN 
          CY1(I)=-YMIN 
       ELSE 
          CY1(I)=CY1(I-1)-DDY 
       END IF
       CY2(I)=-CY1(I)+DDY 
    END DO
    DO I=1,NCL 
       IF(I.EQ.1) THEN 
          CZ1(I)=-ZMIN 
       ELSE 
          CZ1(I)=CZ1(I-1)-DDZ 
       END IF
       CZ2(I)=-CZ1(I)+DDZ 
    END DO
    IJKCLIM(1)=1
    IJKCLIM(2)=NCL
    IJKCLIM(3)=1
    IJKCLIM(4)=NCL
    IJKCLIM(5)=1
    IJKCLIM(6)=NCL
    VNI(:)=[1.0_W_P,0.0_W_P,0.0_W_P]
    VNJ(:)=[0.0_W_P,1.0_W_P,0.0_W_P]
    VNK(:)=[0.0_W_P,0.0_W_P,1.0_W_P]
    CI1(:)=CX1(:)
    CI2(:)=CX2(:)
    CJ1(:)=CY1(:)
    CJ2(:)=CY2(:)
    CK1(:)=CZ1(:)
    CK2(:)=CZ2(:)
    DO IC=IJKCLIM(1),IJKCLIM(2) 
       IF(NCL.EQ.1) THEN 
          CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,    &
               NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,        &
               ZNS0,ZNST)                                                  
       ELSE 
          CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,    &
               NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,        &
               ZNS2,ZNST)                                                  
       END IF
       IF(IC.GT.1) CALL INTE3D(CI1(IC),ICONTN,ICONTP,IPV2,NIPV2,        &
            NTP2,NTS2,NTV2,VERTP2,VNI(1),XNS2,VNI(2),YNS2,VNI(3),ZNS2)        
       IF(IC.LT.NCL) CALL INTE3D(CI2(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
            NTS2,NTV2,VERTP2,-VNI(1),XNS2,-VNI(2),YNS2,-VNI(3),ZNS2)  
       DO JC=IJKCLIM(3),IJKCLIM(4) 
          IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,      &
               NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,        &
               XNS2,YNS1,YNS2,ZNS1,ZNS2)                                   
          IF(JC.GT.1) CALL INTE3D(CJ1(JC),ICONTN,ICONTP,IPV1,NIPV1,NTP1,&
               NTS1,NTV1,VERTP1,VNJ(1),XNS1,VNJ(2),YNS1,VNJ(3),ZNS1)
          IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
             IF(JC.LT.NCL) CALL INTE3D(CJ2(JC),ICONTN,ICONTP,IPV1,      &
                  NIPV1,NTP1,NTS1,NTV1,VERTP1,-VNJ(1),XNS1,-VNJ(2),     &
                  YNS1,-VNJ(3),ZNS1)                                         
             IF(ICONTP.NE.0) THEN 
                DO KC=IJKCLIM(5),IJKCLIM(6) 
                   IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0,   &
                        NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,     &
                        VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                   IF(KC.GT.1) CALL INTE3D(CK1(KC),ICONTN,ICONTP,IPV0,  &
                        NIPV0,NTP0,NTS0,NTV0,VERTP0,VNK(1),XNS0,        &
                        VNK(2),YNS0,VNK(3),ZNS0)                              
                   IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                      IF(KC.LT.NCL) CALL INTE3D(CK2(KC),ICONTN,ICONTP,  &
                           IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,-VNK(1),    &
                           XNS0,-VNK(2),YNS0,-VNK(3),ZNS0)               
                      IF(ICONTP.NE.0) THEN 
                         !..   Subcell determination by truncation  
                         IF(NCL.GT.1) THEN 
                            ICONTP=0 
                            ICONTN=0 
                            DO IP=1,NTP0 
                               ICHECK(IP)=0 
                            END DO
                            DO IS=1,NTS0 
                               DO IV=1,NIPV0(IS) 
                                  IP=IPV0(IS,IV) 
                                  IF(ICHECK(IP).EQ.0) THEN 
                                     ICHECK(IP)=1 
                                     X=VERTP0(IP,1) 
                                     Y=VERTP0(IP,2) 
                                     Z=VERTP0(IP,3) 
                                     CALL PFUNC3D(PHIV(IP),CPARAB,VN,   &
                                          X,Y,Z)
                                     IF(PHIV(IP).GT.0.0_W_P) THEN 
                                        IA(IP)=1 
                                        ICONTP=ICONTP+1 
                                     ELSE 
                                        IA(IP)=0 
                                        ICONTN=ICONTN+1 
                                     END IF
                                  END IF
                               END DO
                            END DO
                         END IF
                         IF(ICONTN.EQ.0) THEN 
                            CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,        &
                                 VOLF,XNS0,YNS0,ZNS0)                 
                            VF=VF+VOLF 
                         ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                            NTSINI=NTS0
                            CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,ISCUT,    &
                                 NIPV0,NTP0,NTS0,NTV0,1.0_W_P,XNS0,     &
                                 0.0_W_P,YNS0,0.0_W_P,ZNS0)
                            !.. Location of the new intersection points   
                            IF(NTS0.GT.NTSINI) THEN 
                               IS=NTS0 
                               IS2=NTS0
                               XMAX2=CX2(IC)
                               XMIN2=-CX1(IC)
                               YMAX2=CY2(JC)
                               YMIN2=-CY1(JC)
                               ZMAX2=CZ2(KC)
                               ZMIN2=-CZ1(KC)
                               DO IS=NTSINI+1,NTS0
                                  SUMX=0.0_W_P
                                  SUMY=0.0_W_P
                                  SUMZ=0.0_W_P
                                  DO IV=1,NIPV0(IS) 
                                     IP=IPV0(IS,IV) 
                                     IP0=IPIA0(IP) 
                                     IP1=IPIA1(IP) 
                                     V0(1)=VERTP0(IP0,1) 
                                     V0(2)=VERTP0(IP0,2) 
                                     V0(3)=VERTP0(IP0,3) 
                                     V1(1)=VERTP0(IP1,1) 
                                     V1(2)=VERTP0(IP1,2) 
                                     V1(3)=VERTP0(IP1,3)
                                     CALL INTEPFUNC3D(CPARAB,VN,V0,V1,  &
                                          VI)
                                     VERTP0(IP,1)=VI(1) 
                                     VERTP0(IP,2)=VI(2) 
                                     VERTP0(IP,3)=VI(3) 
                                     SUMX=SUMX+VERTP0(IP,1)
                                     SUMY=SUMY+VERTP0(IP,2)
                                     SUMZ=SUMZ+VERTP0(IP,3)
                                  END DO
                                  NTP0=NTP0+1
                                  VERTP0(NTP0,1)=SUMX/NIPV0(IS)
                                  VERTP0(NTP0,2)=SUMY/NIPV0(IS)
                                  VERTP0(NTP0,3)=SUMZ/NIPV0(IS)
                                  V0(1)=VERTP0(NTP0,1)
                                  V0(2)=VERTP0(NTP0,2)
                                  V0(3)=VERTP0(NTP0,3)
                                  CALL FINDBRACKETP(CPARAB,VN,DD/REAL(  &
                                       NCL,KIND=W_P),IEBRACKET,V0,V1)
                                  IF(IEBRACKET.EQ.2) THEN 
                                     VI=V1 
                                  ELSEIF(IEBRACKET.EQ.1) THEN
                                     CALL INTEPFUNC3D(CPARAB,VN,V0,V1,  &
                                          VI)
                                  ELSE
                                     VI=V0
                                  END IF
                                  VERTP0(NTP0,1)=VI(1) 
                                  VERTP0(NTP0,2)=VI(2) 
                                  VERTP0(NTP0,3)=VI(3)
                                  ISINI=IS2+1
                                  DO IV=1,NIPV0(IS)
                                     IS2=IS2+1
                                     IV2=IV+1
                                     IF(IV2.GT.NIPV0(IS)) IV2=1
                                     NIPV0(IS2)=3
                                     IPV0(IS2,1)=NTP0
                                     IPV0(IS2,2)=IPV0(IS,IV)
                                     IPV0(IS2,3)=IPV0(IS,IV2)
                                     XV1=VERTP0(IPV0(IS2,2),1)-         &
                                          VERTP0(IPV0(IS2,1),1)
                                     YV1=VERTP0(IPV0(IS2,2),2)-         &
                                          VERTP0(IPV0(IS2,1),2)
                                     ZV1=VERTP0(IPV0(IS2,2),3)-         &
                                          VERTP0(IPV0(IS2,1),3)
                                     XV2=VERTP0(IPV0(IS2,3),1)-         &
                                          VERTP0(IPV0(IS2,2),1)
                                     YV2=VERTP0(IPV0(IS2,3),2)-         &
                                          VERTP0(IPV0(IS2,2),2)
                                     ZV2=VERTP0(IPV0(IS2,3),3)-         &
                                          VERTP0(IPV0(IS2,2),3)
                                     XM=YV1*ZV2-ZV1*YV2
                                     YM=ZV1*XV2-XV1*ZV2
                                     ZM=XV1*YV2-YV1*XV2
                                     AMOD=(XM**2+YM**2+ZM**2)**0.5_W_P
                                     IF(AMOD.NE.0.0_W_P) THEN
                                        XNS0(IS2)=XM/AMOD
                                        YNS0(IS2)=YM/AMOD
                                        ZNS0(IS2)=ZM/AMOD
                                     ELSE
                                        XNS0(IS2)=XM
                                        YNS0(IS2)=YM
                                        ZNS0(IS2)=ZM
                                     END IF
                                  END DO
                                  !* Cancel the IS face
                                  IF(IS2.GT.IS) NIPV0(IS)=0
                               END DO
                               NTS0=IS2
                            END IF
                            CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,VOLF,   &
                                 XNS0,YNS0,ZNS0)
                            VF=VF+VOLF 
                         END IF
                      END IF
                   END IF
                END DO
             END IF
          END IF
       END DO
    END DO
    RETURN 
  END SUBROUTINE INTPV3DPAOLD
!------------------------- END OF INTPV3DPAOLD --------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                             INTPV3DPA                               | 
! Volume of the polyhedral approximation of the region of intersection|
! between a paraboloid and an arbitrary polyhedron                    |
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! IPV      = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NC       = number of sub-cells along each coordinate axis of the    | 
!            superimposed Cartesian grid                              | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = vertex coordinates of the original polyhedron            | 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  | 
! On return:                                                          | 
!===========                                                          | 
! VF       = volume of intersection                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INTPV3DPA(CPARAB,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF,XNS,YNS, &
       ZNS) BIND(C)                                         
    !.. Scalar Arguments                                                    
    REAL (W_P), INTENT(IN) :: CPARAB(12)
    REAL(W_P), INTENT(OUT) :: VF 
    INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
    !.. Local Scalars                                                       
    REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DMOD,DVP,DVPMAX,DVPMIN,DX,DY,DZ,&
         SUMX,SUMY,SUMZ,TOLPHI,VOLF,X,XM,XMAX,XMAX2,XMIN,XMIN2,XP,   &
         XV1,XV2,Y,YM,YMAX,YMAX2,YMIN,YMIN2,YP,YV1,YV2,Z,ZM,ZMAX, &
         ZMAX2,ZMIN,ZMIN2,ZP,ZV1,ZV2
    INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IEBRACKET,IP,                    &
         IP0,IP1,IS,IS2,ISINI,IV,IV2,JC,KC,                             &
         NCL,NTP0,NTP1,NTP2,NTPT,                                       &
         NTS0,NTS1,NTS2,NTST,NTSINI,NTV0,NTV1,NTV2,NTVT                
    !LOGICAL :: ICONVEX
    !.. Local Arrays                                                        
    REAL(W_P) :: CI1(NC),CI2(NC),CJ1(NC),CJ2(NC),CK1(NC),CK2(NC),       &
         CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC),CX2(NC),        &
         CY1(NC),CY2(NC),CZ1(NC),CZ2(NC),PHIV(NV),PHIVMIN(NS),V(8,3),   &
         V0(3),V1(3),VI(3),VNI(3),VNJ(3),VNK(3),VERTP0(NV,3),           &
         VERTP1(NV,3),VERTP2(NV,3),VERTPT(NV,3),VN(9),XNS0(NS),         &
         XNS1(NS),XNS2(NS),XNST(NS),YNS0(NS),YNS1(NS),YNS2(NS),         &
         YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),ZNST(NS)         
    INTEGER(I_P) :: IA(NV),ICHECK(NV),ICTAG(NC),IJKCLIM(6),IPIA0(NV),             &
         IPIA1(NV),IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),     &
         ISCONTN(NS),ISCONTP(NS),ISCUT(NS),ITAGP(NC,NC,NC),ITAGP2(NC,NC,NC),JCTAG(NC,NC),NIPV0(NS),   &
         NIPV1(NS),NIPV2(NS),NIPVT(NS)
    !REAL(W_P) :: DC,DCMAX,DCMIN,DCP,DF,DVF,DVFMAX,DVFMIN,R,XC,YC,ZC
    TOLPHI=1.0E-16_W_P
    !.. Coordinate extremes of the cell and vertex tagging                  
    NCL=NC 
    VF=0.0_W_P 
    XMIN=1.0E+20_W_P 
    XMAX=-1.0E+20_W_P 
    YMIN=1.0E+20_W_P 
    YMAX=-1.0E+20_W_P 
    ZMIN=1.0E+20_W_P 
    ZMAX=-1.0E+20_W_P 
    ICONTP=0 
    ICONTN=0 
    V0(1)=0.0_W_P 
    V0(2)=0.0_W_P 
    V0(3)=0.0_W_P 
    DO IP=1,NTP 
       ICHECK(IP)=0 
    END DO
    !Paraboloid orthonormal basis
    VN(1)=CPARAB(7) 
    VN(2)=CPARAB(8) 
    VN(3)=CPARAB(9) 
    VN(4)=VN(2)
    VN(5)=-VN(1)
    VN(6)=0.0_W_P
    DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
    IF(DMOD.NE.0.0_W_P) THEN
       VN(4)=VN(4)/DMOD
       VN(5)=VN(5)/DMOD
    ELSE
       VN(4)=VN(3)
       VN(5)=0.0_W_P
       VN(6)=-VN(1)
       DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
       VN(4)=VN(4)/DMOD
       VN(6)=VN(6)/DMOD
    END IF
    VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
    VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
    VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
    
    DO IS=1,NTS
       ISCONTP(IS)=0
       ISCONTN(IS)=0
       PHIVMIN(IS)=1.0E+20_W_P
       CS(IS)=-XNS(IS)*VERTP(IPV(IS,1),1)-YNS(IS)*VERTP(IPV(IS,1),2)    &
            -ZNS(IS)*VERTP(IPV(IS,1),3)
       DO IV=1,NIPV(IS) 
          IP=IPV(IS,IV) 
          IF(ICHECK(IP).EQ.0) THEN 
             ICHECK(IP)=1 
             XP=VERTP(IP,1) 
             YP=VERTP(IP,2) 
             ZP=VERTP(IP,3) 
             XMIN=DMIN1(XMIN,XP) 
             XMAX=DMAX1(XMAX,XP) 
             YMIN=DMIN1(YMIN,YP) 
             YMAX=DMAX1(YMAX,YP) 
             ZMIN=DMIN1(ZMIN,ZP) 
             ZMAX=DMAX1(ZMAX,ZP)
             IF(NC.EQ.1) THEN
                CALL PFUNC3D(PHIV(IP),CPARAB,VN,XP,YP,ZP)
                IF(PHIV(IP).GT.0.0_W_P) THEN 
                   IA(IP)=1 
                   ICONTP=ICONTP+1 
                ELSE 
                   IA(IP)=0 
                   ICONTN=ICONTN+1 
                END IF
             END IF
          END IF
       END DO
    END DO
    !.. initialization                                                      
    DX=XMAX-XMIN 
    DY=YMAX-YMIN 
    DZ=ZMAX-ZMIN 
    DD=0.01*MIN(DX,DY,DZ)
    IF(DD.LT.1.0E-20_W_P) THEN
       VF=0.0_W_P 
       RETURN 
    END IF
    CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,NTS,NTVT,     &
         NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)
    DDX=DX/REAL(NCL,KIND=W_P) 
    DDY=DY/REAL(NCL,KIND=W_P) 
    DDZ=DZ/REAL(NCL,KIND=W_P) 
    DO I=1,NCL 
       IF(I.EQ.1) THEN 
          CX1(I)=-XMIN 
       ELSE 
          CX1(I)=CX1(I-1)-DDX 
       END IF
       CX2(I)=-CX1(I)+DDX 
    END DO
    DO I=1,NCL 
       IF(I.EQ.1) THEN 
          CY1(I)=-YMIN 
       ELSE 
          CY1(I)=CY1(I-1)-DDY 
       END IF
       CY2(I)=-CY1(I)+DDY 
    END DO
    DO I=1,NCL 
       IF(I.EQ.1) THEN 
          CZ1(I)=-ZMIN 
       ELSE 
          CZ1(I)=CZ1(I-1)-DDZ 
       END IF
       CZ2(I)=-CZ1(I)+DDZ 
    END DO
    IJKCLIM(1)=1
    IJKCLIM(2)=NCL
    IJKCLIM(3)=1
    IJKCLIM(4)=NCL
    IJKCLIM(5)=1
    IJKCLIM(6)=NCL
    VNI(:)=[1.0_W_P,0.0_W_P,0.0_W_P]
    VNJ(:)=[0.0_W_P,1.0_W_P,0.0_W_P]
    VNK(:)=[0.0_W_P,0.0_W_P,1.0_W_P]
    CI1(:)=CX1(:)
    CI2(:)=CX2(:)
    CJ1(:)=CY1(:)
    CJ2(:)=CY2(:)
    CK1(:)=CZ1(:)
    CK2(:)=CZ2(:)

    !sub-cell tagging:
    ITAGP(IJKCLIM(1):IJKCLIM(2),IJKCLIM(3):IJKCLIM(4),IJKCLIM(5):       &
         IJKCLIM(6))=0
    ITAGP2(IJKCLIM(1):IJKCLIM(2),IJKCLIM(3):IJKCLIM(4),IJKCLIM(5):       &
         IJKCLIM(6))=0
!    R=0.866025403784_W_P*MAX(DDX,DDY,DDZ) !circunscrit ball radius (smallest
!                                          !sphere that contains all the Pijk
!                                          !vertices)
!    DO IC=IJKCLIM(1),IJKCLIM(2) 
!       DO JC=IJKCLIM(3),IJKCLIM(4) 
!          DO KC=IJKCLIM(5),IJKCLIM(6)
!             !circunscrit ball center
!             XC=XMIN+DDX*(REAL(IC,KIND=W_P)-0.5_W_P)
!             YC=YMIN+DDY*(REAL(JC,KIND=W_P)-0.5_W_P)
!             ZC=ZMIN+DDZ*(REAL(KC,KIND=W_P)-0.5_W_P)
!             CALL PFUNC3D(DC,CPARAB,VN,XC,YC,ZC)
!             DCMIN=1.0E+20_W_P
!             DO IS=1,NTS
!                DF=XNS(IS)*XC+YNS(IS)*YC+ZNS(IS)*ZC+CS(IS)
!                !                   IF(ICONVEX.AND.DF.GE.R) THEN
!                !                      ITAGP(IC,JC,KC)=2
!                !                      GOTO 10
!                !                   END IF
!                DCMIN=MIN(DCMIN,DF)
!             END DO
!             IF(DC.GE.R.AND.DCMIN.GE.R) THEN
!                ITAGP(IC,JC,KC)=1
!                GOTO 10
!             END IF
!             IF(DC.LE.-R.AND.DCMIN.GE.R) THEN
!                ITAGP(IC,JC,KC)=2
!                GOTO 10
!             END IF
!10           CONTINUE
!          END DO
!       END DO
!    END DO
    DO IC=IJKCLIM(1),IJKCLIM(2) 
       DO JC=IJKCLIM(3),IJKCLIM(4) 
          DO KC=IJKCLIM(5),IJKCLIM(6)
!             IF(ITAGP(IC,JC,KC).EQ.0) THEN
             V(1,:)=[XMAX+DDX*REAL(IC-NCL,KIND=W_P),YMIN+DDY*REAL(JC-1, &
                  KIND=W_P),ZMAX+DDZ*REAL(KC-NCL,KIND=W_P)]
             V(2,:)=[XMAX+DDX*REAL(IC-NCL,KIND=W_P),YMIN+DDY*REAL(JC-1, &
                  KIND=W_P),ZMIN+DDZ*REAL(KC-1,KIND=W_P)]
             V(3,:)=[XMAX+DDX*REAL(IC-NCL,KIND=W_P),YMAX+DDY*REAL(JC-NCL&
                  ,KIND=W_P),ZMIN+DDZ*REAL(KC-1,KIND=W_P)]
             V(4,:)=[XMAX+DDX*REAL(IC-NCL,KIND=W_P),YMAX+DDY*REAL(JC-NCL&
                  ,KIND=W_P),ZMAX+DDZ*REAL(KC-NCL,KIND=W_P)]
             V(5,:)=[XMIN+DDX*REAL(IC-1,KIND=W_P),YMIN+DDY*REAL(JC-1,   &
                  KIND=W_P),ZMAX+DDZ*REAL(KC-NCL,KIND=W_P)]
             V(6,:)=[XMIN+DDX*REAL(IC-1,KIND=W_P),YMIN+DDY*REAL(JC-1,   &
                  KIND=W_P),ZMIN+DDZ*REAL(KC-1,KIND=W_P)]
             V(7,:)=[XMIN+DDX*REAL(IC-1,KIND=W_P),YMAX+DDY*REAL(JC-NCL, &
                  KIND=W_P),ZMIN+DDZ*REAL(KC-1,KIND=W_P)]
             V(8,:)=[XMIN+DDX*REAL(IC-1,KIND=W_P),YMAX+DDY*REAL(JC-NCL, &
                  KIND=W_P),ZMAX+DDZ*REAL(KC-NCL,KIND=W_P)]
             DVPMIN=1.0E+20_W_P
             DVPMAX=-1.0E+20_W_P
!             DVFMIN=1.0E+20_W_P
             DO IV=1,8
                CALL PFUNC3D(DVP,CPARAB,VN,V(IV,1),V(IV,2),V(IV,3))
                DVPMAX=MAX(DVPMAX,DVP)
                DVPMIN=MIN(DVPMIN,DVP)
             END DO
             IF(DVPMAX.LE.0) THEN
                ITAGP(IC,JC,KC)=2
             ELSEIF(DVPMIN.GE.0) THEN
                ITAGP2(IC,JC,KC)=1
                DO IV=1,8
                   DO IS=1,NTS
                      IF((XNS(IS)*V(IV,1)+YNS(IS)*V(IV,2)+ZNS(IS)*      &
                           V(IV,3)+CS(IS)).GT.0.0_W_P) GOTO 20
                   END DO
                END DO
                ITAGP(IC,JC,KC)=1                
20              CONTINUE
             END IF
!                DO IS=1,NTS
!                   DVFMAX=-1E+20_W_P
!                   DO IV=1,8
!                      DVF=XNS(IS)*V(IV,1)+YNS(IS)*V(IV,2)+ZNS(IS)*      &
!                           V(IV,3)+CS(IS)
!                      DVFMIN=MIN(DVFMIN,DVF)
!                      DVFMAX=MAX(DVFMAX,DVF)
!                   END DO
!!                   IF(ICONVEX.AND.DVFMAX.LE.0) THEN
!!                      ITAGP(IC,JC,KC)=2
!!                      GOTO 20
!!                   END IF
!                END DO
!                IF(DVPMIN.GE.R.AND.DVFMIN.GE.0) ITAGP(IC,JC,KC)=1
!             END IF
!20           CONTINUE
          END DO
       END DO
    END DO
    ICTAG(:)=0
    JCTAG(:,:)=0
    DO IC=IJKCLIM(1),IJKCLIM(2)
       IF(PRODUCT(ITAGP(IC,:,:)).NE.0) THEN
          IF(SUM(ITAGP(IC,:,:)).EQ.NCL*NCL) THEN
             VF=VF+DDX*DY*DZ
             ICTAG(IC)=1
             GOTO 25
          END IF
          IF(SUM(ITAGP(IC,:,:)).EQ.2*NCL*NCL) THEN
             ICTAG(IC)=2
             GOTO 25
          END IF
       END IF
       DO JC=IJKCLIM(3),IJKCLIM(4) 
          IF(PRODUCT(ITAGP(IC,JC,:)).NE.0) THEN
             IF(SUM(ITAGP(IC,JC,:)).EQ.NCL) THEN
                VF=VF+DDX*DDY*DZ
                JCTAG(IC,JC)=1
             ELSEIF(SUM(ITAGP(IC,JC,:)).EQ.2*NCL) THEN
                JCTAG(IC,JC)=2
             END IF
          END IF
       END DO
25     CONTINUE
    END DO             
    !----------

    
    DO IC=IJKCLIM(1),IJKCLIM(2)
       IF(ICTAG(IC).NE.0) GOTO 30
       IF(NCL.EQ.1) THEN 
          CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,    &
               NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,        &
               ZNS0,ZNST)                                                  
       ELSE 
          CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,    &
               NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,        &
               ZNS2,ZNST)                                                  
       END IF
       IF(IC.GT.1) CALL INTE3D(CI1(IC),ICONTN,ICONTP,IPV2,NIPV2,        &
            NTP2,NTS2,NTV2,VERTP2,VNI(1),XNS2,VNI(2),YNS2,VNI(3),ZNS2)        
       IF(IC.LT.NCL) CALL INTE3D(CI2(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
            NTS2,NTV2,VERTP2,-VNI(1),XNS2,-VNI(2),YNS2,-VNI(3),ZNS2)  
       DO JC=IJKCLIM(3),IJKCLIM(4)
          IF(JCTAG(IC,JC).NE.0) GOTO 40
          IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,      &
               NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,        &
               XNS2,YNS1,YNS2,ZNS1,ZNS2)                                   
          IF(JC.GT.1) CALL INTE3D(CJ1(JC),ICONTN,ICONTP,IPV1,NIPV1,NTP1,&
               NTS1,NTV1,VERTP1,VNJ(1),XNS1,VNJ(2),YNS1,VNJ(3),ZNS1)
          IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
             IF(JC.LT.NCL) CALL INTE3D(CJ2(JC),ICONTN,ICONTP,IPV1,      &
                  NIPV1,NTP1,NTS1,NTV1,VERTP1,-VNJ(1),XNS1,-VNJ(2),     &
                  YNS1,-VNJ(3),ZNS1)                                         
             IF(ICONTP.NE.0) THEN 
                DO KC=IJKCLIM(5),IJKCLIM(6)                 
!                   IF(ITAGP(IC,JC,KC).NE.0) THEN
                   IF(ITAGP(IC,JC,KC).EQ.1) THEN
                      VF=VF+DDX*DDY*DDZ
                      GOTO 50
                   END IF
                   IF(ITAGP(IC,JC,KC).EQ.2)  GOTO 50
                   IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0,   &
                        NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,     &
                        VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                   IF(KC.GT.1) CALL INTE3D(CK1(KC),ICONTN,ICONTP,IPV0,  &
                        NIPV0,NTP0,NTS0,NTV0,VERTP0,VNK(1),XNS0,        &
                        VNK(2),YNS0,VNK(3),ZNS0)                              
                   IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                      IF(KC.LT.NCL) CALL INTE3D(CK2(KC),ICONTN,ICONTP,  &
                           IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,-VNK(1),    &
                           XNS0,-VNK(2),YNS0,-VNK(3),ZNS0)               
                      IF(ICONTP.NE.0) THEN 
                         !..   Subcell determination by truncation  
!                         IF(NCL.GT.1.and.itagp2(ic,jc,kc).eq.0) THEN 
                         IF(NCL.GT.1) THEN 
                            ICONTP=0 
                            ICONTN=0 
                            DO IP=1,NTP0 
                               ICHECK(IP)=0 
                            END DO
                            DO IS=1,NTS0 
                               DO IV=1,NIPV0(IS) 
                                  IP=IPV0(IS,IV) 
                                  IF(ICHECK(IP).EQ.0) THEN 
                                     ICHECK(IP)=1 
                                     X=VERTP0(IP,1) 
                                     Y=VERTP0(IP,2) 
                                     Z=VERTP0(IP,3) 
                                     CALL PFUNC3D(PHIV(IP),CPARAB,VN,   &
                                          X,Y,Z)
                                     IF(PHIV(IP).GT.0.0_W_P) THEN 
                                        IA(IP)=1 
                                        ICONTP=ICONTP+1 
                                     ELSE 
                                        IA(IP)=0 
                                        ICONTN=ICONTN+1 
                                     END IF
                                  END IF
                               END DO
                            END DO
                         END IF
!                         IF(ICONTN.EQ.0.or.itagp2(ic,jc,kc).eq.1) THEN 
                         IF(ICONTN.EQ.0) THEN 
                            CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,        &
                                 VOLF,XNS0,YNS0,ZNS0)                 
                            VF=VF+VOLF 
                         ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                            NTSINI=NTS0
                            CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,ISCUT,    &
                                 NIPV0,NTP0,NTS0,NTV0,1.0_W_P,XNS0,     &
                                 0.0_W_P,YNS0,0.0_W_P,ZNS0)
                            !.. Location of the new intersection points   
                            IF(NTS0.GT.NTSINI) THEN 
                               IS=NTS0 
                               IS2=NTS0
                               XMAX2=CX2(IC)
                               XMIN2=-CX1(IC)
                               YMAX2=CY2(JC)
                               YMIN2=-CY1(JC)
                               ZMAX2=CZ2(KC)
                               ZMIN2=-CZ1(KC)
                               DO IS=NTSINI+1,NTS0
                                  SUMX=0.0_W_P
                                  SUMY=0.0_W_P
                                  SUMZ=0.0_W_P
                                  DO IV=1,NIPV0(IS) 
                                     IP=IPV0(IS,IV) 
                                     IP0=IPIA0(IP) 
                                     IP1=IPIA1(IP) 
                                     V0(1)=VERTP0(IP0,1) 
                                     V0(2)=VERTP0(IP0,2) 
                                     V0(3)=VERTP0(IP0,3) 
                                     V1(1)=VERTP0(IP1,1) 
                                     V1(2)=VERTP0(IP1,2) 
                                     V1(3)=VERTP0(IP1,3)
                                     CALL INTEPFUNC3D(CPARAB,VN,V0,V1,  &
                                          VI)
                                     VERTP0(IP,1)=VI(1) 
                                     VERTP0(IP,2)=VI(2) 
                                     VERTP0(IP,3)=VI(3) 
                                     SUMX=SUMX+VERTP0(IP,1)
                                     SUMY=SUMY+VERTP0(IP,2)
                                     SUMZ=SUMZ+VERTP0(IP,3)
                                  END DO
                                  NTP0=NTP0+1
                                  VERTP0(NTP0,1)=SUMX/NIPV0(IS)
                                  VERTP0(NTP0,2)=SUMY/NIPV0(IS)
                                  VERTP0(NTP0,3)=SUMZ/NIPV0(IS)
                                  V0(1)=VERTP0(NTP0,1)
                                  V0(2)=VERTP0(NTP0,2)
                                  V0(3)=VERTP0(NTP0,3)
                                  CALL FINDBRACKETP(CPARAB,VN,DD/REAL(  &
                                       NCL,KIND=W_P),IEBRACKET,V0,V1)
                                  IF(IEBRACKET.EQ.2) THEN 
                                     VI=V1 
                                  ELSEIF(IEBRACKET.EQ.1) THEN
                                     CALL INTEPFUNC3D(CPARAB,VN,V0,V1,  &
                                          VI)
                                  ELSE
                                     VI=V0
                                  END IF
                                  VERTP0(NTP0,1)=VI(1) 
                                  VERTP0(NTP0,2)=VI(2) 
                                  VERTP0(NTP0,3)=VI(3)
                                  ISINI=IS2+1
                                  DO IV=1,NIPV0(IS)
                                     IS2=IS2+1
                                     IV2=IV+1
                                     IF(IV2.GT.NIPV0(IS)) IV2=1
                                     NIPV0(IS2)=3
                                     IPV0(IS2,1)=NTP0
                                     IPV0(IS2,2)=IPV0(IS,IV)
                                     IPV0(IS2,3)=IPV0(IS,IV2)
                                     XV1=VERTP0(IPV0(IS2,2),1)-         &
                                          VERTP0(IPV0(IS2,1),1)
                                     YV1=VERTP0(IPV0(IS2,2),2)-         &
                                          VERTP0(IPV0(IS2,1),2)
                                     ZV1=VERTP0(IPV0(IS2,2),3)-         &
                                          VERTP0(IPV0(IS2,1),3)
                                     XV2=VERTP0(IPV0(IS2,3),1)-         &
                                          VERTP0(IPV0(IS2,2),1)
                                     YV2=VERTP0(IPV0(IS2,3),2)-         &
                                          VERTP0(IPV0(IS2,2),2)
                                     ZV2=VERTP0(IPV0(IS2,3),3)-         &
                                          VERTP0(IPV0(IS2,2),3)
                                     XM=YV1*ZV2-ZV1*YV2
                                     YM=ZV1*XV2-XV1*ZV2
                                     ZM=XV1*YV2-YV1*XV2
                                     AMOD=(XM**2+YM**2+ZM**2)**0.5_W_P
                                     IF(AMOD.NE.0.0_W_P) THEN
                                        XNS0(IS2)=XM/AMOD
                                        YNS0(IS2)=YM/AMOD
                                        ZNS0(IS2)=ZM/AMOD
                                     ELSE
                                        XNS0(IS2)=XM
                                        YNS0(IS2)=YM
                                        ZNS0(IS2)=ZM
                                     END IF
                                  END DO
                                  !* Cancel the IS face
                                  IF(IS2.GT.IS) NIPV0(IS)=0
                               END DO
                               NTS0=IS2
                            END IF
                            CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,VOLF,   &
                                 XNS0,YNS0,ZNS0)
                            VF=VF+VOLF 
                         END IF
                      END IF
                   END IF
50                 CONTINUE
                END DO ! do kc
             END IF
          END IF
40        CONTINUE
       END DO ! do jc
30     CONTINUE
    END DO ! do ic
    RETURN 
  END SUBROUTINE INTPV3DPA
!------------------------- END OF INTPV3DPA --------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            FINDBRACKETP                             | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! VN       = paraboloid orthonormal basis                             |
! DD       = differential size                                        | 
! V0       = vertex coordinates of the initial point                  | 
! On return:                                                          | 
!===========                                                          | 
! IEBRACKET= 2, the root is found                                     | 
!            1, the bracket is found                                  | 
!            0, the bracket is not found                              | 
!           -1, null space gradient case                              | 
! V0       = vertex coordinates of the relocated initial point        | 
! V1       = vertex coordinates of the final point with FUNC3D value  | 
!            of different sign                                        | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE FINDBRACKETP(CPARAB,VN,DD,IEBRACKET,V0,V1) BIND(C) 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: DD 
    INTEGER(I_P), INTENT(OUT) :: IEBRACKET 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: CPARAB(12),VN(9) 
    REAL(W_P), INTENT(INOUT) :: V0(3) 
    REAL(W_P), INTENT(OUT) :: V1(3) 
    !.. Local Scalars                                                       
    REAL(W_P) :: BBALL,DFF,DFU,DFV,DFX,DFY,DFZ,DMOD,F,F0,F0INI,F1,      &
         TOLB,U,V,XT,YT,ZT 
    INTEGER(I_P) :: ITER,NITER 
    !.. Local Arrays                                                        
    REAL(W_P) :: V00(3)                                              
    !. normal computation                                                   
    NITER=10 
    ITER=0 
    V00=V0                                                           
    TOLB=1E-12_W_P
    BBALL=DD*50.0_W_P
    
    XT=V0(1)-CPARAB(10)
    YT=V0(2)-CPARAB(11)
    ZT=V0(3)-CPARAB(12)
    F=XT*VN(1)+YT*VN(2)+ZT*VN(3)
    U=XT*VN(4)+YT*VN(5)+ZT*VN(6)
    V=XT*VN(7)+YT*VN(8)+ZT*VN(9)
    DFU=-CPARAB(2)-2.0_W_P*CPARAB(4)*U-CPARAB(5)*V
    DFV=-CPARAB(3)-CPARAB(5)*U-2.0_W_P*CPARAB(6)*V
    DFF=1.0_W_P
    DFX=VN(1)*DFF+VN(4)*DFU+VN(7)*DFV
    DFY=VN(2)*DFF+VN(5)*DFU+VN(8)*DFV
    DFZ=VN(3)*DFF+VN(6)*DFU+VN(9)*DFV
    DMOD=(DFX**2+DFY**2+DFZ**2)**0.5_W_P 
    IF(DMOD.NE.0.0_W_P) THEN 
       !. find bracket                                                         
       DFX=DFX/DMOD 
       DFY=DFY/DMOD 
       DFZ=DFZ/DMOD 
       CALL PFUNC3D(F0,CPARAB,VN,V0(1),V0(2),V0(3))
       F0INI=F0 
10     CONTINUE 
       ITER=ITER+1 
       V1(1)=V0(1)-DFX*SIGN(MAX(ABS(F0),DD),F0) 
       V1(2)=V0(2)-DFY*SIGN(MAX(ABS(F0),DD),F0) 
       V1(3)=V0(3)-DFZ*SIGN(MAX(ABS(F0),DD),F0)  
       IF(((V00(1)-V1(1))**2+(V00(2)-V1(2))**2+(V00(3)-V1(3))**2)**     &
            0.5_W_P.GT.BBALL) THEN
          IEBRACKET=0
          RETURN
       END IF
       CALL PFUNC3D(F1,CPARAB,VN,V1(1),V1(2),V1(3))
       IF(ABS(F1).LT.TOLB) THEN 
          IEBRACKET=2 
          RETURN 
       END IF
       IF(F1*F0INI.LE.0.0_W_P) THEN 
          IEBRACKET=1 
          RETURN 
       END IF
       IF(ITER.EQ.NITER.OR.(F0*F1.GT.0.0_W_P.AND.ABS(F1).GT.ABS(F0)))   &
            THEN 
          IEBRACKET=0 
          RETURN 
       END IF
       F0=F1 
       V0=V1 
       GOTO 10 
    ELSE 
       IEBRACKET=-1 
    END IF
    RETURN 
  END SUBROUTINE FINDBRACKETP
!----------------------- END OF FINDBRACKETP -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            INTEPFUNC3D                              | 
! Intersection between a paraboloid and the segment V0-V1             |
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CPARAB   = local paraboloid coefficients                            |
! VN       = paraboloid orthonormal basis                             |
! V0       = vertex coordinates of the initial point                  | 
! V1       = vertex coordinates of the next point along the segment   | 
!            where the intersection point is been located             | 
! On return:                                                          | 
!===========                                                          | 
! VI       = vertex coordinates of the point of intersection between  | 
!            the segment and the paraboloid interface                 | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INTEPFUNC3D(CPARAB,VN,V0,V1,VI) BIND(C) 
    !.. Array Arguments
    REAL(W_P), INTENT(IN) :: CPARAB(12),V0(3),V1(3),VN(9) 
    REAL(W_P), INTENT(OUT) :: VI(3)
    !.. Local Scalars                                                       
    REAL(W_P) :: A,B,C,D,DX,DY,DZ,T,XT,YT,ZT 
    !.. Local Arrays                                                        
    REAL(W_P) :: VL0(3),VL1(3),VLI(3)
    !. System transformation. From global (V) to local (VL)
    XT=V0(1)-CPARAB(10)
    YT=V0(2)-CPARAB(11) 
    ZT=V0(3)-CPARAB(12) 
    VL0(3)=XT*VN(1)+YT*VN(2)+ZT*VN(3) 
    VL0(1)=XT*VN(4)+YT*VN(5)+ZT*VN(6) 
    VL0(2)=XT*VN(7)+YT*VN(8)+ZT*VN(9) 
    
    XT=V1(1)-CPARAB(10)
    YT=V1(2)-CPARAB(11) 
    ZT=V1(3)-CPARAB(12) 
    VL1(3)=XT*VN(1)+YT*VN(2)+ZT*VN(3) 
    VL1(1)=XT*VN(4)+YT*VN(5)+ZT*VN(6) 
    VL1(2)=XT*VN(7)+YT*VN(8)+ZT*VN(9) 
    
    DX=VL1(1)-VL0(1)
    DY=VL1(2)-VL0(2)
    DZ=VL1(3)-VL0(3)
    A=CPARAB(4)*DX**2+CPARAB(5)*DX*DY+CPARAB(6)*DY**2
    B=CPARAB(2)*DX+CPARAB(3)*DY+2.0_W_P*CPARAB(4)*VL0(1)*DX+CPARAB(5)   &
         *VL0(1)*DY+CPARAB(5)*VL0(2)*DX+2.0_W_P*CPARAB(6)*VL0(2)*DY-DZ
    C=CPARAB(1)+CPARAB(2)*VL0(1)+CPARAB(3)*VL0(2)+CPARAB(4)*VL0(1)**2+  &
         CPARAB(5)*VL0(1)*VL0(2)+CPARAB(6)*VL0(2)**2-VL0(3)
    D=B**2-4.0_W_P*A*C
    T=-1.0_W_P
    IF(ABS(A).LT.1.0E-16_W_P.AND.B.NE.0.0_W_P) THEN
       T=-C/B
    ELSEIF(A.NE.0.0_W_P.AND.D.GT.0.0_W_P) THEN
       T=(-B-D**0.5_W_P)/(2.0_W_P*A)
       IF(T.LT.0.0_W_P.OR.T.GT.1.0_W_P) T=(-B+D**0.5_W_P)/(2.0_W_P*A)
    END IF
    IF(T.GE.0.0_W_P.AND.T.LE.1.0_W_P) THEN
       VLI(1)=VL0(1)+T*DX
       VLI(2)=VL0(2)+T*DY
       VLI(3)=VL0(3)+T*DZ
    ELSE
       !Choose starting point closest to interface
       CALL PFUNC3D(A,CPARAB,VN,V0(1),V0(2),V0(3))
       CALL PFUNC3D(B,CPARAB,VN,V1(1),V1(2),V1(3))
       IF(ABS(A).LT.ABS(B)) THEN
          VI=V0
          RETURN
       ELSE
          VI=V1
          RETURN
       END IF
    END IF
    !. System transformation. From local (VL) to global (V)
    VI(1)=VN(1)*VLI(3)+VN(4)*VLI(1)+VN(7)*VLI(2)
    VI(2)=VN(2)*VLI(3)+VN(5)*VLI(1)+VN(8)*VLI(2)
    VI(3)=VN(3)*VLI(3)+VN(6)*VLI(1)+VN(9)*VLI(2)
    VI(1)=VI(1)+CPARAB(10)
    VI(2)=VI(2)+CPARAB(11)
    VI(3)=VI(3)+CPARAB(12)
    RETURN 
  END SUBROUTINE INTEPFUNC3D
!------------------------ END OF INTEPFUNC3D -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              TOOLV3D                                | 
!---------------------------------------------------------------------| 
!          This routine computes the volume of a polyhedron           | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! VERTI    = vertex coordinates of the polyhedron                     | 
! XNS, ... = unit-lenght normals to the faces of the polyhedron       | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTS      = total number of faces                                    | 
! On return:                                                          | 
!===========                                                          | 
! VOL      = volume of the polyhedron                                 | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE TOOLV3D(IPV,NIPV,NTS,VERTI,VOL,XNS,YNS,ZNS) BIND(C) 
    ! .. Scalar Arguments ..                                                
    INTEGER(I_P), INTENT(IN) :: NTS 
    REAL(W_P), INTENT(OUT) :: VOL 
    ! .. Array Arguments ..                                                 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(IN) :: VERTI(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    ! .. Local Scalars ..                                                   
    INTEGER(I_P) :: I,IH,IP,IP1,IP2,IPROJ,IS 
    REAL(W_P) :: CNMAX,DNMAX,SUMP,SUMS,TOL,XV1,XV2,YV1,YV2,ZV1,ZV2 
    
    TOL=1.0E-16_W_P 
    SUMS=0.0_W_P
    DO 20 IS=1,NTS 
       IF(NIPV(IS).GT.0) THEN 
          SUMP=0.0_W_P 
          CNMAX=0.0_W_P
          IF(ABS(YNS(IS)).GE.ABS(XNS(IS)).AND.ABS(YNS(IS)).GE.          &
               ABS(ZNS(IS))) THEN                                     
             IPROJ=2 
             DNMAX=YNS(IS) 
             IF(ABS(DNMAX).GT.TOL) CNMAX=VERTI(IPV(IS,1),2)+(XNS(IS)*   &
                  VERTI(IPV(IS,1),1)+ZNS(IS)*VERTI(IPV(IS,1),3))/DNMAX   
          ELSEIF(ABS(ZNS(IS)).GE.ABS(XNS(IS)).AND.ABS(ZNS(IS)).GE.      &
               ABS(YNS(IS))) THEN                                     
             IPROJ=3 
             DNMAX=ZNS(IS) 
             IF(ABS(DNMAX).GT.TOL) CNMAX=VERTI(IPV(IS,1),3)+(XNS(IS)*   &
                  VERTI(IPV(IS,1),1)+YNS(IS)*VERTI(IPV(IS,1),2))/DNMAX   
          ELSE 
             IPROJ=1 
             DNMAX=XNS(IS) 
             IF(ABS(DNMAX).GT.TOL) CNMAX=VERTI(IPV(IS,1),1)+(YNS(IS)*   &
                  VERTI(IPV(IS,1),2)+ZNS(IS)*VERTI(IPV(IS,1),3))/DNMAX   
          END IF
          IH=INT((NIPV(IS)-2)/2) 
          DO I=2,IH+1 
             IP=2*I 
             IP1=IP-1 
             IP2=IP-2 
             IF(IPROJ.EQ.1) THEN 
                YV1=VERTI(IPV(IS,IP1),2)-VERTI(IPV(IS,1),2) 
                ZV1=VERTI(IPV(IS,IP1),3)-VERTI(IPV(IS,1),3) 
                YV2=VERTI(IPV(IS,IP),2)-VERTI(IPV(IS,IP2),2) 
                ZV2=VERTI(IPV(IS,IP),3)-VERTI(IPV(IS,IP2),3) 
                SUMP=SUMP+YV1*ZV2-ZV1*YV2 
             ELSEIF(IPROJ.EQ.2) THEN 
                XV1=VERTI(IPV(IS,IP1),1)-VERTI(IPV(IS,1),1) 
                ZV1=VERTI(IPV(IS,IP1),3)-VERTI(IPV(IS,1),3) 
                XV2=VERTI(IPV(IS,IP),1)-VERTI(IPV(IS,IP2),1) 
                ZV2=VERTI(IPV(IS,IP),3)-VERTI(IPV(IS,IP2),3) 
                SUMP=SUMP+ZV1*XV2-XV1*ZV2 
             ELSE 
                XV1=VERTI(IPV(IS,IP1),1)-VERTI(IPV(IS,1),1) 
                YV1=VERTI(IPV(IS,IP1),2)-VERTI(IPV(IS,1),2) 
                XV2=VERTI(IPV(IS,IP),1)-VERTI(IPV(IS,IP2),1) 
                YV2=VERTI(IPV(IS,IP),2)-VERTI(IPV(IS,IP2),2) 
                SUMP=SUMP+XV1*YV2-YV1*XV2 
             END IF
          END DO
          IF(2*(IH+1).LT.NIPV(IS)) THEN 
             IF(IPROJ.EQ.1) THEN 
                YV1=VERTI(IPV(IS,NIPV(IS)),2)-VERTI(IPV(IS,1),2) 
                ZV1=VERTI(IPV(IS,NIPV(IS)),3)-VERTI(IPV(IS,1),3) 
                YV2=VERTI(IPV(IS,1),2)-VERTI(IPV(IS,NIPV(IS)-1),2) 
                ZV2=VERTI(IPV(IS,1),3)-VERTI(IPV(IS,NIPV(IS)-1),3) 
                SUMP=SUMP+YV1*ZV2-ZV1*YV2 
             ELSEIF(IPROJ.EQ.2) THEN 
                XV1=VERTI(IPV(IS,NIPV(IS)),1)-VERTI(IPV(IS,1),1) 
                ZV1=VERTI(IPV(IS,NIPV(IS)),3)-VERTI(IPV(IS,1),3) 
                XV2=VERTI(IPV(IS,1),1)-VERTI(IPV(IS,NIPV(IS)-1),1) 
                ZV2=VERTI(IPV(IS,1),3)-VERTI(IPV(IS,NIPV(IS)-1),3) 
                SUMP=SUMP+ZV1*XV2-XV1*ZV2 
             ELSE 
                XV1=VERTI(IPV(IS,NIPV(IS)),1)-VERTI(IPV(IS,1),1) 
                YV1=VERTI(IPV(IS,NIPV(IS)),2)-VERTI(IPV(IS,1),2) 
                XV2=VERTI(IPV(IS,1),1)-VERTI(IPV(IS,NIPV(IS)-1),1) 
                YV2=VERTI(IPV(IS,1),2)-VERTI(IPV(IS,NIPV(IS)-1),2) 
                SUMP=SUMP+XV1*YV2-YV1*XV2 
             END IF
          ENDIF
          IF(ABS(DNMAX).GT.TOL) SUMS=SUMS+CNMAX*SUMP 
       END IF
20  END DO
    VOL=SUMS/6.0_W_P 
    RETURN 
  END SUBROUTINE TOOLV3D
!-------------------------- END OF TOOLV3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                               INTV3D                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! C        = constant of the plane containing the new face \Gamma_c   | 
! IPV0     = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NIPV0    = number of vertices of each face                          | 
! NTP0     = last global vertex index                                 | 
! NTS0     = total number of faces                                    | 
! VERTP0   = vertex coordinates of the original polyhedron            | 
! XNC, ... = unit-lenght normal to the new face \Gamma_c              | 
! XNS0, ...= unit-lenght normals to the faces of the original pol.    | 
! On return:                                                          | 
!===========                                                          | 
! VOL      = volume of the truncated polyhedron                       | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INTV3D(C,IPV0,NIPV0,NTP0,NTS0,VERTP0,VOL,XNC,XNS0,         &
       YNC,YNS0,ZNC,ZNS0) BIND(C)                                   
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NTP0,NTS0 
    REAL(W_P), INTENT(IN) :: C,XNC,YNC,ZNC 
    REAL(W_P), INTENT(OUT) :: VOL 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPV0(NS,NV),NIPV0(NS) 
    REAL(W_P), INTENT(IN) :: XNS0(NS),YNS0(NS),ZNS0(NS) 
    REAL(W_P), INTENT(INOUT) :: VERTP0(NV,3) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,ICONTN,ICONTP,IH,IP,IP0,IP0I,IP1,IP1I,IP2,        &
         IPNEW,IPREF,IPROJ,IS,ISI,IV,IV1,NINT,NIPNEW,NISCUT,NISMIX,     &
         NIV,NTP1 
    REAL(W_P) :: CNMAX,DNMAX,SUMP,SUMS,TOL,XV1,XV2,YV1,YV2,ZV1,ZV2 
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IA(NV),IPIA0(NV),IPIA1(NV),IPV1(NS,NV),             &
         MARKIS(NS),NIPV1(NS),ISCUT(NS),ISMIX(NS)        
    INTEGER(I_P2) IPE(NV,NV) 
    REAL(W_P) :: PHIV(NV) 
    
    ICONTP=0 
    ICONTN=0 
    DO IP=1,NTP0 
       IA(IP)=-1 
    END DO
    !* Distance function and values of IA                                   
    DO IS=1,NTS0 
       DO IV=1,NIPV0(IS) 
          IP=IPV0(IS,IV) 
          IF(IA(IP).EQ.(-1)) THEN 
             PHIV(IP)=XNC*VERTP0(IP,1)+YNC*VERTP0(IP,2)+                &
                  ZNC*VERTP0(IP,3)+C                                  
             IF(PHIV(IP).GT.0.0_W_P) THEN 
                IA(IP)=1 
                ICONTP=ICONTP+1
                IF(ICONTP.EQ.1) IPREF=IP
             ELSE 
                IA(IP)=0 
                ICONTN=ICONTN+1 
             END IF
          END IF
       END DO
    END DO
    IF(ICONTP.EQ.0) THEN 
       VOL=0.0_W_P 
    ELSEIF(ICONTN.EQ.0) THEN 
       CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,VOL,XNS0,YNS0,ZNS0) 
    ELSE 
       !* Determination of the cut faces                                       
       NISCUT=0 
       NISMIX=0 
       DO IS=1,NTS0 
          MARKIS(IS)=0 
          IF(NIPV0(IS).GT.0) THEN 
             ISCUT(IS)=0 
             DO IV=1,NIPV0(IS) 
                IP=IPV0(IS,IV) 
                IV1=IV+1 
                IF(IV.EQ.NIPV0(IS)) IV1=1 
                IP1=IPV0(IS,IV1) 
                IF(IA(IP).NE.IA(IP1)) THEN 
                   IPE(IP,IP1)=0 
                   ISCUT(IS)=1 
                   NISCUT=NISCUT+1 
                END IF
             END DO
             IF(ISCUT(IS).EQ.0) THEN 
                IF(IA(IPV0(IS,1)).EQ.0) THEN 
                   NIPV1(IS)=0 
                ELSE 
                   NIPV1(IS)=NIPV0(IS) 
                   DO IV=1,NIPV0(IS) 
                      IPV1(IS,IV)=IPV0(IS,IV) 
                   END DO
                END IF
             ELSE 
                NISMIX=NISMIX+1 
                ISMIX(NISMIX)=IS 
             END IF
          ELSE 
             NIPV1(IS)=0 
          END IF
       END DO
       NIPNEW=NTP0 
       !* Disjoint regions may produce NISCUT=0 and both ICONTP and ICONTN \NEQ
       IF(NISCUT.EQ.0) GOTO 50 
       IPREF=NTP0+1 
       !* Construction of the cut faces                                        
       DO ISI=1,NISMIX 
          IS=ISMIX(ISI) 
          NIV=0 
          NINT=0 
          DO IV=1,NIPV0(IS) 
             IP=IPV0(IS,IV) 
             IV1=IV+1 
             IF(IV1.GT.NIPV0(IS))IV1=1 
             IP1=IPV0(IS,IV1) 
             IF(IA(IP).EQ.1) THEN 
                NIV=NIV+1 
                IPV1(IS,NIV)=IPV0(IS,IV) 
             END IF
             IF(IA(IP).NE.IA(IP1)) THEN 
                NINT=NINT+1 
                NIV=NIV+1 
                IF(IA(IP).EQ.1) THEN 
                   IP1I=IP 
                   IP0I=IP1 
                ELSE 
                   IP1I=IP1 
                   IP0I=IP 
                END IF
                IF(IPE(IP1,IP).NE.0) THEN 
                   IPNEW=IPE(IP1,IP) 
                   IPV1(IS,NIV)=IPNEW 
                   IF(IPNEW.EQ.IPREF) MARKIS(IS)=1 
                   GOTO 10 
                END IF
                NIPNEW=NIPNEW+1 
                IPE(IP,IP1)=INT(NIPNEW,KIND=I_P2) 
                IPIA0(NIPNEW)=IP0I 
                IPIA1(NIPNEW)=IP1I 
                IPV1(IS,NIV)=NIPNEW 
                IF(NIPNEW.EQ.IPREF) MARKIS(IS)=1 
             END IF
10           CONTINUE 
          END DO
          NIPV1(IS)=NIV 
       END DO
       !* Assign the vertices of the new truncated polyhedron                  
50     CONTINUE 
       NTP1=NIPNEW 
       !* Position of the new vertices                                         
       DO IP=NTP0+1,NTP1 
          IP0=IPIA0(IP) 
          IP1=IPIA1(IP) 
          VERTP0(IP,1)=VERTP0(IP0,1)-PHIV(IP0)*(VERTP0(IP1,1)-          &
               VERTP0(IP0,1))/(PHIV(IP1)-PHIV(IP0))                   
          VERTP0(IP,2)=VERTP0(IP0,2)-PHIV(IP0)*(VERTP0(IP1,2)-          &
               VERTP0(IP0,2))/(PHIV(IP1)-PHIV(IP0))                   
          VERTP0(IP,3)=VERTP0(IP0,3)-PHIV(IP0)*(VERTP0(IP1,3)-          &
               VERTP0(IP0,3))/(PHIV(IP1)-PHIV(IP0))                   
          !. Faces with less than 3 vertices are supressed. 
          IF(NIPV1(IS).LT.3) NIPV1(IS)=0 
       END DO
       !* Volume computation                                                   
       TOL=1.0E-16_W_P 
       SUMS=0.0_W_P
       DO IS=1,NTS0 
          IF(NIPV1(IS).GT.0.AND.MARKIS(IS).EQ.0) THEN 
             SUMP=0.0_W_P 
             CNMAX=0.0_W_P
             IF(ABS(YNS0(IS)).GE.ABS(XNS0(IS)).AND.ABS(YNS0(IS)).GE.    &
                  ABS(ZNS0(IS))) THEN                                    
                IPROJ=2 
                DNMAX=YNS0(IS) 
                IF(ABS(DNMAX).GT.TOL) CNMAX=VERTP0(IPV1(IS,1),2)-       &
                     VERTP0(IPREF,2)+(XNS0(IS)*(VERTP0(IPV1(IS,1),      &
                     1)-VERTP0(IPREF,1))+ZNS0(IS)*(VERTP0(              &
                     IPV1(IS,1),3)-VERTP0(IPREF,3)))/DNMAX         
             ELSEIF(ABS(ZNS0(IS)).GE.ABS(XNS0(IS)).AND.                 &
                  ABS(ZNS0(IS)).GE.ABS(YNS0(IS))) THEN       
                IPROJ=3 
                DNMAX=ZNS0(IS) 
                IF(ABS(DNMAX).GT.TOL) CNMAX=VERTP0(IPV1(IS,1),3)-       &
                     VERTP0(IPREF,3)+(XNS0(IS)*(VERTP0(IPV1(IS,1),      &
                     1)-VERTP0(IPREF,1))+YNS0(IS)*(VERTP0(              &
                     IPV1(IS,1),2)-VERTP0(IPREF,2)))/DNMAX 
             ELSE 
                IPROJ=1 
                DNMAX=XNS0(IS) 
                IF(ABS(DNMAX).GT.TOL) CNMAX=VERTP0(IPV1(IS,1),1)-       &
                     VERTP0(IPREF,1)+(YNS0(IS)*(VERTP0(IPV1(IS,1),      &
                     2)-VERTP0(IPREF,2))+ZNS0(IS)*(VERTP0(              &
                     IPV1(IS,1),3)-VERTP0(IPREF,3)))/DNMAX 
             END IF
             IH=INT((NIPV1(IS)-2)/2) 
             DO I=2,IH+1 
                IP=2*I 
                IP1=IP-1 
                IP2=IP-2 
                IF(IPROJ.EQ.1) THEN 
                   YV1=VERTP0(IPV1(IS,IP1),2)-VERTP0(IPV1(IS,1),2) 
                   ZV1=VERTP0(IPV1(IS,IP1),3)-VERTP0(IPV1(IS,1),3) 
                   YV2=VERTP0(IPV1(IS,IP),2)-VERTP0(IPV1(IS,IP2),2) 
                   ZV2=VERTP0(IPV1(IS,IP),3)-VERTP0(IPV1(IS,IP2),3) 
                   SUMP=SUMP+YV1*ZV2-ZV1*YV2 
                ELSEIF(IPROJ.EQ.2) THEN 
                   XV1=VERTP0(IPV1(IS,IP1),1)-VERTP0(IPV1(IS,1),1) 
                   ZV1=VERTP0(IPV1(IS,IP1),3)-VERTP0(IPV1(IS,1),3) 
                   XV2=VERTP0(IPV1(IS,IP),1)-VERTP0(IPV1(IS,IP2),1) 
                   ZV2=VERTP0(IPV1(IS,IP),3)-VERTP0(IPV1(IS,IP2),3) 
                   SUMP=SUMP+ZV1*XV2-XV1*ZV2 
                ELSE 
                   XV1=VERTP0(IPV1(IS,IP1),1)-VERTP0(IPV1(IS,1),1) 
                   YV1=VERTP0(IPV1(IS,IP1),2)-VERTP0(IPV1(IS,1),2) 
                   XV2=VERTP0(IPV1(IS,IP),1)-VERTP0(IPV1(IS,IP2),1) 
                   YV2=VERTP0(IPV1(IS,IP),2)-VERTP0(IPV1(IS,IP2),2) 
                   SUMP=SUMP+XV1*YV2-YV1*XV2 
                END IF
             END DO
             IF(2*(IH+1).LT.NIPV1(IS)) THEN 
                IF(IPROJ.EQ.1) THEN 
                   YV1=VERTP0(IPV1(IS,NIPV1(IS)),2)-                    &
                        VERTP0(IPV1(IS,1),2) 
                   ZV1=VERTP0(IPV1(IS,NIPV1(IS)),3)-                    &
                        VERTP0(IPV1(IS,1),3) 
                   YV2=VERTP0(IPV1(IS,1),2)-                            &
                        VERTP0(IPV1(IS,NIPV1(IS)-1),2) 
                   ZV2=VERTP0(IPV1(IS,1),3)-                            &
                        VERTP0(IPV1(IS,NIPV1(IS)-1),3) 
                   SUMP=SUMP+YV1*ZV2-ZV1*YV2 
                ELSEIF(IPROJ.EQ.2) THEN 
                   XV1=VERTP0(IPV1(IS,NIPV1(IS)),1)-                    &
                        VERTP0(IPV1(IS,1),1) 
                   ZV1=VERTP0(IPV1(IS,NIPV1(IS)),3)-                    &
                        VERTP0(IPV1(IS,1),3) 
                   XV2=VERTP0(IPV1(IS,1),1)-                            &
                        VERTP0(IPV1(IS,NIPV1(IS)-1),1)  
                   ZV2=VERTP0(IPV1(IS,1),3)-                            &
                        VERTP0(IPV1(IS,NIPV1(IS)-1),3)   
                   SUMP=SUMP+ZV1*XV2-XV1*ZV2 
                ELSE 
                   XV1=VERTP0(IPV1(IS,NIPV1(IS)),1)-                    &
                        VERTP0(IPV1(IS,1),1) 
                   YV1=VERTP0(IPV1(IS,NIPV1(IS)),2)-                    &
                        VERTP0(IPV1(IS,1),2) 
                   XV2=VERTP0(IPV1(IS,1),1)-                            &
                        VERTP0(IPV1(IS,NIPV1(IS)-1),1)    
                   YV2=VERTP0(IPV1(IS,1),2)-                            &
                        VERTP0(IPV1(IS,NIPV1(IS)-1),2)  
                   SUMP=SUMP+XV1*YV2-YV1*XV2 
                END IF
             ENDIF
             IF(ABS(DNMAX).GT.TOL) SUMS=SUMS+CNMAX*SUMP 
          END IF
       END DO
       VOL=SUMS/6.0_W_P 
    END IF
    RETURN 
  END SUBROUTINE INTV3D
!--------------------------- END OF INTV3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              CPPOL3D                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CS0      = constants of the planes containing the faces of the      | 
!            original polyhedron                                      | 
! IPV0     = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NIPV0    = number of vertices of each face                          | 
! NTS0     = total number of faces                                    | 
! NTP0     = last global vertex index                                 | 
! NTV0     = total number of vertices                                 | 
! VERTI0   = vertex coordinates of the original polyhedron            | 
! XNS0, ...= unit-lenght normals to the faces of the original pol.    | 
! On return:                                                          | 
!===========                                                          | 
! CS       = constants of the planes containing the faces of the      | 
!            copied polyhedron                                        | 
! IPV      = array containing the global indices of the copied pol.   | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTS      = total number of faces                                    | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTI    = vertex coordinates of the copied polyhedron              | 
! XNS,  ...= unit-lenght normals to the faces of the copied pol.      | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE CPPOL3D(CS,CS0,IPV,IPV0,NIPV,NIPV0,NTP,NTP0,NTS,NTS0,      &
       NTV,NTV0,VERTI,VERTI0,XNS,XNS0,YNS,YNS0,ZNS,ZNS0) BIND(C)    
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NTP0,NTS0,NTV0 
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPV0(NS,NV),NIPV0(NS) 
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(IN) :: CS0(NS),VERTI0(NV,3),XNS0(NS),YNS0(NS),    &
         ZNS0(NS)                                                     
    REAL(W_P), INTENT(OUT) :: CS(NS),VERTI(NV,3),XNS(NS),YNS(NS),       &
         ZNS(NS)                                                      
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,IP,J 
    
    NTS=NTS0 
    NTV=NTV0 
    NTP=NTP0 
    DO IP=1,NTP0 
       DO J=1,3 
          VERTI(IP,J)=VERTI0(IP,J) 
       END DO
    END DO
    DO I=1,NTS0 
       XNS(I)=XNS0(I) 
       YNS(I)=YNS0(I) 
       ZNS(I)=ZNS0(I) 
       NIPV(I)=NIPV0(I) 
       CS(I)=CS0(I) 
       DO J=1,NIPV0(I) 
          IPV(I,J)=IPV0(I,J) 
       END DO
    END DO
    RETURN 
  END SUBROUTINE CPPOL3D
!-------------------------- END OF CPPOL3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            RESTORE3D                                | 
!---------------------------------------------------------------------| 
!          This routine restores the structure a polyhedron           | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! CS       = constants of the planes containing the faces of the      | 
!            original polyhedron                                      | 
! XNS, ... = unit-lenght normals to the faces of the original pol.    | 
! IPV      = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTS      = total number of faces                                    | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTI    = vertex coordinates of the original polyhedron            | 
! On return:                                                          | 
!===========                                                          | 
! CS       = constants of the planes containing the faces of the      | 
!            restored polyhedron                                      | 
! XNS,  ...= unit-lenght normals to the faces of the restored pol.    | 
! IPV      = array containing the global indices of the restored pol. | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTS      = total number of faces                                    | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTI    = vertex coordinates of the restored polyhedron            | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE RESTORE3D(CS,IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)       &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(INOUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(INOUT) :: IPV(NS,NV),NIPV(NS) 
    REAL (W_P), INTENT(INOUT) :: CS(NS),VERTP(NV,3),XNS(NS),YNS(NS),    &
         ZNS(NS)                                                      
    !.. Local Scalars           
    REAL (W_P) :: DMOD,TOLP 
    INTEGER(I_P) :: IC,IP,IP0,IP1,IP2,IPT,IS,IV,IV0,IVT,NTP0,NTS0,NTV0 
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IPT0(NV),IPV0(NS,NV),NIPV0(NS) 
    REAL (W_P) :: CS0(NS),VERTP0(NV,3),XNS0(NS),YNS0(NS),ZNS0(NS) 
    !* Obtain the work polyhedron                                           
    CALL CPPOL3D(CS0,CS,IPV0,IPV,NIPV0,NIPV,NTP0,NTP,NTS0,NTS,NTV0,     &
         NTV,VERTP0,VERTP,XNS0,XNS,YNS0,YNS,ZNS0,ZNS)                 
    !* In each face, consecutive vertices with the same vector position     
    !* are eliminated. We use the tolerance TOLP                            
    TOLP=1.0E-16_W_P 
    DO IS=1,NTS0 
       IPV(IS,1)=IPV0(IS,1) 
       IVT=0 
       DO IV=1,NIPV0(IS) 
          IP=IPV0(IS,IV) 
          IV0=IV-1 
          IF(IV0.EQ.0) IV0=NIPV0(IS) 
          IP0=IPV0(IS,IV0) 
          DMOD=((VERTP0(IP,1)-VERTP0(IP0,1))**2+(VERTP0(IP,2)-VERTP0(   &
               IP0,2))**2+(VERTP0(IP,3)-VERTP0(IP0,3))**2)**0.5_W_P
          IF(DMOD.GT.TOLP) THEN 
             IVT=IVT+1 
             IPV(IS,IVT)=IPV0(IS,IV) 
          END IF
       END DO
       NIPV(IS)=IVT 
    END DO
    CALL CPPOL3D(CS0,CS,IPV0,IPV,NIPV0,NIPV,NTP0,NTP,NTS0,NTS,NTV0,     &
         NTV,VERTP0,VERTP,XNS0,XNS,YNS0,YNS,ZNS0,ZNS)                 
    !* Eliminate faces with zero or only one vertex                         
    NTS=0 
    DO IS=1,NTS0 
       IF(NIPV0(IS).GT.1) THEN 
          NTS=NTS+1 
          NIPV(NTS)=NIPV0(IS) 
          DO IV=1,NIPV0(IS) 
             IPV(NTS,IV)=IPV0(IS,IV) 
             CS(NTS)=CS0(IS) 
             XNS(NTS)=XNS0(IS) 
             YNS(NTS)=YNS0(IS) 
             ZNS(NTS)=ZNS0(IS) 
          END DO
       END IF
    END DO
    !* Link coincident vertices of different faces                          
    DO IP1=1,NTP-1 
       DO IP2=IP1+1,NTP 
          DMOD=((VERTP(IP1,1)-VERTP(IP2,1))**2+(VERTP(IP1,2)-VERTP(     &
               IP2,2))**2+(VERTP(IP1,3)-VERTP(IP2,3))**2)**0.5_W_P   
          IF(DMOD.LE.TOLP) THEN 
             DO IS=1,NTS 
                DO IV=1,NIPV(IS) 
                   IF(IPV(IS,IV).EQ.IP2) IPV(IS,IV)=IP1 
                END DO
             END DO
          END IF
       END DO
    END DO
    !* Renumber consecutively all the vertex indices making NTP=NTV         
    IPT=0 
    DO IP=1,NTP 
       IC=0 
       DO IS=1,NTS 
          DO IV=1,NIPV(IS) 
             IF(IPV(IS,IV).EQ.IP.AND.IC.EQ.0) THEN 
                IC=1 
                IPT=IPT+1 
                IPT0(IP)=IPT 
             END IF
          END DO
       END DO
    END DO
    CALL CPPOL3D(CS0,CS,IPV0,IPV,NIPV0,NIPV,NTP0,NTP,NTS0,NTS,NTV0,     &
         NTV,VERTP0,VERTP,XNS0,XNS,YNS0,YNS,ZNS0,ZNS)                 
    NTP=IPT 
    NTV=IPT 
    DO IS=1,NTS0 
       DO IV=1,NIPV0(IS) 
          IP=IPV0(IS,IV) 
          IP1=IPT0(IP) 
          IPV(IS,IV)=IP1 
          VERTP(IP1,1)=VERTP0(IP,1) 
          VERTP(IP1,2)=VERTP0(IP,2) 
          VERTP(IP1,3)=VERTP0(IP,3) 
       END DO
    END DO
    RETURN 
  END SUBROUTINE RESTORE3D
!-------------------------- END OF RESTORE3D -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                               DIST3D                                | 
!---------------------------------------------------------------------| 
!   This routine computes the distance from a point to a polygon      | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! N         = number of vertices of the polygon                       | 
! X,Y,Z     = vertex coordinates of the polygon                       | 
! XP,YP,ZP  = coordinates of the point                                | 
! On return:                                                          | 
!===========                                                          | 
! D         = exact distance from the point (XP,YP,ZP) to the polygon | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE DIST3D(D,N,X,Y,Z,XP,YP,ZP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: N 
    REAL(W_P), INTENT(IN) :: XP,YP,ZP 
    REAL(W_P), INTENT(OUT) :: D 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: X(NV),Y(NV),Z(NV) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,I2,I3 
    REAL(W_P) :: C,C1,C2,PHI1,PHI2,T0,TMOD,TOL,VMOD,XN,XQ,XT,XV1,       &
         XV2,YN,YQ,YT,YV1,YV2,ZN,ZQ,ZT,ZV1,ZV2                            
    LOGICAL :: INSIDE 
    !.. Local Arrays                                                        
    REAL(W_P) :: CI(NV),PHI(NV),XNI(NV),XNT(NV),YNI(NV),YNT(NV),        &
         ZNI(NV),ZNT(NV)                                              
    !*                                                                      
    !*                  ^N                                                  
    !*            o-----|---------o                                         
    !*           /      |         |                                         
    !*          /      _|         |                                         
    !*         /      | |         |                                         
    !*        /                   o                                         
    !*   I-1 o                   /                                          
    !*        \        ^NI      /                                           
    !*         \       |       /                                            
    !*          o-------------o                                             
    !*         I      -->     I+1                                           
    !*                NTI                                                   
    !*                                                                      
    !* Obtain the eq. X·N+C=0 that defines the plane containing the polygon
    IF(N.LT.3) THEN
       WRITE(6,*) 'N<3. REVISE THE POLYGONAL SHAPE.'
       RETURN
    END IF
    TOL=1.0E-20_W_P 
    VMOD=0.0_W_P
    DO I=1,N-2 
       I2=I+1 
       I3=I2+1 
       XV1=X(I2)-X(I) 
       YV1=Y(I2)-Y(I) 
       ZV1=Z(I2)-Z(I) 
       XV2=X(I3)-X(I2) 
       YV2=Y(I3)-Y(I2) 
       ZV2=Z(I3)-Z(I2) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       VMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       IF(VMOD.GT.0.0_W_P) GOTO 10 
    END DO
10  CONTINUE 
    IF(VMOD.LT.TOL) THEN 
       D=((XP-X(1))**2+(YP-Y(1))**2+(ZP-Z(1))**2)**0.5_W_P 
       RETURN 
    ENDIF
    XN=XN/VMOD 
    YN=YN/VMOD 
    ZN=ZN/VMOD 
    C=-1.0_W_P*(XN*X(1)+YN*Y(1)+ZN*Z(1)) 
    !* Compute the edges normal NT, NI = N x NT and the distance PHI from ea
    !* vertex I of the polygon to the plane defined as X·NI+CI=0           
    DO I=1,N 
       I2=I+1 
       IF(I.EQ.N) I2=1 
       XT=X(I2)-X(I) 
       YT=Y(I2)-Y(I) 
       ZT=Z(I2)-Z(I) 
       TMOD=(XT**2+YT**2+ZT**2)**0.5_W_P 
       IF(TMOD.LT.TOL) THEN 
          PHI(I)=0.0_W_P 
       ELSE 
          XNT(I)=XT/TMOD 
          YNT(I)=YT/TMOD 
          ZNT(I)=ZT/TMOD 
          XNI(I)=YN*ZNT(I)-ZN*YNT(I) 
          YNI(I)=ZN*XNT(I)-XN*ZNT(I) 
          ZNI(I)=XN*YNT(I)-YN*XNT(I) 
          CI(I)=-1.0_W_P*(XNI(I)*X(I)+YNI(I)*Y(I)+ZNI(I)*Z(I)) 
          PHI(I)=XNI(I)*XP+YNI(I)*YP+ZNI(I)*ZP+CI(I) 
       END IF
    END DO
    INSIDE=.TRUE. 
    !* Init loop                                                            
    DO I=1,N 
       I2=I+1 
       IF(I.EQ.N) I2=1 
       IF(PHI(I).LT.0.0_W_P) THEN 
          INSIDE=.FALSE. 
          C1=-1.0_W_P*(XNT(I)*X(I)+YNT(I)*Y(I)+ZNT(I)*Z(I)) 
          C2=1.0_W_P*(XNT(I)*X(I2)+YNT(I)*Y(I2)+ZNT(I)*Z(I2)) 
          PHI1=XNT(I)*XP+YNT(I)*YP+ZNT(I)*ZP+C1 
          PHI2=-1.0_W_P*(XNT(I)*XP+YNT(I)*YP+ZNT(I)*ZP)+C2 
          IF(PHI1.GE.0.0_W_P.AND.PHI2.GE.0.0_W_P) THEN 
             T0=XNT(I)*(XP-X(I))+YNT(I)*(YP-Y(I))+ZNT(I)*(ZP-Z(I)) 
             XQ=X(I)+T0*XNT(I) 
             YQ=Y(I)+T0*YNT(I) 
             ZQ=Z(I)+T0*ZNT(I) 
             D=((XP-XQ)**2+(YP-YQ)**2+(ZP-ZQ)**2)**0.5_W_P 
             RETURN 
          ELSEIF(PHI1.LE.0.0_W_P) THEN 
             D=((XP-X(I))**2+(YP-Y(I))**2+(ZP-Z(I))**2)**0.5_W_P 
             IF(I.NE.1) RETURN 
          ELSEIF(PHI2.LE.0.0_W_P.AND.PHI(I2).GE.0.0_W_P) THEN 
             D=((XP-X(I2))**2+(YP-Y(I2))**2+(ZP-Z(I2))**2)**0.5_W_P 
             RETURN 
          END IF
       END IF
    END DO
    IF(INSIDE) D=ABS(XN*XP+YN*YP+ZN*ZP+C) 
    RETURN 
  END SUBROUTINE DIST3D
!--------------------------- END OF DIST3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              POLOUT3D                               | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! IFILE    = number # used to name the external VTK file              | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index (note that if the polyhedron    | 
!            is not previously truncated, then NTP=NTV)               | 
! NTS      = total number of faces                                    | 
! VERTP    = vertex coordinates of the polyhedron                     | 
! On return:                                                          | 
!===========                                                          | 
! pol#.vtk = external VTK file                                        | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE POLOUT3D(IFILE,IPV,NIPV,NTP,NTS,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: IFILE,NTP,NTS 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,3) 
    INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IS,IV,NDATA,NPOLY 
    CHARACTER(12) :: FILENAME 
    
    WRITE(FILENAME,'("pol",I5.5,".vtk")')IFILE 
    OPEN(11, FILE=FILENAME) 
    WRITE(11,'(A26)')'# vtk DataFile Version 2.0' 
    WRITE(11,'(A6,I5.5)')'File: ', IFILE 
    WRITE(11,'(A5)')'ASCII' 
    WRITE(11,*)' ' 
    WRITE(11,'(A16)')'DATASET POLYDATA' 
    WRITE(11,'(A6,I7,A6)')'POINTS',NTP,' float' 
    DO IP=1,NTP 
       WRITE(11,'(3F12.6)')VERTP(IP,1),VERTP(IP,2),VERTP(IP,3) 
    END DO
    NPOLY=0 
    NDATA=0 
    DO IS=1,NTS 
       IF(NIPV(IS).GT.0) THEN 
          NPOLY=NPOLY+1 
          NDATA=NDATA+NIPV(IS)+1 
       END IF
    END DO
    WRITE(11,'(A8,I7,I7)')'POLYGONS',NPOLY,NDATA 
    DO IS=1,NTS 
       IF(NIPV(IS).GT.0) THEN 
          WRITE(11,'(I7)')NIPV(IS) 
          DO IV=1,NIPV(IS) 
             WRITE(11,'(I7)')IPV(IS,IV)-1 
          END DO
       END IF
    END DO
    CLOSE(11) 
    RETURN 
  END SUBROUTINE POLOUT3D
!------------------------- END OF POLOUT3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                               INTC3D                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! XNC, ... = unit-lenght normal to the new face \Gamma_c              | 
! C        = constant of the plane containing the new face \Gamma_c   | 
! IPV0     = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NIPV0    = number of vertices of each face                          | 
! NTP0     = last global vertex index                                 | 
! NTS0     = total number of faces                                    | 
! VERTP0   = vertex coordinates of the original polyhedron            | 
! On return:                                                          | 
!===========                                                          | 
! CEN      = centroid of the intersection vertices resulting from the | 
!            intersection between \Gamma_c and the polyhedron         | 
! IECEN    = 1 if the calculation is successful                       | 
!            0 otherwise                                              | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INTC3D(C,CEN,IECEN,IPV0,NIPV0,NTP0,NTS0,VERTP0,XNC,        &
       YNC,ZNC) BIND(C)                                             
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NTP0,NTS0 
    REAL(W_P), INTENT(IN) :: C,XNC,YNC,ZNC 
    INTEGER(I_P), INTENT(OUT) :: IECEN 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPV0(NS,NV),NIPV0(NS) 
    REAL(W_P), INTENT(INOUT) :: VERTP0(NV,3) 
    REAL(W_P), INTENT(OUT) :: CEN(3) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: ICONTN,ICONTP,IP,IP0,IP1,IS,IV,IV1,J,NIPNEW 
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IA(NV),IPIA0(NV),IPIA1(NV) 
    INTEGER(I_P2) :: IPE(NV,NV) 
    REAL(W_P) :: PHIV(NV) 
    
    IECEN=0 
    ICONTP=0 
    ICONTN=0 
    DO IP=1,NTP0 
       IA(IP)=-1 
    END DO
    !* Distance function and values of IA                                   
    DO IS=1,NTS0 
       DO IV=1,NIPV0(IS) 
          IP=IPV0(IS,IV) 
          IV1=IV+1 
          IF(IV.EQ.NIPV0(IS)) IV1=1 
          IP1=IPV0(IS,IV1) 
          IPE(IP,IP1)=0 
          IF(IA(IP).EQ.(-1)) THEN 
             PHIV(IP)=XNC*VERTP0(IP,1)+YNC*VERTP0(IP,2)+                &
                  ZNC*VERTP0(IP,3)+C                                  
             IF(PHIV(IP).GT.0.0_W_P) THEN 
                IA(IP)=1 
                ICONTP=ICONTP+1 
             ELSE 
                IA(IP)=0 
                ICONTN=ICONTN+1 
             END IF
          END IF
       END DO
    END DO
    CEN(1)=0.0_W_P 
    CEN(2)=0.0_W_P 
    CEN(3)=0.0_W_P 
    IF(ICONTP.NE.0.AND.ICONTN.NE.0) THEN 
       !* Determination of the new vertices                                    
       NIPNEW=NTP0 
       DO IS=1,NTS0 
          IF(NIPV0(IS).GT.0) THEN 
             DO IV=1,NIPV0(IS) 
                IP=IPV0(IS,IV) 
                IV1=IV+1 
                IF(IV.EQ.NIPV0(IS)) IV1=1 
                IP1=IPV0(IS,IV1) 
                IF(IA(IP).NE.IA(IP1).AND.IPE(IP1,IP).EQ.0) THEN 
                   NIPNEW=NIPNEW+1 
                   IPE(IP,IP1)=INT(NIPNEW,KIND=I_P2) 
                   IF(IA(IP).EQ.0) THEN 
                      IPIA0(NIPNEW)=IP 
                      IPIA1(NIPNEW)=IP1 
                   ELSE 
                      IPIA0(NIPNEW)=IP1 
                      IPIA1(NIPNEW)=IP 
                   END IF
                END IF
             END DO
          END IF
       END DO
       !* Disjoint regions may produce NIPNEW=NTP0 and both ICONTP and ICONTN
       IF(NIPNEW.EQ.NTP0) RETURN 
       !* Position of the new vertices and cetroid computation                 
       DO IP=NTP0+1,NIPNEW 
          IP0=IPIA0(IP) 
          IP1=IPIA1(IP) 
          DO J=1,3 
             VERTP0(IP,J)=VERTP0(IP0,J)-PHIV(IP0)*(VERTP0(IP1,J)-       &
                  VERTP0(IP0,J))/(PHIV(IP1)-PHIV(IP0))                
             CEN(J)=CEN(J)+VERTP0(IP,J) 
          END DO
       END DO
       IECEN=1 
       DO J=1,3 
          CEN(J)=CEN(J)/(NIPNEW-NTP0) 
       END DO
    END IF
    RETURN 
  END SUBROUTINE INTC3D
!--------------------------- END OF INTC3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              BOX3D                                  | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! NTP      = number of vertices                                       | 
! VERTP    = vertex coordinates                                       | 
! On return:                                                          | 
!===========                                                          | 
! BOX      = maximum and minimum position values along the coordinate | 
!            directions of the hexahedral box that contains a set of  | 
!            NTP polyhedron vertices                                  | 
!            1 -> XMIN                                                | 
!            2 -> XMAX                                                | 
!            3 -> YMIN                                                | 
!            4 -> YMAX                                                | 
!            5 -> ZMIN                                                | 
!            6 -> ZMAX                                                | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE BOX3D(BOX,NTP,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NTP 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,3) 
    REAL(W_P), INTENT(OUT) :: BOX(6) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP 
    
    BOX(1)=1E20_W_P 
    BOX(2)=-1E20_W_P 
    BOX(3)=1E20_W_P 
    BOX(4)=-1E20_W_P 
    BOX(5)=1E20_W_P 
    BOX(6)=-1E20_W_P 
    DO IP=1,NTP 
       BOX(1)=MIN(BOX(1),VERTP(IP,1)) 
       BOX(2)=MAX(BOX(2),VERTP(IP,1)) 
       BOX(3)=MIN(BOX(3),VERTP(IP,2)) 
       BOX(4)=MAX(BOX(4),VERTP(IP,2)) 
       BOX(5)=MIN(BOX(5),VERTP(IP,3)) 
       BOX(6)=MAX(BOX(6),VERTP(IP,3)) 
    END DO
    RETURN 
  END SUBROUTINE BOX3D
!-------------------------- END OF BOX3D -----------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            INTE3DFACE                               | 
! Intersection between a 3D planar face, either convex or non-convex, | 
! an a half-space                                                     | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! XNC, ... = unit-lenght normal of the half-space interface           | 
! C        = constant of the half-space interface                     | 
! IPV      = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = vertex coordinates of the original polygonal face        | 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the truncat. pol. | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! ICONTN   = num. of vertices of the original region that are outside | 
!            the truncated region                                     | 
! ICONTP   = num. of vertices of the original region that remain in   | 
!            the truncated region                                     | 
! VERTP    = vertex coordinates of the truncated polygonal face       | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INTE3DFACE(C,ICONTN,ICONTP,IPV,NTP,NTV,VERTP,XNC,YNC,      &
       ZNC) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: C,XNC,YNC,ZNC 
    INTEGER(I_P), INTENT(INOUT) :: NTP,NTV 
    INTEGER(I_P), INTENT(OUT) :: ICONTN,ICONTP 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(INOUT) :: IPV(NV) 
    REAL(W_P), INTENT(INOUT) :: VERTP(NV,3) 
    !.. Local Scalars                                                       
    INTEGER IP,IP0,IP0I,IP1,IP1I,IV,IV1,NINT,NIPNEW,NIV 
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IA(NV),IPIA0(NV),IPIA1(NV),IPV1(NV) 
    REAL(W_P) :: PHIV(NV) 
    
    ICONTP=0 
    ICONTN=0 
    DO IP=1,NTP 
       IA(IP)=-1 
    END DO
    !* Distance function and values of IA                                   
    DO IV=1,NTV 
       IP=IPV(IV) 
       IF(IA(IP).EQ.(-1)) THEN 
          PHIV(IP)=XNC*VERTP(IP,1)+YNC*VERTP(IP,2)+ZNC*VERTP(IP,3)+C 
          IF(PHIV(IP).GT.0.0_W_P) THEN 
             IA(IP)=1 
             ICONTP=ICONTP+1 
          ELSE 
             IA(IP)=0 
             ICONTN=ICONTN+1 
          END IF
       END IF
    END DO
    IF(ICONTP.NE.0.AND.ICONTN.NE.0) THEN 
       !* Construction of the new polygonal face                               
       NINT=0 
       NIV=0 
       DO IV=1,NTV 
          IP=IPV(IV) 
          IV1=IV+1 
          IF(IV1.GT.NTV)IV1=1 
          IP1=IPV(IV1) 
          IF(IA(IP).EQ.1) THEN 
             NIV=NIV+1 
             IPV1(NIV)=IPV(IV) 
          END IF
          IF(IA(IP).NE.IA(IP1)) THEN 
             NINT=NINT+1 
             NIV=NIV+1 
             NIPNEW=NTP+NINT 
             IPV1(NIV)=NIPNEW 
             IF(IA(IP).EQ.1) THEN 
                IP1I=IP 
                IP0I=IP1 
             ELSE 
                IP1I=IP1 
                IP0I=IP 
             END IF
             IPIA0(NIPNEW)=IP0I 
             IPIA1(NIPNEW)=IP1I 
          END IF
       END DO
       !* Position of the new vertices                                         
       DO IP=NTP+1,NTP+NINT 
          IP0=IPIA0(IP) 
          IP1=IPIA1(IP) 
          VERTP(IP,1)=VERTP(IP0,1)-PHIV(IP0)*(VERTP(IP1,1)-             &
               VERTP(IP0,1))/(PHIV(IP1)-PHIV(IP0))                    
          VERTP(IP,2)=VERTP(IP0,2)-PHIV(IP0)*(VERTP(IP1,2)-             &
               VERTP(IP0,2))/(PHIV(IP1)-PHIV(IP0))                    
          VERTP(IP,3)=VERTP(IP0,3)-PHIV(IP0)*(VERTP(IP1,3)-             &
               VERTP(IP0,3))/(PHIV(IP1)-PHIV(IP0))                    
       END DO
       !* Update the polygonal face arragement
       DO IV=1,NIV 
          IPV(IV)=IPV1(IV) 
       END DO
       NTV=NIV 
       NTP=NTP+NINT 
    END IF
    RETURN 
  END SUBROUTINE INTE3DFACE
!------------------------- END OF INTE3DFACE -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              AREAFACE                               | 
!---------------------------------------------------------------------| 
!        This routine computes the area of a 3D polygonal face        | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! VERTP    = vertex coordinates of the polyhedron                     | 
! XNS, ... = unit-lenght normal to the 3D polygonal face              | 
! IPV      = array containing the global indices of the 3D polygonal  | 
!            face                                                     | 
! NTV      = total number of vertices                                 |  
! On return:                                                          | 
!===========                                                          | 
! A        = area of the 3D polygonal face                            | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE AREAFACE(A,IPV,NTV,VERTP,XNS,YNS,ZNS) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NTV 
    REAL(W_P), INTENT(IN) :: XNS,YNS,ZNS 
    REAL(W_P), INTENT(OUT) :: A 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPV(NV) 
    REAL(W_P), INTENT(IN) :: VERTP(NV,3) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,IH,IP,IP1,IP2,IPROJ 
    REAL(W_P) :: DNMAX,SUMP,TOL,XV1,XV2,YV1,YV2,ZV1,ZV2 
    
    TOL=1.0E-16_W_P 
    SUMP=0.0_W_P 
    IF(ABS(YNS).GE.ABS(XNS).AND.ABS(YNS).GE.ABS(ZNS)) THEN 
       IPROJ=2 
       DNMAX=YNS 
    ELSEIF(ABS(ZNS).GE.ABS(XNS).AND.ABS(ZNS).GE.ABS(YNS)) THEN 
       IPROJ=3 
       DNMAX=ZNS 
    ELSE 
       IPROJ=1 
       DNMAX=XNS 
    END IF
    IH=INT((NTV-2)/2) 
    DO I=2,IH+1 
       IP=2*I 
       IP1=IP-1 
       IP2=IP-2 
       IF(IPROJ.EQ.1) THEN 
          YV1=VERTP(IPV(IP1),2)-VERTP(IPV(1),2) 
          ZV1=VERTP(IPV(IP1),3)-VERTP(IPV(1),3) 
          YV2=VERTP(IPV(IP),2)-VERTP(IPV(IP2),2) 
          ZV2=VERTP(IPV(IP),3)-VERTP(IPV(IP2),3) 
          SUMP=SUMP+YV1*ZV2-ZV1*YV2 
       ELSEIF(IPROJ.EQ.2) THEN 
          XV1=VERTP(IPV(IP1),1)-VERTP(IPV(1),1) 
          ZV1=VERTP(IPV(IP1),3)-VERTP(IPV(1),3) 
          XV2=VERTP(IPV(IP),1)-VERTP(IPV(IP2),1) 
          ZV2=VERTP(IPV(IP),3)-VERTP(IPV(IP2),3) 
          SUMP=SUMP+ZV1*XV2-XV1*ZV2 
       ELSE 
          XV1=VERTP(IPV(IP1),1)-VERTP(IPV(1),1) 
          YV1=VERTP(IPV(IP1),2)-VERTP(IPV(1),2) 
          XV2=VERTP(IPV(IP),1)-VERTP(IPV(IP2),1) 
          YV2=VERTP(IPV(IP),2)-VERTP(IPV(IP2),2) 
          SUMP=SUMP+XV1*YV2-YV1*XV2 
       END IF
    END DO
    IF(2*(IH+1).LT.NTV) THEN 
       IF(IPROJ.EQ.1) THEN 
          YV1=VERTP(IPV(NTV),2)-VERTP(IPV(1),2) 
          ZV1=VERTP(IPV(NTV),3)-VERTP(IPV(1),3) 
          YV2=VERTP(IPV(1),2)-VERTP(IPV(NTV-1),2) 
          ZV2=VERTP(IPV(1),3)-VERTP(IPV(NTV-1),3) 
          SUMP=SUMP+YV1*ZV2-ZV1*YV2 
       ELSEIF(IPROJ.EQ.2) THEN 
          XV1=VERTP(IPV(NTV),1)-VERTP(IPV(1),1) 
          ZV1=VERTP(IPV(NTV),3)-VERTP(IPV(1),3) 
          XV2=VERTP(IPV(1),1)-VERTP(IPV(NTV-1),1) 
          ZV2=VERTP(IPV(1),3)-VERTP(IPV(NTV-1),3) 
          SUMP=SUMP+ZV1*XV2-XV1*ZV2 
       ELSE 
          XV1=VERTP(IPV(NTV),1)-VERTP(IPV(1),1) 
          YV1=VERTP(IPV(NTV),2)-VERTP(IPV(1),2) 
          XV2=VERTP(IPV(1),1)-VERTP(IPV(NTV-1),1) 
          YV2=VERTP(IPV(1),2)-VERTP(IPV(NTV-1),2) 
          SUMP=SUMP+XV1*YV2-YV1*XV2 
       END IF
    ENDIF
    IF(ABS(DNMAX).GT.TOL) THEN 
       A=(SUMP/DNMAX)/2.0_W_P 
    ELSE 
       A=0.0_W_P 
    END IF
    RETURN 
  END SUBROUTINE AREAFACE
!-------------------------- END OF AREAFACE --------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                                PVFIT                                | 
! Obtain a paraboloid from a Polygonal-set Volumetric Fit             | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! NIV      = number of vertices of each polygon                       | 
! NPOL     = number of polygons                                       | 
! VN0      = orthonormal basis (x,y,z)-components                     | 
! VP0      = reference point (x,y,z)-coordinates                      | 
! XN,YN,ZN = (x,y,z)-components of the unit-lenght normals to the     | 
!            polygons                                                 | 
! XV,YV,ZV = array containing the (x,y,z)-coordinates of every        | 
!            polygon vertices                                         | 
! On return:                                                          | 
!===========                                                          | 
! COEF     = coefficients of the fit hypersurface in the new          | 
!            orthonormal basis                                        | 
! ERRFIT   = fit error                                                | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE PVFIT(COEF,ERRFIT,NIV,NPOL,VN0,VP0,XN,XV,YN,YV,ZN,ZV)      &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NPOL 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: NIV(NS) 
    REAL(W_P), INTENT(IN) :: VN0(3,3),VP0(3),XN(NS),XV(NS,NV),          &
         YN(NS),YV(NS,NV),ZN(NS),ZV(NS,NV)                            
    INTEGER(I_P), PARAMETER :: N=6 
    REAL(W_P), INTENT(OUT) :: ERRFIT
    REAL(W_P), INTENT(OUT) :: COEF(N) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,I2,IEINV,IPOL,J
    REAL(W_P) :: BR1(NPOL),BR2(NPOL),BR3(NPOL),DU,DV,F1,F2,FN,U1,U2,    &
         UN,V1,V2,VN,X1,X2,Y1,Y2,Z1,Z2   
    !.. Local Arrays                                                        
    REAL(W_P) :: A(N,N),AINV(N,N),B(N),R(NPOL,N),SOL(N),SR(N) 
    DO I=1,N 
       B(I)=0.0_W_P 
       DO J=1,N 
          A(I,J)=0.0_W_P 
       END DO
    END DO
    DO IPOL=1,NPOL 
       FN=XN(IPOL)*VN0(1,1)+YN(IPOL)*VN0(1,2)+ZN(IPOL)*VN0(1,3) 
       UN=XN(IPOL)*VN0(2,1)+YN(IPOL)*VN0(2,2)+ZN(IPOL)*VN0(2,3) 
       VN=XN(IPOL)*VN0(3,1)+YN(IPOL)*VN0(3,2)+ZN(IPOL)*VN0(3,3) 
       X1=XV(IPOL,1) 
       Y1=YV(IPOL,1) 
       Z1=ZV(IPOL,1) 
       CALL SYSTRA(F1,U1,V1,VN0,VP0,X1,Y1,Z1) 
       BR1(IPOL)=(F1*FN+U1*UN+V1*VN)/FN 
       BR2(IPOL)=-UN/FN 
       BR3(IPOL)=-VN/FN 
       DO J=1,N 
          SR(J)=0.0_W_P 
       END DO
       DO I=1,NIV(IPOL) 
          X1=XV(IPOL,I) 
          Y1=YV(IPOL,I) 
          Z1=ZV(IPOL,I) 
          CALL SYSTRA(F1,U1,V1,VN0,VP0,X1,Y1,Z1) 
          IF(I.EQ.NIV(IPOL)) THEN 
             I2=1 
          ELSE 
             I2=I+1 
          END IF
          X2=XV(IPOL,I2) 
          Y2=YV(IPOL,I2) 
          Z2=ZV(IPOL,I2) 
          CALL SYSTRA(F2,U2,V2,VN0,VP0,X2,Y2,Z2) 
          DU=U2-U1 
          DV=V2-V1 
          R(IPOL,1)=(U2+U1)*DV/2.0_W_P 
          R(IPOL,2)=(U2**2+U2*U1+U1**2)*DV/6.0_W_P 
          R(IPOL,3)=-(V2**2+V2*V1+V1**2)*DU/6.0_W_P 
          R(IPOL,4)=(4.0_W_P*U1**3+6.0_W_P*U1**2*DU+4.0_W_P*U1*DU**2    &
               +DU**3)*DV/12.0_W_P
          R(IPOL,5)=(6.0_W_P*U1*V1+2.0_W_P*DU*DV+3.0_W_P*U1*DV+         &
               3.0_W_P*V1*DU)*(U1*DV-V1*DU)/24.0_W_P      
          R(IPOL,6)=-(4.0_W_P*V1**3+6.0_W_P*V1**2*DV+                   &
               4.0_W_P*V1*DV**2+DV**3)*DU/12.0_W_P  
          DO J=1,N 
             SR(J)=SR(J)+R(IPOL,J) 
          END DO
       END DO
       DO I=1,N 
          B(I)=B(I)+SR(I)*(BR1(IPOL)*SR(1)+BR2(IPOL)*SR(2)+             &
               BR3(IPOL)*SR(3)) 
          DO J=1,N 
             A(I,J)=A(I,J)+SR(I)*SR(J) 
          END DO
       END DO
    END DO
    !. F(U,V)=SOL(1)+SOL(2)*U+SOL(3)*V+SOL(4)*U**2+SOL(5)*U*V+SOL(6)*V**2   
    !. Solve the 6x6 linear system of equations                             
    CALL MATINVGAUSSJ(A,AINV,IEINV,N)
    IF(IEINV.EQ.0) THEN
       SOL=MATMUL(AINV,B)
    ELSE
       SOL=0.0_W_P
    END IF
    DO I=1,N 
       COEF(I)=SOL(I) 
    END DO
    !. Fit error computation      
    ERRFIT=0.0_W_P
    DO IPOL=1,NPOL 
       ERRFIT=ERRFIT+((COEF(1)-BR1(IPOL))*R(IPOL,1)+(COEF(2)-BR2(IPOL)) &
            *R(IPOL,2)+(COEF(3)-BR3(IPOL))*R(IPOL,3)+COEF(4)*R(IPOL,4)+ &
            COEF(5)*R(IPOL,5)+COEF(6)*R(IPOL,6))**2
    END DO
    RETURN 
  END SUBROUTINE PVFIT
!---------------------------- END OF PVFIT ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              SYSTRA                                 | 
! Obtain the coordinates of a point in a new orthonormal basis        |
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! VN0      = array of dimension (3,3) containing unit-vectors x,y,z-  | 
!            components of the new orthonormal basis                  | 
! VP0      = array of dimension (3) containing the x,y,z-coordinates  | 
!            of the reference point where the new orthonormal basis   | 
!            is traslated                                             | 
! X,Y,Z    = x,y,z-coordinates                                        | 
! On return:                                                          | 
!===========                                                          | 
! F,U,V    = f,u,v-coordinates in the new orthonormal basis           | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE SYSTRA(F,U,V,VN0,VP0,X,Y,Z) BIND(C) 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: X,Y,Z 
    REAL(W_P), INTENT(OUT) :: F,U,V 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VN0(3,3),VP0(3) 
    F=(X-VP0(1))*VN0(1,1)+(Y-VP0(2))*VN0(1,2)+(Z-VP0(3))*VN0(1,3) 
    U=(X-VP0(1))*VN0(2,1)+(Y-VP0(2))*VN0(2,2)+(Z-VP0(3))*VN0(2,3) 
    V=(X-VP0(1))*VN0(3,1)+(Y-VP0(2))*VN0(3,2)+(Z-VP0(3))*VN0(3,3) 
    RETURN 
  END SUBROUTINE SYSTRA
!-------------------------- END OF SYSTRA ----------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           MATINVGAUSSJ                              | 
!.. Matrix inversion using Gauss Jordan                               | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! A        = matrix elements                                          | 
! N        = A-matrix size                                            | 
! On return:                                                          | 
!===========                                                          | 
! AINV     = inversed A-matrix                                        | 
! IEINV    = 0 if A is inverted, 1 otherwise                          | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE MATINVGAUSSJ(A,AINV,IEINV,N) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: N 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IEINV
    REAL(W_P), INTENT(IN) :: A(N,N) 
    REAL(W_P), INTENT(OUT) :: AINV(N,N) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,J,J2,K 
    REAL(W_P) :: RATIO 
    !.. Local Arrays                                                        
    REAL(W_P) :: AUX(2*N,2*N) 
    IEINV=0
    !. Identity                                                             
    DO I=1,N 
       DO J=1,N 
          AUX(I,J)=A(I,J) 
          IF(I.EQ.J) THEN 
             AUX(I,J+N)=1.0_W_P 
          ELSE 
             AUX(I,J+N)=0.0_W_P 
          END IF
       END DO
    END DO
    !. Diagonal                                                             
    DO I=1,N 
       IF(AUX(I,I).EQ.0.0_W_P) THEN
          IEINV=1
          RETURN
       END IF
       DO J=1,N 
          IF(I.NE.J) THEN
             RATIO=AUX(J,I)/AUX(I,I) 
             DO K=1,2*N 
                AUX(J,K)=AUX(J,K)-(AUX(I,K)*RATIO) 
             END DO
          END IF
       END DO
    END DO
    DO I=1,N 
       IF(AUX(I,I).EQ.0.0_W_P) THEN
          IEINV=1
          RETURN
       END IF
       DO J=N+1,2*N 
          AUX(I,J)=AUX(I,J)/AUX(I,I) 
       END DO
    END DO
    !. Inverse copy                                                         
    DO I=1,N 
       DO J=1,N 
          J2=J+N 
          AINV(I,J)=AUX(I,J2) 
       END DO
    END DO
    RETURN 
  END SUBROUTINE MATINVGAUSSJ
!----------------------- END OF MATINVGAUSSJ -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            VOFTOOLS_DIM3D                           |  
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! NSOUT    = parameter for dimensioning arrays related with faces     | 
! NVOUT    = parameter for dimensioning arrays related with vertices  | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_DIM3D(NSOUT,NVOUT) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NSOUT,NVOUT 
    NSOUT=NS 
    NVOUT=NV 
    RETURN 
  END SUBROUTINE VOFTOOLS_DIM3D
!----------------------- END OF VOFTOOLS_DIM3D -----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              ENFORV2D                               | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! IPV      = array containing the global indices of the polygon       | 
!            vertices                                                 | 
! NTP      = last global vertex index (note that if the polygon is    | 
!            not previously truncated, then NTP=NTV)                  | 
! NTV      = total number of vertices                                 | 
! V        = liquid volume                                            | 
! VT       = total volume of the polygon                              | 
! VERTP    = vertex coordinates of the polygon                        | 
! XNC, ... = unit-lenght normal to the new edges on \Gamma_c          | 
! On return:                                                          | 
!===========                                                          | 
! C        = solution of the problem                                  | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE ENFORV2D(C,IPV,NTP,NTV,V,VT,VERTP,XNC,YNC) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NTP,NTV 
    REAL (W_P), INTENT(IN) :: V,VT 
    REAL (W_P), INTENT(IN) :: XNC,YNC 
    REAL (W_P), INTENT(OUT) :: C 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPV(NV) 
    REAL (W_P), INTENT(IN) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,I1,I2,ICUTEND,ICUTINI,ICUTNEX,IH,II,IMAX,         &
         IMAXL,IMAXLOLD,IMIN,IMINL,INVERT,IP,IP0,IP1,IP2,IPF1,IPF2,     &
         IPN,IPN0,IPREF,ISOL,IV,NCUT,NTP0,NTPINI,NTV0                     
    REAL (W_P) :: BET1,BET2,C0,C1,C2,C3,CAUX,CF1,CF2,CMAX,CMIN,         &
         CSOLN,CTR,CUT1,CUT2,DREF,DSOL,DSOLN,PHIINT,SV,TOLC,VAUX,       &
         VMAX,VMAXL,VMIN,VMINL,VMINLL,X1,XNCOR,XNCS,XNCT,XV1,XV2,Y1,    &
         YNCOR,YNCS,YNCT,YV1,YV2                                  
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IA(NV),IPIA0(NV),IPIA1(NV),IPV0(NV),LISTV(NV) 
    REAL (W_P) :: PHIV(NV),VERTP0(NV,2),XNCUT(NV),YNCUT(NV) 
    
    IF(VT.LE.0.0_W_P) THEN 
       WRITE(6,*) 'THE POLYGON HAS NULL OR NEGATIVE AREA.' 
       RETURN 
    END IF
    IF(NTP.GT.NTV) THEN
       WRITE(6,*) 'NTP>NTV. THE POLYGON MUST BE RESTORED.'
       RETURN
    END IF
    
    TOLC=1.0E-12_W_P 
    VAUX=V 
    LISTV(1)=1 
    DO IV=1,NTV 
       IA(IV)=0 
       PHIV(IV)=XNC*VERTP(IV,1)+YNC*VERTP(IV,2) 
       !* Ordered list of global vertex indices                                
       DO I=1,IV-1 
          IF(PHIV(IV).GT.PHIV(LISTV(I))) THEN 
             DO II=IV,I+1,-1 
                LISTV(II)=LISTV(II-1) 
             END DO
             LISTV(I)=IV 
             GOTO 10 
          END IF
       END DO
       LISTV(IV)=IV 
10     CONTINUE 
    END DO
    !* Begin the procedure SETIA used to obtain the brackets CMAX and CMIN  
    !* of the soluction C                                                   
    INVERT=0 
    XNCOR=XNC 
    YNCOR=YNC 
    CMAX=PHIV(LISTV(1)) 
    CMIN=PHIV(LISTV(NTP)) 
    IMIN=1 
    IMAX=NTP 
    VMIN=0.0_W_P 
    VMAX=VT 
    IMAXLOLD=NTP+1 
22  CONTINUE 
    !* Obtain the tentative solution bracketing by interpolation            
    PHIINT=PHIV(LISTV(IMIN))-(PHIV(LISTV(IMIN))-PHIV(LISTV(IMAX)))*     &
         (V-VMIN)/(VMAX-VMIN)                                         
    IMAXL=0 
    IMINL=0 
    DO IP=IMIN+1,IMAX 
       I=IP 
       IF(PHIV(LISTV(IP)).LT.PHIINT) THEN 
          IMAXL=IP 
          IMINL=IP-1 
          GOTO 11 
       END IF
    END DO
    IF(IMAXL.EQ.0.AND.IMINL.EQ.0) THEN 
       C=-PHIINT 
       RETURN 
    END IF
11  CONTINUE 
    CMAX=PHIV(LISTV(IMINL)) 
    CMIN=PHIV(LISTV(IMAXL)) 
    IF((NTP-IMAXL).LT.(IMINL-1)) THEN 
       INVERT=1 
       CAUX=CMIN 
       CMIN=-CMAX 
       CMAX=-CAUX 
       VAUX=VT-V 
       XNCT=-XNCOR 
       YNCT=-YNCOR 
       IPREF=LISTV(IMAXL) 
    ELSE 
       INVERT=0 
       VAUX=V 
       XNCT=XNCOR 
       YNCT=YNCOR 
       IPREF=LISTV(IMINL) 
    END IF
    DO I=1,NTP 
       IF(I.LE.IMINL) THEN 
          IA(LISTV(I))=1-INVERT 
       ELSE 
          IA(LISTV(I))=INVERT 
       END IF
    END DO
    !* End of procedure SETIA                                               
    CALL TRPOL2D(IPREF,IPV,IPV0,NTP,NTP0,NTV,NTV0,VERTP,VERTP0) 
    CTR=XNCT*VERTP(IPREF,1)+YNCT*VERTP(IPREF,2) 
    CMIN=CMIN-CTR 
    CMAX=CMAX-CTR 
    !* Construction of the new polygon                                      
    NTPINI=NTP0 
    CALL NEWPOL2D(IA,IPIA0,IPIA1,IPV0,NTP0,NTV0,VERTP0,XNCUT,YNCUT) 
    NCUT=NTP0-NTPINI 
    DO IP=NTPINI+1,NTP0 
       VERTP0(IP,1)=0.0_W_P 
       VERTP0(IP,2)=0.0_W_P 
       IA(IP)=0 
    END DO
    C0=-2.0_W_P*VAUX 
    C1=0.0_W_P 
    C2=0.0_W_P 
    C3=0.0_W_P 
    IF((XNCUT(1)*YNC-YNCUT(1)*XNC).GT.0.0_W_P) THEN 
       ICUTINI=1 
       ICUTEND=NCUT 
       ICUTNEX=1 
    ELSE 
       ICUTINI=NCUT 
       ICUTEND=1 
       ICUTNEX=-1 
    END IF
    XNCS=-XNCT 
    YNCS=-YNCT 
    DO I1=ICUTINI,ICUTEND,2*ICUTNEX 
       I2=I1+ICUTNEX 
       IPF1=IPIA1(I1) 
       IPF2=IPIA1(I2) 
       CF1=-(VERTP0(IPF1,1)*XNCUT(I1)+VERTP0(IPF1,2)*YNCUT(I1)) 
       CF2=-(VERTP0(IPF2,1)*XNCUT(I2)+VERTP0(IPF2,2)*YNCUT(I2)) 
       CUT1=XNCUT(I1)*YNCS-YNCUT(I1)*XNCS 
       !cut edge 1 and \Gamma_c normal are perpen
       IF(CUT1.EQ.0.0_W_P) THEN 
          BET1=0.0_W_P 
       ELSE 
          BET1=1.0_W_P/CUT1 
       END IF
       CUT2=XNCUT(I2)*YNCS-YNCUT(I2)*XNCS 
       !cut edge 2 and \Gamma_c normal are perpen
       IF(CUT2.EQ.0.0_W_P) THEN 
          BET2=0.0_W_P 
       ELSE 
          BET2=-1.0_W_P/CUT2 
       END IF
       C2=C2+(YNCUT(I2)*XNCUT(I1)-XNCUT(I2)*YNCUT(I1))*BET1*BET2 
       C1=C1-2.0_W_P*(CF2*BET2+CF1*BET1) 
       C0=C0-(XNCS*VERTP0(IPF1,1)+YNCS*VERTP0(IPF1,2))*CF1*BET1-        &
            (XNCS*VERTP0(IPF2,1)+YNCS*VERTP0(IPF2,2))*CF2*BET2        
    END DO
    IH=INT((NTV0-2)/2) 
    IP0=IPV0(1) 
    X1=VERTP0(IP0,1)*IA(IP0) 
    Y1=VERTP0(IP0,2)*IA(IP0) 
    DO I=2,IH+1 
       IV=2*I 
       IP=IPV0(IV) 
       IP1=IPV0(IV-1) 
       IP2=IPV0(IV-2) 
       XV1=VERTP0(IP1,1)*IA(IP1)-X1 
       YV1=VERTP0(IP1,2)*IA(IP1)-Y1 
       XV2=VERTP0(IP,1)*IA(IP)-VERTP0(IP2,1)*IA(IP2) 
       YV2=VERTP0(IP,2)*IA(IP)-VERTP0(IP2,2)*IA(IP2) 
       C0=C0+XV1*YV2-YV1*XV2 
    END DO
    IF(2*(IH+1).LT.NTV0) THEN 
       IPN0=IPV0(NTV0-1) 
       IPN=IPV0(NTV0) 
       XV1=VERTP0(IPN,1)*IA(IPN)-X1 
       YV1=VERTP0(IPN,2)*IA(IPN)-Y1 
       XV2=X1-VERTP0(IPN0,1)*IA(IPN0) 
       YV2=Y1-VERTP0(IPN0,2)*IA(IPN0) 
       C0=C0+XV1*YV2-YV1*XV2 
    ENDIF
    VMAXL=(C2*CMIN*CMIN+C1*CMIN+C0+2.0_W_P*VAUX)/2.0_W_P 
    VMINL=(C2*CMAX*CMAX+C1*CMAX+C0+2.0_W_P*VAUX)/2.0_W_P 
    IF(INVERT.EQ.1) THEN 
       VMINLL=VT-VMAXL 
       VMAXL=VT-VMINL 
       VMINL=VMINLL 
    END IF
    SV=(VMINL-V)*(VMAXL-V) 
    IF(SV.GT.0.0_W_P.AND.(IMAX-IMIN).GT.1.AND.IMAXLOLD.NE.IMAXL         &
         ) THEN 
       IF(VMAXL.GT.V) THEN 
          VMAX=VMINL 
          IMAX=IMINL 
       ELSE 
          VMIN=VMAXL 
          IMIN=IMAXL 
       END IF
       IMAXLOLD=IMAXL 
       GOTO 22 
    END IF
    CALL EQSOL3D(C0,C1,C2,C3,CMIN,CMAX,C) 
    DSOL=ABS(C-CMIN)+ABS(C-CMAX) 
    DREF=ABS(CMAX-CMIN) 
    IF((DSOL/DREF).GT.(1.0_W_P+TOLC)) THEN 
       CALL NEWTON3D(C0,C1,C2,C3,CMIN,CMAX,CSOLN,ISOL) 
       DSOLN=ABS(CSOLN-CMIN)+ABS(CSOLN-CMAX) 
       IF((DSOLN/DREF).GT.(1.0_W_P+TOLC)) C=CSOLN 
    END IF
    IF(INVERT.EQ.0) C=-C 
    !. DETRANSLATE                                                          
    IF(INVERT.EQ.1) THEN 
       C=C+CTR 
    ELSE 
       C=C-CTR 
    END IF
    RETURN 
  END SUBROUTINE ENFORV2D
!-----------------------    END OF ENFORV2D   ------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              TRPOL2D                                | 
!---------------------------------------------------------------------| 
!         This routine translate a polygon to a reference point       | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! VERTP    = vertex coordinates of the original polygon               | 
! IPV      = array containing the global indices of the original      | 
!            polygon vertices                                         | 
! IPREF    = reference point                                          | 
! NTP      = last global vertex index (note that if the polygon is    | 
!            not previously truncated, then NTP=NTV)                  | 
! NTV      = total number of vertices                                 | 
! On return:                                                          | 
!===========                                                          | 
! VERTP1   = vertex coordinates of the copied polygon                 | 
! IPV1     = array containing the global indices of the copied        | 
!            polygon vertices                                         | 
! NTP1     = last global vertex index (note that if the polygon is    | 
!            not previously truncated, then NTP=NTV)                  | 
! NTV1     = total number of vertices                                 | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE TRPOL2D(IPREF,IPV,IPV1,NTP,NTP1,NTV,NTV1,VERTP,VERTP1) 
    !.. Scalar Arguments         
    INTEGER(I_P), INTENT(IN) :: IPREF,NTP,NTV 
    INTEGER(I_P), INTENT(OUT) :: NTP1,NTV1 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPV(NV) 
    REAL(W_P), INTENT(IN) :: VERTP(NV,2) 
    INTEGER(I_P), INTENT(OUT) :: IPV1(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP1(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IV 
    
    NTP1=NTP 
    NTV1=NTV 
    DO IV=1,NTV 
       IP=IPV(IV) 
       IPV1(IV)=IP 
       VERTP1(IP,1)=VERTP(IP,1)-VERTP(IPREF,1) 
       VERTP1(IP,2)=VERTP(IP,2)-VERTP(IPREF,2) 
    END DO
    RETURN 
  END SUBROUTINE TRPOL2D
!-------------------------- END OF TRPOL2D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          ENFORV2DSZ                                 | 
!... Scardovelli and Zaleski version for rectangle                    | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! DX, ...  = side lengths of the rectangle                            | 
! VERTP    = vertex coordinates of the rectangle                      | 
! XNC, ... = unit-lenght normal to the new face \Gamma_c              | 
! V        = liquid volume                                            | 
! On return:                                                          | 
!===========                                                          | 
! C        = solution of the problem                                  | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE ENFORV2DSZ(C,DX,DY,V,VERTP,XNC,YNC) BIND(C) 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: DX,DY,XNC,YNC 
    REAL(W_P), INTENT(INOUT) :: V 
    REAL(W_P), INTENT(OUT) :: C 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    REAL(W_P) :: ALPHA,CI,CMAX,CMIN,M,M1,SN,V1,VBACK,VT,XM,XMI,YM,YMI 
    INTEGER(I_P) :: I,IMAX,IMIN 
    
    CMIN=1.0E+14_W_P 
    CMAX=-1.0E+14_W_P 
    VT=DX*DY 
    VBACK=V 
    V=V/VT 
    !.. The vertex indices of the rectangular parallelepiped are supposed   
    !.. to be listed from 1 to 4.                                           
    DO I=1,4 
       CI=-(VERTP(I,1)*XNC+VERTP(I,2)*YNC) 
       IF(CI.LE.CMIN) THEN 
          CMIN=CI 
          IMIN=I 
       END IF
       IF(CI.GE.CMAX) THEN 
          CMAX=CI 
          IMAX=I 
       END IF
    END DO
    !.. If the liquid volume fraction is higher than 0.5, solve the         
    !.. inverse problem                                                     
    IF((VBACK/VT).LE.(1.0_W_P/2.0_W_P)) THEN 
       CI=CMIN 
       I=IMIN 
    ELSE 
       CI=CMAX 
       I=IMAX 
       V=1.0_W_P-V 
    END IF
    !.. Normalize the plane equation                                        
    SN=ABS(XNC)+ABS(YNC) 
    XM=XNC/SN 
    YM=YNC/SN 
    XMI=XM*DX 
    YMI=YM*DY 
    SN=ABS(XMI)+ABS(YMI) 
    XM=ABS(XMI)/SN 
    YM=ABS(YMI)/SN 
    !.. Region limits                                                       
    M1=MIN(XM,YM) 
    M=M1 
    V1=M/(2.0_W_P*(1.0_W_P-M)) 
    !.. Solution of the inverse problem                                     
    IF(V.GE.0.0_W_P.AND.V.LT.V1) THEN 
       ALPHA=SQRT(2.0_W_P*M*(1.0_W_P-M)*V) 
    ELSE 
       ALPHA=V*(1.0_W_P-M)+M/2.0_W_P 
    END IF
    IF((VBACK/VT).LE.(1.0_W_P/2.0_W_P)) THEN 
       C=CMIN+ALPHA*ABS(CMAX-CMIN) 
    ELSE 
       C=CMAX-ALPHA*ABS(CMAX-CMIN) 
    END IF
    V=VBACK 
    RETURN 
  END SUBROUTINE ENFORV2DSZ
!---------------------   END OF ENFORV2DSZ   -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                             NEWPOL2D                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! IA       = 0 if \Gamma_c points out of the vertex, 1 otherwise      | 
! IPV0     = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NTP0     = last global vertex index                                 | 
! NTV0     = total number of vertices                                 | 
! VERTP0   = vertex coordinates of the polygon                        | 
! On return:                                                          | 
!===========                                                          | 
! IPV0     = array containing the global indices of the truncat. pol. | 
!            vertices                                                 | 
! NTP0     = last global vertex index                                 | 
! NTV0     = total number of vertices                                 | 
! IPIA0    = global vertex index of the original poligon with IA=0    | 
!            and which is in the edge containing the intersection     | 
!            point                                                    | 
! IPIA1    = global vertex index of the original poligon with IA=1    | 
!            and which is in the edge containing the intersection     | 
!            point                                                    | 
! XNCUT,...= unit-lenght normals to the edges cut by \Gamma_c         | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE NEWPOL2D(IA,IPIA0,IPIA1,IPV0,NTP0,NTV0,VERTP0,XNCUT,YNCUT) &
       BIND(C)                                         
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(INOUT) :: NTP0,NTV0 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(INOUT) :: IA(NV) 
    INTEGER(I_P), INTENT(INOUT) :: IPV0(NV) 
    INTEGER(I_P), INTENT(OUT) :: IPIA0(NV),IPIA1(NV) 
    REAL (W_P), INTENT(IN) :: VERTP0(NV,2) 
    REAL (W_P), INTENT(OUT) :: XNCUT(NV),YNCUT(NV) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: ICUT,IP,IP2,IV,IV2,NTV1 
    REAL (W_P) :: RMOD,XV,YV 
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IPV1(NV) 
    
    !* Determination of the cut edges                                       
    NTV1=0 
    ICUT=0 
    DO IV=1,NTV0 
       IP=IPV0(IV) 
       IV2=IV+1 
       IF(IV.EQ.NTV0) IV2=1 
       IP2=IPV0(IV2) 
       IF(IA(IP).EQ.1) THEN 
          NTV1=NTV1+1 
          IPV1(NTV1)=IPV0(IV) 
       END IF
       IF(IA(IP).NE.IA(IP2)) THEN 
          ICUT=ICUT+1 
          NTP0=NTP0+1 
          NTV1=NTV1+1 
          IPV1(NTV1)=NTP0 
          IA(NTP0)=0 
          IF(IA(IP2).EQ.0) THEN 
             IPIA0(ICUT)=IP2 
             IPIA1(ICUT)=IP 
          ELSE 
             IPIA0(ICUT)=IP 
             IPIA1(ICUT)=IP2 
          END IF
          XV=VERTP0(IP2,1)-VERTP0(IP,1) 
          YV=VERTP0(IP2,2)-VERTP0(IP,2) 
          RMOD=(XV**2+YV**2)**0.5_W_P 
          XNCUT(ICUT)=YV/RMOD 
          YNCUT(ICUT)=-XV/RMOD 
       END IF
    END DO
    NTV0=NTV1 
    DO IV=1,NTV1 
       IPV0(IV)=IPV1(IV) 
    END DO
    RETURN 
  END SUBROUTINE NEWPOL2D
!------------------------- END OF NEWPOL2D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                               INTE2D                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! C        = constant of the line containing the new edges on \Gamma_c| 
! IPV0     = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NTP0     = last global vertex index                                 | 
! NTV0     = total number of vertices                                 | 
! VERTP0   = vertex coordinates of the original polygon               | 
! XNC, ... = unit-lenght normal to the new edges on \Gamma_c          | 
! On return:                                                          | 
!===========                                                          | 
! ICONTN   = num. of vertices of the original region that are outside | 
!            the truncated region                                     | 
! ICONTP   = num. of vertices of the original region that remain in   | 
!            the truncated region                                     | 
! IPV0     = array containing the global indices of the truncat. pol. | 
!            vertices                                                 | 
! NTP0     = last global vertex index                                 | 
! NTV0     = total number of vertices                                 | 
! VERTP0   = vertex coordinates of the truncated polygon              | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INTE2D(C,ICONTN,ICONTP,IPV0,NTP0,NTV0,VERTP0,XNC,YNC)      &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(INOUT) :: NTP0,NTV0 
    INTEGER(I_P), INTENT(OUT) :: ICONTN,ICONTP 
    REAL(W_P), INTENT(IN) :: C,XNC,YNC 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(INOUT) :: IPV0(NV) 
    REAL(W_P), INTENT(INOUT) :: VERTP0(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IP0,IP1,IV,NTPINI 
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IA(NV),IPIA0(NV),IPIA1(NV) 
    REAL(W_P) :: PHIV(NV),XNCUT(NV),YNCUT(NV) 
    
    ICONTP=0 
    ICONTN=0 
    !* Distance function and values of IA                                   
    DO IV=1,NTV0 
       IP=IPV0(IV) 
       PHIV(IP)=XNC*VERTP0(IP,1)+YNC*VERTP0(IP,2)+C 
       IF(PHIV(IP).GT.0.0_W_P) THEN 
          IA(IP)=1 
          ICONTP=ICONTP+1 
       ELSE 
          IA(IP)=0 
          ICONTN=ICONTN+1 
       END IF
    END DO
    IF(ICONTP.NE.0.AND.ICONTN.NE.0) THEN 
       !* Construction of the new polygon                                      
       NTPINI=NTP0 
       CALL NEWPOL2D(IA,IPIA0,IPIA1,IPV0,NTP0,NTV0,VERTP0,XNCUT,YNCUT)        
       !* Position of the new vertices                                         
       DO IP=NTPINI+1,NTP0 
          IP0=IPIA0(IP-NTPINI) 
          IP1=IPIA1(IP-NTPINI) 
          VERTP0(IP,1)=VERTP0(IP0,1)-PHIV(IP0)*(VERTP0(IP1,1)-          &
               VERTP0(IP0,1))/(PHIV(IP1)-PHIV(IP0))                
          VERTP0(IP,2)=VERTP0(IP0,2)-PHIV(IP0)*(VERTP0(IP1,2)-          &
               VERTP0(IP0,2))/(PHIV(IP1)-PHIV(IP0))                
       END DO
    END IF
    RETURN 
  END SUBROUTINE INTE2D
!--------------------------- END OF INTE2D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              TOOLV2D                                | 
!---------------------------------------------------------------------| 
!          This routine computes the volume of a polygon              | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! VERTP    = vertex coordinates of the polygon                        | 
! IPV      = array containing the global indices of the polygon       | 
!            vertices                                                 | 
! NTV      = total number of vertices                                 | 
! On return:                                                          | 
!===========                                                          | 
! VOL      = volume of the polygon                                    | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE TOOLV2D(IPV,NTV,VERTP,VOL) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NTV 
    REAL(W_P), INTENT(OUT) :: VOL 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPV(NV) 
    REAL(W_P), INTENT(IN) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    REAL(W_P) :: SUMS,XV1,XV2,YV1,YV2 
    INTEGER(I_P) :: I,IH,IP,IP1,IP2 
    
    SUMS=0.0_W_P 
    IH=INT((NTV-2)/2) 
    DO I=2,IH+1 
       IP=2*I 
       IP1=IP-1 
       IP2=IP-2 
       XV1=VERTP(IPV(IP1),1)-VERTP(IPV(1),1) 
       YV1=VERTP(IPV(IP1),2)-VERTP(IPV(1),2) 
       XV2=VERTP(IPV(IP),1)-VERTP(IPV(IP2),1) 
       YV2=VERTP(IPV(IP),2)-VERTP(IPV(IP2),2) 
       SUMS=SUMS+XV1*YV2-YV1*XV2 
    END DO
    IF(2*(IH+1).LT.NTV) THEN 
       XV1=VERTP(IPV(NTV),1)-VERTP(IPV(1),1) 
       YV1=VERTP(IPV(NTV),2)-VERTP(IPV(1),2) 
       XV2=VERTP(IPV(1),1)-VERTP(IPV(NTV-1),1) 
       YV2=VERTP(IPV(1),2)-VERTP(IPV(NTV-1),2) 
       SUMS=SUMS+XV1*YV2-YV1*XV2 
    ENDIF
    VOL=SUMS/2.0_W_P                                                 
    RETURN 
  END SUBROUTINE TOOLV2D
!-------------------------- END OF TOOLV2D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              CPPOL2D                                | 
!---------------------------------------------------------------------| 
!         This routine copies a polygon into a new one                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! VERTP    = vertex coordinates of the original polygon               | 
! IPV      = array containing the global indices of the original      | 
!            polygon vertices                                         | 
! NTP      = last global vertex index (note that if the polygon is    | 
!            not previously truncated, then NTP=NTV)                  | 
! NTV      = total number of vertices                                 | 
! On return:                                                          | 
!===========                                                          | 
! VERTP1   = vertex coordinates of the copied polygon                 | 
! IPV1     = array containing the global indices of the copied        | 
!            polygon vertices                                         | 
! NTP1     = last global vertex index (note that if the polygon is    | 
!            not previously truncated, then NTP=NTV)                  | 
! NTV1     = total number of vertices                                 | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE CPPOL2D(IPV,IPV1,NTP,NTP1,NTV,NTV1,VERTP,VERTP1) BIND(C)   
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NTP,NTV 
    INTEGER(I_P), INTENT(OUT) :: NTP1,NTV1 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: VERTP(NV,2) 
    REAL(W_P), INTENT(OUT) :: VERTP1(NV,2) 
    INTEGER(I_P), INTENT(IN) :: IPV(NV) 
    INTEGER(I_P), INTENT(OUT) :: IPV1(NV) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IV 
    
    NTP1=NTP 
    NTV1=NTV 
    DO IV=1,NTV 
       IP=IPV(IV) 
       IPV1(IV)=IP 
       VERTP1(IP,1)=VERTP(IP,1) 
       VERTP1(IP,2)=VERTP(IP,2) 
    END DO
    
    RETURN 
  END SUBROUTINE CPPOL2D
!-------------------------- END OF CPPOL2D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            RESTORE2D                                | 
!---------------------------------------------------------------------| 
!                 This routine restores a polygon                     | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! VERTP    = vertex coordinates of the original polygon               | 
! IPV      = array containing the global indices of the original      | 
!            polygon vertices                                         | 
! NTP      = last global vertex index (note that if the polygon is    | 
!            not previously truncated, then NTP=NTV)                  | 
! NTV      = total number of vertices                                 | 
! On return:                                                          | 
!===========                                                          | 
! VERTP    = vertex coordinates of the restored polygon               | 
! IPV      = array containing the global indices of the restored      | 
!            polygon vertices                                         | 
! NTP      = last global vertex index (note that if the polygon is    | 
!            not previously truncated, then NTP=NTV)                  | 
! NTV      = total number of vertices                                 | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE RESTORE2D(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(INOUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(INOUT) :: IPV(NV) 
    REAL (W_P), INTENT(INOUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IP0,IV,IV0,IVT,NTP0,NTV0 
    REAL (W_P) :: DMOD,TOLP 
    !.. Local Arrays                                                        
    INTEGER(I_P) :: IPV0(NV) 
    REAL (W_P) :: VERTP0(NV,2) 
    
    !* Obtain the work polygon                                              
    CALL CPPOL2D(IPV,IPV0,NTP,NTP0,NTV,NTV0,VERTP,VERTP0) 
    !* Consecutive vertices with the same vector position are               
    !* eliminated. We use the tolerance TOLP                                
    TOLP=1.0E-16_W_P 
    IVT=0 
    DO IV=1,NTV0 
       IP=IPV0(IV) 
       IV0=IV-1 
       IF(IV0.EQ.0) IV0=NTV0 
       IP0=IPV0(IV0) 
       DMOD=((VERTP0(IP,1)-VERTP0(IP0,1))**2+(VERTP0(IP,2)-             &
            VERTP0(IP0,2))**2)**0.5_W_P                                 
       IF(DMOD.GT.TOLP) THEN 
          IVT=IVT+1 
          IPV(IVT)=IVT 
          VERTP(IVT,1)=VERTP0(IP,1) 
          VERTP(IVT,2)=VERTP0(IP,2) 
       END IF
    END DO
    NTV=IVT 
    NTP=IVT 
    RETURN 
  END SUBROUTINE RESTORE2D
!-------------------------- END OF RESTORE2D -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                               DIST2D                                | 
!---------------------------------------------------------------------| 
!   This routine computes the distance from a point to a segment      | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! X,Y       = vertex coordinates of the segment                       | 
! XP,YP     = coordinates of the point                                | 
! On return:                                                          | 
!===========                                                          | 
! D         = exact distance from the point (XP,YP) to the segment    | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE DIST2D(D,X,Y,XP,YP) BIND(C) 
    !.. Scalar Arguments                                                    
    REAL(W_P), INTENT(IN) :: XP,YP 
    REAL(W_P), INTENT(OUT) :: D 
    !.. Array Arguments                                                     
    REAL(W_P), INTENT(IN) :: X(2),Y(2) 
    !.. Local Scalars                                                       
    REAL(W_P) :: C1,C2,PHI1,PHI2,VMOD,XN,XNT,YN,YNT 
    
    XNT=X(2)-X(1) 
    YNT=Y(2)-Y(1) 
    VMOD=(XNT**2+YNT**2)**0.5_W_P 
    XNT=XNT/VMOD 
    YNT=YNT/VMOD 
    XN=-YNT 
    YN=XNT 
    C1=-1.0_W_P*(XNT*X(1)+YNT*Y(1)) 
    C2=1.0_W_P*(XNT*X(2)+YNT*Y(2)) 
    PHI1=XNT*XP+YNT*YP+C1 
    PHI2=-XNT*XP-YNT*YP+C2 
    IF(PHI1.GE.0.0_W_P.AND.PHI2.GE.0.0_W_P) THEN 
       D=ABS(XN*X(1)+YN*Y(1)-(XN*XP+YN*YP)) 
    ELSEIF(PHI1.LE.0.0_W_P) THEN 
       D=((XP-X(1))**2+(YP-Y(1))**2)**0.5_W_P 
    ELSE 
       D=((XP-X(2))**2+(YP-Y(2))**2)**0.5_W_P 
    END IF
    RETURN 
  END SUBROUTINE DIST2D
!--------------------------- END OF DIST2D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              INITF2D                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! FUNC2D   = external user-supplied function where the interface      | 
!            shape is analytically defined                            | 
! IPV      = array containing the global indices of the original pol. | 
!            vertices                                                 | 
! NC       = number of sub-cells along each coordinate axis of the    | 
!            superimposed Cartesian grid                              | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! TOL      = prescribed positive tolerance for the distance to the    | 
!            interface                                                | 
! VERTP    = vertex coordinates of the original polygon               | 
! On return:                                                          | 
!===========                                                          | 
! VF       = material area fraction                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE INITF2D(FUNC2D,IPV,NC,NTP,NTV,TOL,VERTP,VF) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: NC,NTP,NTV 
    REAL(W_P), INTENT(IN) :: TOL 
    REAL(W_P), INTENT(OUT) :: VF 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPV(NV) 
    REAL(W_P), INTENT(IN) :: VERTP(NV,2) 
    !.. Procedure Arguments                                                 
    PROCEDURE (VOFTOOLS_FUNC2D) :: FUNC2D 
    !.. Local Scalars                                                       
    REAL(W_P) :: CX1,CX2,CY1,CY2,DDX,DDY,DX,DY,PHIMIN,VOLF,VOLT,XC,     &
         XMAX,XMIN,XP,YC,YMAX,YMIN,YP                                 
    INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IP,IP0,IP1,IPHI,IV,JC,NTP1,      &
         NTP2,NTPINI,NTV1,NTV2                                        
    !.. Local Arrays                                                        
    REAL (W_P) :: PHIV(NV),VERTP1(NV,2),VERTP2(NV,2),XNCUT(NV),         &
         YNCUT(NV)                                                    
    INTEGER(I_P) :: IA(NV),IPIA0(NV),IPIA1(NV),IPV1(NV),IPV2(NV) 
    
    !.. Coordinate extremes of the cell and vertex tagging                  
    XMIN=1.0E+20_W_P 
    XMAX=-1.0E+20_W_P 
    YMIN=1.0E+20_W_P 
    YMAX=-1.0E+20_W_P 
    ICONTP=0 
    ICONTN=0 
    DO IV=1,NTV 
       IP=IPV(IV) 
       XP=VERTP(IP,1) 
       YP=VERTP(IP,2) 
       XMIN=DMIN1(XMIN,XP) 
       XMAX=DMAX1(XMAX,XP) 
       YMIN=DMIN1(YMIN,YP) 
       YMAX=DMAX1(YMAX,YP) 
       PHIV(IP)=FUNC2D(XP,YP) 
       IF(PHIV(IP).GE.0.0_W_P) THEN 
          IA(IP)=1 
          ICONTP=ICONTP+1 
       ELSE 
          IA(IP)=0 
          ICONTN=ICONTN+1 
       END IF
    END DO
    DX=XMAX-XMIN 
    DY=YMAX-YMIN 
    IPHI=0 
    PHIMIN=10.0_W_P*MAX(DX,DY) 
    DO I=1,NTV 
       PHIMIN=MIN(PHIMIN,ABS(PHIV(IPV(I)))) 
    END DO
    IF(PHIMIN.LT.TOL*DX) IPHI=1 
    IF(ICONTP.EQ.NTV.AND.IPHI.EQ.0) THEN 
       VF=1.0_W_P 
    ELSEIF(ICONTN.EQ.NTV.AND.IPHI.EQ.0) THEN 
       VF=0.0_W_P 
    ELSE 
       !.. Total volume VOLT of the original polygon                           
       CALL TOOLV2D(IPV,NTV,VERTP,VOLT) 
       DDX=DX/NC 
       DDY=DY/NC 
       VF=0.0_W_P 
       DO IC=1,NC 
          XC=XMIN+(IC-1)*DDX 
          CALL CPPOL2D(IPV,IPV2,NTP,NTP2,NTV,NTV2,VERTP,VERTP2) 
          CX1=-XC 
          IF(IC.GT.1) CALL INTE2D(CX1,ICONTN,ICONTP,IPV2,NTP2,NTV2,     &
               VERTP2,1.0_W_P,0.0_W_P)                                    
          CX2=XC+DDX 
          CALL INTE2D(CX2,ICONTN,ICONTP,IPV2,NTP2,NTV2,VERTP2,          &
               -1.0_W_P,0.0_W_P)                                          
          DO JC=1,NC 
             YC=YMIN+(JC-1)*DDY 
             CALL CPPOL2D(IPV2,IPV1,NTP2,NTP1,NTV2,NTV1,VERTP2,VERTP1) 
             CY1=-YC 
             IF(JC.GT.1)CALL INTE2D(CY1,ICONTN,ICONTP,IPV1,NTP1,        &
                  NTV1,VERTP1,0.0_W_P,1.0_W_P)                            
             IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
                CY2=YC+DDY 
                CALL INTE2D(CY2,ICONTN,ICONTP,IPV1,NTP1,NTV1,           &
                     VERTP1,0.0_W_P,-1.0_W_P)                             
                IF(ICONTP.NE.0) THEN 
                   ICONTP=0 
                   ICONTN=0 
                   DO IV=1,NTV1 
                      IP=IPV1(IV) 
                      XP=VERTP1(IP,1) 
                      YP=VERTP1(IP,2) 
                      PHIV(IP)=FUNC2D(XP,YP) 
                      IF(PHIV(IP).GE.0.0_W_P) THEN 
                         IA(IP)=1 
                         ICONTP=ICONTP+1 
                      ELSE 
                         IA(IP)=0 
                         ICONTN=ICONTN+1 
                      END IF
                   END DO
                   
                   IF(ICONTN.EQ.0) THEN 
                      CALL TOOLV2D(IPV1,NTV1,VERTP1,VOLF) 
                      VF=VF+VOLF                           
                   ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0) THEN 
                      NTPINI=NTP1 
                      CALL NEWPOL2D(IA,IPIA0,IPIA1,IPV1,NTP1,           &
                           NTV1,VERTP1,XNCUT,YNCUT)                   
                      !.. Location of the new intersection points   
                      DO IP=NTPINI+1,NTP1 
                         IP0=IPIA0(IP-NTPINI) 
                         IP1=IPIA1(IP-NTPINI) 
                         VERTP1(IP,1)=VERTP1(IP0,1)-PHIV(IP0)*          &
                              (VERTP1(IP1,1)-VERTP1(IP0,1))/(PHIV(IP1)- &
                              PHIV(IP0))                              
                         VERTP1(IP,2)=VERTP1(IP0,2)-PHIV(IP0)*          &
                              (VERTP1(IP1,2)-VERTP1(IP0,2))/(PHIV(IP1)- &
                              PHIV(IP0))                              
                      END DO
                      CALL TOOLV2D(IPV1,NTV1,VERTP1,VOLF) 
                      VF=VF+VOLF 
                   END IF
                END IF
             END IF
          END DO
       END DO
       VF=VF/VOLT 
    END IF
    RETURN 
  END SUBROUTINE INITF2D
!-------------------------- END OF INITF2D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                              POLOUT2D                               | 
! Write in an external file the vertex coordinates of the polygon in  | 
! two columns format to be plotted, e.g., using GNUPLOT program       | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! IFILE    = number # used to name the external file                  | 
! IPV      = array containing the global indices of the polygon       | 
!            vertices                                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = vertex coordinates of the polygon                        | 
! On return:                                                          | 
!===========                                                          | 
! pol#.out = external file                                            | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE POLOUT2D(IFILE,IPV,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: IFILE,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(IN) :: IPV(NV) 
    REAL(W_P), INTENT(IN) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IV 
    CHARACTER(12) :: FILENAME 
    
    WRITE(FILENAME,'("pol",I5.5,".out")')IFILE 
    OPEN(11, FILE=FILENAME) 
    WRITE(11,'(A7,I5.5)')'#File: ', IFILE 
    WRITE(11,'(A9,I7)')'#VERTICES',NTV 
    WRITE(11,'(A16)')'#X Y COORDINATES' 
    DO IV=1,NTV 
       IP=IPV(IV) 
       WRITE(11,'(2F12.6)')VERTP(IP,1),VERTP(IP,2) 
    END DO
    IP=IPV(1) 
    WRITE(11,'(2F12.6)')VERTP(IP,1),VERTP(IP,2) 
    CLOSE(11) 
    RETURN 
  END SUBROUTINE POLOUT2D
!------------------------- END OF POLOUT2D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            VOFTOOLS_DIM2D                           |  
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! NVOUT    = parameter for dimensioning arrays related with vertices  | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_DIM2D(NVOUT) BIND(C) 
    INTEGER(I_P), INTENT(OUT) :: NVOUT 
    NVOUT=NV 
    RETURN 
  END SUBROUTINE VOFTOOLS_DIM2D
!----------------------- END OF VOFTOOLS_DIM2D -----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!         POLYHEDRA AND POLYGONS USED FOR VOFTOOLS TESTING            |  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            DEFPOL3D                                 | 
!---------------------------------------------------------------------| 
! Polyhedron construction                                             | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! ICELLTYPE= Polyhedron type:                                         | 
!.          11, cube                                                  | 
!.          12, irregular hexahedrical polyhedron                     | 
!.          13, tetrahedron                                           | 
!.          14, dodecahedron                                          | 
!.          15, icosahedron                                           | 
!.          16, irregular polyhedron                                  | 
!.         111, non-convex pentagonal pyramid                         | 
!.         112, non-convex polyhedron obtained by subtracting a       | 
!                pyramid to a unit cube                               | 
!.         113, small stellated cube                                  | 
!.         114, non-convex hexahedron                                 | 
!.         115, stellated dodecahedron                                | 
!.         116, stellated icosahedron                                 | 
!.         117, hollowed cube                                         | 
!.         118, drilled cube                                          | 
!.         119, zig-zag prism                                         | 
!.         120, VOFTools logo                                         | 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE DEFPOL3D(ICELLTYPE,IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,     &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: ICELLTYPE 
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    
    IF(ICELLTYPE.LT.11.OR.ICELLTYPE.GT.120.OR.(ICELLTYPE.GT.16.AND.     &
         ICELLTYPE.LT.111)) THEN                                      
       WRITE(6,*)'-----------------------------------------------------' 
       WRITE(6,*)'|---------------------------------------------------|' 
       WRITE(6,*)'|*********** WARNING FOR CELL SELECTION ************|' 
       WRITE(6,*)'|---------------------------------------------------|' 
       WRITE(6,*)'-----------------------------------------------------' 
       WRITE(6,*) "1.- Edit the vofvardef file." 
       WRITE(6,*) "2.- Choose an appropriate ICELLTYPE value (",        &
            "between 11 and 16 for convex cells or between ",           &
            "111 and 120 for non-convex cells)."               
       STOP 
    END IF
    IF(ICELLTYPE.EQ.11) THEN 
       !* Cube                                                                 
       CALL VOFTOOLS_CUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.12) THEN 
       !* Irregular hexahedrical polyhedron                                    
       CALL VOFTOOLS_IHEXA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.13) THEN 
       !* Tetrahedron                                                          
       CALL VOFTOOLS_TETRA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.14) THEN 
       !* Dodecahedron                                                         
       CALL VOFTOOLS_DODECA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.15) THEN 
       ! Icosahedron                                                           
       CALL VOFTOOLS_ICOSA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.16) THEN 
       !* Irregular polyhedron                                                 
       CALL VOFTOOLS_IPOL3D(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
       
       !* Non-convex cells:                                                    
    ELSEIF(ICELLTYPE.EQ.111) THEN 
       !* Non-convex pentagonal pyramid                                        
       CALL VOFTOOLS_NCPENTAPY(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)
    ELSEIF(ICELLTYPE.EQ.112) THEN 
       !* Non-convex polyhedron obtained by subtracting a pyramid to a unit cube
       CALL VOFTOOLS_NCCUBEPY(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.113) THEN 
       !* Small stellated cube                                                 
       CALL VOFTOOLS_SCUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.114) THEN 
       !* Non-convex hexahedrical polyhedron                                   
       CALL VOFTOOLS_NCHEXA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.115) THEN 
       !* Small stellated dodecahedron                                         
       CALL VOFTOOLS_SDODECA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.116) THEN 
       !* Small stellated icosahedron                                          
       CALL VOFTOOLS_SICOSA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.117) THEN 
       !* Hollowed cube                                                        
       CALL VOFTOOLS_HCUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.118) THEN 
       !* Drilled cube                                                         
       CALL VOFTOOLS_DRCUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.119) THEN 
       !* Zig-zag prism                                                        
       CALL VOFTOOLS_ZIGZAG(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    ELSEIF(ICELLTYPE.EQ.120) THEN 
       !* VOFTools logo                                                        
       CALL VOFTOOLS_LOGO(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    END IF
    RETURN 
  END SUBROUTINE DEFPOL3D
!------------------------- END OF DEFPOL3D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            DEFPOL2D                                 | 
!---------------------------------------------------------------------| 
! Polygon construction                                                | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! ICELLTYPE= Polyhedron type:                                         | 
!.           1, square                                                | 
!.           2, hexagon                                               | 
!.           3, triangule                                             | 
!.           4, quadrangle                                            | 
!.           5, irregular pentagon                                    | 
!.           6, irregular hexagon                                     | 
!.         101, non-convex quadrangle                                 | 
!.         102, non-convex pentagon                                   | 
!.         103, non-convex hexagon                                    | 
!.         104, non-convex stellated hexagon                          | 
!.         105, hollowed square                                       | 
!.         106, non-convex multi-square polygon                       | 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE DEFPOL2D(ICELLTYPE,IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(IN) :: ICELLTYPE 
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    
    IF(ICELLTYPE.LT.1.OR.ICELLTYPE.GT.106.OR.(ICELLTYPE.GT.6.AND.       &
         ICELLTYPE.LT.101)) THEN                                      
       WRITE(6,*)'-----------------------------------------------------' 
       WRITE(6,*)'|---------------------------------------------------|' 
       WRITE(6,*)'|*********** WARNING FOR CELL SELECTION ************|' 
       WRITE(6,*)'|---------------------------------------------------|' 
       WRITE(6,*)'-----------------------------------------------------' 
       WRITE(6,*) "1.- Edit the vofvardef file." 
       WRITE(6,*) "2.- Choose an appropriate ICELLTYPE value (",        &
            "between 1 and 6 for convex cells or between 101 ",         &
            "and 106 for non-convex cells)."                   
       STOP 
    END IF
    IF(ICELLTYPE.EQ.1) THEN 
       !* Square                                                               
       CALL VOFTOOLS_SQUARE(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.2) THEN 
       !* Hexagon                                                              
       CALL VOFTOOLS_HEXAGON(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.3) THEN 
       !* Triangular mesh                                                      
       CALL VOFTOOLS_TRI(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.4) THEN 
       !* Quadrangular mesh                                                    
       CALL VOFTOOLS_QUAD(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.5) THEN 
       !* Pentagonal mesh                                                      
       CALL VOFTOOLS_PENTAGON(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.6) THEN 
       !* Irregular hexagonal mesh                                             
       CALL VOFTOOLS_IHEXAGON(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.101) THEN 
       !* Non-convex quadrangle                                                
       CALL VOFTOOLS_NCQUAD(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.102) THEN 
       !* Non-convex pentagon                                                  
       CALL VOFTOOLS_NCPENTAGON(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.103) THEN 
       !* Non-convex hexagon                                                   
       CALL VOFTOOLS_NCHEXAGON(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.104) THEN 
       !* Non-convex stellated hexagon                                         
       CALL VOFTOOLS_SHEXAGON(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.105) THEN 
       !* Hollowed square                                                      
       CALL VOFTOOLS_HSQUARE(IPV,NTP,NTV,VERTP) 
    ELSEIF(ICELLTYPE.EQ.106) THEN 
       !* Non-convex multi-square cell                                         
       CALL VOFTOOLS_MSQUARE(IPV,NTP,NTV,VERTP) 
    ENDIF
    RETURN 
  END SUBROUTINE DEFPOL2D
!------------------------- END OF DEFPOL2D ---------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_CUBE                              |  
!---------------------------------------------------------------------| 
! Unit cube                                                           | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_CUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)      &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    REAL(W_P) :: D0,D1 
    
    !          |               c          |                                 
    !          |______         c          |______                           
    !         /|      |        c         /      /|                          
    !        / |  ·3  |        c        /  ·4  / |                        
    !       /  |      |        c       /______/  |                          
    !       |·6------------    c       |      |·1|------                  
    !       | /      /         c       |  ·5  | /                          
    !       |/  ·2  /          c       |      |/                           
    !       /------/           c       /------/                             
    !      /                   c      /                                     
    !     /                    c     /                                      
    !                                                                       
    !       7/----------/3                                                  
    !       /|         /|                                                   
    !      / |        / |                                                   
    !    8/__|______4/  |                                                   
    !     |  |       |  |                                                   
    !     |  /6------|--/2                                                  
    !     | /        | /                                                    
    !     |/_________|/                                                     
    !     5           1                                                     
    !                                                                       
    D0=0.0_W_P 
    D1=1.0_W_P
    
    XNS(1)=D1 
    YNS(1)=D0 
    ZNS(1)=D0 
    XNS(2)=D0 
    YNS(2)=-D1 
    ZNS(2)=D0 
    XNS(3)=D0 
    YNS(3)=D0 
    ZNS(3)=-D1 
    XNS(4)=D0 
    YNS(4)=D1 
    ZNS(4)=D0 
    XNS(5)=D0 
    YNS(5)=D0 
    ZNS(5)=D1 
    XNS(6)=-D1 
    YNS(6)=D0 
    ZNS(6)=D0 
    NTS=6 
    NTV=8 
    NTP=NTV 
    NIPV(1)=4 
    IPV(1,1)=1 
    IPV(1,2)=2 
    IPV(1,3)=3 
    IPV(1,4)=4 
    NIPV(2)=4 
    IPV(2,1)=2 
    IPV(2,2)=1 
    IPV(2,3)=5 
    IPV(2,4)=6 
    NIPV(3)=4 
    IPV(3,1)=3 
    IPV(3,2)=2 
    IPV(3,3)=6 
    IPV(3,4)=7 
    NIPV(4)=4 
    IPV(4,1)=4 
    IPV(4,2)=3 
    IPV(4,3)=7 
    IPV(4,4)=8 
    NIPV(5)=4 
    IPV(5,1)=1 
    IPV(5,2)=4 
    IPV(5,3)=8 
    IPV(5,4)=5 
    NIPV(6)=4 
    IPV(6,1)=6 
    IPV(6,2)=5 
    IPV(6,3)=8 
    IPV(6,4)=7 
    VERTP(1,1)=D1 
    VERTP(1,2)=D0 
    VERTP(1,3)=D1 
    VERTP(2,1)=D1 
    VERTP(2,2)=D0 
    VERTP(2,3)=D0 
    VERTP(3,1)=D1 
    VERTP(3,2)=D1 
    VERTP(3,3)=D0 
    VERTP(4,1)=D1 
    VERTP(4,2)=D1 
    VERTP(4,3)=D1 
    VERTP(5,1)=D0 
    VERTP(5,2)=D0 
    VERTP(5,3)=D1 
    VERTP(6,1)=D0 
    VERTP(6,2)=D0 
    VERTP(6,3)=D0 
    VERTP(7,1)=D0 
    VERTP(7,2)=D1 
    VERTP(7,3)=D0 
    VERTP(8,1)=D0 
    VERTP(8,2)=D1 
    VERTP(8,3)=D1 
    RETURN 
  END SUBROUTINE VOFTOOLS_CUBE
!---------------------- END OF VOFTOOLS_CUBE -------------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_IHEXA                             |  
!---------------------------------------------------------------------| 
! Irregular hexahedron                                                | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_IHEXA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)     &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: ICONTN,ICONTP 
    REAL(W_P) :: C,DMOD,XNC,YNC,ZNC 
    !.. Local Arrays                                                        
    REAL(W_P) :: CS(NS) 
    
    CALL VOFTOOLS_CUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    !.. Cutting planes passing through the point (0,0,0)                    
    C=0.0_W_P 
    XNC=1.0_W_P 
    YNC=-0.1_W_P 
    ZNC=-0.1_W_P 
    DMOD=(XNC**2+YNC**2+ZNC**2)**0.5_W_P 
    XNC=XNC/DMOD 
    YNC=YNC/DMOD 
    ZNC=ZNC/DMOD 
    CALL INTE3D(C,ICONTN,ICONTP,IPV,NIPV,NTP,NTS,NTV,VERTP,XNC,         &
         XNS,YNC,YNS,ZNC,ZNS)                                         
    XNC=-0.05_W_P 
    YNC=1.0_W_P
    ZNC=-0.1_W_P
    DMOD=(XNC**2+YNC**2+ZNC**2)**0.5_W_P 
    XNC=XNC/DMOD 
    YNC=YNC/DMOD 
    ZNC=ZNC/DMOD 
    CALL INTE3D(C,ICONTN,ICONTP,IPV,NIPV,NTP,NTS,NTV,VERTP,XNC,         &
         XNS,YNC,YNS,ZNC,ZNS)                                         
    XNC=-0.05_W_P 
    YNC=-0.1_W_P
    ZNC=1.0_W_P
    DMOD=(XNC**2+YNC**2+ZNC**2)**0.5_W_P 
    XNC=XNC/DMOD 
    YNC=YNC/DMOD 
    ZNC=ZNC/DMOD 
    CALL INTE3D(C,ICONTN,ICONTP,IPV,NIPV,NTP,NTS,NTV,VERTP,XNC,         &
         XNS,YNC,YNS,ZNC,ZNS)                                         
    !.. Cutting planes passing through the point (1,1,1)                    
    XNC=-1.0_W_P 
    YNC=0.05_W_P
    ZNC=0.1_W_P
    DMOD=(XNC**2+YNC**2+ZNC**2)**0.5_W_P 
    XNC=XNC/DMOD 
    YNC=YNC/DMOD 
    ZNC=ZNC/DMOD 
    C=-1.0_W_P*(XNC+YNC+ZNC) 
    CALL INTE3D(C,ICONTN,ICONTP,IPV,NIPV,NTP,NTS,NTV,VERTP,XNC,         &
         XNS,YNC,YNS,ZNC,ZNS)                                         
    XNC=0.05_W_P 
    YNC=-1.0_W_P 
    ZNC=0.025_W_P 
    DMOD=(XNC**2+YNC**2+ZNC**2)**0.5_W_P 
    XNC=XNC/DMOD 
    YNC=YNC/DMOD 
    ZNC=ZNC/DMOD 
    C=-1.0_W_P*(XNC+YNC+ZNC) 
    CALL INTE3D(C,ICONTN,ICONTP,IPV,NIPV,NTP,NTS,NTV,VERTP,XNC,         &
         XNS,YNC,YNS,ZNC,ZNS)                                         
    XNC=0.05_W_P 
    YNC=0.05_W_P
    ZNC=-1.0_W_P 
    DMOD=(XNC**2+YNC**2+ZNC**2)**0.5_W_P 
    XNC=XNC/DMOD 
    YNC=YNC/DMOD 
    ZNC=ZNC/DMOD 
    C=-1.0_W_P*(XNC+YNC+ZNC) 
    CALL INTE3D(C,ICONTN,ICONTP,IPV,NIPV,NTP,NTS,NTV,VERTP,XNC,         &
         XNS,YNC,YNS,ZNC,ZNS)                                         
    CALL RESTORE3D(CS,IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    RETURN 
  END SUBROUTINE VOFTOOLS_IHEXA
!----------------------- END OF VOFTOOLS_IHEXA -----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_TETRA                             |  
!---------------------------------------------------------------------| 
! Tetrahedron                                                         | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_TETRA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)     &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP1,IP2,IP3,IS 
    REAL(W_P) :: DMOD,XN,XV1,XV2,YN,YV1,YV2,ZN,ZV1,ZV2 
    
    NTS=4 
    NTV=4 
    NTP=NTV 
    NIPV(1)=3 
    IPV(1,1)=1 
    IPV(1,2)=3 
    IPV(1,3)=2 
    NIPV(2)=3 
    IPV(2,1)=3 
    IPV(2,2)=1 
    IPV(2,3)=4 
    NIPV(3)=3 
    IPV(3,1)=2 
    IPV(3,2)=3 
    IPV(3,3)=4 
    NIPV(4)=3 
    IPV(4,1)=1 
    IPV(4,2)=2 
    IPV(4,3)=4 
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(1,3)=0.0_W_P 
    VERTP(2,1)=0.91_W_P 
    VERTP(2,2)=0.24_W_P 
    VERTP(2,3)=1.0_W_P 
    VERTP(3,1)=0.72_W_P 
    VERTP(3,2)=0.16_W_P 
    VERTP(3,3)=0.07_W_P 
    VERTP(4,1)=1.0_W_P 
    VERTP(4,2)=1.0_W_P 
    VERTP(4,3)=1.0_W_P 
    DO IS=1,NTS 
       IP1=IPV(IS,1) 
       IP2=IPV(IS,2) 
       IP3=IPV(IS,3) 
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    
    RETURN 
  END SUBROUTINE VOFTOOLS_TETRA
!-------------------- END OF VOFTOOLS_TETRAMESH ----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_DODECA                            | 
!---------------------------------------------------------------------| 
! Dodecahedron                                                        | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_DODECA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,        &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,IP1,IP2,IP3,IS 
    REAL(W_P) :: A,B,C,DMOD,XN,XV1,XV2,YN,YV1,YV2,ZN,ZV1,ZV2 
    
    A=1.0_W_P/(3.0_W_P)**0.5_W_P 
    B=((3.0_W_P-(5.0_W_P)**0.5_W_P)/6.0_W_P)**0.5_W_P 
    C=((3.0_W_P+(5.0_W_P)**0.5_W_P)/6.0_W_P)**0.5_W_P 
    NTS=12 
    NTV=20 
    NTP=NTV 
    I=1 
    VERTP(I,1)=A 
    VERTP(I,2)=A 
    VERTP(I,3)=A 
    I=I+1 
    VERTP(I,1)=A 
    VERTP(I,2)=A 
    VERTP(I,3)=-A 
    I=I+1 
    VERTP(I,1)=A 
    VERTP(I,2)=-A 
    VERTP(I,3)=A 
    I=I+1 
    VERTP(I,1)=A 
    VERTP(I,2)=-A 
    VERTP(I,3)=-A 
    I=I+1 
    VERTP(I,1)=-A 
    VERTP(I,2)=A 
    VERTP(I,3)=A 
    I=I+1 
    VERTP(I,1)=-A 
    VERTP(I,2)=A 
    VERTP(I,3)=-A 
    I=I+1 
    VERTP(I,1)=-A 
    VERTP(I,2)=-A 
    VERTP(I,3)=A 
    I=I+1 
    VERTP(I,1)=-A 
    VERTP(I,2)=-A 
    VERTP(I,3)=-A 
    I=I+1 
    VERTP(I,1)=B 
    VERTP(I,2)=C 
    VERTP(I,3)=0.0_W_P 
    I=I+1 
    VERTP(I,1)=-B 
    VERTP(I,2)=C 
    VERTP(I,3)=0.0_W_P 
    I=I+1 
    VERTP(I,1)=B 
    VERTP(I,2)=-C 
    VERTP(I,3)=0.0_W_P 
    I=I+1 
    VERTP(I,1)=-B 
    VERTP(I,2)=-C 
    VERTP(I,3)=0.0_W_P 
    I=I+1 
    VERTP(I,1)=C 
    VERTP(I,2)=0.0_W_P 
    VERTP(I,3)=B 
    I=I+1 
    VERTP(I,1)=C 
    VERTP(I,2)=0.0_W_P 
    VERTP(I,3)=-B 
    I=I+1 
    VERTP(I,1)=-C 
    VERTP(I,2)=0.0_W_P 
    VERTP(I,3)=B 
    I=I+1 
    VERTP(I,1)=-C 
    VERTP(I,2)=0.0_W_P 
    VERTP(I,3)=-B 
    I=I+1 
    VERTP(I,1)=0.0_W_P 
    VERTP(I,2)=B 
    VERTP(I,3)=C 
    I=I+1 
    VERTP(I,1)=0.0_W_P 
    VERTP(I,2)=-B 
    VERTP(I,3)=C 
    I=I+1 
    VERTP(I,1)=0.0_W_P 
    VERTP(I,2)=B 
    VERTP(I,3)=-C 
    I=I+1 
    VERTP(I,1)=0.0_W_P 
    VERTP(I,2)=-B 
    VERTP(I,3)=-C 
    DO IS=1,NTS 
       NIPV(IS)=5 
    END DO
    IS=1 
    I=1 
    IPV(IS,I)=1 
    I=I+1 
    IPV(IS,I)=9 
    I=I+1 
    IPV(IS,I)=10 
    I=I+1 
    IPV(IS,I)=5 
    I=I+1 
    IPV(IS,I)=17 
    IS=IS+1 
    I=1 
    IPV(IS,I)=1 
    I=I+1 
    IPV(IS,I)=17 
    I=I+1 
    IPV(IS,I)=18 
    I=I+1 
    IPV(IS,I)=3 
    I=I+1 
    IPV(IS,I)=13 
    IS=IS+1 
    I=1 
    IPV(IS,I)=13 
    I=I+1 
    IPV(IS,I)=3 
    I=I+1 
    IPV(IS,I)=11 
    I=I+1 
    IPV(IS,I)=4 
    I=I+1 
    IPV(IS,I)=14 
    IS=IS+1 
    I=1 
    IPV(IS,I)=10 
    I=I+1 
    IPV(IS,I)=6 
    I=I+1 
    IPV(IS,I)=16 
    I=I+1 
    IPV(IS,I)=15 
    I=I+1 
    IPV(IS,I)=5 
    IS=IS+1 
    I=1 
    IPV(IS,I)=4 
    I=I+1 
    IPV(IS,I)=20 
    I=I+1 
    IPV(IS,I)=19 
    I=I+1 
    IPV(IS,I)=2 
    I=I+1 
    IPV(IS,I)=14 
    IS=IS+1 
    I=1 
    IPV(IS,I)=8 
    I=I+1 
    IPV(IS,I)=12 
    I=I+1 
    IPV(IS,I)=7 
    I=I+1 
    IPV(IS,I)=15 
    I=I+1 
    IPV(IS,I)=16 
    IS=IS+1 
    I=1 
    IPV(IS,I)=1 
    I=I+1 
    IPV(IS,I)=13 
    I=I+1 
    IPV(IS,I)=14 
    I=I+1 
    IPV(IS,I)=2 
    I=I+1 
    IPV(IS,I)=9 
    IS=IS+1 
    I=1 
    IPV(IS,I)=9 
    I=I+1 
    IPV(IS,I)=2 
    I=I+1 
    IPV(IS,I)=19 
    I=I+1 
    IPV(IS,I)=6 
    I=I+1 
    IPV(IS,I)=10 
    IS=IS+1 
    I=1 
    IPV(IS,I)=17 
    I=I+1 
    IPV(IS,I)=5 
    I=I+1 
    IPV(IS,I)=15 
    I=I+1 
    IPV(IS,I)=7 
    I=I+1 
    IPV(IS,I)=18 
    IS=IS+1 
    I=1 
    IPV(IS,I)=7 
    I=I+1 
    IPV(IS,I)=12 
    I=I+1 
    IPV(IS,I)=11 
    I=I+1 
    IPV(IS,I)=3 
    I=I+1 
    IPV(IS,I)=18 
    IS=IS+1 
    I=1 
    IPV(IS,I)=8 
    I=I+1 
    IPV(IS,I)=16 
    I=I+1 
    IPV(IS,I)=6 
    I=I+1 
    IPV(IS,I)=19 
    I=I+1 
    IPV(IS,I)=20 
    IS=IS+1 
    I=1 
    IPV(IS,I)=8 
    I=I+1 
    IPV(IS,I)=20 
    I=I+1 
    IPV(IS,I)=4 
    I=I+1 
    IPV(IS,I)=11 
    I=I+1 
    IPV(IS,I)=12 
    DO IS=1,NTS 
       IP1=IPV(IS,1) 
       IP2=IPV(IS,2) 
       IP3=IPV(IS,3) 
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    RETURN 
  END SUBROUTINE VOFTOOLS_DODECA
!---------------------- END OF VOFTOOLS_DODECA -----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                         VOFTOOLS_ICOSA                              | 
!---------------------------------------------------------------------| 
! Icosahedron                                                         | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_ICOSA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)     &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,IP1,IP2,IP3,IS 
    REAL(W_P) :: A,DMOD,T,XN,XV1,XV2,YN,YV1,YV2,ZN,ZV1,ZV2 
    
    T=(1.0_W_P+(5.0_W_P)**0.5_W_P)/2.0_W_P 
    A=(1.0_W_P+T**2.0_W_P)**0.5_W_P 
    NTS=20 
    NTV=12 
    NTP=NTV 
    I=1 
    VERTP(I,1)=T/A 
    VERTP(I,2)=1.0_W_P/A 
    VERTP(I,3)=0.0_W_P/A 
    I=I+1 
    VERTP(I,1)=-T/A 
    VERTP(I,2)=1.0_W_P/A 
    VERTP(I,3)=0.0_W_P/A 
    I=I+1 
    VERTP(I,1)=T/A 
    VERTP(I,2)=-1.0_W_P/A 
    VERTP(I,3)=0.0_W_P/A 
    I=I+1 
    VERTP(I,1)=-T/A 
    VERTP(I,2)=-1.0_W_P/A 
    VERTP(I,3)=0.0_W_P/A 
    I=I+1 
    VERTP(I,1)=1.0_W_P/A 
    VERTP(I,2)=0.0_W_P/A 
    VERTP(I,3)=T/A 
    I=I+1 
    VERTP(I,1)=1.0_W_P/A 
    VERTP(I,2)=0.0_W_P/A 
    VERTP(I,3)=-T/A 
    I=I+1 
    VERTP(I,1)=-1.0_W_P/A 
    VERTP(I,2)=0.0_W_P/A 
    VERTP(I,3)=T/A 
    I=I+1 
    VERTP(I,1)=-1.0_W_P/A 
    VERTP(I,2)=0.0_W_P/A 
    VERTP(I,3)=-T/A 
    I=I+1 
    VERTP(I,1)=0.0_W_P/A 
    VERTP(I,2)=T/A 
    VERTP(I,3)=1.0_W_P/A 
    I=I+1 
    VERTP(I,1)=0.0_W_P/A 
    VERTP(I,2)=-T/A 
    VERTP(I,3)=1.0_W_P/A 
    I=I+1 
    VERTP(I,1)=0.0_W_P/A 
    VERTP(I,2)=T/A 
    VERTP(I,3)=-1.0_W_P/A 
    I=I+1 
    VERTP(I,1)=0.0_W_P/A 
    VERTP(I,2)=-T/A 
    VERTP(I,3)=-1.0_W_P/A 
    DO IS=1,NTS 
       NIPV(IS)=3 
    END DO
    IS=1 
    I=1 
    IPV(IS,I)=1 
    I=I+1 
    IPV(IS,I)=9 
    I=I+1 
    IPV(IS,I)=5 
    IS=IS+1 
    I=1 
    IPV(IS,I)=1 
    I=I+1 
    IPV(IS,I)=6 
    I=I+1 
    IPV(IS,I)=11 
    IS=IS+1 
    I=1 
    IPV(IS,I)=3 
    I=I+1 
    IPV(IS,I)=5 
    I=I+1 
    IPV(IS,I)=10 
    IS=IS+1 
    I=1 
    IPV(IS,I)=3 
    I=I+1 
    IPV(IS,I)=12 
    I=I+1 
    IPV(IS,I)=6 
    IS=IS+1 
    I=1 
    IPV(IS,I)=2 
    I=I+1 
    IPV(IS,I)=7 
    I=I+1 
    IPV(IS,I)=9 
    IS=IS+1 
    I=1 
    IPV(IS,I)=2 
    I=I+1 
    IPV(IS,I)=11 
    I=I+1 
    IPV(IS,I)=8 
    IS=IS+1 
    I=1 
    IPV(IS,I)=4 
    I=I+1 
    IPV(IS,I)=10 
    I=I+1 
    IPV(IS,I)=7 
    IS=IS+1 
    I=1 
    IPV(IS,I)=4 
    I=I+1 
    IPV(IS,I)=8 
    I=I+1 
    IPV(IS,I)=12 
    IS=IS+1 
    I=1 
    IPV(IS,I)=1 
    I=I+1 
    IPV(IS,I)=11 
    I=I+1 
    IPV(IS,I)=9 
    IS=IS+1 
    I=1 
    IPV(IS,I)=2 
    I=I+1 
    IPV(IS,I)=9 
    I=I+1 
    IPV(IS,I)=11 
    IS=IS+1 
    I=1 
    IPV(IS,I)=3 
    I=I+1 
    IPV(IS,I)=10 
    I=I+1 
    IPV(IS,I)=12 
    IS=IS+1 
    I=1 
    IPV(IS,I)=4 
    I=I+1 
    IPV(IS,I)=12 
    I=I+1 
    IPV(IS,I)=10 
    IS=IS+1 
    I=1 
    IPV(IS,I)=5 
    I=I+1 
    IPV(IS,I)=3 
    I=I+1 
    IPV(IS,I)=1 
    IS=IS+1 
    I=1 
    IPV(IS,I)=6 
    I=I+1 
    IPV(IS,I)=1 
    I=I+1 
    IPV(IS,I)=3 
    IS=IS+1 
    I=1 
    IPV(IS,I)=7 
    I=I+1 
    IPV(IS,I)=2 
    I=I+1 
    IPV(IS,I)=4 
    IS=IS+1 
    I=1 
    IPV(IS,I)=8 
    I=I+1 
    IPV(IS,I)=4 
    I=I+1 
    IPV(IS,I)=2 
    IS=IS+1 
    I=1 
    IPV(IS,I)=9 
    I=I+1 
    IPV(IS,I)=7 
    I=I+1 
    IPV(IS,I)=5 
    IS=IS+1 
    I=1 
    IPV(IS,I)=10 
    I=I+1 
    IPV(IS,I)=5 
    I=I+1 
    IPV(IS,I)=7 
    IS=IS+1 
    I=1 
    IPV(IS,I)=11 
    I=I+1 
    IPV(IS,I)=6 
    I=I+1 
    IPV(IS,I)=8 
    IS=IS+1 
    I=1 
    IPV(IS,I)=12 
    I=I+1 
    IPV(IS,I)=8 
    I=I+1 
    IPV(IS,I)=6 
    DO IS=1,NTS 
       IP1=IPV(IS,1) 
       IP2=IPV(IS,2) 
       IP3=IPV(IS,3) 
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    RETURN 
  END SUBROUTINE VOFTOOLS_ICOSA
!---------------------- END OF VOFTOOLS_ICOSA ------------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                         VOFTOOLS_IPOL3D                             | 
!---------------------------------------------------------------------| 
! Irregular polyhedron                                                | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_IPOL3D(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,        &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP1,IP2,IP3,IS 
    REAL(W_P) :: DMOD,XN,XV1,XV2,YN,YV1,YV2,ZN,ZV1,ZV2 
    
    NTP=32 
    NTV=NTP 
    NTS=18 
    VERTP(1,1)=0.542827704131611521_W_P 
    VERTP(1,2)=0.103161810115955432_W_P 
    VERTP(1,3)=0.036812175979487702_W_P 
    VERTP(2,1)=0.600855902479279003_W_P 
    VERTP(2,2)=0.086471258131132003_W_P 
    VERTP(2,3)=0.056436950730949877_W_P 
    VERTP(3,1)=0.580277964506970667_W_P 
    VERTP(3,2)=0.163039123851804080_W_P 
    VERTP(3,3)=0.063539333285191152_W_P 
    VERTP(4,1)=0.595353203042033874_W_P 
    VERTP(4,2)=0.109843129311963592_W_P 
    VERTP(4,3)=0.046191353733568030_W_P 
    VERTP(5,1)=0.543760908872757964_W_P 
    VERTP(5,2)=0.094099097938159251_W_P 
    VERTP(5,3)=0.040511888762036471_W_P 
    VERTP(6,1)=0.576819361018633514_W_P 
    VERTP(6,2)=0.166401017225910497_W_P 
    VERTP(6,3)=0.070695345095658793_W_P 
    VERTP(7,1)=0.563208132688422847_W_P 
    VERTP(7,2)=0.155406657743345611_W_P 
    VERTP(7,3)=0.108888651199260125_W_P 
    VERTP(8,1)=0.539375361775393247_W_P 
    VERTP(8,2)=0.123540417024526422_W_P 
    VERTP(8,3)=0.108841211139604044_W_P 
    VERTP(9,1)=0.567496472062291590_W_P 
    VERTP(9,2)=0.128649916760601390_W_P 
    VERTP(9,3)=0.113035361390195654_W_P 
    VERTP(10,1)=0.600028673063590978_W_P 
    VERTP(10,2)=0.085143233872209040_W_P 
    VERTP(10,3)=0.059111439263878407_W_P 
    VERTP(11,1)=0.526213727798502173_W_P 
    VERTP(11,2)=0.075636612108421930_W_P 
    VERTP(11,3)=0.077638126137438007_W_P 
    VERTP(12,1)=0.585556321506447985_W_P 
    VERTP(12,2)=0.087406427365641859_W_P 
    VERTP(12,3)=0.092250691458415329_W_P 
    VERTP(13,1)=0.559954651117444135_W_P 
    VERTP(13,2)=0.133408124832590513_W_P 
    VERTP(13,3)=0.115142136143722096_W_P 
    VERTP(14,1)=0.524564746594361031_W_P 
    VERTP(14,2)=0.076122995267018601_W_P 
    VERTP(14,3)=0.083047795609934638_W_P 
    VERTP(15,1)=0.564747090248686634_W_P 
    VERTP(15,2)=0.145410923059303421_W_P 
    VERTP(15,3)=0.110587477743786994_W_P 
    VERTP(16,1)=0.514395820566891815_W_P 
    VERTP(16,2)=0.112406169868730282_W_P 
    VERTP(16,3)=0.074847147170632553_W_P 
    VERTP(17,1)=0.561075920034260656_W_P 
    VERTP(17,2)=0.154023426807431363_W_P 
    VERTP(17,3)=0.110265478973935432_W_P 
    VERTP(18,1)=0.600086961628965465_W_P 
    VERTP(18,2)=0.099753327716150253_W_P 
    VERTP(18,3)=0.051150970749093465_W_P 
    VERTP(19,1)=0.523529840650993616_W_P 
    VERTP(19,2)=0.075758256340824406_W_P 
    VERTP(19,3)=0.081652754048494577_W_P 
    VERTP(20,1)=0.580306952541070453_W_P 
    VERTP(20,2)=0.163300101039615730_W_P 
    VERTP(20,3)=0.064077552617180802_W_P 
    VERTP(21,1)=0.560784564570740995_W_P 
    VERTP(21,2)=0.154556861208633767_W_P 
    VERTP(21,3)=0.110001263915814051_W_P 
    VERTP(22,1)=0.562766593882476296_W_P 
    VERTP(22,2)=0.155209023571326599_W_P 
    VERTP(22,3)=0.109311173701962666_W_P 
    VERTP(23,1)=0.535792240519188834_W_P 
    VERTP(23,2)=0.158071087967216972_W_P 
    VERTP(23,3)=0.055846886029540778_W_P 
    VERTP(24,1)=0.562461680790533380_W_P 
    VERTP(24,2)=0.155100229495437003_W_P 
    VERTP(24,3)=0.109460804789442229_W_P 
    VERTP(25,1)=0.528789432867762255_W_P 
    VERTP(25,2)=0.128164972986322317_W_P 
    VERTP(25,3)=0.044046149723425451_W_P 
    VERTP(26,1)=0.535717736632420283_W_P 
    VERTP(26,2)=0.158416280041318303_W_P 
    VERTP(26,3)=0.056565341810804984_W_P 
    VERTP(27,1)=0.527966627100669772_W_P 
    VERTP(27,2)=0.148427477131785279_W_P 
    VERTP(27,3)=0.097455495587370988_W_P 
    VERTP(28,1)=0.531197945823301376_W_P 
    VERTP(28,2)=0.154922874892573614_W_P 
    VERTP(28,3)=0.054094280101616717_W_P 
    VERTP(29,1)=0.519703120392784435_W_P 
    VERTP(29,2)=0.149093981287893751_W_P 
    VERTP(29,3)=0.082950196610910618_W_P 
    VERTP(30,1)=0.530093766604715744_W_P 
    VERTP(30,2)=0.156612444958861563_W_P 
    VERTP(30,3)=0.058283874375187901_W_P 
    VERTP(31,1)=0.518229286434464531_W_P 
    VERTP(31,2)=0.144572125378080146_W_P 
    VERTP(31,3)=0.084271163208895244_W_P 
    VERTP(32,1)=0.520436917533184662_W_P 
    VERTP(32,2)=0.148367611160416940_W_P 
    VERTP(32,3)=0.087663831740394063_W_P 
    
    NIPV(1)= 5 
    NIPV(2)=9 
    NIPV(3)=4 
    NIPV(4)=5 
    NIPV(5)=4 
    NIPV(6)=6 
    NIPV(7)=6 
    NIPV(8)=10 
    NIPV(9)=3 
    NIPV(10)=7 
    NIPV(11)=5 
    NIPV(12)=5 
    NIPV(13)=6 
    NIPV(14)=5 
    NIPV(15)=6 
    NIPV(16)=3 
    NIPV(17)=4 
    NIPV(18)=3 
    
    !      IPV(1,1:NIPV(1))=(/5,1,4,18,2/)                                  
    IPV(1,1)=5 
    IPV(1,2)=1 
    IPV(1,3)=4 
    IPV(1,4)=18 
    IPV(1,5)=2 
    
    !      IPV(2,1:NIPV(2))=(/18,20,6,7,15,9,12,10,2/)                      
    IPV(2,1)=18 
    IPV(2,2)=20 
    IPV(2,3)=6 
    IPV(2,4)=7 
    IPV(2,5)=15 
    IPV(2,6)=9 
    IPV(2,7)=12 
    IPV(2,8)=10 
    IPV(2,9)=2 
    
    !      IPV(3,::)=(/10,11,5,2/)                                          
    IPV(3,1)=10 
    IPV(3,2)=11 
    IPV(3,3)=5 
    IPV(3,4)=2 
    
    !      IPV(4,1:NIPV(4))=(/23,26,6,20,3/)                                
    IPV(4,1)=23 
    IPV(4,2)=26 
    IPV(4,3)=6 
    IPV(4,4)=20 
    IPV(4,5)=3 
    
    !      IPV(5,1:NIPV(5))=(/20,18,4,3/)                                   
    IPV(5,1)=20 
    IPV(5,2)=18 
    IPV(5,3)=4 
    IPV(5,4)=3 
    
    !      IPV(6,1:NIPV(6))=(/4,1,25,28,23,3/)                              
    IPV(6,1)=4 
    IPV(6,2)=1 
    IPV(6,3)=25 
    IPV(6,4)=28 
    IPV(6,5)=23 
    IPV(6,6)=3 
    
    !      IPV(7,1:NIPV(7))=(/11,19,16,25,1,5/)                             
    IPV(7,1)=11 
    IPV(7,2)=19 
    IPV(7,3)=16 
    IPV(7,4)=25 
    IPV(7,5)=1 
    IPV(7,6)=5 
    
    !      IPV(8,1:NIPV(8))=(/26,30,29,32,27,21,24,22,7,6/)                 
    IPV(8,1)=26 
    IPV(8,2)=30 
    IPV(8,3)=29 
    IPV(8,4)=32 
    IPV(8,5)=27 
    IPV(8,6)=21 
    IPV(8,7)=24 
    IPV(8,8)=22 
    IPV(8,9)=7 
    IPV(8,10)=6 
    
    !      IPV(9,1:NIPV(9))=(/22,15,7/)                                     
    IPV(9,1)=22 
    IPV(9,2)=15 
    IPV(9,3)=7 
    
    !      IPV(10,1:NIPV(10))=(/27,32,31,16,19,14,8/)                       
    IPV(10,1)=27 
    IPV(10,2)=32 
    IPV(10,3)=31 
    IPV(10,4)=16 
    IPV(10,5)=19 
    IPV(10,6)=14 
    IPV(10,7)=8 
    
    !      IPV(11,1:NIPV(11))=(/14,12,9,13,8/)                              
    IPV(11,1)=14 
    IPV(11,2)=12 
    IPV(11,3)=9 
    IPV(11,4)=13 
    IPV(11,5)=8 
    
    !      IPV(12,1:NIPV(12))=(/13,17,21,27,8/)                             
    IPV(12,1)=13 
    IPV(12,2)=17 
    IPV(12,3)=21 
    IPV(12,4)=27 
    IPV(12,5)=8 
    
    !      IPV(13,1:NIPV(13))=(/15,22,24,17,13,9/)                          
    IPV(13,1)=15 
    IPV(13,2)=22 
    IPV(13,3)=24 
    IPV(13,4)=17 
    IPV(13,5)=13 
    IPV(13,6)=9 
    
    !      IPV(14,1:NIPV(14))=(/12,14,19,11,10/)                            
    IPV(14,1)=12 
    IPV(14,2)=14 
    IPV(14,3)=19 
    IPV(14,4)=11 
    IPV(14,5)=10 
    
    !      IPV(15,1:NIPV(15))=(/31,29,30,28,25,16/)                         
    IPV(15,1)=31 
    IPV(15,2)=29 
    IPV(15,3)=30 
    IPV(15,4)=28 
    IPV(15,5)=25 
    IPV(15,6)=16 
    
    !      IPV(16,1:NIPV(16))=(/24,21,17/)                                  
    IPV(16,1)=24 
    IPV(16,2)=21 
    IPV(16,3)=17 
    
    !      IPV(17,1:NIPV(17))=(/28,30,26,23/)                               
    IPV(17,1)=28 
    IPV(17,2)=30 
    IPV(17,3)=26 
    IPV(17,4)=23 
    
    !      IPV(18,1:NIPV(18))=(/31,32,29/)                                  
    IPV(18,1)=31 
    IPV(18,2)=32 
    IPV(18,3)=29 
    
    DO IS=1,NTS 
       IP1=IPV(IS,1) 
       IP2=IPV(IS,2) 
       IP3=IPV(IS,3) 
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    
    RETURN 
  END SUBROUTINE VOFTOOLS_IPOL3D
!---------------------- END OF VOFTOOLS_IPOL3D -----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_DCUBE                             | 
!---------------------------------------------------------------------| 
! Polyhedron obtained by moving vertices 4 and 7 of the unit cube     | 
! along the y axis and decomposing the original face 4 into the new   | 
! triangular faces 4 and 7                                            | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_DCUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,         &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IS 
    REAL(W_P) :: AMOD,D0,D1,XM,XV1,XV2,YM,YV1,YV2,ZM,ZV1,ZV2 
    
    D0=0.0_W_P 
    D1=1.0_W_P 
    
    XNS(1)=D1 
    YNS(1)=D0 
    ZNS(1)=D0 
    XNS(2)=D0 
    YNS(2)=-D1 
    ZNS(2)=D0 
    XNS(3)=D0 
    YNS(3)=D0 
    ZNS(3)=-D1 
    XNS(5)=D0 
    YNS(5)=D0 
    ZNS(5)=D1 
    XNS(6)=-D1 
    YNS(6)=D0 
    ZNS(6)=D0 
    NTS=7 
    NTV=8 
    NTP=NTV 
    NIPV(1)=4 
    IPV(1,1)=1 
    IPV(1,2)=2 
    IPV(1,3)=3 
    IPV(1,4)=4 
    NIPV(2)=4 
    IPV(2,1)=2 
    IPV(2,2)=1 
    IPV(2,3)=5 
    IPV(2,4)=6 
    NIPV(3)=4 
    IPV(3,1)=3 
    IPV(3,2)=2 
    IPV(3,3)=6 
    IPV(3,4)=7 
    NIPV(4)=3 
    IPV(4,1)=4 
    IPV(4,2)=3 
    IPV(4,3)=7 
    NIPV(5)=4 
    IPV(5,1)=1 
    IPV(5,2)=4 
    IPV(5,3)=8 
    IPV(5,4)=5 
    NIPV(6)=4 
    IPV(6,1)=6 
    IPV(6,2)=5 
    IPV(6,3)=8 
    IPV(6,4)=7 
    NIPV(7)=3 
    IPV(7,1)=4 
    IPV(7,2)=7 
    IPV(7,3)=8 
    VERTP(1,1)=D1 
    VERTP(1,2)=D0 
    VERTP(1,3)=D1 
    VERTP(2,1)=D1 
    VERTP(2,2)=D0 
    VERTP(2,3)=D0 
    VERTP(3,1)=D1 
    VERTP(3,2)=D1 
    VERTP(3,3)=D0 
    VERTP(4,1)=D1 
    VERTP(4,2)=0.25_W_P 
    VERTP(4,3)=D1 
    VERTP(5,1)=D0 
    VERTP(5,2)=D0 
    VERTP(5,3)=D1 
    VERTP(6,1)=D0 
    VERTP(6,2)=D0 
    VERTP(6,3)=D0 
    VERTP(7,1)=D0 
    VERTP(7,2)=0.25_W_P 
    VERTP(7,3)=D0 
    VERTP(8,1)=D0 
    VERTP(8,2)=D1 
    VERTP(8,3)=D1 
    ! Orientation of the triangular face 4:                                 
    IS=4 
    XV1=VERTP(IPV(IS,2),1)-VERTP(IPv(IS,1),1) 
    YV1=VERTP(IPv(IS,2),2)-VERTP(IPv(IS,1),2) 
    ZV1=VERTP(IPv(IS,2),3)-VERTP(IPv(IS,1),3) 
    XV2=VERTP(IPv(IS,3),1)-VERTP(IPv(IS,2),1) 
    YV2=VERTP(IPv(IS,3),2)-VERTP(IPv(IS,2),2) 
    ZV2=VERTP(IPv(IS,3),3)-VERTP(IPv(IS,2),3) 
    XM=YV1*ZV2-ZV1*YV2 
    YM=ZV1*XV2-XV1*ZV2 
    ZM=XV1*YV2-YV1*XV2 
    AMOD=(XM**2+YM**2+ZM**2)**0.5_W_P 
    XNS(IS)=XM/AMOD 
    YNS(IS)=YM/AMOD 
    ZNS(IS)=ZM/AMOD 
    ! Orientation of the triangular face 7:                                 
    IS=7 
    XV1=VERTP(IPV(IS,2),1)-VERTP(IPv(IS,1),1) 
    YV1=VERTP(IPv(IS,2),2)-VERTP(IPv(IS,1),2) 
    ZV1=VERTP(IPv(IS,2),3)-VERTP(IPv(IS,1),3) 
    XV2=VERTP(IPv(IS,3),1)-VERTP(IPv(IS,2),1) 
    YV2=VERTP(IPv(IS,3),2)-VERTP(IPv(IS,2),2) 
    ZV2=VERTP(IPv(IS,3),3)-VERTP(IPv(IS,2),3) 
    XM=YV1*ZV2-ZV1*YV2 
    YM=ZV1*XV2-XV1*ZV2 
    ZM=XV1*YV2-YV1*XV2 
    AMOD=(XM**2+YM**2+ZM**2)**0.5_W_P 
    XNS(IS)=XM/AMOD 
    YNS(IS)=YM/AMOD 
    ZNS(IS)=ZM/AMOD 
    RETURN 
  END SUBROUTINE VOFTOOLS_DCUBE
!---------------------- END OF VOFTOOLS_DCUBE ------------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                         VOFTOOLS_NCPENTAPY                          | 
!---------------------------------------------------------------------| 
! Non-convex pentagonal pyramid                                       | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_NCPENTAPY(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,     &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IS 
    REAL(W_P) :: AMOD,XM,XV1,XV2,YM,YV1,YV2,ZM,ZV1,ZV2 
    
    NTS=6 
    NTV=6 
    NTP=NTV 
    
    VERTP(1,1)=0.04_W_P 
    VERTP(1,2)=0.77_W_P 
    VERTP(1,3)=0.0_W_P 
    VERTP(2,1)=0.0_W_P 
    VERTP(2,2)=0.0_W_P 
    VERTP(2,3)=0.0_W_P 
    VERTP(3,1)=0.49_W_P 
    VERTP(3,2)=0.22_W_P 
    VERTP(3,3)=0.0_W_P 
    VERTP(4,1)=1.0_W_P 
    VERTP(4,2)=0.13_W_P 
    VERTP(4,3)=0.0_W_P 
    VERTP(5,1)=0.16_W_P 
    VERTP(5,2)=1.0_W_P 
    VERTP(5,3)=0.0_W_P 
    VERTP(6,1)=0.1_W_P 
    VERTP(6,2)=0.5_W_P 
    VERTP(6,3)=1.0_W_P 
    
    !. IS=1                                                                 
    NIPV(1)=5 
    IPV(1,1)=1 
    IPV(1,2)=5 
    IPV(1,3)=4 
    IPV(1,4)=3 
    IPV(1,5)=2 
    !. IS=2                                                                 
    NIPV(2)=3 
    IPV(2,1)=1 
    IPV(2,2)=2 
    IPV(2,3)=6 
    !. IS=3                                                                 
    NIPV(3)=3 
    IPV(3,1)=2 
    IPV(3,2)=3 
    IPV(3,3)=6 
    !. IS=4                                                                 
    NIPV(4)=3 
    IPV(4,1)=3 
    IPV(4,2)=4 
    IPV(4,3)=6 
    !. IS=5                                                                 
    NIPV(5)=3 
    IPV(5,1)=4 
    IPV(5,2)=5 
    IPV(5,3)=6 
    !. IS=6                                                                 
    NIPV(6)=3 
    IPV(6,1)=5 
    IPV(6,2)=1 
    IPV(6,3)=6 
    
    DO IS=1,NTS 
       XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1) 
       YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2) 
       ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3) 
       XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1) 
       YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2) 
       ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3) 
       XM=YV1*ZV2-ZV1*YV2 
       YM=ZV1*XV2-XV1*ZV2 
       ZM=XV1*YV2-YV1*XV2 
       AMOD=(XM**2+YM**2+ZM**2)**0.5_W_P 
       XNS(IS)=XM/AMOD 
       YNS(IS)=YM/AMOD 
       ZNS(IS)=ZM/AMOD 
    END DO
    
    RETURN 
  END SUBROUTINE VOFTOOLS_NCPENTAPY
!--------------------- END OF VOFTOOLS_NCPENTAPY ---------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_NCCUBEPY                          | 
!---------------------------------------------------------------------| 
! Non-convex polyhedron obtained by subtracting a pyramid to a unit   | 
! cube                                                                | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_NCCUBEPY(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,      &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IS 
    REAL(W_P) :: D0,D1,AMOD,XM,XV1,XV2,YM,YV1,YV2,ZM,ZV1,ZV2 
    
    D0=0.0_W_P 
    D1=1.0_W_P
    
    NTS=9 
    NTV=9 
    NTP=NTV 
    NIPV(1)=4 
    IPV(1,1)=1 
    IPV(1,2)=2 
    IPV(1,3)=3 
    IPV(1,4)=4 
    NIPV(2)=4 
    IPV(2,1)=2 
    IPV(2,2)=1 
    IPV(2,3)=5 
    IPV(2,4)=6 
    NIPV(3)=4 
    IPV(3,1)=3 
    IPV(3,2)=2 
    IPV(3,3)=6 
    IPV(3,4)=7 
    NIPV(4)=3 
    IPV(4,1)=4 
    IPV(4,2)=9 
    IPV(4,3)=8 
    NIPV(5)=4 
    IPV(5,1)=1 
    IPV(5,2)=4 
    IPV(5,3)=8 
    IPV(5,4)=5 
    NIPV(6)=4 
    IPV(6,1)=6 
    IPV(6,2)=5 
    IPV(6,3)=8 
    IPV(6,4)=7 
    
    NIPV(7)=3 
    IPV(7,1)=7 
    IPV(7,2)=8 
    IPV(7,3)=9 
    
    NIPV(8)=3 
    IPV(8,1)=3 
    IPV(8,2)=7 
    IPV(8,3)=9 
    
    NIPV(9)=3 
    IPV(9,1)=4 
    IPV(9,2)=3 
    IPV(9,3)=9 
    
    VERTP(1,1)=D1 
    VERTP(1,2)=D0 
    VERTP(1,3)=D1 
    VERTP(2,1)=D1 
    VERTP(2,2)=D0 
    VERTP(2,3)=D0 
    VERTP(3,1)=D1 
    VERTP(3,2)=D1 
    VERTP(3,3)=D0 
    VERTP(4,1)=D1 
    VERTP(4,2)=D1 
    VERTP(4,3)=D1 
    VERTP(5,1)=D0 
    VERTP(5,2)=D0 
    VERTP(5,3)=D1 
    VERTP(6,1)=D0 
    VERTP(6,2)=D0 
    VERTP(6,3)=D0 
    VERTP(7,1)=D0 
    VERTP(7,2)=D1 
    VERTP(7,3)=D0 
    VERTP(8,1)=D0 
    VERTP(8,2)=D1 
    VERTP(8,3)=D1 
    
    VERTP(9,1)=0.5_W_P 
    VERTP(9,2)=0.5_W_P
    VERTP(9,3)=0.5_W_P
        
    DO IS=1,NTS 
       XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1) 
       YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2) 
       ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3) 
       XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1) 
       YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2) 
       ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3) 
       XM=YV1*ZV2-ZV1*YV2 
       YM=ZV1*XV2-XV1*ZV2 
       ZM=XV1*YV2-YV1*XV2 
       AMOD=(XM**2+YM**2+ZM**2)**0.5_W_P 
       XNS(IS)=XM/AMOD 
       YNS(IS)=YM/AMOD 
       ZNS(IS)=ZM/AMOD 
    END DO
    
    RETURN 
  END SUBROUTINE VOFTOOLS_NCCUBEPY
!--------------------- END OF VOFTOOLS_NCCUBEPY ----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_SCUBE                            | 
!---------------------------------------------------------------------| 
! Small stellated cubicmesh                                           | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_SCUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)     &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IP1,IP2,IP3,IS,IV,IV2,NTP0,NTS0,NTSI 
    REAL(W_P) :: A,DMOD,XC,XN,XV1,XV2,YC,YN,YV1,YV2,ZC,ZN,ZV1,ZV2 
    
    CALL VOFTOOLS_CUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    NTS0=NTS 
    NTSI=NTS 
    NTP0=NTP 
    A=1.0_W_P 
    !.. Face centroid                                                       
    DO IS=1,NTS 
       XC=0.0_W_P 
       YC=0.0_W_P 
       ZC=0.0_W_P 
       DO IV=1,NIPV(IS) 
          IP=IPV(IS,IV) 
          XC=XC+VERTP(IP,1) 
          YC=YC+VERTP(IP,2) 
          ZC=ZC+VERTP(IP,3) 
       END DO
       NTP0=NTP0+1 
       VERTP(NTP0,1)=XC/NIPV(IS)+A*XNS(IS) 
       VERTP(NTP0,2)=YC/NIPV(IS)+A*YNS(IS) 
       VERTP(NTP0,3)=ZC/NIPV(IS)+A*ZNS(IS) 
       
       DO IV=1,NIPV(IS) 
          IV2=IV+1 
          IF(IV.EQ.NIPV(IS)) IV2=1 
          NTS0=NTS0+1 
          NIPV(NTS0)=3 
          IPV(NTS0,1)=IPV(IS,IV) 
          IPV(NTS0,2)=IPV(IS,IV2) 
          IPV(NTS0,3)=NTP0 
       END DO
    END DO
    
    NTS=NTS0-NTSI 
    DO IS=1,NTS 
       NIPV(IS)=NIPV(NTSI+IS) 
       DO IV=1,NIPV(IS) 
          IPV(IS,IV)=IPV(NTSI+IS,IV) 
       END DO
    END DO
    NTP=NTP0 
    NTV=NTP 
    DO IS=1,NTS 
       IP1=IPV(IS,1) 
       IP2=IPV(IS,2) 
       IP3=IPV(IS,3) 
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    RETURN 
  END SUBROUTINE VOFTOOLS_SCUBE
!----------------------- END OF XVOFTOOS_SCUBE -----------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_NCHEXA                           | 
!---------------------------------------------------------------------| 
! Non-convex hexahedron                                               | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_NCHEXA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,        &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP1,IP2,IP3,IS 
    REAL(W_P) :: D0,D1,DMOD,XN,XV1,XV2,YN,YV1,YV2,ZN,ZV1,ZV2 
    
    D0=0.0_W_P 
    D1=1.0_W_P
    
    NTS=6 
    NTV=8 
    NTP=NTV 
    NIPV(1)=4 
    IPV(1,1)=1 
    IPV(1,2)=2 
    IPV(1,3)=3 
    IPV(1,4)=4 
    NIPV(2)=4 
    IPV(2,1)=2 
    IPV(2,2)=1 
    IPV(2,3)=5 
    IPV(2,4)=6 
    NIPV(3)=4 
    IPV(3,1)=3 
    IPV(3,2)=2 
    IPV(3,3)=6 
    IPV(3,4)=7 
    NIPV(4)=4 
    IPV(4,1)=4 
    IPV(4,2)=3 
    IPV(4,3)=7 
    IPV(4,4)=8 
    NIPV(5)=4 
    IPV(5,1)=1 
    IPV(5,2)=4 
    IPV(5,3)=8 
    IPV(5,4)=5 
    NIPV(6)=4 
    IPV(6,1)=6 
    IPV(6,2)=5 
    IPV(6,3)=8 
    IPV(6,4)=7 
    VERTP(1,1)=0.5_W_P 
    VERTP(1,2)=0.75_W_P
    VERTP(1,3)=D1 
    VERTP(2,1)=0.5_W_P
    VERTP(2,2)=0.75_W_P
    VERTP(2,3)=D0 
    VERTP(3,1)=D1 
    VERTP(3,2)=D1 
    VERTP(3,3)=D0 
    VERTP(4,1)=D1 
    VERTP(4,2)=D1 
    VERTP(4,3)=D1 
    VERTP(5,1)=D0 
    VERTP(5,2)=D0 
    VERTP(5,3)=D1 
    VERTP(6,1)=D0 
    VERTP(6,2)=D0 
    VERTP(6,3)=D0 
    VERTP(7,1)=D0 
    VERTP(7,2)=D1 
    VERTP(7,3)=D0 
    VERTP(8,1)=D0 
    VERTP(8,2)=D1 
    VERTP(8,3)=D1 
    
    DO IS=1,NTS 
       IP1=IPV(IS,1) 
       IP2=IPV(IS,2) 
       IP3=IPV(IS,3) 
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    
    RETURN 
  END SUBROUTINE VOFTOOLS_NCHEXA
!---------------------- END OF VOFTOOLS_NCHEXA -----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_SDODECA                           | 
!---------------------------------------------------------------------| 
! Small stellated dodecahedron                                        | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_SDODECA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,       &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IP1,IP2,IP3,IS,IV,IV2,NTP0,NTS0,NTSI 
    REAL(W_P) :: A,DMOD,XC,XN,XV1,XV2,YC,YN,YV1,YV2,ZC,ZN,ZV1,ZV2 
    
    CALL VOFTOOLS_DODECA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    NTS0=NTS 
    NTSI=NTS 
    NTP0=NTP 
    A=0.5_W_P 
    !.. Face centroid                                                       
    DO IS=1,NTS 
       XC=0.0_W_P 
       YC=0.0_W_P 
       ZC=0.0_W_P 
       DO IV=1,NIPV(IS) 
          IP=IPV(IS,IV) 
          XC=XC+VERTP(IP,1) 
          YC=YC+VERTP(IP,2) 
          ZC=ZC+VERTP(IP,3) 
       END DO
       NTP0=NTP0+1 
       VERTP(NTP0,1)=XC/NIPV(IS)+A*XNS(IS) 
       VERTP(NTP0,2)=YC/NIPV(IS)+A*YNS(IS) 
       VERTP(NTP0,3)=ZC/NIPV(IS)+A*ZNS(IS) 
       
       DO IV=1,NIPV(IS) 
          IV2=IV+1 
          IF(IV.EQ.NIPV(IS)) IV2=1 
          NTS0=NTS0+1 
          NIPV(NTS0)=3 
          IPV(NTS0,1)=IPV(IS,IV) 
          IPV(NTS0,2)=IPV(IS,IV2) 
          IPV(NTS0,3)=NTP0 
       END DO
    END DO
    
    NTS=NTS0-NTSI 
    DO IS=1,NTS 
       NIPV(IS)=NIPV(NTSI+IS) 
       DO IV=1,NIPV(IS) 
          IPV(IS,IV)=IPV(NTSI+IS,IV) 
       END DO
    END DO
    NTP=NTP0 
    NTV=NTP 
    DO IS=1,NTS 
       IP1=IPV(IS,1) 
       IP2=IPV(IS,2) 
       IP3=IPV(IS,3) 
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    RETURN 
  END SUBROUTINE VOFTOOLS_SDODECA
!---------------------- END OF VOFTOOLS_SDODECA ----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_SICOSA                           | 
!---------------------------------------------------------------------| 
! Small stellated icosahedron                                         | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_SICOSA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,        &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP,IP1,IP2,IP3,IS,IV,IV2,NTP0,NTS0,NTSI 
    REAL(W_P) :: A,DMOD,XC,XN,XV1,XV2,YC,YN,YV1,YV2,ZC,ZN,ZV1,ZV2 
    
    CALL VOFTOOLS_ICOSA(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS) 
    NTS0=NTS 
    NTSI=NTS 
    NTP0=NTP 
    A=1.0_W_P 
    !.. Face centroid                                                       
    DO IS=1,NTS 
       XC=0.0_W_P 
       YC=0.0_W_P 
       ZC=0.0_W_P 
       DO IV=1,NIPV(IS) 
          IP=IPV(IS,IV) 
          XC=XC+VERTP(IP,1) 
          YC=YC+VERTP(IP,2) 
          ZC=ZC+VERTP(IP,3) 
       END DO
       NTP0=NTP0+1 
       VERTP(NTP0,1)=XC/NIPV(IS)+A*XNS(IS) 
       VERTP(NTP0,2)=YC/NIPV(IS)+A*YNS(IS) 
       VERTP(NTP0,3)=ZC/NIPV(IS)+A*ZNS(IS) 
       
       DO IV=1,NIPV(IS) 
          IV2=IV+1 
          IF(IV.EQ.NIPV(IS)) IV2=1 
          NTS0=NTS0+1 
          NIPV(NTS0)=3 
          IPV(NTS0,1)=IPV(IS,IV) 
          IPV(NTS0,2)=IPV(IS,IV2) 
          IPV(NTS0,3)=NTP0 
       END DO
    END DO
    
    NTS=NTS0-NTSI 
    DO IS=1,NTS 
       NIPV(IS)=NIPV(NTSI+IS) 
       DO IV=1,NIPV(IS) 
          IPV(IS,IV)=IPV(NTSI+IS,IV) 
       END DO
    END DO
    NTP=NTP0 
    NTV=NTP 
    DO IS=1,NTS 
       IP1=IPV(IS,1) 
       IP2=IPV(IS,2) 
       IP3=IPV(IS,3) 
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    RETURN 
  END SUBROUTINE VOFTOOLS_SICOSA
!---------------------- END OF VOFTOOLS_SICOSA -----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_HCUBE                            | 
!---------------------------------------------------------------------| 
! Non-convex hollowed cube                                            | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_HCUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)     &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IS,IV,IV2 
    REAL(W_P) :: D0,D1,D14 
    
    ! Unit-length cube with a half-length cubic hollow in its center:       
    D0=0.0_W_P 
    D1=1.0_W_P 
    D14=0.25_W_P 
    
    XNS(1)=D1 
    YNS(1)=D0 
    ZNS(1)=D0 
    XNS(2)=D0 
    YNS(2)=-D1 
    ZNS(2)=D0 
    XNS(3)=D0 
    YNS(3)=D0 
    ZNS(3)=-D1 
    XNS(4)=D0 
    YNS(4)=D1 
    ZNS(4)=D0 
    XNS(5)=D0 
    YNS(5)=D0 
    ZNS(5)=D1 
    XNS(6)=-D1 
    YNS(6)=D0 
    ZNS(6)=D0 
    NTS=12 
    NTV=16 
    NTP=NTV 
    NIPV(1)=4 
    IPV(1,1)=1 
    IPV(1,2)=2 
    IPV(1,3)=3 
    IPV(1,4)=4 
    NIPV(2)=4 
    IPV(2,1)=2 
    IPV(2,2)=1 
    IPV(2,3)=5 
    IPV(2,4)=6 
    NIPV(3)=4 
    IPV(3,1)=3 
    IPV(3,2)=2 
    IPV(3,3)=6 
    IPV(3,4)=7 
    NIPV(4)=4 
    IPV(4,1)=4 
    IPV(4,2)=3 
    IPV(4,3)=7 
    IPV(4,4)=8 
    NIPV(5)=4 
    IPV(5,1)=1 
    IPV(5,2)=4 
    IPV(5,3)=8 
    IPV(5,4)=5 
    NIPV(6)=4 
    IPV(6,1)=6 
    IPV(6,2)=5 
    IPV(6,3)=8 
    IPV(6,4)=7 
    DO IS=1,6 
       XNS(IS+6)=-XNS(IS) 
       YNS(IS+6)=-YNS(IS) 
       ZNS(IS+6)=-ZNS(IS) 
       NIPV(IS+6)=NIPV(IS) 
       DO IV=1,4 
          IV2=4-IV+1 
          IPV(IS+6,IV)=IPV(IS,IV2)+8 
       END DO
    END DO
    !       7/----------/3                                                  
    !       /|         /|                                                   
    !      / |        / |                                                   
    !    8/__|______4/  |                                                   
    !     |  |       |  |                                                   
    !     |  /6------|--/2                                                  
    !     | /        | /                                                    
    !     |/_________|/                                                     
    !     5           1                                                     
    VERTP(1,1)=D1 
    VERTP(1,2)=D0 
    VERTP(1,3)=D1 
    VERTP(2,1)=D1 
    VERTP(2,2)=D0 
    VERTP(2,3)=D0 
    VERTP(3,1)=D1 
    VERTP(3,2)=D1 
    VERTP(3,3)=D0 
    VERTP(4,1)=D1 
    VERTP(4,2)=D1 
    VERTP(4,3)=D1 
    VERTP(5,1)=D0 
    VERTP(5,2)=D0 
    VERTP(5,3)=D1 
    VERTP(6,1)=D0 
    VERTP(6,2)=D0 
    VERTP(6,3)=D0 
    VERTP(7,1)=D0 
    VERTP(7,2)=D1 
    VERTP(7,3)=D0 
    VERTP(8,1)=D0 
    VERTP(8,2)=D1 
    VERTP(8,3)=D1 
    
    VERTP(9,1)=D1-D14 
    VERTP(9,2)=D0+D14 
    VERTP(9,3)=D1-D14 
    VERTP(10,1)=D1-D14 
    VERTP(10,2)=D0+D14 
    VERTP(10,3)=D0+D14 
    VERTP(11,1)=D1-D14 
    VERTP(11,2)=D1-D14 
    VERTP(11,3)=D0+D14 
    VERTP(12,1)=D1-D14 
    VERTP(12,2)=D1-D14 
    VERTP(12,3)=D1-D14 
    VERTP(13,1)=D0+D14 
    VERTP(13,2)=D0+D14 
    VERTP(13,3)=D1-D14 
    VERTP(14,1)=D0+D14 
    VERTP(14,2)=D0+D14 
    VERTP(14,3)=D0+D14 
    VERTP(15,1)=D0+D14 
    VERTP(15,2)=D1-D14 
    VERTP(15,3)=D0+D14 
    VERTP(16,1)=D0+D14 
    VERTP(16,2)=D1-D14 
    VERTP(16,3)=D1-D14 
    RETURN 
  END SUBROUTINE VOFTOOLS_HCUBE
!---------------------- END OF VOFTOOLS_HCUBE ------------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_DRCUBE                           | 
!---------------------------------------------------------------------| 
! Drilled cube (example of non-simply connected polyhedron)           | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_DRCUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,        &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    REAL(W_P) :: D0,D02,D1,D12
    
    CALL VOFTOOLS_CUBE(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)         
    D0=0.0_W_P 
    D1=1.0_W_P
    
    XNS(NTS+1)=-D1 
    YNS(NTS+1)=-D0 
    ZNS(NTS+1)=-D0 
    XNS(NTS+2)=-D0 
    YNS(NTS+2)=D1 
    ZNS(NTS+2)=-D0 
    XNS(NTS+3)=-D0 
    YNS(NTS+3)=-D0 
    ZNS(NTS+3)=D1 
    XNS(NTS+4)=-D0 
    YNS(NTS+4)=-D1 
    ZNS(NTS+4)=-D0 
    XNS(NTS+5)=-D0 
    YNS(NTS+5)=-D0 
    ZNS(NTS+5)=-D1 
    XNS(NTS+6)=D1 
    YNS(NTS+6)=-D0 
    ZNS(NTS+6)=-D0 
    
    NIPV(NTS+1)=4 
    IPV(NTS+1,4)=NTP+1 
    IPV(NTS+1,3)=NTP+2 
    IPV(NTS+1,2)=NTP+3 
    IPV(NTS+1,1)=NTP+4 
    NIPV(NTS+2)=4 
    IPV(NTS+2,4)=NTP+2 
    IPV(NTS+2,3)=NTP+1 
    IPV(NTS+2,2)=NTP+5 
    IPV(NTS+2,1)=NTP+6 
    NIPV(NTS+3)=4 
    IPV(NTS+3,4)=NTP+3 
    IPV(NTS+3,3)=NTP+2 
    IPV(NTS+3,2)=NTP+6 
    IPV(NTS+3,1)=NTP+7 
    NIPV(NTS+4)=4 
    IPV(NTS+4,4)=NTP+4 
    IPV(NTS+4,3)=NTP+3 
    IPV(NTS+4,2)=NTP+7 
    IPV(NTS+4,1)=NTP+8 
    NIPV(NTS+5)=4 
    IPV(NTS+5,4)=NTP+1 
    IPV(NTS+5,3)=NTP+4 
    IPV(NTS+5,2)=NTP+8 
    IPV(NTS+5,1)=NTP+5 
    NIPV(NTS+6)=4 
    IPV(NTS+6,4)=NTP+6 
    IPV(NTS+6,3)=NTP+5 
    IPV(NTS+6,2)=NTP+8 
    IPV(NTS+6,1)=NTP+7 
    
    D02=0.25_W_P 
    D12=0.75_W_P 
    
    VERTP(NTP+1,1)=D12 
    VERTP(NTP+1,2)=D0 
    VERTP(NTP+1,3)=D12 
    VERTP(NTP+2,1)=D12 
    VERTP(NTP+2,2)=D0 
    VERTP(NTP+2,3)=D02 
    VERTP(NTP+3,1)=D12 
    VERTP(NTP+3,2)=D1 
    VERTP(NTP+3,3)=D02 
    VERTP(NTP+4,1)=D12 
    VERTP(NTP+4,2)=D1 
    VERTP(NTP+4,3)=D12 
    VERTP(NTP+5,1)=D02 
    VERTP(NTP+5,2)=D0 
    VERTP(NTP+5,3)=D12 
    VERTP(NTP+6,1)=D02 
    VERTP(NTP+6,2)=D0 
    VERTP(NTP+6,3)=D02 
    VERTP(NTP+7,1)=D02 
    VERTP(NTP+7,2)=D1 
    VERTP(NTP+7,3)=D02 
    VERTP(NTP+8,1)=D02 
    VERTP(NTP+8,2)=D1 
    VERTP(NTP+8,3)=D12 
    
    NTS=NTS+6 
    NTV=NTV+8 
    NTP=NTV 
    
    RETURN 
  END SUBROUTINE VOFTOOLS_DRCUBE
!---------------------- END OF VOFTOOLS_DRCUBE -----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_ZIGZAG                           | 
!---------------------------------------------------------------------| 
! Zig-zag polyhedron                                                  | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_ZIGZAG(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,        &
       ZNS) BIND(C)                                                 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: IP1,IP2,IP3,IS,IV,NZIGS 
    REAL(W_P) :: D0,D1,DMOD,DOFF,XN,XV1,XV2,YN,YV1,YV2,ZN,ZV1,ZV2 
    
    !. Change NZIGS to modify the number of zig-zag sections                
    NZIGS=5 
    DOFF=0.1_W_P 
    D0=0.0_W_P 
    D1=1.0_W_P 
    NTP=4*NZIGS 
    NTV=NTP 
    NTS=2*NZIGS+2 
    DO IV=1,NZIGS 
       VERTP(IV,1)=D1*(IV-1) 
       VERTP(IV,2)=DOFF+D1*MOD(IV-1,2) 
       VERTP(IV,3)=D0 
       VERTP(IV+NZIGS,1)=D1*(NZIGS-(IV-1)-1) 
       VERTP(IV+NZIGS,2)=D1*MOD(NZIGS-(IV-1)-1,2) 
       VERTP(IV+NZIGS,3)=D0 
       VERTP(IV+2*NZIGS,1)=D1*(IV-1) 
       VERTP(IV+2*NZIGS,2)=DOFF+D1*MOD(IV-1,2) 
       VERTP(IV+2*NZIGS,3)=D1 
       VERTP(IV+3*NZIGS,1)=D1*(NZIGS-(IV-1)-1) 
       VERTP(IV+3*NZIGS,2)=D1*MOD(NZIGS-(IV-1)-1,2) 
       VERTP(IV+3*NZIGS,3)=D1 
    END DO
    NIPV(1)=2*NZIGS 
    NIPV(2)=2*NZIGS 
    DO IV=1,2*NZIGS 
       IPV(1,IV)=IV 
       IPV(2,IV)=4*NZIGS-(IV-1) 
    END DO
    IV=1 
    NIPV(3)=4 
    IPV(3,1)=IV 
    IPV(3,2)=2*NZIGS-(IV-1) 
    IPV(3,3)=4*NZIGS-(IV-1) 
    IPV(3,4)=IV+2*NZIGS 
    IV=NZIGS 
    NIPV(4)=4 
    IPV(4,4)=IV 
    IPV(4,3)=2*NZIGS-(IV-1) 
    IPV(4,2)=4*NZIGS-(IV-1) 
    IPV(4,1)=IV+2*NZIGS 
    DO IV=1,NZIGS-1 
       NIPV(IV+4)=4 
       IPV(IV+4,1)=IV 
       IPV(IV+4,2)=IV+2*NZIGS 
       IPV(IV+4,3)=IV+2*NZIGS+1 
       IPV(IV+4,4)=IV+1 
       NIPV(IV+4+(NZIGS-1))=4 
       IPV(IV+4+(NZIGS-1),1)=2*NZIGS-(IV-1) 
       IPV(IV+4+(NZIGS-1),2)=2*NZIGS-(IV-1)-1 
       IPV(IV+4+(NZIGS-1),3)=2*NZIGS-(IV-1)-1+2*NZIGS 
       IPV(IV+4+(NZIGS-1),4)=2*NZIGS-(IV-1)+2*NZIGS 
    END DO
    DO IS=1,NTS
       IF(IS.EQ.2) THEN
          IP1=IPV(IS,4) 
          IP2=IPV(IS,5) 
          IP3=IPV(IS,6)
       ELSE
          IP1=IPV(IS,1) 
          IP2=IPV(IS,2) 
          IP3=IPV(IS,3)
       END IF
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    RETURN 
  END SUBROUTINE VOFTOOLS_ZIGZAG
!--------------------- END OF VOFTOOLS_ZIGZAG ------------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_LOGO                             | 
!---------------------------------------------------------------------| 
! VOFTools logo                                                       | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NIPV     = number of vertices of each face                          | 
! NTP      = last global vertex index                                 | 
! NTS      = total number of faces                                    | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
! XNS,  ...= components of the unit-lenght vector normal to each      | 
!            face of the polyhedron                                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_LOGO(IPV,NIPV,NTP,NTS,NTV,VERTP,XNS,YNS,ZNS)      &
       BIND(C)                                                      
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTS,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NS,NV),NIPV(NS) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I,IP1,IP2,IP3,IS,IV,NTPI,NTPL,NTSI 
    REAL(W_P) :: DEPTH,DISP,DMOD,FACTOR,XN,XV1,XV2,YN,YV1,YV2,ZN,       &
         ZV1,ZV2                                                          
    
    NTS=0 
    NTP=0 
    DEPTH=1.0_W_P 
    !.. V letter:                                                           
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=1.0_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=0.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=2.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=4.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=6.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=5.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=3.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=1.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    
    !..O letter:                                                            
    DISP=6.2_W_P 
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=1.0_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    !..                                                                     
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=1.0_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    !..F letter:                                                            
    DISP=DISP+4.6_W_P 
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=1.0_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=2.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=2.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=3.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=3.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.4*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.4*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    
    !..T letter:                                                            
    DISP=DISP+3.45_W_P 
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=1.0_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+2.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.65*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.65*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.35*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.35*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+2.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    !..o letter:                                                            
    DISP=DISP+4.2_W_P 
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=0.7_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    !..                                                                     
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=0.7_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    
    !..o letter:                                                            
    DISP=DISP+3.3_W_P 
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=0.7_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    !..                                                                     
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=0.7_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    !..l letter:                                                            
    DISP=DISP+2.7_W_P 
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=1.0_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+2.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+2.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    !..s letter:                                                            
    DISP=DISP+2.5_W_P 
    NTSI=NTS+1 
    NTPI=NTP+1 
    FACTOR=0.7_W_P 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=0.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=3.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=3.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+1.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=4.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+4.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=5.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=2.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=2.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+3.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTP=NTP+1 
    VERTP(NTP,1)=DISP+0.0_W_P*FACTOR 
    VERTP(NTP,2)=1.0_W_P*FACTOR 
    VERTP(NTP,3)=DEPTH 
    NTS=NTS+1 
    NIPV(NTS)=NTP-NTPI+1 
    NTPL=NTP-NTPI+1 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+IV-1 
    END DO
    DO I=1,NTPL 
       NTP=NTP+1 
       VERTP(NTP,1)=VERTP(NTPI+I-1,1) 
       VERTP(NTP,2)=VERTP(NTPI+I-1,2) 
       VERTP(NTP,3)=0.0_W_P 
    END DO
    DO IS=2,NTPL+1 
       NTS=NTS+1 
       NIPV(NTS)=4 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,1)=(NTPI-1)+1 
       ELSE 
          IPV(NTS,1)=(NTPI-1)+IS 
       ENDIF
       IPV(NTS,2)=(NTPI-1)+IS-1 
       IPV(NTS,3)=(NTPI-1)+IS+NTPL-1 
       IF(IS.EQ.(NTPL+1)) THEN 
          IPV(NTS,4)=(NTPI-1)+1+NTPL 
       ELSE 
          IPV(NTS,4)=(NTPI-1)+IS+NTPL 
       END IF
    END DO
    NTS=NTS+1 
    NIPV(NTS)=NIPV(NTSI) 
    DO IV=1,NIPV(NTS) 
       IPV(NTS,IV)=NTPI+NTPL*2-IV 
    END DO
    !............                                                           
    NTV=NTP 
    DO IS=1,NTS 
       IP1=IPV(IS,1) 
       IP2=IPV(IS,2) 
       IP3=IPV(IS,3) 
       XV1=VERTP(IP2,1)-VERTP(IP1,1) 
       YV1=VERTP(IP2,2)-VERTP(IP1,2) 
       ZV1=VERTP(IP2,3)-VERTP(IP1,3) 
       XV2=VERTP(IP3,1)-VERTP(IP2,1) 
       YV2=VERTP(IP3,2)-VERTP(IP2,2) 
       ZV2=VERTP(IP3,3)-VERTP(IP2,3) 
       XN=YV1*ZV2-ZV1*YV2 
       YN=ZV1*XV2-XV1*ZV2 
       ZN=XV1*YV2-YV1*XV2 
       DMOD=(XN**2+YN**2+ZN**2)**0.5_W_P 
       XNS(IS)=XN/DMOD 
       YNS(IS)=YN/DMOD 
       ZNS(IS)=ZN/DMOD 
    END DO
    RETURN 
  END SUBROUTINE VOFTOOLS_LOGO
!---------------------- END OF VOFTOOLS_LOGO -------------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_SQUARE                            | 
!---------------------------------------------------------------------| 
! Unit square                                                         | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_SQUARE(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=4 
    NTP=4 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=1.0_W_P 
    VERTP(2,2)=0.0_W_P 
    VERTP(3,1)=1.0_W_P 
    VERTP(3,2)=1.0_W_P 
    VERTP(4,1)=0.0_W_P 
    VERTP(4,2)=1.0_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_SQUARE
!---------------------- END OF VOFTOOLS_SQUARE -----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_HEXAGON                          | 
!---------------------------------------------------------------------| 
! Regular hexagon                                                     | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_HEXAGON(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=6 
    NTP=6 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.5_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=0.9330127_W_P 
    VERTP(2,2)=0.25_W_P 
    VERTP(3,1)=0.9330127_W_P 
    VERTP(3,2)=0.75_W_P 
    VERTP(4,1)=0.5_W_P 
    VERTP(4,2)=1.0_W_P 
    VERTP(5,1)=0.066987298_W_P 
    VERTP(5,2)=0.75_W_P 
    VERTP(6,1)=0.066987298_W_P 
    VERTP(6,2)=0.25_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_HEXAGON
!---------------------- END OF VOFTOOLS_HEXAGON ----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                             VOFTOOLS_TRI                            | 
!---------------------------------------------------------------------| 
! Triangle                                                            | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_TRI(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=3 
    NTP=3 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=0.72_W_P 
    VERTP(2,2)=0.13_W_P 
    VERTP(3,1)=1.0_W_P 
    VERTP(3,2)=1.0_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_TRI
!------------------------ END OF VOFTOOLS_TRI ------------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            VOFTOOLS_QUAD                            | 
!---------------------------------------------------------------------| 
! Quadrangle                                                          | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_QUAD(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=4 
    NTP=4 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=1.0_W_P 
    VERTP(2,2)=0.13_W_P 
    VERTP(3,1)=0.72_W_P 
    VERTP(3,2)=1.0_W_P 
    VERTP(4,1)=0.13_W_P 
    VERTP(4,2)=0.56_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_QUAD
!----------------------- END OF VOFTOOLS_QUAD ------------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                         VOFTOOLS_PENTAGON                           | 
!---------------------------------------------------------------------| 
! Pentagon                                                            | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_PENTAGON(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=5 
    NTP=5 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.15_W_P 
    VERTP(2,1)=0.09_W_P 
    VERTP(2,2)=0.0_W_P 
    VERTP(3,1)=1.0_W_P 
    VERTP(3,2)=0.13_W_P 
    VERTP(4,1)=0.16_W_P 
    VERTP(4,2)=1.0_W_P 
    VERTP(5,1)=0.04_W_P 
    VERTP(5,2)=0.77_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_PENTAGON
!--------------------- END OF VOFTOOLS_PENTAGON ----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_IHEXAGON                          | 
!---------------------------------------------------------------------| 
! Irregular hexagon                                                   | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_IHEXAGON(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=6 
    NTP=6 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=0.66_W_P 
    VERTP(2,2)=0.03_W_P 
    VERTP(3,1)=1.0_W_P 
    VERTP(3,2)=0.22_W_P 
    VERTP(4,1)=0.9_W_P 
    VERTP(4,2)=0.77_W_P 
    VERTP(5,1)=0.72_W_P 
    VERTP(5,2)=1.0_W_P 
    VERTP(6,1)=0.33_W_P 
    VERTP(6,2)=0.86_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_IHEXAGON
!---------------------- END OF VOFTOOLS_IHEXAGON ---------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                            VOFTOOLS_NCQUAD                          | 
!---------------------------------------------------------------------| 
! Non-convex quadrangle                                               | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_NCQUAD(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=4 
    NTP=4 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=1.0_W_P 
    VERTP(2,2)=0.13_W_P 
    VERTP(3,1)=0.72_W_P 
    VERTP(3,2)=1.0_W_P 
    VERTP(4,1)=0.75_W_P 
    VERTP(4,2)=0.56_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_NCQUAD
!--------------------- END OF VOFTOOLS_NCQUAD ------------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                        VOFTOOLS_NCPENTAGON                          | 
!---------------------------------------------------------------------| 
! Non-convex pentagon                                                 | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_NCPENTAGON(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=5 
    NTP=5 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=0.49_W_P 
    VERTP(2,2)=0.22_W_P 
    VERTP(3,1)=1.0_W_P 
    VERTP(3,2)=0.13_W_P 
    VERTP(4,1)=0.16_W_P 
    VERTP(4,2)=1.0_W_P 
    VERTP(5,1)=0.04_W_P 
    VERTP(5,2)=0.77_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_NCPENTAGON
!-------------------- END OF VOFTOOLS_NCPENTAGON ---------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                         VOFTOOLS_NCHEXAGON                          | 
!---------------------------------------------------------------------| 
! Non-convex hexagon                                                  | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_NCHEXAGON(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=6 
    NTP=6 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=0.33_W_P 
    VERTP(2,2)=0.43_W_P 
    VERTP(3,1)=1.0_W_P 
    VERTP(3,2)=0.22_W_P 
    VERTP(4,1)=0.9_W_P 
    VERTP(4,2)=0.77_W_P 
    VERTP(5,1)=0.72_W_P 
    VERTP(5,2)=1.0_W_P 
    VERTP(6,1)=0.33_W_P 
    VERTP(6,2)=0.86_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_NCHEXAGON
!--------------------- END OF VOFTOOLS_NCHEXAGON ---------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                          VOFTOOLS_SHEXAGON                          | 
!---------------------------------------------------------------------| 
! Stellated hexagon                                                   | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_SHEXAGON(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=12 
    NTP=12 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.2_W_P 
    VERTP(2,1)=0.25_W_P 
    VERTP(2,2)=0.25_W_P 
    VERTP(3,1)=0.4_W_P 
    VERTP(3,2)=0.0_W_P 
    VERTP(4,1)=0.55_W_P 
    VERTP(4,2)=0.3_W_P 
    VERTP(5,1)=0.8_W_P 
    VERTP(5,2)=0.35_W_P 
    VERTP(6,1)=0.65_W_P 
    VERTP(6,2)=0.55_W_P 
    VERTP(7,1)=0.8_W_P 
    VERTP(7,2)=0.75_W_P 
    VERTP(8,1)=0.5_W_P 
    VERTP(8,2)=0.7_W_P 
    VERTP(9,1)=0.35_W_P 
    VERTP(9,2)=0.9_W_P 
    VERTP(10,1)=0.25_W_P 
    VERTP(10,2)=0.7_W_P 
    VERTP(11,1)=-0.1_W_P 
    VERTP(11,2)=0.55_W_P 
    VERTP(12,1)=0.2_W_P 
    VERTP(12,2)=0.45_W_P 
    RETURN 
  END SUBROUTINE VOFTOOLS_SHEXAGON
!--------------------- END OF VOFTOOLS_SHEXAGON ----------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_HSQUARE                          | 
!---------------------------------------------------------------------| 
! Hollowed square                                                     | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_HSQUARE(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=10 
    NTP=10 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=1.0_W_P 
    VERTP(2,2)=0.0_W_P 
    VERTP(3,1)=1.0_W_P 
    VERTP(3,2)=1.0_W_P 
    VERTP(4,1)=0.0_W_P 
    VERTP(4,2)=1.0_W_P 
    VERTP(5,1)=VERTP(1,1) 
    VERTP(5,2)=VERTP(1,2) 
    !.. hollow                                                              
    VERTP(6,1)=0.25_W_P 
    VERTP(6,2)=0.25_W_P 
    VERTP(7,1)=0.25_W_P 
    VERTP(7,2)=0.75_W_P 
    VERTP(8,1)=0.75_W_P 
    VERTP(8,2)=0.75_W_P 
    VERTP(9,1)=0.75_W_P 
    VERTP(9,2)=0.25_W_P 
    VERTP(10,1)=VERTP(6,1) 
    VERTP(10,2)=VERTP(6,2) 
    
    RETURN 
  END SUBROUTINE VOFTOOLS_HSQUARE
!----------------------- END OF VOFTOOLS_HSQUARE ---------------------|  
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           VOFTOOLS_MSQUARE                          | 
!---------------------------------------------------------------------| 
! Non-convex multi-square                                             | 
!---------------------------------------------------------------------| 
! On return:                                                          | 
!===========                                                          | 
! IPV      = array containing the global indices of the polyhedron    | 
!            vertices                                                 | 
! NTP      = last global vertex index                                 | 
! NTV      = total number of vertices                                 | 
! VERTP    = coordinates of the polyhedron vertices                   | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
  SUBROUTINE VOFTOOLS_MSQUARE(IPV,NTP,NTV,VERTP) BIND(C) 
    !.. Scalar Arguments                                                    
    INTEGER(I_P), INTENT(OUT) :: NTP,NTV 
    !.. Array Arguments                                                     
    INTEGER(I_P), INTENT(OUT) :: IPV(NV) 
    REAL(W_P), INTENT(OUT) :: VERTP(NV,2) 
    !.. Local Scalars                                                       
    INTEGER(I_P) :: I 
    
    NTV=15 
    NTP=15 
    DO I=1,NTV 
       IPV(I)=I 
    END DO
    VERTP(1,1)=0.0_W_P 
    VERTP(1,2)=0.0_W_P 
    VERTP(2,1)=1.0_W_P 
    VERTP(2,2)=0.0_W_P 
    VERTP(3,1)=1.0_W_P 
    VERTP(3,2)=1.0_W_P 
    VERTP(4,1)=0.0_W_P 
    VERTP(4,2)=1.0_W_P 
    VERTP(5,1)=VERTP(1,1) 
    VERTP(5,2)=VERTP(1,2) 
    !.. hollow                                                              
    VERTP(6,1)=0.25_W_P 
    VERTP(6,2)=0.25_W_P 
    VERTP(7,1)=0.25_W_P 
    VERTP(7,2)=0.75_W_P 
    VERTP(8,1)=0.75_W_P 
    VERTP(8,2)=0.75_W_P 
    VERTP(9,1)=0.75_W_P 
    VERTP(9,2)=0.25_W_P 
    VERTP(10,1)=VERTP(6,1) 
    VERTP(10,2)=VERTP(6,2) 
    !.. liquid inside hollow                                                
    VERTP(11,1)=0.4_W_P 
    VERTP(11,2)=0.4_W_P 
    VERTP(12,1)=0.6_W_P 
    VERTP(12,2)=0.4_W_P 
    VERTP(13,1)=0.6_W_P 
    VERTP(13,2)=0.6_W_P 
    VERTP(14,1)=0.4_W_P 
    VERTP(14,2)=0.6_W_P 
    VERTP(15,1)=VERTP(11,1) 
    VERTP(15,2)=VERTP(11,2) 
    RETURN 
  END SUBROUTINE VOFTOOLS_MSQUARE
!---------------------- END OF VOFTOOLS_MSQUARE ----------------------|  
!---------------------------------------------------------------------|
!---------------------------------------------------------------------|
!---------------------------------------------------------------------|
!                           VOFTOOLSLOGO                              |
!---------------------------------------------------------------------|
! This routine prints on screen the VOFTools logo                     |
!---------------------------------------------------------------------|
!---------------------------------------------------------------------|
  SUBROUTINE VOFTOOLSLOGO() BIND(C)                
    WRITE(6,*)'-----------------------------------------------------------'
    WRITE(6,*)'-----------------------------------------------------------'
    WRITE(6,*)' _       ___________________________                       ' 
    WRITE(6,*)'| |     / / ____  / ______/___  ___/_______________   _____'
    WRITE(6,*)'| |    / / /   / / /         / /  / ___  / ___  / /  / ___/'
    WRITE(6,*)'| |   / / /   / / /___      / /  / /  / / /  / / /  / /__  '
    WRITE(6,*)'| |  / / /   / / ____/     / /  / /  / / /  / / /  /__  /  '
    WRITE(6,*)'| |_/ / /___/ / /         / /  / /__/ / /__/ / /_____/ /   '
    WRITE(6,*)'|____/_______/_/         /_/  /______/______/____/____/    '
    WRITE(6,*)'                                                           '
    WRITE(6,*)'                Copyright (C) 2025 J. Lopez                '
    WRITE(6,*)'-----------------------------------------------------------'
    WRITE(6,*)'-----------------------------------------------------------' 
    RETURN
  END SUBROUTINE VOFTOOLSLOGO
!------------------------ END OF VOFTOOLSLOGO ------------------------|
!---------------------------------------------------------------------|      
!*********************************************************************
!*********************************************************************
!RUTINAS QUE DEBEN SER ELIMINADAS DE LA VERSION DEFINITIVAL
!*********************************************************************
!*********************************************************************
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                               ENFORVP                               c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! CPARAB   = local paraboloid coefficients                            c
! IPV      = array containing the global indices of the polyhedron    c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! V        = liquid volume                                            c 
! VT       = total volume of the polyhedron                           c 
! VERTP    = vertex coordinates of the polyhedron                     c 
! XNS, ... = unit-lenght normals to the faces of the polyhedron       c 
! On return:                                                          c 
!===========                                                          c 
! C        = solution of the problem                                  c 
! IE       = 0, if the root is found; 1, otherwise                    c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE ENFORVP(C,CPARAB,IE,IPV,NC,NE,NIPV,NTP,NTS,V,VT,VERTP, &
           XNS,YNS,ZNS) BIND(C)                                 
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(OUT) :: C 
      REAL(W_P), INTENT(IN) :: V, VT 
      INTEGER(I_P), INTENT(OUT) :: IE 
      INTEGER(I_P), INTENT(IN) :: NC,NE,NTP,NTS
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: CPARAB(12),VERTP(NV,3),XNS(NS),YNS(NS),  &
           ZNS(NS) 
      INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS)
!.. Local Scalars
      INTEGER(I_P) :: I,II,IP,ITER,NITER,NTV
      REAL(W_P) :: C0,C1,CI,CIQ,DMOD,D,D0,D1,DD,DVF,FL,P,Q,R,S,T,TOLF,  &
           UL,VL,VF,VF0,VF1,VFI,VFIQ,VFREF,X,XMAX,XMIN,Y,YMAX,YMIN,Z,   &
           ZMAX,ZMIN
!.. Local Arrays      
      INTEGER(I_P) :: LISTV(NV) !list of ordered vertices
      REAL(W_P) :: CPARABL(12),PHI(NV),VN(9)
      IE=0
      NITER=100 ! Maximum number of Brent's iterations
      NTV=NTP !it's suppossed that the polyhedron hasn't been truncated
      TOLF=1.0E-14_W_P ! volume of fluid fraction tolerance
      VFREF=V/VT
      ! Initial guess
      CALL INTPV3D(CPARAB,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VF,XNS,YNS,  &
           ZNS)
      C0=CPARAB(1)
      VF0=VF/VT
      IF(ABS(VF0-VFREF).LT.TOLF) THEN
         C=C0
         RETURN
      END IF
      !Paraboloid orthonormal basis
      VN(1)=CPARAB(7) ! x-component of the shift vector
      VN(2)=CPARAB(8) ! y-component of the shift vector
      VN(3)=CPARAB(9) ! z-component of the shift vector
      VN(4)=VN(2)
      VN(5)=-VN(1)
      VN(6)=0.0_W_P
      DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
      IF(DMOD.NE.0.0_W_P) THEN
         VN(4)=VN(4)/DMOD
         VN(5)=VN(5)/DMOD
      ELSE
         VN(4)=VN(3)
         VN(5)=0.0_W_P
         VN(6)=-VN(1)
         DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
         VN(4)=VN(4)/DMOD
         VN(6)=VN(6)/DMOD
      END IF
      VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
      VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
      VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
      LISTV(1)=1
      XMAX=0.0_W_P
      XMIN=1.0E+20_W_P
      YMAX=0.0_W_P
      YMIN=1.0E+20_W_P
      ZMAX=0.0_W_P
      ZMIN=1.0E+20_W_P
      DO IP=1,NTP
         X=VERTP(IP,1)
         Y=VERTP(IP,2)
         Z=VERTP(IP,3)
         XMAX=MAX(XMAX,X)
         XMIN=MIN(XMIN,X)
         YMAX=MAX(YMAX,Y)
         YMIN=MIN(YMIN,Y)
         ZMAX=MAX(ZMAX,Z)
         ZMIN=MIN(ZMIN,Z)
         CALL PFUNC3D(PHI(IP),CPARAB,VN,X,Y,Z)
         !* Ordered list of global vertex indices                                
         DO I=1,IP-1 
            IF(PHI(IP).GT.PHI(LISTV(I))) THEN 
               DO II=IP,I+1,-1 
                  LISTV(II)=LISTV(II-1) 
               END DO 
               LISTV(I)=IP 
               GOTO 10 
            END IF 
         END DO 
         LISTV(IP)=IP
   10    CONTINUE 
      END DO
      ! Solution bracketting.
      ! LISTV(1) --> gives the vertex IP through which the shifted
      !              paraboloid passes and truncates zero fluid volume
      ! LISTV(NTP)-> gives the vertex IP through which the shifted
      !              paraboloid passes and truncates the complete polyhedron
      CPARABL(2:12)=CPARAB(2:12)
      IF(VF0.GT.VFREF) THEN 
         DO I=NTP,1,-1
            IP=LISTV(I)
            IF(PHI(IP).GT.0.0_W_P) THEN
               X=VERTP(IP,1)-CPARAB(10)
               Y=VERTP(IP,2)-CPARAB(11)
               Z=VERTP(IP,3)-CPARAB(12)
               FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
               UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
               VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
               CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)* &
                    UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
               CALL INTPV3D(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,   &
                    VF1,XNS,YNS,ZNS)
               VF1=VF1/VT
               IF(VF1.LE.VFREF) THEN ! solution bracketted
                  C1=CPARABL(1)
                  GOTO 20
               END IF
            END IF
         END DO
      ELSE
         DO I=1,NTP
            IP=LISTV(I)
            IF(PHI(IP).LT.0.0_W_P) THEN
               X=VERTP(IP,1)-CPARAB(10)
               Y=VERTP(IP,2)-CPARAB(11)
               Z=VERTP(IP,3)-CPARAB(12)
               FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
               UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
               VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
               CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)* &
                    UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
               CALL INTPV3D(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,   &
                    VF1,XNS,YNS,ZNS)
               VF1=VF1/VT
               IF(VF1.GE.VFREF) THEN ! solution bracketted
                  C1=CPARABL(1)
                  GOTO 20
               END IF
            END IF
         END DO
      END IF
      DD=MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN)
      IF(VF0.GT.VFREF) THEN
         CPARABL(1)=CPARAB(1)+DD
      ELSE
         CPARABL(1)=CPARAB(1)-DD
      END IF
      CALL INTPV3D(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VF1,XNS,YNS,&
           ZNS)
      VF1=VF1/VT
      IF((VF0-VFREF)*(VF1-VFREF).LT.0.0_W_P) THEN
         C1=CPARABL(1)
         GOTO 20
      END IF
      IE=1 ! the solution can not be bracketted
      RETURN
20    CONTINUE
      IF(ABS(VF1-VFREF).LT.TOLF) THEN
         C=C1
         RETURN
      END IF
      ! Init Brent's iteration
      DO ITER=1,NITER
         ! Secant interpolation
         DVF=-(VF0-VFREF)/(VF1-VF0)
         CI=C0*(1.0_W_P-DVF)+C1*DVF
         CPARABL(1)=CI
         CALL INTPV3D(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VFI,XNS, &
              YNS,ZNS)
         VFI=VFI/VT
         IF(ABS(VFI-VFREF).LT.TOLF) THEN
            C=CI
            RETURN
         END IF
         IF((VFI-VFREF)/(VF0-VFREF).GT.1.0_W_P.OR.(VFI-VFREF)/(VF0-     &
              VFREF).GT.1.0_W_P) THEN
            ! Bisection
            CI=(C0+C1)/2.0_W_P
            CPARABL(1)=CI
            CALL INTPV3D(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VFI,  &
                 XNS,YNS,ZNS)
            VFI=VFI/VT
            IF(ABS(VFI-VFREF).LT.TOLF) THEN
               C=CI
               RETURN
            END IF            
         END IF
         ! Inverse-quadratic interpolation
         R=(VFI-VFREF)/(VF1-VFREF)
         S=(VFI-VFREF)/(VF0-VFREF)
         T=(VF0-VFREF)/(VF1-VFREF)
         Q=(T-1.0_W_P)*(R-1.0_W_P)*(S-1.0_W_P)
         IF(Q.EQ.0.0_W_P) THEN
!            C=CI
!            RETURN !*******
!         END IF
            !. Bisection
            CI=(C0+C1)/2.0_W_P
            CPARABL(1)=CI
            CALL INTPV3D(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VFI,  &
                 XNS,YNS,ZNS)
            VFI=VFI/VT
         ELSE
            P=S*(T*(R-T)*(C1-CI)-(1.0_W_P-R)*(CI-C0))
            CIQ=CI+P/Q
            CPARABL(1)=CIQ
            CALL INTPV3D(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VFIQ, &
                 XNS,YNS,ZNS)
            VFIQ=VFIQ/VT
         ! Check bracket
            D0=ABS(C0-CIQ)
            D1=ABS(C1-CIQ)
            D=ABS(C0-C1)
            IF(MAX(D0,D1).LT.(D*(1.0_W_P-1.0E-1_W_P))) THEN
               CI=CIQ
               VFI=VFIQ
            ELSE
               !. Bisection
               CI=(C0+C1)/2.0_W_P
               CPARABL(1)=CI
               CALL INTPV3D(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,   &
                    VFI,XNS,YNS,ZNS)
               VFI=VFI/VT
            END IF
         END IF
         IF(ABS(VFI-VFREF).LT.TOLF) THEN
            C=CI
            RETURN
         END IF
         IF((VFI-VFREF)*(VF1-VFREF).GT.0.0) THEN
            C1=CI
            VF1=VFI
         ELSE
            C0=CI
            VF0=VFI
         END IF
      END DO
!      IE=1 ! the solution is not found
      IF(ABS(VF0-VFREF).LT.ABS(VF1-VFREF)) THEN
         C=C0
      ELSE
         C=C1
      END IF
      RETURN
    END SUBROUTINE ENFORVP
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c       
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              ENFORVPA_bak                               c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! CPARAB   = local paraboloid coefficients                            c
! IPV      = array containing the global indices of the polyhedron    c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! V        = liquid volume                                            c 
! VT       = total volume of the polyhedron                           c 
! VERTP    = vertex coordinates of the polyhedron                     c 
! XNS, ... = unit-lenght normals to the faces of the polyhedron       c 
! On return:                                                          c 
!===========                                                          c 
! C        = solution of the problem                                  c 
! IE       = 0, if the root is found; 1, otherwise                    c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE ENFORVPA_bak(C,CPARAB,IE,IPV,NC,NE,NIPV,NTP,NTS,V,VT,VERTP,&
           XNS,YNS,ZNS) BIND(C)                                 
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(OUT) :: C 
      REAL(W_P), INTENT(IN) :: V, VT 
      INTEGER(I_P), INTENT(OUT) :: IE 
      INTEGER(I_P), INTENT(IN) :: NC,NE,NTP,NTS
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: CPARAB(12),VERTP(NV,3),XNS(NS),YNS(NS),  &
           ZNS(NS) 
      INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS)
!.. Local Scalars
      INTEGER(I_P) :: I,II,IP,ITER,NITER,NTV
      REAL(W_P) :: C0,C1,CI,CIQ,DMOD,D,D0,D1,DD,DVF,FL,P,Q,R,S,T,TOLF,  &
           UL,VL,VF,VF0,VF1,VFI,VFIQ,VFREF,X,XMAX,XMIN,Y,YMAX,YMIN,Z,   &
           ZMAX,ZMIN
!.. Local Arrays      
      INTEGER(I_P) :: LISTV(NV) !list of ordered vertices
      REAL(W_P) :: CPARABL(12),PHI(NV),VN(9)
      IE=0
      NITER=100 ! Maximum number of Brent's iterations
      NTV=NTP !it's suppossed that the polyhedron hasn't been truncated
      TOLF=1.0E-14_W_P ! volume of fluid fraction tolerance
      VFREF=V/VT
      ! Initial guess
      CALL INTPV3DPA_bak(CPARAB,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VF,XNS,YNS,&
           ZNS)
      C0=CPARAB(1)
      VF0=VF/VT
      IF(ABS(VF0-VFREF).LT.TOLF) THEN
         C=C0
         RETURN
      END IF
      !Paraboloid orthonormal basis
      VN(1)=CPARAB(7) ! x-component of the shift vector
      VN(2)=CPARAB(8) ! y-component of the shift vector
      VN(3)=CPARAB(9) ! z-component of the shift vector
      VN(4)=VN(2)
      VN(5)=-VN(1)
      VN(6)=0.0_W_P
      DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
      IF(DMOD.NE.0.0_W_P) THEN
         VN(4)=VN(4)/DMOD
         VN(5)=VN(5)/DMOD
      ELSE
         VN(4)=VN(3)
         VN(5)=0.0_W_P
         VN(6)=-VN(1)
         DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
         VN(4)=VN(4)/DMOD
         VN(6)=VN(6)/DMOD
      END IF
      VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
      VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
      VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
      LISTV(1)=1
      XMAX=0.0_W_P
      XMIN=1.0E+20_W_P
      YMAX=0.0_W_P
      YMIN=1.0E+20_W_P
      ZMAX=0.0_W_P
      ZMIN=1.0E+20_W_P
      DO IP=1,NTP
         X=VERTP(IP,1)
         Y=VERTP(IP,2)
         Z=VERTP(IP,3)
         XMAX=MAX(XMAX,X)
         XMIN=MIN(XMIN,X)
         YMAX=MAX(YMAX,Y)
         YMIN=MIN(YMIN,Y)
         ZMAX=MAX(ZMAX,Z)
         ZMIN=MIN(ZMIN,Z)
         CALL PFUNC3D(PHI(IP),CPARAB,VN,X,Y,Z)
         !* Ordered list of global vertex indices                                
         DO I=1,IP-1 
            IF(PHI(IP).GT.PHI(LISTV(I))) THEN 
               DO II=IP,I+1,-1 
                  LISTV(II)=LISTV(II-1) 
               END DO 
               LISTV(I)=IP 
               GOTO 10 
            END IF 
         END DO 
         LISTV(IP)=IP
   10    CONTINUE 
      END DO
      ! Solution bracketting.
      ! LISTV(1) --> gives the vertex IP through which the shifted
      !              paraboloid passes and truncates zero fluid volume
      ! LISTV(NTP)-> gives the vertex IP through which the shifted
      !              paraboloid passes and truncates the complete polyhedron
      CPARABL(2:12)=CPARAB(2:12)
      IF(VF0.GT.VFREF) THEN 
         DO I=NTP,1,-1
            IP=LISTV(I)
            IF(PHI(IP).GT.0.0_W_P) THEN
               X=VERTP(IP,1)-CPARAB(10)
               Y=VERTP(IP,2)-CPARAB(11)
               Z=VERTP(IP,3)-CPARAB(12)
               FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
               UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
               VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
               CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)* &
                    UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
               CALL INTPV3DPA_bak(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP, &
                    VF1,XNS,YNS,ZNS)
               VF1=VF1/VT
               IF(VF1.LE.VFREF) THEN ! solution bracketted
                  C1=CPARABL(1)
                  GOTO 20
               END IF
            END IF
         END DO
      ELSE
         DO I=1,NTP
            IP=LISTV(I)
            IF(PHI(IP).LT.0.0_W_P) THEN
               X=VERTP(IP,1)-CPARAB(10)
               Y=VERTP(IP,2)-CPARAB(11)
               Z=VERTP(IP,3)-CPARAB(12)
               FL=X*VN(1)+Y*VN(2)+Z*VN(3) 
               UL=X*VN(4)+Y*VN(5)+Z*VN(6) 
               VL=X*VN(7)+Y*VN(8)+Z*VN(9) 
               CPARABL(1)=PHI(IP)-(CPARAB(2)*UL+CPARAB(3)*VL+CPARAB(4)* &
                    UL**2+CPARAB(5)*UL*VL+CPARAB(6)*VL**2-FL)
               CALL INTPV3DPA_bak(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP, &
                    VF1,XNS,YNS,ZNS)
               VF1=VF1/VT
               IF(VF1.GE.VFREF) THEN ! solution bracketted
                  C1=CPARABL(1)
                  GOTO 20
               END IF
            END IF
         END DO
      END IF
      DD=MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN)
      IF(VF0.GT.VFREF) THEN
         CPARABL(1)=CPARAB(1)+DD
      ELSE
         CPARABL(1)=CPARAB(1)-DD
      END IF
      CALL INTPV3DPA_bak(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VF1,XNS,  &
           YNS,ZNS)
      VF1=VF1/VT
      IF((VF0-VFREF)*(VF1-VFREF).LT.0.0_W_P) THEN
         C1=CPARABL(1)
         GOTO 20
      END IF
      IE=1 ! the solution can not be bracketted
      RETURN
20    CONTINUE
      IF(ABS(VF1-VFREF).LT.TOLF) THEN
         C=C1
         RETURN
      END IF
      ! Init Brent's iteration
      DO ITER=1,NITER
         ! Secant interpolation
         DVF=-(VF0-VFREF)/(VF1-VF0)
         CI=C0*(1.0_W_P-DVF)+C1*DVF
         CPARABL(1)=CI
         CALL INTPV3DPA_bak(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VFI,   &
              XNS,YNS,ZNS)
         VFI=VFI/VT
         IF(ABS(VFI-VFREF).LT.TOLF) THEN
            C=CI
            RETURN
         END IF
         IF((VFI-VFREF)/(VF0-VFREF).GT.1.0_W_P.OR.(VFI-VFREF)/(VF0-     &
              VFREF).GT.1.0_W_P) THEN
            ! Bisection
            CI=(C0+C1)/2.0_W_P
            CPARABL(1)=CI
            CALL INTPV3DPA_bak(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VFI,&
                 XNS,YNS,ZNS)
            VFI=VFI/VT
            IF(ABS(VFI-VFREF).LT.TOLF) THEN
               C=CI
               RETURN
            END IF            
         END IF
         ! Inverse-quadratic interpolation
         R=(VFI-VFREF)/(VF1-VFREF)
         S=(VFI-VFREF)/(VF0-VFREF)
         T=(VF0-VFREF)/(VF1-VFREF)
         Q=(T-1.0_W_P)*(R-1.0_W_P)*(S-1.0_W_P)
         IF(Q.EQ.0.0_W_P) THEN
!            C=CI
!            RETURN !*******
!         END IF
            !. Bisection
            CI=(C0+C1)/2.0_W_P
            CPARABL(1)=CI
            CALL INTPV3DPA_bak(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VFI,&
                 XNS,YNS,ZNS)
            VFI=VFI/VT
         ELSE
            P=S*(T*(R-T)*(C1-CI)-(1.0_W_P-R)*(CI-C0))
            CIQ=CI+P/Q
            CPARABL(1)=CIQ
            CALL INTPV3DPA_bak(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,    &
                 VFIQ,XNS,YNS,ZNS)
            VFIQ=VFIQ/VT
         ! Check bracket
            D0=ABS(C0-CIQ)
            D1=ABS(C1-CIQ)
            D=ABS(C0-C1)
            IF(MAX(D0,D1).LT.(D*(1.0_W_P-1.0E-1_W_P))) THEN
               CI=CIQ
               VFI=VFIQ
            ELSE
               !. Bisection
               CI=(C0+C1)/2.0_W_P
               CPARABL(1)=CI
               CALL INTPV3DPA_bak(CPARABL,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP, &
                    VFI,XNS,YNS,ZNS)
               VFI=VFI/VT
            END IF
         END IF
         IF(ABS(VFI-VFREF).LT.TOLF) THEN
            C=CI
            RETURN
         END IF
         IF((VFI-VFREF)*(VF1-VFREF).GT.0.0) THEN
            C1=CI
            VF1=VFI
         ELSE
            C0=CI
            VF0=VFI
         END IF
      END DO
!      IE=1 ! the solution is not found
      IF(ABS(VF0-VFREF).LT.ABS(VF1-VFREF)) THEN
         C=C0
      ELSE
         C=C1
      END IF
      RETURN
    END SUBROUTINE ENFORVPA_bak
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c       
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                             XINITFM3D                               c 
! This version uses the array FCOEF containing the coefficients for   c 
! the multi implict functions definition                              c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FCOEF    = array containing the coefficients for the multi implict  c 
!            functions definition                                     c 
! IPV      = array containing the global indices of the original pol. c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! NTV      = total number of vertices                                 c 
! TOL      = prescribed positive tolerance for the distance to the    c 
!            interface                                                c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! VF       = material volume fraction                                 c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE XINITFM3D(FCOEF,IPV,NC,NIPV,NTP,NTS,NTV,TOL,VERTP,VF,  &
     &     XNS,YNS,ZNS) BIND(C)                                         
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(IN) :: TOL 
      REAL(W_P), INTENT(OUT) :: VF 
      INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
      REAL(W_P), INTENT(IN) :: FCOEF(10000) 
! FCOEF(1) = number of implicit functions ('+' sign means union and
!            '-' sign means intersection)                               
! FCOEF(2) = 2, index position of FCOEF where the information if the    
!            implicit function 1 begins                                 
! FCOEF(3) = 0 for global system; 1 for local system                    
! FCOEF(4-6) = xyz-coordinates of the system-reference origin           
! FCOEF(7-15) = xyz-components of the normal vectors that define the    
!               orthonormal reference system                            
! FCOEF(16-19) = C1,C2,C3,C4 coeficients of the first term of the       
!                implicit function 1: C1 X^C2 Y^C3 Z^C4                 
! Follow the same pattern for the rest of information                   
      INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
!.. Local Scalars                                                       
      REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DX,DY,DZ,EPSILON,F0,F1,F2,F3,F4, &
     &     F5,F6,SUMX,SUMY,SUMZ,VOLF,VOLT,VOLTRI,X,XM,XMAX,XMIN,        &
     &     XP,XV1,XV2,Y,YM,YMAX,YMIN,YP,YV1,YV2,Z,ZM,ZMAX,ZMIN,ZP,ZV1,  &
     &     ZV2                                                          
      INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IE,IEBRACKET,IP,IP0,IP1,       &
     &     IS,IS2,ISINI,IV,IV2,JC,KC,NCL,NTP0,NTP1,NTP2,                &
     &     NTPT,NTS0,NTS1,NTS2,NTST,NTSINI,NTV0,NTV1,NTV2,NTVT          
!.. Local Arrays                                                        
      REAL(W_P) :: CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC),      &
     &     CX2(NC),CY1(NC),CY2(NC),CZ1(NC),CZ2(NC),PHIV(NV),V0(3),V1(3),&
     &     V2(3),V3(3),VI(3),VERTP0(NV,3),VERTP1(NV,3),VERTP2(NV,3),    &
     &     VERTPT(NV,3),XNS0(NS),XNS1(NS),XNS2(NS),XNST(NS),YNS0(NS),   &
     &     YNS1(NS),YNS2(NS),YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),       &
     &     ZNST(NS)                                                     
      INTEGER(I_P) :: IA(NV),ICHECK(NV),IPIA0(NV),IPIA1(NV),            &
     &     IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),ISCUT(NS),   &
     &     NIPV0(NS),NIPV1(NS),NIPV2(NS),NIPVT(NS)                      
!.. Coordinate extremes of the cell and vertex tagging                  
      NCL=NC 
      VF=0.0 
      XMIN=1.0D+20 
      XMAX=-1.0D+20 
      YMIN=1.0D+20 
      YMAX=-1.0D+20 
      ZMIN=1.0D+20 
      ZMAX=-1.0D+20 
      ICONTP=0 
      ICONTN=0 
      V0(1)=0.0 
      V0(2)=0.0 
      V0(3)=0.0 
!      PHIMIN=1D+20                                                     
      DO IP=1,NTP 
         ICHECK(IP)=0 
      END DO 
      DO IS=1,NTS 
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(ICHECK(IP).EQ.0) THEN 
               ICHECK(IP)=1 
               XP=VERTP(IP,1) 
               YP=VERTP(IP,2) 
               ZP=VERTP(IP,3) 
               V0(1)=V0(1)+XP 
               V0(2)=V0(2)+YP 
               V0(3)=V0(3)+ZP 
               XMIN=DMIN1(XMIN,XP) 
               XMAX=DMAX1(XMAX,XP) 
               YMIN=DMIN1(YMIN,YP) 
               YMAX=DMAX1(YMAX,YP) 
               ZMIN=DMIN1(ZMIN,ZP) 
               ZMAX=DMAX1(ZMAX,ZP) 
               CALL MFUNC3D(PHIV(IP),FCOEF,XP,YP,ZP) 
               IF(PHIV(IP).GE.0.0) THEN 
                  IA(IP)=1 
                  ICONTP=ICONTP+1 
               ELSE 
                  IA(IP)=0 
                  ICONTN=ICONTN+1 
               END IF 
            END IF 
         END DO 
      END DO 
!.. initialization                                                      
      DX=XMAX-XMIN 
      DY=YMAX-YMIN 
      DZ=ZMAX-ZMIN 
      DD=0.01*MIN(DX,DY,DZ) 
      IF(DD.LT.1.0E-20_W_P) THEN
         VF=0._W_P 
         RETURN 
      END IF
      IF(NC.GT.1) THEN 
         EPSILON=MAX(DX,DY,DZ)*TOL 
         V0(1)=V0(1)/(ICONTP+ICONTN) 
         V0(2)=V0(2)/(ICONTP+ICONTN) 
         V0(3)=V0(3)/(ICONTP+ICONTN) 
         CALL MFUNC3D(F0,FCOEF,V0(1),V0(2),V0(3)) 
         CALL MFUNC3D(F1,FCOEF,V0(1)+DX/2._W_P+EPSILON,V0(2),V0(3)) 
         CALL MFUNC3D(F2,FCOEF,V0(1)-DX/2._W_P-EPSILON,V0(2),V0(3)) 
         CALL MFUNC3D(F3,FCOEF,V0(1),V0(2)+DY/2._W_P+EPSILON,V0(3)) 
         CALL MFUNC3D(F4,FCOEF,V0(1),V0(2)-DY/2._W_P-EPSILON,V0(3)) 
         CALL MFUNC3D(F5,FCOEF,V0(1),V0(2),V0(3)+DZ/2._W_P+EPSILON) 
         CALL MFUNC3D(F6,FCOEF,V0(1),V0(2),V0(3)-DZ/2._W_P-EPSILON)
      ELSE
         F0=0.0_W_P
         F1=0.0_W_P
         F2=0.0_W_P
         F3=0.0_W_P
         F4=0.0_W_P
         F5=0.0_W_P
         F6=0.0_W_P
      END IF 
      IF((ICONTP.EQ.0.AND.NC.GT.1.AND.MAX(F0,F1,F2,F3,F4,F5,F6).LT.     &
     &     0._W_P).OR.(ICONTP.EQ.0.AND.NC.EQ.1)) THEN                   
            VF=0._W_P 
            RETURN 
      END IF 
      IF((ICONTN.EQ.0.AND.NC.GT.1.AND.MIN(F0,F1,F2,F3,F4,F5,F6).GT.     &
     &     0._W_P).OR.(ICONTN.EQ.0.AND.NC.EQ.1)) THEN                   
            VF=1._W_P 
            RETURN 
      END IF 
      CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,            &
     &     NTS,NTVT,NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)        
!. Root finding using Brent's method                                    
      DDX=DX/NCL 
      DDY=DY/NCL 
      DDZ=DZ/NCL 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CX1(I)=-XMIN 
         ELSE 
            CX1(I)=CX1(I-1)-DDX 
         END IF 
         CX2(I)=-CX1(I)+DDX 
      END DO 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CY1(I)=-YMIN 
         ELSE 
            CY1(I)=CY1(I-1)-DDY 
         END IF 
         CY2(I)=-CY1(I)+DDY 
      END DO 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CZ1(I)=-ZMIN 
         ELSE 
            CZ1(I)=CZ1(I-1)-DDZ 
         END IF 
         CZ2(I)=-CZ1(I)+DDZ 
      END DO 
!.. compute the volume VOLT of the original polyhedron                  
      CALL TOOLV3D(IPV,NIPV,NTS,VERTP,VOLT,XNS,YNS,ZNS)
      IF(VOLT.EQ.0.0_W_P) THEN
         VF=0.0_W_P
         RETURN
      END IF
      DO IC=1,NCL 
         IF(NCL.EQ.1) THEN 
            CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,  &
     &           NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,ZNS0, &
     &           ZNST)                                                  
         ELSE 
            CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,  &
     &           NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,ZNS2, &
     &           ZNST)                                                  
         END IF 
         IF(IC.GT.1) CALL INTE3D(CX1(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
     &        NTS2,NTV2,VERTP2,1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)        
         IF(IC.LT.NCL) CALL INTE3D(CX2(IC),ICONTN,ICONTP,IPV2,NIPV2,    &
     &        NTP2,NTS2,NTV2,VERTP2,-1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)  
         DO JC=1,NCL 
            IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,    &
     &           NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,XNS2, &
     &           YNS1,YNS2,ZNS1,ZNS2)                                   
            IF(JC.GT.1) CALL INTE3D(CY1(JC),ICONTN,ICONTP,IPV1,NIPV1,   &
     &           NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,1.0D0,YNS1,0.0D0,ZNS1)
            IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
               IF(JC.LT.NCL) CALL INTE3D(CY2(JC),ICONTN,ICONTP,IPV1,    &
     &              NIPV1,NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,-1.0D0,YNS1, &
     &              0.0D0,ZNS1)                                         
               IF(ICONTP.NE.0) THEN 
                  DO KC=1,NCL 
                     IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0, &
     &                    NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,   &
     &                    VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                     IF(KC.GT.1) CALL INTE3D(CZ1(KC),ICONTN,ICONTP,IPV0,&
     &                    NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,XNS0,0.0D0, &
     &                    YNS0,1.0D0,ZNS0)                              
                     IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                        IF(KC.LT.NCL) CALL INTE3D(CZ2(KC),ICONTN,ICONTP,&
     &                       IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,    &
     &                       XNS0,0.0D0,YNS0,-1.0D0,ZNS0)               
                        IF(ICONTP.NE.0) THEN 
!..   Subcell dedtermination by truncation                              
                           IF(NCL.GT.1) THEN 
                              ICONTP=0 
                              ICONTN=0 
                              DO IP=1,NTP0 
                                 ICHECK(IP)=0 
                              END DO 
                              DO IS=1,NTS0 
                                 DO IV=1,NIPV0(IS) 
                                    IP=IPV0(IS,IV) 
                                    IF(ICHECK(IP).EQ.0) THEN 
                                       ICHECK(IP)=1 
                                       X=VERTP0(IP,1) 
                                       Y=VERTP0(IP,2) 
                                       Z=VERTP0(IP,3) 
                                       CALL MFUNC3D(PHIV(IP),FCOEF,X,Y, &
     &                                      Z)                          
                                       IF(PHIV(IP).GE.0.0) THEN 
                                          IA(IP)=1 
                                          ICONTP=ICONTP+1 
                                       ELSE 
                                          IA(IP)=0 
                                          ICONTN=ICONTN+1 
                                       END IF 
                                    END IF 
                                 END DO 
                              END DO 
                           END IF 
                           IF(ICONTN.EQ.0) THEN 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
     &                             VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                              NTSINI=NTS0 
                              CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,        &
     &                             ISCUT,NIPV0,NTP0,NTS0,NTV0,          &
     &                             1.0d0,XNS0,0.0d0,YNS0,0.0d0,         &
     &                             ZNS0)                                
!.. Location of the new intersection points                             
                              IF(NTS0.GT.NTSINI) THEN 
                                 IS=NTS0 
                                 IS2=NTS0 
                                 DO IS=NTSINI+1,NTS0 
                                    SUMX=0.0 
                                    SUMY=0.0 
                                    SUMZ=0.0 
                                    DO IV=1,NIPV0(IS) 
                                       IP=IPV0(IS,IV) 
                                       IP0=IPIA0(IP) 
                                       IP1=IPIA1(IP) 
                                       V0(1)=VERTP0(IP0,1) 
                                       V0(2)=VERTP0(IP0,2) 
                                       V0(3)=VERTP0(IP0,3) 
                                       V1(1)=VERTP0(IP1,1) 
                                       V1(2)=VERTP0(IP1,2) 
                                       V1(3)=VERTP0(IP1,3) 
                                       CALL INTEMFUNC3D(MAX(DX,DY,DZ),  &
                                            FCOEF,IE,V0,V1,VI)                   
                                       IF(IE.EQ.0) THEN 
                                          VERTP0(IP,1)=VI(1) 
                                          VERTP0(IP,2)=VI(2) 
                                          VERTP0(IP,3)=VI(3) 
                                       ELSE 
                                       VERTP0(IP,1)=VERTP0(IP0,1)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      1)-VERTP0(IP0,1))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       VERTP0(IP,2)=VERTP0(IP0,2)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      2)-VERTP0(IP0,2))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       VERTP0(IP,3)=VERTP0(IP0,3)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      3)-VERTP0(IP0,3))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       END IF 
                                       SUMX=SUMX+VERTP0(IP,1) 
                                       SUMY=SUMY+VERTP0(IP,2) 
                                       SUMZ=SUMZ+VERTP0(IP,3) 
                                    END DO 
                                    NTP0=NTP0+1 
                                    VERTP0(NTP0,1)=SUMX/NIPV0(IS) 
                                    VERTP0(NTP0,2)=SUMY/NIPV0(IS) 
                                    VERTP0(NTP0,3)=SUMZ/NIPV0(IS) 
                                    V0(1)=VERTP0(NTP0,1) 
                                    V0(2)=VERTP0(NTP0,2) 
                                    V0(3)=VERTP0(NTP0,3) 
                                    CALL FINDBRACKETM(DD/DBLE(NCL),     &
     &                                   FCOEF,IEBRACKET,V0,V1)         
                                    IF(IEBRACKET.EQ.2) THEN 
                                       VI=V1 
                                    ELSE 
                                       CALL INTEMFUNC3D(DD*50.0_W_P/    &
                                            DBLE(NCL),FCOEF,IE,V0,V1,VI)
                                    END IF 
                                    IF(IE.EQ.0.OR.IEBRACKET.EQ.2)THEN 
                                       VERTP0(NTP0,1)=VI(1) 
                                       VERTP0(NTP0,2)=VI(2) 
                                       VERTP0(NTP0,3)=VI(3) 
                                    END IF 
                                    ISINI=IS2+1 
                                    DO IV=1,NIPV0(IS) 
                                       IS2=IS2+1 
                                       IV2=IV+1 
                                       IF(IV2.GT.                       &
     &                                      NIPV0(IS)) IV2=1            
                                       NIPV0(IS2)=3 
                                       IPV0(IS2,1)=NTP0 
                                       IPV0(IS2,2)=IPV0(IS,IV) 
                                       IPV0(IS2,3)=IPV0(IS,IV2) 
                                       XV1=VERTP0(IPV0(IS2,2),1)-       &
     &                                      VERTP0(IPV0(IS2,1),1)       
                                       YV1=VERTP0(IPV0(IS2,2),2)-       &
     &                                      VERTP0(IPV0(IS2,1),2)       
                                       ZV1=VERTP0(IPV0(IS2,2),3)-       &
     &                                      VERTP0(IPV0(IS2,1),3)       
                                       XV2=VERTP0(IPV0(IS2,3),1)-       &
     &                                      VERTP0(IPV0(IS2,2),1)       
                                       YV2=VERTP0(IPV0(IS2,3),2)-       &
     &                                      VERTP0(IPV0(IS2,2),2)       
                                       ZV2=VERTP0(IPV0(IS2,3),3)-       &
     &                                      VERTP0(IPV0(IS2,2),3)       
                                       XM=YV1*ZV2-ZV1*YV2 
                                       YM=ZV1*XV2-XV1*ZV2 
                                       ZM=XV1*YV2-YV1*XV2 
                                       AMOD=(XM**2.0+YM**2.0+           &
     &                                      ZM**2.0)**0.5               
                                       IF(AMOD.NE.0.0) THEN 
                                          XNS0(IS2)=XM/AMOD 
                                          YNS0(IS2)=YM/AMOD 
                                          ZNS0(IS2)=ZM/AMOD 
                                       ELSE 
                                          NIPV0(IS2)=0 
                                       END IF 
!..   Gauss quadrature volumes                                          
                                       V1(1)=VERTP0(IPV0(IS2,1),1) 
                                       V1(2)=VERTP0(IPV0(IS2,1),2) 
                                       V1(3)=VERTP0(IPV0(IS2,1),3) 
                                       V2(1)=VERTP0(IPV0(IS2,2),1) 
                                       V2(2)=VERTP0(IPV0(IS2,2),2) 
                                       V2(3)=VERTP0(IPV0(IS2,2),3) 
                                       V3(1)=VERTP0(IPV0(IS2,3),1) 
                                       V3(2)=VERTP0(IPV0(IS2,3),2) 
                                       V3(3)=VERTP0(IPV0(IS2,3),3) 
                                       CALL TRIVOLM(FCOEF,V1,V2,V3,     &
     &                                      VOLTRI)                     
                                       VF=VF+VOLTRI 
                                    END DO 
!* Cancel the IS face                                                   
                                    IF(IS2.GT.IS) NIPV0(IS)=0 
                                 END DO 
                                 NTS0=IS2 
                              end if 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
     &                             VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           END IF 
                        END IF 
                     END IF 
                  END DO 
               END IF 
            END IF 
         END DO 
      END DO 
      VF=VF/VOLT 
      RETURN 
      END                                           
!------------------------- END OF XINITFM3D --------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              XINITF3D                               c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! IPV      = array containing the global indices of the original pol. c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! NTV      = total number of vertices                                 c 
! TOL      = prescribed positive tolerance for the distance to the    c 
!            interface                                                c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! VF       = material volume fraction                                 c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE XINITF3D(FUNC3D,IPV,NC,NIPV,NTP,NTS,NTV,TOL,VERTP,VF,  &
     &     XNS,YNS,ZNS) BIND(C)                                         
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(IN) :: TOL 
      REAL(W_P), INTENT(OUT) :: VF 
      INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
      INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DX,DY,DZ,EPSILON,F0,F1,F2,F3,F4, &
     &     F5,F6,SUMX,SUMY,SUMZ,VOLF,VOLT,VOLTRI,X,XM,XMAX,XMIN,        &
     &     XP,XV1,XV2,Y,YM,YMAX,YMIN,YP,YV1,YV2,Z,ZM,ZMAX,ZMIN,ZP,ZV1,  &
     &     ZV2                                                          
      INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IE,IEBRACKET,IP,IP0,IP1,       &
     &     IS,IS2,ISINI,IV,IV2,JC,KC,NCL,NTP0,NTP1,NTP2,                &
     &     NTPT,NTS0,NTS1,NTS2,NTST,NTSINI,NTV0,NTV1,NTV2,NTVT          
!.. Local Arrays                                                        
      REAL(W_P) :: CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC),      &
     &     CX2(NC),CY1(NC),CY2(NC),CZ1(NC),CZ2(NC),PHIV(NV),V0(3),V1(3),&
     &     V2(3),V3(3),VI(3),VERTP0(NV,3),VERTP1(NV,3),VERTP2(NV,3),    &
     &     VERTPT(NV,3),XNS0(NS),XNS1(NS),XNS2(NS),XNST(NS),YNS0(NS),   &
     &     YNS1(NS),YNS2(NS),YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),       &
     &     ZNST(NS)                                                     
      INTEGER(I_P) :: IA(NV),ICHECK(NV),IPIA0(NV),IPIA1(NV),            &
     &     IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),ISCUT(NS),   &
     &     NIPV0(NS),NIPV1(NS),NIPV2(NS),NIPVT(NS)                      
!.. Coordinate extremes of the cell and vertex tagging                  
      NCL=NC 
      VF=0.0 
      XMIN=1.0D+20 
      XMAX=-1.0D+20 
      YMIN=1.0D+20 
      YMAX=-1.0D+20 
      ZMIN=1.0D+20 
      ZMAX=-1.0D+20 
      ICONTP=0 
      ICONTN=0 
      V0(1)=0.0 
      V0(2)=0.0 
      V0(3)=0.0 
!      PHIMIN=1D+20                                                     
      DO IP=1,NTP 
         ICHECK(IP)=0 
      END DO 
      DO IS=1,NTS 
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(ICHECK(IP).EQ.0) THEN 
               ICHECK(IP)=1 
               XP=VERTP(IP,1) 
               YP=VERTP(IP,2) 
               ZP=VERTP(IP,3) 
               V0(1)=V0(1)+XP 
               V0(2)=V0(2)+YP 
               V0(3)=V0(3)+ZP 
               XMIN=DMIN1(XMIN,XP) 
               XMAX=DMAX1(XMAX,XP) 
               YMIN=DMIN1(YMIN,YP) 
               YMAX=DMAX1(YMAX,YP) 
               ZMIN=DMIN1(ZMIN,ZP) 
               ZMAX=DMAX1(ZMAX,ZP) 
               PHIV(IP)=FUNC3D(XP,YP,ZP) 
!               PHIMIN=MIN(PHIMIN,ABS(PHIV(IP)))                       
               IF(PHIV(IP).GE.0.0) THEN 
                  IA(IP)=1 
                  ICONTP=ICONTP+1 
               ELSE 
                  IA(IP)=0 
                  ICONTN=ICONTN+1 
               END IF 
            END IF 
         END DO 
      END DO 
!.. initialization                                                      
      DX=XMAX-XMIN 
      DY=YMAX-YMIN 
      DZ=ZMAX-ZMIN 
      DD=0.01*MIN(DX,DY,DZ) 
      IF(DD.LT.1.0E-20_W_P) THEN
         VF=0._W_P 
         RETURN 
      END IF
      IF(NC.GT.1) THEN 
         EPSILON=MAX(DX,DY,DZ)*TOL 
         V0(1)=V0(1)/(ICONTP+ICONTN) 
         V0(2)=V0(2)/(ICONTP+ICONTN) 
         V0(3)=V0(3)/(ICONTP+ICONTN) 
         F0=FUNC3D(V0(1),V0(2),V0(3)) 
         F1=FUNC3D(V0(1)+DX/2._W_P+EPSILON,V0(2),V0(3)) 
         F2=FUNC3D(V0(1)-DX/2._W_P-EPSILON,V0(2),V0(3)) 
         F3=FUNC3D(V0(1),V0(2)+DY/2._W_P+EPSILON,V0(3)) 
         F4=FUNC3D(V0(1),V0(2)-DY/2._W_P-EPSILON,V0(3)) 
         F5=FUNC3D(V0(1),V0(2),V0(3)+DZ/2._W_P+EPSILON) 
         F6=FUNC3D(V0(1),V0(2),V0(3)-DZ/2._W_P-EPSILON)
      ELSE
         F0=0.0_W_P
         F1=0.0_W_P
         F2=0.0_W_P
         F3=0.0_W_P
         F4=0.0_W_P
         F5=0.0_W_P
         F6=0.0_W_P         
      END IF 
!      IPHI=0                                                           
      IF((ICONTP.EQ.0.AND.NC.GT.1.AND.MAX(F0,F1,F2,F3,F4,F5,F6).LT.     &
     &     0._W_P).OR.(ICONTP.EQ.0.AND.NC.EQ.1)) THEN                   
            VF=0._W_P 
            RETURN 
      END IF 
      IF((ICONTN.EQ.0.AND.NC.GT.1.AND.MIN(F0,F1,F2,F3,F4,F5,F6).GT.     &
     &     0._W_P).OR.(ICONTN.EQ.0.AND.NC.EQ.1)) THEN                   
            VF=1._W_P 
            RETURN 
      END IF 
!      IF(PHIMIN.LT.EPSILON) IPHI=1                                     
!      IF(IPHI.EQ.0) THEN                                               
!         IF(ICONTP.EQ.NTV) THEN                                        
!            VF=1.0                                                     
!            RETURN                                                     
!         END IF                                                        
!         IF(ICONTN.EQ.NTV) THEN                                        
!            VF=0.0                                                     
!            RETURN                                                     
!         END IF                                                        
!      END IF                                                           
      CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,            &
     &     NTS,NTVT,NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)        
!. Root finding using Brent's method                                    
!     Quitar la condicion NC.EQ.1. Hacer para cualquier NC.             
!     VI sera el punto de control.                                      
!     Si no se encuentra VI, hacer VI=V0 y forzar la division:          
!     Este seria el caso de una esfera centrada en la celda.            
!     Para determinar la division que debe pasar por el punto de control
!     hago:                                                             
!     ICONTROL=MAX(1,MIN(NC-1,INT(NC*(VI(1)-XMIN)/(XMAX-XMIN)+0.5)))    
!     JCONTROL=MAX(1,MIN(NC-1,INT(NC*(VI(2)-YMIN)/(YMAX-YMIN)+0.5)))    
!     KCONTROL=MAX(1,MIN(NC-1,INT(NC*(VI(3)-ZMIN)/(ZMAX-ZMIN)+0.5)))    
!     Despues hacer                                                     
!     CX2(ICONTROL)=VI(1); CX1(ICONTROL+1)=-VI(1)                       
!     CY2(JCONTROL)=VI(2); CY1(JCONTROL+1)=-VI(2)                       
!     CZ2(KCONTROL)=VI(3); CZ1(KCONTROL+1)=-VI(3)                       
!     Ojo, las expresiones anteriores valen si VI esta entre limites    
!      IF(NC.EQ.1) THEN                                                 
!      IF((ICONTP.EQ.0.AND.F0.GE.0.0).OR.(ICONTN.EQ.0.AND.              
!     -     F0.LE.0.0)) THEN                                            
!         VI=V0                                                         
!         IF(NC.EQ.1) THEN                                              
!            NCL=2                                                      
!         END IF                                                        
!c      ELSE                                                            
!c         ICONTROL=0                                                   
!c         JCONTROL=0                                                   
!c         KCONTROL=0                                                   
!c         CALL FINDBRACKET(DFX,DFY,DFZ,DD,FUNC3D,IEBRACKET,V0,V1)      
!c         IF(IEBRACKET.NE.-1) THEN                                     
!c            IF(IEBRACKET.EQ.2) THEN                                   
!c               VI=V1                                                  
!c            ELSE                                                      
!c               CALL INTEFUNC3D(FUNC3D,IE,NITER,V0,V1,VI)              
!c            END IF                                                    
!c            IF(IE.EQ.0.OR.IEBRACKET.EQ.2) THEN                        
!c               ICONTP2=0                                              
!c               ICONTN2=0                                              
!c               CPLIC=-(DFX*VI(1)+DFY*VI(2)+DFZ*VI(3))                 
!c               DO IP=1,NTP                                            
!c                  IF(ICHECK(IP).EQ.1) THEN                            
!c                     PHI2=DFX*VERTPT(IP,1)+DFY*VERTPT(IP,2)+DFZ*      
!c     -                    VERTPT(IP,3)+CPLIC                          
!c                     IF(PHI2.LT.0.0) THEN                             
!c                        ICONTN2=ICONTN2+1                             
!c                     ELSE                                             
!c                        ICONTP2=ICONTP2+1                             
!c                     END IF                                           
!c                  END IF                                              
!c               END DO                                                 
!c               IF((ICONTP*ICONTN.EQ.0.AND.ICONTP2*ICONTN2.NE.0).OR.   
!c     -              (ICONTP*ICONTN.NE.0.AND.ICONTP2*ICONTN2.EQ.0)) THE
!cC.. SI NC=1 FORZAR REFINAMIENTO                                       
!c                  IF(NC.EQ.1) THEN                                    
!c                     IF(VI(1).GT.XMIN.AND.VI(1).LT.XMAX) NCX=2        
!c                     IF(VI(2).GT.YMIN.AND.VI(2).LT.YMAX) NCY=2        
!c                     IF(VI(3).GT.ZMIN.AND.VI(3).LT.ZMAX) NCZ=2        
!c                  END IF                                              
!c               END IF                                                 
!c            END IF                                                    
!c         ELSE                                                         
!c            VI=V0                                                     
!c            IF(NC.EQ.1) THEN                                          
!c               NCX=2                                                  
!c               NCY=2                                                  
!c               NCZ=2                                                  
!c            END IF                                                    
!c         END IF                                                       
!      END IF                                                           
!      IF(VI(1).GT.XMIN.AND.VI(1).LT.XMAX.AND.NCX.GT.1) ICONTROL=MAX(1, 
!     -     MIN(NCX-1,INT(NCX*(VI(1)-XMIN)/(XMAX-XMIN)+0.5)))           
!      IF(VI(2).GT.YMIN.AND.VI(2).LT.YMAX.AND.NCY.GT.1) JCONTROL=MAX(1, 
!     -     MIN(NCY-1,INT(NCY*(VI(2)-YMIN)/(YMAX-YMIN)+0.5)))           
!      IF(VI(3).GT.ZMIN.AND.VI(3).LT.ZMAX.AND.NCZ.GT.1) KCONTROL=MAX(1, 
!     -     MIN(NCZ-1,INT(NCZ*(VI(3)-ZMIN)/(ZMAX-ZMIN)+0.5)))           
                                                                        
!      IF(VI(2).GT.YMIN.AND.VI(2).LT.YMAX) THEN                         
!         NCY=2                                                         
!         CY1(1)=-YMIN                                                  
!         CY2(1)=VI(2)                                                  
!         CY1(2)=-VI(2)                                                 
!         CY2(2)=YMAX                                                   
!      END IF                                                           
!      IF(VI(3).GT.ZMIN.AND.VI(3).LT.ZMAX) THEN                         
!         NCZ=2                                                         
!         CZ1(1)=-ZMIN                                                  
!         CZ2(1)=VI(3)                                                  
!         CZ1(2)=-VI(3)                                                 
!         CZ2(2)=ZMAX                                                   
!      END IF                                                           
!      ELSE                                                             
      DDX=DX/NCL 
      DDY=DY/NCL 
      DDZ=DZ/NCL 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CX1(I)=-XMIN 
         ELSE 
            CX1(I)=CX1(I-1)-DDX 
         END IF 
         CX2(I)=-CX1(I)+DDX 
      END DO 
!      IF(ICONTROL.NE.0) THEN                                           
!         CX2(ICONTROL)=VI(1)                                           
!         CX1(ICONTROL+1)=-VI(1)                                        
!      END IF                                                           
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CY1(I)=-YMIN 
         ELSE 
            CY1(I)=CY1(I-1)-DDY 
         END IF 
         CY2(I)=-CY1(I)+DDY 
      END DO 
!      IF(JCONTROL.NE.0) THEN                                           
!         CY2(JCONTROL)=VI(2)                                           
!         CY1(JCONTROL+1)=-VI(2)                                        
!      END IF                                                           
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CZ1(I)=-ZMIN 
         ELSE 
            CZ1(I)=CZ1(I-1)-DDZ 
         END IF 
         CZ2(I)=-CZ1(I)+DDZ 
      END DO 
!      IF(KCONTROL.NE.0) THEN                                           
!         CZ2(KCONTROL)=VI(3)                                           
!         CZ1(KCONTROL+1)=-VI(3)                                        
!      END IF                                                           
                                                                        
                                                                        
!      END IF                                                           
!-----------------------------------                                    
!      DX=XMAX-XMIN                                                     
!      DY=YMAX-YMIN                                                     
!      DZ=ZMAX-ZMIN                                                     
!++++      DD=0.05*MIN(DX,DY,DZ)                                        
                                                                        
!.. compute the volume VOLT of the original polyhedron                  
      CALL TOOLV3D(IPV,NIPV,NTS,VERTP,VOLT,XNS,YNS,ZNS)
      IF(VOLT.EQ.0.0_W_P) THEN
         VF=0.0_W_P
         RETURN
      END IF
!      DDX=DX/NC                                                        
!      DDY=DY/NC                                                        
!      DDZ=DZ/NC                                                        
                                                                        
      DO IC=1,NCL 
!         XC=XMIN+(IC-1)*DDX                                            
!         CALL CPPOL3D(CS2,CS,IPV2,IPV,NIPV2,NIPV,NTP2,NTP,NTS2,        
!     -        NTS,NTV2,NTV,VERTP2,VERTP,XNS2,XNS,YNS2,YNS,ZNS2,ZNS)    
         IF(NCL.EQ.1) THEN 
            CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,  &
     &           NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,ZNS0, &
     &           ZNST)                                                  
         ELSE 
            CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,  &
     &           NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,ZNS2, &
     &           ZNST)                                                  
         END IF 
!         CX1=-XC                                                       
         IF(IC.GT.1) CALL INTE3D(CX1(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
     &        NTS2,NTV2,VERTP2,1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)        
!         CX2=XC+DDX                                                    
         IF(IC.LT.NCL) CALL INTE3D(CX2(IC),ICONTN,ICONTP,IPV2,NIPV2,    &
     &        NTP2,NTS2,NTV2,VERTP2,-1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)  
         DO JC=1,NCL 
!            YC=YMIN+(JC-1)*DDY                                         
            IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,    &
     &           NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,XNS2, &
     &           YNS1,YNS2,ZNS1,ZNS2)                                   
!            CY1=-YC                                                    
            IF(JC.GT.1) CALL INTE3D(CY1(JC),ICONTN,ICONTP,IPV1,NIPV1,   &
     &           NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,1.0D0,YNS1,0.0D0,ZNS1)
            IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
!               CY2=YC+DDY                                              
               IF(JC.LT.NCL) CALL INTE3D(CY2(JC),ICONTN,ICONTP,IPV1,    &
     &              NIPV1,NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,-1.0D0,YNS1, &
     &              0.0D0,ZNS1)                                         
               IF(ICONTP.NE.0) THEN 
                  DO KC=1,NCL 
!                     ZC=ZMIN+(KC-1)*DDZ                                
                     IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0, &
     &                    NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,   &
     &                    VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
!                     CZ1=-ZC                                           
                     IF(KC.GT.1) CALL INTE3D(CZ1(KC),ICONTN,ICONTP,IPV0,&
     &                    NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,XNS0,0.0D0, &
     &                    YNS0,1.0D0,ZNS0)                              
                     IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
!                        CZ2=ZC+DDZ                                     
                        IF(KC.LT.NCL) CALL INTE3D(CZ2(KC),ICONTN,ICONTP,&
     &                       IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,    &
     &                       XNS0,0.0D0,YNS0,-1.0D0,ZNS0)               
                        IF(ICONTP.NE.0) THEN 
!..   Subcell dedtermination by truncation                              
                           IF(NCL.GT.1) THEN 
                              ICONTP=0 
                              ICONTN=0 
                              DO IP=1,NTP0 
                                 ICHECK(IP)=0 
                              END DO 
                              DO IS=1,NTS0 
                                 DO IV=1,NIPV0(IS) 
                                    IP=IPV0(IS,IV) 
                                    IF(ICHECK(IP).EQ.0) THEN 
                                       ICHECK(IP)=1 
                                       X=VERTP0(IP,1) 
                                       Y=VERTP0(IP,2) 
                                       Z=VERTP0(IP,3) 
                                       PHIV(IP)=FUNC3D(X,Y,Z) 
                                       IF(PHIV(IP).GE.0.0) THEN 
                                          IA(IP)=1 
                                          ICONTP=ICONTP+1 
                                       ELSE 
                                          IA(IP)=0 
                                          ICONTN=ICONTN+1 
                                       END IF 
                                    END IF 
                                 END DO 
                              END DO 
                           END IF 
                           IF(ICONTN.EQ.0) THEN 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
     &                             VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
!                  write(6,*)'->',volf,ic,jc,kc                         
                           ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                              NTSINI=NTS0 
                              CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,        &
     &                             ISCUT,NIPV0,NTP0,NTS0,NTV0,          &
     &                             1.0d0,XNS0,0.0d0,YNS0,0.0d0,         &
     &                             ZNS0)                                
!.. Location of the new intersection points                             
                              IF(NTS0.GT.NTSINI) THEN 
                                 IS=NTS0 
                                 IS2=NTS0 
                                 DO IS=NTSINI+1,NTS0 
                                    SUMX=0.0 
                                    SUMY=0.0 
                                    SUMZ=0.0 
                                    DO IV=1,NIPV0(IS) 
                                       IP=IPV0(IS,IV) 
                                       IP0=IPIA0(IP) 
                                       IP1=IPIA1(IP) 
                                       V0(1)=VERTP0(IP0,1) 
                                       V0(2)=VERTP0(IP0,2) 
                                       V0(3)=VERTP0(IP0,3) 
                                       V1(1)=VERTP0(IP1,1) 
                                       V1(2)=VERTP0(IP1,2) 
                                       V1(3)=VERTP0(IP1,3) 
!---                                                                    
                                       CALL INTEFUNC3D(MAX(DX,DY,DZ),   &
     &                                      FUNC3D,IE,V0,V1,VI)                   
                                       IF(IE.EQ.0) THEN 
                                          VERTP0(IP,1)=VI(1) 
                                          VERTP0(IP,2)=VI(2) 
                                          VERTP0(IP,3)=VI(3) 
                                       ELSE 
!---                                                                    
                                       VERTP0(IP,1)=VERTP0(IP0,1)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      1)-VERTP0(IP0,1))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       VERTP0(IP,2)=VERTP0(IP0,2)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      2)-VERTP0(IP0,2))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       VERTP0(IP,3)=VERTP0(IP0,3)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      3)-VERTP0(IP0,3))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       END IF 
                                       SUMX=SUMX+VERTP0(IP,1) 
                                       SUMY=SUMY+VERTP0(IP,2) 
                                       SUMZ=SUMZ+VERTP0(IP,3) 
                                    END DO 
                                    NTP0=NTP0+1 
                                    VERTP0(NTP0,1)=SUMX/NIPV0(IS) 
                                    VERTP0(NTP0,2)=SUMY/NIPV0(IS) 
                                    VERTP0(NTP0,3)=SUMZ/NIPV0(IS) 
!---                                                                    
                                    V0(1)=VERTP0(NTP0,1) 
                                    V0(2)=VERTP0(NTP0,2) 
                                    V0(3)=VERTP0(NTP0,3) 
!. OJO, SI LA SUPERFICIE ES CONCAVA HABRIA QUE CAMBIAR A -XNV, ...      
!                                       V1(1)=V0(1)+XNV*DD/DBLE(NC)     
!                                       V1(2)=V0(2)+YNV*DD/DBLE(NC)     
!                                       V1(3)=V0(3)+ZNV*DD/DBLE(NC)     
                                    CALL FINDBRACKET(DD/DBLE(NCL),      &
     &                                   FUNC3D,IEBRACKET,V0,V1)        
                                    IF(IEBRACKET.EQ.2) THEN 
                                       VI=V1 
                                    ELSE 
                                       CALL INTEFUNC3D(DD*50.0_W_P/DBLE(&
                                            NCL),FUNC3D,IE,V0,V1,VI)
                                    END IF 
                                    IF(IE.EQ.0.OR.IEBRACKET.EQ.2)THEN 
                                       VERTP0(NTP0,1)=VI(1) 
                                       VERTP0(NTP0,2)=VI(2) 
                                       VERTP0(NTP0,3)=VI(3) 
                                    END IF 
!---                                                                    
!: The new face IS is replaced by NIPV(IS) triangular faces             
!                                    XNV=0.0                            
!                                    YNV=0.0                            
!                                    ZNV=0.0                            
                                    ISINI=IS2+1 
                                    DO IV=1,NIPV0(IS) 
                                       IS2=IS2+1 
                                       IV2=IV+1 
                                       IF(IV2.GT.                       &
     &                                      NIPV0(IS)) IV2=1            
                                       NIPV0(IS2)=3 
                                       IPV0(IS2,1)=NTP0 
                                       IPV0(IS2,2)=IPV0(IS,IV) 
                                       IPV0(IS2,3)=IPV0(IS,IV2) 
                                       XV1=VERTP0(IPV0(IS2,2),1)-       &
     &                                      VERTP0(IPV0(IS2,1),1)       
                                       YV1=VERTP0(IPV0(IS2,2),2)-       &
     &                                      VERTP0(IPV0(IS2,1),2)       
                                       ZV1=VERTP0(IPV0(IS2,2),3)-       &
     &                                      VERTP0(IPV0(IS2,1),3)       
                                       XV2=VERTP0(IPV0(IS2,3),1)-       &
     &                                      VERTP0(IPV0(IS2,2),1)       
                                       YV2=VERTP0(IPV0(IS2,3),2)-       &
     &                                      VERTP0(IPV0(IS2,2),2)       
                                       ZV2=VERTP0(IPV0(IS2,3),3)-       &
     &                                      VERTP0(IPV0(IS2,2),3)       
                                       XM=YV1*ZV2-ZV1*YV2 
                                       YM=ZV1*XV2-XV1*ZV2 
                                       ZM=XV1*YV2-YV1*XV2 
                                       AMOD=(XM**2.0+YM**2.0+           &
     &                                      ZM**2.0)**0.5               
                                       IF(AMOD.NE.0.0) THEN 
                                          XNS0(IS2)=XM/AMOD 
                                          YNS0(IS2)=YM/AMOD 
                                          ZNS0(IS2)=ZM/AMOD 
                                       ELSE 
                                          NIPV0(IS2)=0 
                                       END IF 
!..   Gauss quadrature volumes                                          
                                       V1(1)=VERTP0(IPV0(IS2,1),1) 
                                       V1(2)=VERTP0(IPV0(IS2,1),2) 
                                       V1(3)=VERTP0(IPV0(IS2,1),3) 
                                       V2(1)=VERTP0(IPV0(IS2,2),1) 
                                       V2(2)=VERTP0(IPV0(IS2,2),2) 
                                       V2(3)=VERTP0(IPV0(IS2,2),3) 
                                       V3(1)=VERTP0(IPV0(IS2,3),1) 
                                       V3(2)=VERTP0(IPV0(IS2,3),2) 
                                       V3(3)=VERTP0(IPV0(IS2,3),3) 
                                       CALL TRIVOL(FUNC3D,V1,V2,V3,     &
     &                                      VOLTRI)                     
                                       VF=VF+VOLTRI 
                                    END DO 
!                                    AMOD=(XM**2.0+YM**2.0+             
!     -                                   ZM**2.0)**0.5                 
!                                    IF(AMOD.NE.0.0) THEN               
!c                                       XNV=XNV/AMOD                   
!c                                       YNV=YNV/AMOD                   
!c                                       ZNV=ZNV/AMOD                   
!C                                       V0(1)=VERTP0(NTP0,1)           
!                                       V0(2)=VERTP0(NTP0,2)            
!                                       V0(3)=VERTP0(NTP0,3)            
!c. OJO, SI LA SUPERFICIE ES CONCAVA HABRIA QUE CAMBIAR A -XNV, ...     
!c                                       V1(1)=V0(1)+XNV*DD/DBLE(NC)    
!c                                       V1(2)=V0(2)+YNV*DD/DBLE(NC)    
!c                                       V1(3)=V0(3)+ZNV*DD/DBLE(NC)    
!                                       CALL FINDBRACKET(DFX,DFY,DFZ,   
!     -                                      DD/DBLE(NC),FUNC3D,        
!     -                                      IEBRACKET,V0,V1)           
!                                       IF(IEBRACKET.EQ.2) THEN         
!                                          VI=V1                        
!                                       ELSE                            
!                                          CALL INTEFUNC3D(FUNC3D,IE,   
!     -                                         NITER,V0,V1,VI)         
!                                       END IF                          
!                                       IF(IE.EQ.0.OR.IEBRACKET.EQ.2)THE
!                                          VERTP0(NTP0,1)=VI(1)         
!                                          VERTP0(NTP0,2)=VI(2)         
!                                          VERTP0(NTP0,3)=VI(3)         
!. Compute again the normal vectors of the triangular-cap faces         
!                                          DO IST=ISINI,IS2             
!                                             XV1=VERTP0(IPV0(IST,2),1)-
!     -                                            VERTP0(IPV0(IST,1),1)
!                                             YV1=VERTP0(IPV0(IST,2),2)-
!     -                                            VERTP0(IPV0(IST,1),2)
!                                             ZV1=VERTP0(IPV0(IST,2),3)-
!     -                                            VERTP0(IPV0(IST,1),3)
!                                             XV2=VERTP0(IPV0(IST,3),1)-
!     -                                            VERTP0(IPV0(IST,2),1)
!                                             YV2=VERTP0(IPV0(IST,3),2)-
!     -                                            VERTP0(IPV0(IST,2),2)
!                                             ZV2=VERTP0(IPV0(IST,3),3)-
!     -                                            VERTP0(IPV0(IST,2),3)
!                                             XM=YV1*ZV2-ZV1*YV2        
!                                             YM=ZV1*XV2-XV1*ZV2        
!                                             ZM=XV1*YV2-YV1*XV2        
!                                             AMOD=(XM**2.0+YM**2.0+    
!     -                                            ZM**2.0)**0.5        
!                                             IF(AMOD.NE.0.0) THEN      
!                                                XNS0(IST)=XM/AMOD      
!                                                YNS0(IST)=YM/AMOD      
!                                                ZNS0(IST)=ZM/AMOD      
!                                             END IF                    
!                                          END DO                       
!                                       END IF                          
!                                    END IF                             
                                                                        
!* Cancel the IS face                                                   
                                    IF(IS2.GT.IS) NIPV0(IS)=0 
                                 END DO 
                                 NTS0=IS2 
                              end if 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
     &                             VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           END IF 
                        END IF 
                     END IF 
                  END DO 
               END IF 
            END IF 
         END DO 
      END DO 
      VF=VF/VOLT 
      RETURN 
      END                                           
!------------------------- END OF XINITF3D ---------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              HINITF3D                               c 
! Improved version of HIVOF                                           c
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! IPV      = array containing the global indices of the original pol. c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! NTV      = total number of vertices                                 c 
! TOL      = prescribed positive tolerance for the distance to the    c 
!            interface                                                c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! VF       = material volume fraction                                 c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE HINITF3D(FUNC3D,IPV,NC,NE,NIPV,NTP,NTS,NTV,TOL,VERTP,  &
           VF,XNS,YNS,ZNS) BIND(C)                                         
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(IN) :: TOL 
      REAL(W_P), INTENT(OUT) :: VF 
      INTEGER(I_P), INTENT(IN) :: NC, NE, NTP, NTS, NTV 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
      INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DX,DY,DZ,EPSILON,F0,F1,F2,F3,F4, &
           F5,F6,VOLF,VOLT,VOLTRI,X,XM,XMAX,XMIN,XP,XV1,XV2,Y,YM,YMAX,  &
           YMIN,YP,YV1,YV2,Z,ZM,ZMAX,ZMIN,ZP,ZV1,ZV2        
      INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IE,IEBRACKET,IP,IP0,IP1,       &
     &     IS,IS2,ISINI,IV,IV2,JC,KC,NCL,NTP0,NTP1,NTP2,NTPINI,         &
     &     NTPT,NTS0,NTS1,NTS2,NTST,NTSINI,NTV0,NTV1,NTV2,NTVT          
!.. Local Arrays                                                        
      REAL(W_P) :: CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC),      &
     &     CX2(NC),CY1(NC),CY2(NC),CZ1(NC),CZ2(NC),PHIV(NV),V0(3),V1(3),&
     &     V2(3),V3(3),VI(3),VERTP0(NV,3),VERTP1(NV,3),VERTP2(NV,3),    &
     &     VERTPT(NV,3),XNS0(NS),XNS1(NS),XNS2(NS),XNST(NS),YNS0(NS),   &
     &     YNS1(NS),YNS2(NS),YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),       &
     &     ZNST(NS)                                                     
      INTEGER(I_P) :: IA(NV),ICHECK(NV),IPIA0(NV),IPIA1(NV),            &
     &     IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),ISCFIP(NV),  &
     &     NIPV0(NS),NIPV1(NS),NIPV2(NS),NIPVT(NS)                      
!.. Coordinate extremes of the cell and vertex tagging                  
      NCL=NC 
      VF=0.0 
      XMIN=1.0D+20 
      XMAX=-1.0D+20 
      YMIN=1.0D+20 
      YMAX=-1.0D+20 
      ZMIN=1.0D+20 
      ZMAX=-1.0D+20 
      ICONTP=0 
      ICONTN=0 
      V0(1)=0.0 
      V0(2)=0.0 
      V0(3)=0.0 
      DO IP=1,NTP 
         ICHECK(IP)=0 
      END DO 
      DO IS=1,NTS 
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(ICHECK(IP).EQ.0) THEN 
               ICHECK(IP)=1 
               XP=VERTP(IP,1) 
               YP=VERTP(IP,2) 
               ZP=VERTP(IP,3) 
               V0(1)=V0(1)+XP 
               V0(2)=V0(2)+YP 
               V0(3)=V0(3)+ZP 
               XMIN=DMIN1(XMIN,XP) 
               XMAX=DMAX1(XMAX,XP) 
               YMIN=DMIN1(YMIN,YP) 
               YMAX=DMAX1(YMAX,YP) 
               ZMIN=DMIN1(ZMIN,ZP) 
               ZMAX=DMAX1(ZMAX,ZP) 
               PHIV(IP)=FUNC3D(XP,YP,ZP) 
               IF(PHIV(IP).GE.0.0) THEN 
                  IA(IP)=1 
                  ICONTP=ICONTP+1 
               ELSE 
                  IA(IP)=0 
                  ICONTN=ICONTN+1 
               END IF 
            END IF 
         END DO 
      END DO 
!.. initialization                                                      
      DX=XMAX-XMIN 
      DY=YMAX-YMIN 
      DZ=ZMAX-ZMIN 
      DD=0.01*MIN(DX,DY,DZ) 
      IF(DD.LT.1.0E-20_W_P) THEN
         VF=0._W_P 
         RETURN 
      END IF
      IF(NC.GT.1) THEN 
         EPSILON=MAX(DX,DY,DZ)*TOL 
         V0(1)=V0(1)/(ICONTP+ICONTN) 
         V0(2)=V0(2)/(ICONTP+ICONTN) 
         V0(3)=V0(3)/(ICONTP+ICONTN) 
         F0=FUNC3D(V0(1),V0(2),V0(3)) 
         F1=FUNC3D(V0(1)+DX/2._W_P+EPSILON,V0(2),V0(3)) 
         F2=FUNC3D(V0(1)-DX/2._W_P-EPSILON,V0(2),V0(3)) 
         F3=FUNC3D(V0(1),V0(2)+DY/2._W_P+EPSILON,V0(3)) 
         F4=FUNC3D(V0(1),V0(2)-DY/2._W_P-EPSILON,V0(3)) 
         F5=FUNC3D(V0(1),V0(2),V0(3)+DZ/2._W_P+EPSILON) 
         F6=FUNC3D(V0(1),V0(2),V0(3)-DZ/2._W_P-EPSILON)
      ELSE
         F0=0.0_W_P
         F1=0.0_W_P
         F2=0.0_W_P
         F3=0.0_W_P
         F4=0.0_W_P
         F5=0.0_W_P
         F6=0.0_W_P         
      END IF 
      IF((ICONTP.EQ.0.AND.NC.GT.1.AND.MAX(F0,F1,F2,F3,F4,F5,F6).LT.     &
           0._W_P).OR.(ICONTP.EQ.0.AND.NC.EQ.1)) THEN                   
         VF=0._W_P 
         RETURN 
      END IF
      IF((ICONTN.EQ.0.AND.NC.GT.1.AND.MIN(F0,F1,F2,F3,F4,F5,F6).GT.     &
           0._W_P).OR.(ICONTN.EQ.0.AND.NC.EQ.1)) THEN                   
         VF=1._W_P 
         RETURN 
      END IF
!.. compute the volume VOLT of the original polyhedron                  
      CALL TOOLV3D(IPV,NIPV,NTS,VERTP,VOLT,XNS,YNS,ZNS)
      IF(VOLT.EQ.0.0_W_P) THEN
         VF=0.0_W_P
         RETURN
      END IF
      CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,            &
           NTS,NTVT,NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)        
!. Root finding using Brent's method                                    
      DDX=DX/NCL 
      DDY=DY/NCL 
      DDZ=DZ/NCL 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CX1(I)=-XMIN 
         ELSE 
            CX1(I)=CX1(I-1)-DDX 
         END IF
         CX2(I)=-CX1(I)+DDX 
      END DO
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CY1(I)=-YMIN 
         ELSE 
            CY1(I)=CY1(I-1)-DDY 
         END IF 
         CY2(I)=-CY1(I)+DDY 
      END DO 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CZ1(I)=-ZMIN 
         ELSE 
            CZ1(I)=CZ1(I-1)-DDZ 
         END IF 
         CZ2(I)=-CZ1(I)+DDZ 
      END DO 
      DO IC=1,NCL 
         IF(NCL.EQ.1) THEN 
            CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,  &
                 NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,ZNS0, &
                 ZNST)                                                  
         ELSE 
            CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,  &
                 NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,ZNS2, &
                 ZNST)                                                  
         END IF
         IF(IC.GT.1) CALL INTE3D(CX1(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
              NTS2,NTV2,VERTP2,1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)        
         IF(IC.LT.NCL) CALL INTE3D(CX2(IC),ICONTN,ICONTP,IPV2,NIPV2,    &
              NTP2,NTS2,NTV2,VERTP2,-1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)  
         DO JC=1,NCL 
            IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,    &
                 NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,XNS2, &
                 YNS1,YNS2,ZNS1,ZNS2)                                   
            IF(JC.GT.1) CALL INTE3D(CY1(JC),ICONTN,ICONTP,IPV1,NIPV1,   &
                 NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,1.0D0,YNS1,0.0D0,ZNS1)
            IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
               IF(JC.LT.NCL) CALL INTE3D(CY2(JC),ICONTN,ICONTP,IPV1,    &
                    NIPV1,NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,-1.0D0,YNS1, &
                    0.0D0,ZNS1)                                         
               IF(ICONTP.NE.0) THEN 
                  DO KC=1,NCL 
                     IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0, &
                          NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,   &
                          VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                     IF(KC.GT.1) CALL INTE3D(CZ1(KC),ICONTN,ICONTP,IPV0,&
                          NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,XNS0,0.0D0, &
                          YNS0,1.0D0,ZNS0)                              
                     IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                        IF(KC.LT.NCL) CALL INTE3D(CZ2(KC),ICONTN,ICONTP,&
                             IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,    &
                             XNS0,0.0D0,YNS0,-1.0D0,ZNS0)               
                        IF(ICONTP.NE.0) THEN 
!..   Subcell dedtermination by truncation                              
                           IF(NCL.GT.1) THEN 
                              ICONTP=0 
                              ICONTN=0 
                              DO IP=1,NTP0 
                                 ICHECK(IP)=0 
                              END DO
                              DO IS=1,NTS0 
                                 DO IV=1,NIPV0(IS) 
                                    IP=IPV0(IS,IV) 
                                    IF(ICHECK(IP).EQ.0) THEN 
                                       ICHECK(IP)=1 
                                       X=VERTP0(IP,1) 
                                       Y=VERTP0(IP,2) 
                                       Z=VERTP0(IP,3) 
                                       PHIV(IP)=FUNC3D(X,Y,Z) 
                                       IF(PHIV(IP).GE.0.0) THEN 
                                          IA(IP)=1 
                                          ICONTP=ICONTP+1 
                                       ELSE 
                                          IA(IP)=0 
                                          ICONTN=ICONTN+1 
                                       END IF
                                    END IF
                                 END DO
                              END DO
                           END IF
                           IF(ICONTN.EQ.0) THEN 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
                                   VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                              NTSINI=NTS0
                              NTPINI=NTP0
!                              CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,        &
!                                   ISCUT,NIPV0,NTP0,NTS0,NTV0,          &
!                                   1.0d0,XNS0,0.0d0,YNS0,0.0d0,         &
!                                   ZNS0)
                              CALL NEWPOLCF3D(IA,IPIA0,IPIA1,IPV0,      &
                                   ISCFIP,NIPV0,NTP0,NTS0,NTV0)
                              !.. Location of the new intersection points   
                              IF(NTS0.GT.NTSINI) THEN 
                                 IS=NTS0 
                                 IS2=NTS0 
                                 DO IS=NTSINI+1,NTS0 
                                    DO IV=1,NIPV0(IS) 
                                       IP=IPV0(IS,IV) 
                                       IP0=IPIA0(IP) 
                                       IP1=IPIA1(IP) 
                                       V0(1)=VERTP0(IP0,1) 
                                       V0(2)=VERTP0(IP0,2) 
                                       V0(3)=VERTP0(IP0,3) 
                                       V1(1)=VERTP0(IP1,1) 
                                       V1(2)=VERTP0(IP1,2) 
                                       V1(3)=VERTP0(IP1,3) 
                                       CALL INTEFUNC3D(MAX(DX,DY,DZ),   &
                                            FUNC3D,IE,V0,V1,VI)                   
                                       IF(IE.EQ.0) THEN 
                                          VERTP0(IP,1)=VI(1) 
                                          VERTP0(IP,2)=VI(2) 
                                          VERTP0(IP,3)=VI(3) 
                                       ELSE 
                                          VERTP0(IP,1)=VERTP0(IP0,1)-   &
                                               PHIV(IP0)*(VERTP0(IP1,   &
                                               1)-VERTP0(IP0,1))/(      &
                                               PHIV(IP1)-PHIV(IP0))        
                                          VERTP0(IP,2)=VERTP0(IP0,2)-   &
                                               PHIV(IP0)*(VERTP0(IP1,   &
                                               2)-VERTP0(IP0,2))/(      &
                                               PHIV(IP1)-PHIV(IP0))   
                                          VERTP0(IP,3)=VERTP0(IP0,3)-   &
                                               PHIV(IP0)*(VERTP0(IP1,   &
                                               3)-VERTP0(IP0,3))/(      &
                                               PHIV(IP1)-PHIV(IP0))    
                                       END IF
                                    END DO                                    
                                 END DO
                                 !Refine cap
                                 CALL REFINECAP(DD,FUNC3D,IPV0,ISCFIP,  &
                                      NE,NIPV0,NTP0,NTS0,NTSINI,NTV0,   &
                                      VERTP0,XNS0,YNS0,ZNS0)
                                 DO IS2=NTSINI+1,NTS0
                                    IF(NIPV0(IS2).GT.0) THEN
!..   Gauss quadrature volumes                                          
                                       V1(1)=VERTP0(IPV0(IS2,1),1) 
                                       V1(2)=VERTP0(IPV0(IS2,1),2) 
                                       V1(3)=VERTP0(IPV0(IS2,1),3) 
                                       V2(1)=VERTP0(IPV0(IS2,2),1) 
                                       V2(2)=VERTP0(IPV0(IS2,2),2) 
                                       V2(3)=VERTP0(IPV0(IS2,2),3) 
                                       V3(1)=VERTP0(IPV0(IS2,3),1) 
                                       V3(2)=VERTP0(IPV0(IS2,3),2) 
                                       V3(3)=VERTP0(IPV0(IS2,3),3) 
                                       CALL TRIVOL(FUNC3D,V1,V2,V3,     &
                                            VOLTRI)                     
                                       VF=VF+VOLTRI
                                    END IF
                                 END DO
                                 
                                 CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
                                      VOLF,XNS0,YNS0,ZNS0)                 
                                 VF=VF+VOLF 
                              END IF
                           END IF
                        END IF
                     END IF
                  END DO
               END IF
            END IF
         END DO
      END DO
      VF=VF/VOLT 
      RETURN 
    END SUBROUTINE HINITF3D
!------------------------- END OF HINITF3D ---------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              TRICAP                                 c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! DD       = differential size                                        c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! IPV      = array containing the global indices of the truncated pol.c 
!            vertices                                                 c 
! ISCFIP   = array containing the index of the clipped face           c
!            associated to each new intersection point                c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
! NIPV     = number of vertices of each face                          c 
! NS2      = size of arrays involving polyhedron faces                c
! NTP      = last global vertex index                                 c 
! NTS      = last face index of the truncated polyhedron              c 
! NTSINI   = last face index of the original polyhedron               c 
! NTV      = total number of vertices                                 c 
! NV2      = size of arrays involving polyhedron vertices             c
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! IPV      = array containing the global indices of the refined-poly. c 
!            vertices                                                 c 
! NIPV     = number of vertices of each face of the refined poly.     c 
! NTP      = last global vertex index of the refined polyhedron       c 
! NTS      = last face index of the refined polyhedron                c 
! NTV      = total number of vertices of the refined polyhedron       c 
! VERTP    = vertex coordinates of the refined polyhedron             c 
! XNS, ... = unit-lenght normals to the faces of the refined polyh.   c 
!---------------------------------------------------------------------c 
    SUBROUTINE TRICAP(DD,FUNC3D,IPV,ISCFIP,NE,NIPV,NS2,NTP,NTS,NTSINI,  &
         NTV,NV2,VERTP,XNS,YNS,ZNS) BIND(C)
!.. Scalar Arguments                                                    
      INTEGER(I_P), INTENT(IN) :: NE, NS2, NTSINI, NV2
      INTEGER(I_P), INTENT(IN) :: ISCFIP(NV)
      REAL(W_P), INTENT(IN) :: DD
      INTEGER(I_P), INTENT(INOUT) :: NTP, NTS, NTV 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(INOUT) :: VERTP(NV2,3),XNS(NS2),YNS(NS2),ZNS(NS2) 
      INTEGER(I_P), INTENT(INOUT) :: IPV(NS2,NV2),NIPV(NS2) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      INTEGER(I_P) :: I,IE,IEBRACKET,IER,IP,IP2,IPNEW,IS,ISNEW,IST,IV,  &
           IV2,IVISNEW,IVNEW,JU,JU1,JV,JV1,JW,JW1,NPC,NTPINI
      REAL(W_P) :: DMOD,XM,XV1,XV2,YM,YV1,YV2,ZM,ZV1,ZV2
!.. Local Arrays
      INTEGER(I_P) :: IPT(NE+2,NE+2,NE+2),IPV2(NS2,NV2)
      REAL(W_P) :: SUMP(3),V0(3),VE0(3),V1(3),VE1(3),VEI(3),VEN(3),     &
           VET(3),VI(3)
      
      IPNEW=NTP
      IST=NTS
      DO ISNEW=NTSINI+1,NTS
         NTPINI=IPNEW
         DO IVISNEW=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IVISNEW)
            IF(IVISNEW.EQ.NIPV(ISNEW)) THEN
               IP2=IPV(ISNEW,1)
            ELSE
               IP2=IPV(ISNEW,IVISNEW+1)
            END IF
            IS=ISCFIP(IP)
            DO IV=1,NIPV(IS)
               IF(IP.EQ.IPV(IS,IV)) THEN ! new vertex insertion on cap-edge
                  DO I=1,3
                     VET(I)=VERTP(IP2,I)-VERTP(IP,I)
                  END DO
                  VEN(1)=YNS(IS)*VET(3)-ZNS(IS)*VET(2)
                  VEN(2)=ZNS(IS)*VET(1)-XNS(IS)*VET(3)
                  VEN(3)=XNS(IS)*VET(2)-YNS(IS)*VET(1)
                  DMOD=(VEN(1)**2+VEN(2)**2+VEN(3)**2)**0.5
                  IF(DMOD.NE.0.0_W_P) THEN
                     DO I=1,3
                        VEN(I)=VEN(I)/DMOD
                     END DO
                  END IF
                  DO IVNEW=1,NE
                     IPNEW=IPNEW+1
                     ! new vertex location
                     DO I=1,3 
                        VE0(I)=VERTP(IP,I)+VET(I)*REAL(IVNEW,KIND=W_P)/ &
                        (REAL(NE,KIND=W_P)+1.0)
                     END DO
                     IF(DMOD.NE.0.0_W_P) THEN
                        CALL FINDBRACKETN(DD,FUNC3D,IEBRACKET,VE0,VE1,VEN)
                        IF(IEBRACKET.EQ.2) THEN 
                           VEI=VE1 
                        ELSE 
                           CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,VE0,  &
                                VE1,VEI)
                           IF(IER.EQ.1) VEI=VE1
                        END IF
                     ELSE
                        VEI=VE0
                     END IF
                     DO I=1,3
                        VERTP(IPNEW,I)=VEI(I)
                     END DO
                  END DO
                  !Arrange refined clipped face
                  IE=0        
                  DO IV2=1,NIPV(IS)                                   
                     IPV2(IS,IV2+IE)=IPV(IS,IV2)
                     IF(IPV(IS,IV2).EQ.IP2) THEN                      
                        DO I=1,NE
                           IE=IE+1
                           IPV2(IS,IV2+IE)=IPNEW-I+1
                        END DO 
                     END IF
                  END DO
                  IPV(IS,:)=IPV2(IS,:)
                  !------
                  NIPV(IS)=NIPV(IS)+NE
                  GOTO 10
               END IF
            END DO
10          CONTINUE
            
! Arrange refineed cap face
!         IPIN=IPNEW
!         DO IVISNEW=NIPV(ISNEW),1,-1
!            IPV(ISNEW,IVISNEW+NE*(IVISNEW-1))=IPV(ISNEW,IVISNEW)
!            DO IE=1,NE
!               IPV(ISNEW,IVISNEW+NE*IVISNEW-(IE-1))=IPIN
!               IPIN=IPIN-1
!            END DO
!         END DO
!         NIPV(ISNEW)=NIPV(ISNEW)*(NE+1)
      END DO
! New faces triangulation
         SUMP=0.0_W_P
         DO IV=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IV)
            DO I=1,3
               SUMP(I)=SUMP(I)+VERTP(IP,I)
            END DO
         END DO
         IPNEW=IPNEW+1 !Central vertex insertion on cap-face
         DO I=1,3
            V0(I)=SUMP(I)/NIPV(ISNEW)
         END DO
         CALL FINDBRACKET(DD,FUNC3D,IEBRACKET,V0,V1)        
         IF(IEBRACKET.EQ.2) THEN 
            VI=V1 
         ELSE 
            CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,V0,V1,VI)                   
         END IF
         IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
            VERTP(IPNEW,1)=VI(1) 
            VERTP(IPNEW,2)=VI(2) 
            VERTP(IPNEW,3)=VI(3)
         ELSE
            VERTP(IPNEW,1)=V0(1) 
            VERTP(IPNEW,2)=V0(2) 
            VERTP(IPNEW,3)=V0(3)            
         END IF
         !Vertices insertion on radial edges
         NPC=IPNEW
         DO IV=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IV)
            DO I=1,3
               VET(I)=VERTP(NPC,I)-VERTP(IP,I)
            END DO
            DO IVNEW=1,NE
               IPNEW=IPNEW+1
               ! new vertex location
               DO I=1,3 
                  V0(I)=VERTP(IP,I)+VET(I)*REAL(IVNEW,KIND=W_P)/ &
                       (REAL(NE,KIND=W_P)+1.0)
               END DO
               CALL FINDBRACKET(DD,FUNC3D,IEBRACKET,V0,V1)        
               IF(IEBRACKET.EQ.2) THEN 
                  VI=V1 
               ELSE 
                  CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,V0,V1,VI)     
               END IF
               IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
                  VERTP(IPNEW,1)=VI(1) 
                  VERTP(IPNEW,2)=VI(2) 
                  VERTP(IPNEW,3)=VI(3)
               ELSE
                  VERTP(IPNEW,1)=V0(1) 
                  VERTP(IPNEW,2)=V0(2) 
                  VERTP(IPNEW,3)=V0(3)            
               END IF               
            END DO
         END DO
         !------------------------------------
         !Triangulation
         DO IV=1,NIPV(ISNEW)
            !Control points for Triangulation
            IPT(1,1,NE+2)=IPV(ISNEW,IV)
            IF(IV.EQ.NIPV(ISNEW)) THEN
               IPT(NE+2,1,1)=IPV(ISNEW,1)
            ELSE
               IPT(NE+2,1,1)=IPV(ISNEW,IV+1)
            END IF
            IPT(1,NE+2,1)=NPC
            JV=0
            DO JU=1,NE
               JW=(NE+1)-JU-JV
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IPT(JU1,JV1,JW1)=NTPINI+(IV-1)*NE+JU
            END DO
            JU=0
            DO JV=1,NE
               JW=(NE+1)-JU-JV
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IPT(JU1,JV1,JW1)=NPC+(IV-1)*NE+JV
            END DO
            JW=0
            DO JV=1,NE
               JU=(NE+1)-JV-JW
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IF(IV.EQ.NIPV(ISNEW)) THEN
                  IPT(JU1,JV1,JW1)=NPC+JV
               ELSE
                  IPT(JU1,JV1,JW1)=NPC+IV*NE+JV
               END IF
            END DO
            DO JV=1,NE-1
               DO JU=1,NE-JV
                  JW=(NE+1)-JU-JV
                  !Insert internal points on the cap-triangle
                  IPNEW=IPNEW+1
                  JU1=JU+1
                  JV1=JV+1
                  JW1=JW+1
                  IPT(JU1,JV1,JW1)=IPNEW
                  DO I=1,3
                     VET(I)=VERTP(IPT((NE+1)-JV+1,JV1,1),I)-            &
                          VERTP(IPT(1,JV1,(NE+1)-JV+1),I)
                  END DO
                  DO I=1,3 
                     V0(I)=VERTP(IPT(1,JV1,(NE+1)-JV+1),I)+VET(I)*      &
                          REAL(JU,KIND=W_P)/(REAL(NE-JV,KIND=W_P)+1.0)
                  END DO
                  CALL FINDBRACKET(DD,FUNC3D,IEBRACKET,V0,V1)        
                  IF(IEBRACKET.EQ.2) THEN 
                     VI=V1 
                  ELSE 
                     CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,V0,V1,VI)  
                  END IF
                  IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
                     VERTP(IPNEW,1)=VI(1) 
                     VERTP(IPNEW,2)=VI(2) 
                     VERTP(IPNEW,3)=VI(3)
                  ELSE
                     VERTP(IPNEW,1)=V0(1) 
                     VERTP(IPNEW,2)=V0(2) 
                     VERTP(IPNEW,3)=V0(3)            
                  END IF                  
               END DO
            END DO

!-------------------
            DO JV=0,NE
               DO JU=0,NE-JV
                  JW=(NE+1)-JU-JV
                  JU1=JU+1
                  JV1=JV+1
                  JW1=JW+1
                  IF(JU.GT.0) THEN
                     IST=IST+1
                     IS=IST
                     NIPV(IS)=3
                     IPV(IS,1)=IPT(JU1,JV1,JW1)
                     IPV(IS,2)=IPT(JU1,JV1+1,JW1-1)
                     IPV(IS,3)=IPT(JU1-1,JV1+1,JW1)
                     XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1)       
                     YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2)       
                     ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3)       
                     XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1)       
                     YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2)       
                     ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3)       
                     XM=YV1*ZV2-ZV1*YV2 
                     YM=ZV1*XV2-XV1*ZV2 
                     ZM=XV1*YV2-YV1*XV2 
                     DMOD=(XM**2+YM**2+ZM**2)**0.5               
                     IF(DMOD.NE.0.0) THEN 
                        XNS(IS)=XM/DMOD 
                        YNS(IS)=YM/DMOD 
                        ZNS(IS)=ZM/DMOD 
                     ELSE 
                        NIPV(IS)=0 
                     END IF
                  END IF
                  IST=IST+1
                  IS=IST
                  NIPV(IS)=3
                  IPV(IS,1)=IPT(JU1,JV1,JW1)
                  IPV(IS,2)=IPT(JU1+1,JV1,JW1-1)
                  IPV(IS,3)=IPT(JU1,JV1+1,JW1-1)
                  XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1)       
                  YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2)       
                  ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3)       
                  XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1)       
                  YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2)       
                  ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3)       
                  XM=YV1*ZV2-ZV1*YV2 
                  YM=ZV1*XV2-XV1*ZV2 
                  ZM=XV1*YV2-YV1*XV2 
                  DMOD=(XM**2+YM**2+ZM**2)**0.5               
                  IF(DMOD.NE.0.0) THEN 
                     XNS(IS)=XM/DMOD 
                     YNS(IS)=YM/DMOD 
                     ZNS(IS)=ZM/DMOD 
                  ELSE 
                     NIPV(IS)=0 
                  END IF
               END DO
            END DO
         END DO
      END DO
      DO ISNEW=NTSINI+1,NTS
         NIPV(ISNEW)=0
      END DO
      NTV=NTV+IPNEW-NTP
      NTP=IPNEW
      NTS=IS
      RETURN
    END SUBROUTINE TRICAP
!-------------------------- END OF TRICAP ----------------------------c 
!---------------------------------------------------------------------c     
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              TRIMCAP                                c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! DD       = differential size                                        c 
! FCOEF    = array containing the coefficients for the multi implict  c 
!            functions definition                                     c 
! IPV      = array containing the global indices of the truncated pol.c 
!            vertices                                                 c 
! ISCFIP   = array containing the index of the clipped face           c
!            associated to each new intersection point                c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
! NIPV     = number of vertices of each face                          c 
! NS2      = size of arrays involving polyhedron faces                c
! NTP      = last global vertex index                                 c 
! NTS      = last face index of the truncated polyhedron              c 
! NTSINI   = last face index of the original polyhedron               c 
! NTV      = total number of vertices                                 c 
! NV2      = size of arrays involving polyhedron vertices             c
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! IPV      = array containing the global indices of the refined-poly. c 
!            vertices                                                 c 
! NIPV     = number of vertices of each face of the refined poly.     c 
! NTP      = last global vertex index of the refined polyhedron       c 
! NTS      = last face index of the refined polyhedron                c 
! NTV      = total number of vertices of the refined polyhedron       c 
! VERTP    = vertex coordinates of the refined polyhedron             c 
! XNS, ... = unit-lenght normals to the faces of the refined polyh.   c 
!---------------------------------------------------------------------c 
    SUBROUTINE TRIMCAP(DD,FCOEF,IPV,ISCFIP,NE,NIPV,NS2,NTP,NTS,NTSINI,  &
         NTV,NV2,VERTP,XNS,YNS,ZNS) BIND(C)
!.. Scalar Arguments                                                    
      INTEGER(I_P), INTENT(IN) :: NE, NS2, NTSINI, NV2
      INTEGER(I_P), INTENT(IN) :: ISCFIP(NV)
      REAL(W_P), INTENT(IN) :: DD
      INTEGER(I_P), INTENT(INOUT) :: NTP, NTS, NTV 
!.. Array Arguments                                                     
      INTEGER(I_P), INTENT(INOUT) :: IPV(NS2,NV2),NIPV(NS2) 
      REAL(W_P), INTENT(INOUT) :: VERTP(NV2,3),XNS(NS2),YNS(NS2),ZNS(NS2) 
      REAL(W_P), INTENT(IN) :: FCOEF(10000) 
! FCOEF(1) = number of implicit functions ('+' sign means union and
!            '-' sign means intersection)                               
! FCOEF(2) = number of terms of the implicit function 1                 
! FCOEF(3) = 0 for global system; 1 for local system                    
! FCOEF(4-6) = xyz-coordinates of the system-reference origin           
! FCOEF(7-15) = xyz-components of the normal vectors that define the    
!               orthonormal reference system                            
! FCOEF(16) = number of subterms of term 1 of the implicit function 1   
! FCOEF(17,18) = coefficient and exponent of term 1 of imp. funct. 1    
! FCOEF(19-22) = C1,C2,C3,C4 coefficients of the first subterm of term 1
!                of imp. funct. 1: C1 X^C2 Y^C3 Z^C4                    
! Follow the same pattern for the rest of information                   
!.. Local Scalars                                                       
      INTEGER(I_P) :: I,IE,IEBRACKET,IER,IP,IP2,IPNEW,IS,ISNEW,IST,IV,  &
           IV2,IVISNEW,IVNEW,JU,JU1,JV,JV1,JW,JW1,NPC,NTPINI
      REAL(W_P) :: DMOD,XM,XV1,XV2,YM,YV1,YV2,ZM,ZV1,ZV2
!.. Local Arrays
      INTEGER(I_P) :: IPT(NE+2,NE+2,NE+2),IPV2(NS2,NV2)
      REAL(W_P) :: SUMP(3),V0(3),VE0(3),V1(3),VE1(3),VEI(3),VEN(3),     &
           VET(3),VI(3)
      
      IPNEW=NTP
      IST=NTS
      DO ISNEW=NTSINI+1,NTS
         NTPINI=IPNEW
         DO IVISNEW=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IVISNEW)
            IF(IVISNEW.EQ.NIPV(ISNEW)) THEN
               IP2=IPV(ISNEW,1)
            ELSE
               IP2=IPV(ISNEW,IVISNEW+1)
            END IF
            IS=ISCFIP(IP)
            DO IV=1,NIPV(IS)
               IF(IP.EQ.IPV(IS,IV)) THEN ! new vertex insertion on cap-edge
                  DO I=1,3
                     VET(I)=VERTP(IP2,I)-VERTP(IP,I)
                  END DO
                  VEN(1)=YNS(IS)*VET(3)-ZNS(IS)*VET(2)
                  VEN(2)=ZNS(IS)*VET(1)-XNS(IS)*VET(3)
                  VEN(3)=XNS(IS)*VET(2)-YNS(IS)*VET(1)
                  DMOD=(VEN(1)**2+VEN(2)**2+VEN(3)**2)**0.5
                  IF(DMOD.NE.0.0_W_P) THEN
                     DO I=1,3
                        VEN(I)=VEN(I)/DMOD
                     END DO
                  END IF
                  DO IVNEW=1,NE
                     IPNEW=IPNEW+1
                     ! new vertex location
                     DO I=1,3 
                        VE0(I)=VERTP(IP,I)+VET(I)*REAL(IVNEW,KIND=W_P)/ &
                        (REAL(NE,KIND=W_P)+1.0)
                     END DO
                     IF(DMOD.NE.0.0_W_P) THEN
                        CALL FINDBRACKETNM(DD,FCOEF,IEBRACKET,VE0,VE1,VEN)
                        IF(IEBRACKET.EQ.2) THEN 
                           VEI=VE1 
                        ELSE 
                           CALL INTEMFUNC3D(DD*50.0_W_P,FCOEF,IER,VE0,  &
                                VE1,VEI)
                           IF(IER.EQ.1) VEI=VE1
                        END IF
                     ELSE
                        VEI=VE0
                     END IF
                     DO I=1,3
                        VERTP(IPNEW,I)=VEI(I)
                     END DO
                  END DO
                  !Arrange refined clipped face
                  IE=0        
                  DO IV2=1,NIPV(IS)                                   
                     IPV2(IS,IV2+IE)=IPV(IS,IV2)
                     IF(IPV(IS,IV2).EQ.IP2) THEN                      
                        DO I=1,NE
                           IE=IE+1
                           IPV2(IS,IV2+IE)=IPNEW-I+1
                        END DO 
                     END IF
                  END DO
                  IPV(IS,:)=IPV2(IS,:)
                  !------
                  NIPV(IS)=NIPV(IS)+NE
                  GOTO 10
               END IF
            END DO
10          CONTINUE            
      END DO
! New faces triangulation
         SUMP=0.0_W_P
         DO IV=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IV)
            DO I=1,3
               SUMP(I)=SUMP(I)+VERTP(IP,I)
            END DO
         END DO
         IPNEW=IPNEW+1 !Central vertex insertion on cap-face
         DO I=1,3
            V0(I)=SUMP(I)/NIPV(ISNEW)
         END DO
         CALL FINDBRACKETM(DD,FCOEF,IEBRACKET,V0,V1) 
         IF(IEBRACKET.EQ.2) THEN 
            VI=V1 
         ELSE 
            CALL INTEMFUNC3D(DD*50.0_W_P,FCOEF,IER,V0,V1,VI)
         END IF
         IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
            VERTP(IPNEW,1)=VI(1) 
            VERTP(IPNEW,2)=VI(2) 
            VERTP(IPNEW,3)=VI(3)
         ELSE
            VERTP(IPNEW,1)=V0(1) 
            VERTP(IPNEW,2)=V0(2) 
            VERTP(IPNEW,3)=V0(3)            
         END IF
         !Vertices insertion on radial edges
         NPC=IPNEW
         DO IV=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IV)
            DO I=1,3
               VET(I)=VERTP(NPC,I)-VERTP(IP,I)
            END DO
            DO IVNEW=1,NE
               IPNEW=IPNEW+1
               ! new vertex location
               DO I=1,3 
                  V0(I)=VERTP(IP,I)+VET(I)*REAL(IVNEW,KIND=W_P)/ &
                       (REAL(NE,KIND=W_P)+1.0)
               END DO
               CALL FINDBRACKETM(DD,FCOEF,IEBRACKET,V0,V1) 
               IF(IEBRACKET.EQ.2) THEN 
                  VI=V1 
               ELSE 
                  CALL INTEMFUNC3D(DD*50.0_W_P,FCOEF,IER,V0,V1,VI)
               END IF
               IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
                  VERTP(IPNEW,1)=VI(1) 
                  VERTP(IPNEW,2)=VI(2) 
                  VERTP(IPNEW,3)=VI(3)
               ELSE
                  VERTP(IPNEW,1)=V0(1) 
                  VERTP(IPNEW,2)=V0(2) 
                  VERTP(IPNEW,3)=V0(3)            
               END IF               
            END DO
         END DO
         !------------------------------------
         !Triangulation
         DO IV=1,NIPV(ISNEW)
            !Control points for Triangulation
            IPT(1,1,NE+2)=IPV(ISNEW,IV)
            IF(IV.EQ.NIPV(ISNEW)) THEN
               IPT(NE+2,1,1)=IPV(ISNEW,1)
            ELSE
               IPT(NE+2,1,1)=IPV(ISNEW,IV+1)
            END IF
            IPT(1,NE+2,1)=NPC
            JV=0
            DO JU=1,NE
               JW=(NE+1)-JU-JV
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IPT(JU1,JV1,JW1)=NTPINI+(IV-1)*NE+JU
            END DO
            JU=0
            DO JV=1,NE
               JW=(NE+1)-JU-JV
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IPT(JU1,JV1,JW1)=NPC+(IV-1)*NE+JV
            END DO
            JW=0
            DO JV=1,NE
               JU=(NE+1)-JV-JW
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IF(IV.EQ.NIPV(ISNEW)) THEN
                  IPT(JU1,JV1,JW1)=NPC+JV
               ELSE
                  IPT(JU1,JV1,JW1)=NPC+IV*NE+JV
               END IF
            END DO
            DO JV=1,NE-1
               DO JU=1,NE-JV
                  JW=(NE+1)-JU-JV
                  !Insert internal points on the cap-triangle
                  IPNEW=IPNEW+1
                  JU1=JU+1
                  JV1=JV+1
                  JW1=JW+1
                  IPT(JU1,JV1,JW1)=IPNEW
                  DO I=1,3
                     VET(I)=VERTP(IPT((NE+1)-JV+1,JV1,1),I)-            &
                          VERTP(IPT(1,JV1,(NE+1)-JV+1),I)
                  END DO
                  DO I=1,3 
                     V0(I)=VERTP(IPT(1,JV1,(NE+1)-JV+1),I)+VET(I)*      &
                          REAL(JU,KIND=W_P)/(REAL(NE-JV,KIND=W_P)+1.0)
                  END DO
                  CALL FINDBRACKETM(DD,FCOEF,IEBRACKET,V0,V1) 
                  IF(IEBRACKET.EQ.2) THEN 
                     VI=V1 
                  ELSE 
                     CALL INTEMFUNC3D(DD*50.0_W_P,FCOEF,IER,V0,V1,VI)
                  END IF
                  IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
                     VERTP(IPNEW,1)=VI(1) 
                     VERTP(IPNEW,2)=VI(2) 
                     VERTP(IPNEW,3)=VI(3)
                  ELSE
                     VERTP(IPNEW,1)=V0(1) 
                     VERTP(IPNEW,2)=V0(2) 
                     VERTP(IPNEW,3)=V0(3)            
                  END IF                  
               END DO
            END DO

!-------------------
            DO JV=0,NE
               DO JU=0,NE-JV
                  JW=(NE+1)-JU-JV
                  JU1=JU+1
                  JV1=JV+1
                  JW1=JW+1
                  IF(JU.GT.0) THEN
                     IST=IST+1
                     IS=IST
                     NIPV(IS)=3
                     IPV(IS,1)=IPT(JU1,JV1,JW1)
                     IPV(IS,2)=IPT(JU1,JV1+1,JW1-1)
                     IPV(IS,3)=IPT(JU1-1,JV1+1,JW1)
                     XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1)       
                     YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2)       
                     ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3)       
                     XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1)       
                     YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2)       
                     ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3)       
                     XM=YV1*ZV2-ZV1*YV2 
                     YM=ZV1*XV2-XV1*ZV2 
                     ZM=XV1*YV2-YV1*XV2 
                     DMOD=(XM**2+YM**2+ZM**2)**0.5               
                     IF(DMOD.NE.0.0) THEN 
                        XNS(IS)=XM/DMOD 
                        YNS(IS)=YM/DMOD 
                        ZNS(IS)=ZM/DMOD 
                     ELSE 
                        NIPV(IS)=0 
                     END IF
                  END IF
                  IST=IST+1
                  IS=IST
                  NIPV(IS)=3
                  IPV(IS,1)=IPT(JU1,JV1,JW1)
                  IPV(IS,2)=IPT(JU1+1,JV1,JW1-1)
                  IPV(IS,3)=IPT(JU1,JV1+1,JW1-1)
                  XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1)       
                  YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2)       
                  ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3)       
                  XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1)       
                  YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2)       
                  ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3)       
                  XM=YV1*ZV2-ZV1*YV2 
                  YM=ZV1*XV2-XV1*ZV2 
                  ZM=XV1*YV2-YV1*XV2 
                  DMOD=(XM**2+YM**2+ZM**2)**0.5               
                  IF(DMOD.NE.0.0) THEN 
                     XNS(IS)=XM/DMOD 
                     YNS(IS)=YM/DMOD 
                     ZNS(IS)=ZM/DMOD 
                  ELSE 
                     NIPV(IS)=0 
                  END IF
               END DO
            END DO
         END DO
      END DO
      DO ISNEW=NTSINI+1,NTS
         NIPV(ISNEW)=0
      END DO
      NTV=NTV+IPNEW-NTP
      NTP=IPNEW
      NTS=IS
      RETURN
    END SUBROUTINE TRIMCAP
!-------------------------- END OF TRIMCAP ---------------------------c 
!---------------------------------------------------------------------c     
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                            TOOLV3DDIM                               c 
!---------------------------------------------------------------------c 
!          This routine computes the volume of a polyhedron           c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! IPV      = array containing the global indices of the polyhedron    c 
!            vertices                                                 c 
! NIPV     = number of vertices of each face                          c 
! NS2      = size of arrays involving polyhedron faces                c
! NTS      = total number of faces                                    c 
! NV2      = size of arrays involving polyhedron vertices             c
! VERTI    = vertex coordinates of the polyhedron                     c 
! XNS, ... = unit-lenght normals to the faces of the polyhedron       c 
! On return:                                                          c 
!===========                                                          c 
! VOL      = volume of the polyhedron                                 c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
    SUBROUTINE TOOLV3DDIM(IPV,NIPV,NS2,NTS,NV2,VERTI,VOL,XNS,YNS,ZNS) &
         BIND(C) 
! .. Scalar Arguments ..                                                
      INTEGER(I_P), INTENT(IN) :: NS2,NTS,NV2 
      REAL(W_P), INTENT(OUT) :: VOL 
! .. Array Arguments ..                                                 
      INTEGER(I_P), INTENT(IN) :: IPV(NS2,NV2),NIPV(NS2) 
      REAL(W_P), INTENT(IN) :: VERTI(NV2,3),XNS(NS2),YNS(NS2),ZNS(NS2) 
! .. Local Scalars ..                                                   
      INTEGER(I_P) :: I,IH,IP,IP1,IP2,IPROJ,IS 
      REAL(W_P) :: CNMAX,DNMAX,SUMP,SUMS,TOL,XV1,XV2,YV1,YV2,ZV1,ZV2 
                                                                        
      TOL=1.0D-16 
      SUMS=0.0 
      DO 20 IS=1,NTS 
         IF(NIPV(IS).GT.0) THEN 
            SUMP=0.0 
            CNMAX=0.0 
            IF(ABS(YNS(IS)).GE.ABS(XNS(IS)).AND.ABS(YNS(IS)).GE.        &
     &           ABS(ZNS(IS))) THEN                                     
               IPROJ=2 
               DNMAX=YNS(IS) 
               IF(ABS(DNMAX).GT.TOL) CNMAX=VERTI(IPV(IS,1),2)+(XNS(IS)*&
     &           VERTI(IPV(IS,1),1)+ZNS(IS)*VERTI(IPV(IS,1),3))/DNMAX   
            ELSEIF(ABS(ZNS(IS)).GE.ABS(XNS(IS)).AND.ABS(ZNS(IS)).GE.    &
     &           ABS(YNS(IS))) THEN                                     
               IPROJ=3 
               DNMAX=ZNS(IS) 
               IF(ABS(DNMAX).GT.TOL) CNMAX=VERTI(IPV(IS,1),3)+(XNS(IS)*&
     &           VERTI(IPV(IS,1),1)+YNS(IS)*VERTI(IPV(IS,1),2))/DNMAX   
            ELSE 
               IPROJ=1 
               DNMAX=XNS(IS) 
               IF(ABS(DNMAX).GT.TOL) CNMAX=VERTI(IPV(IS,1),1)+(YNS(IS)*&
     &           VERTI(IPV(IS,1),2)+ZNS(IS)*VERTI(IPV(IS,1),3))/DNMAX   
            END IF 
            IH=INT((NIPV(IS)-2)/2) 
            DO I=2,IH+1 
               IP=2*I 
               IP1=IP-1 
               IP2=IP-2 
               IF(IPROJ.EQ.1) THEN 
                  YV1=VERTI(IPV(IS,IP1),2)-VERTI(IPV(IS,1),2) 
                  ZV1=VERTI(IPV(IS,IP1),3)-VERTI(IPV(IS,1),3) 
                  YV2=VERTI(IPV(IS,IP),2)-VERTI(IPV(IS,IP2),2) 
                  ZV2=VERTI(IPV(IS,IP),3)-VERTI(IPV(IS,IP2),3) 
                  SUMP=SUMP+YV1*ZV2-ZV1*YV2 
               ELSEIF(IPROJ.EQ.2) THEN 
                  XV1=VERTI(IPV(IS,IP1),1)-VERTI(IPV(IS,1),1) 
                  ZV1=VERTI(IPV(IS,IP1),3)-VERTI(IPV(IS,1),3) 
                  XV2=VERTI(IPV(IS,IP),1)-VERTI(IPV(IS,IP2),1) 
                  ZV2=VERTI(IPV(IS,IP),3)-VERTI(IPV(IS,IP2),3) 
                  SUMP=SUMP+ZV1*XV2-XV1*ZV2 
               ELSE 
                  XV1=VERTI(IPV(IS,IP1),1)-VERTI(IPV(IS,1),1) 
                  YV1=VERTI(IPV(IS,IP1),2)-VERTI(IPV(IS,1),2) 
                  XV2=VERTI(IPV(IS,IP),1)-VERTI(IPV(IS,IP2),1) 
                  YV2=VERTI(IPV(IS,IP),2)-VERTI(IPV(IS,IP2),2) 
                  SUMP=SUMP+XV1*YV2-YV1*XV2 
               END IF 
            END DO 
            IF(2*(IH+1).LT.NIPV(IS)) THEN 
               IF(IPROJ.EQ.1) THEN 
                  YV1=VERTI(IPV(IS,NIPV(IS)),2)-VERTI(IPV(IS,1),2) 
                  ZV1=VERTI(IPV(IS,NIPV(IS)),3)-VERTI(IPV(IS,1),3) 
                  YV2=VERTI(IPV(IS,1),2)-VERTI(IPV(IS,NIPV(IS)-1),2) 
                  ZV2=VERTI(IPV(IS,1),3)-VERTI(IPV(IS,NIPV(IS)-1),3) 
                  SUMP=SUMP+YV1*ZV2-ZV1*YV2 
               ELSEIF(IPROJ.EQ.2) THEN 
                  XV1=VERTI(IPV(IS,NIPV(IS)),1)-VERTI(IPV(IS,1),1) 
                  ZV1=VERTI(IPV(IS,NIPV(IS)),3)-VERTI(IPV(IS,1),3) 
                  XV2=VERTI(IPV(IS,1),1)-VERTI(IPV(IS,NIPV(IS)-1),1) 
                  ZV2=VERTI(IPV(IS,1),3)-VERTI(IPV(IS,NIPV(IS)-1),3) 
                  SUMP=SUMP+ZV1*XV2-XV1*ZV2 
               ELSE 
                  XV1=VERTI(IPV(IS,NIPV(IS)),1)-VERTI(IPV(IS,1),1) 
                  YV1=VERTI(IPV(IS,NIPV(IS)),2)-VERTI(IPV(IS,1),2) 
                  XV2=VERTI(IPV(IS,1),1)-VERTI(IPV(IS,NIPV(IS)-1),1) 
                  YV2=VERTI(IPV(IS,1),2)-VERTI(IPV(IS,NIPV(IS)-1),2) 
                  SUMP=SUMP+XV1*YV2-YV1*XV2 
               END IF 
            ENDIF 
            IF(ABS(DNMAX).GT.TOL) SUMS=SUMS+CNMAX*SUMP 
         END IF 
   20 END DO 
      VOL=SUMS/6.0 
      RETURN 
      END                                           
!------------------------- END OF TOOLV3DDIM -------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                             REFINECAP                               c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! DD       = differential size                                        c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! IPV      = array containing the global indices of the truncated pol.c 
!            vertices                                                 c 
! ISCFIP   = array containing the index of the clipped face           c
!            associated to each new intersection point                c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = last face index of the truncated polyhedron              c 
! NTSINI   = last face index of the original polyhedron               c 
! NTV      = total number of vertices                                 c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! IPV      = array containing the global indices of the refined-poly. c 
!            vertices                                                 c 
! NIPV     = number of vertices of each face of the refined poly.     c 
! NTP      = last global vertex index of the refined polyhedron       c 
! NTS      = last face index of the refined polyhedron                c 
! NTV      = total number of vertices of the refined polyhedron       c 
! VERTP    = vertex coordinates of the refined polyhedron             c 
! XNS, ... = unit-lenght normals to the faces of the refined polyh.   c 
!---------------------------------------------------------------------c 
    SUBROUTINE REFINECAP(DD,FUNC3D,IPV,ISCFIP,NE,NIPV,NTP,NTS,NTSINI,   &
         NTV,VERTP,XNS,YNS,ZNS) BIND(C)
!.. Scalar Arguments                                                    
      INTEGER(I_P), INTENT(IN) :: NE, NTSINI
      INTEGER(I_P), INTENT(IN) :: ISCFIP(NV)
      REAL(W_P), INTENT(IN) :: DD
      INTEGER(I_P), INTENT(INOUT) :: NTP, NTS, NTV 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(INOUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
      INTEGER(I_P), INTENT(INOUT) :: IPV(NS,NV),NIPV(NS) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      INTEGER(I_P) :: I,IE,IEBRACKET,IER,IP,IP2,IPNEW,IS,ISNEW,IST,IV,      &
           IV2,IVISNEW,IVNEW,JU,JU1,JV,JV1,JW,JW1,NPC,NTPINI
      REAL(W_P) :: DMOD,XM,XV1,XV2,YM,YV1,YV2,ZM,ZV1,ZV2
!.. Local Arrays
      INTEGER(I_P) :: IPT(NE+2,NE+2,NE+2),IPV2(NS,NV)
      REAL(W_P) :: SUMP(3),V0(3),VE0(3),V1(3),VE1(3),VEI(3),VEN(3),     &
           VET(3),VI(3)
      
      IPNEW=NTP
      IST=NTS
      DO ISNEW=NTSINI+1,NTS
         NTPINI=IPNEW
         DO IVISNEW=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IVISNEW)
            IF(IVISNEW.EQ.NIPV(ISNEW)) THEN
               IP2=IPV(ISNEW,1)
            ELSE
               IP2=IPV(ISNEW,IVISNEW+1)
            END IF
            IS=ISCFIP(IP)
            DO IV=1,NIPV(IS)
               IF(IP.EQ.IPV(IS,IV)) THEN ! new vertex insertion on cap-edge
                  DO I=1,3
                     VET(I)=VERTP(IP2,I)-VERTP(IP,I)
                  END DO
                  VEN(1)=YNS(IS)*VET(3)-ZNS(IS)*VET(2)
                  VEN(2)=ZNS(IS)*VET(1)-XNS(IS)*VET(3)
                  VEN(3)=XNS(IS)*VET(2)-YNS(IS)*VET(1)
                  DMOD=(VEN(1)**2+VEN(2)**2+VEN(3)**2)**0.5
                  IF(DMOD.NE.0.0_W_P) THEN
                     DO I=1,3
                        VEN(I)=VEN(I)/DMOD
                     END DO
                  END IF
                  DO IVNEW=1,NE
                     IPNEW=IPNEW+1
                     ! new vertex location
                     DO I=1,3 
                        VE0(I)=VERTP(IP,I)+VET(I)*REAL(IVNEW,KIND=W_P)/ &
                        (REAL(NE,KIND=W_P)+1.0)
                     END DO
                     IF(DMOD.NE.0.0_W_P) THEN
                        CALL FINDBRACKETN(DD,FUNC3D,IEBRACKET,VE0,VE1,VEN)
                        IF(IEBRACKET.EQ.2) THEN 
                           VEI=VE1 
                        ELSE 
                           CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,VE0,  &
                                VE1,VEI)
                           IF(IER.EQ.1) VEI=VE1
                        END IF
                     ELSE
                        VEI=VE0
                     END IF
                     DO I=1,3
                        VERTP(IPNEW,I)=VEI(I)
                     END DO
                  END DO
                  !Arrange refined clipped face
                  IE=0        
                  DO IV2=1,NIPV(IS)                                   
                     IPV2(IS,IV2+IE)=IPV(IS,IV2)
                     IF(IPV(IS,IV2).EQ.IP2) THEN                      
                        DO I=1,NE
                           IE=IE+1
                           IPV2(IS,IV2+IE)=IPNEW-I+1
                        END DO 
                     END IF
                  END DO
                  IPV(IS,:)=IPV2(IS,:)
                  !------
                  NIPV(IS)=NIPV(IS)+NE
                  GOTO 10
               END IF
            END DO
10          CONTINUE
            
! Arrange refineed cap face
!         IPIN=IPNEW
!         DO IVISNEW=NIPV(ISNEW),1,-1
!            IPV(ISNEW,IVISNEW+NE*(IVISNEW-1))=IPV(ISNEW,IVISNEW)
!            DO IE=1,NE
!               IPV(ISNEW,IVISNEW+NE*IVISNEW-(IE-1))=IPIN
!               IPIN=IPIN-1
!            END DO
!         END DO
!         NIPV(ISNEW)=NIPV(ISNEW)*(NE+1)
      END DO
! New faces triangulation
         SUMP=0.0_W_P
         DO IV=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IV)
            DO I=1,3
               SUMP(I)=SUMP(I)+VERTP(IP,I)
            END DO
         END DO
         IPNEW=IPNEW+1 !Central vertex insertion on cap-face
         DO I=1,3
            V0(I)=SUMP(I)/NIPV(ISNEW)
         END DO
         CALL FINDBRACKET(DD,FUNC3D,IEBRACKET,V0,V1)        
         IF(IEBRACKET.EQ.2) THEN 
            VI=V1 
         ELSE 
            CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,V0,V1,VI)                   
         END IF
         IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
            VERTP(IPNEW,1)=VI(1) 
            VERTP(IPNEW,2)=VI(2) 
            VERTP(IPNEW,3)=VI(3)
         ELSE
            VERTP(IPNEW,1)=V0(1) 
            VERTP(IPNEW,2)=V0(2) 
            VERTP(IPNEW,3)=V0(3)            
         END IF
         !Vertices insertion on radial edges
         NPC=IPNEW
         DO IV=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IV)
            DO I=1,3
               VET(I)=VERTP(NPC,I)-VERTP(IP,I)
            END DO
            DO IVNEW=1,NE
               IPNEW=IPNEW+1
               ! new vertex location
               DO I=1,3 
                  V0(I)=VERTP(IP,I)+VET(I)*REAL(IVNEW,KIND=W_P)/ &
                       (REAL(NE,KIND=W_P)+1.0)
               END DO
               CALL FINDBRACKET(DD,FUNC3D,IEBRACKET,V0,V1)        
               IF(IEBRACKET.EQ.2) THEN 
                  VI=V1 
               ELSE 
                  CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,V0,V1,VI)     
               END IF
               IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
                  VERTP(IPNEW,1)=VI(1) 
                  VERTP(IPNEW,2)=VI(2) 
                  VERTP(IPNEW,3)=VI(3)
               ELSE
                  VERTP(IPNEW,1)=V0(1) 
                  VERTP(IPNEW,2)=V0(2) 
                  VERTP(IPNEW,3)=V0(3)            
               END IF               
            END DO
         END DO
         !------------------------------------
         !Triangulation
         DO IV=1,NIPV(ISNEW)
            !Control points for Triangulation
            IPT(1,1,NE+2)=IPV(ISNEW,IV)
            IF(IV.EQ.NIPV(ISNEW)) THEN
               IPT(NE+2,1,1)=IPV(ISNEW,1)
            ELSE
               IPT(NE+2,1,1)=IPV(ISNEW,IV+1)
            END IF
            IPT(1,NE+2,1)=NPC
            JV=0
            DO JU=1,NE
               JW=(NE+1)-JU-JV
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IPT(JU1,JV1,JW1)=NTPINI+(IV-1)*NE+JU
            END DO
            JU=0
            DO JV=1,NE
               JW=(NE+1)-JU-JV
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IPT(JU1,JV1,JW1)=NPC+(IV-1)*NE+JV
            END DO
            JW=0
            DO JV=1,NE
               JU=(NE+1)-JV-JW
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IF(IV.EQ.NIPV(ISNEW)) THEN
                  IPT(JU1,JV1,JW1)=NPC+JV
               ELSE
                  IPT(JU1,JV1,JW1)=NPC+IV*NE+JV
               END IF
            END DO
            DO JV=1,NE-1
               DO JU=1,NE-JV
                  JW=(NE+1)-JU-JV
                  !Insert internal points on the cap-triangle
                  IPNEW=IPNEW+1
                  JU1=JU+1
                  JV1=JV+1
                  JW1=JW+1
                  IPT(JU1,JV1,JW1)=IPNEW
                  DO I=1,3
                     VET(I)=VERTP(IPT((NE+1)-JV+1,JV1,1),I)-            &
                          VERTP(IPT(1,JV1,(NE+1)-JV+1),I)
                  END DO
                  DO I=1,3 
                     V0(I)=VERTP(IPT(1,JV1,(NE+1)-JV+1),I)+VET(I)*      &
                          REAL(JU,KIND=W_P)/(REAL(NE-JV,KIND=W_P)+1.0)
                  END DO
                  CALL FINDBRACKET(DD,FUNC3D,IEBRACKET,V0,V1)        
                  IF(IEBRACKET.EQ.2) THEN 
                     VI=V1 
                  ELSE 
                     CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,V0,V1,VI) 
                  END IF
                  IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
                     VERTP(IPNEW,1)=VI(1) 
                     VERTP(IPNEW,2)=VI(2) 
                     VERTP(IPNEW,3)=VI(3)
                  ELSE
                     VERTP(IPNEW,1)=V0(1) 
                     VERTP(IPNEW,2)=V0(2) 
                     VERTP(IPNEW,3)=V0(3)            
                  END IF                  
               END DO
            END DO

!-------------------
            DO JV=0,NE
               DO JU=0,NE-JV
                  JW=(NE+1)-JU-JV
                  JU1=JU+1
                  JV1=JV+1
                  JW1=JW+1
                  IF(JU.GT.0) THEN
                     IST=IST+1
                     IS=IST
                     NIPV(IS)=3
                     IPV(IS,1)=IPT(JU1,JV1,JW1)
                     IPV(IS,2)=IPT(JU1,JV1+1,JW1-1)
                     IPV(IS,3)=IPT(JU1-1,JV1+1,JW1)
                     XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1)       
                     YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2)       
                     ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3)       
                     XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1)       
                     YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2)       
                     ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3)       
                     XM=YV1*ZV2-ZV1*YV2 
                     YM=ZV1*XV2-XV1*ZV2 
                     ZM=XV1*YV2-YV1*XV2 
                     DMOD=(XM**2+YM**2+ZM**2)**0.5               
                     IF(DMOD.NE.0.0) THEN 
                        XNS(IS)=XM/DMOD 
                        YNS(IS)=YM/DMOD 
                        ZNS(IS)=ZM/DMOD 
                     ELSE 
                        NIPV(IS)=0 
                     END IF
                  END IF
                  IST=IST+1
                  IS=IST
                  NIPV(IS)=3
                  IPV(IS,1)=IPT(JU1,JV1,JW1)
                  IPV(IS,2)=IPT(JU1+1,JV1,JW1-1)
                  IPV(IS,3)=IPT(JU1,JV1+1,JW1-1)
                  XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1)       
                  YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2)       
                  ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3)       
                  XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1)       
                  YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2)       
                  ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3)       
                  XM=YV1*ZV2-ZV1*YV2 
                  YM=ZV1*XV2-XV1*ZV2 
                  ZM=XV1*YV2-YV1*XV2 
                  DMOD=(XM**2+YM**2+ZM**2)**0.5               
                  IF(DMOD.NE.0.0) THEN 
                     XNS(IS)=XM/DMOD 
                     YNS(IS)=YM/DMOD 
                     ZNS(IS)=ZM/DMOD 
                  ELSE 
                     NIPV(IS)=0 
                  END IF
               END DO
            END DO
         END DO
      END DO
      DO ISNEW=NTSINI+1,NTS
         NIPV(ISNEW)=0
      END DO
      NTV=NTV+IPNEW-NTP
      NTP=IPNEW
      NTS=IS
      RETURN
    END SUBROUTINE REFINECAP
!------------------------- END OF REFINECAP --------------------------c 
!---------------------------------------------------------------------c     
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                             REFINECAP_bak                               c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! DD       = differential size                                        c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! IPV      = array containing the global indices of the truncated pol.c 
!            vertices                                                 c 
! ISCFIP   = array containing the index of the clipped face           c
!            associated to each new intersection point                c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
!            superimposed Cartesian grid                              c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = last face index of the truncated polyhedron              c 
! NTSINI   = last face index of the original polyhedron               c 
! NTV      = total number of vertices                                 c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! IPV      = array containing the global indices of the refined-poly. c 
!            vertices                                                 c 
! NIPV     = number of vertices of each face of the refined poly.     c 
! NTP      = last global vertex index of the refined polyhedron       c 
! NTS      = last face index of the refined polyhedron                c 
! NTV      = total number of vertices of the refined polyhedron       c 
! VERTP    = vertex coordinates of the refined polyhedron             c 
! XNS, ... = unit-lenght normals to the faces of the refined polyh.   c 
!---------------------------------------------------------------------c 
    SUBROUTINE REFINECAP_bak(DD,FUNC3D,IPV,ISCFIP,NE,NIPV,NTP,NTS,NTSINI,   &
         NTV,VERTP,XNS,YNS,ZNS) BIND(C)
!.. Scalar Arguments                                                    
      INTEGER(I_P), INTENT(IN) :: NE, NTSINI
      INTEGER(I_P), INTENT(IN) :: ISCFIP(NV)
      REAL(W_P), INTENT(IN) :: DD
      INTEGER(I_P), INTENT(INOUT) :: NTP, NTS, NTV 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(INOUT) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
      INTEGER(I_P), INTENT(INOUT) :: IPV(NS,NV),NIPV(NS) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      INTEGER(I_P) :: I,IE,IEBRACKET,IER,IP,IP2,IPIN,IPNEW,IS,ISNEW,IV, &
           IV2,IVISNEW,IVNEW
      REAL(W_P) :: DMOD,XM,XV1,XV2,YM,YV1,YV2,ZM,ZV1,ZV2
!.. Local Arrays
      INTEGER(I_P) :: IPV2(NS,NV)
      REAL(W_P) :: SUMP(3),V0(3),VE0(3),V1(3),VE1(3),VEI(3),VEN(3),     &
           VET(3),VI(3)
      
      IPNEW=NTP
      DO ISNEW=NTSINI+1,NTS
         DO IVISNEW=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IVISNEW)
            IF(IVISNEW.EQ.NIPV(ISNEW)) THEN
               IP2=IPV(ISNEW,1)
            ELSE
               IP2=IPV(ISNEW,IVISNEW+1)
            END IF
            IS=ISCFIP(IP)
            DO IV=1,NIPV(IS)
               IF(IP.EQ.IPV(IS,IV)) THEN ! new vertex insertion
!                  DO IV2=1,NIPV(IS)-IV
!                     IPV(IS,NIPV(IS)+IV2)=IPV(IS,IV+IV2)
!                  END DO
                  DO I=1,3
                     VET(I)=VERTP(IP2,I)-VERTP(IP,I)
                  END DO
                  VEN(1)=YNS(IS)*VET(3)-ZNS(IS)*VET(2)
                  VEN(2)=ZNS(IS)*VET(1)-XNS(IS)*VET(3)
                  VEN(3)=XNS(IS)*VET(2)-YNS(IS)*VET(1)
                  DMOD=(VEN(1)**2+VEN(2)**2+VEN(3)**2)**0.5
                  IF(DMOD.NE.0.0_W_P) THEN
                     DO I=1,3
                        VEN(I)=VEN(I)/DMOD
                     END DO
                  END IF
                  DO IVNEW=1,NE
                     IPNEW=IPNEW+1
!                     IPV(IS,IV+IVNEW)=IPNEW
                     ! new vertex location
                     DO I=1,3 
                        VE0(I)=VERTP(IP,I)+VET(I)*REAL(IVNEW,KIND=W_P)/ &
                        (REAL(NE,KIND=W_P)+1.0)
                     END DO
                     IF(DMOD.NE.0.0_W_P) THEN
                        CALL FINDBRACKETN(DD,FUNC3D,IEBRACKET,VE0,VE1,VEN)
                        IF(IEBRACKET.EQ.2) THEN 
                           VEI=VE1 
                        ELSE 
                           CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,VE0,  &
                                VE1,VEI)
                           IF(IER.EQ.1) VEI=VE1
                        END IF
                     ELSE
                        VEI=VE0
                     END IF
                     DO I=1,3
                        VERTP(IPNEW,I)=VEI(I)
                     END DO
                  END DO
                  !------
                  IE=0        
                  DO IV2=1,NIPV(IS)                                   
                     IPV2(IS,IV2+IE)=IPV(IS,IV2)
                     IF(IPV(IS,IV2).EQ.IP2) THEN                      
                        DO I=1,NE
                           IE=IE+1
                           IPV2(IS,IV2+IE)=IPNEW-I+1
                        END DO 
                     END IF
                  END DO
                  IPV(IS,:)=IPV2(IS,:)
                  !------
                  NIPV(IS)=NIPV(IS)+NE
                  GOTO 10
               END IF
            END DO
10          CONTINUE
         END DO
! Arrange refine-cap face
         IPIN=IPNEW
         DO IVISNEW=NIPV(ISNEW),1,-1
            IPV(ISNEW,IVISNEW+NE*(IVISNEW-1))=IPV(ISNEW,IVISNEW)
            DO IE=1,NE
               IPV(ISNEW,IVISNEW+NE*IVISNEW-(IE-1))=IPIN
               IPIN=IPIN-1
            END DO
         END DO
         NIPV(ISNEW)=NIPV(ISNEW)*(NE+1)
      END DO
! New faces triangulation
      IS=NTS
      DO ISNEW=NTSINI+1,NTS
         SUMP=0.0_W_P
         DO IV=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IV)
            DO I=1,3
               SUMP(I)=SUMP(I)+VERTP(IP,I)
            END DO
         END DO
         IPNEW=IPNEW+1
         DO I=1,3
            V0(I)=SUMP(I)/NIPV(ISNEW)
         END DO
         CALL FINDBRACKET(DD,FUNC3D,IEBRACKET,V0,V1)        
         IF(IEBRACKET.EQ.2) THEN 
            VI=V1 
         ELSE 
            CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IER,V0,V1,VI)                   
         END IF
         IF(IER.EQ.0.OR.IEBRACKET.EQ.2)THEN 
            VERTP(IPNEW,1)=VI(1) 
            VERTP(IPNEW,2)=VI(2) 
            VERTP(IPNEW,3)=VI(3)
         ELSE
            VERTP(IPNEW,1)=V0(1) 
            VERTP(IPNEW,2)=V0(2) 
            VERTP(IPNEW,3)=V0(3)            
         END IF
         !Triangulation
         DO IV=1,NIPV(ISNEW)
            IS=IS+1
            IP=IPV(ISNEW,IV)
            IF(IV.EQ.NIPV(ISNEW)) THEN
               IP2=IPV(ISNEW,1)
            ELSE
               IP2=IPV(ISNEW,IV+1)
            END IF
            NIPV(IS)=3 
            IPV(IS,1)=IPNEW 
            IPV(IS,2)=IP
            IPV(IS,3)=IP2 
            XV1=VERTP(IP,1)-VERTP(IPNEW,1)       
            YV1=VERTP(IP,2)-VERTP(IPNEW,2)       
            ZV1=VERTP(IP,3)-VERTP(IPNEW,3)       
            XV2=VERTP(IP2,1)-VERTP(IP,1)       
            YV2=VERTP(IP2,2)-VERTP(IP,2)       
            ZV2=VERTP(IP2,3)-VERTP(IP,3)       
            XM=YV1*ZV2-ZV1*YV2 
            YM=ZV1*XV2-XV1*ZV2 
            ZM=XV1*YV2-YV1*XV2 
            DMOD=(XM**2+YM**2+ZM**2)**0.5               
            IF(DMOD.NE.0.0) THEN 
               XNS(IS)=XM/DMOD 
               YNS(IS)=YM/DMOD 
               ZNS(IS)=ZM/DMOD 
            ELSE 
               NIPV(IS)=0 
            END IF            
         END DO
      END DO
      DO ISNEW=NTSINI+1,NTS
         NIPV(ISNEW)=0
      END DO
      NTV=NTV+IPNEW-NTP
      NTP=IPNEW
      NTS=IS
      RETURN
    END SUBROUTINE REFINECAP_bak
!------------------------- END OF REFINECAP_bak --------------------------c 
!---------------------------------------------------------------------c     
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                               TRIVOL                                c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! V1,V2,V3 = coordinates of the three triangle vertices               c 
! On return:                                                          c 
!===========                                                          c 
! VOLTRI   = Gaussian quadrature volume                               c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE TRIVOL(FUNC3D,V1,V2,V3,VOLTRI) BIND(C) 
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(OUT) :: VOLTRI 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: V1(3),V2(3),V3(3) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: A,D,DD,DMOD,F0,S,T,W,X,XMAX,XMIN,XN,XNU,XV1,XV2,   &
     &     Y,YMAX,YMIN,YN,YNU,YV1,YV2,Z,ZMAX,ZMIN,ZN,ZNU,ZV1,ZV2  
      INTEGER(I_P) :: IE,IEBRACKET,IGAUSS,IN,IORDER,NGAUSS 
!.. Local Arrays                                                        
      REAL(W_P) :: P0(3),P1(3),PI(3),SGAUSS(10),TGAUSS(10),WGAUSS(10) 
      XMAX=MAX(V1(1),V2(1),V3(1)) 
      XMIN=MIN(V1(1),V2(1),V3(1)) 
      YMAX=MAX(V1(2),V2(2),V3(2)) 
      YMIN=MIN(V1(2),V2(2),V3(2)) 
      ZMAX=MAX(V1(3),V2(3),V3(3)) 
      ZMIN=MIN(V1(3),V2(3),V3(3)) 
      DD=0.1*MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN) 
!. Gauss quadrature points                                              
!. [Pavel Solin, Karel Segeth, Ivo Dolezel, Higher-order finite element 
!. methods, Chapman & Hall, CRC, Boca Raton, 2004]                      
                                ! Parece que el orden 2 es suficiente   
      IORDER=2 
      IF(IORDER.EQ.2) THEN 
         NGAUSS=3 
         SGAUSS(1)=1./6.0 
         TGAUSS(1)=1./6.0 
         SGAUSS(2)=2./3.0 
         TGAUSS(2)=1./6.0 
         SGAUSS(3)=1./6.0 
         TGAUSS(3)=2./3.0 
         WGAUSS(1)=1./3. 
         WGAUSS(2)=1./3. 
         WGAUSS(3)=1./3. 
      ELSEIF(IORDER.EQ.3) THEN 
         NGAUSS=4 
         SGAUSS(1)=1./3. 
         TGAUSS(1)=1./3. 
         SGAUSS(2)=1./5. 
         TGAUSS(2)=3./5. 
         SGAUSS(3)=1./5. 
         TGAUSS(3)=1./5. 
         SGAUSS(4)=3./5. 
         TGAUSS(4)=1./5. 
         WGAUSS(1)=-27./48. 
         WGAUSS(2)=25./48. 
         WGAUSS(3)=25./48. 
         WGAUSS(4)=25./48. 
      ELSEIF(IORDER.EQ.4) THEN 
         NGAUSS=6 
         SGAUSS(1)=(1.0-0.108103018168070)/2. 
         TGAUSS(1)=(1.0-0.108103018168070)/2. 
         SGAUSS(2)=(1.0-0.108103018168070)/2. 
         TGAUSS(2)=(1.0-0.783793963663860)/2. 
         SGAUSS(3)=(1.0-0.783793963663860)/2. 
         TGAUSS(3)=(1.0-0.108103018168070)/2. 
         SGAUSS(4)=(1.0-0.816847572980458)/2. 
         TGAUSS(4)=(1.0-0.816847572980458)/2. 
         SGAUSS(5)=(1.0-0.816847572980458)/2. 
         TGAUSS(5)=(1.0+0.633695145960918)/2. 
         SGAUSS(6)=(1.0+0.633695145960918)/2. 
         TGAUSS(6)=(1.0-0.816847572980458)/2. 
         WGAUSS(1)=0.446763179356022/2. 
         WGAUSS(2)=WGAUSS(1) 
         WGAUSS(3)=WGAUSS(1) 
         WGAUSS(4)=0.219903487310644/2. 
         WGAUSS(5)=WGAUSS(4) 
         WGAUSS(6)=WGAUSS(4) 
      ELSEIF(IORDER.EQ.5) THEN 
         NGAUSS=7 
         SGAUSS(1)=1./3. 
         TGAUSS(1)=1./3. 
         SGAUSS(2)=(1.0-0.059715871789770)/2. 
         TGAUSS(2)=(1.0-0.059715871789770)/2. 
         SGAUSS(3)=(1.0-0.059715871789770)/2. 
         TGAUSS(3)=(1.0-0.880568256420460)/2. 
         SGAUSS(4)=(1.0-0.880568256420460)/2. 
         TGAUSS(4)=(1.0-0.059715871789770)/2. 
         SGAUSS(5)=(1.0-0.797426985353088)/2. 
         TGAUSS(5)=(1.0-0.797426985353088)/2. 
         SGAUSS(6)=(1.0-0.797426985353088)/2. 
         TGAUSS(6)=(1.0+0.594853970706174)/2. 
         SGAUSS(7)=(1.0+0.594853970706174)/2. 
         TGAUSS(7)=(1.0-0.797426985353088)/2. 
         WGAUSS(1)=0.225 
         WGAUSS(2)=0.264788305577012/2. 
         WGAUSS(3)=WGAUSS(2) 
         WGAUSS(4)=WGAUSS(2) 
         WGAUSS(5)=0.251878361089654/2. 
         WGAUSS(6)=WGAUSS(5) 
         WGAUSS(7)=WGAUSS(5) 
      END IF 
!. Vector normal to the triangle                                        
      XV1=V2(1)-V1(1) 
      YV1=V2(2)-V1(2) 
      ZV1=V2(3)-V1(3) 
      XV2=V3(1)-V1(1) 
      YV2=V3(2)-V1(2) 
      ZV2=V3(3)-V1(3) 
      XN=YV1*ZV2-ZV1*YV2 
      YN=ZV1*XV2-XV1*ZV2 
      ZN=XV1*YV2-YV1*XV2 
      DMOD=(XN**2+YN**2+ZN**2)**0.5 
!      write(6,*)'Triangle area:',A                                     
!. Unit-length normal vector                                            
      IF(DMOD.NE.0.0) THEN 
         XNU=XN/DMOD 
         YNU=YN/DMOD 
         ZNU=ZN/DMOD 
      ELSE 
         VOLTRI=0.0 
         RETURN 
      END IF 
!. Triangle area                                                        
      A=DMOD/2D0 
!. Projection plane: IN=1: YZ, IN=2: XZ, IN=3: XY                       
      IF((ABS(XN).GE.ABS(YN)).AND.(ABS(XN).GE.ABS(ZN))) THEN 
         IN=1 
      ELSEIF((ABS(YN).GE.ABS(XN)).AND.(ABS(YN).GE.ABS(ZN))) THEN 
         IN=2 
      ELSE 
         IN=3 
      END IF 
!      write(6,*)'----IN',IN,XN,YN,ZN                                   
      VOLTRI=0.0 
! Local reference sistem (S,T), GAUSS WEIGHT W                          
      DO IGAUSS=1,NGAUSS 
         S=SGAUSS(IGAUSS) 
         T=TGAUSS(IGAUSS) 
         W=WGAUSS(IGAUSS) 
                                ! YZ                                    
         IF(IN.EQ.1) THEN 
            Y=V1(2)+(V2(2)-V1(2))*S+(V3(2)-V1(2))*T 
            Z=V1(3)+(V2(3)-V1(3))*S+(V3(3)-V1(3))*T 
            X=V1(1)+YNU*(V1(2)-Y)/XNU+ZNU*(V1(3)-Z)/XNU 
                                ! XZ                                    
         ELSEIF(IN.EQ.2) THEN 
            X=V1(1)+(V2(1)-V1(1))*S+(V3(1)-V1(1))*T 
            Z=V1(3)+(V2(3)-V1(3))*S+(V3(3)-V1(3))*T 
            Y=V1(2)+XNU*(V1(1)-X)/YNU+ZNU*(V1(3)-Z)/YNU 
                                ! XY                                    
         ELSE 
            X=V1(1)+(V2(1)-V1(1))*S+(V3(1)-V1(1))*T 
            Y=V1(2)+(V2(2)-V1(2))*S+(V3(2)-V1(2))*T 
            Z=V1(3)+XNU*(V1(1)-X)/ZNU+YNU*(V1(2)-Y)/ZNU 
         END IF 
         P0(1)=X 
         P0(2)=Y 
         P0(3)=Z 
         CALL FINDBRACKET(DD,FUNC3D,IEBRACKET,P0,P1) 
         IF(IEBRACKET.EQ.2) THEN 
            PI=P1 
         ELSE 
            CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IE,P0,P1,PI) 
         END IF 
         F0=FUNC3D(X,Y,Z) 
         IF(IE.EQ.0) THEN 
            D=SIGN(((X-PI(1))**2+(Y-PI(2))**2+(Z-PI(3))**2)**0.5,F0) 
            VOLTRI=VOLTRI+W*D*A 
         ELSE 
            VOLTRI=VOLTRI+W*F0*A 
         ENDIF 
      END DO 
      RETURN 
      END                                           
!------------------------ END OF  TRIVOL -----------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                             TRIVOLP                                 c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! CPARAB   = local paraboloid coefficients                            c
! VN       = paraboloid orthonormal basis                             c
! V1,V2,V3 = coordinates of the three triangle vertices               c 
! On return:                                                          c 
!===========                                                          c 
! VOLTRI   = Gaussian quadrature volume                               c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE TRIVOLP(CPARAB,VN,V1,V2,V3,VOLTRI) BIND(C) 
        !.. Scalar Arguments                                                    
        REAL(W_P), INTENT(OUT) :: VOLTRI 
        !.. Array Arguments                                                     
        REAL(W_P), INTENT(IN) :: CPARAB(12),V1(3),V2(3),V3(3),VN(9) 
        !.. Local Scalars                                                       
        REAL(W_P) :: A,D,DD,DMOD,F0,S,T,W,X,XMAX,XMIN,XN,XNU,XV1,XV2,   &
             Y,YMAX,YMIN,YN,YNU,YV1,YV2,Z,ZMAX,ZMIN,ZN,ZNU,ZV1,ZV2  
        INTEGER(I_P) :: IE,IEBRACKET,IGAUSS,IN,IORDER,NGAUSS 
        !.. Local Arrays                                                        
        REAL(W_P) :: P0(3),P1(3),PI(3),SGAUSS(10),TGAUSS(10),WGAUSS(10) 
        XMAX=MAX(V1(1),V2(1),V3(1)) 
        XMIN=MIN(V1(1),V2(1),V3(1)) 
        YMAX=MAX(V1(2),V2(2),V3(2)) 
        YMIN=MIN(V1(2),V2(2),V3(2)) 
        ZMAX=MAX(V1(3),V2(3),V3(3)) 
        ZMIN=MIN(V1(3),V2(3),V3(3)) 
        DD=0.1*MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN) 
        !. Gauss quadrature points                                              
        !. [Pavel Solin, Karel Segeth, Ivo Dolezel, Higher-order finite element 
        !. methods, Chapman & Hall, CRC, Boca Raton, 2004]                      
        ! Parece que el orden 2 es suficiente   
        IORDER=2 
        IF(IORDER.EQ.2) THEN 
           NGAUSS=3 
           SGAUSS(1)=1./6.0 
           TGAUSS(1)=1./6.0 
           SGAUSS(2)=2./3.0 
           TGAUSS(2)=1./6.0 
           SGAUSS(3)=1./6.0 
           TGAUSS(3)=2./3.0 
           WGAUSS(1)=1./3. 
           WGAUSS(2)=1./3. 
           WGAUSS(3)=1./3. 
        ELSEIF(IORDER.EQ.3) THEN 
           NGAUSS=4 
           SGAUSS(1)=1./3. 
           TGAUSS(1)=1./3. 
           SGAUSS(2)=1./5. 
           TGAUSS(2)=3./5. 
           SGAUSS(3)=1./5. 
           TGAUSS(3)=1./5. 
           SGAUSS(4)=3./5. 
           TGAUSS(4)=1./5. 
           WGAUSS(1)=-27./48. 
           WGAUSS(2)=25./48. 
           WGAUSS(3)=25./48. 
           WGAUSS(4)=25./48. 
        ELSEIF(IORDER.EQ.4) THEN 
           NGAUSS=6 
           SGAUSS(1)=(1.0-0.108103018168070)/2. 
           TGAUSS(1)=(1.0-0.108103018168070)/2. 
           SGAUSS(2)=(1.0-0.108103018168070)/2. 
           TGAUSS(2)=(1.0-0.783793963663860)/2. 
           SGAUSS(3)=(1.0-0.783793963663860)/2. 
           TGAUSS(3)=(1.0-0.108103018168070)/2. 
           SGAUSS(4)=(1.0-0.816847572980458)/2. 
           TGAUSS(4)=(1.0-0.816847572980458)/2. 
           SGAUSS(5)=(1.0-0.816847572980458)/2. 
           TGAUSS(5)=(1.0+0.633695145960918)/2. 
           SGAUSS(6)=(1.0+0.633695145960918)/2. 
           TGAUSS(6)=(1.0-0.816847572980458)/2. 
           WGAUSS(1)=0.446763179356022/2. 
           WGAUSS(2)=WGAUSS(1) 
           WGAUSS(3)=WGAUSS(1) 
           WGAUSS(4)=0.219903487310644/2. 
           WGAUSS(5)=WGAUSS(4) 
           WGAUSS(6)=WGAUSS(4) 
        ELSEIF(IORDER.EQ.5) THEN 
           NGAUSS=7 
           SGAUSS(1)=1./3. 
           TGAUSS(1)=1./3. 
           SGAUSS(2)=(1.0-0.059715871789770)/2. 
           TGAUSS(2)=(1.0-0.059715871789770)/2. 
           SGAUSS(3)=(1.0-0.059715871789770)/2. 
           TGAUSS(3)=(1.0-0.880568256420460)/2. 
           SGAUSS(4)=(1.0-0.880568256420460)/2. 
           TGAUSS(4)=(1.0-0.059715871789770)/2. 
           SGAUSS(5)=(1.0-0.797426985353088)/2. 
           TGAUSS(5)=(1.0-0.797426985353088)/2. 
           SGAUSS(6)=(1.0-0.797426985353088)/2. 
           TGAUSS(6)=(1.0+0.594853970706174)/2. 
           SGAUSS(7)=(1.0+0.594853970706174)/2. 
           TGAUSS(7)=(1.0-0.797426985353088)/2. 
           WGAUSS(1)=0.225 
           WGAUSS(2)=0.264788305577012/2. 
           WGAUSS(3)=WGAUSS(2) 
           WGAUSS(4)=WGAUSS(2) 
           WGAUSS(5)=0.251878361089654/2. 
           WGAUSS(6)=WGAUSS(5) 
           WGAUSS(7)=WGAUSS(5) 
        END IF
        !. Vector normal to the triangle                                        
        XV1=V2(1)-V1(1) 
        YV1=V2(2)-V1(2) 
        ZV1=V2(3)-V1(3) 
        XV2=V3(1)-V1(1) 
        YV2=V3(2)-V1(2) 
        ZV2=V3(3)-V1(3) 
        XN=YV1*ZV2-ZV1*YV2 
        YN=ZV1*XV2-XV1*ZV2 
        ZN=XV1*YV2-YV1*XV2 
        DMOD=(XN**2+YN**2+ZN**2)**0.5 
        !. Unit-length normal vector                                            
        IF(DMOD.NE.0.0) THEN 
           XNU=XN/DMOD 
           YNU=YN/DMOD 
           ZNU=ZN/DMOD 
        ELSE 
           VOLTRI=0.0 
           RETURN 
        END IF
        !. Triangle area                                                        
        A=DMOD/2D0 
        !. Projection plane: IN=1: YZ, IN=2: XZ, IN=3: XY                       
        IF((ABS(XN).GE.ABS(YN)).AND.(ABS(XN).GE.ABS(ZN))) THEN 
           IN=1 
        ELSEIF((ABS(YN).GE.ABS(XN)).AND.(ABS(YN).GE.ABS(ZN))) THEN 
           IN=2 
        ELSE 
           IN=3 
        END IF
        VOLTRI=0.0 
        ! Local reference sistem (S,T), GAUSS WEIGHT W                          
        DO IGAUSS=1,NGAUSS 
           S=SGAUSS(IGAUSS) 
           T=TGAUSS(IGAUSS) 
           W=WGAUSS(IGAUSS) 
           ! YZ                                    
           IF(IN.EQ.1) THEN 
              Y=V1(2)+(V2(2)-V1(2))*S+(V3(2)-V1(2))*T 
              Z=V1(3)+(V2(3)-V1(3))*S+(V3(3)-V1(3))*T 
              X=V1(1)+YNU*(V1(2)-Y)/XNU+ZNU*(V1(3)-Z)/XNU 
              ! XZ                                    
           ELSEIF(IN.EQ.2) THEN 
              X=V1(1)+(V2(1)-V1(1))*S+(V3(1)-V1(1))*T 
              Z=V1(3)+(V2(3)-V1(3))*S+(V3(3)-V1(3))*T 
              Y=V1(2)+XNU*(V1(1)-X)/YNU+ZNU*(V1(3)-Z)/YNU 
              ! XY                                    
           ELSE 
              X=V1(1)+(V2(1)-V1(1))*S+(V3(1)-V1(1))*T 
              Y=V1(2)+(V2(2)-V1(2))*S+(V3(2)-V1(2))*T 
              Z=V1(3)+XNU*(V1(1)-X)/ZNU+YNU*(V1(2)-Y)/ZNU 
           END IF
           P0(1)=X 
           P0(2)=Y 
           P0(3)=Z 
           CALL FINDBRACKETP(CPARAB,VN,DD,IEBRACKET,P0,P1)
           IF(IEBRACKET.EQ.2) THEN 
              PI=P1 
           ELSEIF(IEBRACKET.EQ.1) THEN
              CALL INTEPFUNC3D(CPARAB,VN,P0,P1,PI)
           ELSE
              PI=P0
           END IF
           CALL PFUNC3D(F0,CPARAB,VN,X,Y,Z)
!           IF(IE.EQ.0) THEN 
              D=SIGN(((X-PI(1))**2+(Y-PI(2))**2+(Z-PI(3))**2)**0.5,F0) 
              VOLTRI=VOLTRI+W*D*A 
!           ELSE 
!              VOLTRI=VOLTRI+W*F0*A 
!           ENDIF
        END DO
        RETURN 
      END SUBROUTINE TRIVOLP
!------------------------ END OF  TRIVOLP ----------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              TRIVOLM                                c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FCOEF    = array containing the coefficients for the multi implict  c 
!            functions definition                                     c 
! V1,V2,V3 = coordinates of the three triangle vertices               c 
! On return:                                                          c 
!===========                                                          c 
! VOLTRI   = Gaussian quadrature volume                               c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE TRIVOLM(FCOEF,V1,V2,V3,VOLTRI) BIND(C) 
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(OUT) :: VOLTRI 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: V1(3),V2(3),V3(3) 
      REAL(W_P), INTENT(IN) :: FCOEF(10000) 
! FCOEF(1) = number of implicit functions ('+' sign means union and
!            '-' sign means intersection)                               
! FCOEF(2) = 2, index position of FCOEF where the information if the    
!            implicit function 1 begins                                 
! FCOEF(3) = 0 for global system; 1 for local system                    
! FCOEF(4-6) = xyz-coordinates of the system-reference origin           
! FCOEF(7-15) = xyz-components of the normal vectors that define the    
!               orthonormal reference system                            
! FCOEF(16-19) = C1,C2,C3,C4 coeficients of the first term of the       
!                implicit function 1: C1 X^C2 Y^C3 Z^C4                 
! Follow the same pattern for the rest of information                   
!.. Local Scalars                                                       
      REAL(W_P) :: A,D,DD,DMOD,F0,S,T,W,X,XMAX,XMIN,XN,XNU,XV1,XV2, &
     &     Y,YMAX,YMIN,YN,YNU,YV1,YV2,Z,ZMAX,ZMIN,ZN,ZNU,ZV1,ZV2      
      INTEGER(I_P) :: IE,IEBRACKET,IGAUSS,IN,IORDER,NGAUSS 
!.. Local Arrays                                                        
      REAL(W_P) :: P0(3),P1(3),PI(3),SGAUSS(10),TGAUSS(10),WGAUSS(10) 
      XMAX=MAX(V1(1),V2(1),V3(1)) 
      XMIN=MIN(V1(1),V2(1),V3(1)) 
      YMAX=MAX(V1(2),V2(2),V3(2)) 
      YMIN=MIN(V1(2),V2(2),V3(2)) 
      ZMAX=MAX(V1(3),V2(3),V3(3)) 
      ZMIN=MIN(V1(3),V2(3),V3(3)) 
      DD=0.1*MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN) 
!. Gauss quadrature points                                              
!. [Pavel Solin, Karel Segeth, Ivo Dolezel, Higher-order finite element 
!. methods, Chapman & Hall, CRC, Boca Raton, 2004]                      
                                ! Parece que el orden 2 es suficiente   
      IORDER=2 
      IF(IORDER.EQ.2) THEN 
         NGAUSS=3 
         SGAUSS(1)=1./6.0 
         TGAUSS(1)=1./6.0 
         SGAUSS(2)=2./3.0 
         TGAUSS(2)=1./6.0 
         SGAUSS(3)=1./6.0 
         TGAUSS(3)=2./3.0 
         WGAUSS(1)=1./3. 
         WGAUSS(2)=1./3. 
         WGAUSS(3)=1./3. 
      ELSEIF(IORDER.EQ.3) THEN 
         NGAUSS=4 
         SGAUSS(1)=1./3. 
         TGAUSS(1)=1./3. 
         SGAUSS(2)=1./5. 
         TGAUSS(2)=3./5. 
         SGAUSS(3)=1./5. 
         TGAUSS(3)=1./5. 
         SGAUSS(4)=3./5. 
         TGAUSS(4)=1./5. 
         WGAUSS(1)=-27./48. 
         WGAUSS(2)=25./48. 
         WGAUSS(3)=25./48. 
         WGAUSS(4)=25./48. 
      ELSEIF(IORDER.EQ.4) THEN 
         NGAUSS=6 
         SGAUSS(1)=(1.0-0.108103018168070)/2. 
         TGAUSS(1)=(1.0-0.108103018168070)/2. 
         SGAUSS(2)=(1.0-0.108103018168070)/2. 
         TGAUSS(2)=(1.0-0.783793963663860)/2. 
         SGAUSS(3)=(1.0-0.783793963663860)/2. 
         TGAUSS(3)=(1.0-0.108103018168070)/2. 
         SGAUSS(4)=(1.0-0.816847572980458)/2. 
         TGAUSS(4)=(1.0-0.816847572980458)/2. 
         SGAUSS(5)=(1.0-0.816847572980458)/2. 
         TGAUSS(5)=(1.0+0.633695145960918)/2. 
         SGAUSS(6)=(1.0+0.633695145960918)/2. 
         TGAUSS(6)=(1.0-0.816847572980458)/2. 
         WGAUSS(1)=0.446763179356022/2. 
         WGAUSS(2)=WGAUSS(1) 
         WGAUSS(3)=WGAUSS(1) 
         WGAUSS(4)=0.219903487310644/2. 
         WGAUSS(5)=WGAUSS(4) 
         WGAUSS(6)=WGAUSS(4) 
      ELSEIF(IORDER.EQ.5) THEN 
         NGAUSS=7 
         SGAUSS(1)=1./3. 
         TGAUSS(1)=1./3. 
         SGAUSS(2)=(1.0-0.059715871789770)/2. 
         TGAUSS(2)=(1.0-0.059715871789770)/2. 
         SGAUSS(3)=(1.0-0.059715871789770)/2. 
         TGAUSS(3)=(1.0-0.880568256420460)/2. 
         SGAUSS(4)=(1.0-0.880568256420460)/2. 
         TGAUSS(4)=(1.0-0.059715871789770)/2. 
         SGAUSS(5)=(1.0-0.797426985353088)/2. 
         TGAUSS(5)=(1.0-0.797426985353088)/2. 
         SGAUSS(6)=(1.0-0.797426985353088)/2. 
         TGAUSS(6)=(1.0+0.594853970706174)/2. 
         SGAUSS(7)=(1.0+0.594853970706174)/2. 
         TGAUSS(7)=(1.0-0.797426985353088)/2. 
         WGAUSS(1)=0.225 
         WGAUSS(2)=0.264788305577012/2. 
         WGAUSS(3)=WGAUSS(2) 
         WGAUSS(4)=WGAUSS(2) 
         WGAUSS(5)=0.251878361089654/2. 
         WGAUSS(6)=WGAUSS(5) 
         WGAUSS(7)=WGAUSS(5) 
      END IF 
!. Vector normal to the triangle                                        
      XV1=V2(1)-V1(1) 
      YV1=V2(2)-V1(2) 
      ZV1=V2(3)-V1(3) 
      XV2=V3(1)-V1(1) 
      YV2=V3(2)-V1(2) 
      ZV2=V3(3)-V1(3) 
      XN=YV1*ZV2-ZV1*YV2 
      YN=ZV1*XV2-XV1*ZV2 
      ZN=XV1*YV2-YV1*XV2 
      DMOD=(XN**2+YN**2+ZN**2)**0.5 
!. Unit-length normal vector                                            
      IF(DMOD.NE.0.0) THEN 
         XNU=XN/DMOD 
         YNU=YN/DMOD 
         ZNU=ZN/DMOD 
      ELSE 
         VOLTRI=0.0 
         RETURN 
      END IF 
!. Triangle area                                                        
      A=DMOD/2D0 
!. Projection plane: IN=1: YZ, IN=2: XZ, IN=3: XY                       
      IF((ABS(XN).GE.ABS(YN)).AND.(ABS(XN).GE.ABS(ZN))) THEN 
         IN=1 
      ELSEIF((ABS(YN).GE.ABS(XN)).AND.(ABS(YN).GE.ABS(ZN))) THEN 
         IN=2 
      ELSE 
         IN=3 
      END IF 
      VOLTRI=0.0 
! Local reference sistem (S,T), GAUSS WEIGHT W                          
      DO IGAUSS=1,NGAUSS 
         S=SGAUSS(IGAUSS) 
         T=TGAUSS(IGAUSS) 
         W=WGAUSS(IGAUSS) 
                                ! YZ                                    
         IF(IN.EQ.1) THEN 
            Y=V1(2)+(V2(2)-V1(2))*S+(V3(2)-V1(2))*T 
            Z=V1(3)+(V2(3)-V1(3))*S+(V3(3)-V1(3))*T 
            X=V1(1)+YNU*(V1(2)-Y)/XNU+ZNU*(V1(3)-Z)/XNU 
                                ! XZ                                    
         ELSEIF(IN.EQ.2) THEN 
            X=V1(1)+(V2(1)-V1(1))*S+(V3(1)-V1(1))*T 
            Z=V1(3)+(V2(3)-V1(3))*S+(V3(3)-V1(3))*T 
            Y=V1(2)+XNU*(V1(1)-X)/YNU+ZNU*(V1(3)-Z)/YNU 
                                ! XY                                    
         ELSE 
            X=V1(1)+(V2(1)-V1(1))*S+(V3(1)-V1(1))*T 
            Y=V1(2)+(V2(2)-V1(2))*S+(V3(2)-V1(2))*T 
            Z=V1(3)+XNU*(V1(1)-X)/ZNU+YNU*(V1(2)-Y)/ZNU 
         END IF 
         P0(1)=X 
         P0(2)=Y 
         P0(3)=Z 
         CALL FINDBRACKETM(DD,FCOEF,IEBRACKET,P0,P1) 
         IF(IEBRACKET.EQ.2) THEN 
            PI=P1 
         ELSE 
            CALL INTEMFUNC3D(DD*50.0_W_P,FCOEF,IE,P0,P1,PI) 
         END IF 
         CALL MFUNC3D(F0,FCOEF,X,Y,Z) 
         IF(IE.EQ.0) THEN 
            D=SIGN(((X-PI(1))**2+(Y-PI(2))**2+(Z-PI(3))**2)**0.5,F0) 
            VOLTRI=VOLTRI+W*D*A 
         ELSE 
            VOLTRI=VOLTRI+W*F0*A 
         ENDIF 
      END DO 
      RETURN 
      END                                           
!------------------------ END OF  TRIVOLM ----------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                               INTPV3D                               c 
! Volume of intersection between a paraboloid and an arbitrary        c
! polyhedron                                                          c
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! CPARAB   = local paraboloid coefficients                            c
! IPV      = array containing the global indices of the original pol. c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! NTV      = total number of vertices                                 c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! VF       = volume of intersection                                   c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE INTPV3D(CPARAB,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VF,    &
           XNS,YNS,ZNS) BIND(C)                                         
!.. Scalar Arguments                                                    
        REAL (W_P), INTENT(IN) :: CPARAB(12)
        REAL(W_P), INTENT(OUT) :: VF 
        INTEGER(I_P), INTENT(IN) :: NC, NE, NTP, NTS, NTV 
!.. Array Arguments                                                     
        REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
        INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
!.. Local Scalars                                                       
      REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DMOD,DX,DY,DZ,EPSILON,F0,F1,F2,  &
           F3,F4,F5,F6,TOLRF,VOLF,VOLTRI,X,XM,XMAX,XMIN,XP,XV1,XV2,Y,YM,&
           YMAX,YMIN,YP,YV1,YV2,Z,ZM,ZMAX,ZMIN,ZP,ZV1,ZV2        
      INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IE,IEBRACKET,IP,IP0,IP1,IRF,   &
           IRFC,IS,IS2,ISINI,IV,IV2,JC,KC,NCL,NS2,NSDIM,NTP0,NTP1,NTP2, &
           NTPA,NTPINI,NTPT,NTS0,NTS1,NTS2,NTSA,NTST,NTSINI,NTV0,NTV1,  &
           NTV2,NTVA,NTVT,NV2,NVDIM
!.. Local Arrays                                                        
      REAL(W_P) :: CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC*5),    &
           CX2(NC*5),CY1(NC*5),CY2(NC*5),CZ1(NC*5),CZ2(NC*5),PHIV(NV),  &
           PHIVMIN(NS),V0(3),V1(3),V2(3),V3(3),VI(3),VERTP0(NV,3),      &
           VERTP1(NV,3),VERTP2(NV,3),VERTPT(NV,3),VN(9),XNS0(NS),       &
           XNS1(NS),XNS2(NS),XNST(NS),YNS0(NS),YNS1(NS),YNS2(NS),       &
           YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),ZNST(NS)         
      INTEGER(I_P) :: IA(NV),ICHECK(NV),IPIA0(NV),IPIA1(NV),            &
           IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),ISCFIP(NV),  &
           ISCONTN(NS),ISCONTP(NS),NIPV0(NS),NIPV1(NS),NIPV2(NS),       &
           NIPVT(NS)
!.. Local Allocatable Arrays
      INTEGER(I_P), ALLOCATABLE, DIMENSION (:) :: NIPVA
      INTEGER(I_P), ALLOCATABLE, DIMENSION (:,:) :: IPVA
      REAL(W_P), ALLOCATABLE, DIMENSION (:) :: XNSA,YNSA,ZNSA
      REAL(W_P), ALLOCATABLE, DIMENSION (:,:) :: VERTPA
!.. Coordinate extremes of the cell and vertex tagging                  
      NCL=NC 
      VF=0.0 
      XMIN=1.0E+20_W_P 
      XMAX=-1.0E+20_W_P 
      YMIN=1.0E+20_W_P 
      YMAX=-1.0E+20_W_P 
      ZMIN=1.0E+20_W_P 
      ZMAX=-1.0E+20_W_P 
      ICONTP=0 
      ICONTN=0 
      V0(1)=0.0_W_P 
      V0(2)=0.0_W_P 
      V0(3)=0.0_W_P 
      DO IP=1,NTP 
         ICHECK(IP)=0 
      END DO
      !Paraboloid orthonormal basis
      VN(1)=CPARAB(7) 
      VN(2)=CPARAB(8) 
      VN(3)=CPARAB(9) 
      VN(4)=VN(2)
      VN(5)=-VN(1)
      VN(6)=0.0_W_P
      DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
      IF(DMOD.NE.0.0_W_P) THEN
         VN(4)=VN(4)/DMOD
         VN(5)=VN(5)/DMOD
      ELSE
         VN(4)=VN(3)
         VN(5)=0.0_W_P
         VN(6)=-VN(1)
         DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
         VN(4)=VN(4)/DMOD
         VN(6)=VN(6)/DMOD
      END IF
      VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
      VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
      VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
      
      DO IS=1,NTS
         ISCONTP(IS)=0
         ISCONTN(IS)=0
         PHIVMIN(IS)=1.0E+20_W_P
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(ICHECK(IP).EQ.0) THEN 
               ICHECK(IP)=1 
               XP=VERTP(IP,1) 
               YP=VERTP(IP,2) 
               ZP=VERTP(IP,3) 
!               V0(1)=V0(1)+XP 
!               V0(2)=V0(2)+YP 
!               V0(3)=V0(3)+ZP 
               XMIN=DMIN1(XMIN,XP) 
               XMAX=DMAX1(XMAX,XP) 
               YMIN=DMIN1(YMIN,YP) 
               YMAX=DMAX1(YMAX,YP) 
               ZMIN=DMIN1(ZMIN,ZP) 
               ZMAX=DMAX1(ZMAX,ZP)
               IF(NC.EQ.1) THEN
                  CALL PFUNC3D(PHIV(IP),CPARAB,VN,XP,YP,ZP)
                  IF(PHIV(IP).GT.0.0_W_P) THEN 
                     IA(IP)=1 
                     ICONTP=ICONTP+1 
                  ELSE 
                     IA(IP)=0 
                     ICONTN=ICONTN+1 
                  END IF
               END IF
            END IF 
!            IF(PHIV(IP).GT.0.0_W_P) THEN 
!               ISCONTP(IS)=ISCONTP(IS)+1 
!            ELSE 
!               ISCONTN(IS)=ISCONTN(IS)+1 
!            END IF
!            PHIVMIN(IS)=MIN(PHIVMIN(IS),ABS(PHIV(IP)))
         END DO
      END DO 
!.. initialization                                                      
      DX=XMAX-XMIN 
      DY=YMAX-YMIN 
      DZ=ZMAX-ZMIN 
      DD=0.01*MIN(DX,DY,DZ)
      IF(DD.LT.1.0E-20_W_P) THEN
         VF=0._W_P 
         RETURN 
      END IF
!      TOLRF=0.01_W_P*MAX(DX,DY,DZ)
!      IRF=0
!      DO IS=1,NTS
!         IF(PHIVMIN(IS).LT.TOLRF.AND.(ISCONTP(IS).EQ.0.OR.ISCONTN(IS)   &
!              .EQ.0)) THEN
!            IRFC=0
!            DO IV=1,NIPV(IS)
!               IP=IPV(IS,IV)
!               IF(ABS(PHIV(IP)).LT.TOLRF) THEN
!                  IRFC=IRFC+1
!                  IF(IRFC.EQ.2) THEN
!                     IRF=1
!                     GOTO 10
!                  END IF
!               END IF
!            END DO
!         END IF
!      END DO
!10    CONTINUE
!      EPSILON=MAX(DX,DY,DZ)*TOL 
!      V0(1)=V0(1)/(ICONTP+ICONTN) 
!      V0(2)=V0(2)/(ICONTP+ICONTN) 
!      V0(3)=V0(3)/(ICONTP+ICONTN) 
!      CALL PFUNC3D(F0,CPARAB,VN,V0(1),V0(2),V0(3))
!      CALL PFUNC3D(F1,CPARAB,VN,V0(1)+DX/2._W_P+EPSILON,V0(2),V0(3))
!      CALL PFUNC3D(F2,CPARAB,VN,V0(1)-DX/2._W_P-EPSILON,V0(2),V0(3))
!      CALL PFUNC3D(F3,CPARAB,VN,V0(1),V0(2)+DY/2._W_P+EPSILON,V0(3))
!      CALL PFUNC3D(F4,CPARAB,VN,V0(1),V0(2)-DY/2._W_P-EPSILON,V0(3))
!      CALL PFUNC3D(F5,CPARAB,VN,V0(1),V0(2),V0(3)+DZ/2._W_P+EPSILON)
!      CALL PFUNC3D(F6,CPARAB,VN,V0(1),V0(2),V0(3)-DZ/2._W_P-EPSILON)
!      IF(IRF.EQ.0.AND.(ICONTP.EQ.0.AND.MAX(F0,F1,F2,F3,F4,F5,F6).GT.    &
!           0.0_W_P).OR.(ICONTN.EQ.0.AND.MIN(F0,F1,F2,F3,F4,F5,F6).LT.   &
!           0.0_W_P)) IRF=1
!      IF(IRF.EQ.0.AND.ICONTP.EQ.0) THEN   
!         VF=0._W_P 
!         RETURN 
!      END IF
!      IF(IRF.EQ.0.AND.ICONTN.EQ.0) THEN 
!         CALL TOOLV3D(IPV,NIPV,NTS,VERTP,VF,XNS,YNS,ZNS)
!         RETURN 
!      END IF
      CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,            &
           NTS,NTVT,NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)
!      IF(IRF.EQ.1) NCL=5*NC
      NV2=NV+10*NE*(NE+5)/2
      NS2=NS+10*(NE+1)*(NE+1)
      ALLOCATE(IPVA(NS2,NV2))
      ALLOCATE(NIPVA(NS2))
      ALLOCATE(VERTPA(NV2,3))
      ALLOCATE(XNSA(NS2))
      ALLOCATE(YNSA(NS2))
      ALLOCATE(ZNSA(NS2))

      DDX=DX/NCL 
      DDY=DY/NCL 
      DDZ=DZ/NCL 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CX1(I)=-XMIN 
         ELSE 
            CX1(I)=CX1(I-1)-DDX 
         END IF
         CX2(I)=-CX1(I)+DDX 
      END DO
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CY1(I)=-YMIN 
         ELSE 
            CY1(I)=CY1(I-1)-DDY 
         END IF 
         CY2(I)=-CY1(I)+DDY 
      END DO 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CZ1(I)=-ZMIN 
         ELSE 
            CZ1(I)=CZ1(I-1)-DDZ 
         END IF 
         CZ2(I)=-CZ1(I)+DDZ 
      END DO 
      DO IC=1,NCL 
         IF(NCL.EQ.1) THEN 
            CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,  &
                 NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,ZNS0, &
                 ZNST)                                                  
         ELSE 
            CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,  &
                 NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,ZNS2, &
                 ZNST)                                                  
         END IF
         IF(IC.GT.1) CALL INTE3D(CX1(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
              NTS2,NTV2,VERTP2,1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)        
         IF(IC.LT.NCL) CALL INTE3D(CX2(IC),ICONTN,ICONTP,IPV2,NIPV2,    &
              NTP2,NTS2,NTV2,VERTP2,-1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)  
         DO JC=1,NCL 
            IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,    &
                 NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,XNS2, &
                 YNS1,YNS2,ZNS1,ZNS2)                                   
            IF(JC.GT.1) CALL INTE3D(CY1(JC),ICONTN,ICONTP,IPV1,NIPV1,   &
                 NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,1.0D0,YNS1,0.0D0,ZNS1)
            IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
               IF(JC.LT.NCL) CALL INTE3D(CY2(JC),ICONTN,ICONTP,IPV1,    &
                    NIPV1,NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,-1.0D0,YNS1, &
                    0.0D0,ZNS1)                                         
               IF(ICONTP.NE.0) THEN 
                  DO KC=1,NCL 
                     IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0, &
                          NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,   &
                          VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                     IF(KC.GT.1) CALL INTE3D(CZ1(KC),ICONTN,ICONTP,IPV0,&
                          NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,XNS0,0.0D0, &
                          YNS0,1.0D0,ZNS0)                              
                     IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                        IF(KC.LT.NCL) CALL INTE3D(CZ2(KC),ICONTN,ICONTP,&
                             IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,    &
                             XNS0,0.0D0,YNS0,-1.0D0,ZNS0)               
                        IF(ICONTP.NE.0) THEN 
                           !..   Subcell determination by truncation  
                           IF(NCL.GT.1) THEN 
                              ICONTP=0 
                              ICONTN=0 
                              DO IP=1,NTP0 
                                 ICHECK(IP)=0 
                              END DO
                              DO IS=1,NTS0 
                                 DO IV=1,NIPV0(IS) 
                                    IP=IPV0(IS,IV) 
                                    IF(ICHECK(IP).EQ.0) THEN 
                                       ICHECK(IP)=1 
                                       X=VERTP0(IP,1) 
                                       Y=VERTP0(IP,2) 
                                       Z=VERTP0(IP,3) 
                                       CALL PFUNC3D(PHIV(IP),CPARAB,VN, &
                                            X,Y,Z)
                                       IF(PHIV(IP).GT.0.0_W_P) THEN 
                                          IA(IP)=1 
                                          ICONTP=ICONTP+1 
                                       ELSE 
                                          IA(IP)=0 
                                          ICONTN=ICONTN+1 
                                       END IF
                                    END IF
                                 END DO
                              END DO
                           END IF
                           IF(ICONTN.EQ.0) THEN 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
                                   VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                              NTSINI=NTS0
                              NTPINI=NTP0
                              CALL NEWPOLCF3D(IA,IPIA0,IPIA1,IPV0,      &
                                   ISCFIP,NIPV0,NTP0,NTS0,NTV0)
                              !.. Location of the new intersection points   
                              IF(NTS0.GT.NTSINI) THEN 
                                 IS=NTS0 
                                 IS2=NTS0
                                 NSDIM=NTS0
                                 NVDIM=NTP0
                                 DO IS=NTSINI+1,NTS0
                                    NSDIM=NSDIM+NIPV0(IS)*(NE+1)**2
                                    NVDIM=NVDIM+NIPV0(IS)*(2*NE+MAX(0,  &
                                         (NE-1)*NE/2))+1
                                    DO IV=1,NIPV0(IS) 
                                       IP=IPV0(IS,IV) 
                                       IP0=IPIA0(IP) 
                                       IP1=IPIA1(IP) 
                                       V0(1)=VERTP0(IP0,1) 
                                       V0(2)=VERTP0(IP0,2) 
                                       V0(3)=VERTP0(IP0,3) 
                                       V1(1)=VERTP0(IP1,1) 
                                       V1(2)=VERTP0(IP1,2) 
                                       V1(3)=VERTP0(IP1,3)
                                       CALL INTEPFUNC3D(CPARAB,VN,V0,V1,&
                                            VI)
                                       VERTP0(IP,1)=VI(1) 
                                       VERTP0(IP,2)=VI(2) 
                                       VERTP0(IP,3)=VI(3) 
                                    END DO
                                 END DO
                                 !Refine cap
                                 IF(NVDIM.GT.NV2.OR.NSDIM.GT.NS2) THEN
                                    DEALLOCATE(IPVA,NIPVA,VERTPA,XNSA,  &
                                         YNSA,ZNSA)
                                    NV2=NVDIM
                                    NS2=NSDIM
                                    ALLOCATE(IPVA(NS2,NV2))
                                    ALLOCATE(NIPVA(NS2))
                                    ALLOCATE(VERTPA(NV2,3))
                                    ALLOCATE(XNSA(NS2))
                                    ALLOCATE(YNSA(NS2))
                                    ALLOCATE(ZNSA(NS2))
                                 END IF
                                 NTSA=NTS0 
                                 NTVA=NTV0 
                                 NTPA=NTP0 
                                 DO IP=1,NTP0 
                                    DO I=1,3 
                                       VERTPA(IP,I)=VERTP0(IP,I) 
                                    END DO
                                 END DO
                                 DO IS=1,NTS0 
                                    XNSA(IS)=XNS0(IS) 
                                    YNSA(IS)=YNS0(IS) 
                                    ZNSA(IS)=ZNS0(IS) 
                                    NIPVA(IS)=NIPV0(IS) 
                                    DO IV=1,NIPV0(IS) 
                                       IPVA(IS,IV)=IPV0(IS,IV) 
                                    END DO
                                 END DO
                                 CALL TRIPCAP(CPARAB,VN,DD/REAL(NCL,    &
                                      KIND=W_P),IPVA,ISCFIP,NE,NIPVA,   &
                                      NS2,NTPA,NTSA,NTSINI,NTVA,NV2,    &
                                      VERTPA,XNSA,YNSA,ZNSA)
                                 DO IS2=NTSINI+1,NTSA
                                    IF(NIPVA(IS2).GT.0) THEN
!..   Gauss quadrature volumes                                          
                                       V1(1)=VERTPA(IPVA(IS2,1),1) 
                                       V1(2)=VERTPA(IPVA(IS2,1),2) 
                                       V1(3)=VERTPA(IPVA(IS2,1),3) 
                                       V2(1)=VERTPA(IPVA(IS2,2),1) 
                                       V2(2)=VERTPA(IPVA(IS2,2),2) 
                                       V2(3)=VERTPA(IPVA(IS2,2),3) 
                                       V3(1)=VERTPA(IPVA(IS2,3),1) 
                                       V3(2)=VERTPA(IPVA(IS2,3),2) 
                                       V3(3)=VERTPA(IPVA(IS2,3),3) 
                                       CALL TRIVOLP(CPARAB,VN,V1,V2,V3, &
                                            VOLTRI)
                                       VF=VF+VOLTRI
                                    END IF
                                 END DO
                                 
                                 CALL TOOLV3DDIM(IPVA,NIPVA,NS2,NTSA,   &
                                      NV2,VERTPA,VOLF,XNSA,YNSA,ZNSA) 
                                 VF=VF+VOLF 
                              END IF
                           END IF
                        END IF
                     END IF
                  END DO
               END IF
            END IF
         END DO
      END DO
      !VF=VF
      DEALLOCATE(IPVA,NIPVA,VERTPA,XNSA,YNSA,ZNSA)
      RETURN 
    END SUBROUTINE INTPV3D
!------------------------- END OF INTPV3D ----------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              INTPV3DPA_bak2                              c 
! Polyhedral approximation of the volume of intersection between a    c
! paraboloid and an arbitrary polyhedron                              c
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! CPARAB   = local paraboloid coefficients                            c
! IPV      = array containing the global indices of the original pol. c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! NTV      = total number of vertices                                 c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! VF       = volume of intersection                                   c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
    SUBROUTINE INTPV3DPA_bak2(CPARAB,IPV,NC,NIPV,NTP,NTS,NTV,VERTP,VF,XNS, &
         YNS,ZNS) BIND(C)                                         
!.. Scalar Arguments                                                    
        REAL (W_P), INTENT(IN) :: CPARAB(12)
        REAL(W_P), INTENT(OUT) :: VF 
        INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
!.. Array Arguments                                                     
        REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
        INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
!.. Local Scalars                                                       
      REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DMOD,DX,DY,DZ,E,EPSILON,F0,F1,F2,&
           F3,F4,F5,F6,PHI,SUMX,SUMY,SUMZ,TOLRF,TOLPHI,VOLF,VOLTRI,X,XM,&
           XMAX,XMAX2,XMIN,XMIN2,XP,XV1,XV2,Y,YM,YMAX,YMAX2,YMIN,YMIN2, &
           YP,YV1,YV2,Z,ZM,ZMAX,ZMAX2,ZMIN,ZMIN2,ZP,ZV1,ZV2
      INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IE,IEBRACKET,ILIM1,ILIM2,IP,   &
           IP0,IP1,IRF,IRFC,IS,IS2,ISINI,IV,IV2,JC,JLIM1,JLIM2,JS,KC,   &
           KLIM1,KLIM2,NCL,NS2,NSDIM,NTP0,NTP1,NTP2,NTPA,NTPINI,NTPT,   &
           NTS0,NTS1,NTS2,NTSA,NTST,NTSINI,NTV0,NTV1,NTV2,NTVA,NTVT,NV2,&
           NVDIM
!.. Local Arrays                                                        
      REAL(W_P) :: BOX(6),CI1(NC),CI2(NC),CJ1(NC),CJ2(NC),CK1(NC),      &
           CK2(NC),CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC),      &
           CX2(NC),CY1(NC),CY2(NC),CZ1(NC),CZ2(NC),PHIV(NV),PHIVMIN(NS),&
           V0(3),V1(3),V2(3),V3(3),VI(3),VNI(3),VNJ(3),VNK(3),          &
           VERTP0(NV,3),VERTP1(NV,3),VERTP2(NV,3),VERTPT(NV,3),VN(9),   &
           XNS0(NS),XNS1(NS),XNS2(NS),XNST(NS),YNS0(NS),YNS1(NS),       &
           YNS2(NS),YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),ZNST(NS)         
      INTEGER(I_P) :: IA(NV),ICHECK(NV),IJKCLIM(6),IPIA0(NV),IPIA1(NV), &
           IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),ISCFIP(NV),  &
           ISCONTN(NS),ISCONTP(NS),ISCUT(NS),NIPV0(NS),NIPV1(NS),       &
           NIPV2(NS),NIPVT(NS)
      TOLPHI=1.0E-16_W_P
!.. Coordinate extremes of the cell and vertex tagging                  
      NCL=NC 
      VF=0.0 
      XMIN=1.0E+20_W_P 
      XMAX=-1.0E+20_W_P 
      YMIN=1.0E+20_W_P 
      YMAX=-1.0E+20_W_P 
      ZMIN=1.0E+20_W_P 
      ZMAX=-1.0E+20_W_P 
      ICONTP=0 
      ICONTN=0 
      V0(1)=0.0_W_P 
      V0(2)=0.0_W_P 
      V0(3)=0.0_W_P 
      DO IP=1,NTP 
         ICHECK(IP)=0 
      END DO
      !Paraboloid orthonormal basis
      VN(1)=CPARAB(7) 
      VN(2)=CPARAB(8) 
      VN(3)=CPARAB(9) 
      VN(4)=VN(2)
      VN(5)=-VN(1)
      VN(6)=0.0_W_P
      DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
      IF(DMOD.NE.0.0_W_P) THEN
         VN(4)=VN(4)/DMOD
         VN(5)=VN(5)/DMOD
      ELSE
         VN(4)=VN(3)
         VN(5)=0.0_W_P
         VN(6)=-VN(1)
         DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
         VN(4)=VN(4)/DMOD
         VN(6)=VN(6)/DMOD
      END IF
      VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
      VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
      VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
      
      DO IS=1,NTS
         ISCONTP(IS)=0
         ISCONTN(IS)=0
         PHIVMIN(IS)=1.0E+20_W_P
         CS(IS)=-XNS(IS)*VERTP(IPV(IS,1),1)-YNS(IS)*VERTP(IPV(IS,1),2)- &
              ZNS(IS)*VERTP(IPV(IS,1),3)
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(ICHECK(IP).EQ.0) THEN 
               ICHECK(IP)=1 
               XP=VERTP(IP,1) 
               YP=VERTP(IP,2) 
               ZP=VERTP(IP,3) 
               XMIN=DMIN1(XMIN,XP) 
               XMAX=DMAX1(XMAX,XP) 
               YMIN=DMIN1(YMIN,YP) 
               YMAX=DMAX1(YMAX,YP) 
               ZMIN=DMIN1(ZMIN,ZP) 
               ZMAX=DMAX1(ZMAX,ZP)
               IF(NC.EQ.1) THEN
                  CALL PFUNC3D(PHIV(IP),CPARAB,VN,XP,YP,ZP)
                  IF(PHIV(IP).GT.0.0_W_P) THEN 
                     IA(IP)=1 
                     ICONTP=ICONTP+1 
                  ELSE 
                     IA(IP)=0 
                     ICONTN=ICONTN+1 
                  END IF
               END IF
            END IF 
         END DO
      END DO 
!.. initialization                                                      
      DX=XMAX-XMIN 
      DY=YMAX-YMIN 
      DZ=ZMAX-ZMIN 
      DD=0.01*MIN(DX,DY,DZ)
      IF(DD.LT.1.0E-20_W_P) THEN
         VF=0._W_P 
         RETURN 
      END IF
      CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,            &
           NTS,NTVT,NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)

      DDX=DX/NCL 
      DDY=DY/NCL 
      DDZ=DZ/NCL 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CX1(I)=-XMIN 
         ELSE 
            CX1(I)=CX1(I-1)-DDX 
         END IF
         CX2(I)=-CX1(I)+DDX 
      END DO
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CY1(I)=-YMIN 
         ELSE 
            CY1(I)=CY1(I-1)-DDY 
         END IF 
         CY2(I)=-CY1(I)+DDY 
      END DO 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CZ1(I)=-ZMIN 
         ELSE 
            CZ1(I)=CZ1(I-1)-DDZ 
         END IF 
         CZ2(I)=-CZ1(I)+DDZ 
      END DO
      !. truncation limits
      BOX(1)=XMIN
      BOX(2)=XMAX
      BOX(3)=YMIN
      BOX(4)=YMAX
      BOX(5)=ZMIN
      BOX(6)=ZMAX
      E=2.0_W_P*CPARAB(4)*(1.0_W_P+CPARAB(3)**2)+2.0_W_P*CPARAB(6)*(    &
           1.0_W_P+CPARAB(2)**2)-2.0_W_P*CPARAB(2)*CPARAB(3)*CPARAB(5)
      IF(NCL.GT.1.AND.CPARAB(4)*CPARAB(6).GT.0.0_W_P.AND.E.GT.0.0_W_P)  &
           THEN
         CALL INTPLIM(BOX,CPARAB,IJKCLIM,NCL,VN)
         IF((IJKCLIM(2)-IJKCLIM(1)).LT.(IJKCLIM(4)-IJKCLIM(3)).AND.     &
              (IJKCLIM(2)-IJKCLIM(1)).LT.(IJKCLIM(6)-IJKCLIM(5))) THEN
            ILIM1=IJKCLIM(1)
            ILIM2=IJKCLIM(2)
            VNI(:)=[1.0_W_P,0.0_W_P,0.0_W_P]
            CI1(:)=CX1(:)
            CI2(:)=CX2(:)
            IF((IJKCLIM(4)-IJKCLIM(3)).LT.(IJKCLIM(6)-IJKCLIM(5))) THEN
               JLIM1=IJKCLIM(3)
               JLIM2=IJKCLIM(4)
               VNJ(:)=[0.0_W_P,1.0_W_P,0.0_W_P]
               CJ1(:)=CY1(:)
               CJ2(:)=CY2(:)
               KLIM1=IJKCLIM(5)
               KLIM2=IJKCLIM(6)
               VNK(:)=[0.0_W_P,0.0_W_P,1.0_W_P]
               CK1(:)=CZ1(:)
               CK2(:)=CZ2(:)
            ELSE
               JLIM1=IJKCLIM(5)
               JLIM2=IJKCLIM(6)
               VNJ(:)=[0.0_W_P,0.0_W_P,1.0_W_P]
               CJ1(:)=CZ1(:)
               CJ2(:)=CZ2(:)
               KLIM1=IJKCLIM(3)
               KLIM2=IJKCLIM(4)
               VNK(:)=[0.0_W_P,1.0_W_P,0.0_W_P]
               CK1(:)=CY1(:)
               CK2(:)=CY2(:)
            ENDIF
         ELSEIF((IJKCLIM(4)-IJKCLIM(3)).LT.(IJKCLIM(2)-IJKCLIM(1)).AND. &
              (IJKCLIM(4)-IJKCLIM(3)).LT.(IJKCLIM(6)-IJKCLIM(5))) THEN
            ILIM1=IJKCLIM(3)
            ILIM2=IJKCLIM(4)
            VNI(:)=[0.0_W_P,1.0_W_P,0.0_W_P]
            CI1(:)=CY1(:)
            CI2(:)=CY2(:)
            IF((IJKCLIM(2)-IJKCLIM(1)).LT.(IJKCLIM(6)-IJKCLIM(5))) THEN
               JLIM1=IJKCLIM(1)
               JLIM2=IJKCLIM(2)
               VNJ(:)=[1.0_W_P,0.0_W_P,0.0_W_P]
               CJ1(:)=CX1(:)
               CJ2(:)=CX2(:)
               KLIM1=IJKCLIM(5)
               KLIM2=IJKCLIM(6)
               VNK(:)=[0.0_W_P,0.0_W_P,1.0_W_P]
               CK1(:)=CZ1(:)
               CK2(:)=CZ2(:)
            ELSE
               JLIM1=IJKCLIM(5)
               JLIM2=IJKCLIM(6)
               VNJ(:)=[0.0_W_P,0.0_W_P,1.0_W_P]
               CJ1(:)=CZ1(:)
               CJ2(:)=CZ2(:)
               KLIM1=IJKCLIM(1)
               KLIM2=IJKCLIM(2)
               VNK(:)=[1.0_W_P,0.0_W_P,0.0_W_P]
               CK1(:)=CX1(:)
               CK2(:)=CX2(:)
            ENDIF
         ELSE
            ILIM1=IJKCLIM(5)
            ILIM2=IJKCLIM(6)
            VNI(:)=[0.0_W_P,0.0_W_P,1.0_W_P]
            CI1(:)=CZ1(:)
            CI2(:)=CZ2(:)
            IF((IJKCLIM(2)-IJKCLIM(1)).LT.(IJKCLIM(4)-IJKCLIM(3))) THEN
               JLIM1=IJKCLIM(1)
               JLIM2=IJKCLIM(2)
               VNJ(:)=[1.0_W_P,0.0_W_P,0.0_W_P]
               CJ1(:)=CX1(:)
               CJ2(:)=CX2(:)
               KLIM1=IJKCLIM(3)
               KLIM2=IJKCLIM(4)
               VNK(:)=[0.0_W_P,1.0_W_P,0.0_W_P]
               CK1(:)=CY1(:)
               CK2(:)=CY2(:)
            ELSE
               JLIM1=IJKCLIM(3)
               JLIM2=IJKCLIM(4)
               VNJ(:)=[0.0_W_P,1.0_W_P,0.0_W_P]
               CJ1(:)=CY1(:)
               CJ2(:)=CY2(:)
               KLIM1=IJKCLIM(1)
               KLIM2=IJKCLIM(2)
               VNK(:)=[1.0_W_P,0.0_W_P,0.0_W_P]
               CK1(:)=CX1(:)
               CK2(:)=CX2(:)
            ENDIF
         ENDIF
         IJKCLIM(1)=ILIM1
         IJKCLIM(2)=ILIM2
         IJKCLIM(3)=JLIM1
         IJKCLIM(4)=JLIM2
         IJKCLIM(5)=KLIM1
         IJKCLIM(6)=KLIM2
      ELSE
         IJKCLIM(1)=1
         IJKCLIM(2)=NCL
         IJKCLIM(3)=1
         IJKCLIM(4)=NCL
         IJKCLIM(5)=1
         IJKCLIM(6)=NCL
         VNI(:)=[1.0_W_P,0.0_W_P,0.0_W_P]
         VNJ(:)=[0.0_W_P,1.0_W_P,0.0_W_P]
         VNK(:)=[0.0_W_P,0.0_W_P,1.0_W_P]
         CI1(:)=CX1(:)
         CI2(:)=CX2(:)
         CJ1(:)=CY1(:)
         CJ2(:)=CY2(:)
         CK1(:)=CZ1(:)
         CK2(:)=CZ2(:)
      END IF
!      DO IC=1,NCL 
      DO IC=IJKCLIM(1),IJKCLIM(2) 
         IF(NCL.EQ.1) THEN 
            CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,  &
                 NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,ZNS0, &
                 ZNST)                                                  
         ELSE 
            CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,  &
                 NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,ZNS2, &
                 ZNST)                                                  
         END IF
         IF(IC.GT.1) CALL INTE3D(CI1(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
              NTS2,NTV2,VERTP2,VNI(1),XNS2,VNI(2),YNS2,VNI(3),ZNS2)        
         IF(IC.LT.NCL) CALL INTE3D(CI2(IC),ICONTN,ICONTP,IPV2,NIPV2,    &
              NTP2,NTS2,NTV2,VERTP2,-VNI(1),XNS2,-VNI(2),YNS2,-VNI(3),ZNS2)  
!         DO JC=1,NCL 
         DO JC=IJKCLIM(3),IJKCLIM(4) 
            IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,    &
                 NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,XNS2, &
                 YNS1,YNS2,ZNS1,ZNS2)                                   
            IF(JC.GT.1) CALL INTE3D(CJ1(JC),ICONTN,ICONTP,IPV1,NIPV1,   &
                 NTP1,NTS1,NTV1,VERTP1,VNJ(1),XNS1,VNJ(2),YNS1,VNJ(3),ZNS1)
            IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
               IF(JC.LT.NCL) CALL INTE3D(CJ2(JC),ICONTN,ICONTP,IPV1,    &
                    NIPV1,NTP1,NTS1,NTV1,VERTP1,-VNJ(1),XNS1,-VNJ(2),YNS1, &
                    -VNJ(3),ZNS1)                                         
               IF(ICONTP.NE.0) THEN 
!                  DO KC=1,NCL 
                  DO KC=IJKCLIM(5),IJKCLIM(6) 
                     IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0, &
                          NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,   &
                          VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                     IF(KC.GT.1) CALL INTE3D(CK1(KC),ICONTN,ICONTP,IPV0,&
                          NIPV0,NTP0,NTS0,NTV0,VERTP0,VNK(1),XNS0,VNK(2), &
                          YNS0,VNK(3),ZNS0)                              
                     IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                        IF(KC.LT.NCL) CALL INTE3D(CK2(KC),ICONTN,ICONTP,&
                             IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,-VNK(1),    &
                             XNS0,-VNK(2),YNS0,-VNK(3),ZNS0)               
                        IF(ICONTP.NE.0) THEN 
                           !..   Subcell determination by truncation  
                           IF(NCL.GT.1) THEN 
                              ICONTP=0 
                              ICONTN=0 
                              DO IP=1,NTP0 
                                 ICHECK(IP)=0 
                              END DO
                              DO IS=1,NTS0 
                                 DO IV=1,NIPV0(IS) 
                                    IP=IPV0(IS,IV) 
                                    IF(ICHECK(IP).EQ.0) THEN 
                                       ICHECK(IP)=1 
                                       X=VERTP0(IP,1) 
                                       Y=VERTP0(IP,2) 
                                       Z=VERTP0(IP,3) 
                                       CALL PFUNC3D(PHIV(IP),CPARAB,VN, &
                                            X,Y,Z)
                                       IF(PHIV(IP).GT.0.0_W_P) THEN 
                                          IA(IP)=1 
                                          ICONTP=ICONTP+1 
                                       ELSE 
                                          IA(IP)=0 
                                          ICONTN=ICONTN+1 
                                       END IF
                                    END IF
                                 END DO
                              END DO
                           END IF
                           IF(ICONTN.EQ.0) THEN 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
                                   VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                              NTSINI=NTS0
                              CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,ISCUT,  &
                                   NIPV0,NTP0,NTS0,NTV0,1.0_W_P,XNS0,   &
                                   0.0_W_P,YNS0,0.0_W_P,ZNS0)
                              !.. Location of the new intersection points   
                              IF(NTS0.GT.NTSINI) THEN 
                                 IS=NTS0 
                                 IS2=NTS0
                                 XMAX2=CX2(IC)
                                 XMIN2=-CX1(IC)
                                 YMAX2=CY2(JC)
                                 YMIN2=-CY1(JC)
                                 ZMAX2=CZ2(KC)
                                 ZMIN2=-CZ1(KC)
                                 DO IS=NTSINI+1,NTS0
                                    SUMX=0.0_W_P
                                    SUMY=0.0_W_P
                                    SUMZ=0.0_W_P
                                    DO IV=1,NIPV0(IS) 
                                       IP=IPV0(IS,IV) 
                                       IP0=IPIA0(IP) 
                                       IP1=IPIA1(IP) 
                                       V0(1)=VERTP0(IP0,1) 
                                       V0(2)=VERTP0(IP0,2) 
                                       V0(3)=VERTP0(IP0,3) 
                                       V1(1)=VERTP0(IP1,1) 
                                       V1(2)=VERTP0(IP1,2) 
                                       V1(3)=VERTP0(IP1,3)
                                       CALL INTEPFUNC3D(CPARAB,VN,V0,V1,&
                                            VI)
                                       VERTP0(IP,1)=VI(1) 
                                       VERTP0(IP,2)=VI(2) 
                                       VERTP0(IP,3)=VI(3) 
                                       SUMX=SUMX+VERTP0(IP,1)
                                       SUMY=SUMY+VERTP0(IP,2)
                                       SUMZ=SUMZ+VERTP0(IP,3)
                                    END DO
                                    NTP0=NTP0+1
                                    VERTP0(NTP0,1)=SUMX/NIPV0(IS)
                                    VERTP0(NTP0,2)=SUMY/NIPV0(IS)
                                    VERTP0(NTP0,3)=SUMZ/NIPV0(IS)
                                    V0(1)=VERTP0(NTP0,1)
                                    V0(2)=VERTP0(NTP0,2)
                                    V0(3)=VERTP0(NTP0,3)
                                    CALL FINDBRACKETP(CPARAB,VN,DD/REAL(&
                                         NCL,KIND=W_P),IEBRACKET,V0,V1)
                                    IF(IEBRACKET.EQ.2) THEN 
                                       VI=V1 
                                    ELSEIF(IEBRACKET.EQ.1) THEN
                                       CALL INTEPFUNC3D(CPARAB,VN,V0,V1,&
                                            VI)
                                    ELSE
                                       VI=V0
                                    END IF
                                    !Correction 1
                                    !VI(1)=MAX(MIN(VI(1),XMAX2),XMIN2)
                                    !VI(2)=MAX(MIN(VI(2),YMAX2),YMIN2)
                                    !VI(3)=MAX(MIN(VI(3),ZMAX2),ZMIN2)
                                    !Correction 2
                                    !DO JS=1,NTS
                                    !   PHI=VI(1)*XNS(JS)+VI(2)*YNS(JS)+ &
                                    !        VI(3)*ZNS(JS)+CS(JS)
                                    !   IF(PHI.GT.TOLPHI) THEN
                                    !      VI(1)=VI(1)-PHI*XNS(JS)
                                    !      VI(2)=VI(2)-PHI*YNS(JS)
                                    !      VI(3)=VI(3)-PHI*ZNS(JS)
                                    !   END IF
                                    !END DO
                                    
                                    VERTP0(NTP0,1)=VI(1) 
                                    VERTP0(NTP0,2)=VI(2) 
                                    VERTP0(NTP0,3)=VI(3)
                                    ISINI=IS2+1
                                    DO IV=1,NIPV0(IS)
                                       IS2=IS2+1
                                       IV2=IV+1
                                       IF(IV2.GT.NIPV0(IS)) IV2=1
                                       NIPV0(IS2)=3
                                       IPV0(IS2,1)=NTP0
                                       IPV0(IS2,2)=IPV0(IS,IV)
                                       IPV0(IS2,3)=IPV0(IS,IV2)
                                       XV1=VERTP0(IPV0(IS2,2),1)-       &
                                            VERTP0(IPV0(IS2,1),1)
                                       YV1=VERTP0(IPV0(IS2,2),2)-       &
                                            VERTP0(IPV0(IS2,1),2)
                                       ZV1=VERTP0(IPV0(IS2,2),3)-       &
                                            VERTP0(IPV0(IS2,1),3)
                                       XV2=VERTP0(IPV0(IS2,3),1)-       &
                                            VERTP0(IPV0(IS2,2),1)
                                       YV2=VERTP0(IPV0(IS2,3),2)-       &
                                            VERTP0(IPV0(IS2,2),2)
                                       ZV2=VERTP0(IPV0(IS2,3),3)-       &
                                            VERTP0(IPV0(IS2,2),3)
                                       XM=YV1*ZV2-ZV1*YV2
                                       YM=ZV1*XV2-XV1*ZV2
                                       ZM=XV1*YV2-YV1*XV2
                                       AMOD=(XM**2+YM**2+ZM**2)**0.5_W_P
                                       IF(AMOD.NE.0.0_W_P) THEN
                                          XNS0(IS2)=XM/AMOD
                                          YNS0(IS2)=YM/AMOD
                                          ZNS0(IS2)=ZM/AMOD
                                       ELSE
!                                          NIPV0(IS2)=0
                                          XNS0(IS2)=XM
                                          YNS0(IS2)=YM
                                          ZNS0(IS2)=ZM
                                       END IF
                                    END DO
                                    !* Cancel the IS face
                                    IF(IS2.GT.IS) NIPV0(IS)=0
                                 END DO
                                 NTS0=IS2
                              END IF
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,VOLF, &
                                   XNS0,YNS0,ZNS0)
                              VF=VF+VOLF 
                           END IF
                        END IF
                     END IF
                  END DO
               END IF
            END IF
         END DO
      END DO
      RETURN 
    END SUBROUTINE INTPV3DPA_bak2
!------------------------- END OF INTPV3DPA_bak2 --------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                               INTPLIM                               c 
! Determine the xyz-truncation limits for the recursive intersection  c
! operation                                                           c
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! BOX      = array containing the maximum and minimum position values c 
!            along the coordinate  directions of the hexahedral box   c 
!            1 -> XMIN                                                c 
!            2 -> XMAX                                                c 
!            3 -> YMIN                                                c 
!            4 -> YMAX                                                c 
!            5 -> ZMIN                                                c 
!            6 -> ZMAX                                                c 
! CPARAB   = local paraboloid coefficients                            c
! NC       = maximum number of divisions along each coordinate axis   c 
! VN       = paraboloid orthonormal basis                             c
! On return:                                                          c 
!===========                                                          c 
! IJKCLIM  = array containing the truncation index limits             c
!            1 -> ICMIN                                               c
!            2 -> ICMAX                                               c
!            3 -> JCMIN                                               c
!            4 -> JCMAX                                               c
!            5 -> KCMIN                                               c
!            6 -> KCMAX                                               c
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE INTPLIM(BOX,CPARAB,IJKCLIM,NC,VN) BIND(C)   
!.. Scalar Arguments
        INTEGER (I_P), INTENT(IN) :: NC
!.. Array Arguments                                                    
        REAL (W_P), INTENT(IN) :: BOX(6),CPARAB(12),VN(9) 
        INTEGER(I_P), INTENT(OUT) :: IJKCLIM(6)
!.. Local scalars
        REAL (W_P) :: D,F,GF,GU,GV,U,V,VF,VU,VV,X,XN,XNL,Y,YN,YNL,Z,ZN, &
             ZNL
        IJKCLIM(1)=1
        IJKCLIM(2)=NC
        IJKCLIM(3)=1
        IJKCLIM(4)=NC
        IJKCLIM(5)=1
        IJKCLIM(6)=NC
        !. plane x
        XN=1.0_W_P
        YN=0.0_W_P
        ZN=0.0_W_P
        !. change to local reference system
        VF=XN*VN(1)+YN*VN(2)+ZN*VN(3)
        VU=XN*VN(4)+YN*VN(5)+ZN*VN(6)
        VV=XN*VN(7)+YN*VN(8)+ZN*VN(9)
        D=VF*(CPARAB(5)**2-4.0_W_P*CPARAB(4)*CPARAB(6))
        IF(D.NE.0.0_W_P) THEN
           U=(2.0_W_P*CPARAB(6)*VU-CPARAB(5)*VV+(2.0*CPARAB(2)*         &
                CPARAB(6)-CPARAB(3)*CPARAB(5))*VF)/D
           V=(-CPARAB(5)*VU+2.0_W_P*CPARAB(4)*VV+(2.0*CPARAB(3)*        &
                CPARAB(4)-CPARAB(2)*CPARAB(5))*VF)/D
           F=CPARAB(1)+CPARAB(2)*U+CPARAB(3)*V+CPARAB(4)*U**2+          &
                CPARAB(5)*U*V+CPARAB(6)*V**2
           !. change to global reference system
           X=VN(4)*U+VN(7)*V+VN(1)*F+CPARAB(10)   
           IF(X.GT.BOX(1).AND.X.LT.BOX(2)) THEN
              GU=CPARAB(2)+2.0_W_P*CPARAB(4)*U+CPARAB(5)*V
              GV=CPARAB(3)+CPARAB(5)*U+2.0_W_P*CPARAB(6)*V
              GF=-1.0_W_P
              XNL=VN(4)*GU+VN(7)*GV+VN(1)*GF
              IF(XN*XNL.LT.0.0_W_P) THEN
                 IJKCLIM(1)=1+INT(NC*(X-BOX(1))/(BOX(2)-BOX(1)))
              ELSE
                 IJKCLIM(2)=1+INT(NC*(X-BOX(1))/(BOX(2)-BOX(1)))
              END IF
           END IF
        END IF
        !. plane y
        XN=0.0_W_P
        YN=1.0_W_P
        ZN=0.0_W_P
        !. change to local reference system
        VF=XN*VN(1)+YN*VN(2)+ZN*VN(3)
        VU=XN*VN(4)+YN*VN(5)+ZN*VN(6)
        VV=XN*VN(7)+YN*VN(8)+ZN*VN(9)
        D=VF*(CPARAB(5)**2-4.0_W_P*CPARAB(4)*CPARAB(6))
        IF(D.NE.0.0_W_P) THEN
           U=(2.0_W_P*CPARAB(6)*VU-CPARAB(5)*VV+(2.0*CPARAB(2)*         &
                CPARAB(6)-CPARAB(3)*CPARAB(5))*VF)/D
           V=(-CPARAB(5)*VU+2.0_W_P*CPARAB(4)*VV+(2.0*CPARAB(3)*        &
                CPARAB(4)-CPARAB(2)*CPARAB(5))*VF)/D
           F=CPARAB(1)+CPARAB(2)*U+CPARAB(3)*V+CPARAB(4)*U**2+          &
                CPARAB(5)*U*V+CPARAB(6)*V**2
           !. change to global reference system
           Y=VN(5)*U+VN(8)*V+VN(2)*F+CPARAB(11)
           IF(Y.GT.BOX(3).AND.Y.LT.BOX(4)) THEN
              GU=CPARAB(2)+2.0_W_P*CPARAB(4)*U+CPARAB(5)*V
              GV=CPARAB(3)+CPARAB(5)*U+2.0_W_P*CPARAB(6)*V
              GF=-1.0_W_P
              YNL=VN(5)*GU+VN(8)*GV+VN(2)*GF
              IF(YN*YNL.LT.0.0_W_P) THEN
                 IJKCLIM(3)=1+INT(NC*(Y-BOX(3))/(BOX(4)-BOX(3)))
              ELSE
                 IJKCLIM(4)=1+INT(NC*(Y-BOX(3))/(BOX(4)-BOX(3)))
              END IF
           END IF
        END IF
        !. plane z
        XN=0.0_W_P
        YN=0.0_W_P
        ZN=1.0_W_P
        !. change to local reference system
        VF=XN*VN(1)+YN*VN(2)+ZN*VN(3)
        VU=XN*VN(4)+YN*VN(5)+ZN*VN(6)
        VV=XN*VN(7)+YN*VN(8)+ZN*VN(9)
        D=VF*(CPARAB(5)**2-4.0_W_P*CPARAB(4)*CPARAB(6))
        IF(D.NE.0.0_W_P) THEN
           U=(2.0_W_P*CPARAB(6)*VU-CPARAB(5)*VV+(2.0*CPARAB(2)*         &
                CPARAB(6)-CPARAB(3)*CPARAB(5))*VF)/D
           V=(-CPARAB(5)*VU+2.0_W_P*CPARAB(4)*VV+(2.0*CPARAB(3)*        &
                CPARAB(4)-CPARAB(2)*CPARAB(5))*VF)/D
           F=CPARAB(1)+CPARAB(2)*U+CPARAB(3)*V+CPARAB(4)*U**2+          &
                CPARAB(5)*U*V+CPARAB(6)*V**2
           !. change to global reference system
           Z=VN(6)*U+VN(9)*V+VN(3)*F+CPARAB(12)
           IF(Z.GT.BOX(5).AND.Z.LT.BOX(6)) THEN
              GU=CPARAB(2)+2.0_W_P*CPARAB(4)*U+CPARAB(5)*V
              GV=CPARAB(3)+CPARAB(5)*U+2.0_W_P*CPARAB(6)*V
              GF=-1.0_W_P
              ZNL=VN(6)*GU+VN(9)*GV+VN(3)*GF
              IF(ZN*ZNL.LT.0.0_W_P) THEN
                 IJKCLIM(5)=1+INT(NC*(Z-BOX(5))/(BOX(6)-BOX(5)))
              ELSE
                 IJKCLIM(6)=1+INT(NC*(Z-BOX(5))/(BOX(6)-BOX(5)))
              END IF
           END IF
        END IF
        RETURN
      END SUBROUTINE INTPLIM
!-------------------------- END OF INTPLIM ---------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              INTPV3DPA_bak                              c 
! Polyhedral approximation of the volume of intersection between a    c
! paraboloid and an arbitrary polyhedron                              c
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! CPARAB   = local paraboloid coefficients                            c
! IPV      = array containing the global indices of the original pol. c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! NTV      = total number of vertices                                 c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! VF       = volume of intersection                                   c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE INTPV3DPA_bak(CPARAB,IPV,NC,NE,NIPV,NTP,NTS,NTV,VERTP,VF,  &
           XNS,YNS,ZNS) BIND(C)                                         
!.. Scalar Arguments                                                    
        REAL (W_P), INTENT(IN) :: CPARAB(12)
        REAL(W_P), INTENT(OUT) :: VF 
        INTEGER(I_P), INTENT(IN) :: NC, NE, NTP, NTS, NTV 
!.. Array Arguments                                                     
        REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
        INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
!.. Local Scalars                                                       
      REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DMOD,DX,DY,DZ,EPSILON,F0,F1,F2,  &
           F3,F4,F5,F6,TOLRF,VOLF,VOLTRI,X,XM,XMAX,XMIN,XP,XV1,XV2,Y,YM,&
           YMAX,YMIN,YP,YV1,YV2,Z,ZM,ZMAX,ZMIN,ZP,ZV1,ZV2        
      INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IE,IEBRACKET,IP,IP0,IP1,IRF,   &
           IRFC,IS,IS2,ISINI,IV,IV2,JC,KC,NCL,NS2,NSDIM,NTP0,NTP1,NTP2, &
           NTPA,NTPINI,NTPT,NTS0,NTS1,NTS2,NTSA,NTST,NTSINI,NTV0,NTV1,  &
           NTV2,NTVA,NTVT,NV2,NVDIM
!.. Local Arrays                                                        
      REAL(W_P) :: CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC*5),    &
           CX2(NC*5),CY1(NC*5),CY2(NC*5),CZ1(NC*5),CZ2(NC*5),PHIV(NV),  &
           PHIVMIN(NS),V0(3),V1(3),V2(3),V3(3),VI(3),VERTP0(NV,3),      &
           VERTP1(NV,3),VERTP2(NV,3),VERTPT(NV,3),VN(9),XNS0(NS),       &
           XNS1(NS),XNS2(NS),XNST(NS),YNS0(NS),YNS1(NS),YNS2(NS),       &
           YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),ZNST(NS)         
      INTEGER(I_P) :: IA(NV),ICHECK(NV),IPIA0(NV),IPIA1(NV),            &
           IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),ISCFIP(NV),  &
           ISCONTN(NS),ISCONTP(NS),NIPV0(NS),NIPV1(NS),NIPV2(NS),       &
           NIPVT(NS)
!.. Local Allocatable Arrays
      INTEGER(I_P), ALLOCATABLE, DIMENSION (:) :: NIPVA
      INTEGER(I_P), ALLOCATABLE, DIMENSION (:,:) :: IPVA
      REAL(W_P), ALLOCATABLE, DIMENSION (:) :: XNSA,YNSA,ZNSA
      REAL(W_P), ALLOCATABLE, DIMENSION (:,:) :: VERTPA
!.. Coordinate extremes of the cell and vertex tagging                  
      NCL=NC 
      VF=0.0 
      XMIN=1.0E+20_W_P 
      XMAX=-1.0E+20_W_P 
      YMIN=1.0E+20_W_P 
      YMAX=-1.0E+20_W_P 
      ZMIN=1.0E+20_W_P 
      ZMAX=-1.0E+20_W_P 
      ICONTP=0 
      ICONTN=0 
      V0(1)=0.0_W_P 
      V0(2)=0.0_W_P 
      V0(3)=0.0_W_P 
      DO IP=1,NTP 
         ICHECK(IP)=0 
      END DO
      !Paraboloid orthonormal basis
      VN(1)=CPARAB(7) 
      VN(2)=CPARAB(8) 
      VN(3)=CPARAB(9) 
      VN(4)=VN(2)
      VN(5)=-VN(1)
      VN(6)=0.0_W_P
      DMOD=(VN(4)**2+VN(5)**2)**0.5_W_P
      IF(DMOD.NE.0.0_W_P) THEN
         VN(4)=VN(4)/DMOD
         VN(5)=VN(5)/DMOD
      ELSE
         VN(4)=VN(3)
         VN(5)=0.0_W_P
         VN(6)=-VN(1)
         DMOD=(VN(4)**2+VN(6)**2)**0.5_W_P
         VN(4)=VN(4)/DMOD
         VN(6)=VN(6)/DMOD
      END IF
      VN(7)=VN(2)*VN(6)-VN(3)*VN(5)
      VN(8)=VN(3)*VN(4)-VN(1)*VN(6)
      VN(9)=VN(1)*VN(5)-VN(2)*VN(4)
      
      DO IS=1,NTS
         ISCONTP(IS)=0
         ISCONTN(IS)=0
         PHIVMIN(IS)=1.0E+20_W_P
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(ICHECK(IP).EQ.0) THEN 
               ICHECK(IP)=1 
               XP=VERTP(IP,1) 
               YP=VERTP(IP,2) 
               ZP=VERTP(IP,3) 
               XMIN=DMIN1(XMIN,XP) 
               XMAX=DMAX1(XMAX,XP) 
               YMIN=DMIN1(YMIN,YP) 
               YMAX=DMAX1(YMAX,YP) 
               ZMIN=DMIN1(ZMIN,ZP) 
               ZMAX=DMAX1(ZMAX,ZP)
               IF(NC.EQ.1) THEN
                  CALL PFUNC3D(PHIV(IP),CPARAB,VN,XP,YP,ZP)
                  IF(PHIV(IP).GT.0.0_W_P) THEN 
                     IA(IP)=1 
                     ICONTP=ICONTP+1 
                  ELSE 
                     IA(IP)=0 
                     ICONTN=ICONTN+1 
                  END IF
               END IF
            END IF 
         END DO
      END DO 
!.. initialization                                                      
      DX=XMAX-XMIN 
      DY=YMAX-YMIN 
      DZ=ZMAX-ZMIN 
      DD=0.01*MIN(DX,DY,DZ)
      IF(DD.LT.1.0E-20_W_P) THEN
         VF=0._W_P 
         RETURN 
      END IF
      CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,            &
           NTS,NTVT,NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)
      NV2=NV+10*NE*(NE+5)/2
      NS2=NS+10*(NE+1)*(NE+1)
      ALLOCATE(IPVA(NS2,NV2))
      ALLOCATE(NIPVA(NS2))
      ALLOCATE(VERTPA(NV2,3))
      ALLOCATE(XNSA(NS2))
      ALLOCATE(YNSA(NS2))
      ALLOCATE(ZNSA(NS2))

      DDX=DX/NCL 
      DDY=DY/NCL 
      DDZ=DZ/NCL 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CX1(I)=-XMIN 
         ELSE 
            CX1(I)=CX1(I-1)-DDX 
         END IF
         CX2(I)=-CX1(I)+DDX 
      END DO
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CY1(I)=-YMIN 
         ELSE 
            CY1(I)=CY1(I-1)-DDY 
         END IF 
         CY2(I)=-CY1(I)+DDY 
      END DO 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CZ1(I)=-ZMIN 
         ELSE 
            CZ1(I)=CZ1(I-1)-DDZ 
         END IF 
         CZ2(I)=-CZ1(I)+DDZ 
      END DO 
      DO IC=1,NCL 
         IF(NCL.EQ.1) THEN 
            CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,  &
                 NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,ZNS0, &
                 ZNST)                                                  
         ELSE 
            CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,  &
                 NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,ZNS2, &
                 ZNST)                                                  
         END IF
         IF(IC.GT.1) CALL INTE3D(CX1(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
              NTS2,NTV2,VERTP2,1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)        
         IF(IC.LT.NCL) CALL INTE3D(CX2(IC),ICONTN,ICONTP,IPV2,NIPV2,    &
              NTP2,NTS2,NTV2,VERTP2,-1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)  
         DO JC=1,NCL 
            IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,    &
                 NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,XNS2, &
                 YNS1,YNS2,ZNS1,ZNS2)                                   
            IF(JC.GT.1) CALL INTE3D(CY1(JC),ICONTN,ICONTP,IPV1,NIPV1,   &
                 NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,1.0D0,YNS1,0.0D0,ZNS1)
            IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
               IF(JC.LT.NCL) CALL INTE3D(CY2(JC),ICONTN,ICONTP,IPV1,    &
                    NIPV1,NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,-1.0D0,YNS1, &
                    0.0D0,ZNS1)                                         
               IF(ICONTP.NE.0) THEN 
                  DO KC=1,NCL 
                     IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0, &
                          NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,   &
                          VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                     IF(KC.GT.1) CALL INTE3D(CZ1(KC),ICONTN,ICONTP,IPV0,&
                          NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,XNS0,0.0D0, &
                          YNS0,1.0D0,ZNS0)                              
                     IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                        IF(KC.LT.NCL) CALL INTE3D(CZ2(KC),ICONTN,ICONTP,&
                             IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,    &
                             XNS0,0.0D0,YNS0,-1.0D0,ZNS0)               
                        IF(ICONTP.NE.0) THEN 
                           !..   Subcell determination by truncation  
                           IF(NCL.GT.1) THEN 
                              ICONTP=0 
                              ICONTN=0 
                              DO IP=1,NTP0 
                                 ICHECK(IP)=0 
                              END DO
                              DO IS=1,NTS0 
                                 DO IV=1,NIPV0(IS) 
                                    IP=IPV0(IS,IV) 
                                    IF(ICHECK(IP).EQ.0) THEN 
                                       ICHECK(IP)=1 
                                       X=VERTP0(IP,1) 
                                       Y=VERTP0(IP,2) 
                                       Z=VERTP0(IP,3) 
                                       CALL PFUNC3D(PHIV(IP),CPARAB,VN, &
                                            X,Y,Z)
                                       IF(PHIV(IP).GT.0.0_W_P) THEN 
                                          IA(IP)=1 
                                          ICONTP=ICONTP+1 
                                       ELSE 
                                          IA(IP)=0 
                                          ICONTN=ICONTN+1 
                                       END IF
                                    END IF
                                 END DO
                              END DO
                           END IF
                           IF(ICONTN.EQ.0) THEN 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
                                   VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                              NTSINI=NTS0
                              NTPINI=NTP0
                              CALL NEWPOLCF3D(IA,IPIA0,IPIA1,IPV0,      &
                                   ISCFIP,NIPV0,NTP0,NTS0,NTV0)
                              !.. Location of the new intersection points   
                              IF(NTS0.GT.NTSINI) THEN 
                                 IS=NTS0 
                                 IS2=NTS0
                                 NSDIM=NTS0
                                 NVDIM=NTP0
                                 DO IS=NTSINI+1,NTS0
                                    NSDIM=NSDIM+NIPV0(IS)*(NE+1)**2
                                    NVDIM=NVDIM+NIPV0(IS)*(2*NE+MAX(0,  &
                                         (NE-1)*NE/2))+1
                                    DO IV=1,NIPV0(IS) 
                                       IP=IPV0(IS,IV) 
                                       IP0=IPIA0(IP) 
                                       IP1=IPIA1(IP) 
                                       V0(1)=VERTP0(IP0,1) 
                                       V0(2)=VERTP0(IP0,2) 
                                       V0(3)=VERTP0(IP0,3) 
                                       V1(1)=VERTP0(IP1,1) 
                                       V1(2)=VERTP0(IP1,2) 
                                       V1(3)=VERTP0(IP1,3)
                                       CALL INTEPFUNC3D(CPARAB,VN,V0,V1,&
                                            VI)
                                       VERTP0(IP,1)=VI(1) 
                                       VERTP0(IP,2)=VI(2) 
                                       VERTP0(IP,3)=VI(3) 
                                    END DO
                                 END DO
                                 !Refine cap
                                 IF(NVDIM.GT.NV2.OR.NSDIM.GT.NS2) THEN
                                    DEALLOCATE(IPVA,NIPVA,VERTPA,XNSA,  &
                                         YNSA,ZNSA)
                                    NV2=NVDIM
                                    NS2=NSDIM
                                    ALLOCATE(IPVA(NS2,NV2))
                                    ALLOCATE(NIPVA(NS2))
                                    ALLOCATE(VERTPA(NV2,3))
                                    ALLOCATE(XNSA(NS2))
                                    ALLOCATE(YNSA(NS2))
                                    ALLOCATE(ZNSA(NS2))
                                 END IF
                                 NTSA=NTS0 
                                 NTVA=NTV0 
                                 NTPA=NTP0 
                                 DO IP=1,NTP0 
                                    DO I=1,3 
                                       VERTPA(IP,I)=VERTP0(IP,I) 
                                    END DO
                                 END DO
                                 DO IS=1,NTS0 
                                    XNSA(IS)=XNS0(IS) 
                                    YNSA(IS)=YNS0(IS) 
                                    ZNSA(IS)=ZNS0(IS) 
                                    NIPVA(IS)=NIPV0(IS) 
                                    DO IV=1,NIPV0(IS) 
                                       IPVA(IS,IV)=IPV0(IS,IV) 
                                    END DO
                                 END DO
                                 CALL TRIPCAP(CPARAB,VN,DD,IPVA,ISCFIP, &
                                      NE,NIPVA,NS2,NTPA,NTSA,NTSINI,    &
                                      NTVA,NV2,VERTPA,XNSA,YNSA,ZNSA)
                                 CALL TOOLV3DDIM(IPVA,NIPVA,NS2,NTSA,   &
                                      NV2,VERTPA,VOLF,XNSA,YNSA,ZNSA) 
                                 VF=VF+VOLF 
                              END IF
                           END IF
                        END IF
                     END IF
                  END DO
               END IF
            END IF
         END DO
      END DO
      !VF=VF
      DEALLOCATE(IPVA,NIPVA,VERTPA,XNSA,YNSA,ZNSA)
      RETURN 
    END SUBROUTINE INTPV3DPA_bak
!------------------------- END OF INTPV3DPA_bak --------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              TRIPCAP                                c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! CPARAB   = local paraboloid coefficients                            c
! VN       = paraboloid orthonormal basis                             c
! DD       = differential size                                        c 
! IPV      = array containing the global indices of the truncated pol.c 
!            vertices                                                 c 
! ISCFIP   = array containing the index of the clipped face           c
!            associated to each new intersection point                c 
! NE       = number of sub-edges along each curved edge of the        c
!            capping faces                                            c 
! NIPV     = number of vertices of each face                          c 
! NS2      = size of arrays involving polyhedron faces                c
! NTP      = last global vertex index                                 c 
! NTS      = last face index of the truncated polyhedron              c 
! NTSINI   = last face index of the original polyhedron               c 
! NTV      = total number of vertices                                 c 
! NV2      = size of arrays involving polyhedron vertices             c
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! IPV      = array containing the global indices of the refined-poly. c 
!            vertices                                                 c 
! NIPV     = number of vertices of each face of the refined poly.     c 
! NTP      = last global vertex index of the refined polyhedron       c 
! NTS      = last face index of the refined polyhedron                c 
! NTV      = total number of vertices of the refined polyhedron       c 
! VERTP    = vertex coordinates of the refined polyhedron             c 
! XNS, ... = unit-lenght normals to the faces of the refined polyh.   c 
!---------------------------------------------------------------------c 
    SUBROUTINE TRIPCAP(CPARAB,VN,DD,IPV,ISCFIP,NE,NIPV,NS2,NTP,NTS,     &
         NTSINI,NTV,NV2,VERTP,XNS,YNS,ZNS) BIND(C)
      !.. Scalar Arguments                                                    
      INTEGER(I_P), INTENT(IN) :: NE, NS2, NTSINI, NV2
      INTEGER(I_P), INTENT(IN) :: ISCFIP(NV)
      REAL(W_P), INTENT(IN) :: DD
      INTEGER(I_P), INTENT(INOUT) :: NTP, NTS, NTV 
      !.. Array Arguments                                                     
      REAL(W_P), INTENT(INOUT) :: VERTP(NV2,3),XNS(NS2),YNS(NS2),ZNS(NS2)
      REAL(W_P), INTENT(IN) :: CPARAB(12),VN(9)
      INTEGER(I_P), INTENT(INOUT) :: IPV(NS2,NV2),NIPV(NS2) 
      !.. Local Scalars                                                       
      INTEGER(I_P) :: I,IE,IEBRACKET,IER,IP,IP2,IPNEW,IS,ISNEW,IST,IV,  &
           IV2,IVISNEW,IVNEW,JU,JU1,JV,JV1,JW,JW1,NPC,NTPINI
      REAL(W_P) :: DMOD,XM,XV1,XV2,YM,YV1,YV2,ZM,ZV1,ZV2
      !.. Local Arrays
      INTEGER(I_P) :: IPT(NE+2,NE+2,NE+2),IPV2(NS2,NV2)
      REAL(W_P) :: SUMP(3),V0(3),VE0(3),V1(3),VE1(3),VEI(3),VEN(3),     &
           VET(3),VI(3)
      
      IPNEW=NTP
      IST=NTS
      DO ISNEW=NTSINI+1,NTS
         NTPINI=IPNEW
         DO IVISNEW=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IVISNEW)
            IF(IVISNEW.EQ.NIPV(ISNEW)) THEN
               IP2=IPV(ISNEW,1)
            ELSE
               IP2=IPV(ISNEW,IVISNEW+1)
            END IF
            IS=ISCFIP(IP)
            DO IV=1,NIPV(IS)
               IF(IP.EQ.IPV(IS,IV)) THEN ! new vertex insertion on cap-edge
                  DO I=1,3
                     VET(I)=VERTP(IP2,I)-VERTP(IP,I)
                  END DO
                  VEN(1)=YNS(IS)*VET(3)-ZNS(IS)*VET(2)
                  VEN(2)=ZNS(IS)*VET(1)-XNS(IS)*VET(3)
                  VEN(3)=XNS(IS)*VET(2)-YNS(IS)*VET(1)
                  DMOD=(VEN(1)**2+VEN(2)**2+VEN(3)**2)**0.5
                  IF(DMOD.NE.0.0_W_P) THEN
                     DO I=1,3
                        VEN(I)=VEN(I)/DMOD
                     END DO
                  END IF
                  DO IVNEW=1,NE
                     IPNEW=IPNEW+1
                     ! new vertex location
                     DO I=1,3 
                        VE0(I)=VERTP(IP,I)+VET(I)*REAL(IVNEW,KIND=W_P)/ &
                        (REAL(NE,KIND=W_P)+1.0)
                     END DO
                     IF(DMOD.NE.0.0_W_P) THEN
                        CALL FINDBRACKETNP(CPARAB,VN,DD,IEBRACKET,VE0,VE1,VEN)
                        IF(IEBRACKET.EQ.2) THEN 
                           VEI=VE1 
                        ELSE
                           CALL INTEPFUNC3D(CPARAB,VN,VE0,VE1,VEI)
                        END IF
                     ELSE
                        VEI=VE0
                     END IF
                     DO I=1,3
                        VERTP(IPNEW,I)=VEI(I)
                     END DO
                  END DO
                  !Arrange refined clipped face
                  IE=0        
                  DO IV2=1,NIPV(IS)                                   
                     IPV2(IS,IV2+IE)=IPV(IS,IV2)
                     IF(IPV(IS,IV2).EQ.IP2) THEN                      
                        DO I=1,NE
                           IE=IE+1
                           IPV2(IS,IV2+IE)=IPNEW-I+1
                        END DO 
                     END IF
                  END DO
                  IPV(IS,:)=IPV2(IS,:)
                  !------
                  NIPV(IS)=NIPV(IS)+NE
                  GOTO 10
               END IF
            END DO
10          CONTINUE            
      END DO
! New faces triangulation
         SUMP=0.0_W_P
         DO IV=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IV)
            DO I=1,3
               SUMP(I)=SUMP(I)+VERTP(IP,I)
            END DO
         END DO
         IPNEW=IPNEW+1 !Central vertex insertion on cap-face
         DO I=1,3
            V0(I)=SUMP(I)/NIPV(ISNEW)
         END DO
         CALL FINDBRACKETP(CPARAB,VN,DD,IEBRACKET,V0,V1)
         IF(IEBRACKET.EQ.2) THEN 
            VI=V1 
         ELSEIF(IEBRACKET.EQ.1) THEN
            CALL INTEPFUNC3D(CPARAB,VN,V0,V1,VI)
         ELSE
            VI=V0
         END IF
         VERTP(IPNEW,1)=VI(1) 
         VERTP(IPNEW,2)=VI(2) 
         VERTP(IPNEW,3)=VI(3)
         !Vertices insertion on radial edges
         NPC=IPNEW
         DO IV=1,NIPV(ISNEW)
            IP=IPV(ISNEW,IV)
            DO I=1,3
               VET(I)=VERTP(NPC,I)-VERTP(IP,I)
            END DO
            DO IVNEW=1,NE
               IPNEW=IPNEW+1
               ! new vertex location
               DO I=1,3 
                  V0(I)=VERTP(IP,I)+VET(I)*REAL(IVNEW,KIND=W_P)/ &
                       (REAL(NE,KIND=W_P)+1.0)
               END DO
               CALL FINDBRACKETP(CPARAB,VN,DD,IEBRACKET,V0,V1)
               IF(IEBRACKET.EQ.2) THEN 
                  VI=V1 
               ELSEIF(IEBRACKET.EQ.1) THEN
                  CALL INTEPFUNC3D(CPARAB,VN,V0,V1,VI)
               ELSE
                  VI=V0
               END IF
               VERTP(IPNEW,1)=VI(1) 
               VERTP(IPNEW,2)=VI(2) 
               VERTP(IPNEW,3)=VI(3)
            END DO
         END DO
         !------------------------------------
         !Triangulation
         DO IV=1,NIPV(ISNEW)
            !Control points for Triangulation
            IPT(1,1,NE+2)=IPV(ISNEW,IV)
            IF(IV.EQ.NIPV(ISNEW)) THEN
               IPT(NE+2,1,1)=IPV(ISNEW,1)
            ELSE
               IPT(NE+2,1,1)=IPV(ISNEW,IV+1)
            END IF
            IPT(1,NE+2,1)=NPC
            JV=0
            DO JU=1,NE
               JW=(NE+1)-JU-JV
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IPT(JU1,JV1,JW1)=NTPINI+(IV-1)*NE+JU
            END DO
            JU=0
            DO JV=1,NE
               JW=(NE+1)-JU-JV
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IPT(JU1,JV1,JW1)=NPC+(IV-1)*NE+JV
            END DO
            JW=0
            DO JV=1,NE
               JU=(NE+1)-JV-JW
               JU1=JU+1
               JV1=JV+1
               JW1=JW+1
               IF(IV.EQ.NIPV(ISNEW)) THEN
                  IPT(JU1,JV1,JW1)=NPC+JV
               ELSE
                  IPT(JU1,JV1,JW1)=NPC+IV*NE+JV
               END IF
            END DO
            DO JV=1,NE-1
               DO JU=1,NE-JV
                  JW=(NE+1)-JU-JV
                  !Insert internal points on the cap-triangle
                  IPNEW=IPNEW+1
                  JU1=JU+1
                  JV1=JV+1
                  JW1=JW+1
                  IPT(JU1,JV1,JW1)=IPNEW
                  DO I=1,3
                     VET(I)=VERTP(IPT((NE+1)-JV+1,JV1,1),I)-            &
                          VERTP(IPT(1,JV1,(NE+1)-JV+1),I)
                  END DO
                  DO I=1,3 
                     V0(I)=VERTP(IPT(1,JV1,(NE+1)-JV+1),I)+VET(I)*      &
                          REAL(JU,KIND=W_P)/(REAL(NE-JV,KIND=W_P)+1.0)
                  END DO
                  CALL FINDBRACKETP(CPARAB,VN,DD,IEBRACKET,V0,V1)
                  IF(IEBRACKET.EQ.2) THEN 
                     VI=V1 
                  ELSEIF(IEBRACKET.EQ.1) THEN
                     CALL INTEPFUNC3D(CPARAB,VN,V0,V1,VI)
                  ELSE
                     VI=V0
                  END IF
                  VERTP(IPNEW,1)=VI(1) 
                  VERTP(IPNEW,2)=VI(2) 
                  VERTP(IPNEW,3)=VI(3)
               END DO
            END DO

            DO JV=0,NE
               DO JU=0,NE-JV
                  JW=(NE+1)-JU-JV
                  JU1=JU+1
                  JV1=JV+1
                  JW1=JW+1
                  IF(JU.GT.0) THEN
                     IST=IST+1
                     IS=IST
                     NIPV(IS)=3
                     IPV(IS,1)=IPT(JU1,JV1,JW1)
                     IPV(IS,2)=IPT(JU1,JV1+1,JW1-1)
                     IPV(IS,3)=IPT(JU1-1,JV1+1,JW1)
                     XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1)       
                     YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2)       
                     ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3)       
                     XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1)       
                     YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2)       
                     ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3)       
                     XM=YV1*ZV2-ZV1*YV2 
                     YM=ZV1*XV2-XV1*ZV2 
                     ZM=XV1*YV2-YV1*XV2 
                     DMOD=(XM**2+YM**2+ZM**2)**0.5               
                     IF(DMOD.NE.0.0) THEN 
                        XNS(IS)=XM/DMOD 
                        YNS(IS)=YM/DMOD 
                        ZNS(IS)=ZM/DMOD 
                     ELSE 
                        NIPV(IS)=0 
                     END IF
                  END IF
                  IST=IST+1
                  IS=IST
                  NIPV(IS)=3
                  IPV(IS,1)=IPT(JU1,JV1,JW1)
                  IPV(IS,2)=IPT(JU1+1,JV1,JW1-1)
                  IPV(IS,3)=IPT(JU1,JV1+1,JW1-1)
                  XV1=VERTP(IPV(IS,2),1)-VERTP(IPV(IS,1),1)       
                  YV1=VERTP(IPV(IS,2),2)-VERTP(IPV(IS,1),2)       
                  ZV1=VERTP(IPV(IS,2),3)-VERTP(IPV(IS,1),3)       
                  XV2=VERTP(IPV(IS,3),1)-VERTP(IPV(IS,2),1)       
                  YV2=VERTP(IPV(IS,3),2)-VERTP(IPV(IS,2),2)       
                  ZV2=VERTP(IPV(IS,3),3)-VERTP(IPV(IS,2),3)       
                  XM=YV1*ZV2-ZV1*YV2 
                  YM=ZV1*XV2-XV1*ZV2 
                  ZM=XV1*YV2-YV1*XV2 
                  DMOD=(XM**2+YM**2+ZM**2)**0.5               
                  IF(DMOD.NE.0.0) THEN 
                     XNS(IS)=XM/DMOD 
                     YNS(IS)=YM/DMOD 
                     ZNS(IS)=ZM/DMOD 
                  ELSE 
                     NIPV(IS)=0 
                  END IF
               END DO
            END DO
         END DO
      END DO
      DO ISNEW=NTSINI+1,NTS
         NIPV(ISNEW)=0
      END DO
      NTV=NTV+IPNEW-NTP
      NTP=IPNEW
      NTS=IS
      RETURN
    END SUBROUTINE TRIPCAP
!-------------------------- END OF TRPICAP ---------------------------c 
!---------------------------------------------------------------------c     
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                             XINITF3DNEW                             c 
! This version is slightly faster because it does not repeat the      c 
! computation of the intersection points between interface and        c 
! sub-cell edges                                                      c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! IPV      = array containing the global indices of the original pol. c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! NTV      = total number of vertices                                 c 
! TOL      = prescribed positive tolerance for the distance to the    c 
!            interface                                                c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! VF       = material volume fraction                                 c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE XINITF3DNEW(FUNC3D,IPV,NC,NIPV,NTP,NTS,NTV,TOL,VERTP,  &
     &     VF,XNS,YNS,ZNS) BIND(C)                                      
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(IN) :: TOL 
      REAL(W_P), INTENT(OUT) :: VF 
      INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
      INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DX,DY,DZ,EPSILON,F0,F1,F2,F3,F4, &
     &     F5,F6,SUMX,SUMY,SUMZ,VOLF,VOLT,VOLTRI,X,XM,XMAX,XMIN,        &
     &     XP,XV1,XV2,Y,YM,YMAX,YMIN,YP,YV1,YV2,Z,ZM,ZMAX,ZMIN,ZP,ZV1,  &
     &     ZV2                                                          
      INTEGER(I_P) :: I,IAXIS,IC,ICONTN,ICONTP,IE,IEBRACKET,INDEX,IP,   &
     &     IP0,IP1,IS,IS2,ISINI,IV,IV2,JC,KC,NCL,NTP0,NTP1,NTP2,        &
     &     NTPT,NTS0,NTS1,NTS2,NTST,NTSINI,NTV0,NTV1,NTV2,NTVT          
!.. Local Arrays                                                        
      REAL(W_P) :: CS(NS),CS0(NS),CS1(NS),CS2(NS),CST(NS),CX1(NC),      &
     &     CX2(NC),CY1(NC),CY2(NC),CZ1(NC),CZ2(NC),PHIV(NV),V0(3),V1(3),&
     &     V2(3),V3(3),VI(3),VERTP0(NV,3),VERTP1(NV,3),VERTP2(NV,3),    &
     &     VERTPT(NV,3),VIE((NC+1)*(NC+1)*NC,3),VJE((NC+1)*(NC+1)*NC,3),&
     &     VKE((NC+1)*(NC+1)*NC,3),XNS0(NS),XNS1(NS),XNS2(NS),XNST(NS), &
     &     YNS0(NS),YNS1(NS),YNS2(NS),YNST(NS),ZNS0(NS),ZNS1(NS),       &
     &     ZNS2(NS),ZNST(NS)                                            
      INTEGER(I_P) :: IA(NV),ICHECK(NV),IEMARK((NC+1)*(NC+1)*NC),       &
     &     IPIA0(NV),IPIA1(NV),IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),     &
     &     IPVT(NS,NV),ISCUT(NS),JEMARK((NC+1)*(NC+1)*NC),              &
     &     KEMARK((NC+1)*(NC+1)*NC),NIPV0(NS),NIPV1(NS),NIPV2(NS),      &
     &     NIPVT(NS)                                                    
      IF(NC.GT.1) THEN 
         IEMARK=0 
         JEMARK=0 
         KEMARK=0 
      END IF 
!.. Coordinate extremes of the cell and vertex tagging                  
      NCL=NC 
      VF=0.0 
      XMIN=1.0D+20 
      XMAX=-1.0D+20 
      YMIN=1.0D+20 
      YMAX=-1.0D+20 
      ZMIN=1.0D+20 
      ZMAX=-1.0D+20 
      ICONTP=0 
      ICONTN=0 
      V0(1)=0.0 
      V0(2)=0.0 
      V0(3)=0.0 
      DO IP=1,NTP 
         ICHECK(IP)=0 
      END DO 
      DO IS=1,NTS 
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(ICHECK(IP).EQ.0) THEN 
               ICHECK(IP)=1 
               XP=VERTP(IP,1) 
               YP=VERTP(IP,2) 
               ZP=VERTP(IP,3) 
               V0(1)=V0(1)+XP 
               V0(2)=V0(2)+YP 
               V0(3)=V0(3)+ZP 
               XMIN=DMIN1(XMIN,XP) 
               XMAX=DMAX1(XMAX,XP) 
               YMIN=DMIN1(YMIN,YP) 
               YMAX=DMAX1(YMAX,YP) 
               ZMIN=DMIN1(ZMIN,ZP) 
               ZMAX=DMAX1(ZMAX,ZP) 
               PHIV(IP)=FUNC3D(XP,YP,ZP) 
               IF(PHIV(IP).GE.0.0) THEN 
                  IA(IP)=1 
                  ICONTP=ICONTP+1 
               ELSE 
                  IA(IP)=0 
                  ICONTN=ICONTN+1 
               END IF 
            END IF 
         END DO 
      END DO 
!.. initialization                                                      
      DX=XMAX-XMIN 
      DY=YMAX-YMIN 
      DZ=ZMAX-ZMIN 
      IF(NC.GT.1) THEN 
         EPSILON=MAX(DX,DY,DZ)*TOL 
         V0(1)=V0(1)/(ICONTP+ICONTN) 
         V0(2)=V0(2)/(ICONTP+ICONTN) 
         V0(3)=V0(3)/(ICONTP+ICONTN) 
         F0=FUNC3D(V0(1),V0(2),V0(3)) 
         F1=FUNC3D(V0(1)+DX/2._W_P+EPSILON,V0(2),V0(3)) 
         F2=FUNC3D(V0(1)-DX/2._W_P-EPSILON,V0(2),V0(3)) 
         F3=FUNC3D(V0(1),V0(2)+DY/2._W_P+EPSILON,V0(3)) 
         F4=FUNC3D(V0(1),V0(2)-DY/2._W_P-EPSILON,V0(3)) 
         F5=FUNC3D(V0(1),V0(2),V0(3)+DZ/2._W_P+EPSILON) 
         F6=FUNC3D(V0(1),V0(2),V0(3)-DZ/2._W_P-EPSILON) 
      END IF 
      IF((ICONTP.EQ.0.AND.NC.GT.1.AND.MAX(F0,F1,F2,F3,F4,F5,F6).LT.     &
     &     0._W_P).OR.(ICONTP.EQ.0.AND.NC.EQ.1)) THEN                   
            VF=0._W_P 
            RETURN 
      END IF 
      IF((ICONTN.EQ.0.AND.NC.GT.1.AND.MIN(F0,F1,F2,F3,F4,F5,F6).GT.     &
     &     0._W_P).OR.(ICONTN.EQ.0.AND.NC.EQ.1)) THEN                   
            VF=1._W_P 
            RETURN 
      END IF 
      CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,            &
     &     NTS,NTVT,NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)        
!. Root finding using Brent's method                                    
      DD=0.01*MIN(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN) 
      DDX=DX/NCL 
      DDY=DY/NCL 
      DDZ=DZ/NCL 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CX1(I)=-XMIN 
         ELSE 
            CX1(I)=CX1(I-1)-DDX 
         END IF 
         CX2(I)=-CX1(I)+DDX 
      END DO 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CY1(I)=-YMIN 
         ELSE 
            CY1(I)=CY1(I-1)-DDY 
         END IF 
         CY2(I)=-CY1(I)+DDY 
      END DO 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CZ1(I)=-ZMIN 
         ELSE 
            CZ1(I)=CZ1(I-1)-DDZ 
         END IF 
         CZ2(I)=-CZ1(I)+DDZ 
      END DO 
!.. compute the volume VOLT of the original polyhedron                  
      CALL TOOLV3D(IPV,NIPV,NTS,VERTP,VOLT,XNS,YNS,ZNS) 
      DO IC=1,NCL 
         IF(NCL.EQ.1) THEN 
            CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,  &
     &           NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,ZNS0, &
     &           ZNST)                                                  
         ELSE 
            CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,  &
     &           NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,ZNS2, &
     &           ZNST)                                                  
         END IF 
         IF(IC.GT.1) CALL INTE3D(CX1(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
     &        NTS2,NTV2,VERTP2,1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)        
         IF(IC.LT.NCL) CALL INTE3D(CX2(IC),ICONTN,ICONTP,IPV2,NIPV2,    &
     &        NTP2,NTS2,NTV2,VERTP2,-1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)  
         DO JC=1,NCL 
            IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,    &
     &           NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,XNS2, &
     &           YNS1,YNS2,ZNS1,ZNS2)                                   
            IF(JC.GT.1) CALL INTE3D(CY1(JC),ICONTN,ICONTP,IPV1,NIPV1,   &
     &           NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,1.0D0,YNS1,0.0D0,ZNS1)
            IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
               IF(JC.LT.NCL) CALL INTE3D(CY2(JC),ICONTN,ICONTP,IPV1,    &
     &              NIPV1,NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,-1.0D0,YNS1, &
     &              0.0D0,ZNS1)                                         
               IF(ICONTP.NE.0) THEN 
                  DO KC=1,NCL 
                     IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0, &
     &                    NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,   &
     &                    VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
                     IF(KC.GT.1) CALL INTE3D(CZ1(KC),ICONTN,ICONTP,IPV0,&
     &                    NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,XNS0,0.0D0, &
     &                    YNS0,1.0D0,ZNS0)                              
                     IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
                        IF(KC.LT.NCL) CALL INTE3D(CZ2(KC),ICONTN,ICONTP,&
     &                       IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,    &
     &                       XNS0,0.0D0,YNS0,-1.0D0,ZNS0)               
                        IF(ICONTP.NE.0) THEN 
!..   Subcell dedtermination by truncation                              
                           IF(NCL.GT.1) THEN 
                              ICONTP=0 
                              ICONTN=0 
                              DO IP=1,NTP0 
                                 ICHECK(IP)=0 
                              END DO 
                              DO IS=1,NTS0 
                                 DO IV=1,NIPV0(IS) 
                                    IP=IPV0(IS,IV) 
                                    IF(ICHECK(IP).EQ.0) THEN 
                                       ICHECK(IP)=1 
                                       X=VERTP0(IP,1) 
                                       Y=VERTP0(IP,2) 
                                       Z=VERTP0(IP,3) 
                                       PHIV(IP)=FUNC3D(X,Y,Z) 
                                       IF(PHIV(IP).GE.0.0) THEN 
                                          IA(IP)=1 
                                          ICONTP=ICONTP+1 
                                       ELSE 
                                          IA(IP)=0 
                                          ICONTN=ICONTN+1 
                                       END IF 
                                    END IF 
                                 END DO 
                              END DO 
                           END IF 
                           IF(ICONTN.EQ.0) THEN 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
     &                             VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
                              NTSINI=NTS0 
                              CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,        &
     &                             ISCUT,NIPV0,NTP0,NTS0,NTV0,          &
     &                             1.0d0,XNS0,0.0d0,YNS0,0.0d0,         &
     &                             ZNS0)                                
!.. Location of the new intersection points                             
                              IF(NTS0.GT.NTSINI) THEN 
                                 IS=NTS0 
                                 IS2=NTS0 
                                 DO IS=NTSINI+1,NTS0 
                                    SUMX=0.0 
                                    SUMY=0.0 
                                    SUMZ=0.0 
                                    DO IV=1,NIPV0(IS) 
                                       IP=IPV0(IS,IV) 
                                       IP0=IPIA0(IP) 
                                       IP1=IPIA1(IP) 
                                       V0(1)=VERTP0(IP0,1) 
                                       V0(2)=VERTP0(IP0,2) 
                                       V0(3)=VERTP0(IP0,3) 
                                       V1(1)=VERTP0(IP1,1) 
                                       V1(2)=VERTP0(IP1,2) 
                                       V1(3)=VERTP0(IP1,3) 
                                       IF(NC.GT.1) THEN 
                                          CALL EDGEDETECT(DDX,          &
     &                                         DDY,DDZ,IAXIS,IC,JC,KC,  &
     &                                         INDEX,NC,V0,V1,XMIN,YMIN,&
     &                                         ZMIN)                    
                                          IF(IAXIS.EQ.1) THEN 
                                             IF(IEMARK(INDEX).EQ.1)THEN 
                                               VERTP0(IP,1)=VIE(INDEX,1) 
                                               VERTP0(IP,2)=VIE(INDEX,2) 
                                               VERTP0(IP,3)=VIE(INDEX,3) 
                                               GOTO 111 
                                             ELSE 
                                                IEMARK(INDEX)=1 
                                             END IF 
                                          END IF 
                                          IF(IAXIS.EQ.2) THEN 
                                             IF(JEMARK(INDEX).EQ.1)THEN 
                                               VERTP0(IP,1)=VJE(INDEX,1) 
                                               VERTP0(IP,2)=VJE(INDEX,2) 
                                               VERTP0(IP,3)=VJE(INDEX,3) 
                                               GOTO 111 
                                             ELSE 
                                                JEMARK(INDEX)=1 
                                             END IF 
                                          END IF 
                                          IF(IAXIS.EQ.3) THEN 
                                             IF(KEMARK(INDEX).EQ.1)THEN 
                                               VERTP0(IP,1)=VKE(INDEX,1) 
                                               VERTP0(IP,2)=VKE(INDEX,2) 
                                               VERTP0(IP,3)=VKE(INDEX,3) 
                                               GOTO 111 
                                             ELSE 
                                                KEMARK(INDEX)=1 
                                             END IF 
                                          END IF 
                                       END IF 
                                       CALL INTEFUNC3D(MAX(DX,DY,DZ),   &
                                            FUNC3D,IE,V0,V1,VI)                   
                                       IF(IE.EQ.0) THEN 
                                          VERTP0(IP,1)=VI(1) 
                                          VERTP0(IP,2)=VI(2) 
                                          VERTP0(IP,3)=VI(3) 
                                       ELSE 
                                       VERTP0(IP,1)=VERTP0(IP0,1)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      1)-VERTP0(IP0,1))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       VERTP0(IP,2)=VERTP0(IP0,2)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      2)-VERTP0(IP0,2))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       VERTP0(IP,3)=VERTP0(IP0,3)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      3)-VERTP0(IP0,3))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       END IF 
                                       IF(NC.GT.1.AND.IAXIS.NE.0) THEN 
                                          if(iaxis.eq.1) then 
                                             vie(index,1)=vertp0(ip,1) 
                                             vie(index,2)=vertp0(ip,2) 
                                             vie(index,3)=vertp0(ip,3) 
                                          end if 
                                          if(iaxis.eq.2) then 
                                             vje(index,1)=vertp0(ip,1) 
                                             vje(index,2)=vertp0(ip,2) 
                                             vje(index,3)=vertp0(ip,3) 
                                          end if 
                                          if(iaxis.eq.3) then 
                                             vke(index,1)=vertp0(ip,1) 
                                             vke(index,2)=vertp0(ip,2) 
                                             vke(index,3)=vertp0(ip,3) 
                                          end if 
                                       END IF 
  111                                  CONTINUE 
                                       SUMX=SUMX+VERTP0(IP,1) 
                                       SUMY=SUMY+VERTP0(IP,2) 
                                       SUMZ=SUMZ+VERTP0(IP,3) 
                                    END DO 
                                    NTP0=NTP0+1 
                                    VERTP0(NTP0,1)=SUMX/NIPV0(IS) 
                                    VERTP0(NTP0,2)=SUMY/NIPV0(IS) 
                                    VERTP0(NTP0,3)=SUMZ/NIPV0(IS) 
                                    V0(1)=VERTP0(NTP0,1) 
                                    V0(2)=VERTP0(NTP0,2) 
                                    V0(3)=VERTP0(NTP0,3) 
                                    CALL FINDBRACKET(DD/DBLE(NCL),      &
     &                                   FUNC3D,IEBRACKET,V0,V1)        
                                    IF(IEBRACKET.EQ.2) THEN 
                                       VI=V1 
                                    ELSE 
                                       CALL INTEFUNC3D(DD*50.0_W_P/     &
                                            DBLE(NCL),FUNC3D,IE,V0,V1,VI)  
                                    END IF 
                                    IF(IE.EQ.0.OR.IEBRACKET.EQ.2)THEN 
                                       VERTP0(NTP0,1)=VI(1) 
                                       VERTP0(NTP0,2)=VI(2) 
                                       VERTP0(NTP0,3)=VI(3) 
                                    END IF 
                                    ISINI=IS2+1 
                                    DO IV=1,NIPV0(IS) 
                                       IS2=IS2+1 
                                       IV2=IV+1 
                                       IF(IV2.GT.                       &
     &                                      NIPV0(IS)) IV2=1            
                                       NIPV0(IS2)=3 
                                       IPV0(IS2,1)=NTP0 
                                       IPV0(IS2,2)=IPV0(IS,IV) 
                                       IPV0(IS2,3)=IPV0(IS,IV2) 
                                       XV1=VERTP0(IPV0(IS2,2),1)-       &
     &                                      VERTP0(IPV0(IS2,1),1)       
                                       YV1=VERTP0(IPV0(IS2,2),2)-       &
     &                                      VERTP0(IPV0(IS2,1),2)       
                                       ZV1=VERTP0(IPV0(IS2,2),3)-       &
     &                                      VERTP0(IPV0(IS2,1),3)       
                                       XV2=VERTP0(IPV0(IS2,3),1)-       &
     &                                      VERTP0(IPV0(IS2,2),1)       
                                       YV2=VERTP0(IPV0(IS2,3),2)-       &
     &                                      VERTP0(IPV0(IS2,2),2)       
                                       ZV2=VERTP0(IPV0(IS2,3),3)-       &
     &                                      VERTP0(IPV0(IS2,2),3)       
                                       XM=YV1*ZV2-ZV1*YV2 
                                       YM=ZV1*XV2-XV1*ZV2 
                                       ZM=XV1*YV2-YV1*XV2 
                                       AMOD=(XM**2.0+YM**2.0+           &
     &                                      ZM**2.0)**0.5               
                                       IF(AMOD.NE.0.0) THEN 
                                          XNS0(IS2)=XM/AMOD 
                                          YNS0(IS2)=YM/AMOD 
                                          ZNS0(IS2)=ZM/AMOD 
                                       ELSE 
                                          NIPV0(IS2)=0 
                                       END IF 
!..   Gauss quadrature volumes                                          
                                       V1(1)=VERTP0(IPV0(IS2,1),1) 
                                       V1(2)=VERTP0(IPV0(IS2,1),2) 
                                       V1(3)=VERTP0(IPV0(IS2,1),3) 
                                       V2(1)=VERTP0(IPV0(IS2,2),1) 
                                       V2(2)=VERTP0(IPV0(IS2,2),2) 
                                       V2(3)=VERTP0(IPV0(IS2,2),3) 
                                       V3(1)=VERTP0(IPV0(IS2,3),1) 
                                       V3(2)=VERTP0(IPV0(IS2,3),2) 
                                       V3(3)=VERTP0(IPV0(IS2,3),3) 
                                       CALL TRIVOL(FUNC3D,V1,V2,V3,     &
     &                                      VOLTRI)                     
                                       VF=VF+VOLTRI 
                                    END DO 
!* Cancel the IS face                                                   
                                    IF(IS2.GT.IS) NIPV0(IS)=0 
                                 END DO 
                                 NTS0=IS2 
                              end if 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
     &                             VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           END IF 
                        END IF 
                     END IF 
                  END DO 
               END IF 
            END IF 
         END DO 
      END DO 
      VF=VF/VOLT 
      RETURN 
      END                                           
!------------------------ END OF XINITF3DNEW -------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                             EDGEDETECT                              c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! DDX,DDY, = sub-cell size along X, Y, Z                              c 
! DDZ                                                                 c 
! IC,JC,KC = sub-cell indices along X, Y, Z                           c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! VP0,VP1  = vertex coordinates of two points that can be located on  c 
!            an edge of the sub-cell intersected by the hypersurface  c 
! XMIN,YMIN= minimum coordinate values of the domain along X, Y, Z    c 
! ZMIN                                                                c 
! On return:                                                          c 
!===========                                                          c 
! IAXIS    = coordinate axis parallel to the intersected edge         c 
! INDEX    = intersected edge index                                   c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE EDGEDETECT(DDX,DDY,DDZ,IAXIS,IC,JC,KC,INDEX,NC,VP0,VP1,&
     &     XMIN,YMIN,ZMIN) BIND(C)                                      
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(IN) :: DDX,DDY,DDZ,XMIN,YMIN,ZMIN 
      INTEGER(I_P), INTENT(IN) :: IC,JC,KC,NC 
      INTEGER(I_P), INTENT(OUT) :: IAXIS,INDEX 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: VP0(3),VP1(3) 
!.. Local Scalars                                                       
      REAL(W_P) :: FX0,FX1,FY0,FY1,FZ0,FZ1,TOL 
      INTEGER(I_P) :: IE0,IE1,IEDGE0,IEDGE1,IM0,IM1,JE0,JE1,JEDGE0,     &
     &     JEDGE1,JM0,JM1,KE0,KE1,KEDGE0,KEDGE1,KM0,KM1,M0,M1           
      IAXIS=0 
      INDEX=0 
      TOL=1.0E-16_W_P 
!. VP0:                                                                 
      IM0=0 
      JM0=0 
      KM0=0 
      FX0=(VP0(1)-XMIN)/DDX-(REAL(IC, KIND=W_P)-1.0_W_P) 
      IF(ABS(MAX(-FX0,FX0-1.0_W_P)).LT.TOL) IM0=1 
      FY0=(VP0(2)-YMIN)/DDY-(REAL(JC, KIND=W_P)-1.0_W_P) 
      IF(ABS(MAX(-FY0,FY0-1.0_W_P)).LT.TOL) JM0=1 
      FZ0=(VP0(3)-ZMIN)/DDZ-(REAL(KC, KIND=W_P)-1.0_W_P) 
      IF(ABS(MAX(-FZ0,FZ0-1.0_W_P)).LT.TOL) KM0=1 
      M0=IM0+JM0+KM0 
                       ! no intersection                                
      IF(M0.LT.2) THEN 
         RETURN 
      ELSEIF(M0.EQ.2) THEN 
         IE0=IC+IM0*INT(FX0+TOL) 
         JE0=JC+JM0*INT(FY0+TOL) 
         KE0=KC+KM0*INT(FZ0+TOL) 
         IF(IM0.EQ.0) THEN 
            IEDGE0=(KE0-1)*NC*(NC+1)+(JE0-1)*NC+MIN(IC,IE0) 
         ELSE 
            IEDGE0=0 
         END IF 
         IF(JM0.EQ.0) THEN 
            JEDGE0=(KE0-1)*NC*(NC+1)+(MIN(JC,JE0)-1)*(NC+1)+IE0 
         ELSE 
            JEDGE0=0 
         END IF 
         IF(KM0.EQ.0) THEN 
            KEDGE0=(MIN(KC,KE0)-1)*(NC+1)**2+(JE0-1)*(NC+1)+IE0 
         ELSE 
            KEDGE0=0 
         END IF 
      ELSE 
         IE0=IC+IM0*INT(FX0+TOL) 
         JE0=JC+JM0*INT(FY0+TOL) 
         KE0=KC+KM0*INT(FZ0+TOL) 
         IEDGE0=(KE0-1)*NC*(NC+1)+(JE0-1)*NC+MIN(IC,IE0) 
         JEDGE0=(KE0-1)*NC*(NC+1)+(MIN(JC,JE0)-1)*(NC+1)+IE0 
         KEDGE0=(MIN(KC,KE0)-1)*(NC+1)**2+(JE0-1)*(NC+1)+IE0 
      END IF 
!. VP1:                                                                 
      IM1=0 
      JM1=0 
      KM1=0 
      FX1=(VP1(1)-XMIN)/DDX-(REAL(IC, KIND=W_P)-1.0_W_P) 
      IF(ABS(MAX(-FX1,FX1-1.0_W_P)).LT.TOL) IM1=1 
      FY1=(VP1(2)-YMIN)/DDY-(REAL(JC, KIND=W_P)-1.0_W_P) 
      IF(ABS(MAX(-FY1,FY1-1.0_W_P)).LT.TOL) JM1=1 
      FZ1=(VP1(3)-ZMIN)/DDZ-(REAL(KC, KIND=W_P)-1.0_W_P) 
      IF(ABS(MAX(-FZ1,FZ1-1.0_W_P)).LT.TOL) KM1=1 
      M1=IM1+JM1+KM1 
                       ! no intersection                                
      IF(M1.LT.2) THEN 
         RETURN 
      ELSEIF(M1.EQ.2) THEN 
         IE1=IC+IM1*INT(FX1+TOL) 
         JE1=JC+JM1*INT(FY1+TOL) 
         KE1=KC+KM1*INT(FZ1+TOL) 
         IF(IM1.EQ.0) THEN 
            IEDGE1=(KE1-1)*NC*(NC+1)+(JE1-1)*NC+MIN(IC,IE1) 
         ELSE 
            IEDGE1=0 
         END IF 
         IF(JM1.EQ.0) THEN 
            JEDGE1=(KE1-1)*NC*(NC+1)+(MIN(JC,JE1)-1)*(NC+1)+IE1 
         ELSE 
            JEDGE1=0 
         END IF 
         IF(KM1.EQ.0) THEN 
            KEDGE1=(MIN(KC,KE1)-1)*(NC+1)**2+(JE1-1)*(NC+1)+IE1 
         ELSE 
            KEDGE1=0 
         END IF 
      ELSE 
         IE1=IC+IM1*INT(FX1+TOL) 
         JE1=JC+JM1*INT(FY1+TOL) 
         KE1=KC+KM1*INT(FZ1+TOL) 
         IEDGE1=(KE1-1)*NC*(NC+1)+(JE1-1)*NC+MIN(IC,IE1) 
         JEDGE1=(KE1-1)*NC*(NC+1)+(MIN(JC,JE1)-1)*(NC+1)+IE1 
         KEDGE1=(MIN(KC,KE1)-1)*(NC+1)**2+(JE1-1)*(NC+1)+IE1 
      END IF 
      IF(M0.EQ.2.AND.M1.EQ.2.AND.IEDGE0.EQ.IEDGE1.AND.JEDGE0.EQ.JEDGE1  &
     &     .AND.KEDGE0.EQ.KEDGE1) THEN                                   
         IF(IEDGE0.NE.0) THEN 
            IAXIS=1 
            INDEX=IEDGE0 
         ELSEIF(JEDGE0.NE.0) THEN 
            IAXIS=2 
            INDEX=JEDGE0 
         ELSE 
            IAXIS=3 
            INDEX=KEDGE0 
         END IF 
      ELSEIF((M0.EQ.3.OR.M1.EQ.3).AND.(IEDGE0.EQ.IEDGE1.OR.JEDGE0.EQ.   &
     &        JEDGE1.OR.KEDGE0.EQ.KEDGE1)) THEN                         
         IF(IEDGE0.EQ.IEDGE1) THEN 
            IAXIS=1 
            INDEX=IEDGE0 
         ELSEIF(JEDGE0.EQ.JEDGE1) THEN 
            IAXIS=2 
            INDEX=JEDGE0 
         ELSE 
            IAXIS=3 
            INDEX=KEDGE0 
         END IF 
      END IF 
      RETURN 
      END SUBROUTINE EDGEDETECT 
!------------------------- END OF EDGEDETECT -------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                           XINITF3DCHECK                             c 
!. This version checks the face boundaries to correct the quadrature  c 
!. points                                                             c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! IPV      = array containing the global indices of the original pol. c 
!            vertices                                                 c 
! NC       = number of sub-cells along each coordinate axis of the    c 
!            superimposed Cartesian grid                              c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! NTV      = total number of vertices                                 c 
! TOL      = prescribed positive tolerance for the distance to the    c 
!            interface                                                c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! VF       = material volume fraction                                 c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE XINITF3DCHECK(FUNC3D,IPV,NC,NIPV,NTP,NTS,NTV,TOL,      &
     &     VERTP,VF,XNS,YNS,ZNS) BIND(C)                                
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(IN) :: TOL 
      REAL(W_P), INTENT(OUT) :: VF 
      INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
      INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: AMOD,DD,DDX,DDY,DDZ,DX,DY,DZ,EPSILON,F0,PHI,PHI0,    &
     &     PHIMIN,PHIMIN2,SUMX,SUMY,SUMZ,VOLF,VOLT,VOLTRI,X,XI,XM,XMAX, &
     &     XMIN,XP,XV1,XV2,Y,YI,YM,YMAX,YMIN,YP,YV1,YV2,Z,ZI,ZM,ZMAX,   &
     &     ZMIN,ZP,ZV1,ZV2                                              
      INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IE,IEBRACKET,IOUT,IP,IP0,IP1,  &
     &     IPHI,IS,IS2,ISC,ISINI,IST,IV,IV2,JC,KC,NCL,NTP0,NTP1,NTP2,   &
     &     NTPT,NTS0,NTS1,NTS2,NTSC,NTST,NTSINI,NTV0,NTV1,NTV2,NTVT     
!.. Local Arrays                                                        
      REAL(W_P) :: CS(NS),CS0(NS),CS1(NS),CS2(NS),CSC(NS),CST(NS),      &
     &     CX1(MAX(2,NC)),CX2(MAX(2,NC)),CY1(MAX(2,NC)),CY2(MAX(2,NC)), &
     &     CZ1(MAX(2,NC)),CZ2(MAX(2,NC)),PHIV(NV),                      &
     &     V0(3),V1(3),V2(3),V3(3),VI(3),VERTP0(NV,3),VERTP1(NV,3),     &
     &     VERTP2(NV,3),VERTPT(NV,3),XNS0(NS),XNS1(NS),XNS2(NS),        &
     &     XNSC(NS),XNST(NS),YNS0(NS),YNS1(NS),YNS2(NS),YNSC(NS),       &
     &     YNST(NS),ZNS0(NS),ZNS1(NS),ZNS2(NS),ZNSC(NS),ZNST(NS)        
      INTEGER(I_P) :: IA(NV),ICHECK(NV),IPIA0(NV),IPIA1(NV),            &
     &     IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),IPVT(NS,NV),ISCUT(NS),   &
     &     NIPV0(NS),NIPV1(NS),NIPV2(NS),NIPVT(NS)                      
!.. Coordinate extremes of the cell and vertex tagging                  
      NCL=NC 
      VF=0.0 
      XMIN=1.0D+20 
      XMAX=-1.0D+20 
      YMIN=1.0D+20 
      YMAX=-1.0D+20 
      ZMIN=1.0D+20 
      ZMAX=-1.0D+20 
      ICONTP=0 
      ICONTN=0 
      V0(1)=0.0 
      V0(2)=0.0 
      V0(3)=0.0 
      PHIMIN=1D+20 
      DO IP=1,NTP 
         ICHECK(IP)=0 
      END DO 
      DO IS=1,NTS 
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(ICHECK(IP).EQ.0) THEN 
               ICHECK(IP)=1 
               XP=VERTP(IP,1) 
               YP=VERTP(IP,2) 
               ZP=VERTP(IP,3) 
               V0(1)=V0(1)+XP 
               V0(2)=V0(2)+YP 
               V0(3)=V0(3)+ZP 
               XMIN=DMIN1(XMIN,XP) 
               XMAX=DMAX1(XMAX,XP) 
               YMIN=DMIN1(YMIN,YP) 
               YMAX=DMAX1(YMAX,YP) 
               ZMIN=DMIN1(ZMIN,ZP) 
               ZMAX=DMAX1(ZMAX,ZP) 
               PHIV(IP)=FUNC3D(XP,YP,ZP) 
               PHIMIN=MIN(PHIMIN,ABS(PHIV(IP))) 
               IF(PHIV(IP).GE.0.0) THEN 
                  IA(IP)=1 
                  ICONTP=ICONTP+1 
               ELSE 
                  IA(IP)=0 
                  ICONTN=ICONTN+1 
               END IF 
            END IF 
         END DO 
      END DO 
!.. initialization                                                      
      DX=XMAX-XMIN 
      DY=YMAX-YMIN 
      DZ=ZMAX-ZMIN 
      EPSILON=MAX(DX,DY,DZ)*TOL 
      IPHI=0 
!      PHIMIN=10.0*DMAX1(DX,DY,DZ)                                      
!      DO IS=1,NTS                                                      
!         DO IV=1,NIPV(IS)                                              
!            IP=IPV(IS,IV)                                              
!            PHIMIN=DMIN1(PHIMIN,ABS(PHIV(IP)))                        
!         END DO                                                        
!      END DO                                                           
      IF(PHIMIN.LT.EPSILON) IPHI=1 
      IF(IPHI.EQ.0) THEN 
         IF(ICONTP.EQ.NTV) THEN 
            VF=1.0 
            RETURN 
         END IF 
         IF(ICONTN.EQ.NTV) THEN 
            VF=0.0 
            RETURN 
         END IF 
      END IF 
!----                                                                   
      IF(ICONTP.EQ.0.AND.NC.EQ.1) NCL=2 
      IF(ICONTN.EQ.0.AND.NC.EQ.1) NCL=2 
!----                                                                   
      CALL CPPOL3D(CST,CS,IPVT,IPV,NIPVT,NIPV,NTPT,NTP,NTST,            &
     &     NTS,NTVT,NTV,VERTPT,VERTP,XNST,XNS,YNST,YNS,ZNST,ZNS)        
!. Root finding using Brent's method                                    
      DD=0.01*MIN(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN) 
!     Quitar la condicion NC.EQ.1. Hacer para cualquier NC.             
!     VI sera el punto de control.                                      
!     Si no se encuentra VI, hacer VI=V0 y forzar la division:          
!     Este seria el caso de una esfera centrada en la celda.            
!     Para determinar la division que debe pasar por el punto de control
!     hago:                                                             
!     ICONTROL=MAX(1,MIN(NC-1,INT(NC*(VI(1)-XMIN)/(XMAX-XMIN)+0.5)))    
!     JCONTROL=MAX(1,MIN(NC-1,INT(NC*(VI(2)-YMIN)/(YMAX-YMIN)+0.5)))    
!     KCONTROL=MAX(1,MIN(NC-1,INT(NC*(VI(3)-ZMIN)/(ZMAX-ZMIN)+0.5)))    
!     Despues hacer                                                     
!     CX2(ICONTROL)=VI(1); CX1(ICONTROL+1)=-VI(1)                       
!     CY2(JCONTROL)=VI(2); CY1(JCONTROL+1)=-VI(2)                       
!     CZ2(KCONTROL)=VI(3); CZ1(KCONTROL+1)=-VI(3)                       
!     Ojo, las expresiones anteriores valen si VI esta entre limites    
!      IF(NC.EQ.1) THEN                                                 
      V0(1)=V0(1)/(ICONTP+ICONTN) 
      V0(2)=V0(2)/(ICONTP+ICONTN) 
      V0(3)=V0(3)/(ICONTP+ICONTN) 
      F0=FUNC3D(V0(1),V0(2),V0(3)) 
      IF((ICONTP.EQ.0.AND.F0.GE.0.0).OR.(ICONTN.EQ.0.AND.               &
     &     F0.LE.0.0)) THEN                                             
         VI=V0 
         IF(NC.EQ.1) THEN 
            NCL=2 
         END IF 
!      ELSE                                                             
!         ICONTROL=0                                                    
!         JCONTROL=0                                                    
!         KCONTROL=0                                                    
!         CALL FINDBRACKET(DFX,DFY,DFZ,DD,FUNC3D,IEBRACKET,V0,V1)       
!         IF(IEBRACKET.NE.-1) THEN                                      
!            IF(IEBRACKET.EQ.2) THEN                                    
!               VI=V1                                                   
!            ELSE                                                       
!               CALL INTEFUNC3D(FUNC3D,IE,NITER,V0,V1,VI)               
!            END IF                                                     
!            IF(IE.EQ.0.OR.IEBRACKET.EQ.2) THEN                         
!               ICONTP2=0                                               
!               ICONTN2=0                                               
!               CPLIC=-(DFX*VI(1)+DFY*VI(2)+DFZ*VI(3))                  
!               DO IP=1,NTP                                             
!                  IF(ICHECK(IP).EQ.1) THEN                             
!                     PHI2=DFX*VERTPT(IP,1)+DFY*VERTPT(IP,2)+DFZ*       
!     -                    VERTPT(IP,3)+CPLIC                           
!                     IF(PHI2.LT.0.0) THEN                              
!                        ICONTN2=ICONTN2+1                              
!                     ELSE                                              
!                        ICONTP2=ICONTP2+1                              
!                     END IF                                            
!                  END IF                                               
!               END DO                                                  
!               IF((ICONTP*ICONTN.EQ.0.AND.ICONTP2*ICONTN2.NE.0).OR.    
!     -              (ICONTP*ICONTN.NE.0.AND.ICONTP2*ICONTN2.EQ.0)) THEN
!C.. SI NC=1 FORZAR REFINAMIENTO                                        
!                  IF(NC.EQ.1) THEN                                     
!                     IF(VI(1).GT.XMIN.AND.VI(1).LT.XMAX) NCX=2         
!                     IF(VI(2).GT.YMIN.AND.VI(2).LT.YMAX) NCY=2         
!                     IF(VI(3).GT.ZMIN.AND.VI(3).LT.ZMAX) NCZ=2         
!                  END IF                                               
!               END IF                                                  
!            END IF                                                     
!         ELSE                                                          
!            VI=V0                                                      
!            IF(NC.EQ.1) THEN                                           
!               NCX=2                                                   
!               NCY=2                                                   
!               NCZ=2                                                   
!            END IF                                                     
!         END IF                                                        
      END IF 
!      IF(VI(1).GT.XMIN.AND.VI(1).LT.XMAX.AND.NCX.GT.1) ICONTROL=MAX(1, 
!     -     MIN(NCX-1,INT(NCX*(VI(1)-XMIN)/(XMAX-XMIN)+0.5)))           
!      IF(VI(2).GT.YMIN.AND.VI(2).LT.YMAX.AND.NCY.GT.1) JCONTROL=MAX(1, 
!     -     MIN(NCY-1,INT(NCY*(VI(2)-YMIN)/(YMAX-YMIN)+0.5)))           
!      IF(VI(3).GT.ZMIN.AND.VI(3).LT.ZMAX.AND.NCZ.GT.1) KCONTROL=MAX(1, 
!     -     MIN(NCZ-1,INT(NCZ*(VI(3)-ZMIN)/(ZMAX-ZMIN)+0.5)))           
                                                                        
!      IF(VI(2).GT.YMIN.AND.VI(2).LT.YMAX) THEN                         
!         NCY=2                                                         
!         CY1(1)=-YMIN                                                  
!         CY2(1)=VI(2)                                                  
!         CY1(2)=-VI(2)                                                 
!         CY2(2)=YMAX                                                   
!      END IF                                                           
!      IF(VI(3).GT.ZMIN.AND.VI(3).LT.ZMAX) THEN                         
!         NCZ=2                                                         
!         CZ1(1)=-ZMIN                                                  
!         CZ2(1)=VI(3)                                                  
!         CZ1(2)=-VI(3)                                                 
!         CZ2(2)=ZMAX                                                   
!      END IF                                                           
!      ELSE                                                             
      DDX=DX/NCL 
      DDY=DY/NCL 
      DDZ=DZ/NCL 
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CX1(I)=-XMIN 
         ELSE 
            CX1(I)=CX1(I-1)-DDX 
         END IF 
         CX2(I)=-CX1(I)+DDX 
      END DO 
!      IF(ICONTROL.NE.0) THEN                                           
!         CX2(ICONTROL)=VI(1)                                           
!         CX1(ICONTROL+1)=-VI(1)                                        
!      END IF                                                           
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CY1(I)=-YMIN 
         ELSE 
            CY1(I)=CY1(I-1)-DDY 
         END IF 
         CY2(I)=-CY1(I)+DDY 
      END DO 
!      IF(JCONTROL.NE.0) THEN                                           
!         CY2(JCONTROL)=VI(2)                                           
!         CY1(JCONTROL+1)=-VI(2)                                        
!      END IF                                                           
      DO I=1,NCL 
         IF(I.EQ.1) THEN 
            CZ1(I)=-ZMIN 
         ELSE 
            CZ1(I)=CZ1(I-1)-DDZ 
         END IF 
         CZ2(I)=-CZ1(I)+DDZ 
      END DO 
!      IF(KCONTROL.NE.0) THEN                                           
!         CZ2(KCONTROL)=VI(3)                                           
!         CZ1(KCONTROL+1)=-VI(3)                                        
!      END IF                                                           
                                                                        
                                                                        
!      END IF                                                           
!-----------------------------------                                    
!      DX=XMAX-XMIN                                                     
!      DY=YMAX-YMIN                                                     
!      DZ=ZMAX-ZMIN                                                     
!++++      DD=0.05*MIN(DX,DY,DZ)                                        
                                                                        
!.. compute the volume VOLT of the original polyhedron                  
      CALL TOOLV3D(IPV,NIPV,NTS,VERTP,VOLT,XNS,YNS,ZNS) 
!      DDX=DX/NC                                                        
!      DDY=DY/NC                                                        
!      DDZ=DZ/NC                                                        
                                                                        
      DO IC=1,NCL 
!         XC=XMIN+(IC-1)*DDX                                            
!         CALL CPPOL3D(CS2,CS,IPV2,IPV,NIPV2,NIPV,NTP2,NTP,NTS2,        
!     -        NTS,NTV2,NTV,VERTP2,VERTP,XNS2,XNS,YNS2,YNS,ZNS2,ZNS)    
         IF(NCL.EQ.1) THEN 
            CALL CPPOL3D(CS0,CST,IPV0,IPVT,NIPV0,NIPVT,NTP0,NTPT,NTS0,  &
     &           NTST,NTV0,NTVT,VERTP0,VERTPT,XNS0,XNST,YNS0,YNST,ZNS0, &
     &           ZNST)                                                  
         ELSE 
            CALL CPPOL3D(CS2,CST,IPV2,IPVT,NIPV2,NIPVT,NTP2,NTPT,NTS2,  &
     &           NTST,NTV2,NTVT,VERTP2,VERTPT,XNS2,XNST,YNS2,YNST,ZNS2, &
     &           ZNST)                                                  
         END IF 
!         CX1=-XC                                                       
         IF(IC.GT.1) CALL INTE3D(CX1(IC),ICONTN,ICONTP,IPV2,NIPV2,NTP2, &
     &        NTS2,NTV2,VERTP2,1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)        
!         CX2=XC+DDX                                                    
         IF(IC.LT.NCL) CALL INTE3D(CX2(IC),ICONTN,ICONTP,IPV2,NIPV2,    &
     &        NTP2,NTS2,NTV2,VERTP2,-1.0D0,XNS2,0.0D0,YNS2,0.0D0,ZNS2)  
         DO JC=1,NCL 
!            YC=YMIN+(JC-1)*DDY                                         
            IF(NCL.GT.1) CALL CPPOL3D(CS1,CS2,IPV1,IPV2,NIPV1,NIPV2,    &
     &           NTP1,NTP2,NTS1,NTS2,NTV1,NTV2,VERTP1,VERTP2,XNS1,XNS2, &
     &           YNS1,YNS2,ZNS1,ZNS2)                                   
!            CY1=-YC                                                    
            IF(JC.GT.1) CALL INTE3D(CY1(JC),ICONTN,ICONTP,IPV1,NIPV1,   &
     &           NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,1.0D0,YNS1,0.0D0,ZNS1)
            IF(ICONTP.NE.0.OR.JC.EQ.1) THEN 
!               CY2=YC+DDY                                              
               IF(JC.LT.NCL) CALL INTE3D(CY2(JC),ICONTN,ICONTP,IPV1,    &
     &              NIPV1,NTP1,NTS1,NTV1,VERTP1,0.0D0,XNS1,-1.0D0,YNS1, &
     &              0.0D0,ZNS1)                                         
               IF(ICONTP.NE.0) THEN 
                  DO KC=1,NCL 
!                     ZC=ZMIN+(KC-1)*DDZ                                
                     IF(NCL.GT.1) CALL CPPOL3D(CS0,CS1,IPV0,IPV1,NIPV0, &
     &                    NIPV1,NTP0,NTP1,NTS0,NTS1,NTV0,NTV1,VERTP0,   &
     &                    VERTP1,XNS0,XNS1,YNS0,YNS1,ZNS0,ZNS1)         
!                     CZ1=-ZC                                           
                     IF(KC.GT.1) CALL INTE3D(CZ1(KC),ICONTN,ICONTP,IPV0,&
     &                    NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,XNS0,0.0D0, &
     &                    YNS0,1.0D0,ZNS0)                              
                     IF(ICONTP.NE.0.OR.KC.EQ.1) THEN 
!                        CZ2=ZC+DDZ                                     
                        IF(KC.LT.NCL) CALL INTE3D(CZ2(KC),ICONTN,ICONTP,&
     &                       IPV0,NIPV0,NTP0,NTS0,NTV0,VERTP0,0.0D0,    &
     &                       XNS0,0.0D0,YNS0,-1.0D0,ZNS0)               
                        IF(ICONTP.NE.0) THEN 
!..   Subcell dedtermination by truncation                              
                           IF(NCL.GT.1) THEN 
                              ICONTP=0 
                              ICONTN=0 
                              DO IP=1,NTP0 
                                 ICHECK(IP)=0 
                              END DO 
                              DO IS=1,NTS0 
                                 DO IV=1,NIPV0(IS) 
                                    IP=IPV0(IS,IV) 
                                    IF(ICHECK(IP).EQ.0) THEN 
                                       ICHECK(IP)=1 
                                       X=VERTP0(IP,1) 
                                       Y=VERTP0(IP,2) 
                                       Z=VERTP0(IP,3) 
                                       PHIV(IP)=FUNC3D(X,Y,Z) 
                                       IF(PHIV(IP).GE.0.0) THEN 
                                          IA(IP)=1 
                                          ICONTP=ICONTP+1 
                                       ELSE 
                                          IA(IP)=0 
                                          ICONTN=ICONTN+1 
                                       END IF 
                                    END IF 
                                 END DO 
                              END DO 
                           END IF 
                           IF(ICONTN.EQ.0) THEN 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
     &                             VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
!                  write(6,*)'->',volf,ic,jc,kc                         
                           ELSEIF(ICONTN.GT.0.AND.ICONTP.GT.0)THEN 
!-------                                                                
                              NTSC=0 
                              DO IS=1,NTS0 
                                 DO IV=1,NIPV0(IS) 
                                    IF(IV.EQ.1) THEN 
                                       IP=IPV0(IS,IV) 
                                       NTSC=NTSC+1 
                                       XNSC(NTSC)=XNS0(IS) 
                                       YNSC(NTSC)=YNS0(IS) 
                                       ZNSC(NTSC)=ZNS0(IS) 
                                       CSC(NTSC)=-1._W_P*(VERTP0(IP,1)* &
     &                                      XNS0(IS)+VERTP0(IP,2)*      &
     &                                      YNS0(IS)+VERTP0(IP,3)*      &
     &                                      ZNS0(IS))                   
                                    END IF 
                                 END DO 
                              END DO 
!-------                                                                
                              NTSINI=NTS0 
                              CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,        &
     &                             ISCUT,NIPV0,NTP0,NTS0,NTV0,          &
     &                             1.0d0,XNS0,0.0d0,YNS0,0.0d0,         &
     &                             ZNS0)                                
!.. Location of the new intersection points                             
                              IF(NTS0.GT.NTSINI) THEN 
                                 IS=NTS0 
                                 IS2=NTS0 
                                 DO IS=NTSINI+1,NTS0 
                                    SUMX=0.0 
                                    SUMY=0.0 
                                    SUMZ=0.0 
                                    DO IV=1,NIPV0(IS) 
                                       IP=IPV0(IS,IV) 
                                       IP0=IPIA0(IP) 
                                       IP1=IPIA1(IP) 
                                       V0(1)=VERTP0(IP0,1) 
                                       V0(2)=VERTP0(IP0,2) 
                                       V0(3)=VERTP0(IP0,3) 
                                       V1(1)=VERTP0(IP1,1) 
                                       V1(2)=VERTP0(IP1,2) 
                                       V1(3)=VERTP0(IP1,3) 
!---                                                                    
                                       CALL INTEFUNC3D(MAX(DX,DY,DZ),   &
                                            FUNC3D,IE,V0,V1,VI)                   
                                       IF(IE.EQ.0) THEN 
                                          VERTP0(IP,1)=VI(1) 
                                          VERTP0(IP,2)=VI(2) 
                                          VERTP0(IP,3)=VI(3) 
                                       ELSE 
!---                                                                    
                                       VERTP0(IP,1)=VERTP0(IP0,1)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      1)-VERTP0(IP0,1))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       VERTP0(IP,2)=VERTP0(IP0,2)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      2)-VERTP0(IP0,2))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       VERTP0(IP,3)=VERTP0(IP0,3)-      &
     &                                      PHIV(IP0)*(VERTP0(IP1,      &
     &                                      3)-VERTP0(IP0,3))/(         &
     &                                      PHIV(IP1)-PHIV(IP0))        
                                       END IF 
                                       SUMX=SUMX+VERTP0(IP,1) 
                                       SUMY=SUMY+VERTP0(IP,2) 
                                       SUMZ=SUMZ+VERTP0(IP,3) 
                                    END DO 
                                    NTP0=NTP0+1 
                                    VERTP0(NTP0,1)=SUMX/NIPV0(IS) 
                                    VERTP0(NTP0,2)=SUMY/NIPV0(IS) 
                                    VERTP0(NTP0,3)=SUMZ/NIPV0(IS) 
!---                                                                    
                                    V0(1)=VERTP0(NTP0,1) 
                                    V0(2)=VERTP0(NTP0,2) 
                                    V0(3)=VERTP0(NTP0,3) 
!. OJO, SI LA SUPERFICIE ES CONCAVA HABRIA QUE CAMBIAR A -XNV, ...      
!                                       V1(1)=V0(1)+XNV*DD/DBLE(NC)     
!                                       V1(2)=V0(2)+YNV*DD/DBLE(NC)     
!                                       V1(3)=V0(3)+ZNV*DD/DBLE(NC)     
                                    CALL FINDBRACKET(DD/DBLE(NCL),      &
     &                                   FUNC3D,IEBRACKET,V0,V1)        
                                    IF(IEBRACKET.EQ.2) THEN 
                                       VI=V1 
                                    ELSE 
                                       CALL INTEFUNC3D(DD*50.0_W_P/     &
                                            DBLE(NCL),FUNC3D,IE,V0,V1,VI) 
                                    END IF 
                                    IF(IE.EQ.0.OR.IEBRACKET.EQ.2)THEN 
!-----                                                                  
                                       IOUT=0 
                                       PHIMIN2=1D+20 
                                       DO ISC=1,NTSC 
                                          PHI=VI(1)*XNSC(ISC)+VI(2)*    &
     &                                         YNSC(ISC)+VI(3)*ZNSC(ISC)&
     &                                         +CSC(ISC)                
                                          IF(PHI.GT.0.0) THEN 
                                             IF(PHI.LT.PHIMIN2) THEN 
                                                IOUT=1 
                                                PHIMIN2=PHI 
                                                PHI0=VERTP0(NTP0,1)*    &
     &                                               XNSC(ISC)+VERTP0(  &
     &                                               NTP0,2)*YNSC(ISC)+ &
     &                                               VERTP0(NTP0,3)*    &
     &                                               ZNSC(ISC)+CSC(ISC) 
                                             END IF 
                                          END IF 
                                       END DO 
                                       IF(IOUT.EQ.1) THEN 
                                          XI=VI(1) 
                                          YI=VI(2) 
                                          ZI=VI(3) 
                                          X=VERTP0(NTP0,1) 
                                          Y=VERTP0(NTP0,2) 
                                          Z=VERTP0(NTP0,3) 
                                          VI(1)=-(PHI0*XI-X*PHIMIN2)/   &
     &                                         (PHIMIN2-PHI0)           
                                          VI(2)=-(PHI0*YI-Y*PHIMIN2)/   &
     &                                         (PHIMIN2-PHI0)           
                                          VI(3)=-(PHI0*ZI-Z*PHIMIN2)/   &
     &                                         (PHIMIN2-PHI0)           
                                       END IF 
!-----                                                                  
                                       VERTP0(NTP0,1)=VI(1) 
                                       VERTP0(NTP0,2)=VI(2) 
                                       VERTP0(NTP0,3)=VI(3) 
                                    END IF 
!---                                                                    
!: The new face IS is replaced by NIPV(IS) triangular faces             
!                                    XNV=0.0                            
!                                    YNV=0.0                            
!                                    ZNV=0.0                            
                                    ISINI=IS2+1 
                                    DO IV=1,NIPV0(IS) 
                                       IS2=IS2+1 
                                       IV2=IV+1 
                                       IF(IV2.GT.                       &
     &                                      NIPV0(IS)) IV2=1            
                                       NIPV0(IS2)=3 
                                       IPV0(IS2,1)=NTP0 
                                       IPV0(IS2,2)=IPV0(IS,IV) 
                                       IPV0(IS2,3)=IPV0(IS,IV2) 
                                       XV1=VERTP0(IPV0(IS2,2),1)-       &
     &                                      VERTP0(IPV0(IS2,1),1)       
                                       YV1=VERTP0(IPV0(IS2,2),2)-       &
     &                                      VERTP0(IPV0(IS2,1),2)       
                                       ZV1=VERTP0(IPV0(IS2,2),3)-       &
     &                                      VERTP0(IPV0(IS2,1),3)       
                                       XV2=VERTP0(IPV0(IS2,3),1)-       &
     &                                      VERTP0(IPV0(IS2,2),1)       
                                       YV2=VERTP0(IPV0(IS2,3),2)-       &
     &                                      VERTP0(IPV0(IS2,2),2)       
                                       ZV2=VERTP0(IPV0(IS2,3),3)-       &
     &                                      VERTP0(IPV0(IS2,2),3)       
                                       XM=YV1*ZV2-ZV1*YV2 
                                       YM=ZV1*XV2-XV1*ZV2 
                                       ZM=XV1*YV2-YV1*XV2 
                                       AMOD=(XM**2.0+YM**2.0+           &
     &                                      ZM**2.0)**0.5               
                                       IF(AMOD.NE.0.0) THEN 
                                          XNS0(IS2)=XM/AMOD 
                                          YNS0(IS2)=YM/AMOD 
                                          ZNS0(IS2)=ZM/AMOD 
                                       ELSE 
                                          NIPV0(IS2)=0 
                                       END IF 
!..   Gauss quadrature volumes                                          
                                       V1(1)=VERTP0(IPV0(IS2,1),1) 
                                       V1(2)=VERTP0(IPV0(IS2,1),2) 
                                       V1(3)=VERTP0(IPV0(IS2,1),3) 
                                       V2(1)=VERTP0(IPV0(IS2,2),1) 
                                       V2(2)=VERTP0(IPV0(IS2,2),2) 
                                       V2(3)=VERTP0(IPV0(IS2,2),3) 
                                       V3(1)=VERTP0(IPV0(IS2,3),1) 
                                       V3(2)=VERTP0(IPV0(IS2,3),2) 
                                       V3(3)=VERTP0(IPV0(IS2,3),3) 
!                                       CALL TRIVOL(FUNC3D,V1,V2,V3,    
!     -                                      VOLTRI)                    
                                       CALL TRIVOLC(CSC,FUNC3D,NTSC,V1, &
     &                                      V2,V3,VOLTRI,XNSC,YNSC,ZNSC)
                                       VF=VF+VOLTRI 
                                    END DO 
!                                    AMOD=(XM**2.0+YM**2.0+             
!     -                                   ZM**2.0)**0.5                 
!                                    IF(AMOD.NE.0.0) THEN               
!c                                       XNV=XNV/AMOD                   
!c                                       YNV=YNV/AMOD                   
!c                                       ZNV=ZNV/AMOD                   
!C                                       V0(1)=VERTP0(NTP0,1)           
!                                       V0(2)=VERTP0(NTP0,2)            
!                                       V0(3)=VERTP0(NTP0,3)            
!c. OJO, SI LA SUPERFICIE ES CONCAVA HABRIA QUE CAMBIAR A -XNV, ...     
!c                                       V1(1)=V0(1)+XNV*DD/DBLE(NC)    
!c                                       V1(2)=V0(2)+YNV*DD/DBLE(NC)    
!c                                       V1(3)=V0(3)+ZNV*DD/DBLE(NC)    
!                                       CALL FINDBRACKET(DFX,DFY,DFZ,   
!     -                                      DD/DBLE(NC),FUNC3D,        
!     -                                      IEBRACKET,V0,V1)           
!                                       IF(IEBRACKET.EQ.2) THEN         
!                                          VI=V1                        
!                                       ELSE                            
!                                          CALL INTEFUNC3D(FUNC3D,IE,   
!     -                                         NITER,V0,V1,VI)         
!                                       END IF                          
!                                       IF(IE.EQ.0.OR.IEBRACKET.EQ.2)THE
!                                          VERTP0(NTP0,1)=VI(1)         
!                                          VERTP0(NTP0,2)=VI(2)         
!                                          VERTP0(NTP0,3)=VI(3)         
!. Compute again the normal vectors of the triangular-cap faces         
!                                          DO IST=ISINI,IS2             
!                                             XV1=VERTP0(IPV0(IST,2),1)-
!     -                                            VERTP0(IPV0(IST,1),1)
!                                             YV1=VERTP0(IPV0(IST,2),2)-
!     -                                            VERTP0(IPV0(IST,1),2)
!                                             ZV1=VERTP0(IPV0(IST,2),3)-
!     -                                            VERTP0(IPV0(IST,1),3)
!                                             XV2=VERTP0(IPV0(IST,3),1)-
!     -                                            VERTP0(IPV0(IST,2),1)
!                                             YV2=VERTP0(IPV0(IST,3),2)-
!     -                                            VERTP0(IPV0(IST,2),2)
!                                             ZV2=VERTP0(IPV0(IST,3),3)-
!     -                                            VERTP0(IPV0(IST,2),3)
!                                             XM=YV1*ZV2-ZV1*YV2        
!                                             YM=ZV1*XV2-XV1*ZV2        
!                                             ZM=XV1*YV2-YV1*XV2        
!                                             AMOD=(XM**2.0+YM**2.0+    
!     -                                            ZM**2.0)**0.5        
!                                             IF(AMOD.NE.0.0) THEN      
!                                                XNS0(IST)=XM/AMOD      
!                                                YNS0(IST)=YM/AMOD      
!                                                ZNS0(IST)=ZM/AMOD      
!                                             END IF                    
!                                          END DO                       
!                                       END IF                          
!                                    END IF                             
                                                                        
!* Cancel the IS face                                                   
                                    IF(IS2.GT.IS) NIPV0(IS)=0 
                                 END DO 
                                 NTS0=IS2 
                              end if 
                              CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,      &
     &                             VOLF,XNS0,YNS0,ZNS0)                 
                              VF=VF+VOLF 
                           END IF 
                        END IF 
                     END IF 
                  END DO 
               END IF 
            END IF 
         END DO 
      END DO 
      VF=VF/VOLT 
      RETURN 
      END                                           
!---------------------- END OF XINITF3DCHECK -------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                              TRIVOLC                                c 
! This version takes into account the bounds of the polyhedron faces  c 
! to compute the quadrature points                                    c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! CSC      = position of each boundary face                           c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! NTSC     = number of boundary faces                                 c 
! V1,V2,V3 = coordinates of the three triangle vertices               c 
! XNSC,... = components of the vector normal to each boundary face    c 
! On return:                                                          c 
!===========                                                          c 
! VOLTRI   = Gaussian quadrature volume                               c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE TRIVOLC(CSC,FUNC3D,NTSC,V1,V2,V3,VOLTRI,XNSC,YNSC,ZNSC)&
     &     BIND(C)                                                      
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(OUT) :: VOLTRI 
      INTEGER(I_P), INTENT(IN) :: NTSC 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: CSC(NS),V1(3),V2(3),V3(3),XNSC(NS),      &
     &     YNSC(NS),ZNSC(NS)                                            
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: A,D,DD,DFX,DFY,DFZ,DMOD,F0,PHI,PHI0,PHIMIN,S,T,      &
     &     VOLGAUSS,W,X,X1,X2,X3,XI,XMAX,XMIN,XN,XNU,XV1,XV2,Y,Y1,Y2,Y3,&
     &     YI,YMAX,YMIN,YN,YNU,YV1,YV2,Z,Z1,Z2,Z3,ZI,ZMAX,ZMIN,ZN,ZNU,  &
     &     ZV1,ZV2                                                      
      INTEGER(I_P) :: IE,IEBRACKET,IGAUSS,IN,IORDER,IOUT,IP1,IP2,IS,IV, &
     &     NGAUSS                                                       
!.. Local Arrays                                                        
      REAL(W_P) :: P0(3),P1(3),PI(3),SGAUSS(10),TGAUSS(10),WGAUSS(10) 
      XMAX=MAX(V1(1),V2(1),V3(1)) 
      XMIN=MIN(V1(1),V2(1),V3(1)) 
      YMAX=MAX(V1(2),V2(2),V3(2)) 
      YMIN=MIN(V1(2),V2(2),V3(2)) 
      ZMAX=MAX(V1(3),V2(3),V3(3)) 
      ZMIN=MIN(V1(3),V2(3),V3(3)) 
      DD=0.1*MAX(XMAX-XMIN,YMAX-YMIN,ZMAX-ZMIN) 
!. Gauss quadrature points                                              
!. [Pavel Solin, Karel Segeth, Ivo Dolezel, Higher-order finite element 
!. methods, Chapman & Hall, CRC, Boca Raton, 2004]                      
                                ! Parece que el orden 2 es suficiente   
      IORDER=2 
      IF(IORDER.EQ.2) THEN 
         NGAUSS=3 
         SGAUSS(1)=1./6.0 
         TGAUSS(1)=1./6.0 
         SGAUSS(2)=2./3.0 
         TGAUSS(2)=1./6.0 
         SGAUSS(3)=1./6.0 
         TGAUSS(3)=2./3.0 
         WGAUSS(1)=1./3. 
         WGAUSS(2)=1./3. 
         WGAUSS(3)=1./3. 
      ELSEIF(IORDER.EQ.3) THEN 
         NGAUSS=4 
         SGAUSS(1)=1./3. 
         TGAUSS(1)=1./3. 
         SGAUSS(2)=1./5. 
         TGAUSS(2)=3./5. 
         SGAUSS(3)=1./5. 
         TGAUSS(3)=1./5. 
         SGAUSS(4)=3./5. 
         TGAUSS(4)=1./5. 
         WGAUSS(1)=-27./48. 
         WGAUSS(2)=25./48. 
         WGAUSS(3)=25./48. 
         WGAUSS(4)=25./48. 
      ELSEIF(IORDER.EQ.4) THEN 
         NGAUSS=6 
         SGAUSS(1)=(1.0-0.108103018168070)/2. 
         TGAUSS(1)=(1.0-0.108103018168070)/2. 
         SGAUSS(2)=(1.0-0.108103018168070)/2. 
         TGAUSS(2)=(1.0-0.783793963663860)/2. 
         SGAUSS(3)=(1.0-0.783793963663860)/2. 
         TGAUSS(3)=(1.0-0.108103018168070)/2. 
         SGAUSS(4)=(1.0-0.816847572980458)/2. 
         TGAUSS(4)=(1.0-0.816847572980458)/2. 
         SGAUSS(5)=(1.0-0.816847572980458)/2. 
         TGAUSS(5)=(1.0+0.633695145960918)/2. 
         SGAUSS(6)=(1.0+0.633695145960918)/2. 
         TGAUSS(6)=(1.0-0.816847572980458)/2. 
         WGAUSS(1)=0.446763179356022/2. 
         WGAUSS(2)=WGAUSS(1) 
         WGAUSS(3)=WGAUSS(1) 
         WGAUSS(4)=0.219903487310644/2. 
         WGAUSS(5)=WGAUSS(4) 
         WGAUSS(6)=WGAUSS(4) 
      ELSEIF(IORDER.EQ.5) THEN 
         NGAUSS=7 
         SGAUSS(1)=1./3. 
         TGAUSS(1)=1./3. 
         SGAUSS(2)=(1.0-0.059715871789770)/2. 
         TGAUSS(2)=(1.0-0.059715871789770)/2. 
         SGAUSS(3)=(1.0-0.059715871789770)/2. 
         TGAUSS(3)=(1.0-0.880568256420460)/2. 
         SGAUSS(4)=(1.0-0.880568256420460)/2. 
         TGAUSS(4)=(1.0-0.059715871789770)/2. 
         SGAUSS(5)=(1.0-0.797426985353088)/2. 
         TGAUSS(5)=(1.0-0.797426985353088)/2. 
         SGAUSS(6)=(1.0-0.797426985353088)/2. 
         TGAUSS(6)=(1.0+0.594853970706174)/2. 
         SGAUSS(7)=(1.0+0.594853970706174)/2. 
         TGAUSS(7)=(1.0-0.797426985353088)/2. 
         WGAUSS(1)=0.225 
         WGAUSS(2)=0.264788305577012/2. 
         WGAUSS(3)=WGAUSS(2) 
         WGAUSS(4)=WGAUSS(2) 
         WGAUSS(5)=0.251878361089654/2. 
         WGAUSS(6)=WGAUSS(5) 
         WGAUSS(7)=WGAUSS(5) 
      END IF 
!. Vector normal to the triangle                                        
      XV1=V2(1)-V1(1) 
      YV1=V2(2)-V1(2) 
      ZV1=V2(3)-V1(3) 
      XV2=V3(1)-V1(1) 
      YV2=V3(2)-V1(2) 
      ZV2=V3(3)-V1(3) 
      XN=YV1*ZV2-ZV1*YV2 
      YN=ZV1*XV2-XV1*ZV2 
      ZN=XV1*YV2-YV1*XV2 
      DMOD=(XN**2+YN**2+ZN**2)**0.5 
!      write(6,*)'Triangle area:',A                                     
!. Unit-length normal vector                                            
      IF(DMOD.NE.0.0) THEN 
         XNU=XN/DMOD 
         YNU=YN/DMOD 
         ZNU=ZN/DMOD 
      ELSE 
         VOLTRI=0.0 
         RETURN 
      END IF 
!. Triangle area                                                        
      A=DMOD/2D0 
!. Projection plane: IN=1: YZ, IN=2: XZ, IN=3: XY                       
      IF((ABS(XN).GE.ABS(YN)).AND.(ABS(XN).GE.ABS(ZN))) THEN 
         IN=1 
      ELSEIF((ABS(YN).GE.ABS(XN)).AND.(ABS(YN).GE.ABS(ZN))) THEN 
         IN=2 
      ELSE 
         IN=3 
      END IF 
!      write(6,*)'----IN',IN,XN,YN,ZN                                   
      VOLTRI=0.0 
! Local reference sistem (S,T), GAUSS WEIGHT W                          
      DO IGAUSS=1,NGAUSS 
         S=SGAUSS(IGAUSS) 
         T=TGAUSS(IGAUSS) 
         W=WGAUSS(IGAUSS) 
                                ! YZ                                    
         IF(IN.EQ.1) THEN 
            Y=V1(2)+(V2(2)-V1(2))*S+(V3(2)-V1(2))*T 
            Z=V1(3)+(V2(3)-V1(3))*S+(V3(3)-V1(3))*T 
            X=V1(1)+YNU*(V1(2)-Y)/XNU+ZNU*(V1(3)-Z)/XNU 
                                ! XZ                                    
         ELSEIF(IN.EQ.2) THEN 
            X=V1(1)+(V2(1)-V1(1))*S+(V3(1)-V1(1))*T 
            Z=V1(3)+(V2(3)-V1(3))*S+(V3(3)-V1(3))*T 
            Y=V1(2)+XNU*(V1(1)-X)/YNU+ZNU*(V1(3)-Z)/YNU 
                                ! XY                                    
         ELSE 
            X=V1(1)+(V2(1)-V1(1))*S+(V3(1)-V1(1))*T 
            Y=V1(2)+(V2(2)-V1(2))*S+(V3(2)-V1(2))*T 
            Z=V1(3)+XNU*(V1(1)-X)/ZNU+YNU*(V1(2)-Y)/ZNU 
         END IF 
         P0(1)=X 
         P0(2)=Y 
         P0(3)=Z 
         CALL FINDBRACKET(DD,FUNC3D,IEBRACKET,P0,P1) 
         IF(IEBRACKET.EQ.2) THEN 
            PI=P1 
         ELSE 
            CALL INTEFUNC3D(DD*50.0_W_P,FUNC3D,IE,P0,P1,PI) 
         END IF 
         F0=FUNC3D(X,Y,Z) 
         IF(IE.EQ.0) THEN 
!------                                                                 
            IOUT=0 
            PHIMIN=1D+20 
            DO IS=1,NTSC 
               PHI=PI(1)*XNSC(IS)+PI(2)*YNSC(IS)+PI(3)*ZNSC(IS)+        &
     &              CSC(IS)                                             
               IF(PHI.GT.0.0) THEN 
                  IF(PHI.LT.PHIMIN) THEN 
                     IOUT=1 
                     PHIMIN=PHI 
                     PHI0=X*XNSC(IS)+Y*YNSC(IS)+Z*ZNSC(IS)+CSC(IS) 
                  END IF 
               END IF 
            END DO 
            IF(IOUT.EQ.1) THEN 
               XI=PI(1) 
               YI=PI(2) 
               ZI=PI(3) 
               PI(1)=-(PHI0*XI-X*PHIMIN)/(PHIMIN-PHI0) 
               PI(2)=-(PHI0*YI-Y*PHIMIN)/(PHIMIN-PHI0) 
               PI(3)=-(PHI0*ZI-Z*PHIMIN)/(PHIMIN-PHI0) 
            END IF 
!-----                                                                  
            D=SIGN(((X-PI(1))**2+(Y-PI(2))**2+(Z-PI(3))**2)**0.5,F0) 
            VOLTRI=VOLTRI+W*D*A 
         ELSE 
            VOLTRI=VOLTRI+W*F0*A 
         ENDIF 
      END DO 
      RETURN 
      END                                           
!------------------------ END OF  TRIVOLC ----------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                            FINDBRACKET                              c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! DD       = differential size                                        c 
! V0       = vertex coordinates of the initial point                  c 
! On return:                                                          c 
!===========                                                          c 
! IEBRACKET= 2, the root is found                                     c 
!            1, the bracket is found                                  c 
!            0, the bracket is not found                              c 
!           -1, null space gradient case                              c 
! V0       = vertex coordinates of the relocated initial point        c 
! V1       = vertex coordinates of the final point with FUNC3D value  c 
!            of different sign                                        c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE FINDBRACKET(DD,FUNC3D,IEBRACKET,V0,V1) BIND(C) 
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(IN) :: DD 
      INTEGER(I_P), INTENT(OUT) :: IEBRACKET 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(INOUT) :: V0(3) 
      REAL(W_P), INTENT(OUT) :: V1(3) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: BBALL,DFX,DFY,DFZ,DMOD,F0,F0INI,F1,TOLB 
      INTEGER(I_P) :: ITER,NITER 
!.. Local Arrays                                                        
      REAL(W_P) :: V00(3)                                              
!. normal computation                                                   
      NITER=10 
      ITER=0 
      V00=V0                                                           
      TOLB=1D-12
      BBALL=DD*50.0_W_P !equivalent to half the size of a cubic cell
                                                                        
      F0=FUNC3D(V0(1)-DD,V0(2),V0(3)) 
      F1=FUNC3D(V0(1)+DD,V0(2),V0(3)) 
      DFX=(F1-F0)/(2.0*DD) 
      F0=FUNC3D(V0(1),V0(2)-DD,V0(3)) 
      F1=FUNC3D(V0(1),V0(2)+DD,V0(3)) 
      DFY=(F1-F0)/(2.0*DD) 
      F0=FUNC3D(V0(1),V0(2),V0(3)-DD) 
      F1=FUNC3D(V0(1),V0(2),V0(3)+DD) 
      DFZ=(F1-F0)/(2.0*DD) 
      DMOD=(DFX**2+DFY**2+DFZ**2)**0.5 
      IF(DMOD.NE.0.0) THEN 
!. find bracket                                                         
         DFX=DFX/DMOD 
         DFY=DFY/DMOD 
         DFZ=DFZ/DMOD 
         F0=FUNC3D(V0(1),V0(2),V0(3)) 
         F0INI=F0 
   10    CONTINUE 
         ITER=ITER+1 
         V1(1)=V0(1)-DFX*SIGN(MAX(ABS(F0),DD),F0) 
         V1(2)=V0(2)-DFY*SIGN(MAX(ABS(F0),DD),F0) 
         V1(3)=V0(3)-DFZ*SIGN(MAX(ABS(F0),DD),F0)
         IF(((V00(1)-V1(1))**2+(V00(2)-V1(2))**2+(V00(3)-V1(3))**2)**   &
              0.5_W_P.GT.BBALL) THEN
            IEBRACKET=0
            RETURN
         END IF
         F1=FUNC3D(V1(1),V1(2),V1(3)) 
         IF(ABS(F1).LT.TOLB) THEN 
            IEBRACKET=2 
            RETURN 
         END IF 
         IF(F1*F0INI.LE.0.0) THEN 
            IEBRACKET=1 
            RETURN 
         END IF 
         IF(ITER.EQ.NITER) THEN 
            IEBRACKET=0 
            RETURN 
         END IF 
         F0=F1 
         V0=V1 
         GOTO 10 
      ELSE 
         IEBRACKET=-1 
      END IF 
      RETURN 
      END                                           
!----------------------- END OF FINDBRACKET --------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c
!---------------------------------------------------------------------c
!                           FINDBRACKETN                              c
!---------------------------------------------------------------------c
! On entry:                                                           c
!==========                                                           c
! FUNC3D   = external user-supplied function where the interface      c
!            shape is analytically defined                            c
! DD       = differential size                                        c
! V0       = vertex coordinates of the initial point                  c
! VN       = normal direction in which the solution must be brackettedc
! On return:                                                          c
!===========                                                          c
! IEBRACKET= 2, the root is found                                     c
!            1, the bracket is found                                  c
!            0, the bracket is not found                              c
! V0       = vertex coordinates of the relocated initial point        c
! V1       = vertex coordinates of the final point with FUNC3D value  c
!            of different sign                                        c
!---------------------------------------------------------------------c
!---------------------------------------------------------------------c
      SUBROUTINE FINDBRACKETN(DD,FUNC3D,IEBRACKET,V0,V1,VN) BIND(C,     &
           NAME="findbracketn")
!.. Scalar Arguments
      REAL(W_P), INTENT(IN) :: DD
      INTEGER(I_P), INTENT(OUT) :: IEBRACKET
!.. Array Arguments
      REAL(W_P), INTENT(IN) :: VN(3)
      REAL(W_P), INTENT(INOUT) :: V0(3)
      REAL(W_P), INTENT(OUT) :: V1(3)
!.. Procedure Arguments 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D
!.. Local Scalars 
      REAL(W_P) :: BBALL,DFX,DFY,DFZ,DMOD,F0,F0INI,F1,TOLB
      INTEGER(I_P) :: ITER,NITER
!.. Locall Arrays
      REAL(W_P) :: V00(3)
      
      NITER=10
      ITER=0
      TOLB=1D-12
      V00=V0
      BBALL=DD*50.0_W_P
      DFX=VN(1)
      DFY=VN(2)
      DFZ=VN(3)
      F0=FUNC3D(V0(1),V0(2),V0(3))
      F0INI=F0
10    CONTINUE
      ITER=ITER+1
      V1(1)=V0(1)+DFX*SIGN(MAX(ABS(F0),DD),F0)
      V1(2)=V0(2)+DFY*SIGN(MAX(ABS(F0),DD),F0)
      V1(3)=V0(3)+DFZ*SIGN(MAX(ABS(F0),DD),F0)
      IF(((V00(1)-V1(1))**2+(V00(2)-V1(2))**2+(V00(3)-V1(3))**2)**      &
           0.5_W_P.GT.BBALL) THEN
         IEBRACKET=0
         RETURN
      END IF
      F1=FUNC3D(V1(1),V1(2),V1(3))
      IF(ABS(F1).LT.TOLB) THEN
         IEBRACKET=2
         RETURN
      END IF
      IF(F1*F0INI.LE.0.0) THEN
         IEBRACKET=1
         RETURN
      END IF
      IF(ITER.EQ.NITER) THEN
         IEBRACKET=0
         RETURN
      END IF
      F0=F1
      V0=V1
      GOTO 10
      RETURN
    END SUBROUTINE FINDBRACKETN
!----------------------- END OF FINDBRACKETN -------------------------c
!---------------------------------------------------------------------c      
!---------------------------------------------------------------------c
!---------------------------------------------------------------------c
!                           FINDBRACKETNM                             c
!---------------------------------------------------------------------c
! On entry:                                                           c
!==========                                                           c
! FCOEF    = array containing the coefficients for the multi implict  c 
!            functions definition                                     c 
! DD       = differential size                                        c
! V0       = vertex coordinates of the initial point                  c
! VN       = normal direction in which the solution must be brackettedc
! On return:                                                          c
!===========                                                          c
! IEBRACKET= 2, the root is found                                     c
!            1, the bracket is found                                  c
!            0, the bracket is not found                              c
! V0       = vertex coordinates of the relocated initial point        c
! V1       = vertex coordinates of the final point with FUNC3D value  c
!            of different sign                                        c
!---------------------------------------------------------------------c
!---------------------------------------------------------------------c
      SUBROUTINE FINDBRACKETNM(DD,FCOEF,IEBRACKET,V0,V1,VN) BIND(C,     &
           NAME="findbracketnm")
!.. Scalar Arguments
      REAL(W_P), INTENT(IN) :: DD
      INTEGER(I_P), INTENT(OUT) :: IEBRACKET
!.. Array Arguments
      REAL(W_P), INTENT(IN) :: VN(3)
      REAL(W_P), INTENT(INOUT) :: V0(3)
      REAL(W_P), INTENT(OUT) :: V1(3)
      REAL(W_P), INTENT(IN) :: FCOEF(10000) 
! FCOEF(1) = number of implicit functions ('+' sign means union and
!            '-' sign means intersection)                               
! FCOEF(2) = number of terms of the implicit function 1                 
! FCOEF(3) = 0 for global system; 1 for local system                    
! FCOEF(4-6) = xyz-coordinates of the system-reference origin           
! FCOEF(7-15) = xyz-components of the normal vectors that define the    
!               orthonormal reference system                            
! FCOEF(16) = number of subterms of term 1 of the implicit function 1   
! FCOEF(17,18) = coefficient and exponent of term 1 of imp. funct. 1    
! FCOEF(19-22) = C1,C2,C3,C4 coefficients of the first subterm of term 1
!                of imp. funct. 1: C1 X^C2 Y^C3 Z^C4                    
! Follow the same pattern for the rest of information                   
!.. Local Scalars 
      REAL(W_P) :: BBALL,DFX,DFY,DFZ,DMOD,F0,F0INI,F1,TOLB
      INTEGER(I_P) :: ITER,NITER
!.. Local Arrays
      REAL(W_P) :: V00(3)
      NITER=10
      ITER=0
      TOLB=1D-12
      V00=V0
      BBALL=DD*50.0_W_P
      DFX=VN(1)
      DFY=VN(2)
      DFZ=VN(3)
      CALL MFUNC3D(F0,FCOEF,V0(1),V0(2),V0(3)) 
      F0INI=F0
10    CONTINUE
      ITER=ITER+1
      V1(1)=V0(1)+DFX*SIGN(MAX(ABS(F0),DD),F0)
      V1(2)=V0(2)+DFY*SIGN(MAX(ABS(F0),DD),F0)
      V1(3)=V0(3)+DFZ*SIGN(MAX(ABS(F0),DD),F0)
      IF(((V00(1)-V1(1))**2+(V00(2)-V1(2))**2+(V00(3)-V1(3))**2)**      &
           0.5_W_P.GT.BBALL) THEN
         IEBRACKET=0
         RETURN
      END IF
      CALL MFUNC3D(F1,FCOEF,V1(1),V1(2),V1(3)) 
      IF(ABS(F1).LT.TOLB) THEN
         IEBRACKET=2
         RETURN
      END IF
      IF(F1*F0INI.LE.0.0) THEN
         IEBRACKET=1
         RETURN
      END IF
      IF(ITER.EQ.NITER) THEN
         IEBRACKET=0
         RETURN
      END IF
      F0=F1
      V0=V1
      GOTO 10
      RETURN
    END SUBROUTINE FINDBRACKETNM
!----------------------- END OF FINDBRACKETNM ------------------------c
!---------------------------------------------------------------------c      
!---------------------------------------------------------------------c
!---------------------------------------------------------------------c
!                           FINDBRACKETNP                             c
!---------------------------------------------------------------------c
! On entry:                                                           c
!==========                                                           c
! CPARAB   = local paraboloid coefficients                            c
!            shape is analytically defined                            c
! VPN      = paraboloid orthonormal basis                             c
! DD       = differential size                                        c
! V0       = vertex coordinates of the initial point                  c
! VN       = normal direction in which the solution must be brackettedc
! On return:                                                          c
!===========                                                          c
! IEBRACKET= 2, the root is found                                     c
!            1, the bracket is found                                  c
!            0, the bracket is not found                              c
! V0       = vertex coordinates of the relocated initial point        c
! V1       = vertex coordinates of the final point with FUNC3D value  c
!            of different sign                                        c
!---------------------------------------------------------------------c
!---------------------------------------------------------------------c
      SUBROUTINE FINDBRACKETNP(CPARAB,VPN,DD,IEBRACKET,V0,V1,VN) BIND(C,&
           NAME="findbracketnp")
!.. Scalar Arguments
      REAL(W_P), INTENT(IN) :: DD
      INTEGER(I_P), INTENT(OUT) :: IEBRACKET
!.. Array Arguments
      REAL(W_P), INTENT(IN) :: CPARAB(12),VN(3),VPN(9)
      REAL(W_P), INTENT(INOUT) :: V0(3)
      REAL(W_P), INTENT(OUT) :: V1(3)
!.. Local Scalars 
      REAL(W_P) :: BBALL,DFX,DFY,DFZ,DMOD,F0,F0INI,F1,TOLB
      INTEGER(I_P) :: ITER,NITER
!.. Local Arrays
      REAL(W_P) :: V00(3)
      
      NITER=10
      ITER=0
      TOLB=1D-12
      V00=V0
      BBALL=DD*50.0_W_P
      DFX=VN(1)
      DFY=VN(2)
      DFZ=VN(3)
      CALL PFUNC3D(F0,CPARAB,VPN,V0(1),V0(2),V0(3))
         F0INI=F0
 10      CONTINUE
         ITER=ITER+1
         V1(1)=V0(1)+DFX*SIGN(MAX(ABS(F0),DD),F0)
         V1(2)=V0(2)+DFY*SIGN(MAX(ABS(F0),DD),F0)
         V1(3)=V0(3)+DFZ*SIGN(MAX(ABS(F0),DD),F0)
         IF(((V00(1)-V1(1))**2+(V00(2)-V1(2))**2+(V00(3)-V1(3))**2)**   &
              0.5_W_P.GT.BBALL) THEN
            IEBRACKET=0
            RETURN
         END IF
         CALL PFUNC3D(F1,CPARAB,VPN,V1(1),V1(2),V1(3))
         IF(ABS(F1).LT.TOLB) THEN
            IEBRACKET=2
            RETURN
         END IF
         IF(F1*F0INI.LE.0.0) THEN
            IEBRACKET=1
            RETURN
         END IF
         IF(ITER.EQ.NITER.OR.(F0*F1.GT.0.0_W_P.AND.ABS(F1).GT.ABS(F0))) &
              THEN 
            IEBRACKET=0
            RETURN
         END IF
         F0=F1
         V0=V1
         GOTO 10
      RETURN
      END
!----------------------- END OF FINDBRACKETNP ------------------------c
!---------------------------------------------------------------------c      
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                           FINDBRACKETM                              c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FCOEF    = array containing the coefficients for the multi implict  c 
!            functions definition                                     c 
! DD       = differential size                                        c 
! V0       = vertex coordinates of the initial point                  c 
! On return:                                                          c 
!===========                                                          c 
! IEBRACKET= 2, the root is found                                     c 
!            1, the bracket is found                                  c 
!            0, the bracket is not found                              c 
!           -1, null space gradient case                              c 
! V0       = vertex coordinates of the relocated initial point        c 
! V1       = vertex coordinates of the final point with FUNC3D value  c 
!            of different sign                                        c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE FINDBRACKETM(DD,FCOEF,IEBRACKET,V0,V1) BIND(C) 
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(IN) :: DD 
      INTEGER(I_P), INTENT(OUT) :: IEBRACKET 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: FCOEF(10000) 
! FCOEF(1) = number of implicit functions ('+' sign means union and
!            '-' sign means intersection)                               
! FCOEF(2) = 2, index position of FCOEF where the information if the    
!            implicit function 1 begins                                 
! FCOEF(3) = 0 for global system; 1 for local system                    
! FCOEF(4-6) = xyz-coordinates of the system-reference origin           
! FCOEF(7-15) = xyz-components of the normal vectors that define the    
!               orthonormal reference system                            
! FCOEF(16-19) = C1,C2,C3,C4 coeficients of the first term of the       
!                implicit function 1: C1 X^C2 Y^C3 Z^C4                 
! Follow the same pattern for the rest of information                   
      REAL(W_P), INTENT(INOUT) :: V0(3) 
      REAL(W_P), INTENT(OUT) :: V1(3) 
!.. Local Scalars                                                       
      REAL(W_P) :: BBALL,DFX,DFY,DFZ,DMOD,F0,F0INI,F1,TOLB 
      INTEGER(I_P) :: ITER,NITER 
!.. Local Arrays                                                        
      REAL(W_P) :: V00(3)                                              
!. normal computation                                                   
      NITER=10 
      ITER=0 
      TOLB=1D-12
      V00=V0
      BBALL=DD*50.0_W_P
                                                                        
      CALL MFUNC3D(F0,FCOEF,V0(1)-DD,V0(2),V0(3)) 
      CALL MFUNC3D(F1,FCOEF,V0(1)+DD,V0(2),V0(3)) 
      DFX=(F1-F0)/(2.0*DD) 
      CALL MFUNC3D(F0,FCOEF,V0(1),V0(2)-DD,V0(3)) 
      CALL MFUNC3D(F1,FCOEF,V0(1),V0(2)+DD,V0(3)) 
      DFY=(F1-F0)/(2.0*DD) 
      CALL MFUNC3D(F0,FCOEF,V0(1),V0(2),V0(3)-DD) 
      CALL MFUNC3D(F1,FCOEF,V0(1),V0(2),V0(3)+DD) 
      DFZ=(F1-F0)/(2.0*DD) 
      DMOD=(DFX**2+DFY**2+DFZ**2)**0.5 
      IF(DMOD.NE.0.0) THEN 
!. find bracket                                                         
         DFX=DFX/DMOD 
         DFY=DFY/DMOD 
         DFZ=DFZ/DMOD 
         CALL MFUNC3D(F0,FCOEF,V0(1),V0(2),V0(3)) 
         F0INI=F0 
   10    CONTINUE 
         ITER=ITER+1 
         V1(1)=V0(1)-DFX*SIGN(MAX(ABS(F0),DD),F0) 
         V1(2)=V0(2)-DFY*SIGN(MAX(ABS(F0),DD),F0) 
         V1(3)=V0(3)-DFZ*SIGN(MAX(ABS(F0),DD),F0) 
         IF(((V00(1)-V1(1))**2+(V00(2)-V1(2))**2+(V00(3)-V1(3))**2)**   &
              0.5_W_P.GT.BBALL) THEN
            IEBRACKET=0
            RETURN
         END IF
         CALL MFUNC3D(F1,FCOEF,V1(1),V1(2),V1(3)) 
         IF(ABS(F1).LT.TOLB) THEN 
            IEBRACKET=2 
            RETURN 
         END IF 
         IF(F1*F0INI.LE.0.0) THEN 
            IEBRACKET=1 
            RETURN 
         END IF 
         IF(ITER.EQ.NITER) THEN 
            IEBRACKET=0 
            RETURN 
         END IF 
         F0=F1 
         V0=V1 
         GOTO 10 
      ELSE 
         IEBRACKET=-1 
      END IF 
      RETURN 
      END                                           
!----------------------- END OF FINDBRACKETM -------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                            INTEFUNC3D                               c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! BBALL    = bounding ball                                            c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! V0       = vertex coordinates of the initial point                  c 
! V1       = vertex coordinates of the next point along the line      c 
!            where the root is been searching                         c 
! On return:                                                          c 
!===========                                                          c 
! IE       = 0, if the root is found; 1, otherwise                    c 
! VI       = vertex coordinates of the point of intersection between  c 
!            the line and the hypersurface                            c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE INTEFUNC3D(BBALL,FUNC3D,IE,V0,V1,VI) BIND(C) 
!.. Scalar Arguments                                                    
        INTEGER(I_P), INTENT(OUT) :: IE
        REAL(W_P), INTENT(IN) :: BBALL
!.. Array Arguments                                                     
      REAL(W_P), INTENT(INOUT) :: V0(3),V1(3) 
      REAL(W_P), INTENT(OUT) :: VI(3) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: D,D0,D1,DF,F0,F1,FI,FIQ,Q,R,S,T,TOLB 
      INTEGER(I_P) :: I,IBRACKET,ITER,NITER 
!.. Local Arrays                                                        
      REAL(W_P) :: P(3),V0INIT(3),V1INIT(3),VIQ(3) 
!. Root finding using Brent's method                                    
      TOLB=1D-12 
      NITER=100
      F0=FUNC3D(V0(1),V0(2),V0(3)) 
      F1=FUNC3D(V1(1),V1(2),V1(3)) 
      IF(ABS(F0).LT.TOLB)THEN 
         VI=V0 
         IE=0 
         RETURN 
      END IF 
      IF(ABS(F1).LT.TOLB)THEN 
         VI=V1 
         IE=0 
         RETURN 
      END IF 
      V0INIT=V0 
      V1INIT=V1 
      IF(F0*F1.LT.0.0) THEN 
                    ! bracketed init                                    
         IBRACKET=1 
!         D=((V0(1)-V1(1))**2+(V0(2)-V1(2))**2+(V0(3)-V1(3))**2)**0.5 
      ELSE 
         IBRACKET=0 
!..   PROBAR A ENCONTRAR UN NUEVO PUNTO 1: V1=V1-F1*VN                  
!..   VN ES LA DIRECCION DE LA LINEA DE INTERSECCION.                   
!..   EL PROCESO SE PUDEDE REPETIR UN NUMERO MAXIMO DE VECES HASTA      
!..   ENCONTRAR UN V1 TAL QUE F0*F1<0                                   
      END IF 
      IF((F1-F0).EQ.0.0_W_P) THEN
         IE=1
         RETURN
      END IF
      DO ITER=1,NITER 
!. Secant interpolation                                                 
         DF=-F0/(F1-F0) 
         DO I=1,3 
            VI(I)=V0(I)*(1.0-DF)+V1(I)*DF 
         END DO 
         D0=((V0INIT(1)-VI(1))**2+(V0INIT(2)-VI(2))**2+(V0INIT(3)-VI(3) &
              )**2)**0.5_W_P
         D1=((V1INIT(1)-VI(1))**2+(V1INIT(2)-VI(2))**2+(V1INIT(3)-VI(3) &
              )**2)**0.5_W_P
         FI=FUNC3D(VI(1),VI(2),VI(3)) 
!----                                                                   
         IF(ABS(FI).LT.TOLB) THEN 
            IE=0 
            GOTO 10 
         ELSEIF(FI/F0.GT.1.0.OR.FI/F1.GT.1.0.OR.D0.GT.BBALL.OR.D1.GT.   &
              BBALL) THEN 
!. Bisection                                                            
            VI=(V0+V1)/2.0 
            FI=FUNC3D(VI(1),VI(2),VI(3)) 
         END IF 
!----                                                                   
!. Inverse-quadratic interpolation                                      
         R=FI/F1 
         S=FI/F0 
         T=F0/F1 
         Q=(T-1.0)*(R-1.0)*(S-1.0)
         IF(Q.EQ.0.0_W_P) THEN
            IE=1
            RETURN
         END IF
         DO I=1,3 
            P(I)=S*(T*(R-T)*(V1(I)-VI(I))-(1.0-R)*(VI(I)-V0(I))) 
            VIQ(I)=VI(I)+P(I)/Q 
         END DO 
         FIQ=FUNC3D(VIQ(1),VIQ(2),VIQ(3)) 
                                ! check bracketting                     
         IF(IBRACKET.EQ.1) THEN 
!            D0=((V0INIT(1)-VIQ(1))**2+(V0INIT(2)-VIQ(2))**2+(V0INIT(3)- &
!     &           VIQ(3))**2)**0.5                                       
!            D1=((V1INIT(1)-VIQ(1))**2+(V1INIT(2)-VIQ(2))**2+(V1INIT(3)- &
!     &           VIQ(3))**2)**0.5                                       
            D0=((V0(1)-VIQ(1))**2+(V0(2)-VIQ(2))**2+(V0(3)-VIQ(3))**2   &
                 )**0.5_W_P
            D1=((V1(1)-VIQ(1))**2+(V1(2)-VIQ(2))**2+(V1(3)-VIQ(3))**2   &
                 )**0.5_W_P
            D=((V0(1)-V1(1))**2+(V0(2)-V1(2))**2+(V0(3)-V1(3))**2)**0.5 
            IF(MAX(D0,D1).LT.(D*(1.0_W_P-1.0E-1_W_P))) THEN 
               VI=VIQ 
               FI=FIQ
            ELSE
               !. Bisection
               VI=(V0+V1)/2.0 
               FI=FUNC3D(VI(1),VI(2),VI(3))                
            END IF
         END IF 
         IF(ABS(FI).LT.TOLB) THEN 
            IE=0 
            GOTO 10 
         END IF 
         IF(FI*F1.GT.0.0) THEN 
            DO I=1,3 
               V1(I)=VI(I) 
            END DO 
            F1=FI 
         ELSE 
            DO I=1,3 
               V0(I)=VI(I) 
            END DO 
            F0=FI 
         END IF 
      END DO 
      IE=1 
   10 CONTINUE 
      RETURN 
      END                                           
!------------------------- END OF INTEFUNC3D -------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                               MFUNC3D                               | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! FCOEF    = array containing the coefficients for the multi implict  | 
!            functions definition                                     | 
! X,Y,Z    = coordinates of the point where VALUE is computed         | 
! On return:                                                          | 
!===========                                                          | 
! A        = value of the multi-implicit interface shape functions:   | 
!            > 0 (inside the interface), < 0 (outside the             | 
!            interface); = 0 (on the interface)                       | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
      SUBROUTINE MFUNC3D(A,FCOEF,X,Y,Z) BIND(C) 
        !.. Scalar Arguments                                                    
        REAL(W_P), INTENT(IN) :: X,Y,Z 
        REAL(W_P), INTENT(OUT) :: A 
        !.. Array Arguments                                                     
        REAL(W_P), INTENT(IN) :: FCOEF(10000) 
        ! FCOEF(1) = number of implicit functions ('+' sign means union and
        !            '-' sign means intersection)                              
        ! FCOEF(2) = number of terms of the implicit function 1                 
        ! FCOEF(3) = 0 for global system; 1 for local system                    
        ! FCOEF(4-6) = xyz-coordinates of the system-reference origin           
        ! FCOEF(7-15) = xyz-components of the normal vectors that define the    
        !               orthonormal reference system                            
        ! FCOEF(16) = number of subterms of term 1 of the implicit function 1   
        ! FCOEF(17,18) = coefficient and exponent of term 1 of imp. funct. 1    
        ! FCOEF(19)    = type of first subterm of term 1    
        ! FCOEF(20-23) = C1,C2,C3,C4 coefficients of the first subterm of term 1
        !                of imp. funct. 1: C1 X^C2 Y^C3 Z^C4                    
        ! Follow the same pattern for the rest of information                   
        !.. Local Scalars                                                       
        INTEGER(I_P) :: IFUNC,IREF,ISTERM,ITERM,ITYPE,JPOSF,NFUNC,      &
             NSTERM,NTERM 
        REAL(W_P) :: C0,C1,C2,C3,C4,C5,FSUM,FSUM2,XN1,XN2,XN3,XT,XV,YN1,&
             YN2,YN3,YT,YV,ZN1,ZN2,ZN3,ZT,ZV                              
        !.. Local Arrays                                                        
        ! index of FCOEF where the information  
        INTEGER(I_P) :: IPOSF(100) 
        ! of implicit function J begins       
        !     IPOSF(1)=2                                                        
        IF(FCOEF(1).GT.0.0_W_P) THEN
           A=-1.0E+20_W_P
        ELSE
           A=1.0E+20_W_P
        END IF
        NFUNC=INT(ABS(FCOEF(1)),KIND=I_P) 
        DO IFUNC=1,NFUNC 
           IF(IFUNC.EQ.1) THEN 
              IPOSF(1)=2 
           ELSE 
              NTERM=INT(FCOEF(IPOSF(IFUNC-1)),KIND=I_P) 
              IPOSF(IFUNC)=IPOSF(IFUNC-1)+14 
              DO ITERM=1,NTERM 
                 NSTERM=INT(FCOEF(IPOSF(IFUNC)),KIND=I_P) 
                 IPOSF(IFUNC)=IPOSF(IFUNC)+5*NSTERM+3 
              END DO
           END IF
           !reference system type         
           IREF=INT(FCOEF(IPOSF(IFUNC)+1),KIND=I_P) 
           IF(IREF.EQ.0) THEN 
              XV=X-FCOEF(IPOSF(IFUNC)+2) 
              YV=Y-FCOEF(IPOSF(IFUNC)+3) 
              ZV=Z-FCOEF(IPOSF(IFUNC)+4) 
           ELSE 
              !. System transformation. From global (X,Y,Z) to local (XV,YV,ZV) 
              XN1=FCOEF(IPOSF(IFUNC)+5) 
              YN1=FCOEF(IPOSF(IFUNC)+6) 
              ZN1=FCOEF(IPOSF(IFUNC)+7) 
              XN2=FCOEF(IPOSF(IFUNC)+8) 
              YN2=FCOEF(IPOSF(IFUNC)+9) 
              ZN2=FCOEF(IPOSF(IFUNC)+10) 
              XN3=FCOEF(IPOSF(IFUNC)+11) 
              YN3=FCOEF(IPOSF(IFUNC)+12) 
              ZN3=FCOEF(IPOSF(IFUNC)+13) 
              XT=X-FCOEF(IPOSF(IFUNC)+2) 
              YT=Y-FCOEF(IPOSF(IFUNC)+3) 
              ZT=Z-FCOEF(IPOSF(IFUNC)+4) 
              XV=XT*XN1+YT*YN1+ZT*ZN1 
              YV=XT*XN2+YT*YN2+ZT*ZN2 
              ZV=XT*XN3+YT*YN3+ZT*ZN3 
           END IF
           NTERM=INT(FCOEF(IPOSF(IFUNC)),KIND=I_P) 
           FSUM=0.0_W_P 
           JPOSF=IPOSF(IFUNC)+14 
           DO ITERM=1,NTERM 
              NSTERM=INT(FCOEF(JPOSF),KIND=I_P) 
              FSUM2=0.0_W_P 
              DO ISTERM=1,NSTERM
                 ITYPE=INT(FCOEF(JPOSF+3+(ISTERM-1)*5),KIND=I_P)
                 C1=FCOEF(JPOSF+4+(ISTERM-1)*5) 
                 C2=FCOEF(JPOSF+5+(ISTERM-1)*5) 
                 C3=FCOEF(JPOSF+6+(ISTERM-1)*5) 
                 C4=FCOEF(JPOSF+7+(ISTERM-1)*5) 
                 IF(ITYPE.EQ.1) FSUM2=FSUM2+C1*(XV**C2)*(YV**C3)*(ZV**C4) 
                 IF(ITYPE.EQ.2) FSUM2=FSUM2+C1*COS(XV*C2)*COS(YV*C3)*   &
                      COS(ZV*C4) 
              END DO
              C0=FCOEF(JPOSF+1) 
              C5=FCOEF(JPOSF+2) 
              FSUM=FSUM+C0*FSUM2**C5 
              JPOSF=JPOSF+5*NSTERM+3 
           END DO
           IF(FCOEF(1).GT.0.0_W_P) THEN
              A=MAX(A,FSUM)
           ELSE
              A=MIN(A,FSUM)
           END IF
        END DO
        RETURN 
      END SUBROUTINE MFUNC3D
!--------------------------- END OF MFUNC3D --------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
!                           INTEMFUNC3D                               | 
!---------------------------------------------------------------------| 
! On entry:                                                           | 
!==========                                                           | 
! BBALL    = bounding ball                                            | 
! FCOEF    = array containing the coefficients for the multi implict  | 
!            functions definition                                     | 
! V0       = vertex coordinates of the initial point                  | 
! V1       = vertex coordinates of the next point along the line      | 
!            where the root is been searching                         | 
! On return:                                                          | 
!===========                                                          | 
! IE       = 0, if the root is found; 1, otherwise                    | 
! VI       = vertex coordinates of the point of intersection between  | 
!            the line and the hypersurface                            | 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------| 
    SUBROUTINE INTEMFUNC3D(BBALL,FCOEF,IE,V0,V1,VI) BIND(C) 
      !.. Scalar Arguments                                                    
      INTEGER(I_P), INTENT(OUT) :: IE
      REAL(W_P), INTENT(IN) :: BBALL
      !.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: FCOEF(10000) 
      ! FCOEF(1) = number of implicit functions ('+' sign means union and
      !            '-' sign means intersection)                               
      ! FCOEF(2) = 2, index position of FCOEF where the information if the    
      !            implicit function 1 begins                                 
      ! FCOEF(3) = 0 for global system; 1 for local system                    
      ! FCOEF(4-6) = xyz-coordinates of the system-reference origin           
      ! FCOEF(7-15) = xyz-components of the normal vectors that define the    
      !               orthonormal reference system                            
      ! FCOEF(16-19) = C1,C2,C3,C4 coeficients of the first term of the       
      !                implicit function 1: C1 X^C2 Y^C3 Z^C4                 
      ! Follow the same pattern for the rest of information                   
      REAL(W_P), INTENT(INOUT) :: V0(3),V1(3) 
      REAL(W_P), INTENT(OUT) :: VI(3) 
      !.. Local Scalars                                                       
      REAL(W_P) :: D,D0,D1,DF,F0,F1,FI,FIQ,Q,R,S,T,TOLB 
      INTEGER(I_P) :: I,IBRACKET,ITER,NITER 
      !.. Local Arrays                                                        
      REAL(W_P) :: P(3),V0INIT(3),V1INIT(3),VIQ(3) 
      !. Root finding using Brent's method                                    
      TOLB=1E-12_W_P 
      NITER=100 
      CALL MFUNC3D(F0,FCOEF,V0(1),V0(2),V0(3)) 
      CALL MFUNC3D(F1,FCOEF,V1(1),V1(2),V1(3)) 
      IF(ABS(F0).LT.TOLB)THEN 
         VI=V0 
         IE=0 
         RETURN 
      END IF
      IF(ABS(F1).LT.TOLB)THEN 
         VI=V1 
         IE=0 
         RETURN 
      END IF
      V0INIT=V0 
      V1INIT=V1 
      IF(F0*F1.LT.0.0) THEN 
         ! bracketed init                                    
         IBRACKET=1 
         D=((V0(1)-V1(1))**2+(V0(2)-V1(2))**2+(V0(3)-V1(3))**2)**0.5 
      ELSE 
         IBRACKET=0 
      END IF
      IF((F1-F0).EQ.0.0_W_P) THEN
         IE=1
         RETURN
      END IF
      DO ITER=1,NITER 
         !. Secant interpolation                                                 
         DF=-F0/(F1-F0) 
         DO I=1,3 
            VI(I)=V0(I)*(1.0_W_P-DF)+V1(I)*DF 
         END DO
         D0=((V0INIT(1)-VI(1))**2+(V0INIT(2)-VI(2))**2+(V0INIT(3)-VI(3) &
              )**2)**0.5_W_P
         D1=((V1INIT(1)-VI(1))**2+(V1INIT(2)-VI(2))**2+(V1INIT(3)-VI(3) &
              )**2)**0.5_W_P
         CALL MFUNC3D(FI,FCOEF,VI(1),VI(2),VI(3)) 
         IF(ABS(FI).LT.TOLB) THEN 
            IE=0 
            GOTO 10 
         ELSEIF(FI/F0.GT.1.0_W_P.OR.FI/F1.GT.1.0_W_P.OR.D0.GT.BBALL.OR. &
              D1.GT.BBALL) THEN 
            !. Bisection      
            VI=(V0+V1)/2.0_W_P
            CALL MFUNC3D(FI,FCOEF,VI(1),VI(2),VI(3)) 
         END IF
         !. Inverse-quadratic interpolation                                      
         R=FI/F1 
         S=FI/F0 
         T=F0/F1 
         Q=(T-1.0_W_P)*(R-1.0_W_P)*(S-1.0_W_P)
         IF(Q.EQ.0.0_W_P) THEN
            IE=1
            RETURN
         END IF
         DO I=1,3 
            P(I)=S*(T*(R-T)*(V1(I)-VI(I))-(1.0_W_P-R)*(VI(I)-V0(I))) 
            VIQ(I)=VI(I)+P(I)/Q 
         END DO
         CALL MFUNC3D(FIQ,FCOEF,VIQ(1),VIQ(2),VIQ(3)) 
         ! check bracketting                     
         IF(IBRACKET.EQ.1) THEN 
            D0=((V0INIT(1)-VIQ(1))**2+(V0INIT(2)-VIQ(2))**2+(V0INIT(3)- &
                 VIQ(3))**2)**0.5_W_P                                       
            D1=((V1INIT(1)-VIQ(1))**2+(V1INIT(2)-VIQ(2))**2+(V1INIT(3)- &
                 VIQ(3))**2)**0.5_W_P                                   
            D=((V0(1)-V1(1))**2+(V0(2)-V1(2))**2+(V0(3)-V1(3))**2)**    &
                 0.5_W_P 
            IF(MAX(D0,D1).LT.(D*(1.0_W_P-1.0E-1_W_P))) THEN 
               VI=VIQ 
               FI=FIQ
            ELSE
               !. Bisection
               VI=(V0+V1)/2.0_W_P
               CALL MFUNC3D(FI,FCOEF,VI(1),VI(2),VI(3)) 
            END IF
         END IF
         IF(ABS(FI).LT.TOLB) THEN 
            IE=0 
            GOTO 10 
         END IF
         IF(FI*F1.GT.0.0_W_P) THEN 
            DO I=1,3 
               V1(I)=VI(I) 
            END DO
            F1=FI 
         ELSE 
            DO I=1,3 
               V0(I)=VI(I) 
            END DO
            F0=FI 
         END IF
      END DO
      IE=1 
10    CONTINUE 
      RETURN 
    END SUBROUTINE INTEMFUNC3D
!------------------------ END OF INTEMFUNC3D -------------------------| 
!---------------------------------------------------------------------| 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                               INTP3D                                c 
!...  Triangulated surface resulting from the intersection between    c
!...  the iso-surface 0 of an implicitly-defined function and an      c 
!...  arbitrary polyhedron                                            c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FCOEF    = array containing the coefficients for the multi implict  c 
!            functions definition                                     c 
! IPV      = array containing the indices of the vertices of each     c 
!            face of the polyhedron                                   c 
! NIPV     = number of vertices of each face of the polyhedron        c 
! NTP      = number of vertices of the polyhedron                     c 
! NTS      = number of faces of the polyhedron                        c 
! VERTP    = coordinates of the vertices of the polyhedron            c 
! On return:                                                          c 
!===========                                                          c 
! IPVISO   = array conatining the indices of the iso-vertices of each c 
!            iso-polygon                                              c 
! ISOEFACE = face index of the polyhedron over which is constructed   c 
!            each iso-edge                                            c 
! NIPVISO  = number of iso-vertices of each iso-polygon               c 
! NISO     = number of iso-polygons                                   c 
! VERTISO  = coordinates of the iso vertices                          c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE INTP3D(FCOEF,IPV,IPVISO,ISOEFACE,NIPV,NIPVISO,    &
     &     NISO,NTP,NTS,VERTISO,VERTP) BIND(C)                          
!.. Scalar Arguments                                                    
      INTEGER (I_P), INTENT(IN) :: NTP,NTS 
      INTEGER (I_P), INTENT(OUT) :: NISO 
!.. Array Arguments                                                     
      INTEGER (I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
      INTEGER (I_P), INTENT(OUT) :: IPVISO(NS,NV),ISOEFACE(NV),         &
           NIPVISO(NS)
      REAL (W_P), INTENT(IN) :: FCOEF(10000)
      REAL (W_P), INTENT(IN) :: VERTP(NV,3) 
      REAL (W_P), INTENT(OUT) :: VERTISO(NV,3) 
!.. Local Scalars                                                       
      INTEGER (I_P) :: ICONTN,ICONTP,IE,IEBRACKET,IP,IP0,IP1,IS,IV,     &
     &     NISO2,NTPISO,NTPISOINI                                       
      REAL (W_P) :: DD,DX,DY,DZ,PHIISO,XMAX,XMIN,YMAX,YMIN,ZMAX,ZMIN 
!.. Local Arrays                                                        
      INTEGER (I_P) :: IA(NV),IPIA0(NV),IPIA1(NV),IPVISO2(NS,NV) 
      REAL (W_P) :: PHI(NV),V0(3),V1(3),VI(3) 
!* Working parameters                                                   
      ICONTP=0 
      ICONTN=0 
      NISO=0 
      PHIISO=0.0 
      DO IP=1,NTP 
         IA(IP)=-1 
         CALL MFUNC3D(PHI(IP),FCOEF,VERTP(IP,1),VERTP(IP,2),VERTP(IP,3)) 
      END DO 
!* Tag the vertices of the polyhedron                                   
      XMIN=1.0E-20_W_P 
      XMAX=-1.0E-20_W_P 
      YMIN=1.0E-20_W_P 
      YMAX=-1.0E-20_W_P 
      ZMIN=1.0E-20_W_P 
      ZMAX=-1.0E-20_W_P 
      DO IS=1,NTS 
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(IA(IP).EQ.(-1)) THEN 
               XMIN=MIN(XMIN,VERTP(IP,1)) 
               XMAX=MAX(XMAX,VERTP(IP,1)) 
               YMIN=MIN(YMIN,VERTP(IP,2)) 
               YMAX=MAX(YMAX,VERTP(IP,2)) 
               ZMIN=MIN(ZMIN,VERTP(IP,3)) 
               ZMAX=MAX(ZMAX,VERTP(IP,3)) 
               IF(PHI(IP).GT.PHIISO) THEN 
                  IA(IP)=1 
                  ICONTP=ICONTP+1 
               ELSE 
                  IA(IP)=0 
                  ICONTN=ICONTN+1 
               END IF 
            END IF 
         END DO 
      END DO 
      IF(ICONTP.NE.0.AND.ICONTN.NE.0) THEN
         DX=XMAX-XMIN
         DY=YMAX-YMIN
         DZ=ZMAX-ZMIN
         DD=0.01*MIN(DX,DY,DZ) 
!* Arrange the vertices of the intersected isosurface    
         CALL ISOPOL3D(IA,IPIA0,IPIA1,IPV,IPVISO,ISOEFACE,NIPV,NIPVISO, &
              NISO,NTS)     
!* Iso-vertices positioning by root finding                             
         NTPISO=0 
         DO IS=1,NISO 
            NTPISO=NTPISO+NIPVISO(IS) 
         END DO 
         NTPISOINI=NTPISO 
         DO IS=1,NISO 
            NTPISO=NTPISO+1 
            VERTISO(NTPISO,1)=0.0 
            VERTISO(NTPISO,2)=0.0 
            VERTISO(NTPISO,3)=0.0 
            DO IV=1,NIPVISO(IS) 
               IP=IPVISO(IS,IV) 
               IP0=IPIA0(IP) 
               IP1=IPIA1(IP) 
               V0(1)=VERTP(IP0,1) 
               V0(2)=VERTP(IP0,2) 
               V0(3)=VERTP(IP0,3) 
               V1(1)=VERTP(IP1,1) 
               V1(2)=VERTP(IP1,2) 
               V1(3)=VERTP(IP1,3) 
               CALL INTEMFUNC3D(MAX(DX,DY,DZ),FCOEF,IE,V0,V1,VI)
               IF(IE.EQ.0) THEN 
                  VERTISO(IP,1)=VI(1) 
                  VERTISO(IP,2)=VI(2) 
                  VERTISO(IP,3)=VI(3) 
               ELSE 
                  VERTISO(IP,1)=VERTP(IP0,1)+(PHIISO-PHI(IP0))*(        &
     &                 VERTP(IP1,1)-VERTP(IP0,1))/(PHI(IP1)-PHI(IP0))   
                  VERTISO(IP,2)=VERTP(IP0,2)+(PHIISO-PHI(IP0))*(        &
     &                 VERTP(IP1,2)-VERTP(IP0,2))/(PHI(IP1)-PHI(IP0))   
                  VERTISO(IP,3)=VERTP(IP0,3)+(PHIISO-PHI(IP0))*(        &
     &                 VERTP(IP1,3)-VERTP(IP0,3))/(PHI(IP1)-PHI(IP0))   
               END IF 
               VERTISO(NTPISO,1)=VERTISO(NTPISO,1)+VERTISO(IP,1) 
               VERTISO(NTPISO,2)=VERTISO(NTPISO,2)+VERTISO(IP,2) 
               VERTISO(NTPISO,3)=VERTISO(NTPISO,3)+VERTISO(IP,3) 
            END DO 
            IF(NIPVISO(IS).GT.0) THEN 
               VERTISO(NTPISO,1)=VERTISO(NTPISO,1)/NIPVISO(IS) 
               VERTISO(NTPISO,2)=VERTISO(NTPISO,2)/NIPVISO(IS) 
               VERTISO(NTPISO,3)=VERTISO(NTPISO,3)/NIPVISO(IS) 
               V0(1)=VERTISO(NTPISO,1) 
               V0(2)=VERTISO(NTPISO,2) 
               V0(3)=VERTISO(NTPISO,3)
               CALL FINDBRACKETM(DD,FCOEF,IEBRACKET,V0,V1)
               IF(IEBRACKET.EQ.2) THEN 
                  VERTISO(NTPISO,1)=V1(1) 
                  VERTISO(NTPISO,2)=V1(2) 
                  VERTISO(NTPISO,3)=V1(3) 
               ELSE 
                  IF(IEBRACKET.NE.-1) THEN 
                     CALL INTEMFUNC3D(DD*50.0_W_P,FCOEF,IE,V0,V1,VI)
                     IF(IE.EQ.0) THEN 
                        VERTISO(NTPISO,1)=VI(1) 
                        VERTISO(NTPISO,2)=VI(2) 
                        VERTISO(NTPISO,3)=VI(3) 
                     END IF 
                  END IF 
               END IF 
            END IF 
         END DO 
                                                                        
                                                                        
         NISO2=0 
         DO IS=1,NISO 
            DO IV=1,NIPVISO(IS) 
               NISO2=NISO2+1 
               IP=IPVISO(IS,IV) 
               IF(IV.EQ.NIPVISO(IS)) THEN 
                  IP1=IPVISO(IS,1) 
               ELSE 
                  IP1=IPVISO(IS,IV+1) 
               END IF 
               IPVISO2(NISO2,1)=IP 
               IPVISO2(NISO2,2)=IP1 
               IPVISO2(NISO2,3)=NTPISOINI+IS 
            END DO 
         END DO 
         DO IS=1,NISO2 
            NIPVISO(IS)=3 
            IPVISO(IS,1)=IPVISO2(IS,1) 
            IPVISO(IS,2)=IPVISO2(IS,2) 
            IPVISO(IS,3)=IPVISO2(IS,3) 
         END DO 
         NISO=NISO2 
      END IF 
      RETURN 
      END                                           
!-------------------------- END OF INTP3D ----------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                            ISOPOL3D                                 c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! IA       = tag value of each vertex of the polyhedron (0 or 1)      c 
! IPV      = array containing the indices of the vertices of each     c 
!            face of the polyhedron                                   c 
! NIPV     = number of vertices of each face of the polyhedron        c 
! NTS      = number of faces of the polyhedron                        c 
! On return:                                                          c 
!===========                                                          c 
! IPIA0    = vertex index of the polihedron with IA=0 and which is in c 
!            the edge containing the iso-vertex                       c 
! IPIA1    = vertex index of the polihedron with IA=1 and which is in c 
!            the edge containing the iso-vertex                       c 
! IPVISO   = array conatining the indices of the iso-vertices of each c 
!            iso-polygon                                              c 
! ISOEFACE = face index of the polyhedron over which is constructed   c 
!            each iso-edge                                            c 
! NIPVISO  = number of iso-vertices of each iso-polygon               c 
! NISO     = number of iso-polygons                                   c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE ISOPOL3D(IA,IPIA0,IPIA1,IPV,IPVISO,ISOEFACE,NIPV,      &
     &     NIPVISO,NISO,NTS) BIND(C)                                    
!.. Scalar Arguments                                                    
      INTEGER (I_P), INTENT(IN) :: NTS 
      INTEGER (I_P), INTENT(OUT) :: NISO 
!.. Array Arguments                                                     
      INTEGER (I_P), INTENT(IN) :: IA(NV),IPV(NS,NV),NIPV(NS) 
      INTEGER (I_P), INTENT(OUT) :: IPIA0(NV),IPIA1(NV),IPVISO(NS,NV),  &
     &     ISOEFACE(NV),NIPVISO(NS)                                     
!.. Local Scalars                                                       
      INTEGER (I_P) :: IE,IP,IP0I,IP0N,IP1,IP1N,IP1I,IPINI,IPNEW,IS,IS1,&
     &     ISI,ISNEW,ITYPE,IV,IV1,IVNEW,IVNEWT,NINT,NIPNEW,NISCUT,      &
     &     NISMIX,NIV,NIVNEW                                            
!.. Local Arrays                                                        
      INTEGER (I_P) :: IPVINT(NS,NV),NIPVINT(NS),IPISE(NV,2),IPMARK(NV),&
     &     ISCUT(NS),ISMIX(NS),IVISE(NS,NV),NEDGE(NS)                   
      INTEGER (I_P2) :: IPE(NV,NV) 
!* Determination of the faces intersected by the isosurface             
      NISCUT=0 
      NISMIX=0 
!* NEDGE(IS) = Number of intersected edges of the face IS               
      DO IS=1,NTS 
         NEDGE(IS)=0 
         IF(NIPV(IS).GT.0) THEN 
            ISCUT(IS)=0 
            DO IV=1,NIPV(IS) 
               IP=IPV(IS,IV) 
               IV1=IV+1 
               IF(IV.EQ.NIPV(IS)) IV1=1 
               IP1=IPV(IS,IV1) 
               IF(IA(IP).NE.IA(IP1)) THEN 
                  IPE(IP,IP1)=0 
                  ISCUT(IS)=1 
                  NISCUT=NISCUT+1 
                  NEDGE(IS)=NEDGE(IS)+1 
               END IF 
            END DO 
            IF(ISCUT(IS).EQ.1) THEN 
               NISMIX=NISMIX+1 
               ISMIX(NISMIX)=IS 
            END IF 
         END IF 
      END DO 
!* Disjoint regions may produce NISCUT=0 and both ICONTP and ICONTN \NEQ
      IF(NISCUT.EQ.0) THEN 
         NISO=0 
         RETURN 
      END IF 
!* Iso-vertices insertion                                               
      NIPNEW=0 
      DO ISI=1,NISMIX 
         IS=ISMIX(ISI) 
!         IF(ISCUT(IS).EQ.1) THEN                                       
            NIV=0 
            NINT=0 
            DO IV=1,NIPV(IS) 
               IP=IPV(IS,IV) 
               IV1=IV+1 
               IF(IV1.GT.NIPV(IS))IV1=1 
               IP1=IPV(IS,IV1) 
               IF(IA(IP).NE.IA(IP1)) THEN 
                  NINT=NINT+1 
                  NIV=NIV+1 
                  IF(IA(IP).EQ.1) THEN 
                     IP1I=IP 
                     IP0I=IP1 
                     ITYPE=2 
                  ELSE 
                     IP1I=IP1 
                     IP0I=IP 
                     ITYPE=1 
                  END IF 
                  IF(IPE(IP1,IP).NE.0) THEN 
                     IPNEW=IPE(IP1,IP) 
                     IPVINT(IS,NIV)=IPNEW 
                     IVISE(IS,IPNEW)=NIV 
                     IPISE(IPNEW,ITYPE)=IS 
                     GOTO 10 
                  END IF 
                  NIPNEW=NIPNEW+1 
                  IPE(IP,IP1)=NIPNEW 
                  IPIA0(NIPNEW)=IP0I 
                  IPIA1(NIPNEW)=IP1I 
                  IPVINT(IS,NIV)=NIPNEW 
                  IVISE(IS,NIPNEW)=NIV 
                  IPISE(NIPNEW,ITYPE)=IS 
               END IF 
   10          CONTINUE 
            END DO 
            NIPVINT(IS)=NIV 
      END DO 
!* Iso-vertices arrangement                                             
      NIVNEW=NIPNEW 
      ISNEW=0 
      DO IP=1,NIPNEW 
         IPMARK(IP)=0 
      END DO 
      IVNEWT=0 
      IPNEW=1 
!* First point                                                          
   40 CONTINUE 
      IVNEW=1 
      IVNEWT=IVNEWT+1 
      ISNEW=ISNEW+1 
      IPINI=IPNEW 
      IPVISO(ISNEW,IVNEW)=IPNEW 
      ISOEFACE(IPNEW)=ipise(ipnew,1) 
      IPMARK(IPNEW)=1 
   20 CONTINUE 
      IS=IPISE(IPNEW,1) 
      IV=IVISE(IS,IPNEW) 
      IV1=IV-1 
      IF(IV1.EQ.0) IV1=NIPVINT(IS) 
      IPNEW=IPVINT(IS,IV1) 
      IF(IPNEW.NE.IPINI) THEN 
         IVNEW=IVNEW+1 
         IVNEWT=IVNEWT+1 
         IPVISO(ISNEW,IVNEW)=IPNEW 
         ISOEFACE(IPNEW)=ipise(ipnew,1) 
         IPMARK(IPNEW)=1 
         IF(IVNEWT.EQ.NIVNEW) GOTO 30 
         GOTO 20 
      END IF 
      NIPVISO(ISNEW)=IVNEW 
      DO IPNEW=2,NIPNEW 
         IF(IPMARK(IPNEW).EQ.0) GOTO 40 
      END DO 
   30 CONTINUE 
      NIPVISO(ISNEW)=IVNEW 
      NISO=ISNEW 
                                                                        
      RETURN 
      END                                           
!-------------------------- END OF ISOPOL3D --------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                            INTEFUNC3D2                               c
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! NITER    = maximum number of iterations                             c 
! V0       = vertex coordinates of the initial point                  c 
! V1       = vertex coordinates of the next point along the line      c 
!            where the root is been searching                         c 
! On return:                                                          c 
!===========                                                          c 
! IE       = 0, if the root is found; 1, otherwise                    c 
! VI       = vertex coordinates of the point of intersection between  c 
!            the line and the hypersurface                            c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE INTEFUNC3D2(FUNC3D,IE,NITER,V0,V1,VI) BIND(C) 
!.. Scalar Arguments                                                    
      INTEGER(I_P), INTENT(IN) :: NITER 
      INTEGER(I_P), INTENT(OUT) :: IE 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(INOUT) :: V0(3),V1(3) 
      REAL(W_P), INTENT(OUT) :: VI(3) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: D0,D1,DBA4,DBC,DCD,DD,DF,DSA4,DSB,F0,F1,FA,FAUX,FB,  &
     &     FC,FI,FIQ,FS,Q,R,T,TOLB,TOLD                                 
      INTEGER(I_P) :: I,IBRACKET,ITER,MFLAG 
!.. Local Arrays                                                        
      REAL(W_P) :: A(3),AUX(3),B(3),BA4(3),BC(3),C(3),CD(3),D(3),P(3),  &
     &     S(3),SA4(3),SB(3),V0INIT(3),V1INIT(3),VIQ(3)                 
!. Root finding using Brent's method                                    
      TOLB=1D-12 
      IE=0 
      F0=FUNC3D(V0(1),V0(2),V0(3)) 
      F1=FUNC3D(V1(1),V1(2),V1(3)) 
      IF(ABS(F0).LT.TOLB)THEN 
         VI=V0 
         RETURN 
      END IF 
      IF(ABS(F1).LT.TOLB)THEN 
         VI=V1 
         RETURN 
      END IF 
      IF(ABS(F0).LT.ABS(F1)) THEN 
         A=V1 
         B=V0 
         FA=F1 
         FB=F0 
      ELSE 
         A=V0 
         B=V1 
         FA=F0 
         FB=F1 
      ENDIF 
      C=A 
      FC=FA 
      MFLAG=1 
      TOLD=2._W_P*3D-08*(B(1)**2+B(2)**2+B(3)**2)**0.5+TOLB/2._W_P 
      DO ITER=1,NITER 
         IF(FA.NE.FC.AND.FB.NE.FC) THEN 
!. Inverse-quadratic interpolation                                      
            S=A*FB*FC/((FA-FB)*(FA-FC))+B*FA*FC/((FB-FA)*(FB-FC))+      &
     &           C*FA*FB/((FC-FA)*(FC-FB))                              
         ELSE 
!. secant                                                               
            S=B-FB*(B-A)/(FB-FA) 
         END IF 
         BA4=B-(A*3._W_P+B)/4._W_P 
         DBA4=(BA4(1)**2+BA4(2)**2+BA4(3)**2)**0.5 
         SA4=S-(A*3._W_P+B)/4._W_P 
         DSA4=(SA4(1)**2+SA4(2)**2+SA4(3)**2)**0.5 
         SB=S-B 
         DSB=(SB(1)**2+SB(2)**2+SB(3)**2)**0.5 
         IF(MFLAG.EQ.1) THEN 
            BC=B-C 
            DBC=(BC(1)**2+BC(2)**2+BC(3)**2)**0.5 
         END IF 
         IF(MFLAG.EQ.0) THEN 
            CD=C-D 
            DCD=(CD(1)**2+CD(2)**2+CD(3)**2)**0.5 
         END IF 
         IF((DSA4+DSB).GT.(DBA4+TOLB).OR.                               &
     &        MFLAG.EQ.1.AND.DSB.GE.DBC/2._W_P.OR.                      &
     &        MFLAG.EQ.0.AND.DSB.GE.DCD/2._W_P.OR.                      &
     &        MFLAG.EQ.1.AND.DBC.LT.TOLD.OR.                            &
     &        MFLAG.EQ.0.AND.DCD.LT.TOLD) THEN                          
!. bisection                                                            
            S=(A+B)/2._W_P 
            MFLAG=1 
         ELSE 
            MFLAG=0 
         END IF 
         FS=FUNC3D(S(1),S(2),S(3)) 
         IF(ABS(FS).LT.TOLB) THEN 
            VI=S 
            RETURN 
         END IF 
         D=C 
         C=B 
         IF(FA*FS.LT.0.0) THEN 
            B=S 
            FB=FS 
         ELSE 
            A=S 
            FA=FS 
         END IF 
         IF(FA.LT.FB) THEN 
            AUX=A 
            FAUX=FA 
            A=B 
            FA=FB 
            B=AUX 
            FB=FAUX 
         END IF 
         IF(ABS(FB).LT.TOLB) THEN 
            VI=B 
            RETURN 
         END IF 
      END DO 
      VI=B 
      IE=1 
      RETURN 
      END                                           
!------------------------- END OF INTEFUNC3D2 -------------------------c
!---------------------------------------------------------------------c 
                                                                        
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                            INITFTETRA                               c 
!   Tetrahedral decomposition coupled with Richardson extrapolation   c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! FUNC3D   = external user-supplied function where the interface      c 
!            shape is analytically defined                            c 
! IPV      = array containing the global indices of the original pol. c 
!            vertices                                                 c 
! NC       = refinement level                                         c 
! NIPV     = number of vertices of each face                          c 
! NTP      = last global vertex index                                 c 
! NTS      = total number of faces                                    c 
! NTV      = total number of vertices                                 c 
! TOL      = prescribed positive tolerance for the distance to the    c 
!            interface                                                c 
! VERTP    = vertex coordinates of the original polyhedron            c 
! XNS, ... = unit-lenght normals to the faces of the original polyh.  c 
! On return:                                                          c 
!===========                                                          c 
! VF       = material volume fraction                                 c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE INITFTETRA(FUNC3D,IPV,NC,NIPV,NTP,NTS,NTV,TOL,VERTP,VF,&
     &     XNS,YNS,ZNS) BIND(C)                                         
!.. Scalar Arguments                                                    
      REAL(W_P), INTENT(IN) :: TOL 
      REAL(W_P), INTENT(OUT) :: VF 
      INTEGER(I_P), INTENT(IN) :: NC, NTP, NTS, NTV 
!.. Array Arguments                                                     
      REAL(W_P), INTENT(IN) :: VERTP(NV,3),XNS(NS),YNS(NS),ZNS(NS) 
      INTEGER(I_P), INTENT(IN) :: IPV(NS,NV),NIPV(NS) 
!.. Procedure Arguments                                                 
      PROCEDURE (VOFTOOLS_FUNC3D) :: FUNC3D 
!.. Local Scalars                                                       
      REAL(W_P) :: AMOD,CX1,CX2,CY1,CY2,CZ1,CZ2,DDX,DDY,DDZ,DX,         &
     &     DY,DZ,PHIMIN,SUMX,SUMY,SUMZ,VOLF,VOLT,X,XC,XM,XMAX,XMIN,     &
     &     XP,XV1,XV2,Y,YC,YM,YMAX,YMIN,YP,YV1,YV2,Z,ZC,ZM,ZMAX,        &
     &     ZMIN,ZP,ZV1,ZV2                                              
      INTEGER(I_P) :: I,IC,ICONTN,ICONTP,IP,IP0,IP1,IP2,IPHI,IS,IS2,IV, &
     &     IV2,JC,KC,NTP0,NTP1,NTP2,NTS0,NTS1,NTS2,NTSINI,NTV0,NTV1,    &
     &     NTV2                                                         
!.. Local Arrays                                                        
      REAL(W_P) :: CS(NS),CS0(NS),CS1(NS),CS2(NS),PHIV0(NV),            &
     &     VERTP0(NV,3),VERTP1(NV,3),VERTP2(NV,3),XNS0(NS),XNS1(NS),    &
     &     XNS2(NS),YNS0(NS),YNS1(NS),YNS2(NS),ZNS0(NS),ZNS1(NS),       &
     &     ZNS2(NS)                                                     
      INTEGER(I_P) :: IA(NV),ICHECK(NV),IPIA0(NV),IPIA1(NV),            &
     &     IPV0(NS,NV),IPV1(NS,NV),IPV2(NS,NV),ISCUT(NS),NIPV0(NS),     &
     &     NIPV1(NS),NIPV2(NS)                                          
!.. New Local Scalars                                                   
      INTEGER(I_P) :: IP3,IP4,IPC,IPT1,IPT2,IPT3,IPT4,IR,ITETRA,IVV,    &
     &     IVV2,NITETRA,NPTETRA,NTETRA0,NVCELL                          
      REAL(W_P) :: DMOD,RATIO,SMAX,SMIN,XN,YN,ZN 
!.. New Local Arrays                                                    
                                          ! Maximum refinement levels   
      INTEGER(I_P), PARAMETER :: NCMAX=20 
!      INTEGER(I_P), PARAMETER :: NTETRAMAX=1000000                     
!      INTEGER(I_P) :: IPTETRA(NTETRAMAX,4),ITETRAINT(NCMAX,NTETRAMAX), 
!     -     NTETRA(NCMAX),NTETRAINT(NCMAX)                              
!      REAL(W_P) :: PHIV(NTETRAMAX),VFIR(NCMAX),VFBASE(NCMAX),          
!     -     VP(NTETRAMAX,3)                                             
      INTEGER(I_P) :: NTETRAMAX 
      INTEGER(I_P), DIMENSION(:,:), ALLOCATABLE :: IPTETRA,ITETRAINT 
      REAL(W_P), DIMENSION(:,:), ALLOCATABLE :: VP 
      REAL(W_P), DIMENSION(:), ALLOCATABLE :: PHIV 
      INTEGER(I_P), DIMENSION(:), ALLOCATABLE :: NTETRA,NTETRAINT 
      REAL(W_P), DIMENSION(:), ALLOCATABLE :: VFIR,VFBASE 
!.. Arrays dimension                                                    
      NTETRAMAX=0 
      DO IS=1,NTS 
         DO IV=1,NIPV(IS) 
            NTETRAMAX=NTETRAMAX+1 
         END DO 
      END DO 
      NTETRAMAX=NTETRAMAX*12**NC 
      ALLOCATE(IPTETRA(NTETRAMAX,4)) 
      ALLOCATE(ITETRAINT(NC,NTETRAMAX)) 
      ALLOCATE(VP(NTETRAMAX,3)) 
      ALLOCATE(PHIV(NTETRAMAX)) 
                                                                        
      ALLOCATE(NTETRA(NC)) 
      ALLOCATE(NTETRAINT(NC)) 
      ALLOCATE(VFIR(NC)) 
      ALLOCATE(VFBASE(NC)) 
!.. Coordinate extremes of the cell and vertex tagging                  
      XMIN=1.0D+20 
      XMAX=-1.0D+20 
      YMIN=1.0D+20 
      YMAX=-1.0D+20 
      ZMIN=1.0D+20 
      ZMAX=-1.0D+20 
      ICONTP=0 
      ICONTN=0 
      DO IP=1,NTP 
         ICHECK(IP)=0 
      END DO 
      XC=0.0 
      YC=0.0 
      ZC=0.0 
      NVCELL=0 
      DO IS=1,NTS 
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            IF(ICHECK(IP).EQ.0) THEN 
               ICHECK(IP)=1 
               XP=VERTP(IP,1) 
               YP=VERTP(IP,2) 
               ZP=VERTP(IP,3) 
               VP(IP,1)=XP 
               VP(IP,2)=YP 
               VP(IP,3)=ZP 
               XC=XC+XP 
               YC=YC+YP 
               ZC=ZC+ZP 
               NVCELL=NVCELL+1 
               XMIN=DMIN1(XMIN,XP) 
               XMAX=DMAX1(XMAX,XP) 
               YMIN=DMIN1(YMIN,YP) 
               YMAX=DMAX1(YMAX,YP) 
               ZMIN=DMIN1(ZMIN,ZP) 
               ZMAX=DMAX1(ZMAX,ZP) 
               PHIV(IP)=FUNC3D(XP,YP,ZP) 
               IF(PHIV(IP).GE.0.0) THEN 
                  IA(IP)=1 
                  ICONTP=ICONTP+1 
               ELSE 
                  IA(IP)=0 
                  ICONTN=ICONTN+1 
               END IF 
            END IF 
         END DO 
      END DO 
      IF(NVCELL.NE.0) THEN 
         XC=XC/NVCELL 
         YC=YC/NVCELL 
         ZC=ZC/NVCELL 
         PHIV(NTP+1)=FUNC3D(XC,YC,ZC) 
         VP(NTP+1,1)=XC 
         VP(NTP+1,2)=YC 
         VP(NTP+1,3)=ZC 
      END IF 
      DX=XMAX-XMIN 
      DY=YMAX-YMIN 
      DZ=ZMAX-ZMIN 
!.. initialization                                                      
      IPHI=0 
      PHIMIN=10.0*DMAX1(DX,DY,DZ) 
      DO IS=1,NTS 
         DO IV=1,NIPV(IS) 
            IP=IPV(IS,IV) 
            PHIMIN=DMIN1(PHIMIN,ABS(PHIV(IP))) 
         END DO 
      END DO 
      IF(PHIMIN.LT.TOL*DX) IPHI=1 
      IF(IPHI.EQ.0) THEN 
         IF(ICONTP.EQ.NTV) THEN 
            VF=1.0 
            GOTO 10 
         END IF 
         IF(ICONTN.EQ.NTV) THEN 
            VF=0.0 
            GOTO 10 
         END IF 
      END IF 
!.. compute the volume VOLT of the original polyhedron                  
      CALL TOOLV3D(IPV,NIPV,NTS,VERTP,VOLT,XNS,YNS,ZNS) 
!.. first refinement level                                              
      NTETRA(1)=0 
      NTETRAINT(1)=0 
      NPTETRA=NTP+1 
      VFBASE(1)=0.0 
      DO IS=1,NTS 
!**   SERIA INTERESANTE CONSIDERAR LA OPCION DE QUE NTP ES DISTINTO DE  
!**   NTV, LO QUE OCURRIRA SI EL POLIEDRO ORIGINAL FUE PREVIAMENTE      
!**   TRUNCADO POR UN PLANO                                             
         IF(NIPV(IS).GT.0) THEN 
            NPTETRA=NPTETRA+1 
            XC=0.0 
            YC=0.0 
            ZC=0.0 
            NTETRA0=NTETRA(1) 
            DO IV=1,NIPV(IS) 
               IP=IPV(IS,IV) 
               XC=XC+VERTP(IP,1) 
               YC=YC+VERTP(IP,2) 
               ZC=ZC+VERTP(IP,3) 
               IF(IV.EQ.NIPV(IS)) THEN 
                  IV2=1 
               ELSE 
                  IV2=IV+1 
               END IF 
               IP2=IPV(IS,IV2) 
               NTETRA(1)=NTETRA(1)+1 
               IPTETRA(NTETRA(1),1)=IP 
               IPTETRA(NTETRA(1),2)=IP2 
               IPTETRA(NTETRA(1),3)=NPTETRA 
               IPTETRA(NTETRA(1),4)=NTP+1 
            END DO 
            VP(NPTETRA,1)=XC/NIPV(IS) 
            VP(NPTETRA,2)=YC/NIPV(IS) 
            VP(NPTETRA,3)=ZC/NIPV(IS) 
            PHIV(NPTETRA)=FUNC3D(VP(NPTETRA,1),VP(NPTETRA,2),           &
     &           VP(NPTETRA,3))                                         
                                                                        
!. INCLUYO EN LA LISTA LOS TETRAEDROS POR LOS QUE PASA LA INTERFAZ      
            DO ITETRA=NTETRA0+1,NTETRA(1) 
               IPT1=IPTETRA(ITETRA,1) 
               IPT2=IPTETRA(ITETRA,2) 
               IPT3=IPTETRA(ITETRA,3) 
               IPT4=IPTETRA(ITETRA,4) 
               SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),      &
     &              SIGN(1D0,PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))          
               SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),      &
     &              SIGN(1D0,PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))          
               IF(SMAX*SMIN.LT.0.0) THEN 
                  NTETRAINT(1)=NTETRAINT(1)+1 
                  ITETRAINT(1,NTETRAINT(1))=ITETRA 
               ELSE 
                  IF(SMIN.GT.0.0) THEN 
                     XV1=VP(IPT2,1)-VP(IPT4,1) 
                     YV1=VP(IPT2,2)-VP(IPT4,2) 
                     ZV1=VP(IPT2,3)-VP(IPT4,3) 
                     XV2=VP(IPT3,1)-VP(IPT4,1) 
                     YV2=VP(IPT3,2)-VP(IPT4,2) 
                     ZV2=VP(IPT3,3)-VP(IPT4,3) 
                     XN=YV1*ZV2-ZV1*YV2 
                     YN=ZV1*XV2-XV1*ZV2 
                     ZN=XV1*YV2-YV1*XV2 
                     XV1=VP(IPT1,1)-VP(IPT4,1) 
                     YV1=VP(IPT1,2)-VP(IPT4,2) 
                     ZV1=VP(IPT1,3)-VP(IPT4,3) 
                     VFBASE(1)=VFBASE(1)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
                  END IF 
               END IF 
            END DO 
         END IF 
      END DO 
!. Subsequet refinement levels                                          
      NITETRA=0 
      DO IR=2,NC 
         NITETRA=NITETRA+NTETRA(IR-1) 
         NTETRAINT(IR)=0 
         NTETRA(IR)=0 
         VFBASE(IR)=0.0 
         DO IV=1,NTETRAINT(IR-1) 
            ITETRA=ITETRAINT(IR-1,IV) 
            NPTETRA=NPTETRA+1 
            IPC=NPTETRA 
            VP(NPTETRA,1)=(VP(IPTETRA(ITETRA,1),1)+VP(IPTETRA(ITETRA,2),&
     &           1)+VP(IPTETRA(ITETRA,3),1)+VP(IPTETRA(ITETRA,4),1))/4.0
            VP(NPTETRA,2)=(VP(IPTETRA(ITETRA,1),2)+VP(IPTETRA(ITETRA,2),&
     &           2)+VP(IPTETRA(ITETRA,3),2)+VP(IPTETRA(ITETRA,4),2))/4.0
            VP(NPTETRA,3)=(VP(IPTETRA(ITETRA,1),3)+VP(IPTETRA(ITETRA,2),&
     &           3)+VP(IPTETRA(ITETRA,3),3)+VP(IPTETRA(ITETRA,4),3))/4.0
            PHIV(NPTETRA)=FUNC3D(VP(NPTETRA,1),VP(NPTETRA,2),VP(NPTETRA,&
     &           3))                                                    
            NPTETRA=NPTETRA+1 
            IP1=NPTETRA 
            VP(NPTETRA,1)=(VP(IPTETRA(ITETRA,1),1)+VP(IPTETRA(ITETRA,2),&
     &           1)+VP(IPTETRA(ITETRA,3),1))/3.0                        
            VP(NPTETRA,2)=(VP(IPTETRA(ITETRA,1),2)+VP(IPTETRA(ITETRA,2),&
     &           2)+VP(IPTETRA(ITETRA,3),2))/3.0                        
            VP(NPTETRA,3)=(VP(IPTETRA(ITETRA,1),3)+VP(IPTETRA(ITETRA,2),&
     &           3)+VP(IPTETRA(ITETRA,3),3))/3.0                        
            PHIV(NPTETRA)=FUNC3D(VP(NPTETRA,1),VP(NPTETRA,2),           &
     &           VP(NPTETRA,3))                                         
            NPTETRA=NPTETRA+1 
            IP2=NPTETRA 
            VP(NPTETRA,1)=(VP(IPTETRA(ITETRA,2),1)+VP(IPTETRA(ITETRA,1),&
     &           1)+VP(IPTETRA(ITETRA,4),1))/3.0                        
            VP(NPTETRA,2)=(VP(IPTETRA(ITETRA,2),2)+VP(IPTETRA(ITETRA,1),&
     &           2)+VP(IPTETRA(ITETRA,4),2))/3.0                        
            VP(NPTETRA,3)=(VP(IPTETRA(ITETRA,2),3)+VP(IPTETRA(ITETRA,1),&
     &           3)+VP(IPTETRA(ITETRA,4),3))/3.0                        
            PHIV(NPTETRA)=FUNC3D(VP(NPTETRA,1),VP(NPTETRA,2),           &
     &           VP(NPTETRA,3))                                         
            NPTETRA=NPTETRA+1 
            IP3=NPTETRA 
            VP(NPTETRA,1)=(VP(IPTETRA(ITETRA,3),1)+VP(IPTETRA(ITETRA,2),&
     &           1)+VP(IPTETRA(ITETRA,4),1))/3.0                        
            VP(NPTETRA,2)=(VP(IPTETRA(ITETRA,3),2)+VP(IPTETRA(ITETRA,2),&
     &           2)+VP(IPTETRA(ITETRA,4),2))/3.0                        
            VP(NPTETRA,3)=(VP(IPTETRA(ITETRA,3),3)+VP(IPTETRA(ITETRA,2),&
     &           3)+VP(IPTETRA(ITETRA,4),3))/3.0                        
            PHIV(NPTETRA)=FUNC3D(VP(NPTETRA,1),VP(NPTETRA,2),           &
     &           VP(NPTETRA,3))                                         
            NPTETRA=NPTETRA+1 
            IP4=NPTETRA 
            VP(NPTETRA,1)=(VP(IPTETRA(ITETRA,1),1)+VP(IPTETRA(ITETRA,3),&
     &           1)+VP(IPTETRA(ITETRA,4),1))/3.0                        
            VP(NPTETRA,2)=(VP(IPTETRA(ITETRA,1),2)+VP(IPTETRA(ITETRA,3),&
     &           2)+VP(IPTETRA(ITETRA,4),2))/3.0                        
            VP(NPTETRA,3)=(VP(IPTETRA(ITETRA,1),3)+VP(IPTETRA(ITETRA,3),&
     &           3)+VP(IPTETRA(ITETRA,4),3))/3.0                        
            PHIV(NPTETRA)=FUNC3D(VP(NPTETRA,1),VP(NPTETRA,2),           &
     &           VP(NPTETRA,3))                                         
!. Subtetrahedron 1                                                     
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,1) 
            IPT2=IPTETRA(ITETRA,2) 
            IPT3=IP1 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 2                                                     
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,2) 
            IPT2=IPTETRA(ITETRA,3) 
            IPT3=IP1 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 3                                                     
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,3) 
            IPT2=IPTETRA(ITETRA,1) 
            IPT3=IP1 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 4                                                     
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,2) 
            IPT2=IPTETRA(ITETRA,1) 
            IPT3=IP2 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 5                                                     
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,1) 
            IPT2=IPTETRA(ITETRA,4) 
            IPT3=IP2 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 6                                                     
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,4) 
            IPT2=IPTETRA(ITETRA,2) 
            IPT3=IP2 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 7                                                     
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,3) 
            IPT2=IPTETRA(ITETRA,2) 
            IPT3=IP3 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 8                                                     
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,2) 
            IPT2=IPTETRA(ITETRA,4) 
            IPT3=IP3 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 9                                                     
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,4) 
            IPT2=IPTETRA(ITETRA,3) 
            IPT3=IP3 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 10                                                    
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,1) 
            IPT2=IPTETRA(ITETRA,3) 
            IPT3=IP4 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 11                                                    
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,3) 
            IPT2=IPTETRA(ITETRA,4) 
            IPT3=IP4 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
!. Subtetrahedron 12                                                    
            NTETRA(IR)=NTETRA(IR)+1 
            IPT1=IPTETRA(ITETRA,4) 
            IPT2=IPTETRA(ITETRA,1) 
            IPT3=IP4 
            IPT4=IPC 
            IPTETRA(NITETRA+NTETRA(IR),1)=IPT1 
            IPTETRA(NITETRA+NTETRA(IR),2)=IPT2 
            IPTETRA(NITETRA+NTETRA(IR),3)=IPT3 
            IPTETRA(NITETRA+NTETRA(IR),4)=IPT4 
            SMAX=MAX(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            SMIN=MIN(SIGN(1D0,PHIV(IPT1)),SIGN(1D0,PHIV(IPT2)),SIGN(1D0,&
     &           PHIV(IPT3)),SIGN(1D0,PHIV(IPT4)))                      
            IF(SMAX*SMIN.LT.0.0) THEN 
               NTETRAINT(IR)=NTETRAINT(IR)+1 
               ITETRAINT(IR,NTETRAINT(IR))=NITETRA+NTETRA(IR) 
            ELSE 
               IF(SMIN.GT.0.0) THEN 
                  XV1=VP(IPT2,1)-VP(IPT4,1) 
                  YV1=VP(IPT2,2)-VP(IPT4,2) 
                  ZV1=VP(IPT2,3)-VP(IPT4,3) 
                  XV2=VP(IPT3,1)-VP(IPT4,1) 
                  YV2=VP(IPT3,2)-VP(IPT4,2) 
                  ZV2=VP(IPT3,3)-VP(IPT4,3) 
                  XN=YV1*ZV2-ZV1*YV2 
                  YN=ZV1*XV2-XV1*ZV2 
                  ZN=XV1*YV2-YV1*XV2 
                  XV1=VP(IPT1,1)-VP(IPT4,1) 
                  YV1=VP(IPT1,2)-VP(IPT4,2) 
                  ZV1=VP(IPT1,3)-VP(IPT4,3) 
                  VFBASE(IR)=VFBASE(IR)+(XN*XV1+YN*YV1+ZN*ZV1)/6.0D0 
               END IF 
            END IF 
         END DO 
      END DO 
!. Computation of total fluid volume VF                                 
      DO IV=1,NC 
         VFIR(IV)=0.0 
         DO IVV=1,IV 
            VFIR(IV)=VFIR(IV)+VFBASE(IVV) 
         END DO 
      END DO 
      DO IR=MAX(1,NC-1),NC 
      DO IV=1,NTETRAINT(IR) 
         ITETRA=ITETRAINT(IR,IV) 
!. Tetrahedron construction                                             
         NTP0=4 
         NTV0=4 
         NTS0=4 
         DO IS=1,4 
            NIPV0(IS)=3 
         END DO 
         VERTP0(1,1)=VP(IPTETRA(ITETRA,1),1) 
         VERTP0(1,2)=VP(IPTETRA(ITETRA,1),2) 
         VERTP0(1,3)=VP(IPTETRA(ITETRA,1),3) 
         PHIV0(1)=PHIV(IPTETRA(ITETRA,1)) 
         IF(SIGN(1D0,PHIV(IPTETRA(ITETRA,1))).GT.0.0) THEN 
            IA(1)=1 
         ELSE 
            IA(1)=0 
         END IF 
         VERTP0(2,1)=VP(IPTETRA(ITETRA,2),1) 
         VERTP0(2,2)=VP(IPTETRA(ITETRA,2),2) 
         VERTP0(2,3)=VP(IPTETRA(ITETRA,2),3) 
         PHIV0(2)=PHIV(IPTETRA(ITETRA,2)) 
         IF(SIGN(1D0,PHIV(IPTETRA(ITETRA,2))).GT.0.0) THEN 
            IA(2)=1 
         ELSE 
            IA(2)=0 
         END IF 
         VERTP0(3,1)=VP(IPTETRA(ITETRA,3),1) 
         VERTP0(3,2)=VP(IPTETRA(ITETRA,3),2) 
         VERTP0(3,3)=VP(IPTETRA(ITETRA,3),3) 
         PHIV0(3)=PHIV(IPTETRA(ITETRA,3)) 
         IF(SIGN(1D0,PHIV(IPTETRA(ITETRA,3))).GT.0.0) THEN 
            IA(3)=1 
         ELSE 
            IA(3)=0 
         END IF 
         VERTP0(4,1)=VP(IPTETRA(ITETRA,4),1) 
         VERTP0(4,2)=VP(IPTETRA(ITETRA,4),2) 
         VERTP0(4,3)=VP(IPTETRA(ITETRA,4),3) 
         PHIV0(4)=PHIV(IPTETRA(ITETRA,4)) 
         IF(SIGN(1D0,PHIV(IPTETRA(ITETRA,4))).GT.0.0) THEN 
            IA(4)=1 
         ELSE 
            IA(4)=0 
         END IF 
         IPV0(1,1)=1 
         IPV0(1,2)=2 
         IPV0(1,3)=3 
         IPV0(2,1)=2 
         IPV0(2,2)=1 
         IPV0(2,3)=4 
         IPV0(3,1)=3 
         IPV0(3,2)=2 
         IPV0(3,3)=4 
         IPV0(4,1)=1 
         IPV0(4,2)=3 
         IPV0(4,3)=4 
         DO IS=1,NTS0 
            IP1=IPV0(IS,1) 
            IP2=IPV0(IS,2) 
            IP3=IPV0(IS,3) 
            XV1=VERTP0(IP2,1)-VERTP0(IP1,1) 
            YV1=VERTP0(IP2,2)-VERTP0(IP1,2) 
            ZV1=VERTP0(IP2,3)-VERTP0(IP1,3) 
            XV2=VERTP0(IP3,1)-VERTP0(IP2,1) 
            YV2=VERTP0(IP3,2)-VERTP0(IP2,2) 
            ZV2=VERTP0(IP3,3)-VERTP0(IP2,3) 
            XN=YV1*ZV2-ZV1*YV2 
            YN=ZV1*XV2-XV1*ZV2 
            ZN=XV1*YV2-YV1*XV2 
            DMOD=(XN**2.0D0+YN**2.0D0+ZN**2.0D0)**0.5D0 
            XNS0(IS)=XN/DMOD 
            YNS0(IS)=YN/DMOD 
            ZNS0(IS)=ZN/DMOD 
         END DO 
         NTSINI=NTS0 
         CALL NEWPOL3D(IA,IPIA0,IPIA1,IPV0,ISCUT,NIPV0,NTP0,NTS0,NTV0,  &
     &        1.0d0,XNS0,0.0d0,YNS0,0.0d0,ZNS0)                         
!.. Location of the new intersection points                             
         IF(NTS0.GT.NTSINI) THEN 
            IS=NTS0 
            IS2=NTS0 
            DO IS=NTSINI+1,NTS0 
               SUMX=0.0 
               SUMY=0.0 
               SUMZ=0.0 
               DO IVV=1,NIPV0(IS) 
                  IP=IPV0(IS,IVV) 
                  IP0=IPIA0(IP) 
                  IP1=IPIA1(IP) 
                  VERTP0(IP,1)=VERTP0(IP0,1)-PHIV0(IP0)*(VERTP0(IP1,    &
     &                 1)-VERTP0(IP0,1))/(PHIV0(IP1)-PHIV0(IP0))        
                  VERTP0(IP,2)=VERTP0(IP0,2)-PHIV0(IP0)*(VERTP0(IP1,    &
     &                 2)-VERTP0(IP0,2))/(PHIV0(IP1)-PHIV0(IP0))        
                  VERTP0(IP,3)=VERTP0(IP0,3)-PHIV0(IP0)*(VERTP0(IP1,    &
     &                 3)-VERTP0(IP0,3))/(PHIV0(IP1)-PHIV0(IP0))        
                  SUMX=SUMX+VERTP0(IP,1) 
                  SUMY=SUMY+VERTP0(IP,2) 
                  SUMZ=SUMZ+VERTP0(IP,3) 
               END DO 
               NTP0=NTP0+1 
               VERTP0(NTP0,1)=SUMX/NIPV0(IS) 
               VERTP0(NTP0,2)=SUMY/NIPV0(IS) 
               VERTP0(NTP0,3)=SUMZ/NIPV0(IS) 
!     : The new face IS is replaced by NIPV(IS) triangular faces        
               DO IVV=1,NIPV0(IS) 
                  IS2=IS2+1 
                  IVV2=IVV+1 
                  IF(IVV2.GT.NIPV0(IS)) IVV2=1 
                  NIPV0(IS2)=3 
                  IPV0(IS2,1)=NTP0 
                  IPV0(IS2,2)=IPV0(IS,IVV) 
                  IPV0(IS2,3)=IPV0(IS,IVV2) 
                  XV1=VERTP0(IPV0(IS2,2),1)-VERTP0(IPV0(IS2,1),1) 
                  YV1=VERTP0(IPV0(IS2,2),2)-VERTP0(IPV0(IS2,1),2) 
                  ZV1=VERTP0(IPV0(IS2,2),3)-VERTP0(IPV0(IS2,1),3) 
                  XV2=VERTP0(IPV0(IS2,3),1)-VERTP0(IPV0(IS2,2),1) 
                  YV2=VERTP0(IPV0(IS2,3),2)-VERTP0(IPV0(IS2,2),2) 
                  ZV2=VERTP0(IPV0(IS2,3),3)-VERTP0(IPV0(IS2,2),3) 
                  XM=YV1*ZV2-ZV1*YV2 
                  YM=ZV1*XV2-XV1*ZV2 
                  ZM=XV1*YV2-YV1*XV2 
                  AMOD=(XM**2.0+YM**2.0+ZM**2.0)**0.5 
                  IF(AMOD.NE.0.0) THEN 
                     XNS0(IS2)=XM/AMOD 
                     YNS0(IS2)=YM/AMOD 
                     ZNS0(IS2)=ZM/AMOD 
                  ELSE 
                     NIPV0(IS2)=0 
                  END IF 
               END DO 
!* Cancel the IS face                                                   
               IF(IS2.GT.IS) NIPV0(IS)=0 
            END DO 
            NTS0=IS2 
         END IF 
         CALL TOOLV3D(IPV0,NIPV0,NTS0,VERTP0,VOLF,XNS0,YNS0,ZNS0) 
         VFIR(IR)=VFIR(IR)+VOLF 
      END DO 
      END DO 
      IF(NC.GT.1) THEN 
         RATIO=1.0D0/12D0**(1D0/3D0) 
!. Richardson extrapolation                                             
         VF=(VFIR(NC)-VFIR(NC-1)*RATIO**2)/(1D0-RATIO**2) 
         VF=VF/VOLT 
      ELSE 
         VF=VFIR(NC)/VOLT 
      END IF 
   10 CONTINUE 
      DEALLOCATE(IPTETRA,ITETRAINT,NTETRA,NTETRAINT,PHIV,VFBASE,VFIR,VP) 
      RETURN 
      END                                           
!------------------------- END OF INITFTETRA -------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
!                                PVFIT                                c 
! Polygonal-set Volumetric Fit                                        c 
!---------------------------------------------------------------------c 
! On entry:                                                           c 
!==========                                                           c 
! IORDER   = 2 (quadratic) or 3 (cubic) fit                           c 
! NIV      = number of vertices of each polygon                       c 
! NPOL     = number of polygons                                       c 
! VN0      = orthonormal basis (x,y,z)-components                     c 
! VP0      = reference point (x,y,z)-coordinates                      c 
! XN,YN,ZN = (x,y,z)-components of the unit-lenght normals to the     c 
!            polygons                                                 c 
! XV,YV,ZV = array containing the (x,y,z)-coordinates of every        c 
!            polygon vertices                                         c 
! On return:                                                          c 
!===========                                                          c 
! COEF     = coefficients of the fit hypersurface in the new          c 
!            orthonormal basis                                        c 
!---------------------------------------------------------------------c 
!---------------------------------------------------------------------c 
      SUBROUTINE PVFIT_bak(COEF,IORDER,NIV,NPOL,VN0,VP0,XN,XV,YN,YV,ZN,ZV)  &
     &     BIND(C)                                                      
!.. Scalar Arguments                                                    
      INTEGER(I_P), INTENT(IN) :: IORDER,NPOL 
!.. Array Arguments                                                     
      INTEGER(I_P), INTENT(IN) :: NIV(NS) 
      REAL(W_P), INTENT(IN) :: VN0(3,3),VP0(3),XN(NS),XV(NS,NV),        &
     &     YN(NS),YV(NS,NV),ZN(NS),ZV(NS,NV)                            
      INTEGER(I_P), PARAMETER :: N=6 
      INTEGER(I_P), PARAMETER :: N1=10 
      REAL(W_P), INTENT(OUT) :: COEF(N1) 
!.. Local Scalars                                                       
      INTEGER(I_P) :: I,I2,IEINV,IPOL,J,N0 
      REAL(W_P) :: BR1,BR2,BR3,DU,DV,F1,F2,FN,U1,U2,UN,V1,V2,VN,X1,X2,  &
     &     Y1,Y2,Z1,Z2                                            
!.. Local Arrays                                                        
      REAL(W_P) :: A(N,N),A1(N1,N1),AINV(N,N),AINV1(N1,N1),B(N),B1(N1), &
     &     R(N1),SOL(N),SOL1(N1),SR(N1)                                 
                                                                        
      IF(IORDER.EQ.2) THEN 
         N0=N 
      ELSE 
         N0=N1 
      END IF 
      DO I=1,N 
         B(I)=0.0 
         DO J=1,N 
            A(I,J)=0.0 
         END DO 
      END DO 
      IF(IORDER.EQ.3) THEN 
         DO I=1,N1 
            B1(I)=0.0 
            DO J=1,N1 
               A1(I,J)=0.0 
            END DO 
         END DO 
      END IF 
      DO IPOL=1,NPOL 
!         IC2=LINTCELLS(IN)                                             
!         IND2=INTIC(IC2)                                               
         FN=XN(IPOL)*VN0(1,1)+YN(IPOL)*VN0(1,2)+ZN(IPOL)*VN0(1,3) 
         UN=XN(IPOL)*VN0(2,1)+YN(IPOL)*VN0(2,2)+ZN(IPOL)*VN0(2,3) 
         VN=XN(IPOL)*VN0(3,1)+YN(IPOL)*VN0(3,2)+ZN(IPOL)*VN0(3,3) 
         X1=XV(IPOL,1) 
         Y1=YV(IPOL,1) 
         Z1=ZV(IPOL,1) 
         CALL SYSTRA(F1,U1,V1,VN0,VP0,X1,Y1,Z1) 
         BR1=(F1*FN+U1*UN+V1*VN)/FN 
         BR2=-UN/FN 
         BR3=-VN/FN 
         DO J=1,N 
            SR(J)=0.0 
         END DO 
!         DO IPLIC=1,NPLIC(IND2)                                        
         DO I=1,NIV(IPOL) 
            X1=XV(IPOL,I) 
            Y1=YV(IPOL,I) 
            Z1=ZV(IPOL,I) 
            CALL SYSTRA(F1,U1,V1,VN0,VP0,X1,Y1,Z1) 
            IF(I.EQ.NIV(IPOL)) THEN 
               I2=1 
            ELSE 
               I2=I+1 
            END IF 
            X2=XV(IPOL,I2) 
            Y2=YV(IPOL,I2) 
            Z2=ZV(IPOL,I2) 
            CALL SYSTRA(F2,U2,V2,VN0,VP0,X2,Y2,Z2) 
            DU=U2-U1 
            DV=V2-V1 
!                        R(1)=(U1*V2-U2*V1)/2.                          
            R(1)=(U2+U1)*DV/2. 
!     R(2)=((U1+U2)*(U1*V2-U2*V1))/6.                                   
            R(2)=(U2**2+U2*U1+U1**2)*DV/6. 
!                        R(3)=((V1+V2)*(U1*V2-U2*V1))/6.                
            R(3)=-(V2**2+V2*V1+V1**2)*DU/6. 
!                        R(4)=((U1+U2)*(U1**2+U2**2)*(V2-V1))/12.       
            R(4)=(4.*U1**3+6.*U1**2*DU+4.*U1*DU**2+DU**3)*              &
     &           DV/12.                                                 
!                        R(5)=((U1*V2-U2*V1)*(2*U1*V1+U1*V2+U2*V1+      
!     -                       2*U2*V2))/24.                             
            R(5)=(6.*U1*V1+2.*DU*DV+3.*U1*DV+3.*V1*DU)*(                &
     &           U1*DV-V1*DU)/24.                                       
!     R(6)=((U1-U2)*(V1+V2)*(V1**2+V2**2))/12.                          
            R(6)=-(4.*V1**3+6.*V1**2*DV+4.*V1*DV**2+DV**3)*             &
     &           DU/12.                                                 
            IF(IORDER.EQ.3) THEN 
               R(7)=(5.*U1**4+10.*U1**3*DU+10.*U1**2*DU**2+             &
     &              5.*U1*DU**3+DU**4)*DV/20.                           
!                        R(8)=(10.*U1**3*V1*DV+5.*U1**3*DV**2+          
!     -                       15.*U1**2*V1**2*DU+30.*U1**2*V1*DU*DV+    
!     -                       15.*U1**2*DU*DV**2+15.*U1*V1**2*DU**2+    
!     -                       30.*U1*V1*DU**2*DV+15.*U1*DU**2*DV**2+    
!     -                       5.*V1**2*DU**3+10.*V1*DU**3*DV+           
!     -                       5.*DU**3*DV**2)/60.                       
!                        R(9)=-(10.*V1**3*U1*DU+5.*V1**3*DU**2+         
!     -                       15.*V1**2*U1**2*DV+30.*V1**2*U1*DV*DU+    
!     -                       15.*V1**2*DV*DU**2+15.*V1*U1**2*DV**2+    
!     -                       30.*V1*U1*DV**2*DU+15.*V1*DV**2*DU**2+    
!     -                       5.*U1**2*DV**3+10.*U1*DV**3*DU+           
!     -                       5.*DV**3*DU**2)/60.                       
! NOTA IMPORTANTE. LAS INTEGRALES 8 Y 9 COMOENTADAS DEBEN ESTAR MAL     
!     LAS HE SUSTITUIDO POR LAS ILANGAKOON 22. REVISAR                  
               R(8)=(V2-V1)*(10*U1**3*(V1+V2)+10*U1**2*DU*              &
     &              (V1+2*V2)+5*U1*DU**2*(V1+3*V2)+DU**3*(              &
     &              V1+4*V2))/60                                        
               R(9)=(U1-U2)*(10*V1**3*(U1+U2)+10*V1**2*DV*              &
     &              (U1+2*U2)+5*V1*DV**2*(U1+3*U2)+DV**3*(              &
     &              U1+4*U2))/60                                        
               R(10)=-(5.*V1**4+10.*V1**3*DV+10.*V1**2*                 &
     &              DV**2+5.*V1*DV**3+DV**4)*DU/20.                     
            END IF 
            DO J=1,N0 
               SR(J)=SR(J)+R(J) 
            END DO 
         END DO 
!         END DO                                                        
         DO I=1,N 
            B(I)=B(I)+SR(I)*(BR1*SR(1)+BR2*SR(2)+BR3*SR(3)) 
            DO J=1,N 
               A(I,J)=A(I,J)+SR(I)*SR(J) 
            END DO 
         END DO 
         IF(IORDER.EQ.3) THEN 
            DO I=1,N1 
               B1(I)=B1(I)+SR(I)*(BR1*SR(1)+BR2*SR(2)+                  &
     &              BR3*SR(3))                                          
               DO J=1,N1 
                  A1(I,J)=A1(I,J)+SR(I)*SR(J) 
               END DO 
            END DO 
         END IF 
      END DO 
!. F(U,V)=SOL(1)+SOL(2)*U+SOL(3)*V+SOL(4)*U**2+SOL(5)*U*V+SOL(6)*V**2   
!. Solve the 6x6 linear system of equations                             
      IF(IORDER.EQ.3.AND.NPOL.GE.N1) THEN 
         CALL MATINVGAUSSJ(A1,AINV1,IEINV,N1)
         IF(IEINV.EQ.0) THEN
            SOL1=MATMUL(AINV1,B1)
         ELSE
            SOL1=0.0_W_P
         END IF
         DO I=1,N1 
            COEF(I)=SOL1(I) 
         END DO 
      ELSE 
         CALL MATINVGAUSSJ(A,AINV,IEINV,N) 
         IF(IEINV.EQ.0) THEN
            SOL=MATMUL(AINV,B)
         ELSE
            SOL=0.0_W_P
         END IF
         DO I=1,N 
            COEF(I)=SOL(I) 
         END DO 
      END IF 
!----------                                                             
      RETURN 
      END                                           
!---------------------------- END OF PVFIT ---------------------------c 
!---------------------------------------------------------------------c 
                                                                        
                                                                        
       
  END MODULE VOFTOOLS_MOD
