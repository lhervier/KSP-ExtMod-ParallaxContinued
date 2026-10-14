# Work in progress

Part of [Scatter rotation](README.md): what is still to check before the change can be offered. Each
point says what a player would see if the change broke something, how to play it, what its script needs,
and where it stands. A point moves to [Non-regression tests](non-regression.md) once complete.

## Summary

- **The protocols played by script** — both protocols of [Reproducing the bug](reproducing-the-bug.md),
  on both builds, without any other mod; seen once without the change and with it, with another mod
  installed.
- **A save of a craft on a rock** — the save of *A craft on a rock is thrown off*, one made without the
  change and one with it, by the procedure that moves its `UT` back, itself to check.
- **The colliders on the rocks drawn** — with the change, the collider of each rock keeps the orientation
  of the rock drawn, at every load.
- **A craft saved with the release, loaded with the change** — the one load at which every rock takes its
  new orientation.
- **The scatters along the radius: the trees of Kerbin** — the other branch of `alignToTerrainNormal`.
- **Eve** — both branches of `alignToTerrainNormal` on one body.
- **The poles** — where `FromToRotation` has no single answer, without the change and with it.
- **The other ways the body is turned in the scene** — above the rotating-frame altitude and back, a
  change of sphere of influence, a flight opened from the space centre or the tracking station.
- **OpenGL** — the GLSL variant of the compute shader.
- **Performance** — the time of a frame in a dense scatter, without the change and with it.
- **Out of reach** — macOS, Linux under Vulkan, mods that change the scale of the bodies.

## The protocols played by script

**If the change broke it**: the rocks of **release + change** would still turn, and the protocols would
no longer tell the bug from the change.

**To play**: [The rocks turn at every load](reproducing-the-bug.md#the-rocks-turn-at-every-load) and
[A craft on a rock is thrown off](reproducing-the-bug.md#a-craft-on-a-rock-is-thrown-off), on both
builds, on [the install](README.md#the-builds-and-the-install).

**Script**: `automation/run-rocks-turning.py` and `automation/run-craft-on-a-rock.py`, to write. Tools of
KSP-MCPServer: `load_save`, `warp_to` (check the time after it: it does not report a warp that did not
happen, as when the craft is moving), `set_ui`, `set_camera`, `screenshot`, `quit_game`; of the
instruments: `floatingorigin_record`, `landedvessel_read` and `landedvessel_record`,
`terrainheight_record`, the `_show_window` of each. Starting KSP again is up to the script, outside the
server.

**Where it stands**: both protocols were played on the Mun without the change and with it: without the
change, the rocks turn at every load by the angle of the Mun and a capsule on a rock is thrown off; with
it, the rocks do not move and the capsule stays on its rock through twelve loads after an hour of time
warp each, then twelve loads after a restart of KSP. Those runs had Terrain Precision Fix installed, and
some of their readings came from outside the instruments: they are to play again on the install, by the
scripts.

## A save of a craft on a rock

**Why**: a save of a craft on a rock only holds with a build that orients that rock the same way, and the
change gives every rock a new orientation
([A craft saved with the release, loaded with the change](#a-craft-saved-with-the-release-loaded-with-the-change)):
one save made with **release**, one with **release + change**.

**To play**: [Making the save](reproducing-the-bug.md#making-the-save), by hand: placing a craft on a rock
takes an eye. Then check that the first load of a new session leaves the capsule on its rock, Diag Landed
Vessel showing it has hardly moved: that checks the `UT` moved back by `InverseRotAngle`. With the change,
the orientation of the rocks no longer depends on that angle, and the save holds without it.

**Where it stands**: a save made with **release + change**, with Terrain Precision Fix installed, holds
its capsule; to check without Terrain Precision Fix, which moves the ground a few centimetres. No save
yet with **release**. The procedure that moves the `UT` back has not been tried.

## The colliders on the rocks drawn

**If the change broke it**: a craft would hit a rock where none is drawn, or go through one that is; the
outline Diag Colliders draws around each rock would not match the rock.

**To play**: [the install](README.md#the-builds-and-the-install) with
[KSP Diag - Colliders](https://github.com/lhervier/KSP-Diag-Colliders). Load a save of a craft standing
among rocks with colliders, look at the rocks next to it from some 12 m, slightly from above, and take a
screenshot; time warp an hour, load the same save again, take the same screenshot; then KSP started again,
the same. On every screenshot, the coloured outlines of the colliders follow the rocks drawn. On both
builds: without the change, they follow the rocks too, as both turn together.

**Script**: `automation/run-colliders-on-rocks.py`, to write; the tools of
[The protocols played by script](#the-protocols-played-by-script), `colliders_show_window`,
`colliders_set_display`.

**Where it stands**: played once on **release + change**, with Terrain Precision Fix installed, at the
`UT` of a save and an hour and forty minutes later: the outlines follow the rocks at both dates, as on the
release. The largest blocks have no outline with the change and without it: no collider.

## A craft saved with the release, loaded with the change

**If it goes wrong**: a player who updates Parallax with the change, and loads a base built on a rock or
right next to one, finds it thrown off once, at that first load.

**To play**: the save of a capsule on a rock made with **release**
([A save of a craft on a rock](#a-save-of-a-craft-on-a-rock)), loaded with **release + change**, then
again in the same session, then after a restart. Expected from the code: the rock turns once, at the
first load, and never after; the capsule may be thrown off at that load, and stays where it lands
afterwards. What to say to players depends on it.

**Script**: `automation/run-craft-on-a-rock.py`, with the save and the build given apart.

**Where it stands**: deduced, not tried.

## The scatters along the radius: the trees of Kerbin

**If the change broke it**: the trees, and the other objects that stand along the radius of the body
rather than on the slope of the ground, would lean, turn at every load, or have their colliders apart
from what is drawn.

**Why**: with `alignToTerrainNormal = False`, the normal is the direction of the body's centre, not the
terrain's: the other branch of the code, before the change brings it into the quad's frame. The stock
configs set it on Kerbin, Laythe and Eve, with colliders on Kerbin and Laythe.

**To play**: the protocols of [The protocols played by script](#the-protocols-played-by-script) and
[The colliders on the rocks drawn](#the-colliders-on-the-rocks-drawn) on Kerbin, a craft standing among
trees, seen from the side as well as from above: a tree leaning shows from the side.

**Script**: the same scripts, with another save; `rocks-kerbin-trees.sfs` to make.

**Where it stands**: not played.

## Eve

**If the change broke it**: the vegetation and the rocks of Eve, mixed on one body with both branches of
`alignToTerrainNormal`, would turn, lean or lose their colliders.

**To play**: as [The scatters along the radius: the trees of Kerbin](#the-scatters-along-the-radius-the-trees-of-kerbin),
on Eve, among its vegetation and among its rocks.

**Where it stands**: not played.

## The poles

**If the change broke it**: near a point where the normal points down the `up` axis, the objects would
flip, spin, or vanish, drawn or collider.

**Why**: `FromToRotation(up, n)` has no single answer when `n` points straight down `up`. Without the
change, `up` is the axis of the scene, so this is the south pole of the body; with it, `up` is the Y axis of
each quad, and where that points depends on how KSP orients its quads.

**To play**: both poles of the Mun, a craft put down among rocks with *Set Position*, seen from above, on
**release** and **release + change**; then, if the Y axis of the quads does not point outwards everywhere,
the place where it points inwards.

**Script**: `set_position` puts the craft down; then the steps of
[The rocks turn at every load](reproducing-the-bug.md#the-rocks-turn-at-every-load).

**Where it stands**: not played. How KSP orients its quads is to read first.

## The other ways the body is turned in the scene

**If the change broke it**: the rocks would turn, or their colliders would part from the drawn rocks,
after one of the moments KSP turns the body again in the scene without a load.

**Why**: KSP stops holding the body still above its rotating-frame altitude (100 km on the Mun), and when
the body the craft is near changes. With the change, the orientation no longer depends on the body's angle
in the scene; without it, the drawn rocks would turn at once, and the colliders built before would keep
their old orientation, parted from the drawing.

**To play**, from the save of a craft among rocks, each time with a screenshot from above and Diag
Colliders before and after, and Diag Floating Origin recording the frame and `directRotAngle`:

1. a second craft of the save, landed among the rocks, the first one sent above 100 km and brought back,
   or the switch to a craft in orbit and back;
2. a change of sphere of influence and back;
3. the flight opened again from the space centre, and from the tracking station.

**Script**: `set_orbit`, `switch_vessel`, `go_to_scene`, `fly_vessel`; a save with two crafts to make.

**Where it stands**: not played. That the body stops being held still in those cases is read in the code
of KSP, not seen.

## OpenGL

**If the change broke it**: under OpenGL, the rocks would be drawn wrong, or not at all, or still turn.

**Why**: KSP started with `-force-glcore` on Windows loads the `-linux` bundle of Parallax, its GLSL
variant, the one players get on Linux under OpenGL. The change is in the HLSL source, compiled to GLSL by
Unity: another compiler, another result to see. Proton presents itself as Windows and loads the `-windows`
bundle, the one of the other tests.

**To play**: [The rocks turn at every load](reproducing-the-bug.md#the-rocks-turn-at-every-load), KSP
started with `-force-glcore`, on **release** and **release + change**.

**Where it stands**: not played.

## Performance

**If the change broke it**: a lower frame rate in a dense scatter (the grass of Kerbin, for instance).

**Why**: the change adds, in each call of `GetTRSMatrix`, a matrix product and a transpose for every
object drawn, at every frame.

**To play**: the time of a frame in a dense scatter, the same view, on **release** and
**release + change**. The instrument is to choose.

**Where it stands**: not played.

## Out of reach

Not tested, and said as such when the change is offered:

- **macOS** (the Metal variant of the `-macosx` bundle) and **Linux under Vulkan** (the SPIR-V variant of
  the `-linux` bundle): built, never run;
- **mods that change the scale of the bodies** (Sigma Dimensions among them): the change assumes the scale
  of a quad is the same along its three axes.
