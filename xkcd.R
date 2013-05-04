# Set the XKCD font
library(extrafont)
windowsFonts(Humor='Humor Sans')
par(family='Humor', col=rgb(0,0,0,0.3), pch=16, col='black', cex=1.5)

# Read in the data
data <- read.csv('xkcd_data.csv')

# Filetype stripchart
par(las=2)
plot(data$num, data$num, type='n', yaxt='n', ylab='', ylim=c(0, 500),
     main='Image Filetypes by Comic Number', xlab='Comic number')
stripchart(data$num[data$format=='PNG'], col='black', at=75, add=T, pch='|')
mtext('PNG ', 2, at=75, cex=1.25)
stripchart(data$num[data$format=='JPEG'], col='black', at=275, add=T, pch='|')
mtext('JPEG ', 2, at=275, cex=1.25)
stripchart(data$num[data$format=='GIF'], col='black', at=450, add=T, pch='|')
mtext('GIF ', 2, at=450, cex=1.25)

# Image mode stripchart
plot(data$num, data$num, type='n', yaxt='n', ylab='', ylim=c(0, 300),
     main='Image Mode by Comic Number', xlab='Comic number')
modes = paste(unique(data$mode))

for (i in 1:length(modes)){
  stripchart(data$num[data$mode==modes[i]], col='black', at=15+i*50, add=T, pch='|')
  mtext(paste(modes[i], " "), 2, at=15+i*50, cex=1.25)
}

# Filesize vs. size
plot(data$size, data$filesize, log='x', main='Filesize vs. Image Size', 
     xlab='Image Size (pixels^2)', ylab='filesize (kb)', cex=0.5, col=rgb(0,0,0,0.5))

# Fit log-log and plot
plo
plot(log(data$size), log(data$filesize), main='Filesize vs. Image Size', 
     xlab='log Image Size (pixels^2)', ylab='log filesize (kb)', cex=0.4, 
     col=rgb(0,0,0,0.5), ylim=c(0, 8))
abline(lfs)
summary(lfs)

# Luminosity
plot(data$num, data$lumen, main='Luminosity by Comic Number', cex=0.5,
     col=rgb(0,0,0,0.5), xlab='Comic Number', ylab='Luminosity')

hist(data$lumen, breaks=100, main='Distribution of Luminosity', xlab='Luminosity', 
     ylab='Count', col='black', xlim=c(0, 255))

# height vs. width
plot(data$width, data$height, log='y', cex=0.5, 
     main='Height vs. Width', xlab='Width (pixels)', ylab='Height (pixels)',
     col=rgb(0,0,0,0.5))

# width distribution
hist(data$width, breaks=500, col='black', 
     main='Distribution of Image Widths', xlab='Width (pixels)', ylab='Count')

# width by comic number
plot(data$num, data$width, main='Image Width by Comic Number', cex=0.5,
     col='black', xlab='Comic Number', ylab='Width (pixels)')

# height distribution
hist(data$height, breaks=500, col='black', 
     main='Distribution of Image Heights', xlab='Width (pixels)', ylab='Count')

# aspect versus comic number
plot(data$num, data$aspect, cex=0.5, main='Aspect Ratio by Comic Number',
     xlab='Comic Number', ylab='Aspect Ratio')

# aspect distribution
hist(data$aspect, breaks=200, col='black', ylab='Count', xlab='Aspect Ratio',
     main='Aspect Ratio Distribution', xaxp=c(0, 8, 8))

# filesize by comic number
plot(data$num, data$filesize, main='Filesize by Comic Number', cex=0.5,
     col='black', xlab='Comic Number', ylab='Filesize (kb)', log='y')

# filesize distribution
hist(data$filesize, breaks=250, col='black', xlab='Filesize (kb)', ylab='Count',
     main='Distribution of Filesizes', xlim=c(0,800))
