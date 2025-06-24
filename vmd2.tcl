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

# CRO trans-cis angle
set outfile [open "analysis/CRO_angles.dat" w]
animate goto $start_frame
for {set i 0} {$i < $num_frames} {incr i} {
    animate goto $i
    set atom0 [atomselect top "type 730" frame $i]
    set a0i [$atom0 get index]
    set a0 [lindex $a0i 0]
    set atom1 [atomselect top "type 731" frame $i]
    set a1i [$atom1 get index]
    set a1 [lindex $a1i 0]
    set atom2 [atomselect top "type 734" frame $i]
    set a2i [$atom2 get index]
    set a2 [lindex $a2i 0]
    set atom3 [atomselect top "type 751" frame $i]
    set a3i [$atom3 get index]
    set a3 [lindex $a3i 0]
    set atom4 [atomselect top "type 757" frame $i]
    set a4i [$atom4 get index]
    set a4 [lindex $a4i 0]

    set cistrans [measure angle [list $a1 $a2 $a3] frame $i]
    set dihed_single [measure dihed [list $a0 $a1 $a2 $a3] frame $i]
    set dihed_double [measure dihed [list $a1 $a2 $a3 $a4] frame $i]
    
    puts $outfile "$i $cistrans $dihed_single $dihed_double"
}
close $outfile

selection clear
foreach var [info vars] {
    unset $var
}