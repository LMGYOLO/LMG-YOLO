import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_metrics(ax, metric_col_name, y_label, color, modelname, is_last_model=False):
    res_path = pr_csv_dict[modelname]
    try:
        data = pd.read_csv(res_path)
        data.columns = data.columns.str.strip()  # Remove spaces from column names

        epochs = data['epoch'].values  # epoch column
        metric_data = data[metric_col_name].values  # Get the corresponding metric column
        ax.plot(epochs, metric_data, label=modelname, color=color, linewidth='2')

        if is_last_model:
            # Mark the highest mAP value with a horizontal line at the highest mAP for the last model only
            max_mAP_epoch = np.argmax(metric_data)
            max_mAP_value = metric_data[max_mAP_epoch]

            # Draw horizontal line at the maximum mAP value in gray
            ax.axhline(y=max_mAP_value, color='gray', linestyle='--', linewidth=2)

            # Add text to mark the max value
            ax.text(epochs[max_mAP_epoch], max_mAP_value, f'{max_mAP_value:.2f}', color='gray', fontsize=14,
                    verticalalignment='bottom')

    except Exception as e:
        print(f"Error reading {modelname}: {e}")


# Main function
def plot_all_metrics():
    global pr_csv_dict
    pr_csv_dict = {
        'YOLOv11': r'runs/train/Baseline/results.csv',
        '+LCSG': r'runs/train/base+LCSG/results.csv',
        '+MSI': r'runs/train/base+MSI/results.csv',
        '+GIA': r'runs/train/base+GIA/results.csv',
        'LMG-YOLO': r'runs/train/exp15/results1.csv',
    }

    colors = {
        'YOLOv11': '#00EE76',
        '+LCSG': '#EEEE00',
        '+MSI': '#8470FF',
        '+GIA': 'orange',
        'LMG-YOLO': 'r'
    }

    fig, axs = plt.subplots(1, 1, tight_layout=True)  # Only 1 subplot for mAP@0.5-0.95

    # Set global font size
    plt.rcParams.update({'font.size': 15})

    # Plot mAP@0.5-0.95
    for modelname in pr_csv_dict:
        # Set is_last_model to True only for 'LMG-YOLO'
        is_last_model = (modelname == 'LMG-YOLO')
        plot_metrics(axs, 'metrics/mAP50-95(B)', 'mAP@0.95', colors[modelname], modelname, is_last_model)

    axs.set_xlabel('Epoch', fontsize=15)
    axs.set_ylabel('mAP@0.95', fontsize=15)
    axs.set_xlim(0, None)
    axs.set_ylim(0, 0.7)
    axs.legend(loc='lower right', fontsize=15)
    axs.spines['top'].set_linewidth(2)
    axs.spines['right'].set_linewidth(2)
    axs.spines['left'].set_linewidth(2)
    axs.spines['bottom'].set_linewidth(2)
    axs.tick_params(width=2, labelsize=15)
    # axs.set_title('mAP@0.95', fontsize=15)

    # Add a grid with gray lines
    axs.grid(True, which='both', linestyle='-', color='gray', alpha=0.5)

    plt.subplots_adjust(wspace=0.3)  # Adjust spacing between subplots

    # Save the figure
    plt.savefig('yolo_mAP_0_95.png', dpi=300)
    plt.show()


# Execute plotting
if __name__ == '__main__':
    plot_all_metrics()
