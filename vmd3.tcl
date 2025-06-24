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

# Get distance of COM of oligomer from COM of protein, CRO atom 734
set outfile [open "analysis/olig_com.dat" w]
animate goto $start_frame
for {set i 0} {$i < $num_frames} {incr i} {
    animate goto $i
    set atom2 [atomselect top "type 734" frame $i]
    set atom2_coords [lindex [$atom2 get {x y z}] 0]
    set oligsel [atomselect top "index [expr {$prot}] to [expr {$prot + $pol - 1}]" frame $i]
    set protsel [atomselect top "index 0 to [expr {$prot - 1}]" frame $i]
    set com_olig [measure center $oligsel weight mass]
    set com_prot [measure center $protsel weight mass]
    set dist_coms [vecdist $com_olig $com_prot]
    set dist_cro [vecdist $com_olig $atom2_coords]
    puts $outfile "$i $dist_coms $dist_cro"
}
close $outfile

# CRO - benzene ring C coords
set outfile [open "analysis/CRO_benzene_coords.dat" w]
animate goto $start_frame
for {set i 0} {$i < $num_frames} {incr i} {
    animate goto $i
    set atom0 [atomselect top "type 733" frame $i]
    set a0 [lindex [$atom0 get {x y z}] 0]
    set atom1 [atomselect top "type 732" frame $i]
    set a1 [lindex [$atom1 get {x y z}] 0]
    set a2 [lindex [$atom1 get {x y z}] 1]
    set atom3 [atomselect top "type 730" frame $i]
    set a3 [lindex [$atom3 get {x y z}] 0]
    set a4 [lindex [$atom3 get {x y z}] 1]
    set atom5 [atomselect top "type 731" frame $i]
    set a5 [lindex [$atom5 get {x y z}] 0]
    puts $outfile "$i $a0 $a1 $a2 $a3 $a4 $a5"
}
close $outfile

selection clear
foreach var [info vars] {
    unset $var
}