# face-recognition-attendance-management-system

In the project “Biometric Face Recognition Attendance System”, face detection and face recognition is used. Face detection is used to locate the position of face region and face recognition is used for marking the attendance. 

### Open  CV  based face  recognition approach has been proposed. 

This model integrates a camera that captures an input image, an algorithm for detecting faces from an input  image,  encoding  and  identifying  the  face,  marking  the attendance in a spreadsheet and uploading it to the pymysql server. The training database is created by training the system with the faces of the authorized students. The cropped images are then stored as a database with respective labels. The features are extracted using LBPH algorithm.The database of all the staff in the university is stored and when the face of the individual staff matches with one of the faces stored in the database then the attendance is recorded with components Id, Name, Date and Time to the server.
