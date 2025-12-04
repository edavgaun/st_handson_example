import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def time_series(data):
    """Streamlit tab showing a time series of Uber metrics in Boston."""

    st.header("📈 Time Series of Uber Trips in Boston")

    df = data["Switchbacks"].copy()
    df['period_start'] = pd.to_datetime(df['period_start'])

    # Optional: let user select which metrics to display
    all_metrics = ['trips_pool', 'trips_express', 'rider_cancellations']
    metrics_to_plot = st.multiselect(
        "Select metrics to plot",
        options=all_metrics,
        default=all_metrics
    )

    if not metrics_to_plot:
        st.info("Select at least one metric to display the chart.")
        return

    # Create Plotly figure
    fig = go.Figure()
    for y_column in metrics_to_plot:
        fig.add_trace(
            go.Scatter(
                x=df['period_start'],
                y=df[y_column],
                mode='lines+markers',
                name=y_column
            )
        )

    fig.update_layout(
        title='Time Series of Uber Metrics in Boston',
        xaxis_title='Time',
        yaxis_title='Value',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)
