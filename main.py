import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('data.csv', comment='#')
df.columns = df.columns.str.strip()
# print(df.head())
# print(df.columns)

eeg_channels = ['Fz', 'Cz', 'P3', 'C3', 'F3', 'F4', 'C4', 'P4', 'Fp1', 'Fp2', 
                'T3', 'T4', 'T5', 'T6', 'O1', 'O2', 'F7', 'F8', 'A1', 'A2', 'Pz']
ecg_channels = ['X1:LEOG', 'X2:REOG']
# for ecg in ecg_channels:
#     print(df[ecg])
# print(df['CM'])

fig = make_subplots(rows=2, cols=1, 
                    row_heights=[0.7, 0.3],
                    shared_xaxes=True,
                    vertical_spacing=0.02,
                    subplot_titles=('EEG Channels', 'ECG Channels'))


available_eeg_channels = [col for col in eeg_channels if col in df.columns]
sorted_eeg_channels = sorted(available_eeg_channels, key=lambda col: abs(df[col].mean()), reverse=True)

eeg_count = 0
for col in sorted_eeg_channels:
    y_data = df[col].values / 50
    y_data = y_data - eeg_count * 2

    if col.startswith('F'):
        color = 'blue'
    elif col.startswith('C'):
        color = 'green'
    elif col.startswith('P'):
        color = 'purple'
    elif col.startswith('T'):
        color = 'orange'
    elif col.startswith('O'):
        color = 'brown'
    else:
        color = 'black'

    fig.add_trace(go.Scatter(
        x=df['Time'],
        y=y_data,
        mode='lines',
        name=col,
        line=dict(width=0.5, color=color),
        hovertemplate=f'{col}<br>Time: %{{x:.3f}}s<br>Value: %{{customdata:.2f}} uV<extra></extra>',
        customdata=df[col].values
    ), row=1, col=1)

    eeg_count += 1

# Sort ECG channels by their mean absolute values (highest to lowest)
ecg_cols = ['X1:LEOG', 'X2:REOG', 'CM']
available_ecg_cols = [col for col in ecg_cols if col in df.columns]
sorted_ecg_cols = sorted(available_ecg_cols, key=lambda col: abs(df[col].mean()), reverse=True)

ecg_count = 0
for col in sorted_ecg_cols:
    y_data = df[col].values / 1000
    y_data = y_data - ecg_count * 1

    if col in ecg_channels:
        color = 'red'
    else:
        color = 'gray'

    fig.add_trace(go.Scatter(
        x=df['Time'],
        y=y_data,
        mode='lines',
        name=col,
        line=dict(width=0.8, color=color),
        hovertemplate=f'{col}<br>Time: %{{x:.3f}}s<br>Value: %{{customdata:.2f}} uV<extra></extra>',
        customdata=df[col].values
    ), row=2, col=1)

    ecg_count += 1

fig.update_xaxes(title_text='Time (seconds)', row=2, col=1, 
                 rangeslider=dict(visible=True, thickness=0.08))
fig.update_yaxes(title_text='EEG Amplitude', row=1, col=1)
fig.update_yaxes(title_text='ECG (mV)', row=2, col=1)

fig.update_layout(
    title='EEG/ECG Multichannel Viewer',
    height=800,
    hovermode='closest',
    showlegend=True
)

fig.show()