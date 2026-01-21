# Twix Launcher - Setup Guide

## Quick Start for Users

### Option 1: Download Pre-built Executable (Easiest)

1. Download `TwixLauncher.exe` from GitHub Releases
2. Place it anywhere on your computer
3. Double-click to run
4. The launcher will automatically:
   - Create `C:/Twix` folder
   - Generate configuration files
   - Set up version management

### Option 2: Run from Source

1. Install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)

2. Download/clone this repository

3. Open Command Prompt in the project folder

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the launcher:
   ```bash
   python launcher.py
   ```

## Configuration

### Adding Game Versions

After first run, edit `C:/Twix/versions.json`:

```json
{
  "versions": [
    {
      "name": "ALPHA 1.16.5",
      "description": "Latest version description",
      "download_url": "https://your-server.com/game-v1.16.5.zip",
      "installed": false
    }
  ]
}
```

**Important:** Replace `download_url` with your actual game download link.

### Where to Host Game Files

You can host your game files on:
- Google Drive (get direct download link)
- Dropbox (use direct link)
- Your own web server
- GitHub Releases (for open source games)
- Mega.nz
- MediaFire

#### Getting Direct Download Links:

**Google Drive:**
1. Upload your game zip file
2. Right-click → Get link → Set to "Anyone with the link"
3. Copy the file ID from the URL
4. Use format: `https://drive.google.com/uc?export=download&id=FILE_ID`

**Dropbox:**
1. Upload file and get share link
2. Replace `www.dropbox.com` with `dl.dropboxusercontent.com`
3. Remove `?dl=0` from the end

### Launcher Settings

Settings are saved automatically in `C:/Twix/launcher_config.json`:

- **ram_allocated**: MB of RAM (1024-16384)
- **selected_version**: Currently selected game version
- **last_played**: Last played version

## Building Your Own Executable

### Windows

1. Install Python 3.8+

2. Clone/download the repository

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run build script:
   ```bash
   python build_exe.py
   ```
   Or simply double-click `build.bat`

5. Find your executable in `dist/TwixLauncher.exe`

### Adding Custom Icon

1. Create or download a `.ico` file (256x256 recommended)

2. Save it as `icon.ico` in the project folder

3. Edit `build_exe.py`, uncomment the icon line:
   ```python
   "--icon=icon.ico",
   ```

4. Rebuild: `python build_exe.py`

## Customization

### Change Installation Path

In `launcher.py`, modify:

```python
GAME_PATH = "C:/Twix"  # Change to your preferred path
```

**Note:** After changing, you must rebuild the .exe if using executable version.

### Modify UI Colors

In `launcher.py`, find and modify:

```python
# Main background
fg_color="#1a1a2e"

# Panel background
fg_color="#16213e"

# Accent color (buttons, text)
text_color="#00d4ff"
```

Common color schemes:
- **Dark Blue:** `#1a1a2e`, `#16213e`, `#00d4ff`
- **Dark Purple:** `#1a1a2e`, `#2d1b3d`, `#c74fdb`
- **Dark Green:** `#0d1f0e`, `#1a3a1f`, `#4fff4f`
- **Pure Dark:** `#0a0a0a`, `#1a1a1a`, `#00ffff`

## Testing

Run the comprehensive test suite:

```bash
python test_launcher_functions.py
```

All 28 tests should pass before building for distribution.

## Troubleshooting

### "Python not found"
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation

### "No module named 'customtkinter'"
```bash
pip install -r requirements.txt
```

### "Permission denied" errors
- Run Command Prompt as Administrator
- Check antivirus isn't blocking

### Download fails
- Verify your download URL is correct
- Test the URL in a browser first
- Ensure it's a direct download link (not a webpage)

### Game won't launch
- Check that the game .exe file is in `C:/Twix/[VersionName]/`
- Verify file permissions
- Try running the game .exe directly first

## Distribution

### Sharing Your Launcher

1. Build the executable
2. Test it on a clean machine
3. Upload to:
   - GitHub Releases
   - Your website
   - Google Drive
   - Dropbox

### Creating a Release Package

Include:
- `TwixLauncher.exe`
- `README.txt` (simplified instructions)
- Example `versions.json` (with your download URLs)

Example README.txt:
```
Twix Launcher v1.0.0

Installation:
1. Extract all files
2. Run TwixLauncher.exe
3. Select version and click download
4. Click launch to play

Game files are saved to: C:\Twix

For support: t.me/TwixClient
```

## Advanced: Auto-Update System

To add auto-updates to your launcher:

1. Host a `version.json` on your server:
```json
{
  "latest_version": "1.0.1",
  "download_url": "https://your-server.com/TwixLauncher_v1.0.1.exe",
  "changelog": "Fixed download bug"
}
```

2. Add update checker in launcher code (see comments in launcher.py)

3. Implement download and restart logic

## Support

- Telegram: t.me/TwixClient
- GitHub Issues: Report bugs
- Email: your-email@example.com

## Tips for Success

1. **Test thoroughly** before distributing
2. **Use HTTPS** for download URLs
3. **Version your releases** (v1.0.0, v1.0.1, etc.)
4. **Provide support channel** (Discord, Telegram)
5. **Keep backups** of all versions
6. **Document changes** in changelog
7. **Test on multiple machines** before release

## Security Notes

- Only download games from trusted sources
- Verify file checksums if possible
- Don't hardcode sensitive information
- Use HTTPS for all downloads
- Consider code signing for .exe files

---

Need help? Join our Telegram: t.me/TwixClient
