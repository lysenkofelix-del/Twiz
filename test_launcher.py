import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock, mock_open
from pathlib import Path
import sys

# Mock all external dependencies before importing launcher
sys.modules['customtkinter'] = MagicMock()
sys.modules['psutil'] = MagicMock()
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['requests'] = MagicMock()

# Import after mocking
import launcher


class TestLauncherConfiguration(unittest.TestCase):
    """Test suite for launcher configuration management"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "launcher_config.json")
        self.versions_file = os.path.join(self.test_dir, "versions.json")

        # Patch the constants
        launcher.GAME_PATH = self.test_dir
        launcher.CONFIG_FILE = self.config_file
        launcher.VERSIONS_FILE = self.versions_file

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_default_config_values(self):
        """Test that default configuration values are correct"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    config = app.load_config()

                    self.assertEqual(config['ram_allocated'], 2048)
                    self.assertEqual(config['selected_version'], 'ALPHA 1.16.5')
                    self.assertIsNone(config['last_played'])
                    self.assertEqual(config['game_url'], '')

    def test_config_persistence(self):
        """Test that configuration is saved and loaded correctly"""
        test_config = {
            "ram_allocated": 4096,
            "selected_version": "ALPHA 1.16.4",
            "last_played": "ALPHA 1.16.3",
            "game_url": "https://example.com/game.zip"
        }

        # Save config
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f)

        # Load config
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    loaded_config = app.load_config()

                    self.assertEqual(loaded_config['ram_allocated'], 4096)
                    self.assertEqual(loaded_config['selected_version'], 'ALPHA 1.16.4')
                    self.assertEqual(loaded_config['last_played'], 'ALPHA 1.16.3')

    def test_corrupted_config_fallback(self):
        """Test that corrupted config file falls back to defaults"""
        # Write invalid JSON
        with open(self.config_file, 'w') as f:
            f.write("invalid json {{{")

        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    config = app.load_config()

                    # Should fall back to defaults
                    self.assertEqual(config['ram_allocated'], 2048)
                    self.assertEqual(config['selected_version'], 'ALPHA 1.16.5')

    def test_save_config(self):
        """Test that save_config writes configuration correctly"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.config = {
                        "ram_allocated": 8192,
                        "selected_version": "ALPHA 1.16.5",
                        "last_played": None,
                        "game_url": ""
                    }

                    app.save_config()

                    # Verify file was written
                    self.assertTrue(os.path.exists(self.config_file))

                    # Verify content
                    with open(self.config_file, 'r') as f:
                        saved_config = json.load(f)
                        self.assertEqual(saved_config['ram_allocated'], 8192)


class TestVersionManagement(unittest.TestCase):
    """Test suite for version management"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.versions_file = os.path.join(self.test_dir, "versions.json")
        launcher.GAME_PATH = self.test_dir
        launcher.VERSIONS_FILE = self.versions_file

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_default_versions_creation(self):
        """Test that default versions file is created if missing"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                app = launcher.TwixLauncher()
                app.version_selector = Mock()
                app.load_versions()

                # Verify versions file was created
                self.assertTrue(os.path.exists(self.versions_file))

                # Verify content
                with open(self.versions_file, 'r', encoding='utf-8') as f:
                    versions = json.load(f)
                    self.assertIn('versions', versions)
                    self.assertTrue(len(versions['versions']) >= 3)

    def test_version_loading(self):
        """Test that versions are loaded correctly"""
        test_versions = {
            "versions": [
                {
                    "name": "TEST 1.0.0",
                    "description": "Test version",
                    "download_url": "https://test.com/game.zip",
                    "installed": True
                }
            ]
        }

        with open(self.versions_file, 'w', encoding='utf-8') as f:
            json.dump(test_versions, f)

        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                app = launcher.TwixLauncher()
                app.version_selector = Mock()
                app.load_versions()

                self.assertEqual(len(app.versions_data['versions']), 1)
                self.assertEqual(app.versions_data['versions'][0]['name'], 'TEST 1.0.0')

    def test_version_change_handler(self):
        """Test version change handler updates config"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.status_label = Mock()
                    app.launch_button = Mock()

                    # Mock save_config
                    app.save_config = Mock()

                    app.on_version_change("ALPHA 1.16.4")

                    self.assertEqual(app.config['selected_version'], 'ALPHA 1.16.4')
                    app.save_config.assert_called_once()


class TestGameDirectoryManagement(unittest.TestCase):
    """Test suite for game directory management"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        launcher.GAME_PATH = self.test_dir

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_game_directory_initialization(self):
        """Test that game directory is created on initialization"""
        new_path = os.path.join(self.test_dir, "new_game_dir")
        launcher.GAME_PATH = new_path

        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.initialize_game_directory()

                    self.assertTrue(os.path.exists(new_path))

    def test_game_directory_already_exists(self):
        """Test initialization when directory already exists"""
        # Directory already exists from setUp
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    # Should not raise exception
                    app.initialize_game_directory()
                    self.assertTrue(os.path.exists(self.test_dir))


class TestRAMAllocation(unittest.TestCase):
    """Test suite for RAM allocation functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        launcher.GAME_PATH = self.test_dir
        launcher.CONFIG_FILE = os.path.join(self.test_dir, "config.json")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_ram_change_handler(self):
        """Test RAM slider change handler"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.ram_label = Mock()
                    app.save_config = Mock()

                    app.on_ram_change(4096.0)

                    self.assertEqual(app.config['ram_allocated'], 4096)
                    app.ram_label.configure.assert_called_with(text="Выделенная RAM: 4096 MB")
                    app.save_config.assert_called_once()

    def test_ram_value_bounds(self):
        """Test RAM allocation respects minimum and maximum values"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.ram_label = Mock()
                    app.save_config = Mock()

                    # Test minimum
                    app.on_ram_change(512.0)
                    self.assertEqual(app.config['ram_allocated'], 512)

                    # Test large value
                    app.on_ram_change(16384.0)
                    self.assertEqual(app.config['ram_allocated'], 16384)


class TestDownloadFunctionality(unittest.TestCase):
    """Test suite for game download functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        launcher.GAME_PATH = self.test_dir
        launcher.VERSIONS_FILE = os.path.join(self.test_dir, "versions.json")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('launcher.messagebox.showinfo')
    def test_download_with_no_url(self, mock_messagebox):
        """Test download behavior when no URL is configured"""
        versions_data = {
            "versions": [
                {
                    "name": "TEST 1.0.0",
                    "description": "Test",
                    "download_url": "",
                    "installed": False
                }
            ]
        }

        with open(launcher.VERSIONS_FILE, 'w') as f:
            json.dump(versions_data, f)

        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                app = launcher.TwixLauncher()
                app.version_selector = Mock()
                app.version_selector.get.return_value = "TEST 1.0.0"
                app.load_versions()

                app.download_game()

                # Should show info dialog
                mock_messagebox.assert_called_once()

    @patch('launcher.messagebox.showerror')
    def test_download_with_invalid_version(self, mock_messagebox):
        """Test download with non-existent version"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.version_selector = Mock()
                    app.version_selector.get.return_value = "NONEXISTENT"
                    app.versions_data = {"versions": []}

                    app.download_game()

                    mock_messagebox.assert_called_once()

    @patch('launcher.requests.get')
    @patch('launcher.threading.Thread')
    def test_download_initiates_thread(self, mock_thread, mock_requests):
        """Test that download starts a background thread"""
        versions_data = {
            "versions": [
                {
                    "name": "TEST 1.0.0",
                    "description": "Test",
                    "download_url": "https://test.com/game.zip",
                    "installed": False
                }
            ]
        }

        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.version_selector = Mock()
                    app.version_selector.get.return_value = "TEST 1.0.0"
                    app.versions_data = versions_data
                    app.launch_button = Mock()
                    app.download_button = Mock()
                    app.progress_bar = Mock()
                    app.status_label = Mock()

                    app.download_game()

                    # Verify thread was created
                    mock_thread.assert_called_once()


class TestGameLaunch(unittest.TestCase):
    """Test suite for game launch functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        launcher.GAME_PATH = self.test_dir
        launcher.CONFIG_FILE = os.path.join(self.test_dir, "config.json")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('launcher.messagebox.showwarning')
    def test_launch_game_not_found(self, mock_messagebox):
        """Test launch behavior when game executable is not found"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.version_selector = Mock()
                    app.version_selector.get.return_value = "TEST 1.0.0"
                    app.status_label = Mock()

                    app.launch_game()

                    # Should show warning
                    mock_messagebox.assert_called_once()

    @patch('launcher.subprocess.Popen')
    def test_launch_game_success(self, mock_popen):
        """Test successful game launch"""
        # Create fake game directory with executable
        version_path = os.path.join(self.test_dir, "TEST 1.0.0")
        os.makedirs(version_path)
        exe_file = os.path.join(version_path, "game.exe")

        # Create empty file
        with open(exe_file, 'w') as f:
            f.write("")

        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.version_selector = Mock()
                    app.version_selector.get.return_value = "TEST 1.0.0"
                    app.status_label = Mock()
                    app.save_config = Mock()

                    app.launch_game()

                    # Verify subprocess was called
                    mock_popen.assert_called_once_with([exe_file])

                    # Verify config was updated
                    self.assertEqual(app.config['last_played'], 'TEST 1.0.0')
                    app.save_config.assert_called_once()

    @patch('launcher.subprocess.Popen')
    @patch('launcher.messagebox.showerror')
    def test_launch_game_subprocess_error(self, mock_messagebox, mock_popen):
        """Test launch behavior when subprocess fails"""
        # Create fake game directory with executable
        version_path = os.path.join(self.test_dir, "TEST 1.0.0")
        os.makedirs(version_path)
        exe_file = os.path.join(version_path, "game.exe")

        with open(exe_file, 'w') as f:
            f.write("")

        # Make Popen raise an exception
        mock_popen.side_effect = Exception("Launch failed")

        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.version_selector = Mock()
                    app.version_selector.get.return_value = "TEST 1.0.0"
                    app.status_label = Mock()

                    app.launch_game()

                    # Should show error dialog
                    mock_messagebox.assert_called_once()
                    # Status should indicate error
                    app.status_label.configure.assert_called()


class TestUIComponents(unittest.TestCase):
    """Test suite for UI component behavior"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        launcher.GAME_PATH = self.test_dir

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_window_closing_saves_config(self):
        """Test that closing window saves configuration"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                with patch('launcher.TwixLauncher.load_versions'):
                    app = launcher.TwixLauncher()
                    app.save_config = Mock()
                    app.destroy = Mock()

                    app.on_closing()

                    app.save_config.assert_called_once()
                    app.destroy.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        launcher.GAME_PATH = self.test_dir
        launcher.CONFIG_FILE = os.path.join(self.test_dir, "config.json")
        launcher.VERSIONS_FILE = os.path.join(self.test_dir, "versions.json")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_full_configuration_workflow(self):
        """Test complete configuration workflow"""
        with patch('launcher.ctk.CTk.__init__', return_value=None):
            with patch('launcher.TwixLauncher.setup_ui'):
                app = launcher.TwixLauncher()
                app.version_selector = Mock()
                app.ram_label = Mock()
                app.status_label = Mock()
                app.launch_button = Mock()

                # Change RAM
                app.on_ram_change(4096.0)
                self.assertEqual(app.config['ram_allocated'], 4096)

                # Change version
                app.on_version_change("ALPHA 1.16.4")
                self.assertEqual(app.config['selected_version'], 'ALPHA 1.16.4')

                # Verify config file exists
                self.assertTrue(os.path.exists(launcher.CONFIG_FILE))

                # Create new instance and verify settings persist
                app2 = launcher.TwixLauncher()
                loaded_config = app2.load_config()
                self.assertEqual(loaded_config['ram_allocated'], 4096)
                self.assertEqual(loaded_config['selected_version'], 'ALPHA 1.16.4')


def run_tests():
    """Run all tests and generate report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLauncherConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestVersionManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestGameDirectoryManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestRAMAllocation))
    suite.addTests(loader.loadTestsFromTestCase(TestDownloadFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestGameLaunch))
    suite.addTests(loader.loadTestsFromTestCase(TestUIComponents))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)

    return result


if __name__ == '__main__':
    run_tests()
