set term pngcairo transparent size 1920, 400
set out "fig.png"
set style arrow 1 nohead
unset border
unset key
unset xtics
unset ytics
p "positions.dat" pt 6,"bonds.dat" w vec arrowstyle 1
