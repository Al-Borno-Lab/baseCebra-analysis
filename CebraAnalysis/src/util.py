import numpy as np

def bin10_with_padding(spike_matrix):
    """
    Takes a matrix of neuron spikes, pads it to ensure the number of columns is a multiple of 10,
    and then bins the data into time bins of size 10.
    
    Parameters:
    spike_matrix (numpy.ndarray): A 2D matrix where rows represent neurons and columns represent spikes over time.
    
    Returns:
    numpy.ndarray: A binned matrix where each time bin represents the sum of spikes within that bin.
    """
    num_neurons, num_spikes = spike_matrix.shape
    
    # Calculate the number of spikes needed to make the columns a multiple of 10
    padding_needed = (10 - (num_spikes % 10)) % 10
    
    # Pad the matrix with zeros if necessary
    if padding_needed > 0:
        spike_matrix = np.pad(spike_matrix, ((0, 0), (0, padding_needed)), 'constant')
    
    # Determine the number of bins
    num_bins = spike_matrix.shape[1] // 10
    
    # Reshape the matrix to group spikes into bins of 10
    reshaped_matrix = spike_matrix.reshape(num_neurons, num_bins, 10)
    
    # Sum the spikes within each bin
    binned_matrix = reshaped_matrix.sum(axis=2)
    
    return binned_matrix


if __name__ == "__main__":
    spike_matrix = np.random.randint(0, 2, (5, 93))  # Example spike data with 5 neurons and 93 time points
    binned_spike_matrix = bin10_with_padding(spike_matrix)
    print(binned_spike_matrix)