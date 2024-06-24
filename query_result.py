import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.text import Annotation

def load_json(file_path):
    """Load the JSON data from the specified file path."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def parse_query(query_str):
    """Parse the user input into a dictionary of query conditions."""
    queries = []
    conditions = query_str.split(';')
    for condition in conditions:
        query = {}
        pairs = condition.split(',')
        for pair in pairs:
            key, value = pair.split('=')
            key = key.strip()
            value = value.strip()
            if '-' in value:
                value = tuple(map(float, value.split('-')))
            else:
                try:
                    value = float(value) if '.' in value else int(value)
                except ValueError:
                    pass  # Keep value as a string if it can't be converted to a number
            query[key] = value
        queries.append(query)
    return queries

def filter_entries(data, queries):
    """Filter entries based on the query conditions."""
    filtered_data = data
    for query in queries:
        current_filtered = []
        for entry in filtered_data:
            match = True
            for key, value in query.items():
                keys = key.split('.')
                sub_entry = entry
                for k in keys:
                    if k in sub_entry:
                        sub_entry = sub_entry[k]
                    else:
                        match = False
                        break
                if isinstance(sub_entry, list) and key == 'lemma':
                    if not set(value.split()).issubset(set(sub_entry)):
                        match = False
                        break
                elif isinstance(sub_entry, (int, float)):
                    if isinstance(value, tuple):
                        if not (value[0] <= sub_entry <= value[1]):
                            match = False
                            break
                    elif sub_entry != value:
                        match = False
                        break
                elif sub_entry != value:
                    match = False
                    break
            if match:
                current_filtered.append(entry)
        filtered_data = current_filtered
    return filtered_data

def format_text(text, line_length=40):
    """Format text to fit within a given line length."""
    words = text.split()
    formatted_text = ''
    line = ''
    for word in words:
        if len(line) + len(word) + 1 > line_length:
            formatted_text += line + '\n'
            line = word + ' '
        else:
            line += word + ' '
    formatted_text += line
    return formatted_text

def create_click_annotation(ax, fig, pos, data):
    """Create click annotations for the graph."""
    annot = Annotation("", xy=(0,0), xytext=(20,20),
                       textcoords="offset points",
                       bbox=dict(boxstyle="round", fc="w"),
                       arrowprops=dict(arrowstyle="->"))
    ax.add_artist(annot)
    annot.set_visible(False)

    node_data = {d['title']: d for d in data}

    def update_annot(node, event):
        annot.xy = (event.xdata, event.ydata)
        text = "\n".join(f"{k}: {v}" for k, v in node_data[node].items())
        formatted_text = format_text(text)
        annot.set_text(formatted_text)
        annot.get_bbox_patch().set_alpha(0.9)

        # Get the axes bounds in display coordinates
        ax_bounds = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        ax_left, ax_bottom, ax_right, ax_top = ax_bounds.extents

        # Determine annotation placement based on cursor position
        x_shift, y_shift = 20, 20
        if event.xdata < ax_left + 0.1 * (ax_right - ax_left):
            x_shift = -60
        if event.ydata < ax_bottom + 0.1 * (ax_top - ax_bottom):
            y_shift = -40

        annot.xytext = (x_shift, y_shift)

    def on_click(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            for node, (x, y) in pos.items():
                if abs(x - event.xdata) < 0.05 and abs(y - event.ydata) < 0.05:
                    update_annot(node, event)
                    annot.set_visible(True)
                    plt.draw()
                    return
            if vis:
                annot.set_visible(False)
                plt.draw()

    return on_click

def draw_graph(results):
    """Draw a graph connecting all the results based on the title as the node name."""
    G = nx.Graph()
    
    for entry in results:
        if 'title' in entry:
            G.add_node(entry['title'])
    
    # Connect all nodes in a sequential manner
    titles = [entry['title'] for entry in results if 'title' in entry]
    for i in range(len(titles) - 1):
        G.add_edge(titles[i], titles[i + 1])
    
    # Use a circular layout
    pos = nx.circular_layout(G)
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10, font_weight='bold', edge_color='gray', ax=ax)
    
    click = create_click_annotation(ax, fig, pos, results)
    fig.canvas.mpl_connect("button_press_event", click)
    
    plt.show()

def main():
    file_path = 'allData_result.json'
    data = load_json(file_path)
    
    while True:
        query_str = input("Enter your search queries separated by ';' (or type 'exit' to quit): ")
        if query_str.lower() == 'exit':
            break
        
        queries = parse_query(query_str)
        filtered_data = filter_entries(data, queries)
        
        print("Search results:")
        for entry in filtered_data:
            print(entry)
        
        if filtered_data:
            draw_graph(filtered_data)

if __name__ == "__main__":
    main()