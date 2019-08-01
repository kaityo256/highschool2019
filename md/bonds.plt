set term png
set out "bonds.png"
set size ratio -1
unset xtics
unset ytics
unset key
set style arrow 1 nohead

p "bonds.dat" w vec arrowstyle 1
