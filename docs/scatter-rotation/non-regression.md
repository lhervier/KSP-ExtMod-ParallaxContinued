# Non-regression tests

Part of [Scatter rotation](README.md): what the change has been checked against, and what it gave.

**One test is complete**: [The rocks around a craft](#the-rocks-around-a-craft). What is still to play is
in [Work in progress](work-in-progress.md).

## What makes a test complete

A test moves here from [Work in progress](work-in-progress.md) once:

- wherever it shows rocks with colliders, it shows them with
  [KSP Diag - Colliders](https://github.com/lhervier/KSP-Diag-Colliders), which outlines in colour the
  collider Parallax gives each rock near a craft, and on every screenshot those outlines follow the
  rocks drawn: otherwise a craft would hit a rock where none is drawn, or go through one that is.
  Without the change they do too, as the rock drawn and its collider turn together. Scripts show that
  drawing with `colliders_show_window` and `colliders_set_display`;
- its protocol can be played by hand, from a save published next to it, and says what to look at;
- it has been played on [the install](README.md#the-builds-and-the-install), without any other mod, on
  both builds, **release** and **release + change**;
- its result comes from what a player sees, screenshots included, or from the window of one of the
  instruments named in the install: nothing that only a script can read;
- it is played by a script of `automation/`, so that it can be played again on every new version of the
  change; the script drives KSP through
  [KSP-MCPServer](https://github.com/lhervier/KSP-MCPServer), with Python 3 alone, and only presses
  what a player would press;
- its screenshots and the `KSP.log` of each run are published with it.

## The rocks around a craft

**If the change broke it**: the rocks of **release + change** would still turn at a load, or would be
drawn wrong.

**To play**: [The rocks turn at every load](reproducing-the-bug.md#the-rocks-turn-at-every-load) and
[With the change, the rocks hold still](reproducing-the-bug.md#with-the-change-the-rocks-hold-still):
a kerbal on the ground, a few metres from the nearest rocks, far enough that no rock reaches him as it
turns, near enough to see them. On the Mun, where every scatter with a collider is a rock; on Eve, where
vegetation without colliders grows among the rocks. The configuration of Eve has scatters aligned on the
terrain and others standing along the radius (`alignToTerrainNormal`); which of them grow in this view is
not checked: [The scatters along the radius](work-in-progress.md#the-scatters-along-the-radius-the-trees-of-kerbin)
looks at that branch on its own.

**Script**: [`automation/run-rocks-turning.py`](automation/run-rocks-turning.py). Tools of KSP-MCPServer:
`load_save`, `warp_to` (the script checks the time after it: it does not report a warp that did not
happen), `get_state`, `set_ui`, `set_camera`, `wait`, `screenshot`; of the instruments:
`floatingorigin_record`, and the `_show_window` of each.

**Saves**: [`rocks-mun-jeb.sfs`](saves/rocks-mun-jeb.sfs), [`rocks-eve-jeb.sfs`](saves/rocks-eve-jeb.sfs).

**No collider in this test.** Parallax gives a rock a collider only when it comes within the size of a
craft plus its own size (`SqrDistanceToNearestCraft`); a kerbal a few metres from the nearest rock gets
none, and KSP Diag - Colliders draws only the grey edges of the quads. That the outlines of the colliders
follow the rocks drawn is checked in the tests where a craft stands near enough to rocks to give them
colliders.

**Result**: played by the script, on [the install](README.md#the-builds-and-the-install), on both builds,
twelve loads after an hour of time warp each; the Mun turned by 112.4° in the scene (`directRotAngle`
from 37.0° to −75.4°), Eve by 194.0° (from −164.2° to 1.7°).

| body | build | what the screenshots show | animation (one load a second) | run |
|---|---|---|---|---|
| Mun | **release** | every cluster of rocks turns on itself at every load, the ground, the edges of the quads and the kerbal holding still | [GIF](runs/rocks-mun-jeb/release/rocks-mun-jeb-release.gif), [MP4](runs/rocks-mun-jeb/release/rocks-mun-jeb-release.mp4) | [`release/`](runs/rocks-mun-jeb/release/) |
| Mun | **release + change** | the same rocks at every load | [GIF](runs/rocks-mun-jeb/change/rocks-mun-jeb-change.gif), [MP4](runs/rocks-mun-jeb/change/rocks-mun-jeb-change.mp4) | [`change/`](runs/rocks-mun-jeb/change/) |
| Eve | **release** | the rocks and the plants turn, each on itself, at every load | [GIF](runs/rocks-eve-jeb/release/rocks-eve-jeb-release.gif), [MP4](runs/rocks-eve-jeb/release/rocks-eve-jeb-release.mp4) | [`release/`](runs/rocks-eve-jeb/release/) |
| Eve | **release + change** | the same rocks and plants at every load ([what changes all the same](reproducing-the-bug.md#on-eve-what-changes-at-every-load-all-the-same)) | [GIF](runs/rocks-eve-jeb/change/rocks-eve-jeb-change.gif), [MP4](runs/rocks-eve-jeb/change/rocks-eve-jeb-change.mp4) | [`change/`](runs/rocks-eve-jeb/change/) |

On every run, the hour of time warp alone turns nothing (`warp-NN` against `load-NN` before it), and the
kerbal stays `LANDED` where the save left him, within 6 mm. With the change, nothing turns; what still
changes from one load to the next, the texture of the ground and a plant that shows on some loads only,
does so with the release too and does not come from this bug
([On Eve, what changes at every load all the same](reproducing-the-bug.md#on-eve-what-changes-at-every-load-all-the-same)). Each folder holds the
screenshots (`load-NN` after each load, `warp-NN` before it), the line of KSP Diag - Floating Origin at
each of them (`readings.json`), what the script printed (`output.txt`) and the `KSP.log` of the session.
The first screenshot with the change shows other orientations than the first one of the release: the
change turns every rock once
([A save made with the release, loaded with the change](#a-save-made-with-the-release-loaded-with-the-change)).

## A save made with the release, loaded with the change

**Nothing new for a player.** At the first load with the change, every rock takes the orientation the
change gives it, tied to its quad, and a craft saved on a rock, or right next to one, can start inside
it, once. With Parallax Continued 1.0.4 as released, that already happens at every load: each rock comes
back turned by the body's rotation over the time played since the save, an angle that depends on how the
game was played, so any angle ([The change](the-change.md#why-the-rocks-turn)). Updating to the change
turns the rocks once more, by another such angle, and never again after. Not a test: no protocol could
tell this load from any other load of the release.
