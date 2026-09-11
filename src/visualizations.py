import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

df = pd.read_csv("device_sustainability_deduped.csv")
output_dir = Path("visualizations")
output_dir.mkdir(exist_ok=True)

# 1- Average Reported Lifespan by Manufacturer
fig, ax = plt.subplots(figsize=(14, 6))
df.groupby('manufacturer')['reported_age_years_avg'].mean().sort_values(ascending=False).plot(kind='bar', ax=ax, color='steelblue')
ax.set_title('Average Reported Lifespan by Manufacturer', fontsize=14, fontweight='bold')
ax.set_xlabel('Manufacturer', fontsize=12)
ax.set_ylabel('Average Lifespan (Years)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / '01_avg_lifespan.png', dpi=300, bbox_inches='tight')
plt.close()
print("1- Average Reported Lifespan by Manufacturer - created and saved")

# 2- Average Repairability Score by Manufacturer
fig, ax = plt.subplots(figsize=(14, 6))
df.groupby('manufacturer')['repairability_score'].mean().sort_values(ascending=False).plot(kind='bar', ax=ax, color='seagreen')
ax.set_title('Average Repairability Score by Manufacturer', fontsize=14, fontweight='bold')
ax.set_xlabel('Manufacturer', fontsize=12)
ax.set_ylabel('Average Repairability Score', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / '02_avg_repairability.png', dpi=300, bbox_inches='tight')
plt.close()
print("2- Average Repairability Score by Manufacturer - created and saved")

# 3- Average Battery Life by Manufacturer
fig, ax = plt.subplots(figsize=(14, 6))
df.groupby('manufacturer')['battery_life_hours'].mean().sort_values(ascending=False).plot(kind='bar', ax=ax, color='coral')
ax.set_title('Average Battery Life by Manufacturer', fontsize=14, fontweight='bold')
ax.set_xlabel('Manufacturer', fontsize=12)
ax.set_ylabel('Average Battery Life (Hours)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / '03_avg_battery_life.png', dpi=300, bbox_inches='tight')
plt.close()
print("3- Average Battery Life by Manufacturer - created and saved")

# 4- Release Year Distribution
fig, ax = plt.subplots(figsize=(12, 6))
df['release_year'].dropna().astype(int).value_counts().sort_index().plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
ax.set_title('Release Year Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Release Year', fontsize=12)
ax.set_ylabel('Number of Devices', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / '04_release_year_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("4- Release Year Distribution - created and saved")

# 5- Battery Life vs Reported Lifespan
fig, ax = plt.subplots(figsize=(10, 7))
df_clean = df.dropna(subset=['battery_life_hours', 'reported_age_years_avg'])
ax.scatter(df_clean['battery_life_hours'], df_clean['reported_age_years_avg'], alpha=0.6, s=80)
ax.set_title('Battery Life vs Reported Lifespan', fontsize=14, fontweight='bold')
ax.set_xlabel('Battery Life (Hours)', fontsize=12)
ax.set_ylabel('Reported Lifespan (Years)', fontsize=12)
plt.tight_layout()
plt.savefig(output_dir / '05_battery_vs_lifespan.png', dpi=300, bbox_inches='tight')
plt.close()
print("5- Battery Life vs Reported Lifespan - created and saved")

# 6- Price vs Reported Lifespan
fig, ax = plt.subplots(figsize=(10, 7))
df_clean = df.dropna(subset=['price_usd', 'reported_age_years_avg'])
ax.scatter(df_clean['price_usd'], df_clean['reported_age_years_avg'], alpha=0.6, s=80)
ax.set_title('Price vs Reported Lifespan', fontsize=14, fontweight='bold')
ax.set_xlabel('Price (USD)', fontsize=12)
ax.set_ylabel('Reported Lifespan (Years)', fontsize=12)
plt.tight_layout()
plt.savefig(output_dir / '06_price_vs_lifespan.png', dpi=300, bbox_inches='tight')
plt.close()
print("6- Price vs Reported Lifespan - created and saved")

# 7- Repairability Score vs Reported Lifespan
fig, ax = plt.subplots(figsize=(10, 7))
df_clean = df.dropna(subset=['repairability_score', 'reported_age_years_avg'])
ax.scatter(df_clean['repairability_score'], df_clean['reported_age_years_avg'], alpha=0.6, s=80)
ax.set_title('Repairability Score vs Reported Lifespan', fontsize=14, fontweight='bold')
ax.set_xlabel('Repairability Score', fontsize=12)
ax.set_ylabel('Reported Lifespan (Years)', fontsize=12)
plt.tight_layout()
plt.savefig(output_dir / '07_repairability_vs_lifespan.png', dpi=300, bbox_inches='tight')
plt.close()
print("7- Repairability Score vs Reported Lifespan - created and saved")

# 8- Storage Type Distribution
fig, ax = plt.subplots(figsize=(12, 6))
df['storage_type'].value_counts().plot(kind='bar', ax=ax, color='teal', edgecolor='black')
ax.set_title('Storage Type Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Storage Type', fontsize=12)
ax.set_ylabel('Number of Devices', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / '08_storage_type_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("8- Storage Type Distribution - created and saved")

# 9- Missing Values by Column
fig, ax = plt.subplots(figsize=(14, 6))
missing_values = df.isnull().sum().sort_values(ascending=False)
missing_values = missing_values[missing_values > 0]
if missing_values.empty:
    ax.text(0.5, 0.5, 'No missing values', ha='center', va='center', fontsize=14)
    ax.set_xticks([])
    ax.set_yticks([])
else:
    missing_values.plot(kind='bar', ax=ax, color='salmon', edgecolor='black')
ax.set_title('Missing Values by Column', fontsize=14, fontweight='bold')
ax.set_xlabel('Column Name', fontsize=12)
ax.set_ylabel('Number of Missing Values', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / '09_missing_values.png', dpi=300, bbox_inches='tight')
plt.close()
print("9- Missing Values by Column - created and saved")

# 10- Correlation Heatmap
fig, ax = plt.subplots(figsize=(14, 10))
numeric_cols = ['ram_gb', 'storage_capacity_gb', 'battery_capacity_wh', 'battery_life_hours', 'weight_kg', 
                'repairability_score', 'price_usd', 'reported_age_years_avg']
correlation_matrix = df[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, square=True, linewidths=0.5)
ax.set_title('Correlation Heatmap of Key Variables', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(output_dir / '10_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("10- Correlation Heatmap - created and saved")
