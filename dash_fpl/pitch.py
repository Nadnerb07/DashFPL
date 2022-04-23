
from mplsoccer.pitch import VerticalPitch, Pitch
import matplotlib.pyplot as plt


pitch = Pitch(
    half=False,
    goal_alpha=0.4,
    pitch_type='opta',
    pitch_color='#8d9db6',
    tight_layout=True,
    line_color='white',
    linewidth=2.5,
    axis=True)
fig, ax = pitch.draw(figsize=(11, 17))

plt.savefig('fooshots.png', bbox_inches='tight', pad_inches=0)
plt.show()
