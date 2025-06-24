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

# CRO - imidazole ring C coords
set outfile [open "analysis/CRO_imidazole_coords.dat" w]
animate goto $start_frame
for {set i 0} {$i < $num_frames} {incr i} {
    animate goto $i
    set atom0 [atomselect top "type 751" frame $i]
    set a0 [lindex [$atom0 get {x y z}] 0]
    set atom1 [atomselect top "type 752" frame $i]
    set a1 [lindex [$atom1 get {x y z}] 0]
    set atom2 [atomselect top "type 756" frame $i]
    set a2 [lindex [$atom2 get {x y z}] 0]
    set atom3 [atomselect top "type 750" frame $i]
    set a3 [lindex [$atom3 get {x y z}] 0]
    set atom4 [atomselect top "type 757" frame $i]
    set a4 [lindex [$atom4 get {x y z}] 0]
    puts $outfile "$i $a0 $a1 $a2 $a3 $a4"
}
close $outfile

selection clear
foreach var [info vars] {
    unset $var
}