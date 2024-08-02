import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title='Data Visualizer', layout='centered', page_icon='📊')

st.title('📊  Data Visualizer')

working_dir = os.path.dirname(os.path.abspath(__file__))

folder_path = f"{working_dir}/data"  

files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

selected_file = st.selectbox('Select a file', files, index=None)

if selected_file:
    file_path = os.path.join(folder_path, selected_file)

    df = pd.read_csv(file_path)

    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col1:
        st.write("")
        st.write(df.head())

    with col2:
        x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

        plot_list = [
            'Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 
            'Count Plot', 'Box Plot', 'Violin Plot', 'Heatmap',
            '3D Surface Plot', 'Contour Plot', 'Choropleth Map', 
            'Pair Plot', 'Regression Plot', 'Swarm Plot'
        ]
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

    if st.button('Generate Plot'):
        if plot_type in ['3D Surface Plot', 'Choropleth Map']:
            fig = None
            if plot_type == '3D Surface Plot':
                fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=df.columns[2])
                fig.update_traces(marker=dict(size=5))
            elif plot_type == 'Choropleth Map':
                fig = px.choropleth(df, locations=x_axis, color=y_axis)
            st.plotly_chart(fig)
        else:
            fig, ax = plt.subplots(figsize=(6, 4))

            if plot_type == 'Line Plot':
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Bar Chart':
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Scatter Plot':
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Distribution Plot':
                sns.histplot(df[x_axis], kde=True, ax=ax)
                y_axis = 'Density'
            elif plot_type == 'Count Plot':
                sns.countplot(x=df[x_axis], ax=ax)
                y_axis = 'Count'
            elif plot_type == 'Box Plot':
                sns.boxplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Violin Plot':
                sns.violinplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Heatmap':
                sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
                x_axis = 'Features'
                y_axis = 'Features'
            elif plot_type == 'Contour Plot':
                X, Y = np.meshgrid(df[x_axis], df[y_axis])
                Z = df.iloc[:, 2]
                ax.contourf(X, Y, Z)
            elif plot_type == 'Regression Plot':
                sns.regplot(x=df[x_axis], y=df[y_axis], ax=ax)
            elif plot_type == 'Swarm Plot':
                sns.swarmplot(x=df[x_axis], y=df[y_axis], ax=ax)

            ax.tick_params(axis='x', labelsize=10)
            ax.tick_params(axis='y', labelsize=10)

            plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
            plt.xlabel(x_axis, fontsize=10)
            plt.ylabel(y_axis, fontsize=10)

            st.pyplot(fig)
