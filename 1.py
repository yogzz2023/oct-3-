import numpy as np
import math
import csv
import pandas as pd
from scipy.stats import chi2
# Define lists to store results
r = []
el = []
az = []

# Global Track ID Database
track_id_database = []  # Initialize as an empty list, will store dictionaries with 'id' and 'state'

class CVFilter:
    # ... (CVFilter class code remains the same)

def read_measurements_from_csv(file_path):
    # ... (Function code remains the same)

def sph2cart(az, el, r):
    # ... (Function code remains the same)

def cart2sph(x, y, z):
    # ... (Function code remains the same)

def form_measurement_groups(measurements, max_time_diff=0.050):
    # ... (Function code remains the same)

def form_clusters_via_association(tracks, reports, kalman_filter, chi2_threshold):
    # ... (Function code remains the same)

def mahalanobis_distance(track, report, cov_inv):
    # ... (Function code remains the same)

def select_best_report(cluster_tracks, cluster_reports, kalman_filter):
    # ... (Function code remains the same)

def select_initiation_mode(mode):
    # ... (Function code remains the same)
    
def doppler_correlation(doppler_1, doppler_2, doppler_threshold):
    # ... (Function code remains the same)

def initialize_tracks(measurement_groups, doppler_threshold, range_threshold, firm_threshold, mode):
    # ... (Function code remains the same)

def main():
    file_path = 'ttk.csv'
    measurements = read_measurements_from_csv(file_path)

    kalman_filter = CVFilter()
    measurement_groups = form_measurement_groups(measurements, max_time_diff=0.050)

    tracks = []  
    filter_states = []

    doppler_threshold = 100
    range_threshold = 100
    firm_threshold = 3
    mode = '3-state'

    firm_threshold = select_initiation_mode(mode)
    # Initialize variables outside the loop
    miss_counts = {}
    hit_counts = {}
    firm_ids = set()
    state_map = {}
    progression_states = {
        3: ['Poss1', 'Tentative1', 'Firm'],
        5: ['Poss1', 'Poss2', 'Tentative1', 'Tentative2', 'Firm'],
        7: ['Poss1', 'Poss2', 'Tentative1', 'Tentative2', 'Tentative3', 'Firm']
    }[firm_threshold]

    for group_idx, group in enumerate(measurement_groups):
        print(f"Processing measurement group {group_idx + 1}...")

        if len(group) == 1:  # Single Measurement
            print("Single Measurement Processing")
            rng, azm, ele, mt, md, *rest = group[0]
            x, y, z = sph2cart(azm, ele, rng)
            measurement = (x, y, z, mt)

            # Correlation Check with Existing Tracks
            correlated_track_id = None
            for track_id, track_data in enumerate(tracks):
                if not track_data:
                    continue
                # Assuming correlation check involves distance and maybe Doppler
                if np.linalg.norm(np.array(measurement[:3]) - np.array(track_data['measurements'][-1][0][5:8])) < range_threshold:  # Example distance check
                    correlated_track_id = track_id
                    break

            if correlated_track_id is not None:
                print(f"Measurement correlated with Track ID: {correlated_track_id}")
                # ... (Rest of the logic for existing track, similar to your original code)
            else:
                print("Measurement not correlated, initiating a new track...")
                # Find a free track ID from the database
                free_track_id = None
                for i, track_entry in enumerate(track_id_database):
                    if track_entry['state'] == 'free':
                        free_track_id = track_entry['id']
                        track_id_database[i]['state'] = 'occupied'
                        break

                if free_track_id is not None:
                    # Initialize a new track and assign the measurement
                    new_track = {
                        'track_id': free_track_id,
                        'measurements': [(group[0], 'Poss1')],  # Add measurement to the track
                        'current_state': 'Poss1',
                        'Sf': np.zeros((6, 1)),
                        'Pf': np.eye(6),
                        'Pp': np.eye(6),
                        'Sp': np.zeros((6, 1))
                    }
                    tracks.append(new_track)
                    kalman_filter.initialize_filter_state(x, y, z, 0, 0, 0, mt)
                    new_track['Sf'] = kalman_filter.Sf.copy()
                    new_track['Pf'] = kalman_filter.Pf.copy()
                    new_track['Pp'] = kalman_filter.Pp.copy()
                    new_track['Sp'] = kalman_filter.Sp.copy()
                    hit_counts[free_track_id] = 1  # First hit
                    miss_counts[free_track_id] = 0
                    state_map[free_track_id] = 'Poss1'
                    print(f"New Track initiated with ID: {free_track_id}")
                else:
                    print("No free track IDs available in the database!")

        else:  # Multiple Measurements
            print("Multiple Measurement Processing (JPDA)")
            reports = [(sph2cart(azm, ele, rng)) for rng, azm, ele, mt, md, *rest in group]

            # ... (Perform JPDA, get the best hypothesis report, 
            #      and use it for track state update, similar to your original code)

    # ... (Rest of your code, including summary generation)

if __name__ == "__main__":
    main()