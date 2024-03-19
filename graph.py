import matplotlib.pyplot as plt

# Accuracy and efficiency values for each OCR method (replace placeholders with actual values)
tesseract_accuracy = 0.7
tesseract_efficiency = 0.63
easyocr_accuracy = 0.8
easyocr_efficiency = 0.5
hybrid_accuracy = 0.9
hybrid_efficiency = 0.75

# Data for the bar graph
methods = ['Tesseract OCR', 'EasyOCR', 'Hybrid Model']
accuracy_values = [tesseract_accuracy, easyocr_accuracy, hybrid_accuracy]
efficiency_values = [tesseract_efficiency, easyocr_efficiency, hybrid_efficiency]

# Plotting the bar graph
fig, ax = plt.subplots()
index = range(len(methods))
bar_width = 0.35
opacity = 0.8

rects1 = ax.bar(index, accuracy_values, bar_width, alpha=opacity, color='b', label='Accuracy')
rects2 = ax.bar([p + bar_width for p in index], efficiency_values, bar_width, alpha=opacity, color='g', label='Efficiency')

ax.set_xlabel('OCR Methods')
ax.set_ylabel('Scores')
ax.set_title('Comparison of OCR Methods')
ax.set_xticks([p + bar_width/2 for p in index])
ax.set_xticklabels(methods)
ax.legend()

plt.tight_layout()
plt.show()
