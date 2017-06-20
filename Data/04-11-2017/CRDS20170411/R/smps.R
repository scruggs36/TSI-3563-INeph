smps <- read.delim("/Volumes/CHEM/Groups/Smith_G/MultiPAS-IV/ambient/20170303/smps.txt", "\t", skip = 15, header = T, check.names = F)
smps$Time <- as.POSIXct(paste(smps$Dat, smps$`Start Time`, sep = ''), format = '%m/%d/%y %H:%M:%S')

magplot(as.numeric(colnames(smps[5:111])), smps[414, 5:111], type = 'l', log = 'x', xlab = 'dia (nm)', ylab = 'dw/dlogDp', ylim = c(0, 25000), yaxs = 'i', xaxs = 'i', xlim = c(10, 1000), lwd = 2, col = 'chocolate4')
lines(as.numeric(colnames(smps[5:111])), smps[635, 5:111], col = 'chartreuse4', lwd = 2)
lines(as.numeric(colnames(smps[5:111])), smps[1001, 5:111], col = 'firebrick', lwd = 2)
legend(
  'top', cex = 0.75, bty = 'n',
  col = c('chocolate4', 'chartreuse4', 'firebrick'),
  lty = 'solid', lwd = 2,
  legend = c(
    'A', 'B', 'C'
  )
)
