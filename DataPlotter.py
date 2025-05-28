import matplotlib.pyplot as plt

def plot(data):
    plt.plot(data)
    plt.show()

def verticalBarPlot(data, indices, title = '', ylabel = '', color = 'white', edgecolor = 'black', long_label = False):
    plt.figure(figsize = (6, 4))
    bars = plt.bar(x = range(len(data)), height = data, color = color, edgecolor = edgecolor, width = 0.7)

    for bar in bars:
        height = round(bar.get_height())
        plt.text(bar.get_x() + bar.get_width()/2, height + 200, f'{height}', ha = 'center', fontsize = 10)

    if long_label:
        plt.xticks(range(len(data)), indices, rotation = 45, ha = 'center')
    else:
        plt.xticks(range(len(data)), indices)
    
    plt.ylim(0, max(data) * 1.4)
    plt.title(title, fontsize = 14)
    plt.ylabel(ylabel, fontsize = 12)
    plt.grid(axis = 'y', linestyle = '--', alpha = 0.7)
    plt.tight_layout()
    plt.show()

def horizontalBarPlot(data, indices, title = '', xlabel = '', color = 'white', edgecolor = 'black', long_label = False):
    # convert Series to list 
    data = data.tolist()
    indices = indices.tolist()
    
    plt.figure(figsize = (6, 4))
    bars = plt.barh(y = range(len(data)), width = data, color = color, edgecolor = edgecolor, height = 0.7)

    plt.yticks(range(len(data)), ['' for _ in indices])

    for index, bar in enumerate(bars):
        # calculate text color based on bar color brightness
        text_color = 'black' if color == 'white' else 'white'
        
        # add artist names inside the bars
        plt.text(50, bar.get_y() + bar.get_height() / 2,  # Slight offset from the left
             indices[index], va = 'center', ha = 'left', color = 'white', fontsize = 14)
    
        # add play counts outside the bars
        plt.text(bar.get_width() + 50, bar.get_y() + bar.get_height() / 2,
             f'{data[index]}', va = 'center', ha = 'left', color = 'black', fontsize = 10)
    
    plt.gca().invert_yaxis()
    plt.xlim(0, max(data) * 1.1)
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
