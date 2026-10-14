# Non-regression tests

Part of [Scatter rotation](README.md): what the change has been checked against, and what it gave.

**No test is complete yet.** What is still to play is in [Work in progress](work-in-progress.md).

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

## A save made with the release, loaded with the change

**Nothing new for a player.** At the first load with the change, every rock takes the orientation the
change gives it, tied to its quad, and a craft saved on a rock, or right next to one, can start inside
it, once. With Parallax Continued 1.0.4 as released, that already happens at every load: each rock comes
back turned by the body's rotation over the time played since the save, an angle that depends on how the
game was played, so any angle ([The change](the-change.md#why-the-rocks-turn)). Updating to the change
turns the rocks once more, by another such angle, and never again after. Not a test: no protocol could
tell this load from any other load of the release.
