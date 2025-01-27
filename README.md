# Image Detector - Image Processing and Comparison Tool

example of usage - [link](https://youtu.be/au-47lE0Nsg)

## Description  
ImageDetector is a Python-based GUI application built with Pygame that allows users to load, process, and compare images. It supports various image processing techniques and stores image hashes in a database for similarity checks. This tool is ideal for experimenting with filters and finding visually similar images.

---

## Features  
- **Load Images**: Input an image path to load and display images.  
- **Image Processing**:  
  - **Adjust Brightness**: Solarize the image by adjusting brightness.  
  - **Grayscale Conversion**: Convert images to grayscale.  
  - **Halftone Effect**: Apply a geometric mean filter for a halftone effect.  
  - **Monochrome Conversion**: Convert images to 1-bit monochrome.  
  - **Erosion**: Apply erosion to monochrome images to remove noise.  
- **Database Integration**:  
  - **Add to Database**: Store processed image hashes in a SQLite database.  
  - **Find Similar Images**: Compare the current image against the database to find matches.  
- **GUI Interface**: Intuitive buttons and input fields for easy interaction.  

---

## Usage

example of usage - [link](https://youtu.be/au-47lE0Nsg)

Step by step instruction - 

Run the Application:
    python PrintPic.py  
    
Load an Image: 
    Enter the image path in the input box (e.g., picsBlack/Gosling.png).

Click Load Image to display it.
Apply Filters one by one:

Use the buttons on the right to apply filters (e.g., solar, grayscale).

Database Operations:
Add to DB: After processing, click to store the image hash.

Find Similar: Compare the current image against the database. Results show the closest match and difference percentage.


Output:

Results and errors are displayed in the text area below the image.

Notes
Image Requirements: Images are resized to 64x64 pixels.

Database: Uses SQLHashTable to manage hashes. Hashes are derived from processed pixel data.

Customization: Modify programData.py to set default paths or adjust processing parameters in individual modules.

## Manage database
You can run sub-application for managing database
    python SQL_admin.py  
