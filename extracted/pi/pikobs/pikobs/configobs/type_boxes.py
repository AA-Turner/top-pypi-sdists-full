def type_boxes(fonction):
   if fonction=='omp':
       FNAM  = 'O-P'
       FNAMP = 'O-P'
       SUM   = 'SUMX'
       SUM2  = 'SUMX2'
   if fonction=='stdomp':
       FNAM  = 'O-P'
       FNAMP = 'O-P'
       SUM   = 'SUMX'
       SUM2  = 'SUMX2'

   if fonction=='bcorr':
       FNAM  = 'O-P'
       FNAMP = 'BCORR'
      #FNAMP = 'STATB'  pierre???
       SUM   = 'sumStat'
       SUM2  = 'sumStat2'
   if fonction=='oma':
       FNAM  = 'O-A'
       FNAMP = 'O-A'
       SUM   = 'SUMY'
       SUM2  = 'SUMY2'  
   if fonction=='stdoma':
       FNAM  = 'O-A'
       FNAMP = 'O-A'
       SUM   = 'SUMY'
       SUM2  = 'SUMY2'

   if fonction=='dens':
       FNAM="DENS"
       FNAMP="DENS"
       SUM='N'
       SUM2='N'
   if fonction=='nobs':
       FNAM="DENS"
       FNAMP="DENS"
       SUM='N'
       SUM2='N'
   if fonction=='obs':
       FNAM="OBS"
       FNAMP="OBS"
       SUM='SUMZ'
       SUM2='SUMZ2'

   return FNAM, FNAMP, SUM, SUM2

