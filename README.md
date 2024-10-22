# Parameter Optimization and Text Extraction Utilities

This repository contains two main functionalities:
1. **Parameter Optimization and MSE Calculation**
2. **Text Extraction and Chemical Composition Identification**

## 1. Parameter Optimization and MSE Calculation

This module performs parameter optimization using Mean Squared Error (MSE) as the evaluation metric. It reads data from an Excel file, calculates the MSE for various parameter values, and determines the best set of parameters that minimize the MSE. The code uses vectorized operations to ensure fast performance compared to traditional for-loop-based methods.

### Features
- **Efficient Vectorized MSE Calculation**: Uses NumPy for fast element-wise operations on large datasets.
- **Parameter Grid Search**: Explores a grid of parameters (`b0`, `d1`, `d2`, `ei`) to find the optimal values.
- **Euclidean Distance Calculation**: Computes the Euclidean distance between the original data and the model's output.
- **Optimal Parameters**: Outputs the best parameters that result in the lowest MSE.

### Requirements
- Python 3.x
- Required Python packages:
  - `pandas`
  - `numpy`
  - `openpyxl` (for reading Excel files)

Install the required packages via pip:
```bash
pip install pandas numpy openpyxl
```

### How It Works
1. **Input Data**: The program reads input data from an Excel file specified by the user. The file should contain columns for the x-axis (`ep_values`) and y-axis (`original_results`).
2. **Grid Search**: It performs a grid search across multiple combinations of parameters `b0`, `d1`, `d2`, and `ei` and calculates the MSE using vectorized operations.
3. **Best Parameter Selection**: The combination of parameters with the lowest MSE is selected.

### Example Usage

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
Replace `data.xlsx` with the path to your dataset, and adjust the column names (`X_values`, `Y_values`) accordingly.

### Performance
The vectorized implementation provides significant speedups for large datasets compared to traditional loops, resulting in more efficient optimization.

---

## 2. Text Extraction and Chemical Composition Identification

This module processes text to extract chemical compositions based on a predefined pattern (elements and their counts) and checks if the extracted composition matches known chemical elements.

### Features
- **Regular Expression-Based Extraction**: Uses a regular expression to extract potential chemical compositions from the text.
- **Element Validation**: Cross-checks extracted compositions with a list of valid chemical elements.
- **Minimum Length Filter**: Filters out compositions shorter than a specified minimum length to ensure relevant results.

### How It Works
1. **Text Input**: The program takes a text input, searches for chemical compositions using a regular expression pattern, and compares them against a predefined list of elements.
2. **Element Validation**: Only valid chemical compositions containing known elements are retained.
3. **Length Filtering**: Short compositions (below a specified minimum length) are discarded.

### Example Usage

```python
from utils_v2 import extract_chemical_compositions

# Example text containing chemical compositions
text = "The reaction involves H2O, NaCl, and C6H12O6."
elements = ['H', 'O', 'Na', 'Cl', 'C']  # List of valid chemical elements
min_length = 2  # Minimum length for chemical composition

# Extract chemical compositions
compositions = extract_chemical_compositions(text, elements, min_length)
print(compositions)
```

### Customization
- **Regular Expression**: Modify the regular expression pattern to suit your specific use case.
- **Element List**: Customize the list of valid elements based on your dataset or domain requirements.

---

## Repository Structure

- `code_analysis_v_12.ipynb`: Notebook implementing parameter optimization and MSE calculation.
- `utils_v2.py`: Contains text extraction utilities for identifying chemical compositions from text.
