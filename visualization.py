import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

class Visualizer:
    def __init__(self, data):
        self.data = data

    def generate_heatmap(self, output_path="uploads/artistic_heatmap.png"):
        
        if 'temperature' in self.data.columns and 'date' in self.data.columns:
            pivot_data = self.data.pivot_table(
                index=self.data['date'].dt.month,
                columns=self.data['date'].dt.day,
                values='temperature',
                aggfunc=np.mean
            )
            plt.figure(figsize=(10, 6))
            sns.heatmap(pivot_data, cmap="coolwarm", cbar=True)
            plt.title("Heatmap of Temperatures")
            plt.savefig(output_path)
            plt.close()
            print(f"Heatmap saved to {output_path}.")