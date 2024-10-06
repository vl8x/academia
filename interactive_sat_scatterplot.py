import plotly.express as px
import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact

# Load the data from the Excel file (use the data you uploaded)
df = pd.read_parquet('sat_data.parquet')

# Create slider widgets for score range
min_score_slider = widgets.IntSlider(value=400, min=200, max=800, step=10, description='Min Score:')
max_score_slider = widgets.IntSlider(value=800, min=200, max=800, step=10, description='Max Score:')

# Get unique major options from the dataset
unique_majors = ['All'] + df['Intended Major'].unique().tolist()

# Create a dropdown for selecting a major
major_dropdown = widgets.Dropdown(
    options=unique_majors,
    description='Major:',
    value='All'
)

# Link widgets to interactively update the plot when sliders or dropdown changes
@interact(min_score=min_score_slider, max_score=max_score_slider, selected_major=major_dropdown)
def update_plot(min_score, max_score, selected_major):
    # Filter the data based on the slider values
    filtered_data_erw = df[(df['Score_ERW'] >= min_score) & (df['Score_ERW'] <= max_score)]
    filtered_data_math = df[(df['Score_Math'] >= min_score) & (df['Score_Math'] <= max_score)]

    # Apply major filter if a specific major is selected
    if selected_major != 'All':
        filtered_data_erw = filtered_data_erw[filtered_data_erw['Intended Major'] == selected_major]
        filtered_data_math = filtered_data_math[filtered_data_math['Intended Major'] == selected_major]
    
    # Create scatter plot for ERW
    fig = px.scatter(
        filtered_data_erw, 
        x='Score_ERW', 
        y='Intended Major', 
        color_discrete_sequence=['blue'], 
        title=f"ERW and Math Scores (Filtered by Score Range and Major)",
        labels={'Score_ERW': 'SAT Score', 'Intended Major': 'Major'},
        hover_data=['Intended Major']
    )

    # Add Math scores as a separate trace
    fig.add_scatter(
        x=filtered_data_math['Score_Math'], 
        y=filtered_data_math['Intended Major'], 
        mode='markers', 
        marker=dict(color='red'), 
        name='Math'
    )

    # Add ERW to the legend explicitly
    fig.add_scatter(
        x=filtered_data_erw['Score_ERW'], 
        y=filtered_data_erw['Intended Major'], 
        mode='markers', 
        marker=dict(color='blue'), 
        name='ERW'
    )

    # Adjust layout for better readability
    fig.update_layout(
        height=800, 
        width=1000, 
        legend_title=None,  # Remove the legend title
        legend=dict(x=0, y=1), 
        showlegend=True
    )
    
    # Show the figure
    fig.show()
