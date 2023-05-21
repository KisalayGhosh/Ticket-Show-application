# Ticket Show Application

This is a website management application built using Flask, a Python web framework. The application allows users to sign up, log in, and interact with various features depending on their role (user or admin).

## Features

- User Authentication: Users can sign up and log in to access their profile.
- User Profile: Users can view their profile information, update their details, and view and book shows.
- Show Management: Admins can add, update, and delete shows, including show name, rating, tags, ticket price, capacity, and customer feedback.
- Venue Management: Admins can add, update, and delete venues, including venue name, capacity, and place.
- Booking Management: Users can book shows and view their bookings. Admins can also view and delete bookings made by users.
- Feedback: Users can provide feedback for shows they attended.

## Technologies Used

- Flask: Python web framework for building the application.
- SQLAlchemy: ORM for interacting with the SQLite database.
- HTML, CSS, JavaScript: Front-end technologies for creating the user interface.
- SQLite: Database used to store user and application data.

## Getting Started

1. Install Python (version 3.x) and pip on your system.
2. Clone the repository: `git clone https://github.com/KisalayGhosh/Ticket-Show-application.git`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Set up the database:
   - Modify the `app.config['SQLALCHEMY_DATABASE_URI']` in `app.py` to set the appropriate database URI.
   - Run the following commands in the terminal:
     ```
     python
     from app import db
     db.create_all()
     exit()
     ```
5. Start the application: `python app.py`
6. Access the application in your web browser at `http://localhost:5000`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

Feel free to modify and customize the application to suit your specific needs.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/): Official Flask documentation for reference and guidance.
- [SQLAlchemy](https://www.sqlalchemy.org/): SQLAlchemy documentation for database interaction.
- [Bootstrap](https://getbootstrap.com/): CSS framework for styling the application.

## Author

Arunangshu Das | Kisalay Ghosh
