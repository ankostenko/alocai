from flask import Flask, request, flash


def parse_file(file):
    """
    Parses data.
    :return: 
    """

    return None


def is_csv(filename: str) -> bool:
    """
    Checks if provided file is csv file.
    :return: True if provided file has 'csv' in filename.
    """
    split = filename.rsplit('.', 1)
    if len(split) < 2:
        return False

    return split[1].lower() == 'csv'


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    @app.route('/upload', methods=['POST'])
    def upload():
        """
        Accepts a file and parses.
        :return: 
        """
        # Check if user provided an input file
        if not request.files:
            flash('No input file provided')
            return 'No input file provided', 500

        # Check if request contains 'file' part
        if 'file' not in request.files:
            flash('No file part provided')
            return "No file part. Example: curl -F 'file=...'", 500

        # Get file from the request
        file = request.files['file']

        # Check if file was actually attached to request
        if file.filename == '':
            flash('No file attached')
            return 'No file attached', 500

        # Check if filename contains '.csv' extension 
        if not is_csv(file.filename):
            flash('Provided file is not a .csv file')
            return 'Provided file is not a .csv file', 500

        

        return "hello"

    return app
