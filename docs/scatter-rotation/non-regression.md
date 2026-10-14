# Non-regression tests

Part of [Scatter rotation](README.md): what the change has been checked against, and what it gave.
[Reproducing the bug](reproducing-the-bug.md) shows that with the change, the rocks, the plants and the
cacti no longer turn at a load; the tests here look at whether the change breaks anything else in the
game. What is still to play is in [Work in progress](work-in-progress.md). Each test has a page of its own.

## What makes a test complete

A test moves here from [Work in progress](work-in-progress.md) once:

- wherever it shows rocks with colliders, it shows them with
  [KSP Diag - Colliders](https://github.com/lhervier/KSP-Diag-Colliders), which outlines in colour the
  collider Parallax gives each rock near a craft, and on every screenshot those outlines follow the
  rocks drawn: otherwise a craft would hit a rock where none is drawn, or go through one that is.
  Without the change they do too, as the rock drawn and its collider turn together. Scripts show that
  drawing with `colliders_show_window` and `colliders_set_display`;
- its protocol can be played by hand, from a save published next to it, and says what to look at;
- it has been played on [the install](README.md#the-builds-and-the-install), without any other mod, with
  the **release + change** build, and with the **release** build too wherever the test means something
  there: a test that needs the scatter to stay where the save left it cannot be played on the release,
  where it turns at every load;
- its result comes from what a player sees, screenshots included, or from the window of one of the
  instruments named in the install: nothing that only a script can read;
- it is played by a script of `automation/`, so that it can be played again on every new version of the
  change; the script drives KSP through
  [KSP-MCPServer](https://github.com/lhervier/KSP-MCPServer), with Python 3 alone, and only presses
  what a player would press;
- its screenshots and the `KSP.log` of each run are published with it.

## The colliders on the scatter

With the change, the colliders Parallax gives the scatter near a craft stay on the objects drawn, load
after load: on the Mun among rocks, on Eve among rocks and plants without colliders, on Kerbin in a
cluster of cacti, which stand along the radius of the body. Played with release + change only: on the
release, the scatter turns at every load, and the test means nothing there.

**→ Full chapter: [Non-regression tests: the colliders on the scatter](non-regression/the-colliders-on-the-scatter.md)**

## A save made with the release, loaded with the change

Nothing new for a player: at the first load with the change, every rock turns once more, as it already
does at every load of the release, and never again after. Not a test.

**→ Full chapter: [Non-regression tests: a save made with the release, loaded with the change](non-regression/a-save-made-with-the-release.md)**
