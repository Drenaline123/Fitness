import sqlite3

con = sqlite3.connect('fitness.db', check_same_thread=False)
db = con.cursor()

name = ["Squats", "Leg Press", "Chest Press", "Flys", "Pull Ups", "Cable Rows", "Bicep Curls", "Skull Crushers", "Hamstring Curls", "Shoulder Press" ]
image = ["855a1810-1710-11ed-861d-0242ac120002", "855a1b12-1710-11ed-861d-0242ac120002", "855a1c66-1710-11ed-861d-0242ac120002",
"855a1db0-1710-11ed-861d-0242ac120002", "855a1ef0-1710-11ed-861d-0242ac120002", "855a2026-1710-11ed-861d-0242ac120002", "855a2404-1710-11ed-861d-0242ac120002",
"855a251c-1710-11ed-861d-0242ac120002", "855a2620-1710-11ed-861d-0242ac120002", "855a2724-1710-11ed-861d-0242ac120002" ]
video=["xqvCmoLULNY", "zeWzPUmA", "VmB1G1K7v94", "eozdVDA78K0", "HRV5YKKaeVw", "xQNrFHEMhI4", "ykJmrZ5v0Oo", "d_KZxkY_0cM", "ELOCsoDSmrg", "qEwKCR5JCog" ]
for i in range(10):
    db.execute('INSERT INTO workouts (workout_name, workout_image, workout_video) VALUES(?,?,?)', (name[i], image[i], video[i]))
    con.commit()