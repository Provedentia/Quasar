The script expects a pandas, plotly, and a file named data.csv in the same directory.

Design Choices
The main challenge was the amplitude difference between EEG signals at 10-100 microvolts and ECG/EOG signals at thousands of microvolts. I used Plotly's make_subplots to create two separate y-axes: the top subplot with 70% height displays EEG channels, the bottom with 30% height displays ECG/EOG and reference channels.

EEG channels are scaled by 1/50 with 2-unit vertical offsets between traces. ECG/EOG channels are converted to millivolts by dividing by 1000 with 1 mV offsets. Channels are color-coded by brain region. The shared x-axis maintains temporal alignment across both subplots. A range slider enables scrolling through the time series.

AI Assistance
I primarily work with matplotlib, so I used generative AI to understand Plotly syntax, particularly for subplots, range sliders, and hover templates. I also used it for debugging trace assignment and scaling issues.

Future Work
Channel selection interface. Without neuroscience domain knowledge, I displayed all channels rather than risk hiding important data. Additional features considered: adjustable scaling modes, signal filtering, annotation markers, and frequency domain analysis.