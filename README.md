# Memon Browser 🌐🚀

Memon Browser is a lightweight, PyQt5-based web browser designed for simplicity and efficiency. It features a custom frameless UI, tabbed Browse, and essential navigation functionalities, making it a great starting point for a personalized Browse experience or a learning project in GUI development with Python.

-----

## Features ✨

  * **Custom Frameless Window**: Enjoy a sleek, modern look with custom minimize, maximize, and close buttons.
  * **Tabbed Browse**: Easily open and manage multiple tabs, with a limit to prevent excessive resource usage.
  * **Search and Navigation**: Integrated search bar for URLs and Google queries, along with back and forward navigation buttons.
  * **Bookmarks**: Quickly bookmark and access your favorite pages.
  * **Zoom Control**: Adjust page zoom with a user-friendly slider.
  * **Find on Page**: Search for specific text within the current webpage.
  * **Loading Indicator**: A simple spinner shows when a page is loading.
  * **Responsive Design**: Automatically maximizes on launch for a full-screen experience.

-----

## Prerequisites 🛠️

Before you can run Memon Browser, ensure you have the following installed:

  * **Python 3.x**: Download from [python.org](https://www.python.org/downloads/).
  * **PyQt5**: The core GUI framework.
  * **PyQtWebEngine**: Required for rendering web content.

-----

## Installation 💻

1.  **Clone the repository** (or download the `main.py` file directly):
    ```bash
    git clone https://github.com/your-username/Memon-Browser.git
    cd Memon-Browser
    ```
2.  **Create a `requirements.txt` file**: In the root directory of your project, create a file named `requirements.txt` and paste the following content:
    ```
    PyQt5
    PyQtWebEngine
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

-----

## Usage ▶️

1.  **Prepare assets**: The browser uses a few image files for icons and animations. For the best experience, place the following files in the same directory as `main.py`:

      * `spinner.gif` (for the loading animation)
      * `zoom-in.png` (for the zoom dialog icon)
      * `warning.png` (for the tab limit warning icon)
        If these files are missing, the browser will still function, but these visual elements won't appear.

2.  **Run the script**:

    ```bash
    python main.py
    ```

The browser window will open, maximized by default. You can start typing URLs or search queries into the address bar.

-----

## Output Excel Format 📊

This browser does not produce an Excel output. This section is typically for data extraction scripts.

-----

## Important Notes ⚠️

  * **Custom UI**: The browser uses a frameless window, meaning standard operating system window controls are replaced by custom buttons.
  * **Missing Assets**: As mentioned in the "Prepare assets" section, ensure `spinner.gif`, `zoom-in.png`, and `warning.png` are present for a complete visual experience. You can use any GIF for the spinner and any suitable PNG icons.
  * **`Ctrl+W` Shortcut**: This shortcut is implemented to quickly close the current tab. If no tabs are left, the browser will close.
  * **Tab Limit**: There's a maximum of 25 tabs to manage performance and resources.

-----

## Support My Work ❤️

If you find this project useful and would like to support its development, any contribution is greatly appreciated\! Your support helps in maintaining and improving this browser.

Here are a few ways you can contribute financially:

  * **Patreon**: [Link to your Patreon page] (e.g., `https://www.patreon.com/YourUsername`)
  * **Buy Me a Coffee**: [Link to your Buy Me a Coffee page] (e.g., `https://www.buymeacoffee.com/YourUsername`)
  * **PayPal**: [Link to your PayPal.Me or direct PayPal donation link] (e.g., `https://paypal.me/YourUsername`)

Thank you for your support\!

-----

## Contributing 🤝

Feel free to fork this repository, open issues, and submit pull requests if you have suggestions for improvements or bug fixes. Ideas for future enhancements include:

  * Adding a history feature.
  * Implementing persistent bookmarks (saving/loading to a file).
  * Adding download management.
  * Improving the settings page.

-----
