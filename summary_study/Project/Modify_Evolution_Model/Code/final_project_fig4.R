pr.cuckold <- function( a, b, k, p ){
a*(1-b)*(1-k)*(1-p)/(1+a*(1-b)*(1-k)*(1-p))
}

asr.sim <- function( f, m, q, t ){
ft = mt = qt = rep(NA, t)
if( m>f ){
ft[1]=f; mt[1]=m; qt[1]=q
for( i in 2:t ){
ft[i]<-ft[i-1]*(1-qt[i-1])
mt[i]<-mt[i-1] - qt[i-1]*ft[i-1]
qt[i]<-( qt[i-1]*mt[i-1]-qt[i-1]*ft[i-1] )/(mt[i-1]-qt[i-1]*ft[i-1])
}
}
if( f>=m ){
ft[1]=f; mt[1]=m; qt[1]=q
ft[2:t] <- f - q*m
mt[2:t] <- mt[1]*( 1 - qt[1] )
qt[2:t] <- 0
}
ans<-list( ft,mt,qt )
names( ans ) <- c("ft", "mt", "qt")
ans
}

# fitness of strategies
fitness <- function( p0, q0, t=100, c, u, b, f0, m0, k ){
# first find how the operational sex ratio changes through time
asr.dyn<-asr.sim( f=f0, m=m0, q=q0, t=t )
# reassign variables
ft <- asr.dyn$ft; mt <- asr.dyn$mt; qt <- asr.dyn$qt
# define vector for the frequency of PC over time
pt <- rep(NA, t); pt[1] <- p0
for( i in 2:t ) pt[i] <- pt[i-1] + ( qt[i-1] - qt[i] )/2
# define variables representing reproductive
# payoffs each time period
# for PC, MM, and MG males
vp <- ve <- vg <- 0
# loop over time periods
for( i in 1:t ){
if( mt[i]>0 ){ # if there are males left
# PC and MM relative frequencies (not counting MG males)
pc <- ifelse( qt[i]==1, 0, pt[i]/( 1 - qt[i] ) )
# prob of a female encountering a male after
# MG males have paired with females, set ceiling at one
# and condition for the last time step
apc <- min( 1, ifelse( i==t, mt[i]/ft[i], mt[i+1]*(1-qt[i+1]) / ft[i+1] ) )
# checks to make sure it is a valid value
apc <- ifelse( is.nan(apc), 0, apc)
apc <- ifelse( is.infinite(apc), 0, apc)
# now define variable y, defined in the main text
yt <- min( 1, ft[i]/mt[i] )
# calculate reproductive payoff at time i, following the main text
# parental care (vp)
vp <- vp + (1+c) * u^(i-1) * min( ft[i]/mt[i], 1) * ( 1 - pr.cuckold( a=apc, b=b, p=pc, k=k ) )
# multiple mating (ve)
f <- ifelse( (1 - pt[i] - qt[i]) > 0, yt * pt[i] / ( 1 - pt[i] - qt[i] ), 0 )
gt <- f * pr.cuckold( a=apc, b=b, p=pc, k=k )
zt <- ifelse( (1 - pt[i] - qt[i]) > 0, ( ft[i] - yt * mt[i] * (pt[i]+qt[i]) ) /
( mt[i] * (1 - pt[i] - qt[i] ) ), 0 )
ve <- ve + u^(i-1) * ( zt + gt*(1+c) )
# mate guarding (vg)
fnot <- ifelse( i>1, prod( sapply( seq(1,i-1,1), function(z) 1 - min( ft[z]/mt[z], 1) ) ), 1 )
vg <- vg + u^(i-1) * min( ft[i]/mt[i], 1) * 1/(1-u) * fnot
}
}
# return final fitness values
ans<-c( vp, vg, ve )
names(ans) <- c("Wp", "Wg", "We")
ans
}

delta.sim <- function( startx, starty, c=c, u=u, b=b, f0=f0, m0=m0, k=k ) {
p <- startx
q <- starty
## call to get fitness values
fitpq <- fitness(p0=p, q0=q, t=100, c=c, u=u, b=b, f0=f0, m0=m0, k=k)
fit <- c( fitpq["Wp"], fitpq["Wg"], fitpq["We"] ) # return fitnesses
wbar <- p*fit[1] + q*fit[2] + (1-p-q)*fit[3];
# change in PC frequency
dp <- p*fit[1]/wbar - p;
# change in MG frequency
dq <- q*fit[2]/wbar - q;
# change in MM frequency
dr <- (1-p-q)*fit[3]/wbar - (1-p-q);
# ensure the change in freq. adds up to 0
con <- ( dp + dq + dr )/3
dp <- ifelse( dp==0, 0, dp - con )
dq <- ifelse( dq==0, 0, dq - con )
dr <- ifelse( dr==0, 0, dr - con )
# return frequency changes
c(dp,dq,dr)
}

sim.pq <- function( p0, q0, time, c, u, b, f0, m0, k ){
pt <- qt <- rep(NA,time)
pt[1] <- p0
qt[1] <- q0
for( i in 2:time ){
deltapq <- delta.sim( pt[i-1], qt[i-1], c=c, u=u, b=b, f0=f0, m0=m0, k=k )
pt[i] <- pt[i-1] + deltapq[1]
qt[i] <- qt[i-1] + deltapq[2]
}
ans <- list(pt,qt); names(ans) <- c("pt","qt")
ans
}

sr.sim <- function( p0, q0, time=100, c=2, u=u_survival, b=0.3, k=1, plotit=FALSE){
# function for plot
mseq <- seq(50,150,5)
fseq <- rep(100,length(mseq) )
eq.strat <- matrix( rep(NA,2*length(mseq)), nrow=length(mseq) )
for( i in 1:length(mseq)){
strat.dyn <- sim.pq( p0=p0, q0=q0, time=time, c=c, u=u, b=b, f0=fseq[i], m0=mseq[i], k=k )
eq.strat[i,] <- c( strat.dyn$pt[time], strat.dyn$qt[time] )
}
ratio <- mseq / fseq
if( plotit==TRUE ){
windows()
plot( ratio, eq.strat[,1], axes=FALSE, type="n", ylab="", xlab="", ylim=c(0,1) )
axis( side=1)
mtext( "Sex ratio F/M", side=1, line=2)
mtext( "Equilibrium frequencies", side=2, line=2)
axis( side=2)
lines( ratio, eq.strat[,1], lty=1, lwd=2)
lines( ratio, eq.strat[,2], lty=2, lwd=2)
lines( ratio, 1 - eq.strat[,1] - eq.strat[,2], lty=3, lwd=2)
legend( "topright", legend=c("PC","MG", "MM"), lty=1:3)
}
ans <- list(eq.strat, ratio); names(ans) <- c("eq.strat", "ratio")
ans
}

# define ternary plot function
tern.asr = function(t, c, u, b, f0, m0, k, length=0.012, cont.pqby=0.025, phase.pqby=0.03,
t.contour=F, t.phase=F, t.arrows=F, labcex=0.8 ){
# game fitness function
game = function( p, q, w0=1 ){
ans = fitness(p0=p, q0=q, t=t, c=c, u=u, b=b, f0=f0, m0=m0, k=k)
c( ans["Wp"], ans["Wg"], ans["We"] ) # return fitnesses
}
# run baryplot
bary.init(col="white")
bary.labels("Paternal Care","Mate Guarding", "Multiple Mating")
if( t.contour==T ) bary.contour2(thegame = game, pqby=cont.pqby )
# phase plot
if( t.phase==T ) bary.phase(thegame = game, length = length, pqby=phase.pqby)
if( t.arrows==T ){
# around the center
bary.plotsim( 0.33, 0.33, arrow=TRUE, thegame=game )
bary.plotsim( 0.2, 0.2, arrow=TRUE, thegame=game )
bary.plotsim( 0.6, 0.2, arrow=TRUE, thegame=game )
bary.plotsim( 0.2, 0.6, arrow=TRUE, thegame=game )
}
}

sim.pq <- function( p0, q0, time, c, u, b, f0, m0, k ){
pt <- qt <- rep(NA,time)
pt[1] <- p0
qt[1] <- q0
for( i in 2:time ){
deltapq <- delta.sim( pt[i-1], qt[i-1], c=c, u=u, b=b, f0=f0, m0=m0, k=k )
pt[i] <- pt[i-1] + deltapq[1]
qt[i] <- qt[i-1] + deltapq[2]
}
ans <- list(pt,qt); names(ans) <- c("pt","qt")
ans
}

sr.sim <- function( p0, q0, time=100, c=2, u=0.9, b=0.3, k=1, plotit=FALSE){
# function for plot
mseq <- seq(50,150,5)
fseq <- rep(100,length(mseq) )
eq.strat <- matrix( rep(NA,2*length(mseq)), nrow=length(mseq) )
for( i in 1:length(mseq)){
strat.dyn <- sim.pq( p0=p0, q0=q0, time=time, c=c, u=u, b=b, f0=fseq[i], m0=mseq[i], k=k )
eq.strat[i,] <- c( strat.dyn$pt[time], strat.dyn$qt[time] )
}
ratio <- mseq / fseq
if( plotit==TRUE ){
windows()
plot( ratio, eq.strat[,1], axes=FALSE, type="n", ylab="", xlab="", ylim=c(0,1) )
axis( side=1)
mtext( "Sex ratio F/M", side=1, line=2)
mtext( "Equilibrium frequencies", side=2, line=2)
axis( side=2)
lines( ratio, eq.strat[,1], lty=1, lwd=2)
lines( ratio, eq.strat[,2], lty=2, lwd=2)
lines( ratio, 1 - eq.strat[,1] - eq.strat[,2], lty=3, lwd=2)
legend( "topright", legend=c("PC","MG", "MM"), lty=1:3)
}
ans <- list(eq.strat, ratio); names(ans) <- c("eq.strat", "ratio")
ans
}

#Figure4
# MM common low care high cuckoldry
mm_com_lh <- sr.sim( p0=0.005, q0=0.005, t=100, c=.01, u=0.9, b=0.3, k=0.1 )
# MM common low care low cuckoldry
mm_com_ll <- sr.sim( p0=0.005, q0=0.005, t=100, c=.01, u=0.9, b=0.3, k=1 )
# MM common high care high cuckoldry
mm_com_hh <- sr.sim( p0=0.005, q0=0.005, t=100, c=1, u=0.9, b=0.3, k=0.1 )
# MM common high care low cuckoldry
mm_com_hl <- sr.sim( p0=0.005, q0=0.005, t=100, c=1, u=0.9, b=0.3, k=1 )

windows(width=9, height=6)

par(oma=c(3,4,3,1), mar=c(2,4,2,1), mfcol=c(2,2), cex=0.8 )
plot( mm_com_lh$ratio, mm_com_lh$eq.strat[,1], axes=FALSE, type="n", ylab="", xlab="", ylim=c(0,1) )
axis( side=1, at=seq(0.6,2.0,0.2))
mtext( "Frequency of the Strategy at Equilibrium", side=2, line=3, cex=0.8, at=-0.3)
mtext( "Cuckoldry high (k = 0.1)", side=2, line=6, cex=0.8)
mtext( "Parental care low (c = 0.01)", side=3, line=3, cex=0.8 )

axis( side=2)
lines( mm_com_lh$ratio, mm_com_lh$eq.strat[,1], lty=1, lwd=2)
lines( mm_com_lh$ratio, mm_com_lh$eq.strat[,2], lty=2, lwd=2)
lines( mm_com_lh$ratio, 1 - mm_com_lh$eq.strat[,1] - mm_com_lh$eq.strat[,2], lty=3, lwd=2)
legend( "right", legend=c("Parental Care","Mate Guarding", "Multiple Mating"), lty=1:3, box.lwd=0,
cex=0.8)
plot(mm_com_ll$ratio, mm_com_ll$eq.strat[,1], axes=FALSE, type="n", ylab="", xlab="", ylim=c(0,1) )

axis( side=1)
mtext( "Sex ratio (males / females)", side=1,line=3, cex=0.8, at=1.6)
mtext( "No cuckoldry (k = 1)", side=2, line=6, cex=0.8)
mtext( "", side=3 )
axis( side=2)
lines( mm_com_ll$ratio, mm_com_ll$eq.strat[,1], lty=1, lwd=2)
lines( mm_com_ll$ratio, mm_com_ll$eq.strat[,2], lty=2, lwd=2)
lines( mm_com_ll$ratio, 1 - mm_com_ll$eq.strat[,1] - mm_com_ll$eq.strat[,2], lty=3, lwd=2)
plot( mm_com_hh$ratio, mm_com_hh$eq.strat[,1], axes=FALSE, type="n", ylab="", xlab="", ylim=c(0,1) )

axis( side=1)
#mtext( "Men's survival rate", side=1, line=3)
#mtext( "", side=2, line=2)
mtext( "Parental care high (c = 1)", side=3, line=3, cex=0.8)
axis( side=2)
lines( mm_com_hh$ratio, mm_com_hh$eq.strat[,1], lty=1, lwd=2)
lines( mm_com_hh$ratio, mm_com_hh$eq.strat[,2], lty=2, lwd=2)
lines( mm_com_hh$ratio, 1 - mm_com_hh$eq.strat[,1] - mm_com_hh$eq.strat[,2], lty=3, lwd=2)
plot( mm_com_hl$ratio, mm_com_hl$eq.strat[,1], axes=FALSE, type="n", ylab="", xlab="", ylim=c(0,1) )
axis( side=1)

#mtext( "Sex ratio Males/Females", side=1, line=3, cex=0.8)
mtext( "", side=2, line=2)
#mtext( "MM common", side=3 )
axis( side=2)
lines( mm_com_hl$ratio, mm_com_hl$eq.strat[,1], lty=1, lwd=2)
lines( mm_com_hl$ratio, mm_com_hl$eq.strat[,2], lty=2, lwd=2)
lines( mm_com_hl$ratio, 1 - mm_com_hl$eq.strat[,1] - mm_com_hl$eq.strat[,2], lty=3, lwd=2)

axis( side=2)
lines( mm_com_hl$ratio, mm_com_hl$eq.strat[,1], lty=1, lwd=2)
lines( mm_com_hl$ratio, mm_com_hl$eq.strat[,2], lty=2, lwd=2)
lines( mm_com_hl$ratio, 1 - mm_com_hl$eq.strat[,1] - mm_com_hl$eq.strat[,2], lty=3, lwd=2)