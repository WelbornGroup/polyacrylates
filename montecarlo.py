######################################################
### MONTE CARLO FOR SEQUENCE HUNTING V4
######################################################
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gamma


def get_polymer_length():
    """Sample polymer length from Schulz-Zimm (Gamma) distribution."""
    length = int(np.random.gamma(shape, scale))
    return max(length, 1)  # Ensure at least 1 monomer between caps

def choose_next_monomer(prev_monomer):
    """Choose the next monomer based on reactivity probabilities."""
    choices, probs = zip(*reactivity[prev_monomer].items())
    probs = np.array(probs) / np.sum(probs)  # Normalize
    return np.random.choice(choices, p=probs)

def build_polymer():
    """Monte Carlo polymerization."""
    polymer = ["Sulf"]
    polymer_length = get_polymer_length()  # Get length from gamma distribution
    
    # Generate polymer chain
    for _ in range(polymer_length):
        next_monomer = choose_next_monomer(polymer[-1])
        polymer.append(next_monomer)

    polymer.append("Carb")  # Add end cap
    return polymer, polymer_length

def calculate_composition(polymer):
    """Calculate percentage composition of each monomer type in a polymer."""
    total_monomers = len(polymer) - 2  # Exclude start and end caps
    counts = {m: polymer.count(m) / total_monomers * 100 for m in monomers}
    return [counts.get(m, 0) for m in monomers]  # Return [D, H, I, A] percentages

# def match_composition(simulated_comp, target_comp, tolerance): # Consistent Absolute Tolerance
#     """Check if simulated composition is within x% of the target composition."""
#     return all(abs(simulated_comp[i] - target_comp[i]) <= tolerance for i in range(4))

def match_composition(simulated_comp, target_comp, distance_threshold): # Distance-Based Metrics
    """Check if Euclidean distance between compositions is below threshold"""
    distance = np.sqrt(sum((simulated_comp[i] - target_comp[i])**2 for i in range(len(simulated_comp))))
    return distance <= distance_threshold

def check_polymer_composition(target_composition, tolerance, num_simulations):
    """Generate polymers and determine the fraction matching the given composition within tolerance."""
    matching_count = 0

    for _ in range(num_simulations):
        polymer, _ = build_polymer()
        simulated_composition = calculate_composition(polymer)
        if match_composition(simulated_composition, target_composition, tolerance):
            matching_count += 1

    percentage_matching = (matching_count / num_simulations) * 100
    return percentage_matching

# Run Monte Carlo simulation for polymer lengths
# np.random.seed(42)  # Reproducibility
# random.seed(42)

# Define monomers
monomers = ["D", "H", "I", "A"]

# Experimental reactivity matrix
reactivity_exp = {
    "Sulf": {"D": 1, "H": 1, "I": 1, "A": 1}, # initial same
    "D": {"D": 1, "H": 1/0.49, "I": 1/0.56, "A": 1/0.62},
    "H": {"D": 1/1.20, "H": 1, "I": 1/1.24, "A": 1/1.06},
    "I": {"D": 1/1.40, "H": 1/1.01, "I": 1, "A": 1/1.16},
    "A": {"D": 1/2.37, "H": 1/1.05, "I": 1/1.10, "A": 1},
}
# Normalize
reactivity = {k: {k2: v2 / sum(d.values()) for k2, v2 in d.items()} for k, d in reactivity_exp.items()}

# Polymerization properties
XX = int(1e8)
Mn = 23  # Mean polymer length (excluding caps)
D = 1.2  # Dispersity
best_composition = [22.3, 31.5, 20.7, 25.5]  # % composition of D, H, I, A
worst_composition = [10.9, 30.1, 36.8, 22.1]  # % composition of D, H, I, A
tolerance = 0.05  # Allow plus-minus 5% deviation
num_simulations = XX  # Number of polymers to generate

# Compute gamma distribution shape and scale
shape = 1 / (D - 1)  # Schulz-Zimm parameter
scale = Mn / shape  # Scale for gamma distribution

# polymer_lengths = []
# with open("polymer_lengths_1e7_3.txt", "w") as file:
#     for i in range(num_simulations):
#         pol, length = build_polymer()
#         comp = calculate_composition(pol)
#         file.write(f"{length}\t {comp}\n")  # Each length on a new line

# # Print statistics
# print(f"Simulated Mean Length: {np.mean(polymer_lengths):.2f}")
# print(f"Simulated Dispersity: {np.var(polymer_lengths) / np.mean(polymer_lengths) ** 2 + 1:.2f}")

# # Check polymer composition match
# matching_percentage = check_polymer_composition(best_composition, tolerance,XX)
# print(f"Percentage of polymers matching best composition within ±{tolerance}%: {matching_percentage:.2f}%")
# matching_percentage = check_polymer_composition(worst_composition, tolerance,XX)
# print(f"Percentage of polymers matching worst composition within ±{tolerance}%: {matching_percentage:.2f}%")

# # Plot the distribution of polymer lengths
# sns.set_style("whitegrid")
# plt.figure(figsize=(8, 5))
# fsize = 35
# sns.histplot(polymer_lengths, bins=30, kde=True, color="blue", label=f"Simulated ({np.mean(polymer_lengths):.2f},{np.var(polymer_lengths) / np.mean(polymer_lengths) ** 2 + 1:.2f})")
# x = np.linspace(min(polymer_lengths), max(polymer_lengths), 100)
# gamma_pdf = (x ** (shape - 1)) * (np.exp(-x / scale) / (scale ** shape * np.math.gamma(shape))) # Overlay theoretical gamma distribution
# gamma_pdf *= len(polymer_lengths) * np.diff(plt.xlim())[0] / 30  # Scale for overlay
# plt.plot(x, gamma_pdf, 'r-', label="Theoretical (Gamma)")
# plt.xlabel("Polymer Length (Exc Caps)",fontsize=fsize)
# plt.ylabel("Frequency",fontsize=fsize)
# plt.xticks(fontsize=fsize)
# plt.yticks(fontsize=fsize)
# # plt.title("Distribution of Polymer Lengths")
# plt.legend(fontsize=fsize)
# plt.show()

polymer_lengths = []
total_polymers = 0
with open("bigone/polymer_lengths_1e8_1.txt", "r") as file:
    for line in file:
        parts = line.strip().split("\t")  # Assuming tab-separated values
        length = int(parts[0])  # Extract polymer length
        composition = np.array(eval(parts[1]))  # Convert string list to numpy array
        polymer_lengths.append(length)
        total_polymers += 1
        if (total_polymers % 1e6 == 0):
            print(f"{total_polymers//1e6} M")

# NEW PLOT
hist_color = "blue"
gamma_color = "red"
gamma_linewidth = 3
hist_alpha = 0.7  # Transparency for histogram
sns.set_style("whitegrid")
plt.figure(figsize=(8, 5))
fsize = 35
min_bin = int(np.floor(min(polymer_lengths)))
max_bin = int(np.ceil(max(polymer_lengths)))
bins = np.arange(min_bin, max_bin + 1)
sns.histplot(polymer_lengths, bins=bins, kde=False, stat="probability", color=hist_color, label=f"Simulated ({np.mean(polymer_lengths):.2f}, {np.var(polymer_lengths) / np.mean(polymer_lengths) ** 2 + 1:.2f})", alpha=hist_alpha)
x = np.linspace(min(polymer_lengths), max(polymer_lengths), 500)
gamma_pdf = (x ** (shape - 1)) * (np.exp(-x / scale) / (scale ** shape * np.math.gamma(shape)))/XX
gamma_pdf *= len(polymer_lengths) * np.diff(plt.xlim())[0] / len(bins)  # Scale for overlay
plt.plot(x, gamma_pdf, color=gamma_color, linewidth=gamma_linewidth, label="Theoretical (Gamma)")
plt.xlabel("Oligomer Length (Exc Caps)", fontsize=fsize)
plt.ylabel("Frequency", fontsize=fsize)
plt.xlim(0,60)
plt.xticks(fontsize=fsize)
plt.yticks(fontsize=fsize)
plt.legend(fontsize=fsize)
plt.show()



# # Function to check if a composition is within ±5% of a target composition
# def is_within_tolerance(comp, target, tolerance):
    # return np.all(np.abs((comp - target) / target) <= tolerance)

# polymer_lengths = []
# match_count_1 = 0
# match_count_2 = 0
# total_polymers = 0
# maxpols = 5*1e6

# with open("polymer_lengths_1e6_2.txt", "r") as file:
#     for line in file:
#         parts = line.strip().split("\t")  # Assuming tab-separated values
#         length = int(parts[0])  # Extract polymer length
#         composition = np.array(eval(parts[1]))  # Convert string list to numpy array

#         polymer_lengths.append(length)
#         total_polymers += 1

#         if (total_polymers <= maxpols):

#             # Check if composition matches comp1 or comp2 within ±5%
#             if match_composition(composition, best_composition,tolerance):
#                 match_count_1 += 1
#             if match_composition(composition, worst_composition,tolerance):
#                 match_count_2 += 1
            
#             #     print(f"{polymer_lengths[-1]} {match_count_1} {match_count_2}" )
#             if (total_polymers % 1e6 == 0):
#                 print(f"{total_polymers//1e6} M")
        
#         if (total_polymers == maxpols):
#             break

# # Compute percentage matches
# percent_match_1 = (match_count_1 / total_polymers) * 100
# percent_match_2 = (match_count_2 / total_polymers) * 100

# simulated_mean = np.mean(polymer_lengths)
# simulated_dispersity = np.var(polymer_lengths) / simulated_mean**2 + 1

# # Print results
# print(f"Total polymers processed: {total_polymers}")
# print(f"Simulated Mean: {simulated_mean:.2f}")
# print(f"Simulated Dispersity: {simulated_dispersity:.2f}")
# print(f"Percentage matching best: {percent_match_1:.2f}%")
# print(f"Percentage matching worst: {percent_match_2:.2f}%")

########################################################
# # Fit a gamma distribution to polymer lengths
# shape, loc, scale = gamma.fit(polymer_lengths, floc=0)
# # Plot histogram and gamma distribution
# sns.set_style("whitegrid")
# plt.figure(figsize=(8, 5))
# sns.histplot(polymer_lengths, bins=100, kde=True, color="blue", 
#              label=f"Simulated ({np.mean(polymer_lengths):.2f},"
#                    f"{np.var(polymer_lengths) / np.mean(polymer_lengths) ** 2 + 1:.2f})")

# x = np.linspace(min(polymer_lengths), max(polymer_lengths), 100)
# gamma_pdf = gamma.pdf(x, shape, loc=loc, scale=scale)  # Fitted gamma distribution
# gamma_pdf *= len(polymer_lengths) * np.diff(plt.xlim())[0] / 30  # Scale to match histogram
# plt.plot(x, gamma_pdf, 'r-', label="Theoretical (Gamma)")
# plt.xlabel("Polymer Length (Exc Caps)", fontsize=25)
# plt.ylabel("Frequency", fontsize=25)
# plt.xticks(fontsize=25)
# plt.yticks(fontsize=25)
# plt.title("Distribution of Polymer Lengths")
# plt.legend(fontsize=25)
# plt.show()
# ########################################################
# # Fit a gamma distribution to polymer lengths
# shape, loc, scale = gamma.fit(polymer_lengths, floc=0)
# # Plot histogram and gamma distribution
# plt.figure(figsize=(10, 6))
# # Plot histogram
# bin_width = 1  # Set desired bin width
# bins = np.arange(min(polymer_lengths), max(polymer_lengths) + bin_width, bin_width)
# counts, bins, _ = plt.hist(polymer_lengths, bins=bins, density=True, color="blue", alpha=0.5, label="Simulated Data")
# # Compute and plot gamma PDF
# x = np.linspace(min(polymer_lengths), max(polymer_lengths), 100)
# gamma_pdf = gamma.pdf(x, shape, loc=loc, scale=scale)
# plt.plot(x, gamma_pdf, 'r-', linewidth=2, label="Theoretical (Gamma)")
# # Labels and title
# plt.xlabel("Oligomer Length (Exc Caps)", fontsize=35)
# plt.ylabel("Frequency", fontsize=35)
# plt.xticks(fontsize=35)
# plt.yticks(fontsize=35)
# # plt.title("Distribution of Polymer Lengths", fontsize=25)
# plt.legend(fontsize=35)
# plt.show()
# ########################################################

# from scipy.ndimage import gaussian_filter1d
# # Compute histogram data
# counts, bin_edges = np.histogram(data, bins=100)
# # Apply Gaussian filter for smoothing
# smoothed_counts = gaussian_filter1d(counts, sigma=2)
# # Plot smoothed histogram line
# bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
# plt.plot(bin_centers, smoothed_counts, color='blue')