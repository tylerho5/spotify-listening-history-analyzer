# Spotify Listening History Analyzer

This is a personal project I built to showcase working with real-world Spotify data to create clean, informative visualizations of muslc listening habits. You can request your Spotify streaming history in JSON format directly from Spotify and see some interesting statistics about the music you listen to. This project inspired by Spotify's own statistics analysis project, Spotify Wrapped.

## Key Features

- Data Ingestion and Cleaning: `DataGrabber.py` loads all the JSON files containing your streaming history and combines them into a single dataset. After some brief testing, I was able to determine that in order to mirror the stats that Spotify has for each user (based on my own Spotify Wrapped 2024), only listening entries from January to mid-November of the year count towards the listening statistics. Very short plays (less than 60 seconds) are also excluded to focus on meaningful listens. After the cleaning and filtering, your data is stored in a consolidated CSV for convenience.

- Summary Statistics: `HistoryAnalyzer.py` can quickly get insights into your listening habits, like top songs and top artists for the year, include play counts, similar to Spotify Wrapped. It also calculates total time spent listening over the course of the year and the number of unique songs you listened to.

- Data Visualizations: If the `graph` mode is selected, the analyzer will use `DataPlotter.py` to produce clear charts to visualize some of the statistics mentioned above. 

- Demo in Jupyter Notebook: The project is testable through the `demo.ipynb` Jupyter Notebook for easy demonstration.

## Installation

### Using pip with venv

1. **Clone repo**:
```bash
git clone https://github.com/tylerho5/personal-projects.git
cd personal-projects/Spotify_Listening_History_Analyzer
```

2. **Create a virtual environment for the project**:

```bash
python3 -m venv venv
```

3. **Activate the virtual environment**:
- On macOS/Linux:
```bash
source venv/bin/activate
```

- On Windows:
```bash
.\venv\Scripts\activate
```

4. **Install the required dependencies**:
```bash
pip install -r requirements.txt
```

### Using Conda
1. **Clone repo**:(same as above)

2. **Create Conda environment**:
```bash
conda env create -f environment.yml
```

3. **Activate the Conda environment**:
```bash
conda activate spotify-analyzer
```

## Usage
1. **Obtain and place your Spotify Streaming History JSON files**:
You can request your Sporify listening history thorugh your Spotify settings (Spotify account > Security and privacy > Account Privacy). The request usually takes a few days after which Spotify should sen you an email with a .zip folder containing your streaming history in JSON format. 

2. **Prepare data files**:
Create a folder named `spotify-account-data` inside the `spotify-listening-history-analyzer` project directory. Place all your JSON files inside this folder. These files are typically named `StreamingHistory_music_0.json`, `StreamingHistory_music_1.json`, etc. If they are different, you need to modify the names so that `DataGrabber.py` can find them. Alternatively you can alter the file pattern that the grabber uses to select your music history JSONs. Also make sure each JSON includes fields like "endTime", "artistName", "trackName", and "msPlayed" – which is the format this project expects. The project will not work if Spotify has altered the JSON structure.

3. **Run the Demo**:
You can now open `demo.ipynb` and see your music listening history! Alternatively you can run the through terminal or as a script:

```python
import HistoryAnalyzer

# Initialize the analyzer for a specific year (e.g., 2024). 
# Use type="list" for text output type="graph" for graphical output.
analyzer = HistoryAnalyzer(current_year=2024, type="list")

# Generate analysis results:
analyzer.topSongs()          # Lists top songs of 2024 in the console
analyzer.topArtists()        # Shows a bar chart of top artists of 2024
analyzer.totalListeningTime()# Displays a bar chart of minutes listened per month in 2024
analyzer.howManySongs()      # Prints the number of unique songs listened in 2024
```

*Different Demo modes*:
- set type="list": The analyzer will use pandas to present your metrics in tables
- set type="graph": The analyzer will pop up matplotlib windows if running through terminal/shell or inline in the Jupyter Notebookl

**Note**: If you have data from different years, simply change the current year to whatever year your data is for. Just make sure to place the JSONs in the `spotify-account-data` folder and that the file names are correct.

## Project Structure

`spotify-listening-history-analyzer/`

- **DataGrabber.py** - Module for loading data from JSON files to construct pandas DataFrame. Searches for JSONs in the `spotify-account-data` folder. Once the module has cleaned, filtered, and aggregated data, it stores it in `spotify-history.csv`.

- **HistoryAnalyzer.py** - Main module that handles getting the .csv using `DataGrabber.py`, provides user-facing methods to get top songs, top artists, monthly listening time, etc., formats results in either pandas DataFrame format or using matplotlib by calling DataPlotter.py functions

- **DataPlotter.py** - Defines helper functions for plotting using matplotlib. Has both vertical and horizontal bar plot options for different metrics.

- **spotify-account-data/** - This is where you place your Spotify Streaming History JSON files. You will have to create this folder manually.

- **spotify-history.csv** - Output CSV file that `DataGrabber.py` produces, containing the cleaned, filtered, and aggregated listening history for the specified year. This file is genereated at runtime and is not included in the repo.

- **demo.ipynb** - Jupyter Notebook demonstrating usage of `HistoryAnalyzer.py`. SHows how to instantiate the class and call various methods.
