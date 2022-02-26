# Main code
from mplsoccer.pitch import Pitch
import matplotlib.pyplot as plt
"""
pitch = Pitch(  # pitch extends slightly below halfway line
    half=False,  # half of a pitch
    goal_alpha=0.4,
    pitch_type='opta',
    pitch_color='grey',
    tight_layout=True,
    line_color='white',
    linewidth=4.5)
"""
"""pitch = Pitch(  # pitch extends slightly below halfway line
    half=False,  # half of a pitch
    goal_alpha=0.4,
    pitch_type='opta',
    pitch_color='grey',
    tight_layout=True,
    line_color='white',
    linewidth=2.5)
"""
pitch = Pitch(axis=True, label=True, tick=True, pitch_type='opta')
fig, ax = pitch.draw()
sc1 = pitch.scatter(0.690999985*100, 0.034000001*100, ax=ax)
plt.show()
"""fig, ax = pitch.draw(figsize=(11, 7))
sc1 = pitch.scatter(0.690999985*100, 0.034000001*100, ax=ax)
plt.savefig('football_pitch.png', bbox_inches='tight', pad_inches=0)
"""