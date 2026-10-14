# Non-regression tests: a save made with the release, loaded with the change

Part of [Scatter rotation](../README.md), one chapter of [Non-regression tests](../non-regression.md): what a player sees when updating to the change, and why it is not a test.

**Nothing new for a player.** At the first load with the change, every rock takes the orientation the
change gives it, tied to its quad, and a craft saved on a rock, or right next to one, can start inside
it, once. With Parallax Continued 1.0.4 as released, that already happens at every load: each rock comes
back turned by the body's rotation over the time played since the save, an angle that depends on how the
game was played, so any angle ([The change](../the-change.md#why-the-rocks-turn)). Updating to the change
turns the rocks once more, by another such angle, and never again after. Not a test: no protocol could
tell this load from any other load of the release.
