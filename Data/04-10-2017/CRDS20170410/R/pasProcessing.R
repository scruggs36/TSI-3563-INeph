# load libraries -----
library(aeRo)
library(dplyr)
library(zoo)

# import -----
pas <- importPAS('pas.txt', no.cols = 18) %>%
  # chooseFilterStart()
  chooseFilterStart(graph = FALSE, start = 1627)

# Calculate powers, backgrounds, and tau_0, and add to main data.frame -----
pas <- cbind(pas, getBg(pas)) %>%
  cbind(averagePower(pas)) %>%
  cbind(tau0_s = getTau0(pas$tau_sec))

# ------------------------------------
x <- unique(pas$bg406_mV)
bgs <- c()
for (i in 1:length(unique(x))) {
  if (i == 1 | i == length(unique(x))) { bgs[i] <- x[i] }
  else bgs <- c(bgs, mean(c(x[i], x[(i-1)], x[(i+1)])))
}
pas$bg406_mV <- fillToLength(bgs, period = 1800, ncol=1)

x <- unique(pas$bg532_mV)
bgs <- c()
for (i in 1:length(unique(x))) {
  if (i == 1 | i == length(unique(x))) { bgs[i] <- x[i] }
  else bgs <- c(bgs, mean(c(x[i], x[(i-1)], x[(i+1)])))
}
pas$bg532_mV <- fillToLength(bgs, period = 1800, ncol=1)

x <- unique(pas$bg662_mV)
bgs <- c()
for (i in 1:length(unique(x))) {
  if (i == 1 | i == length(unique(x))) { bgs[i] <- x[i] }
  else bgs <- c(bgs, mean(c(x[i], x[(i-1)], x[(i+1)])))
}
pas$bg662_mV <- fillToLength(bgs, period = 1800, ncol=1)

x <- unique(pas$bg785_mV)
bgs <- c()
for (i in 1:length(unique(x))) {
  if (i == 1 | i == length(unique(x))) { bgs[i] <- x[i] }
  else bgs <- c(bgs, mean(c(x[i], x[(i-1)], x[(i+1)])))
}
pas$bg785_mV <- fillToLength(bgs, period = 1800, ncol=1)

# ---------------------------------------------

# Convert data to absorption & extinction -----
pas <- cbind(pas, convertToAbs(pas[, 2:5], pas[, 19:22], pas[, 23:26], 114000)) %>%
  cbind(ext662_Mm = convertToExt(pas$tau_sec, pas$tau0_s, f_purge = 65))
# Set background periods to NA to cleanliness in plotting
pas[which(pas$filter_state == 1 | pas$elapsedTime_min > 23.5 | pas$elapsedTime_min < 2.0), 28:32] <- NA
pas$ext662_Mm[which(pas$ext662_Mm < 0)] <- NA
# Add rolling average via "zoo" pacakge, but exlude NAs
pas[!is.na(pas$abs406_Mm), 28:31] <- rollmean(na.exclude(pas[, 28:31]), k = 300, fill = NA)
pas[!is.na(pas$ext662_Mm), 32] <- rollmean(na.exclude(pas[, 32]), k = 300, fill = NA)

# plot -----
plot.abs(x = pas$Time, y = pas[, 28:32], lty = rep('solid', 5), col = c('purple', 'forestgreen', 'red', 'darksalmon', 'grey'), ylim = c(0, 30))
# legend(
#   locator(1), bty = 'n',
#   col = c('grey', 'purple', 'forestgreen', 'red', 'darksalmon'),
#   lty = 'solid', lwd = 2,
#   legend = c(
#     expression(paste(alpha[ext-662])),
#     expression(paste(alpha[abs-406])),
#     expression(paste(alpha[abs-532])),
#     expression(paste(alpha[abs-662])),
#     expression(paste(alpha[abs-785]))
#   )
# )

# write to TSV
# write.table(pas, file = 'pas_processed.txt', row.names = F, sep = '\t')
