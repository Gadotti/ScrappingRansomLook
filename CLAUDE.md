# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

A ransomware breach monitoring tool that scrapes [ransomlook.io/recent](https://www.ransomlook.io/recent), deduplicates entries against a local CSV database, filters by keyword watchlists (focused on Brazilian entities), sends email alerts on matches, and exports to SIEM-compatible CSV files.

## Running

```bash
# Install dependencies
pip install -r requirements.txt

# One-shot check
python _main.py

# Scheduled mode — runs daily at 08:00, 12:05, 18:00 (times from config)
python _main.py schedule
```

There are no automated tests; verification is manual.

## Configuration

Copy `config/appconfig-sample.json` to `config/appconfig.json` and fill in credentials. Key fields:

| Field | Purpose |
|---|---|
| `url` | Target scrape URL |
| `email.*` | SMTP credentials and recipients |
| `alert` | Enable/disable email notifications |
| `key_words_alert` | Watchlist — victim/group name substrings that trigger alerts |
| `schedule_times` | List of `"HH:MM"` strings for scheduled mode |
| `siem_breach_log_all` | Absolute path for full SIEM CSV output |
| `siem_breach_log_tag` | Absolute path for keyword-matched SIEM CSV output |

`config/appconfig.json` is gitignored; never commit it.

## Architecture

```
_main.py          — Orchestration: fetch → parse → deduplicate → alert → log
config.py         — Single function: get_config(key) reads appconfig.json
postline.py       — PostLine dataclass: parses one <tr> into date/victim/group/tags
saveresults.py    — CSV persistence + SIEM export (semicolon-delimited, ISO 8601 timestamps)
log.py            — Rotating text log (500 KB limit, auto-increments filename)
notify.py         — Keyword matcher + SMTP email sender
```

### Data flow

1. `_main.py` fetches the page with `requests`, parses the HTML table with BeautifulSoup
2. Each `<tr>` becomes a `PostLine` object
3. `saveresults.is_new_record()` checks the last 100 lines of the CSV — duplicate if date+victim+group match
4. New records are appended to the main CSV and optionally to SIEM files
5. `notify.py` scans `key_words_alert` against victim name and group name (case-insensitive substring); on match, sends one batched email per run
6. All activity is written to a rotating log via `log.py`

### Output files

All outputs land in a `source/` subdirectory (auto-created) by default, except `siem_breach_log_*` paths which are absolute and point to an external dashboard directory.

- `source/ransomlook_posts.csv` — master dedup database; semicolon-delimited: `date;victim;group;tags`
- `source/ransomlook_posts_log_N.txt` — rotating human-readable log
- SIEM CSVs — consumed by an external PowerBI/dashboard at the configured absolute paths
