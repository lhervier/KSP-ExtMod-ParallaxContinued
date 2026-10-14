# Non-regression tests

Part of [Scatter rotation](README.md): what the change has been checked against, and what it gave.

**No test is complete yet.** What is still to play is in [Work in progress](work-in-progress.md).

## What makes a test complete

A test moves here from [Work in progress](work-in-progress.md) once:

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
