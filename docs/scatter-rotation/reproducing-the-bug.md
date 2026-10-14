# Reproducing the bug

Part of [Scatter rotation](README.md): two protocols that show the bug on Parallax Continued 1.0.4, one
with the rocks seen from above, one with a kerbal standing on a rock. Each is played by hand, and by a
script.

## The rocks turn at every load

**The install**: [the install](README.md#the-builds-and-the-install) with the **release** build,
[KSP Diag - Colliders](https://github.com/lhervier/KSP-Diag-Colliders) and
[KSP Diag - Floating Origin](https://github.com/lhervier/KSP-Diag-FloatingOrigin). Diag Colliders is only
there to give the screenshots a mark fixed to the ground: it outlines in grey the collider of every
terrain quad within 300 m, so the edges of the quads meet in a cross at each vertex. It also draws, in
colour, the colliders Parallax gives the rocks near a craft. Diag Floating Origin shows
`directRotAngle`, the angle the Mun is turned by in the scene. `Alt+F6` hides both windows; the drawing
goes on.

**By hand**, about fifteen minutes:

1. Copy [`rocks-mun.sfs`](saves/rocks-mun.sfs) into the folder of a sandbox game and load it: a capsule
   of one part, landed on flat ground of the Mun, a few metres from a vertex of the terrain quads and some
   ten metres from the nearest rocks. Any craft standing still among rocks will do.
2. Press *Record* in the window of Diag Floating Origin. Look at the capsule from straight above, from
   some 40 m, and take a screenshot. Near the capsule, the grey edges meet in a cross: they are fixed to
   the ground, and tell that the view did not move nor turn from one screenshot to the next. The camera
   follows the craft, and a craft that moved would move the whole picture.
3. Let an hour of game time go by without loading anything: time warp ×100 on rails for about 36
   seconds. Take a screenshot again: nothing has moved, and `directRotAngle` has not changed.
4. Load **the same save** again, not a new one. Press *Record*, take the same screenshot: every cluster
   of rocks has turned on itself, around its own centre, while the ground, the quad edges and the capsule
   have not. `directRotAngle` has moved by the angle the Mun turns in an hour.
5. Repeat steps 3 and 4: at each load the rocks turn a little further, by the same angle as
   `directRotAngle`.

The Mun turns once in 138,984 s: 9.3° for an hour of game time, 1.6° for ten minutes played in real time.
Saving and loading straight away turns nothing, and neither does time going by while nothing is loaded:
only loading an older save does, or starting KSP again (see [The change](the-change.md#why-the-rocks-turn)).

**By script**: `automation/run-rocks-turning.py` (*not written yet*: see
[Work in progress](work-in-progress.md#the-rocks-around-a-craft)). Steps 1 to 5, twelve times over,
with a screenshot of each view and the line of Diag Floating Origin at each load; it compares each view
to the first one, to sort the runs where nothing turned from the others. The screenshots are the result.

## A kerbal on a rock is moved

**The install**: [the install](README.md#the-builds-and-the-install) with the **release** build,
[KSP Diag - Floating Origin](https://github.com/lhervier/KSP-Diag-FloatingOrigin),
[KSP Diag - Landed Vessel](https://github.com/lhervier/KSP-Diag-LandedVessel) and
[KSP Diag - Terrain Height](https://github.com/lhervier/KSP-Diag-TerrainHeight). After a load, Diag
Landed Vessel shows how far the kerbal moved from where the save left him, once settled; Diag Terrain
Height, the height of the surface he stands on above the ground of the terrain, which is the top of the
rock under him.

**The save** is a kerbal on EVA standing on a rock, saved **with the same build** as the one it is loaded
with: the change gives every rock another orientation than the release does (see
[Work in progress](work-in-progress.md#a-kerbal-on-a-rock)). It is made so that the first load of a new
session puts the rock where it was when the save was made: the `UT` of the save is moved back by the
time KSP had kept in `InverseRotAngle` (see [Making the save](#making-the-save)).

**Why a kerbal.** At every load, KSP puts a craft of a single part, a kerbal on EVA among others, back
down on the first collider a ray cast from 500 m above it meets (`Vessel.CheckGroundCollision`). A kerbal
on a rock that did not turn is put back where he was; on a rock that turned, he is put back on whatever
the rock now has under him. A craft of several parts is not put back down: it starts where the save left
it, while the rock follows its terrain quad, which stock KSP builds a few centimetres higher or lower at
each load ([Why it is different at every load](https://github.com/lhervier/KSP-TerrainPrecisionFix/blob/main/docs/the-culprit-ground.md#why-it-is-different-at-every-load)).
Such a craft can start slightly inside its rock and jump, with the change as without it: a defect of
stock KSP, not this one.

**By hand**:

1. Start KSP, copy the save into the folder of a sandbox game and load it. Wait for the digits of Diag
   Landed Vessel to stop moving, then press *Record* in the three windows: the kerbal is on his rock, and
   has hardly moved.
2. Let an hour of game time go by: time warp ×100 on rails for about 36 seconds.
3. Load **the same save** again and record: the rock has turned under the kerbal, and KSP has put him
   back on what the rock now has under him: higher, lower, on a slope he slides down, or on the ground
   beside it. Diag Terrain Height shows another surface under him, Diag Landed Vessel how far he moved.
4. Quit KSP, start it again, load the save and record: the kerbal is back on his rock as at step 1.

Ten minutes played instead of the hour of step 2 already turn the rock by 1.6°. A craft of several parts
on a rock that turned starts inside it, and the physics engine throws it out: the behaviour reported to
Parallax Continued in [issue #125](https://github.com/Gameslinx/Parallax-Continued/issues/125), *Mun
Surface Scatter Devoured/Torn Apart Small Vessel Upon Game Relaunch*. In a game played normally, the save
is loaded after a restart of KSP, in a session that has not played the same time as the one the save was
made in.

**By script**: `automation/run-kerbal-on-a-rock.py` (*not written yet*). Twelve loads after an hour of
time warp each, then KSP started again and twelve loads more; at each load, the three instruments
recorded after the digits stop moving, and a view of the kerbal.

### Making the save

1. Start KSP and load [`rocks-mun.sfs`](saves/rocks-mun.sfs). Send the kerbal on EVA, put him just above
   the top of a rock with *Set Position* of the `Alt+F12` menu, and let him settle on a part of the rock
   flat enough that he does not slide.
2. Read `InverseRotAngle` in Diag Floating Origin, and save.
3. In the `.sfs`, in `FLIGHTSTATE`, lower `UT` by `InverseRotAngle / 360 × 138984` seconds (the angle
   taken between 0 and 360).

At the first load of a new session, `InverseRotAngle` is 0, and the Mun is turned as it was when the save
was made. *Not checked yet*: [Work in progress](work-in-progress.md#a-kerbal-on-a-rock).
