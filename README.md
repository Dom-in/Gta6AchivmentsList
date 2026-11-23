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
    { "id": 1, "name": "…", "description": "…", "gamerscore": 5, "secret": true,
      "image": "https://img.xboxachievements.com/…-lo.jpg" }
  ]
}
```

- `id`: the order the list is in, from 1. It is not Microsoft's achievement ID.
- `secret`: the achievement is hidden on Xbox until it unlocks; the launcher hides its description until you click it.
- `image`: where the achievement's picture is, on XboxAchievements.com's image server. The pictures are not stored
  in this repository; the launcher downloads them from there and keeps a copy on the PC.

## Updating it

1. Open the game's achievements page on XboxAchievements.com in a browser and save it (Ctrl+S).
2. `python -I tools/from_xboxachievements.py "<saved page>.html" achievements.json`
3. Commit `achievements.json`.

The script keeps each achievement's name, description, gamerscore, whether it is secret and its picture's address,
and nothing else from the page. `tools/from_saved_page.py` does the same from a saved TrueAchievements page (without
pictures); on 2026-11-23 the two sites agreed on all 55 names, descriptions, gamerscores and secrets.

## Notes

- No game files are in this repository, and nothing here comes from the game's package.
- Achievement names, descriptions and pictures are Rockstar Games'. This list only collects what is publicly shown on
  achievement sites, so the launcher has something to show.
