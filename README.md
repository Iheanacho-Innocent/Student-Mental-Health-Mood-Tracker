# Student Mental Health — Mood Tracker
### Built by Innocent Emeka Iheanacho | Ulster University | MSc International Business with Data Analytics

# Student-Mental-Health-Mood-Tracker
This is a command-line application built in Python that allows university students living in accommodation to log their daily mood, track patterns over time, and receive gentle prompts to seek support when their mood has been consistently low.

## What is this project?

This is a command-line application built in Python that allows university students living in accommodation to log their daily mood, track patterns over time, and receive gentle prompts to seek support when their mood has been consistently low.


## Why was it built?

Student mental health is one of the most important challenges facing UK universities today. Many students experience stress, anxiety, and low mood, especially around deadlines, exams, or when living away from home for the first time.

Most mental health tools are either expensive apps or clinical platforms. This project takes a simpler approach: a lightweight, private, terminal-based tool that any student can run on their own laptop in seconds, with no account, no internet connection, and no data leaving their device.




## What does it do?

| Feature | Description |
|---|---|
| Log today's mood | Enter a score from 1 (very low) to 10 (great) with optional notes |
| View history | See your last 7 entries in a clear table |
| Weekly summary | Get your average score, best day, worst day, and trend direction |
| Mood chart | See a visual bar chart of your last 7 days printed in the terminal |
| Support alert | If your score is 4 or below for 3 days in a row, the app shows mental health support contacts |

---

## How the data is stored

Every entry is saved as one row in a file called `mood_log.csv`. This file is created automatically when you run the program for the first time. You do not need to create it yourself.

Here is what the file looks like:

```
date,time,mood_score,notes
2026-05-10,08:30,7,Felt okay after breakfast
2026-05-11,09:15,6,Bit tired from late night
2026-05-12,08:45,4,Stressed about assignment deadline
2026-05-13,09:00,3,Hardly slept. Very anxious
```

Each column means:

| Column | What it stores | Example |
|---|---|---|
| date | The date of the entry | 2026-05-13 |
| time | The time the entry was logged | 09:00 |
| mood_score | A number from 1 to 10 | 3 |
| notes | Any optional text the student added | Hardly slept |

You can open `mood_log.csv` in Microsoft Excel or Google Sheets at any time to view your full history.

---

## Requirements

- Python 3.8 or higher
- No libraries to install — the project uses only modules that come built into Python (`csv`, `os`, `datetime`)

---

## How to run it

**Step 1 — Clone or download the repository**
```bash
git clone https://github.com/Iheanacho-Innocent/ulster-mood-tracker.git
cd ulster-mood-tracker
```

**Step 2 — Run the program**
```bash
python mood_tracker.py
```

On some computers you may need to use `python3` instead of `python`.

**Step 3 — Follow the menu**
```
===============================================
  Ulster University - Student Mood Tracker
===============================================

  MENU
  ------------------------------
  [1]  Log today's mood
  [2]  View history
  [3]  Weekly summary
  [4]  Show mood chart
  [5]  Exit
  ------------------------------

  Enter 1 to 5:
```

---

## Example output

**Logging a mood (option 1)**
```
  LOG TODAY'S MOOD

  How are you feeling today? (1=very low  10=great): 3
  Any notes? (press Enter to skip): Deadline stress

  ✔  Mood score of 3/10 saved successfully!

  ⚠  Your mood has been low for 3 days in a row.
     You do not have to manage this alone.

  SUPPORT CONTACTS
  ------------------------------------------
  Ulster University Counselling : 028 9036 6369
  Student Wellbeing Portal      : my.ulster.ac.uk/wellbeing
  Samaritans (24hr, free)       : 116 123
  Crisis Text Line              : Text HELLO to 85258
  ------------------------------------------
```

**Weekly summary (option 3)**
```
  WEEKLY SUMMARY

  Days recorded : 7
  Average score : 4.9 out of 10
  Best score    : 7
  Worst score   : 3
  Weekly trend  : Going DOWN - consider talking to someone
```

**Mood chart (option 4)**
```
  MOOD CHART - Last 7 days

  2026-05-10  ███████  7
  2026-05-11  ██████  6
  2026-05-12  ████  4
  2026-05-13  ███  3
  2026-05-14  ███  3
  2026-05-15  █████  5
  2026-05-16  ██████  6
```

---

## Project structure

```
ulster-mood-tracker/
│
├── mood_tracker.py     ← the main program (all features in one file)
├── mood_log.csv        ← auto-created on first run, stores all entries
└── README.md           ← this documentation file
```

---

## How the code is organised

The program is built entirely using Python fundamentals — variables, functions, control flow (if/elif/else), and while loops. There are 8 functions in total, each with one clear job:

| Function | Job |
|---|---|
| `create_file_if_missing()` | Checks if the CSV file exists and creates it if not |
| `save_mood(mood_score, notes)` | Writes one new entry to the CSV file |
| `read_all_entries()` | Opens the CSV and returns all rows as a list |
| `log_mood()` | Asks the user for their score and notes, validates input, saves the entry |
| `check_alert(entries)` | Checks the last 3 scores and shows support contacts if all are low |
| `view_history()` | Displays the last 7 entries as a table |
| `show_chart()` | Draws a bar chart of the last 7 days using block characters |
| `weekly_summary()` | Calculates average, best, worst, and trend from the last 7 entries |

---

## Python concepts demonstrated

| Concept | Where it appears |
|---|---|
| Variables | `total`, `average`, `best`, `worst`, `score`, `notes` |
| Data types | `int` (scores), `str` (dates, notes), `list` (entries), `dict` (each row, support resources) |
| Functions | All 8 functions with clear inputs and outputs |
| While loop | Input validation in `log_mood()`, main menu loop in `main()` |
| For loop | Looping through entries in `view_history()`, `weekly_summary()`, `show_chart()` |
| If / elif / else | Menu routing in `main()`, trend logic in `weekly_summary()`, alert check in `check_alert()` |
| List slicing | `entries[-7:]` to get last 7, `entries[-3:]` to get last 3 |
| Dictionary | `SUPPORT_RESOURCES` storing service names and contacts |
| File I/O | Opening, reading, writing, and closing the CSV file |
| String methods | `.isdigit()` to validate input, `.strip()` to remove whitespace |

---

## Data science relevance

Although this is a beginner-level Python project, it demonstrates several core data science principles:

- **Data collection** — every mood entry is a structured data point with a consistent schema (date, time, score, notes)
- **Data storage** — entries persist in a flat-file database (CSV) that can be opened, analysed, or exported at any time
- **Descriptive statistics** — the weekly summary calculates mean, min, and max from a dataset
- **Trend analysis** — comparing first-half and second-half averages to detect directional change
- **Data visualisation** — the mood chart converts numerical data into a visual representation
- **Threshold-based alerting** — the support alert applies a rule-based detection method to flag anomalies (3 consecutive low scores)

These are the same operations performed at scale in health informatics research — this project demonstrates the underlying logic in its simplest form.

---

## Limitations and future improvements

| Current limitation | How it could be improved |
|---|---|
| Data stored in a local CSV | Connect to a cloud database so data persists across devices |
| No user accounts | Add login so multiple students can use the same device |
| Terminal only | Build a simple web interface using Flask |
| No data visualisation library | Add matplotlib to produce proper charts |
| Staff availability hardcoded | Pull from a live calendar API |

---

## Author

**Innocent Emeka Iheanacho**
MSc International Business with Data Analytics — Ulster University, Birmingham
[LinkedIn](https://www.linkedin.com/in/iheanacho-innocent-emeka/) | [GitHub](https://github.com/Iheanacho-Innocent)

---

## Licence

This project was built for educational purposes as part of an MSc programme at Ulster University. It is free to use, adapt, and share.
