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

# RDF of olig, DMAEA N, HEA O with water
set sel [atomselect top "index [expr {$prot}] to [expr {$prot + $pol - 1}]"]
set dmaea [atomselect top "type 610"]
set hea [atomselect top "type 709"]
set wats [atomselect top "type 349"]

set oligw [measure gofr $sel $wats delta 0.1 rmax 15.0 first $start_frame last $end_frame usepbc true]
set outfile [open "analysis/rdf_olig_w.dat" w]
set r_values [lindex $oligw 0]
set rdf_values [lindex $oligw 1]
set int_values [lindex $oligw 2]
for {set i 0} {$i < [llength $r_values]} {incr i} {
    set r [lindex $r_values $i]
    set rdf [lindex $rdf_values $i]
    set int [lindex $int_values $i]
    puts $outfile [format "%s %s %s" $r $rdf $int]
}
close $outfile

set deaw [measure gofr $dmaea $wats delta 0.1 rmax 15.0 first $start_frame last $end_frame usepbc true]
set outfile [open "analysis/rdf_deaw_w.dat" w]
set r_values [lindex $deaw 0]
set rdf_values [lindex $deaw 1]
set int_values [lindex $deaw 2]
for {set i 0} {$i < [llength $r_values]} {incr i} {
    set r [lindex $r_values $i]
    set rdf [lindex $rdf_values $i]
    set int [lindex $int_values $i]
    puts $outfile [format "%s %s %s" $r $rdf $int]
}
close $outfile

set heaw [measure gofr $hea $wats delta 0.1 rmax 15.0 first $start_frame last $end_frame usepbc true]
set outfile [open "analysis/rdf_heaw_w.dat" w]
set r_values [lindex $heaw 0]
set rdf_values [lindex $heaw 1]
set int_values [lindex $heaw 2]
for {set i 0} {$i < [llength $r_values]} {incr i} {
    set r [lindex $r_values $i]
    set rdf [lindex $rdf_values $i]
    set int [lindex $int_values $i]
    puts $outfile [format "%s %s %s" $r $rdf $int]
}
close $outfile

set ww [measure gofr $wats $wats delta 0.1 rmax 10.0 first $start_frame last $end_frame step 100 usepbc true]
set outfile [open "analysis/rdf_w_w.dat" w]
set r_values [lindex $ww 0]
set rdf_values [lindex $ww 1]
set int_values [lindex $ww 2]
for {set i 0} {$i < [llength $r_values]} {incr i} {
    set r [lindex $r_values $i]
    set rdf [lindex $rdf_values $i]
    set int [lindex $int_values $i]
    puts $outfile [format "%s %s %s" $r $rdf $int]
}
close $outfile

selection clear
foreach var [info vars] {
    unset $var
}