"bary.click" <-
function(thegame=bary.game.hdr, color=FALSE, arrows=FALSE, ...) {
  ## takes a click as input and runs a simulation from that point
  pt <- locator(n=1);
  barypt <- bary.tobary( pt$x, pt$y );
  bary.plotsim( barypt[1] , barypt[2] , arrow=arrows , withcol=color , thegame=thegame, ... );
}
"bary.contour" <-
function( strat=1, thegame=bary.game.hdr, pqby=0.025, col.favored="gray" ) {
  ## plots regions of increase, decrease, and stasis of strat
  ## red = decrease, green = increase, white = no change
  for( i in seq(0,1,by=pqby) ) {
    for( j in seq(0,1,by=pqby) ) {
      p <- i;
      q <- j;
      if( p+q > 1 ) next;
      deltaxy <- bary.sim( p , q , thegame=thegame);
      origin <- c( p , q );
      delta <- deltaxy[strat];
      if( delta < 0 ) bary.point( origin , bg="white" , col="transparent" );
      if( delta > 0 ) bary.point( origin , bg=col.favored , col=col.favored );
      if( delta == 0 ) bary.point( origin , bg="blue" , col="transparent" );
    }
  }
  0;
}
"bary.contour2" <-
function( thegame=bary.game.hdr, pqby=0.025 ) {
  ## plots regions of increase, decrease, and stasis of strat
  ## red = decrease, green = increase, white = no change
  for( i in seq(0,1,by=pqby) ) {
    for( j in seq(0,1,by=pqby) ) {
      p <- i;
      q <- j;
      if( p+q > 1 ) next;
      deltaxy <- bary.sim( p , q , thegame=thegame);
      origin <- c( p , q );
      if( deltaxy[1] > 0 ) bary.point( origin , bg="white" , col=rgb(red=0, green=0, blue=1, alpha=0.5 ) );
      if( deltaxy[2] > 0 ) bary.point( origin , bg="white" , col=rgb( red=1, green=1, blue=0, alpha=0.5 ) );
      if( deltaxy[3] > 0 ) bary.point( origin , bg="white" , col=rgb( red=1, green=0, blue=0, alpha=0.5 ) );
    }
  }
  0;
}
"bary.drawarrow" <-
function( pt1 , pt2 , length=0.025 , col="black" ) {
  ## this draws a basic 45 degree barbed simple line arrow
  ## get screen coords
  dest <- bary.toscreen( pt2[1], pt2[2] );
  origin <- bary.toscreen( pt1[1], pt1[2] );
  ## Find the arrow shaft unit vector.
  vx <- (dest[1] - origin[1]);
  vy <- (dest[2] - origin[2]);
  dist <- sqrt(vx * vx + vy * vy);
  vx <- vx / dist;
  vy <- vy / dist;
  ## Draw the right barb.
    ax <- (-vy - vx);
    ay <- (vx - vy);
  ## Set the proper length.
  ax <- ax * length + dest[1];
  ay <- ay * length + dest[2];
  lines( c( dest[1],ax ) , c( dest[2],ay ) , col=col );
  ## Find the left barb.
    ax <- (vy - vx);
    ay <- (-vx - vy);
  ax <- ax * length + dest[1];
  ay <- ay * length + dest[2];
  lines( c( dest[1],ax ) , c( dest[2],ay ) , col=col );
}
"bary.game.hdr" <-
function( p, q, r, v=2, c=3, w0=5 ) {
  w1 <- (p+q)*(v-c)/2 + r*v + w0;
  w2 <- p*(v-c)/2 + (1-p)*v/2 + w0;
  w3 <- (1-p)*v/2 + w0;
  c(w1,w2,w3);
}
"bary.game.rps" <-
function( p, q, r, b=4 , c=-2 , w0=15 ) {
  w1 <- p*0 + q*b + r*c + w0;
  w2 <- p*c + q*0 + r*b + w0;
  w3 <- p*b + q*c + r*0 + w0;
  c(w1,w2,w3);
}
"bary.game.tft" <-
function( p, q, r, b=2, c=1, w=0.75, w0=15 ) {
  w1 <- (p+q)*(b-c)/(1-w) + r*(-c) + w0;
  w2 <- (p+q)*(b-c)/(1-w) + r*(-c)/(1-w) + w0;
  w3 <- p*b + q*b/(1-w) + w0;
  c(w1,w2,w3);
}
"bary.goodarrow" <-
function( origin , dest , length=0.025 , col="black" , border="black" , angle=pi/6 , backdist=1/2 ) {
  ## draws nice looking filled arrow
  ## get screen coords
  ##dest <- bary.toscreen( pt2[1], pt2[2] );
  ##origin <- bary.toscreen( pt1[1], pt1[2] );
  ## get angle and distance of vector, treating dest as origin
  obj <- bary.screen2polar( dest, origin );
  theta <- obj[1];
  dist <- obj[2];
  ## compute barbs
  barbleft <- bary.polar2screen( length , dest , (theta - angle) );
  barbright <- bary.polar2screen( length , dest , (theta + angle) );
  ## make polygon
  back <- bary.polar2screen( length*backdist , dest , theta );
  polyx <- c( dest[1] , barbleft[1] , back[1] , barbright[1] );
  polyy <- c( dest[2] , barbleft[2] , back[2] , barbright[2] );
  ## draw filled polygon
  polygon( polyx , polyy , col=col , border=border );
  theta;
}
"bary.init" <-
function(l=1, col="black") {
  ## initializes window, coordinates, and draws triangle
  plot.new();
  plot.window(c(0,1), c(0,1), asp=1 );
  bary.line( c(0,0), c(0,1), l=l, col=col, lwd=2 );
  bary.line( c(0,0), c(1,0), l=l, col=col, lwd=2 );
  bary.line( c(1,0), c(0,1), l=l, col=col, lwd=2 );
}
"bary.labels" <-
function( right, top, left, cex=1 ) {
  ## labels for strategies
  text( -0.05, 0.02, left, xpd=NA, adj=c(0.5,3), cex=cex );
  text( 1.05, 0.02, right, xpd=NA, adj=c(0.5,3), cex=cex );
  text( 0.5, 1.05, top, xpd=NA, adj=c(0.5,3), cex=cex );
}
"bary.line" <-
function( point1 , point2, arrow=FALSE, l=1, col="black", lwd=1 ) {
  pt1 <- bary.toscreen(point1[1], point1[2]);
  pt2 <- bary.toscreen(point2[1], point2[2]);
  lines( c(pt1[1],pt2[1]), c(pt1[2],pt2[2]), lty=l, col=col, lwd=lwd );
  if( arrow ) bary.goodarrow( pt1, pt2, length=0.025, col=col, border=col );
}
"bary.locate" <-
function( point=0 ) {
  ## draws point and then draws distances to it as dashed lines
  if( length(point)==1 ) {
    cpt <- locator(n=1);
    point <- bary.tobary(cpt$x,cpt$y);
  }
  bary.line( c( bary.toscreen(point[1],point[2])[1] , 0 ), point, l=2 );
  bary.line( c( 0 , bary.toscreen(point[2],point[1])[1] ), point, l=2 );
  r <- 1 - point[1] - point[2];
  x <- bary.toscreen( point[1] , r )[1];
  y <- bary.toscreen( point[2] , r )[1];
  bary.line( c( x , y ), point, l=2 );
  bary.point( point );
  point;
}
"bary.makecolor" <-
function(scolor) {
  rr <- 2*scolor - 1;
  if(rr < 0) rr <- 0;
  gg <- 2*scolor;
  if(gg > 1) gg <- (-2)*scolor + 2;
  bb <- -2*scolor + 1;
  if(bb < 0) bb <- 0;
  #rgb(rr,gg,bb);
  gray( 0.2 );
}
"bary.maxvelocity" <-
function(thegame=bary.game.hdr,...) {
  ## finds maximum velocity in system
  maxdist <- 0;
  for( i in seq(0,1,by=0.025) ) {
    for( j in seq(0,1,by=0.025) ) {
      p <- i;
      q <- j;
      if( p+q > 1 ) next;
      deltaxy <- bary.sim( p , q , thegame=thegame );
      dist <- sqrt( deltaxy[1]^2 + deltaxy[2]^2 );
      if(dist > maxdist) maxdist <- dist;
    }
  }
  maxdist;
}
bary.phase <-
function(thegame=bary.game.hdr , length=0.02 , pqby = 0.025) {
  ## plots an arrow at each cell of ternary plot
  ## direction of arrow shows trajectory at that point
  ## color shows velocity, blue=slowest, red=fastest
  ## --
  ## first, find maximum velocity
  maxdist <- bary.maxvelocity(thegame=thegame);
  ## now plot arrows
  for( i in seq(0,1,by= pqby) ) {
    for( j in seq(0,1,by= pqby) ) {
      p <- i;
      q <- j;
      if( p+q > 1 ) next;
      deltaxy <- bary.sim( p , q , thegame=thegame );
      dist <- sqrt( deltaxy[1]^2 + deltaxy[2]^2 );
      newpt <- c( p - deltaxy[1] , q - deltaxy[2] );
      origin <- c( p , q );
      pt1 <- bary.toscreen( newpt[1] , newpt[2] );
      pt2 <- bary.toscreen( p , q );
      bc <- bary.makecolor(dist/maxdist);
      bary.goodarrow( pt1 , pt2 , length=length , col=bc , border=bc );
    }
  }
}
"bary.placearrow" <-
function(thegame=bary.game.hdr, ...) {
  ## takes a click as input and draws good arrow at that point, showing system traj
  pt <- locator(n=1);
  barypt <- bary.tobary( pt$x , pt$y );
  p <- barypt[1];
  q <- barypt[2];
  deltaxy <- bary.sim( p , q , thegame=thegame , ... );
  ##dist <- sqrt( deltaxy[1]^2 + deltaxy[2]^2 );
  newpt <- c( p - deltaxy[1] , q - deltaxy[2] );
  origin <- c( p , q );
  pt1 <- bary.toscreen( newpt[1] , newpt[2] );
  pt2 <- bary.toscreen( p , q );
  bary.goodarrow( pt1 , pt2 , length=0.025 );
}
"bary.plotsim" <-
function( sx , sy , arrow=FALSE , withcol=FALSE, thegame=bary.game.hdr, ... ) {
  ## takes a starting point and plots a simulation trajectory
  ## arrow=TRUE plots arrows to show direction of path
  x <- sx;
  y <- sy;
  if(withcol) maxv <- bary.maxvelocity(thegame=thegame, ...);
  dist <- 1;
  arrowcount <- 0;
  while(dist > 0.00001) {
    deltaxy <- bary.sim( x , y , thegame=thegame , ... );
    newpt <- c( deltaxy[1] + x, deltaxy[2] + y );
    # make sure we don't plot outside boundaries
    norm <- (deltaxy[1] + x)+(deltaxy[2]+y)+(deltaxy[3]+(1-x-y))
    newpt <- newpt / norm
    
    origin <- c( x, y );
    arrowflag <- FALSE;
    if( arrowcount > 0.25 && arrow ) {
      arrowcount <- 0;
      arrowflag <- TRUE;
    }
    dist <- sqrt( deltaxy[1]^2 + deltaxy[2]^2 );
    acolor <- "black";
    if(withcol) acolor <- bary.makecolor(dist/maxv);
    bary.line( origin, newpt, arrow=arrowflag, col=acolor );
    arrowcount <- arrowcount + dist;
    x <- newpt[1];
    y <- newpt[2];
  }
  c( c(sx,sy), c(x, y) );
}
"bary.point" <-
function( point1, pch=15, bg="white", col="black" ) {
  ## default point is an empty circle
  pt <- bary.toscreen(point1[1], point1[2]);
  points( pt[1], pt[2], pch=pch, bg=bg, col=col, cex=0.3 );
}
"bary.polar2screen" <-
function( dist, origin, theta ) {
  ## takes dist, angle and origin and returns x and y of destination point
  vx <- cos(theta) * dist;
  vy <- sin(theta) * dist;
  c( origin[1]+vx , origin[2]+vy );
}
"bary.screen2polar" <-
function( origin, dest ) {
  ## takes two points and returns distance and angle, from origin to dest
  vx <- dest[1] - origin[1];
  vy <- dest[2] - origin[2];
  dist <- sqrt( vx*vx + vy*vy );
  theta <- asin( abs(vy) / dist );
  ## correct for quadrant
  if( vx < 0 && vy < 0 ) theta <- pi + theta; # lower-left
  if( vx < 0 && vy > 0 ) theta <- pi - theta; # upper-left
  if( vx > 0 && vy < 0 ) theta <- 2*pi - theta; # lower-right
  if( vx < 0 && vy==0 ) theta <- pi;
  if( vx==0 && vy < 0 ) theta <- 3*pi/2; 
  ## return angle and dist
  c( theta, dist );
}
"bary.sim" <-
function( startx, starty, thegame=bary.game.hdr ) {
  p <- startx;
  q <- starty;
  ## call the game function to get fitness values
  fit <- thegame( p, q );
  test <- c(fit,p,q); names(test) <- c("Wp","Wg","We","p","q")
  print(test)
  wbar <- p*fit[1] + q*fit[2] + (1-p-q)*fit[3];
  dp <- p*fit[1]/wbar - p;
  dq <- q*fit[2]/wbar - q;
  dr <- (1-p-q)*fit[3]/wbar - (1-p-q);
  # ensure the change in freq. adds up to 0
  con <- ( dp + dq + dr )/3
  dp <- ifelse( dp==0, 0, dp - con )
  dq <- ifelse( dq==0, 0, dq - con )
  dr <- ifelse( dr==0, 0, dr - con )
  
  test2 <- c(dp+dq+dr); names(test2) <- c("net_change")
  print( test2 )   

  c(dp,dq,dr);
}
"bary.tobary" <-
function( u , v ) {
  theheight <- 1;
  thewidth <- 1;
  uw <- u / thewidth;
  vw <- v / thewidth;
  y <- vw * 1.14142;
  x <- uw - y/2;
  c( x , y );
}
"bary.toscreen" <-
function(x,y) {
    ## converts barycentric coords to cartesian screen coords
    ## x is freq of strat in lower right
    ## y is freq of strat at top
    ## thus 1-x-y is freq of strat in lower left
    theheight <- 1;
    thewidth <- 1;
    c( (x + y/2)*thewidth , (y/1.14142)*thewidth );   
}
"bary.click" <-
function(thegame=bary.game.hdr, color=FALSE, arrows=FALSE, ...) {
  ## takes a click as input and runs a simulation from that point
  pt <- locator(n=1);
  barypt <- bary.tobary( pt$x, pt$y );
  bary.plotsim( barypt[1] , barypt[2] , arrow=arrows , withcol=color , thegame=thegame, ... );
}
"bary.contour" <-
function( strat=1, thegame=bary.game.hdr, pqby=0.025, col.favored="gray" ) {
  ## plots regions of increase, decrease, and stasis of strat
  ## red = decrease, green = increase, white = no change
  for( i in seq(0,1,by=pqby) ) {
    for( j in seq(0,1,by=pqby) ) {
      p <- i;
      q <- j;
      if( p+q > 1 ) next;
      deltaxy <- bary.sim( p , q , thegame=thegame);
      origin <- c( p , q );
      delta <- deltaxy[strat];
      if( delta < 0 ) bary.point( origin , bg="white" , col="transparent" );
      if( delta > 0 ) bary.point( origin , bg=col.favored , col=col.favored );
      if( delta == 0 ) bary.point( origin , bg="blue" , col="transparent" );
    }
  }
  0;
}
"bary.contour2" <-
function( thegame=bary.game.hdr, pqby=0.025 ) {
  ## plots regions of increase, decrease, and stasis of strat
  ## red = decrease, green = increase, white = no change
  for( i in seq(0,1,by=pqby) ) {
    for( j in seq(0,1,by=pqby) ) {
      p <- i;
      q <- j;
      if( p+q > 1 ) next;
      deltaxy <- bary.sim( p , q , thegame=thegame);
      origin <- c( p , q );
      if( deltaxy[1] > 0 ) bary.point( origin , bg="white" , col=rgb(red=0, green=0, blue=1, alpha=0.5 ) );
      if( deltaxy[2] > 0 ) bary.point( origin , bg="white" , col=rgb( red=1, green=1, blue=0, alpha=0.5 ) );
      if( deltaxy[3] > 0 ) bary.point( origin , bg="white" , col=rgb( red=1, green=0, blue=0, alpha=0.5 ) );
    }
  }
  0;
}
"bary.drawarrow" <-
function( pt1 , pt2 , length=0.025 , col="black" ) {
  ## this draws a basic 45 degree barbed simple line arrow
  ## get screen coords
  dest <- bary.toscreen( pt2[1], pt2[2] );
  origin <- bary.toscreen( pt1[1], pt1[2] );
  ## Find the arrow shaft unit vector.
  vx <- (dest[1] - origin[1]);
  vy <- (dest[2] - origin[2]);
  dist <- sqrt(vx * vx + vy * vy);
  vx <- vx / dist;
  vy <- vy / dist;
  ## Draw the right barb.
    ax <- (-vy - vx);
    ay <- (vx - vy);
  ## Set the proper length.
  ax <- ax * length + dest[1];
  ay <- ay * length + dest[2];
  lines( c( dest[1],ax ) , c( dest[2],ay ) , col=col );
  ## Find the left barb.
    ax <- (vy - vx);
    ay <- (-vx - vy);
  ax <- ax * length + dest[1];
  ay <- ay * length + dest[2];
  lines( c( dest[1],ax ) , c( dest[2],ay ) , col=col );
}
"bary.game.hdr" <-
function( p, q, r, v=2, c=3, w0=5 ) {
  w1 <- (p+q)*(v-c)/2 + r*v + w0;
  w2 <- p*(v-c)/2 + (1-p)*v/2 + w0;
  w3 <- (1-p)*v/2 + w0;
  c(w1,w2,w3);
}
"bary.game.rps" <-
function( p, q, r, b=4 , c=-2 , w0=15 ) {
  w1 <- p*0 + q*b + r*c + w0;
  w2 <- p*c + q*0 + r*b + w0;
  w3 <- p*b + q*c + r*0 + w0;
  c(w1,w2,w3);
}
"bary.game.tft" <-
function( p, q, r, b=2, c=1, w=0.75, w0=15 ) {
  w1 <- (p+q)*(b-c)/(1-w) + r*(-c) + w0;
  w2 <- (p+q)*(b-c)/(1-w) + r*(-c)/(1-w) + w0;
  w3 <- p*b + q*b/(1-w) + w0;
  c(w1,w2,w3);
}
"bary.goodarrow" <-
function( origin , dest , length=0.025 , col="black" , border="black" , angle=pi/6 , backdist=1/2 ) {
  ## draws nice looking filled arrow
  ## get screen coords
  ##dest <- bary.toscreen( pt2[1], pt2[2] );
  ##origin <- bary.toscreen( pt1[1], pt1[2] );
  ## get angle and distance of vector, treating dest as origin
  obj <- bary.screen2polar( dest, origin );
  theta <- obj[1];
  dist <- obj[2];
  ## compute barbs
  barbleft <- bary.polar2screen( length , dest , (theta - angle) );
  barbright <- bary.polar2screen( length , dest , (theta + angle) );
  ## make polygon
  back <- bary.polar2screen( length*backdist , dest , theta );
  polyx <- c( dest[1] , barbleft[1] , back[1] , barbright[1] );
  polyy <- c( dest[2] , barbleft[2] , back[2] , barbright[2] );
  ## draw filled polygon
  polygon( polyx , polyy , col=col , border=border );
  theta;
}
"bary.init" <-
function(l=1, col="black") {
  ## initializes window, coordinates, and draws triangle
  plot.new();
  plot.window(c(0,1), c(0,1), asp=1 );
  bary.line( c(0,0), c(0,1), l=l, col=col, lwd=2 );
  bary.line( c(0,0), c(1,0), l=l, col=col, lwd=2 );
  bary.line( c(1,0), c(0,1), l=l, col=col, lwd=2 );
}
"bary.labels" <-
function( right, top, left, cex=1 ) {
  ## labels for strategies
  text( -0.05, 0.02, left, xpd=NA, adj=c(0.5,3), cex=cex );
  text( 1.05, 0.02, right, xpd=NA, adj=c(0.5,3), cex=cex );
  text( 0.5, 1.05, top, xpd=NA, adj=c(0.5,3), cex=cex );
}
"bary.line" <-
function( point1 , point2, arrow=FALSE, l=1, col="black", lwd=1 ) {
  pt1 <- bary.toscreen(point1[1], point1[2]);
  pt2 <- bary.toscreen(point2[1], point2[2]);
  lines( c(pt1[1],pt2[1]), c(pt1[2],pt2[2]), lty=l, col=col, lwd=lwd );
  if( arrow ) bary.goodarrow( pt1, pt2, length=0.025, col=col, border=col );
}
"bary.locate" <-
function( point=0 ) {
  ## draws point and then draws distances to it as dashed lines
  if( length(point)==1 ) {
    cpt <- locator(n=1);
    point <- bary.tobary(cpt$x,cpt$y);
  }
  bary.line( c( bary.toscreen(point[1],point[2])[1] , 0 ), point, l=2 );
  bary.line( c( 0 , bary.toscreen(point[2],point[1])[1] ), point, l=2 );
  r <- 1 - point[1] - point[2];
  x <- bary.toscreen( point[1] , r )[1];
  y <- bary.toscreen( point[2] , r )[1];
  bary.line( c( x , y ), point, l=2 );
  bary.point( point );
  point;
}
"bary.makecolor" <-
function(scolor) {
  rr <- 2*scolor - 1;
  if(rr < 0) rr <- 0;
  gg <- 2*scolor;
  if(gg > 1) gg <- (-2)*scolor + 2;
  bb <- -2*scolor + 1;
  if(bb < 0) bb <- 0;
  #rgb(rr,gg,bb);
  gray( 0.2 );
}
"bary.maxvelocity" <-
function(thegame=bary.game.hdr,...) {
  ## finds maximum velocity in system
  maxdist <- 0;
  for( i in seq(0,1,by=0.025) ) {
    for( j in seq(0,1,by=0.025) ) {
      p <- i;
      q <- j;
      if( p+q > 1 ) next;
      deltaxy <- bary.sim( p , q , thegame=thegame );
      dist <- sqrt( deltaxy[1]^2 + deltaxy[2]^2 );
      if(dist > maxdist) maxdist <- dist;
    }
  }
  maxdist;
}
bary.phase <-
function(thegame=bary.game.hdr , length=0.02 , pqby = 0.025) {
  ## plots an arrow at each cell of ternary plot
  ## direction of arrow shows trajectory at that point
  ## color shows velocity, blue=slowest, red=fastest
  ## --
  ## first, find maximum velocity
  maxdist <- bary.maxvelocity(thegame=thegame);
  ## now plot arrows
  for( i in seq(0,1,by= pqby) ) {
    for( j in seq(0,1,by= pqby) ) {
      p <- i;
      q <- j;
      if( p+q > 1 ) next;
      deltaxy <- bary.sim( p , q , thegame=thegame );
      dist <- sqrt( deltaxy[1]^2 + deltaxy[2]^2 );
      newpt <- c( p - deltaxy[1] , q - deltaxy[2] );
      origin <- c( p , q );
      pt1 <- bary.toscreen( newpt[1] , newpt[2] );
      pt2 <- bary.toscreen( p , q );
      bc <- bary.makecolor(dist/maxdist);
      bary.goodarrow( pt1 , pt2 , length=length , col=bc , border=bc );
    }
  }
}
"bary.placearrow" <-
function(thegame=bary.game.hdr, ...) {
  ## takes a click as input and draws good arrow at that point, showing system traj
  pt <- locator(n=1);
  barypt <- bary.tobary( pt$x , pt$y );
  p <- barypt[1];
  q <- barypt[2];
  deltaxy <- bary.sim( p , q , thegame=thegame , ... );
  ##dist <- sqrt( deltaxy[1]^2 + deltaxy[2]^2 );
  newpt <- c( p - deltaxy[1] , q - deltaxy[2] );
  origin <- c( p , q );
  pt1 <- bary.toscreen( newpt[1] , newpt[2] );
  pt2 <- bary.toscreen( p , q );
  bary.goodarrow( pt1 , pt2 , length=0.025 );
}
"bary.plotsim" <-
function( sx , sy , arrow=FALSE , withcol=FALSE, thegame=bary.game.hdr, ... ) {
  ## takes a starting point and plots a simulation trajectory
  ## arrow=TRUE plots arrows to show direction of path
  x <- sx;
  y <- sy;
  if(withcol) maxv <- bary.maxvelocity(thegame=thegame, ...);
  dist <- 1;
  arrowcount <- 0;
  while(dist > 0.00001) {
    deltaxy <- bary.sim( x , y , thegame=thegame , ... );
    newpt <- c( deltaxy[1] + x, deltaxy[2] + y );
    # make sure we don't plot outside boundaries
    norm <- (deltaxy[1] + x)+(deltaxy[2]+y)+(deltaxy[3]+(1-x-y))
    newpt <- newpt / norm
    
    origin <- c( x, y );
    arrowflag <- FALSE;
    if( arrowcount > 0.25 && arrow ) {
      arrowcount <- 0;
      arrowflag <- TRUE;
    }
    dist <- sqrt( deltaxy[1]^2 + deltaxy[2]^2 );
    acolor <- "black";
    if(withcol) acolor <- bary.makecolor(dist/maxv);
    bary.line( origin, newpt, arrow=arrowflag, col=acolor );
    arrowcount <- arrowcount + dist;
    x <- newpt[1];
    y <- newpt[2];
  }
  c( c(sx,sy), c(x, y) );
}
"bary.point" <-
function( point1, pch=15, bg="white", col="black" ) {
  ## default point is an empty circle
  pt <- bary.toscreen(point1[1], point1[2]);
  points( pt[1], pt[2], pch=pch, bg=bg, col=col, cex=0.3 );
}
"bary.polar2screen" <-
function( dist, origin, theta ) {
  ## takes dist, angle and origin and returns x and y of destination point
  vx <- cos(theta) * dist;
  vy <- sin(theta) * dist;
  c( origin[1]+vx , origin[2]+vy );
}

"bary.sim" <-
function( startx, starty, thegame=bary.game.hdr ) {
  p <- startx;
  q <- starty;
  ## call the game function to get fitness values
  fit <- thegame( p, q );
  test <- c(fit,p,q); names(test) <- c("Wp","Wg","We","p","q")
  print(test)
  wbar <- p*fit[1] + q*fit[2] + (1-p-q)*fit[3];
  dp <- p*fit[1]/wbar - p;
  dq <- q*fit[2]/wbar - q;
  dr <- (1-p-q)*fit[3]/wbar - (1-p-q);
  # ensure the change in freq. adds up to 0
  con <- ( dp + dq + dr )/3
  dp <- ifelse( dp==0, 0, dp - con )
  dq <- ifelse( dq==0, 0, dq - con )
  dr <- ifelse( dr==0, 0, dr - con )
  
  test2 <- c(dp+dq+dr); names(test2) <- c("net_change")
  print( test2 )   

  c(dp,dq,dr);
}
"bary.tobary" <-
function( u , v ) {
  theheight <- 1;
  thewidth <- 1;
  uw <- u / thewidth;
  vw <- v / thewidth;
  y <- vw * 1.14142;
  x <- uw - y/2;
  c( x , y );
}
"bary.toscreen" <-
function(x,y) {
    ## converts barycentric coords to cartesian screen coords
    ## x is freq of strat in lower right
    ## y is freq of strat at top
    ## thus 1-x-y is freq of strat in lower left
    theheight <- 1;
    thewidth <- 1;
    c( (x + y/2)*thewidth , (y/1.14142)*thewidth );   
}
"bary.click" <-
function(thegame=bary.game.hdr, color=FALSE, arrows=FALSE, ...) {
  ## takes a click as input and runs a simulation from that point
  pt <- locator(n=1);
  barypt <- bary.tobary( pt$x, pt$y );
  bary.plotsim( barypt[1] , barypt[2] , arrow=arrows , withcol=color , thegame=thegame, ... );
}
