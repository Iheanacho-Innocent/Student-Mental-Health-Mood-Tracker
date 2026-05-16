# ============================================================
#  PROJECT  : Student Mental Health - Mood Tracker
#  AUTHOR   : Innocent Emeka Iheanacho
#  VERSION  : 1.0.0
#  DATE     : May 2026
#  CONTEXT  : Built as part of an MSc in International Business
#             with Data Analytics at Ulster University.
#             Designed to support student wellbeing by tracking
#             daily mood and flagging when support may be needed.
# ============================================================

# --- WHY THESE IMPORTS? --------------------------------------
# csv      : lets Python read and write the CSV file that stores
#            all mood entries. Without this we cannot save data.
# os       : lets Python check whether the CSV file already
#            exists on the computer before trying to open it.
# datetime : gives Python access to the current date and time
#            so every entry is automatically time-stamped.
# -------------------------------------------------------------
import csv
import os
import datetime


# --- CONSTANTS -----------------------------------------------
# A constant is a variable whose value we do not change while
# the program is running. Writing them here at the top means
# if we ever want to update them (e.g. change the alert
# threshold from 4 to 3) we only change one line, not ten.
# -------------------------------------------------------------

# The name of the file where all mood entries are saved
FILE_NAME = "mood_log.csv"

# Any mood score at or below this number is considered low
LOW_SCORE_THRESHOLD = 4

# How many days in a row of low scores before we show an alert
ALERT_WINDOW = 3

# How many past entries to show in the history view
HISTORY_LIMIT = 7

# A dictionary of mental health support services.
# Format is: "Name of service" : "Contact detail"
# Add or remove services here without touching any other code.
SUPPORT_RESOURCES = {
    "Ulster University Counselling": "028 9036 6369",
    "Student Wellbeing Portal"     : "my.ulster.ac.uk/wellbeing",
    "Samaritans (24hr, free)"      : "116 123",
    "Crisis Text Line"             : "Text HELLO to 85258",
}

# The column names that appear as the first row in the CSV file.
# Every entry saved must follow this exact order.
CSV_HEADERS = ["date", "time", "mood_score", "notes"]


# ============================================================
# FUNCTION 1 OF 8 : create_file_if_missing()
#
# PURPOSE:
#   When the program runs for the very first time there is no
#   CSV file yet. This function checks for the file and creates
#   it if it is missing, so no other function ever crashes
#   trying to open a file that does not exist.
#
# HOW IT WORKS:
#   - os.path.exists() returns True if the file is found, or
#     False if it is not.
#   - If the file is already there we do nothing (return early).
#   - If it is missing we open a new file, write the header
#     row (the column names), then close the file.
#
# WHEN IT IS CALLED:
#   Once, at the very start of main() before anything else runs.
# ============================================================
def create_file_if_missing():

    # If the file already exists, stop here and do nothing
    if os.path.exists(FILE_NAME):
        return

    # File does not exist - create it and write the header row
    file = open(FILE_NAME, "w", newline="")
    writer = csv.writer(file)
    writer.writerow(CSV_HEADERS)
    file.close()

    print("  New mood log created. Ready to use!")


# ============================================================
# FUNCTION 2 OF 8 : save_mood(mood_score, notes)
#
# PURPOSE:
#   Writes one new row to the CSV file containing the current
#   date, current time, the mood score, and any notes.
#
# PARAMETERS (the values passed in when calling this function):
#   mood_score (int) : a number from 1 to 10 entered by the user
#   notes      (str) : optional text the user types, can be empty
#
# HOW IT WORKS:
#   - Gets today's date and current time from Python's clock.
#   - Opens the CSV file in "append" mode ("a"), which means
#     it adds a new line at the end without deleting old data.
#   - Writes one row with four values: date, time, score, notes.
#   - Closes the file so the data is properly saved to disk.
#
# WHEN IT IS CALLED:
#   Inside log_mood(), after the user has entered a valid score.
# ============================================================
def save_mood(mood_score, notes):

    # Get the current date as text e.g. "2026-05-16"
    date_text = datetime.date.today().strftime("%Y-%m-%d")

    # Get the current time as text e.g. "09:45"
    time_text = datetime.datetime.now().strftime("%H:%M")

    # Open the file in append mode so we add to it, not overwrite
    file = open(FILE_NAME, "a", newline="")
    writer = csv.writer(file)

    # Write one row: [date, time, mood_score, notes]
    writer.writerow([date_text, time_text, mood_score, notes])

    file.close()


# ============================================================
# FUNCTION 3 OF 8 : read_all_entries()
#
# PURPOSE:
#   Opens the CSV file and loads every row into a list so the
#   rest of the program can work with the data.
#
# RETURNS:
#   A list of dictionaries. Each dictionary is one row from the
#   CSV file. Example of one item in the list:
#   {
#     "date"       : "2026-05-15",
#     "time"       : "09:30",
#     "mood_score" : "6",
#     "notes"      : "Feeling okay today"
#   }
#
# HOW IT WORKS:
#   - Opens the file in read mode ("r").
#   - csv.DictReader reads each row and automatically uses the
#     header row as the key names for each dictionary.
#   - We loop through every row and add it to our list.
#   - We return the completed list.
#
# WHEN IT IS CALLED:
#   By view_history(), weekly_summary(), show_chart(), and
#   check_alert() - any function that needs the stored data.
# ============================================================
def read_all_entries():

    # Start with an empty list
    entries = []

    # Open the file for reading
    file = open(FILE_NAME, "r")
    reader = csv.DictReader(file)

    # Go through every row and add it to our list
    for row in reader:
        entries.append(row)

    file.close()

    # Hand the list back to whoever called this function
    return entries


# ============================================================
# FUNCTION 4 OF 8 : log_mood()
#
# PURPOSE:
#   The main check-in feature. Asks the student to rate their
#   mood from 1 to 10, optionally add notes, then saves the
#   entry. It also checks whether a support alert is needed.
#
# HOW IT WORKS:
#   - Uses a while loop to keep asking for a score until the
#     user enters a valid whole number between 1 and 10.
#   - score.isdigit() checks the input contains only digits
#     (no letters or symbols).
#   - int(score) converts the text "7" into the number 7 so
#     we can do arithmetic with it later.
#   - Notes are optional - pressing Enter saves an empty string.
#   - Calls save_mood() to write to the file.
#   - Reloads the entries and calls check_alert() to see if
#     the last 3 scores have all been low.
#
# WHEN IT IS CALLED:
#   From main() when the user chooses option 1.
# ============================================================
def log_mood():

    print()
    print("=" * 47)
    print("  LOG TODAY'S MOOD")
    print("=" * 47)

    # Keep asking until we get a valid score
    while True:
        score = input("\n  How are you feeling today? (1=very low  10=great): ")

        # Check it is a number
        if score.isdigit():
            score = int(score)   # convert text to integer

            # Check it is within the 1-10 range
            if score >= 1 and score <= 10:
                break            # valid - exit the loop
            else:
                print("  Please enter a number between 1 and 10.")
        else:
            print("  That is not a number. Please try again.")

    # Notes are optional - empty string is fine
    notes = input("  Any notes? (press Enter to skip): ")

    # Save to the CSV file
    save_mood(score, notes)

    print("\n  ✔  Mood score of " + str(score) + "/10 saved successfully!")

    # Reload all entries and check whether an alert is needed
    entries = read_all_entries()
    check_alert(entries)


# ============================================================
# FUNCTION 5 OF 8 : check_alert(entries)
#
# PURPOSE:
#   Looks at the last 3 mood scores. If all 3 are at or below
#   the LOW_SCORE_THRESHOLD (4), it prints a supportive message
#   and lists mental health support contacts.
#
# PARAMETER:
#   entries (list) : the full list of entries from read_all_entries()
#
# HOW IT WORKS:
#   - First checks there are at least 3 entries. If not, we
#     cannot check 3 scores so we stop early.
#   - entries[-3:] is Python's way of getting the last 3 items
#     in a list. The minus sign means "count from the end".
#   - We read each score out individually and compare to 4.
#   - If all 3 are low we print the alert and loop through
#     the SUPPORT_RESOURCES dictionary to display each contact.
#
# WHEN IT IS CALLED:
#   After log_mood() saves a new entry, and at the end of
#   weekly_summary() as an extra safety check.
# ============================================================
def check_alert(entries):

    # Need at least 3 entries to compare
    if len(entries) < ALERT_WINDOW:
        return

    # Get the last 3 entries from the list
    last_3 = entries[-3:]

    # Pull out each score individually and convert to integer
    score_1 = int(last_3[0]["mood_score"])
    score_2 = int(last_3[1]["mood_score"])
    score_3 = int(last_3[2]["mood_score"])

    # If all 3 scores are low, show the support message
    if score_1 <= LOW_SCORE_THRESHOLD and score_2 <= LOW_SCORE_THRESHOLD and score_3 <= LOW_SCORE_THRESHOLD:

        print()
        print("  ⚠  Your mood has been low for 3 days in a row.")
        print("     You do not have to manage this alone.")
        print()
        print("  SUPPORT CONTACTS")
        print("  " + "-" * 42)

        # Loop through the dictionary and print each service
        for service in SUPPORT_RESOURCES:
            contact = SUPPORT_RESOURCES[service]
            print("  " + service + " : " + contact)

        print("  " + "-" * 42)


# ============================================================
# FUNCTION 6 OF 8 : view_history()
#
# PURPOSE:
#   Displays the last 7 mood entries as a simple table so the
#   student can see how their mood has changed over time.
#
# HOW IT WORKS:
#   - Calls read_all_entries() to get the full list.
#   - Uses list slicing (entries[-7:]) to get the last 7 only.
#   - Loops through each entry and prints the four values in
#     a neat row: date, time, score, notes.
#
# WHEN IT IS CALLED:
#   From main() when the user chooses option 2.
# ============================================================
def view_history():

    print()
    print("=" * 47)
    print("  MOOD HISTORY - Last 7 entries")
    print("=" * 47)

    entries = read_all_entries()

    # Handle the case where no entries have been saved yet
    if len(entries) == 0:
        print("\n  No entries yet. Go to option 1 to log your first mood!")
        return

    # Get the last 7 entries only
    last_7 = entries[-7:]

    # Print a table header
    print()
    print("  Date          Time    Score   Notes")
    print("  " + "-" * 44)

    # Print each entry as one row in the table
    for entry in last_7:
        date  = entry["date"]
        time  = entry["time"]
        score = entry["mood_score"]
        notes = entry["notes"]

        print("  " + date + "  " + time + "  " + score + "       " + notes)


# ============================================================
# FUNCTION 7 OF 8 : show_chart()
#
# PURPOSE:
#   Draws a simple visual bar chart in the terminal using block
#   characters (█). Each day gets one row; the length of the
#   bar represents the mood score for that day.
#   This turns raw numbers into something visual - a core
#   data science skill called data visualisation.
#
# HOW IT WORKS:
#   - Loads the last 7 entries.
#   - For each entry, multiplies the "█" character by the score.
#     A score of 7 gives "███████", a score of 3 gives "███".
#   - Prints the date, bar, and number on one line.
#
# WHEN IT IS CALLED:
#   From main() when the user chooses option 4.
# ============================================================
def show_chart():

    print()
    print("=" * 47)
    print("  MOOD CHART - Last 7 days")
    print("=" * 47)

    entries = read_all_entries()

    if len(entries) == 0:
        print("\n  No entries to display yet.")
        return

    # Get the last 7 entries
    last_7 = entries[-7:]

    print()

    for entry in last_7:
        date  = entry["date"]
        score = int(entry["mood_score"])   # must be int for multiplication

        # "█" * 7 produces "███████" - one block per mood point
        bar = "█" * score

        print("  " + date + "  " + bar + "  " + str(score))

    print()


# ============================================================
# FUNCTION 8 OF 8 : weekly_summary()
#
# PURPOSE:
#   Analyses the last 7 entries and produces a statistical
#   summary: average score, best day, worst day, and a trend
#   showing whether mood is improving or declining.
#   This is the analytical core of the project - turning a
#   list of numbers into meaningful insight.
#
# HOW IT WORKS:
#   AVERAGE  - adds all scores together then divides by count.
#   BEST     - loops through all scores keeping track of the
#              highest seen so far.
#   WORST    - same but keeps track of the lowest seen.
#   TREND    - splits the entries into first half and second
#              half, calculates an average for each, then
#              compares them. If the second half average is
#              higher, mood is improving. If lower, declining.
#
# WHEN IT IS CALLED:
#   From main() when the user chooses option 3.
# ============================================================
def weekly_summary():

    print()
    print("=" * 47)
    print("  WEEKLY SUMMARY")
    print("=" * 47)

    entries = read_all_entries()

    # Need at least 2 entries to calculate a trend
    if len(entries) < 2:
        print("\n  Please log at least 2 moods to see a summary.")
        return

    # Get the last 7 entries
    last_7 = entries[-7:]

    # --- Calculate the average ---
    total = 0
    for entry in last_7:
        total = total + int(entry["mood_score"])

    average = total / len(last_7)

    # --- Find the best and worst score ---
    best  = 0    # start low so the first real score beats it
    worst = 10   # start high so the first real score beats it

    for entry in last_7:
        score = int(entry["mood_score"])

        if score > best:
            best = score    # new highest found - update best

        if score < worst:
            worst = score   # new lowest found - update worst

    # --- Calculate the trend ---
    # Split the list into two halves
    mid         = len(last_7) // 2   # // means divide and round down
    first_half  = last_7[:mid]       # entries from start to middle
    second_half = last_7[mid:]       # entries from middle to end

    # Add up scores in each half
    first_total = 0
    for entry in first_half:
        first_total = first_total + int(entry["mood_score"])

    second_total = 0
    for entry in second_half:
        second_total = second_total + int(entry["mood_score"])

    # Calculate average for each half
    first_avg  = first_total / len(first_half)
    second_avg = second_total / len(second_half)

    # Compare halves to determine trend direction
    if second_avg > first_avg:
        trend = "Going UP - great progress!"
    elif second_avg < first_avg:
        trend = "Going DOWN - consider talking to someone"
    else:
        trend = "Staying the same"

    # --- Print the summary report ---
    print()
    print("  Days recorded : " + str(len(last_7)))
    print("  Average score : " + str(round(average, 1)) + " out of 10")
    print("  Best score    : " + str(best))
    print("  Worst score   : " + str(worst))
    print("  Weekly trend  : " + trend)

    # Run the alert check as a final safety step
    check_alert(entries)


# ============================================================
# MAIN FUNCTION - The engine that runs the whole program
#
# PURPOSE:
#   Shows the menu, reads the user's choice, calls the right
#   function, and repeats until the user chooses to exit.
#
# HOW IT WORKS:
#   - First calls create_file_if_missing() so the CSV is ready.
#   - Enters a while True loop - this runs forever until we
#     hit the break statement (which only happens on option 5).
#   - Each option maps to one function using if/elif/else.
#   - If the user types something other than 1-5 the else
#     block catches it and asks them to try again.
#
# NOTE:
#   "if __name__ == '__main__'" is a Python convention.
#   It means: only run main() if this file is being run
#   directly (not imported by another file). This is
#   considered good practice in Python programming.
# ============================================================
def main():

    # Make sure the data file exists before anything else runs
    create_file_if_missing()

    print()
    print("=" * 47)
    print("  Ulster University - Student Mood Tracker")
    print("=" * 47)
    print("  Track your daily mood and spot patterns.")
    print("  Your data is saved privately on your device.")
    print("=" * 47)

    # Keep the program running until the user chooses Exit
    while True:

        print()
        print("  MENU")
        print("  " + "-" * 30)
        print("  [1]  Log today's mood")
        print("  [2]  View history")
        print("  [3]  Weekly summary")
        print("  [4]  Show mood chart")
        print("  [5]  Exit")
        print("  " + "-" * 30)

        choice = input("\n  Enter 1 to 5: ").strip()

        if choice == "1":
            log_mood()
        elif choice == "2":
            view_history()
        elif choice == "3":
            weekly_summary()
        elif choice == "4":
            show_chart()
        elif choice == "5":
            print()
            print("  Take care of yourself. Goodbye!")
            print()
            break   # exit the while loop and end the program
        else:
            print("\n  Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
