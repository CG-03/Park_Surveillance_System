import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to results.csv
results_path = "runs/detect/train16/results.csv"  # change train16 if needed

# Load CSV
df = pd.read_csv(results_path)

# Create output folder
output_dir = "results_png"
os.makedirs(output_dir, exist_ok=True)

# ---- Plot Loss ----
plt.figure()
plt.plot(df["train/box_loss"], label="Box Loss")
plt.plot(df["train/cls_loss"], label="Class Loss")
plt.plot(df["train/dfl_loss"], label="DFL Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training Loss")
plt.legend()
plt.savefig(f"{output_dir}/loss.png")
plt.close()

# ---- Plot Precision & Recall ----
plt.figure()
plt.plot(df["metrics/precision(B)"], label="Precision")
plt.plot(df["metrics/recall(B)"], label="Recall")
plt.xlabel("Epoch")
plt.ylabel("Value")
plt.title("Precision & Recall")
plt.legend()
plt.savefig(f"{output_dir}/precision_recall.png")
plt.close()

# ---- Plot mAP@0.5 ----
plt.figure()
plt.plot(df["metrics/mAP50(B)"], label="mAP@0.5")
plt.xlabel("Epoch")
plt.ylabel("mAP")
plt.title("mAP@0.5")
plt.legend()
plt.savefig(f"{output_dir}/map50.png")
plt.close()

print("✅ PNG result plots generated successfully!")
