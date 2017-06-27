library(shiny)
require(dplyr)
require(plyr)
require(ggplot2)
require(httr)
require(RCurl)

    
    neph <- read.csv(file = "/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-20-2017/NL170620.dat", head = F)%>%
      filter(V1 == 'D' | V1 =='T')
    
    # filter out data with no time value ----
    # for unknown reasons, some data points are accompanied by a row of time values
    filt = c()
    for (i in 1:nrow(neph)) {
      if (i == nrow(neph)) {
        rm(i)
        if (length(filt) == 0) {
          rm(filt)
          break()
        }
        else {
          neph = neph[-filt, ]
          rm(filt)
          break()
        }
      }
      else {
        if (neph[i, 1] == neph[(i+1), 1]) {
          filt <- append(filt, i)
        }}
    }
    
    # reorder data to give each extinction value a timepoint ----
    time <- filter(neph, V1 == 'T')
    neph <- filter(neph, V1 == 'D')
    neph$date <- as.Date(paste(time$V2, time$V3, time$V4, sep = '-'), format = '%Y-%m-%d')
    neph$hr   <- time$V5
    neph$min  <- time$V6
    
    # filter zero background points ----
    neph <- filter(neph, V2 != 'ZBXX') %>%
      select(4, 5, 6, 12, 13, 14) %>%
      setNames(c('Blue', 'Green', 'Red', 'Date', 'Hour', 'Min'))
    neph$Date_Hr <- as.POSIXct(paste(neph$Date, ' ', neph$Hour,':',neph$Min, ':00', sep = ''))
    
    # extract desied wavelengths ----
    neph.plot <- neph[ , c(which(colnames(neph) %in% input$data1)), drop = F]
    neph.plot <- stack(neph.plot) %>%
      setNames(c('Scatter', 'Band'))
    neph.plot$Date_Hr <- neph$Date_Hr
    color <- c('Red' = 'red', 'Green' = 'forestgreen', 'Blue' = 'blue')[which(c('Red', 'Green', 'Blue') %in% input$data1)]
    
    scatter.ymax <- input$scatter.ymax
    scatter.ymin <- input$scatter.ymin
    
    # draw neph plot -----
    p.neph <- ggplot(aes(x = Date_Hr, y = Scatter, color = Band), data = neph.plot) + 
      theme_bw() + xlab(' ')  + ylim(scatter.ymin, scatter.ymax) + xlab('Date/Time') +
      ylab(expression(paste('Sacttering (M',m^-1, ')'))) +
      geom_line() + 
      scale_colour_manual(values = color) +
      theme(legend.position = c(0, 1), legend.justification = c(0, 1))  #+ xlim(xmin, xmax)
    print(p.neph)
  
    neph <- read.csv(file  = "/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-20-2017/NL170620.dat", head = F)%>%
      filter(V1 == 'D' | V1 =='T')
    
    # filter out data with no time value ----
    # for unknown reasons, some data points are accompanied by a row of time values
    filt = c()
    for (i in 1:nrow(neph)) {
      if (i == nrow(neph)) {
        rm(i)
        if (length(filt) == 0) {
          rm(filt)
          break()
        }
        else {
          neph = neph[-filt, ]
          rm(filt)
          break()
        }
      }
      else {
        if (neph[i, 1] == neph[(i+1), 1]) {
          filt <- append(filt, i)
        }}
    }
    
    # reorder data to give each extinction value a timepoint ----
    time <- filter(neph, V1 == 'T')
    neph <- filter(neph, V1 == 'D')
    neph$date <- as.Date(paste(time$V2, time$V3, time$V4, sep = '-'), format = '%Y-%m-%d')
    neph$hr   <- time$V5
    neph$min  <- time$V6
    
    # filter zero background points ----
    neph <- filter(neph, V2 != 'ZBXX') %>%
      select(4, 5, 6, 12, 13, 14) %>%
      setNames(c('Blue', 'Green', 'Red', 'Date', 'Hour', 'Min'))
    neph$Date_Hr <- as.POSIXct(paste(neph$Date, ' ', neph$Hour,':',neph$Min, ':00', sep = ''))
    
    # convert from scattering to PM2.5 -----
    neph$PM_2.5 <- neph$Green / 3.2e-6 - 1.665e-6 #4e5 - 5
    PM2.5 <- group_by(neph, Date_Hr) %>%
      select(Date_Hr, PM_2.5)
    
    current <- PM2.5[nrow(PM2.5), 1:2]
    output$current <- renderText({
      paste(current$Date_Hr, as.character(current$PM_2.5))
    })
    
    
    #   # set axis limits -----
    pm.ymax <- input$pm.ymax
    pm.ymin <- input$pm.ymin
    
    # plot PM2.5 values -----
    p.pm <- ggplot(aes(x = Date_Hr, y = PM_2.5), data = PM2.5) + 
      theme_bw() + xlab(' ')  + ylim(pm.ymin, pm.ymax) +
      xlab('Date/Time') +
      ylab(expression(paste('[P',M[2.5], '] (', mu,'g ', m^-3,')'))) + geom_line(color = 'dodgerblue') #+ xlim(xmin, xmax)
    print(p.pm)
    
    write.csv(neph, file = "/home/austen/PycharmProjects/TSI-3563-INeph/Data/06-20-2017/NL170620Frame.csv", row.names = FALSE)
