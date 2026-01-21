# Twix Launcher

Modern game launcher with RAM allocation settings, version management, and automatic download functionality.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Tests](https://img.shields.io/badge/tests-28%20passed-success)

## Features

- **Modern UI**: Sleek, dark-themed interface with gradient effects
- **RAM Allocation**: Adjustable RAM settings for optimal game performance
- **Version Management**: Support for multiple game versions
- **Automatic Downloads**: Built-in game download functionality
- **Fixed Installation Path**: Games saved to `C:/Twix` (configurable in code)
- **Persistent Settings**: Configuration saved between sessions
- **Comprehensive Testing**: 28 unit tests covering all functionality

## Screenshots

The launcher features a modern interface similar to popular game launchers, with:
- Version selector dropdown
- RAM allocation slider
- Play button with visual feedback
- Download progress tracking
- Status messages

## Requirements

- Python 3.8 or higher
- Windows OS (for building .exe)
- Dependencies listed in `requirements.txt`

## Installation

### For Users (Pre-built Executable)

1. Download `TwixLauncher.exe` from the releases page
2. Run the executable
3. The launcher will automatically create `C:/Twix` directory
4. Configure your game versions in `C:/Twix/versions.json`

### For Developers

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Twiz.git
   cd Twiz
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the launcher:
   ```bash
   python launcher.py
   ```

## Building the Executable

### Windows

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```bash
   python build_exe.py
   ```
   Or use the batch file:
   ```bash
   build.bat
   ```

3. The executable will be created in the `dist` folder as `TwixLauncher.exe`

## Configuration

### Game Versions

Edit `C:/Twix/versions.json` to add your game versions:

```json
{
  "versions": [
    {
      "name": "ALPHA 1.16.5",
      "description": "Latest stable version",
      "download_url": "https://yourserver.com/game.zip",
      "installed": false
    }
  ]
}
```

### Launcher Settings

The launcher stores settings in `C:/Twix/launcher_config.json`:

```json
{
  "ram_allocated": 2048,
  "selected_version": "ALPHA 1.16.5",
  "last_played": null,
  "game_url": ""
}
```

## Usage

1. **Launch the application**
   - Run `TwixLauncher.exe` or `python launcher.py`

2. **Select a version**
   - Choose your desired game version from the dropdown

3. **Adjust RAM**
   - Use the slider to allocate RAM (1024 MB - 16384 MB)

4. **Download the game**
   - Click "СКАЧАТЬ ИГРУ" to download the selected version
   - Progress will be shown in the progress bar

5. **Launch the game**
   - Click "ЗАПУСТИТЬ" to start the game

## Testing

The project includes comprehensive unit tests covering all functionality.

### Run all tests:

```bash
python test_launcher_functions.py
```

### Test Coverage:

- **Configuration Management** (5 tests)
  - Default configuration loading
  - Save and load operations
  - Corrupted file handling
  - Value validation
  - Configuration updates

- **Version Management** (5 tests)
  - Version data structure
  - Save and load operations
  - Version lookup
  - Version list extraction

- **Directory Operations** (5 tests)
  - Directory creation
  - Nested directories
  - Executable detection
  - Path validation

- **RAM Calculations** (4 tests)
  - Value conversion
  - Min/max bounds
  - Display formatting

- **Download Validation** (3 tests)
  - URL validation
  - Empty URL handling

- **Path Operations** (2 tests)
  - Path construction
  - Path normalization

- **Status Messages** (2 tests)
  - Message formatting
  - Error messages

- **Integration Tests** (2 tests)
  - Complete workflows
  - End-to-end scenarios

**Total: 28 tests - 100% pass rate**

## Project Structure

```
Twiz/
├── launcher.py              # Main launcher application
├── test_launcher.py         # Original test suite
├── test_launcher_functions.py  # Comprehensive unit tests
├── build_exe.py             # Build script for creating .exe
├── build.bat                # Windows batch build script
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── C:/Twix/                 # Game installation directory (created at runtime)
    ├── launcher_config.json # Launcher configuration
    ├── versions.json        # Game versions data
    └── [version folders]/   # Downloaded game versions
```

## Customization

### Change Installation Path

Edit the `GAME_PATH` constant in `launcher.py`:

```python
GAME_PATH = "C:/YourCustomPath"
```

### Add Custom Icon

1. Create or obtain an `.ico` file
2. Save it as `icon.ico` in the project root
3. Uncomment the icon line in `build_exe.py`:
   ```python
   "--icon=icon.ico",
   ```

### Modify UI Theme

The launcher uses CustomTkinter. Modify colors in `launcher.py`:

```python
# Background colors
fg_color="#1a1a2e"   # Dark blue-grey
fg_color="#16213e"   # Lighter blue-grey

# Accent color
text_color="#00d4ff"  # Cyan
```

## Technical Details

### Dependencies

- **customtkinter**: Modern UI framework
- **requests**: HTTP library for downloads
- **psutil**: System information (RAM detection)
- **pillow**: Image processing
- **pyinstaller**: Executable creation

### Architecture

- **MVC Pattern**: Separation of UI and logic
- **Thread-based Downloads**: Non-blocking download operations
- **JSON Configuration**: Human-readable settings
- **Error Handling**: Comprehensive exception management

## Troubleshooting

### Launcher won't start
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Run from command line to see error messages

### Download fails
- Verify the download URL in `versions.json`
- Check internet connection
- Ensure write permissions to `C:/Twix`

### Game won't launch
- Verify game executable exists in version folder
- Check that .exe file has correct permissions
- Review launcher logs for error messages

### Build fails
- Update PyInstaller: `pip install --upgrade pyinstaller`
- Clear build cache: Delete `build` and `dist` folders
- Check Python version compatibility

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

## Testing Contributions

All code contributions must include tests. Run the test suite before submitting:

```bash
python test_launcher_functions.py
```

## License

This project is provided as-is for educational and personal use.

## Contact

- **Telegram**: [t.me/TwixClient](https://t.me/TwixClient)
- **Issues**: Report bugs on GitHub Issues

## Changelog

### Version 1.0.0 (2026-01-21)

- Initial release
- Modern UI with dark theme
- RAM allocation settings
- Version management system
- Download functionality
- Game launch system
- Comprehensive test suite (28 tests)
- Windows executable build support

## Roadmap

Future improvements planned:

- [ ] Custom icon integration
- [ ] Multi-language support
- [ ] Update checker
- [ ] Mod management
- [ ] Server status indicator
- [ ] Screenshot/video capture
- [ ] Performance monitoring
- [ ] Cloud save sync

---

Made with ❤️ for the Twix community
