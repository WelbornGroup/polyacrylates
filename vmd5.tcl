set prot 3909
set pol 425
set num_frames 10371
# 297 for best_A,best_B,best_C 
# 313 for worst_A,worst_B
# 82 for pe_A, pe_B
# 425 for best23_A,best23_B
# 400 for worst22_A
# 164 for peg_A,peg_B

set start_frame 0
set end_frame [expr {$num_frames - 1}]

# Find coordinates of COM of oligomer and print it to file
set outfile [open "analysis/oligomer_com_coords.dat" w]
for {set i 0} {$i < $num_frames} {incr i} {
    animate goto $start_frame
    set oligsel [atomselect top "index [expr {$prot}] to [expr {$prot + $pol - 1}]" frame $i]
    set com_olig [measure center $oligsel weight mass]
    puts $outfile "$i $com_olig"
}
close $outfile

selection clear
foreach var [info vars] {
    unset $var
}