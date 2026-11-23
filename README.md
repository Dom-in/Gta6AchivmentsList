# GTA VI achievements list

The achievement list of Grand Theft Auto VI (Xbox Series X|S) as one JSON file, for
[Leonida Launcher](https://github.com/ItsNotRexed/Leonida/pull/5859)'s Achievements page, which downloads it when the
launcher starts.

```
https://raw.githubusercontent.com/Dom-in/Gta6AchivmentsList/main/achievements.json
```

## Format

```json
{
  "game": "Grand Theft Auto VI",
  "platform": "Xbox Series X|S",
  "updated": "2026-11-23",
  "count": 55,
  "gamerscore": 1000,
  "achievements": [
    { "id": 1, "name": "…", "description": "…", "gamerscore": 5, "secret": true }
  ]
}
```

- `id`: the order the list is in, from 1. It is not Microsoft's achievement ID.
- `secret`: the achievement is hidden on Xbox until it unlocks; the launcher hides its description until you click it.

## Updating it

1. Open the game's achievements page on TrueAchievements in a browser and save it (Ctrl+S, "Webpage, complete").
2. `python -I tools/from_saved_page.py <saved page.html> achievements.json`
3. Commit `achievements.json`.

The script keeps each achievement's name, description, gamerscore and whether it is secret, and nothing else from
the page.

## Notes

- No game files are in this repository, and nothing here comes from the game's package.
- Achievement names and descriptions are Rockstar Games'. This list only collects what is publicly shown on
  achievement sites, so the launcher has something to show.
