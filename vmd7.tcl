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

# CHROMOPHORE RMSD
set filename [format "analysis/cro_rmsd.dat"]
set outfile [open $filename w]
set reference [atomselect top "index 1849 to 1883" frame 0]
for {set i 0} {$i < $num_frames} {incr i} {
    set compare [atomselect top "index 1849 to 1883" frame $i]
    set trans_mat [measure fit $compare $reference]
    $compare move $trans_mat
    set rmsd [measure rmsd $compare $reference]
    puts $outfile "$i $rmsd"
}
close $outfile

selection clear
foreach var [info vars] {
    unset $var
}