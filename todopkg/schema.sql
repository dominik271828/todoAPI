DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS statusTable;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    passwd TEXT NOT NULL
);

CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brief TEXT NOT NULL,
    detail TEXT NOT NULL,
    taskStatus INTEGER NOT NULL,
    taskOwner INTEGER NOT NULL,
    FOREIGN KEY (taskStatus) REFERENCES statusTable(id),
    FOREIGN KEY (taskOwner) REFERENCES user(id)
);

CREATE TABLE statusTable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    statusName TEXT NOT NULL UNIQUE
);

INSERT INTO statusTable(statusName) VALUES ("completed"), ("in-progress"), ("suspended"), ("dropped");