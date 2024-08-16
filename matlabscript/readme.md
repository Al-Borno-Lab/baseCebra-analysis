# saveKinAggrogate MATLAB Function

## Overview

The saveKinAggrogate function processes and aggregates neural and kinematic data from a given MATLAB .mat file. The function then saves the aggregated data into a new file. This function is designed to work with data structures that include neural firing activity, complex spikes, and kinematic data associated with reach stimulation.

## Prerequisites

*	MATLAB installed on your system.
*	A MATLAB .mat file containing the variables cellData and ReachS which are required by the function.

## Function Syntax
```
saveKinAggrogate(fileName)
```

### Parameters
* fileName: A string representing the path and name of the .mat file containing the necessary data structures (cellData and ReachS).

## usage

1.	Prepare Your Data File: Ensure that your data file (a .mat file) contains the variables cellData and ReachS.
2.	Place the Function in Your MATLAB Workspace: Save the saveKinAggrogate function in a .m file and place it in your current MATLAB working directory or add its location to the MATLAB path.
3.	Call the Function: Use the function by passing the name of your .mat file as an argument.

```
saveKinAggrogate('yourFileName.mat');
```
Replace 'yourFileName.mat' with the actual name of your file.

4. Check the Output: The function will output the number of Purkinje Cells (PCs) processed and save the aggregated data into a new .mat file with a name formatted as:

```
PC<total_PC>trial_<num_trials>_Cebra_scaled_bin1_complex_<exportPrefex>.mat
```

* <total_PC>: The total number of Purkinje Cells processed.
* <num_trials>: The number of trials (stimulations) in the data.
* <exportPrefex>: Any prefix specified (currently empty by default).


## Example
Suppose you have a file named experimentData.mat. To process this file, use the function as follows:

```
saveKinAggrogate('experimentData.mat');
```
After running the function, it will display the number of Purkinje Cells processed and save the output file with a descriptive name, such as PC5trial_10_Cebra_scaled_bin1_complex_.mat.

## Important Notes
* Ensure that your input .mat file contains the variables cellData and ReachS, structured appropriately.
* The function currently assumes a specific structure of cellData and ReachS. Modifications may be needed if your data structure differs.

## Contact
For any questions or issues related to this function, please contact Gunnar Enserro.