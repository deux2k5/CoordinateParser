# Tacview XML Waypoint Parser

A Python GUI application that reads and parses waypoint data from Tacview XML files. The application displays the parsed data in a user-friendly table and allows users to copy specific columns to the clipboard for easy access and further analysis.

## Features

- **XML Parsing**: Reads waypoint data from Tacview-generated XML files.
- **Data Conversion**: Converts latitude and longitude from decimal degrees to Decimal Degrees and Minutes (DDM) format.
- **Data Cleaning**: Removes unwanted substrings (e.g., "Venom1") and formats waypoint names for clarity.
- **User-Friendly Interface**: Utilizes Tkinter for an intuitive GUI with table views and interactive buttons.
- **Clipboard Integration**: Allows users to copy entire columns of data to the clipboard with a single click.

## Screenshots

_Add screenshots of the application here if available._

## Requirements

- Python 3.x
- Tkinter (usually included with Python)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/tacview-xml-parser.git
   cd tacview-xml-parser
   ```

2. **(Optional) Create a Virtual Environment**

   It's good practice to use a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   This application uses only standard Python libraries, so no additional installations are required.

## Usage

1. **Run the Application**

   ```bash
   python parser.py
   ```

2. **Open an XML File**

   - Click on the **"Open XML File"** button.
   - Browse and select the desired Tacview XML file.

3. **View Parsed Waypoints**

   - The application will display the waypoints in a table with the following columns:
     - **Name**: Cleaned waypoint name.
     - **Latitude (DDM)**: Latitude in Decimal Degrees and Minutes format.
     - **Longitude (DDM)**: Longitude in Decimal Degrees and Minutes format.
     - **Altitude (ft)**: Altitude in feet.

4. **Copy Column Data**

   - Click on the **"Copy [Column Name]"** button to copy the entire column's data to the clipboard.
   - A confirmation message will appear upon successful copying.

## Code Overview

### `decimal_degrees_to_ddm(value, is_latitude=True)`

Converts decimal degrees to Decimal Degrees and Minutes (DDM) format.

### `copy_column_to_clipboard(treeview, column_index)`

Copies all values from the specified column in the table to the clipboard.

### `parse_and_populate_tree(file_path, treeview)`

Parses the XML file and populates the table with waypoint data, applying necessary data cleaning and conversion.

### `open_xml_file(treeview)`

Opens a file dialog for the user to select an XML file and triggers the parsing process.

### `main()`

Sets up the main GUI window, including the table view and buttons, and starts the application's main loop.

## Example XML Structure

Ensure your Tacview XML files contain `<Waypoint>` elements structured as follows:

```xml
<Waypoint>
    <Name>ExampleWaypointVenom1</Name>
    <Position>
        <Latitude>34.12345</Latitude>
        <Longitude>-117.12345</Longitude>
        <Altitude>5000</Altitude>
    </Position>
</Waypoint>
```

## Troubleshooting

- **XML Parsing Errors**: Ensure the selected XML file is correctly formatted and contains the necessary `<Waypoint>` elements.
- **Missing Tkinter**: If you encounter issues related to Tkinter, ensure it is installed and properly configured with your Python installation.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## License

_Specify your project's license here, e.g., MIT License._

## Acknowledgements

- [Tacview](https://www.tacview.net/) for providing the XML format used in this parser.
- Python's [Tkinter](https://docs.python.org/3/library/tkinter.html) library for the GUI components.
