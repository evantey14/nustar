PRO groupingPHA2, inputSRC, inputBKG, outfile, min, path

;; notes:  writes an ascii file with the output in three columns:
;;			minchan, maxcan, nchan
;; the channel numbers are inclusice


specSRC = mrdfits(inputSRC, 'SPECTRUM', /FSCALE, srcheader)
specBKG = mrdfits(inputBKG, 'SPECTRUM', /FSCALE, bkgheader)
;bkgBackscal = fxpar(bkgheader, 'BACKSCAL')
;srcBackscal = fxpar(srcheader, 'BACKSCAL')
bkgBackscal = fxpar(bkgheader, 'EXPOSURE')
srcBackscal = fxpar(srcheader, 'EXPOSURE')

subtracted = (specSRC.counts)-((specBKG.counts)*(srcBackscal/bkgBackscal))
;;from https://heasarc.gsfc.nasa.gov/xanadu/xspec/manual/XspecSpectralFitting.html for C(I)

print, "subtracted = ", subtracted

ChannelSize=(size(subtracted))[1]
maxChanNumber = (specSRC.channel)[ChannelSize-1]
tempsum=0.0
minchan = [0]
maxchan = [0]
minchanholder = 0
counter = 1

for i=0, ChannelSize-2 do begin

	tempsum = tempsum+(subtracted)[i]
	
	if (tempsum ge min) || (i eq ChannelSize-2) then begin
	
		if counter eq 1 then begin
			minchan[0] = 1
			maxchan[0] = (specSRC.channel)[i]
			counter = counter+1
		endif else if (i eq ChannelSize-2)then begin
			maxchan = [maxchan, maxChanNumber]
			minchan = [minchan, minchanholder]
		endif else begin
			if minchanholder ne i then begin
				maxchan = [maxchan, (specSRC.channel)[i]]
				minchan = [minchan, minchanholder]
			endif
		endelse
		
		tempsum = 0.0   ;resets tempsum to start the new group	
		minchanholder = (specSRC.channel)[i+1]
	endif
		
endfor
difference = maxchan-minchan+1


;; remove all single bin groups, if they exist
minchan = minchan[where(difference ne 1)]
maxchan = maxchan[where(difference ne 1)]
difference = difference[where(difference ne 1)]


;; remove all consecutive values that have the same grouping, 9999=placeholder
newdiff1 = [difference, 9999]
newdiff2 = [9999, difference]
badindices = where(newdiff1 eq newdiff2)
if badindices[0] ne -1 then begin
	remove, badindices, minchan
	remove, (badindices-1), maxchan, difference
endif


;;;; printing ASCII file
openw, lun2, outfile, /get_lun  
for j=0, (size(minchan))[1]-1 do begin
	printf, lun2, minchan[j], maxchan[j], difference[j]
endfor
close, lun2
free_lun, lun2

print, "* wrote grouping file" 

end
