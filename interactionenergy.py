import re
import subprocess
import os
import csv
import tempfile   # Import tempfile to create temporary files


############################################
# Helper Function: Extract Atom Number
############################################
def extract_atom_number(atom_str):
    """
    Extracts the first sequence of digits found in the atom string and returns it as an integer.
    Raises a ValueError if no digits are found.
    """
    match = re.search(r'\d+', atom_str)
    if match:
        return int(match.group(0))
    else:
        raise ValueError(f"Could not extract atom number from {atom_str}")

############################################
# 1. Frame Generator for Tinker XYZ Trajectory
############################################

def tinker_xyz_frame_generator(filename, log_filename="temp_filenames.log"):
    print("Starting tinker_xyz_frame_generator...", flush=True)
    with open(filename, "r") as f, open(log_filename, "a") as log_file:
        while True:
            # Read the atom count line.
            atom_count_line = f.readline()
            if not atom_count_line:
                print("Reached end of file or no atom count line.", flush=True)
                break  # End of file
            
            atom_count_line = atom_count_line.strip()
            print(f"Read atom count line: {atom_count_line}", flush=True)
            
            if not atom_count_line.isdigit():
                print("Atom count line is not a digit. Breaking out.", flush=True)
                break  # Format error or end of valid frames
            
            n_atoms = int(atom_count_line)
            
            # Read the box size / global info line.
            box_line = f.readline()
            if not box_line:
                print("No box info line available.", flush=True)
                break
            
            print(f"Read box line: {box_line.strip()}", flush=True)
            
            # Collect the frame: atom count, box info, and then n_atoms lines of atom data.
            frame_lines = [atom_count_line + "\n", box_line]
            for i in range(n_atoms):
                atom_line = f.readline()
                if not atom_line:
                    print(f"Missing atom data for atom {i+1} of {n_atoms}.", flush=True)
                    break
                frame_lines.append(atom_line)
            
            # Write the current frame to a temporary file.
            temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".xyz", prefix="temp_frame_", delete=False)
            temp_file.writelines(frame_lines)
            temp_file_name = temp_file.name
            temp_file.close()
            
            # Log the temporary file name.
            log_file.write(temp_file_name + "\n")
            log_file.flush()  # Ensure it's written immediately
            
            print(f"Yielding temporary file: {temp_file_name}", flush=True)
            yield temp_file_name


############################################
# 2. Run Tinker Analyze on a Temporary Frame File
############################################

def run_tinker_analyze(temp_xyz_file, tinker_exe="/projects/welbornlab/Poltype2/TinkerEx/analyze", key_file="tinker.key"):
    """
    Runs Tinker analyze on the temporary XYZ file.
    """
    command = f"{tinker_exe} -k {key_file} {temp_xyz_file}"
    user_input = "D\n"  # Adjust this if needed (simulate pressing D then Enter)
    
    process = subprocess.Popen(command, shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)
    stdout, stderr = process.communicate(input=user_input)
    
    # Create a temporary filename for the analyze output.
    temp_analyze_file = temp_xyz_file.replace("temp_frame", "analyze_output") + ".txt"
    with open(temp_analyze_file, "w") as f:
        f.write("Output:\n")
        f.write(stdout)
        f.write("\nErrors:\n")
        f.write(stderr)
    
    return temp_analyze_file

############################################
# 3. Parse the Tinker Analyze Output
############################################
def parse_analyze_output(analyze_filename, groupA, groupB):
    """
    Reads the Tinker analyze output file and extracts energy sums for the 
    following interaction sections:
      - "Individual Atomic Multipole Interactions :" (data lines start with "Mpole")
      - "Individual Dipole Polarization Interactions :" (data lines start with "Polar")
      - "Individual van der Waals Interactions :" (data lines start with "VDW-Hal")
    
    For each section, only interactions where one atom is in groupA and the other in groupB 
    are considered.
    
    Returns a tuple: (multipole_energy_sum, polar_energy_sum, vdw_energy_sum, total_energy)
    """


    # Define header patterns.
    multipole_header_pattern = re.compile(r"^Individual\s+Atomic\s+Multipole\s+Interactions\s*:$")
    polar_header_pattern   = re.compile(r"^Individual\s+Dipole\s+Polarization\s+Interactions\s*:$")
    vdw_header_pattern     = re.compile(r"^Individual\s+van\s+der\s+Waals\s+Interactions\s*:$")
    
    multipole_data = []
    polar_data = []
    vdw_data = []
    
    in_multipole_section = False
    in_polar_section = False
    in_vdw_section = False
    
    with open(analyze_filename, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        stripped = line.strip()
        # Detect section headers.
        if multipole_header_pattern.search(stripped):
            in_multipole_section = True
            in_polar_section = False
            in_vdw_section = False
            continue
        if polar_header_pattern.search(stripped):
            in_multipole_section = False
            in_polar_section = True
            in_vdw_section = False
            continue
        if vdw_header_pattern.search(stripped):
            in_multipole_section = False
            in_polar_section = False
            in_vdw_section = True
            continue
        
        if not stripped:
            continue
        
        # Process multipole data lines.
        if in_multipole_section:
            columns = stripped.split()
            if len(columns) >= 5 and columns[0] == "Mpole":
                # Extract atom identifiers from columns[1] and columns[2].
                atomA = columns[1]
                atomB = columns[2]
                a_num = extract_atom_number(atomA)
                b_num = extract_atom_number(atomB)
                # Only accept if one atom is in groupA and the other in groupB.
                if (a_num in groupA and b_num in groupB) or (a_num in groupB and b_num in groupA):
                    try:
                        energy = float(columns[4])
                        multipole_data.append(energy)
                    except:
                        pass
                        
        # Process dipole polarization data lines.
        if in_polar_section:
            columns = stripped.split()
            if len(columns) >= 5 and columns[0] == "Polar":
                atomA = columns[1]
                atomB = columns[2]
                a_num = extract_atom_number(atomA)
                b_num = extract_atom_number(atomB)
                if (a_num in groupA and b_num in groupB) or (a_num in groupB and b_num in groupA):
                    try:
                        energy = float(columns[4])
                        polar_data.append(energy)
                    except:
                        pass
                        
        # Process van der Waals data lines.
        if in_vdw_section:
            columns = stripped.split()
            if len(columns) >= 6 and columns[0] == "VDW-Hal":
                atomA = columns[1]
                atomB = columns[2]
                a_num = extract_atom_number(atomA)
                b_num = extract_atom_number(atomB)
                if (a_num in groupA and b_num in groupB) or (a_num in groupB and b_num in groupA):
                    try:
                        energy = float(columns[5])
                        vdw_data.append(energy)
                    except:
                        pass
    
    multipole_energy_sum = sum(multipole_data)
    polar_energy_sum = sum(polar_data)
    vdw_energy_sum = sum(vdw_data)
    total_energy = multipole_energy_sum + polar_energy_sum + vdw_energy_sum
    return multipole_energy_sum, polar_energy_sum, vdw_energy_sum, total_energy


############################################
# 4. Main Script: Process Each Frame and Write CSV
############################################

trajectory_file = "prot_lig.arc"  # Your large trajectory file
csv_filename = "energy_summary_multiframe.csv"


#Define the atom group 
groupA = set(range(1, 3909))
groupB = set(range(3910, 4334))

with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["Frame", "Multipole", "Polar", "VDW", "Total"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    frame_index = 0
    for temp_xyz_file in tinker_xyz_frame_generator(trajectory_file):
        frame_index += 1
        print(f"Processing frame {frame_index} ...")
        
        # Run Tinker analyze on the temporary file.
        analyze_filename = run_tinker_analyze(temp_xyz_file)
        
        # Parse the analyze output to get energy sums, passing groupA and groupB.
        multipole_energy, polar_energy, vdw_energy, total_energy = parse_analyze_output(analyze_filename, groupA, groupB)
        
        # Write a summary row for this frame.
        writer.writerow({
            "Frame": frame_index,
            "Multipole": f"{multipole_energy:.4f}",
            "Polar": f"{polar_energy:.4f}",
            "VDW": f"{vdw_energy:.4f}",
            "Total": f"{total_energy:.4f}"
        })
        
        # Clean up temporary files.
        os.remove(temp_xyz_file)
        os.remove(analyze_filename)

print(f"Energy summary saved to {csv_filename}")

