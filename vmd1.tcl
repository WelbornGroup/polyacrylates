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
file mkdir analysis

# BACKBONE RMSD FOR GFP
set filename [format "analysis/bb_rmsd.dat"]
set outfile [open $filename w]
set reference [atomselect top "protein and backbone" frame 0]
for {set i 0} {$i < $num_frames} {incr i} {
    set compare [atomselect top "protein and backbone" frame $i]
    set trans_mat [measure fit $compare $reference]
    $compare move $trans_mat
    set rmsd [measure rmsd $compare $reference]
    puts $outfile "$i $rmsd"
}
close $outfile

# E2E, Rg, SASA, nSASA for oligomer and Rg for protein
set outfile [open "analysis/olig_vmd.dat" w]
animate goto $start_frame
for {set i 0} {$i < $num_frames} {incr i} {
    animate goto $i
    set atom1 [atomselect top "type 900" frame $i]
    set atom2 [atomselect top "type 950" frame $i]
    set a1i [$atom1 get index]
    set a2i [$atom2 get index]
    set a1 [lindex $a1i 0]
    set a2 [lindex $a2i 0]
    set e2e [measure bond [list $a1 $a2] frame $i]

    set sel [atomselect top "index [expr {$prot}] to [expr {$prot + $pol - 1}]" frame $i]
    set sasa_value [measure sasa 1.4 $sel]
    set rg_value [measure rgyr $sel]
    set sasa_norm [expr {$sasa_value / $pol}]

    set protsel [atomselect top "index 0 to [expr {$prot - 1}]" frame $i]
    set rg_prot [measure rgyr $protsel]
    puts $outfile "$i $e2e $rg_value $sasa_value $sasa_norm $rg_prot"
}
close $outfile

selection clear
foreach var [info vars] {
    unset $var
}