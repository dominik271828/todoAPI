# Simple ToDo list API
This repository contains the source code for a simple ToDo list API I wrote as an excercise to learn flask and python.
## Features
* The API is RESTful
* CRUD operations on tasks
    * Deleting tasks by ID
    * Updating tasks by ID
    * Fetching all tasks, fetching tasks by ID, fetching tasks by status
    * Creating tasks
* Basic user authentication (credentials in base64 sent over a POST header). Password is hashed.
    * Registering a new user
    * Authenticating as a user
## Installation
### Prerequisites
- Python3 with pip
### Setup
1. Clone the repository:
```bash
git clone https://github.com/dominik271828/todoAPI.git
cd todoAPI
```
2. (Optional) Setup a python virtual environment
```bash
python3 -m venv .venv
```
3. Install the project as a python package
```bash
pip install -e .
```
4. Run the server:
```
flask --app todopkg run
```

## API endpoints
### Task management
- **POST** `/todolist/create_task` - create a task, expects a json with the following properties: `Authorization`, `brief`, `detail`, `taskStatus`
- **GET** `/todolist/fetch` - fetch tasks, expects a request with the following url parameters:
`detailed`(optional), `status`(optional)
- **POST** `/todolist/update` - update a task with a given id, expects a json with the following properties: `Authorization`, `brief`(optional), `detail`(optional), `taskStatus`(optional)
- **POST** `/todolist/delete` - delete a task with a given id, expects a json with the following properties: `Authorization`, `id`
### Authorization
- **POST** `/auth/register` - registers a user, expects a json with the following properties: `username`, `passwd`
### JSON properies
`Authorization` - header for user authentication, structured like so: `Authorization: Basic base64_encode("username:passwd")`

`brief` - Every task has a brief description, this is where it's provided.

`detail` - Every task has a detailed description, this is where it's provided.

`taskStatus` - Every task has a completion status (completed, in-progress, dropped, suspended) this is where it's provided.

`id` - ID of the task to be modified
### URL parameters
`detailed` - by default, the fetch view doesn't return detailed information about the listed task. When this parameter is present, more of the information is shown.

`status` - allows filtering the fetching of articles by their status

## Contributing

Feel free to fork this repository, submit issues, or make pull requests. Contributions are always welcome.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


