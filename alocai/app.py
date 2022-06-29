import io
import json
import tempfile
from flask import Flask, request, send_file
import csv
from .transforms import OUTPUT_COLUMNS, OUTPUT_HEADERS, COLUMN_NAME_TO_POSITION
from datetime import datetime


def _parse_file(file) -> list:
    """Parses provided file from request 

    Args:
        file (file): provided file

    Returns:
        list: parsed rows and columns
    """
    parsed_rows = []

    # Decodes bytes and splits file line by line
    file = file.read().decode('utf-8').splitlines()

    # Splits lines by ','
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        parsed_rows.append(row)

    return parsed_rows


def is_csv(filename: str) -> bool:
    """Checks if provided file is css

    Args:
        filename (str): name of the file

    Returns:
        bool: True - file is csv file, otherwise - False
    """
    split = filename.rsplit('.', 1)
    # Check if the file has an extension
    if len(split) < 2:
        return False

    return split[1].lower() == 'csv'


def _fill_corrected_data(parsed_rows, app):
    """_summary_

    Args:
        parsed_rows (_type_): _description_

    Returns:
        _type_: _description_
    """
    if len(OUTPUT_COLUMNS) < len(parsed_rows[0]):
        return "Error"

    # Output list
    output = []

    for row_index in range(len(parsed_rows)):
        row = parsed_rows[row_index]
        output_row = []
        evict_row = False
        for index in range(len(OUTPUT_COLUMNS)):
            column_data = row[index]

            try:
                transform_function = OUTPUT_COLUMNS[index]['transform']
                if transform_function:
                    column_data = transform_function(column_data)
                output_row.append(column_data)
            except Exception as ex:
                # If error occurred while transforming data we evicting
                # current row entirely
                evict_row = True
                app.logger.error(f'[Error]: {ex}')

        if evict_row:
            app.logger.warn(f'Evicting row at index {row_index}')
            continue

        try:
            copies_sold = row[COLUMN_NAME_TO_POSITION["Copies Sold"]]
            copy_price = row[COLUMN_NAME_TO_POSITION["Copy Price"]]

            # Assuming that price of copy in the format: <numeric_price> <currency>
            split_price = copy_price.split(' ')
            currency = " " + split_price[1]
            price = float(split_price[0])

            total_revenue = round(int(copies_sold) * price)
            output_row.append(str(total_revenue) + currency)

            output.append(output_row)
        except Exception as ex:
            app.logger.error(
                f"Couldn't calculate total revenue at index {row_index}." +
                " Evicting the row")

    output.sort(key=lambda row: datetime.strptime(
        row[COLUMN_NAME_TO_POSITION["Release Date"]], "%d.%m.%Y"))

    # Insert headers
    output.insert(0, OUTPUT_HEADERS)

    return output


def _upload(app):
    """Implementation of upload method

    Returns:
        file or error: returns csv file on success or
    """
    # Check if user provided an input file
    if not request.files:
        app.logger.error('No input file provided')
        return 'No input file provided', 500

    # Check if request contains 'file' part
    if 'file' not in request.files:
        app.logger.error('No file part provided')
        return "No file part. Example: curl -F 'file=...'", 500

    # Get file from the request
    file = request.files['file']

    # Check if file was actually attached to request
    if file.filename == '':
        app.logger.error('No file attached')
        return 'No file attached', 500

    # Check if filename contains '.csv' extension
    if not is_csv(file.filename):
        app.logger.error('Provided file is not a .csv file')
        return 'Provided file is not a .csv file', 500

    # Parses file
    parsed_rows = _parse_file(file)

    # Correct data and fill lists
    result = _fill_corrected_data(parsed_rows, app)

    # Writing data to temporary file
    with tempfile.TemporaryFile(mode='a+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        # Write data to file
        for row in result:
            writer.writerow(row)
        csv_file.seek(0)

        # Turn data into bytes
        bf = io.BytesIO(bytes(csv_file.read(), 'utf-8'))
        return send_file(bf, mimetype='text/csv')


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
        return _upload(app)

    return app
