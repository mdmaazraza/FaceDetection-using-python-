import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognitionwithrealt-e9796-default-rtdb.firebaseio.com/"
})
ref = db.reference('Employees')
data = {
    "0001": {
        "Name": "Md Maaz Raza",
        "Major": "CEO",
        "Starting_year": "2017",
        "Standing": "A",
        "year": "6",
        "total_attendance": '702',
        "Last_Attendance_Time": "26-06-2024 12:39:59"

    },
    "0002": {
        "Name": "Shadab Anwer",
        "Major": "Employee",
        "Starting_year": "2020",
        "Standing": "B",
        "year": "3",
        "total_attendance": '1',
        "Last_Attendance_Time": "25-06-2023 12:25:25"

    },
    "0003": {
        "Name": "Fazle Rahman",
        "Major": "HR",
        "Starting_year": "2021",
        "Standing": "G",
        "year": "2",
        "total_attendance": '5',
        "Last_Attendance_Time": "22-06-2023 11:54:07"

    },
    "0004": {
        "Name": "ELon Musk",
        "Major": "Employee",
        "Starting_year": "2021",
        "Standing": "E",
        "year": "2",
        "total_attendance": '1',
        "Last_Attendance_Time": "26-06-2023 00:54:36"

    },
    "0005": {
        "Name": "Murtaza",
        "Major": "Manager",
        "Starting_year": "2020",
        "Standing": "G",
        "year": "3",
        "total_attendance": '2',
        "Last_Attendance_Time": "26-06-2023 10:25:42"

    },
    "0006": {
        "Name": "Emily Blunt",
        "Major": "Receptionist",
        "Starting_year": "2019",
        "Standing": "Avg",
        "year": "4",
        "total_attendance": '3',
        "Last_Attendance_Time": "24-06-2023 11:44:25",

    },
    "1234": {
        "Name": "Arsalan Haidar",
        "Major": "Peon",
        "Starting_year": "2021",
        "Standing": "B",
        "year": "2",
        "total_attendance": '112',
        "Last_Attendance_Time": "29-05-2023 12:05:42"

    },
    "1235": {
        "Name": "Sufiya Jabi",
        "Major": "Accountant",
        "Starting_year": "2022",
        "Standing": "G",
        "year": "1",
        "total_attendance": '21',
        "Last_Attendance_Time": "28-06-2023 10:25:42"

    },
    "01236": {
        "Name": "Wasim Khan",
        "Major": "OWNER",
        "Starting_year": "2016",
        "Standing": "G",
        "year": "7",
        "total_attendance": '01',
        "Last_Attendance_Time": "28-06-2023 10:25:42"
    },

    "1237": {
        "Name": "Zoya Nasreen",
        "Major": "Choti Babu",
        "Starting_year": "2023",
        "Standing": "A",
        "year": "0",
        "total_attendance": '11',
        "Last_Attendance_Time": "28-06-2023 10:25:42"

    },
    "01234": {
        "Name": "Inzmam Alam",
        "Major": "Employee",
        "Starting_year": "2022",
        "Standing": "A",
        "year": "1",
        "total_attendance": '21',
        "Last_Attendance_Time": "25-05-2023 11:25:42"
    },
    "12310": {
        "Name": "Aman shaikh",
        "Major": "employees",
        "Starting_year": "2020",
        "Standing": "G",
        "year": "3",
        "total_attendance": '5',
        "Last_Attendance_Time": "22-08-2023 11:54:07"
    },
    "963852": {
        "Name": "Elon Musk",
        "Major": "employees",
        "Starting_year": "2024",
        "Standing": "G",
        "year": "4",
        "total_attendance": '5',
        "Last_Attendance_Time": "22-08-2024 11:54:07"
    }
}
for key, value in data.items():
    ref.child(key).set(value)

print("executed")
