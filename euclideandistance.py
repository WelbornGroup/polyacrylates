# import numpy as np

# def euclidean_distance(simulated_comp, target_comp):
#     """Calculate Euclidean distance between two compositions."""
#     return np.sqrt(sum((simulated_comp[i] - target_comp[i])**2 for i in range(len(simulated_comp))))

# # Function to check if a composition is within a Euclidean distance threshold
# def match_composition_euclidean(comp, target, threshold):
#     """Check if Euclidean distance between compositions is below threshold."""
#     return euclidean_distance(comp, target) <= threshold

# # Main analysis loop reading from file
# polymer_lengths = []
# match_count_1 = 0
# match_count_2 = 0
# total_polymers = 0
# maxpols = 5*1e6
# best_composition = [22.3, 31.5, 20.7, 25.5]  # % composition of D, H, I, A
# worst_composition = [10.9, 30.1, 36.8, 22.1]  # % composition of D, H, I, A

# # Try different thresholds and track results
# thresholds = [1,2,5,8,10]
# matches_by_threshold_best = {t: 0 for t in thresholds}
# matches_by_threshold_worst = {t: 0 for t in thresholds}

# with open("polymer_lengths_1e6_1.txt", "r") as file:
#     for line in file:
#         parts = line.strip().split("\t")  # Assuming tab-separated values
#         length = int(parts[0])  # Extract polymer length
#         composition = np.array(eval(parts[1]))  # Convert string list to numpy array

#         polymer_lengths.append(length)
#         total_polymers += 1

#         if total_polymers <= maxpols:
#             # Check composition against best_composition for each threshold
#             for threshold in thresholds:
#                 if match_composition_euclidean(composition, np.array(best_composition), threshold):
#                     matches_by_threshold_best[threshold] += 1
#                 if match_composition_euclidean(composition, np.array(worst_composition), threshold):
#                     matches_by_threshold_worst[threshold] += 1
            
#             if total_polymers % 1e6 == 0:
#                 print(f"Processed {total_polymers//1e6} million polymers")
        
#         if total_polymers == maxpols:
#             break

# # Calculate percentage matches for each threshold
# print("\nResults for best composition:")
# print("-----------------------------")
# for threshold in thresholds:
#     percent_match = (matches_by_threshold_best[threshold] / total_polymers) * 100
#     print(f"Threshold {threshold}: {percent_match:.4f}% match")

# print("\nResults for worst composition:")
# print("------------------------------")
# for threshold in thresholds:
#     percent_match = (matches_by_threshold_worst[threshold] / total_polymers) * 100
#     print(f"Threshold {threshold}: {percent_match:.4f}% match")

# # Print final statistics
# print(f"\nTotal polymers processed: {total_polymers}")
# print(f"Simulated Mean Length: {np.mean(polymer_lengths):.2f}")
# print(f"Simulated Dispersity: {np.var(polymer_lengths) / np.mean(polymer_lengths)**2 + 1:.2f}")

# # Optionally, visualize the distribution of distances
# import matplotlib.pyplot as plt

# # Calculate distances for all polymers (limited to first 100,000 for performance)
# best_distances = []
# worst_distances = []
# sample_size = min(100000, len(polymer_lengths))

# # Reopen file to get compositions again
# with open("polymer_lengths_1e6_2.txt", "r") as file:
#     for i, line in enumerate(file):
#         if i >= sample_size:
#             break
#         parts = line.strip().split("\t")
#         composition = np.array(eval(parts[1]))
#         best_distances.append(euclidean_distance(composition, np.array(best_composition)))
#         worst_distances.append(euclidean_distance(composition, np.array(worst_composition)))

# # Plot histograms of distances
# plt.figure(figsize=(12, 6))

# plt.subplot(1, 2, 1)
# plt.hist(best_distances, bins=50, alpha=0.7)
# plt.title("Distance Distribution - Best Composition")
# plt.xlabel("Euclidean Distance")
# plt.ylabel("Frequency")
# for threshold in thresholds:
#     plt.axvline(x=threshold, color='r', linestyle='--', alpha=0.5)

# plt.subplot(1, 2, 2)
# plt.hist(worst_distances, bins=50, alpha=0.7)
# plt.title("Distance Distribution - Worst Composition")
# plt.xlabel("Euclidean Distance")
# plt.ylabel("Frequency")
# for threshold in thresholds:
#     plt.axvline(x=threshold, color='r', linestyle='--', alpha=0.5)

# plt.tight_layout()
# plt.show()




################################################################################################################

import numpy as np
import matplotlib.pyplot as plt

def euclidean_distance(simulated_comp, target_comp):
    """Calculate Euclidean distance between two compositions."""
    return np.sqrt(sum((simulated_comp[i] - target_comp[i])**2 for i in range(len(simulated_comp))))

def composition_similarity_percentage(distance, dimensions=4):
    """
    Convert Euclidean distance to a similarity percentage.
    
    For compositions, the maximum possible distance would be if all components
    were completely different. For percentages that sum to 100%, 
    the theoretical maximum distance is sqrt(2*100²) ≈ 141.42
    
    However, this doesn't account for the actual range of distances in your data.
    We'll use a more practical approach based on your data distribution.
    """
    # Maximum theoretical distance for percentage compositions in n dimensions
    # where each dimension can range from 0-100%
    max_theoretical_distance = np.sqrt(2 * 100**2)  # ≈ 141.42 for 4D
    
    # Convert to similarity percentage (100% = identical, 0% = maximum difference)
    similarity = max(0, 100 * (1 - distance / max_theoretical_distance))
    
    return similarity

# Function to check if a composition is within a Euclidean distance threshold
def match_composition_euclidean(comp, target, threshold):
    """Check if Euclidean distance between compositions is below threshold."""
    return euclidean_distance(comp, target) <= threshold

# Main analysis loop reading from file
polymer_lengths = []
total_polymers = 0
maxpols = 1*1e8
fname = "bigone/polymer_lengths_1e8_3.txt"
# fname = "polymer_lengths_1e6_1.txt"

# Try different thresholds and track results
thresholds = [7.05]
# thresholds =[1.1]
matches_by_threshold_best = {t: 0 for t in thresholds}
matches_by_threshold_worst = {t: 0 for t in thresholds}

# Define the compositions
best_composition = [22.3, 31.5, 20.7, 25.5]  # % composition of D, H, I, A
worst_composition = [10.9, 30.1, 36.8, 22.1]  # % composition of D, H, I, A

with open(fname, "r") as file:
    for line in file:
        parts = line.strip().split("\t")  # Assuming tab-separated values
        length = int(parts[0])  # Extract polymer length
        composition = np.array(eval(parts[1]))  # Convert string list to numpy array

        polymer_lengths.append(length)
        total_polymers += 1

        if total_polymers <= maxpols:
            # Check composition against best_composition for each threshold
            for threshold in thresholds:
                if match_composition_euclidean(composition, np.array(best_composition), threshold):
                    matches_by_threshold_best[threshold] += 1
                if match_composition_euclidean(composition, np.array(worst_composition), threshold):
                    matches_by_threshold_worst[threshold] += 1
            
            if total_polymers % 1e6 == 0:
                print(f"Processed {total_polymers//1e6} million polymers")
        
        if total_polymers == maxpols:
            break

# Calculate and display percentage matches and similarity percentages for each threshold
print("\nResults for best composition:")
print("-----------------------------")
print("Threshold | Match % | Min Similarity %")
print("---------------------------------")
for threshold in thresholds:
    percent_match = (matches_by_threshold_best[threshold] / total_polymers) * 100
    similarity = composition_similarity_percentage(threshold)
    print(f"{threshold:9} | {percent_match:.4f}% | {similarity:.2f}%")

print("\nResults for worst composition:")
print("------------------------------")
print("Threshold | Match % | Min Similarity %")
print("---------------------------------")
for threshold in thresholds:
    percent_match = (matches_by_threshold_worst[threshold] / total_polymers) * 100
    similarity = composition_similarity_percentage(threshold)
    print(f"{threshold:9} | {percent_match:.4f}% | {similarity:.2f}%")

# Print final statistics
print(f"\nTotal polymers processed: {total_polymers}")
print(f"Simulated Mean Length: {np.mean(polymer_lengths):.2f}")
print(f"Simulated Dispersity: {np.var(polymer_lengths) / np.mean(polymer_lengths)**2 + 1:.2f}")

# Collect data for visualization
print("\nCalculating distance distributions for visualization...")
best_distances = []
worst_distances = []
sample_size = min(1e6, len(polymer_lengths))

# Reopen file to get compositions again
with open(fname, "r") as file:
    for i, line in enumerate(file):
        if i >= sample_size:
            break
        parts = line.strip().split("\t")
        composition = np.array(eval(parts[1]))
        best_distances.append(euclidean_distance(composition, np.array(best_composition)))
        worst_distances.append(euclidean_distance(composition, np.array(worst_composition)))

# Calculate average and maximum distances
avg_best_distance = np.mean(best_distances)
avg_worst_distance = np.mean(worst_distances)
max_best_distance = np.max(best_distances)
max_worst_distance = np.max(worst_distances)

print(f"\nBest composition:")
print(f"  - Average distance: {avg_best_distance:.2f} (similarity: {composition_similarity_percentage(avg_best_distance):.2f}%)")
print(f"  - Maximum distance: {max_best_distance:.2f} (similarity: {composition_similarity_percentage(max_best_distance):.2f}%)")

print(f"\nWorst composition:")
print(f"  - Average distance: {avg_worst_distance:.2f} (similarity: {composition_similarity_percentage(avg_worst_distance):.2f}%)")
print(f"  - Maximum distance: {max_worst_distance:.2f} (similarity: {composition_similarity_percentage(max_worst_distance):.2f}%)")

# # Plot histograms of distances with similarity percentages
# fsize = 35  # Define fontsize for tick labels

# # First plot (Best composition)
# plt.figure(figsize=(10, 7))
# ax = plt.gca()
# for spine in ax.spines.values():
#     spine.set_linewidth(3)  # Sets a thicker border
# ax.tick_params(axis='both', which='major', labelsize=fsize)

# plt.hist(best_distances, bins=50, alpha=0.7)
# plt.title("Distance Distribution - Best Composition", fontsize=fsize+2)
# plt.xlabel("Euclidean Distance (lower = more similar)", fontsize=fsize)
# plt.ylabel("Frequency", fontsize=fsize)

# # Add a secondary x-axis for similarity percentage
# ax2 = ax.twiny()
# x_lim = ax.get_xlim()
# similarity_ticks = np.linspace(x_lim[0], x_lim[1], 6)
# similarity_labels = [f"{composition_similarity_percentage(d):.1f}%" for d in similarity_ticks]
# # ax2.set_xlim(x_lim)
# ax2.set_xlim(0,60)
# ax2.set_xticks(similarity_ticks)
# ax2.set_xticklabels(similarity_labels)
# ax2.set_xlabel("Composition Similarity", fontsize=fsize)
# ax2.tick_params(axis='x', which='major', labelsize=fsize)

# # Add threshold lines
# for threshold in thresholds:
#     similarity = composition_similarity_percentage(threshold)
#     plt.axvline(x=threshold, color='r', linestyle='--', alpha=0.5)
#     plt.text(threshold+0.5, plt.ylim()[1]*0.95, f"{similarity:.1f}%", 
#              rotation=90, verticalalignment='top', fontsize=fsize)

# plt.tight_layout()
# plt.show()

# # Second plot (Worst composition)
# plt.figure(figsize=(10, 7))
# ax = plt.gca()
# for spine in ax.spines.values():
#     spine.set_linewidth(3)  # Sets a thicker border
# ax.tick_params(axis='both', which='major', labelsize=fsize)

# plt.hist(worst_distances, bins=50, alpha=0.7)
# plt.title("Distance Distribution - Worst Composition", fontsize=fsize+2)
# plt.xlabel("Euclidean Distance (lower = more similar)", fontsize=fsize)
# plt.ylabel("Frequency", fontsize=fsize)

# # Add a secondary x-axis for similarity percentage
# ax2 = ax.twiny()
# x_lim = ax.get_xlim()
# similarity_ticks = np.linspace(x_lim[0], x_lim[1], 6)
# similarity_labels = [f"{composition_similarity_percentage(d):.1f}%" for d in similarity_ticks]
# # ax2.set_xlim(x_lim)
# ax2.set_xlim(0,60)
# ax2.set_xticks(similarity_ticks)
# ax2.set_xticklabels(similarity_labels)
# ax2.set_xlabel("Composition Similarity", fontsize=fsize)
# ax2.tick_params(axis='x', which='major', labelsize=fsize)

# # Add threshold lines
# for threshold in thresholds:
#     similarity = composition_similarity_percentage(threshold)
#     plt.axvline(x=threshold, color='r', linestyle='--', alpha=0.5)
#     plt.text(threshold+0.5, plt.ylim()[1]*0.95, f"{similarity:.1f}%", 
#              rotation=90, verticalalignment='top', fontsize=fsize)

# plt.tight_layout()
# plt.show()

###################################################################
# # Plot histograms of distances with similarity percentages
# fsize = 35  # Define fontsize for tick labels

# # First plot (Best composition)
# plt.figure(figsize=(10, 7))
# ax = plt.gca()
# for spine in ax.spines.values():
#     spine.set_linewidth(3)  # Sets a thicker border
# ax.tick_params(axis='both', which='major', labelsize=fsize)
# ax.set_xlim(0, 60)

# plt.hist(best_distances, bins=50, alpha=0.7, density=True)
# plt.title("Distance Distribution - Best Composition", fontsize=fsize+2, fontname='Arial')
# plt.xlabel("Euclidean Distance (lower = more similar)", fontsize=fsize, fontname='Arial')
# plt.ylabel("Frequency", fontsize=fsize, fontname='Arial')

# # Add a secondary x-axis for similarity percentage
# ax2 = ax.twiny()
# similarity_ticks = np.linspace(0, 60, 6)
# similarity_labels = [f"{composition_similarity_percentage(d):.1f}%" for d in similarity_ticks]
# ax2.set_xlim(0, 60)
# ax2.set_xticks(similarity_ticks)
# ax2.set_xticklabels(similarity_labels, fontsize=fsize, fontname='Arial')
# ax2.set_xlabel("Composition Similarity", fontsize=fsize, fontname='Arial')
# ax2.tick_params(axis='x', which='major', labelsize=fsize)

# # Add threshold lines
# for threshold in thresholds:
#     similarity = composition_similarity_percentage(threshold)
#     plt.axvline(x=threshold, color='r', linestyle='--', linewidth=5)
#     plt.text(threshold + 0.5, plt.ylim()[1] * 0.95, f"{similarity:.1f}%", 
#              rotation=90, verticalalignment='top', fontsize=fsize, fontname='Arial')

# plt.tight_layout()
# plt.show()

# # Second plot (Worst composition)
# plt.figure(figsize=(10, 7))
# ax = plt.gca()
# for spine in ax.spines.values():
#     spine.set_linewidth(3)
# ax.tick_params(axis='both', which='major', labelsize=fsize)
# ax.set_xlim(0, 60)

# plt.hist(worst_distances, bins=50, alpha=0.7, density=True)
# plt.title("Distance Distribution - Worst Composition", fontsize=fsize+2, fontname='Arial')
# plt.xlabel("Euclidean Distance (lower = more similar)", fontsize=fsize, fontname='Arial')
# plt.ylabel("Frequency", fontsize=fsize, fontname='Arial')

# # Add a secondary x-axis for similarity percentage
# ax2 = ax.twiny()
# similarity_ticks = np.linspace(0, 60, 6)
# similarity_labels = [f"{composition_similarity_percentage(d):.1f}%" for d in similarity_ticks]
# ax2.set_xlim(0, 60)
# ax2.set_xticks(similarity_ticks)
# ax2.set_xticklabels(similarity_labels, fontsize=fsize, fontname='Arial')
# ax2.set_xlabel("Composition Similarity", fontsize=fsize, fontname='Arial')
# ax2.tick_params(axis='x', which='major', labelsize=fsize)

# # Add threshold lines
# for threshold in thresholds:
#     similarity = composition_similarity_percentage(threshold)
#     plt.axvline(x=threshold, color='r', linestyle='--', linewidth=5)
#     plt.text(threshold + 0.5, plt.ylim()[1] * 0.95, f"{similarity:.1f}%",
#              rotation=90, verticalalignment='top', fontsize=fsize, fontname='Arial')

# plt.tight_layout()
# plt.show()
###################################################################
####### NEW PLOTTING CODE
# Plot histograms of distances with similarity percentages only
fsize = 35  # Define fontsize for tick labels

# Convert distances to similarity percentages
best_similarities = [composition_similarity_percentage(d) for d in best_distances]
worst_similarities = [composition_similarity_percentage(d) for d in worst_distances]

# First plot (Best composition)
plt.figure(figsize=(10, 7))
ax = plt.gca()
for spine in ax.spines.values():
    spine.set_linewidth(3)  # Sets a thicker border
ax.tick_params(axis='both', which='major', labelsize=fsize)
# Set x-axis from 100% to 0% (left to right)
ax.set_xlim(100, 50)  

# Use density=True to normalize and divide by bin width 
# Then multiply by len(best_similarities)/total_polymers to get fraction of total
# weights = np.ones_like(best_similarities) / total_polymers
# plt.hist(best_similarities, bins=50, alpha=0.9, weights=weights)
plt.hist(best_similarities, bins=100, alpha=0.9, density=True)

# plt.title("Composition Similarity Distribution - Best Composition", fontsize=fsize+2, fontname='Arial')
plt.xlabel("Composition Similarity (%)", fontsize=fsize, fontname='Arial')
plt.ylabel("Fraction of Total Oligomers", fontsize=fsize, fontname='Arial')

# Add threshold lines (convert thresholds to similarity percentages)
for threshold in thresholds:
    similarity = composition_similarity_percentage(threshold)
    plt.axvline(x=similarity, color='r', linestyle='--', linewidth=5)
    plt.text(similarity - 1, plt.ylim()[1] * 0.95, f"{similarity:.0f}%", 
             rotation=0, verticalalignment='top', fontsize=fsize, fontname='Arial')

plt.tight_layout()
plt.show()

# Second plot (Worst composition)
plt.figure(figsize=(10, 7))
ax = plt.gca()
for spine in ax.spines.values():
    spine.set_linewidth(3)
ax.tick_params(axis='both', which='major', labelsize=fsize)
ax.set_xlim(100, 50)  # Set x-axis from 100% to 0% (left to right)

# Use weights to get fraction of total polymers
# weights = np.ones_like(worst_similarities) / total_polymers
# plt.hist(worst_similarities, bins=50, alpha=0.9, weights=weights)
plt.hist(worst_similarities, bins=100, alpha=0.9, density=True)

# plt.title("Composition Similarity Distribution - Worst Composition", fontsize=fsize+2, fontname='Arial')
plt.xlabel("Composition Similarity (%)", fontsize=fsize, fontname='Arial')
plt.ylabel("Fraction of Total Oligomers", fontsize=fsize, fontname='Arial')

# Add threshold lines
for threshold in thresholds:
    similarity = composition_similarity_percentage(threshold)
    plt.axvline(x=similarity, color='r', linestyle='--', linewidth=5)
    plt.text(similarity - 1, plt.ylim()[1] * 0.95, f"{similarity:.0f}%",
             rotation=0, verticalalignment='top', fontsize=fsize, fontname='Arial')

plt.tight_layout()
plt.show()

###################################################################


