def mask_zz2snv(zz_in_dir=0,bed_out_dir=0,baseq_cutoff_dir=0):


	fi=open(zz_in_dir)
	fo=open(bed_out_dir,'w')

	fqua=open(baseq_cutoff_dir)
	limitbasequa=int(fqua.readline().replace('\n',''))
	fqua.close()
	limitad=1
	limitloc=5
	limitmpqua=0
	allsnv={}
	for line in fi:
		truesnv=[]
		seq=line[0:-1].split('\t')
		mismatch=seq[4].split(';')
		basequa=seq[5].split(',')
		loc=seq[9].split(',') #fragment-loc
		mpqua=int(seq[2])
		####################################################################
 		#change the sam flag 'seq[1]' when you didn't use "bwa -aln" as mapper
		seq[1]=int(seq[1])
		if len(bin(seq[1]))>=7:
			if bin(seq[1])[-3]!='1':
				if bin(seq[1])[-5]=='1':
					seq[1]='16'
				else:
					seq[1]='0'
		elif len(bin(seq[1]))>=5:
			if bin(seq[1])[-3]!='1':
				seq[1]='0'
					 		
		else: 
			seq[1]='0'
		#####################################################################
	
		
		
		if basequa[0]!='*' and mpqua >= limitmpqua and mpqua < 200:


				



			tmp_snv=[]
			i=0
			while i < len(basequa):
				if int(basequa[i]) >= limitbasequa  and  int(loc[i]) > limitloc  :

					truesnv.append([mismatch[i],seq[1],seq[8]])
				if int(loc[i])>limitloc:
					tmp_snv.append(mismatch[i])
					
				i=i+1
			
			fflag=1
			if len(tmp_snv)>0:
				tag=tmp_snv[0].split(':')[0]
				#fflag=1
				for one in tmp_snv:
					if one.split(':')[0] != tag:
						fflag=0
				
			

			if fflag==1:
				for snv in truesnv:
				
					try:
						allsnv[seq[0]+'\t'+snv[0].split(':')[0]+'\t'+snv[0].split(':')[1]][0]=allsnv[seq[0]+'\t'+snv[0].split(':')[0]+'\t'+snv[0].split(':')[1]][0]+1
						if (snv[1]=='16' and snv[2][-1] == '1' ) or (snv[1]=='0' and snv[2][-1] == '2' ):
							allsnv[seq[0]+'\t'+snv[0].split(':')[0]+'\t'+snv[0].split(':')[1]][1]=allsnv[seq[0]+'\t'+snv[0].split(':')[0]+'\t'+snv[0].split(':')[1]][1]+1
						elif (snv[1]=='16' and snv[2][-1] == '2' ) or (snv[1]=='0' and snv[2][-1] == '1' ):
							allsnv[seq[0]+'\t'+snv[0].split(':')[0]+'\t'+snv[0].split(':')[1]][2]=allsnv[seq[0]+'\t'+snv[0].split(':')[0]+'\t'+snv[0].split(':')[1]][2]+1
					except Exception, e:
						if (snv[1]=='16' and snv[2][-1] == '1' ) or (snv[1]=='0' and snv[2][-1] == '2' ):
							allsnv[seq[0]+'\t'+snv[0].split(':')[0]+'\t'+snv[0].split(':')[1]]=[1,1,0]
						elif (snv[1]=='16' and snv[2][-1] == '2' ) or (snv[1]=='0' and snv[2][-1] == '1' ):
							allsnv[seq[0]+'\t'+snv[0].split(':')[0]+'\t'+snv[0].split(':')[1]]=[1,0,1]

	snv_bed=[]
	for snv in allsnv:
		seq=snv.split('\t')
		if allsnv[snv][0]>=limitad:
				if allsnv[snv][1] > allsnv[snv][2]: 
					snv_bed.append([seq[0],int(seq[2]),seq[1],'+',allsnv[snv][0]])
				elif allsnv[snv][2] > allsnv[snv][1]:
					snv_bed.append([seq[0],int(seq[2]),seq[1],'-',allsnv[snv][0]])
				else:
					snv_bed.append([seq[0],int(seq[2]),seq[1],'.',allsnv[snv][0]])

	snv_bed.sort()
	for one in snv_bed:
		fo.write(one[0]+'\t'+str(one[1]-1)+'\t'+str(one[1])+'\t'+one[2]+'\t'+str(one[4])+'\t'+one[3]+'\n')
	fi.close()
	fo.close()

