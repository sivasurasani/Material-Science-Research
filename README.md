# Parameter Optimization and MSE Calculation

This project performs parameter optimization using Mean Squared Error (MSE) as the evaluation metric. It reads data from an Excel file, calculates the MSE for various parameter values, and determines the best set of parameters that minimize the MSE. The code is designed to handle a vectorized calculation for faster performance compared to traditional for-loop-based methods.

## Features
- **Efficient Vectorized MSE Calculation**: Uses NumPy to perform fast, element-wise operations on large datasets.
- **Parameter Grid Search**: Explores a grid of parameters (b0, d1, d2, ei) to find the optimal values.
- **Euclidean Distance Computation**: Calculates the Euclidean distance between the original data and the model's output.
- **User-Friendly Output**: Displays the best parameters and the corresponding MSE value.

## Requirements
- Python 3.x
- Required Python packages:
  - `pandas`
  - `numpy`
  - `openpyxl` (for reading Excel files)

You can install the necessary packages via pip:
```bash
pip install pandas numpy openpyxl
```

## How It Works
1. **Input Data**: The program reads input data from an Excel file specified by the user. The file should contain the columns for the x-axis (`ep_values`) and y-axis (`original_results`), which will be used to calculate the MSE.
2. **Grid Search**: It performs a grid search across multiple combinations of the parameters `b0`, `d1`, `d2`, and `ei` and calculates the MSE for each combination using vectorized operations.
3. **Best Parameter Selection**: The combination of parameters that results in the lowest MSE is selected as the best parameter set.

## Usage

1. **Function Parameters**:
   - `file_path`: Path to the Excel file containing the data.
   - `x_axis`: The column name representing the x-axis values.
   - `y2_axis`: The column name representing the y-axis values (the dependent variable).
   - `from_b0`, `to_b0`: Range of values for the parameter `b0`.
   - `min_d1`, `max_d1`: Range of values for the parameter `d1`.
   - `ee`: A constant value used in the calculations.

2. **Sample Function Call**:
   ```python
   find_best_parameters(
       file_path='data.xlsx',
       x_axis='X_values',
       y2_axis='Y_values',
       from_b0=10,
       to_b0=100,
       min_d1=0.5,
       max_d1=2.0,
       ee=0.01
   )
   ```

   Replace `data.xlsx` with the actual path to your data file, and adjust the column names (`X_values`, `Y_values`) as needed.

## Performance Optimization

This implementation uses vectorized operations with NumPy for better performance. For large datasets, this results in significant speedups compared to traditional Python loops.
