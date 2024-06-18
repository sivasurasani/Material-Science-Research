import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def work_hardening(true_stress, true_strain):
    if len(true_stress) != len(true_strain):
        raise ValueError("true_stress and true_strain must have the same length")

    if len(true_stress) < 2:
        return np.array([])

    work_hardening_rate = np.diff(true_stress) / np.diff(true_strain)
    return work_hardening_rate

# Read the Excel file
data = pd.read_excel('Eng Values.xlsx')

if 't.stress' not in data.columns and 't.strain' not in data.columns:
    data['t.stress'] = data['eng.stress'] * (1 + data['eng.strain'])
    data['t.strain'] = np.log(1 + data['eng.strain'])

# Choose the degree of the polynomial
degree = 5

# Perform the polynomial fit using the correct column names
coefficients = np.polyfit(data['t.strain'], data['t.stress'], degree)

# Create a polynomial function from the coefficients
polynomial = np.poly1d(coefficients)

# Generate evenly spaced values over the range of the original true strain values
new_true_strain = np.linspace(data['t.strain'].min(), data['t.strain'].max(), 65)

# Evaluate the polynomial at the new strain values
fitted_true_stress = polynomial(new_true_strain)

# Create a new DataFrame to store the fitted values
fitted_data = pd.DataFrame({
    't.strain': new_true_strain,
    't.stress': fitted_true_stress
})

work_hardening_rate = work_hardening(fitted_true_stress, new_true_strain)

# Since Work hardening rate has one less entry than the original data, so we'll add NaN at the end
work_hardening_rate_padded = np.append(work_hardening_rate, np.nan)

fitted_data['hard.Rate'] = work_hardening_rate_padded

# Plot both graphs in a single figure with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

ax1.scatter(data['t.strain'], data['t.stress'], label='Original Data', color='blue')
ax1.plot(new_true_strain, fitted_true_stress, label=f'Polynomial Fit (degree={degree})', color='red')
ax1.set_xlabel('True Strain')
ax1.set_ylabel('True Stress')
ax1.legend()
# ax1.set_title('True Stress vs True Strain')

ax2.plot(new_true_strain[:-1], work_hardening_rate, label='Work Hardening Rate', color='green')
ax2.set_xlabel('True Strain')
ax2.set_ylabel('Work Hardening Rate')
ax2.legend()
# ax2.set_title('Work Hardening Rate vs True Strain')

plt.tight_layout()
plt.show()

# let's save the fitted data to a new Excel file
fitted_data.to_excel('fitted_hard_rate_cal.xlsx', index=False)