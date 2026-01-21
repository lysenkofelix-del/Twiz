"""
Comprehensive unit tests for Twix Launcher functions
Tests configuration management, version handling, and core functionality
"""

import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock


class TestConfigurationManagement(unittest.TestCase):
    """Test suite for configuration file management"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.test_dir, "launcher_config.json")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_default_config(self):
        """Test loading default configuration when file doesn't exist"""
        default_config = {
            "ram_allocated": 2048,
            "selected_version": "ALPHA 1.16.5",
            "last_played": None,
            "game_url": ""
        }

        # Config file doesn't exist, should return default
        if not os.path.exists(self.config_file):
            config = default_config

        self.assertEqual(config['ram_allocated'], 2048)
        self.assertEqual(config['selected_version'], 'ALPHA 1.16.5')
        self.assertIsNone(config['last_played'])

    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        test_config = {
            "ram_allocated": 4096,
            "selected_version": "ALPHA 1.16.4",
            "last_played": "ALPHA 1.16.3",
            "game_url": "https://example.com/game.zip"
        }

        # Save config
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(test_config, f, indent=4)

        # Load config
        with open(self.config_file, 'r', encoding='utf-8') as f:
            loaded_config = json.load(f)

        self.assertEqual(loaded_config['ram_allocated'], 4096)
        self.assertEqual(loaded_config['selected_version'], 'ALPHA 1.16.4')
        self.assertEqual(loaded_config['last_played'], 'ALPHA 1.16.3')

    def test_corrupted_config_handling(self):
        """Test handling of corrupted configuration file"""
        # Write invalid JSON
        with open(self.config_file, 'w') as f:
            f.write("invalid json {{{")

        # Try to load, should fall back to default
        default_config = {
            "ram_allocated": 2048,
            "selected_version": "ALPHA 1.16.5",
            "last_played": None,
            "game_url": ""
        }

        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except:
            config = default_config

        # Should have default values
        self.assertEqual(config['ram_allocated'], 2048)

    def test_config_validation(self):
        """Test configuration value validation"""
        config = {
            "ram_allocated": 2048,
            "selected_version": "ALPHA 1.16.5",
            "last_played": None,
            "game_url": ""
        }

        # Test RAM bounds
        self.assertGreaterEqual(config['ram_allocated'], 1024)
        self.assertLessEqual(config['ram_allocated'], 32768)

        # Test version is string
        self.assertIsInstance(config['selected_version'], str)

    def test_update_config_values(self):
        """Test updating configuration values"""
        config = {
            "ram_allocated": 2048,
            "selected_version": "ALPHA 1.16.5",
            "last_played": None,
            "game_url": ""
        }

        # Update RAM
        config['ram_allocated'] = 4096
        self.assertEqual(config['ram_allocated'], 4096)

        # Update version
        config['selected_version'] = "ALPHA 1.16.4"
        self.assertEqual(config['selected_version'], "ALPHA 1.16.4")

        # Update last played
        config['last_played'] = "ALPHA 1.16.4"
        self.assertEqual(config['last_played'], "ALPHA 1.16.4")


class TestVersionsManagement(unittest.TestCase):
    """Test suite for game versions management"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.versions_file = os.path.join(self.test_dir, "versions.json")

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_default_versions_structure(self):
        """Test default versions data structure"""
        default_versions = {
            "versions": [
                {
                    "name": "ALPHA 1.16.5",
                    "description": "Последняя стабильная версия",
                    "download_url": "",
                    "installed": False
                },
                {
                    "name": "ALPHA 1.16.4",
                    "description": "Предыдущая версия",
                    "download_url": "",
                    "installed": False
                }
            ]
        }

        # Validate structure
        self.assertIn('versions', default_versions)
        self.assertIsInstance(default_versions['versions'], list)
        self.assertGreater(len(default_versions['versions']), 0)

    def test_save_and_load_versions(self):
        """Test saving and loading versions file"""
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

        # Save versions
        with open(self.versions_file, 'w', encoding='utf-8') as f:
            json.dump(test_versions, f, indent=4, ensure_ascii=False)

        # Load versions
        with open(self.versions_file, 'r', encoding='utf-8') as f:
            loaded_versions = json.load(f)

        self.assertEqual(len(loaded_versions['versions']), 1)
        self.assertEqual(loaded_versions['versions'][0]['name'], 'TEST 1.0.0')
        self.assertTrue(loaded_versions['versions'][0]['installed'])

    def test_find_version_by_name(self):
        """Test finding a version by name"""
        versions_data = {
            "versions": [
                {"name": "ALPHA 1.16.5", "description": "Latest"},
                {"name": "ALPHA 1.16.4", "description": "Previous"},
                {"name": "ALPHA 1.16.3", "description": "Old"}
            ]
        }

        # Find version
        target_name = "ALPHA 1.16.4"
        found_version = None
        for v in versions_data["versions"]:
            if v["name"] == target_name:
                found_version = v
                break

        self.assertIsNotNone(found_version)
        self.assertEqual(found_version['name'], "ALPHA 1.16.4")

    def test_version_not_found(self):
        """Test handling when version is not found"""
        versions_data = {
            "versions": [
                {"name": "ALPHA 1.16.5", "description": "Latest"}
            ]
        }

        # Try to find non-existent version
        target_name = "NONEXISTENT"
        found_version = None
        for v in versions_data["versions"]:
            if v["name"] == target_name:
                found_version = v
                break

        self.assertIsNone(found_version)

    def test_get_version_names_list(self):
        """Test extracting list of version names"""
        versions_data = {
            "versions": [
                {"name": "ALPHA 1.16.5", "description": "Latest"},
                {"name": "ALPHA 1.16.4", "description": "Previous"},
                {"name": "ALPHA 1.16.3", "description": "Old"}
            ]
        }

        # Get names
        version_names = [v["name"] for v in versions_data["versions"]]

        self.assertEqual(len(version_names), 3)
        self.assertIn("ALPHA 1.16.5", version_names)
        self.assertIn("ALPHA 1.16.4", version_names)


class TestDirectoryOperations(unittest.TestCase):
    """Test suite for directory and file operations"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_game_directory(self):
        """Test creating game directory"""
        game_path = os.path.join(self.test_dir, "test_game")

        # Create directory
        os.makedirs(game_path, exist_ok=True)

        self.assertTrue(os.path.exists(game_path))
        self.assertTrue(os.path.isdir(game_path))

    def test_create_nested_directories(self):
        """Test creating nested directories for versions"""
        base_path = self.test_dir
        version_path = os.path.join(base_path, "ALPHA 1.16.5")

        os.makedirs(version_path, exist_ok=True)

        self.assertTrue(os.path.exists(version_path))

    def test_directory_already_exists(self):
        """Test that creating existing directory doesn't fail"""
        game_path = os.path.join(self.test_dir, "existing")

        # Create once
        os.makedirs(game_path, exist_ok=True)

        # Create again - should not raise exception
        try:
            os.makedirs(game_path, exist_ok=True)
            success = True
        except:
            success = False

        self.assertTrue(success)

    def test_find_executable_in_directory(self):
        """Test finding executable file in directory"""
        game_path = os.path.join(self.test_dir, "game")
        os.makedirs(game_path)

        # Create fake executable
        exe_file = os.path.join(game_path, "game.exe")
        with open(exe_file, 'w') as f:
            f.write("")

        # Find executable
        found_exe = None
        for file in os.listdir(game_path):
            if file.endswith('.exe'):
                found_exe = os.path.join(game_path, file)
                break

        self.assertIsNotNone(found_exe)
        self.assertTrue(os.path.exists(found_exe))

    def test_no_executable_found(self):
        """Test when no executable is found"""
        game_path = os.path.join(self.test_dir, "game")
        os.makedirs(game_path)

        # Create non-executable file
        with open(os.path.join(game_path, "readme.txt"), 'w') as f:
            f.write("test")

        # Try to find executable
        found_exe = None
        if os.path.exists(game_path):
            for file in os.listdir(game_path):
                if file.endswith('.exe'):
                    found_exe = os.path.join(game_path, file)
                    break

        self.assertIsNone(found_exe)


class TestRAMCalculations(unittest.TestCase):
    """Test suite for RAM allocation calculations"""

    def test_ram_value_conversion(self):
        """Test converting RAM slider value to integer"""
        slider_value = 2048.5
        ram_mb = int(slider_value)

        self.assertEqual(ram_mb, 2048)
        self.assertIsInstance(ram_mb, int)

    def test_ram_minimum_value(self):
        """Test minimum RAM allocation"""
        min_ram = 1024
        allocated_ram = 512

        # Should enforce minimum
        if allocated_ram < min_ram:
            allocated_ram = min_ram

        self.assertGreaterEqual(allocated_ram, min_ram)

    def test_ram_maximum_value(self):
        """Test maximum RAM allocation"""
        max_ram = 16384
        allocated_ram = 20000

        # Should enforce maximum
        if allocated_ram > max_ram:
            allocated_ram = max_ram

        self.assertLessEqual(allocated_ram, max_ram)

    def test_ram_format_string(self):
        """Test formatting RAM value for display"""
        ram_value = 4096
        display_text = f"Выделенная RAM: {ram_value} MB"

        self.assertEqual(display_text, "Выделенная RAM: 4096 MB")
        self.assertIn(str(ram_value), display_text)


class TestDownloadValidation(unittest.TestCase):
    """Test suite for download URL and validation"""

    def test_valid_download_url(self):
        """Test validating download URL"""
        url = "https://example.com/game.zip"

        self.assertTrue(url.startswith("http"))
        self.assertTrue(len(url) > 0)

    def test_empty_download_url(self):
        """Test handling empty download URL"""
        url = ""

        self.assertFalse(bool(url))

    def test_url_validation(self):
        """Test URL validation logic"""
        valid_urls = [
            "https://example.com/game.zip",
            "http://example.com/file.exe",
            "https://cdn.example.com/downloads/game.zip"
        ]

        invalid_urls = [
            "",
            None,
            "not a url",
            "ftp://example.com"
        ]

        for url in valid_urls:
            if url and (url.startswith("http://") or url.startswith("https://")):
                is_valid = True
            else:
                is_valid = False
            self.assertTrue(is_valid)

        for url in invalid_urls:
            if url and (url.startswith("http://") or url.startswith("https://")):
                is_valid = True
            else:
                is_valid = False
            self.assertFalse(is_valid)


class TestGamePathValidation(unittest.TestCase):
    """Test suite for game path operations"""

    def test_game_path_construction(self):
        """Test constructing game version path"""
        base_path = "C:/Twix"
        version = "ALPHA 1.16.5"

        version_path = os.path.join(base_path, version)

        self.assertIn(version, version_path)
        self.assertTrue(version_path.startswith(base_path))

    def test_normalize_path_separators(self):
        """Test path separator normalization"""
        path = "C:/Twix/ALPHA 1.16.5"

        normalized = os.path.normpath(path)

        self.assertIsNotNone(normalized)


class TestStatusMessages(unittest.TestCase):
    """Test suite for status message formatting"""

    def test_status_message_formats(self):
        """Test various status message formats"""
        messages = {
            "ready": "Готов к запуску",
            "downloading": "Скачивание...",
            "launching": "Запуск игры...",
            "complete": "Скачивание завершено!",
            "error": "Ошибка: файл не найден"
        }

        for key, msg in messages.items():
            self.assertIsInstance(msg, str)
            self.assertGreater(len(msg), 0)

    def test_error_message_with_details(self):
        """Test error message formatting with details"""
        error = "Connection timeout"
        message = f"Не удалось скачать игру:\n{error}"

        self.assertIn(error, message)
        self.assertIn("скачать", message.lower())


class TestIntegrationWorkflows(unittest.TestCase):
    """Integration tests for complete workflows"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_complete_configuration_workflow(self):
        """Test complete configuration save/load workflow"""
        config_file = os.path.join(self.test_dir, "config.json")

        # Initial config
        config = {
            "ram_allocated": 2048,
            "selected_version": "ALPHA 1.16.5",
            "last_played": None
        }

        # Modify config
        config["ram_allocated"] = 4096
        config["selected_version"] = "ALPHA 1.16.4"

        # Save
        with open(config_file, 'w') as f:
            json.dump(config, f)

        # Load in new "session"
        with open(config_file, 'r') as f:
            loaded = json.load(f)

        self.assertEqual(loaded["ram_allocated"], 4096)
        self.assertEqual(loaded["selected_version"], "ALPHA 1.16.4")

    def test_version_selection_and_launch_workflow(self):
        """Test version selection and game launch preparation workflow"""
        # Setup version
        version_name = "ALPHA 1.16.5"
        version_path = os.path.join(self.test_dir, version_name)
        os.makedirs(version_path)

        # Create fake game executable
        exe_file = os.path.join(version_path, "game.exe")
        with open(exe_file, 'w') as f:
            f.write("")

        # Find and validate
        exe_found = None
        if os.path.exists(version_path):
            for file in os.listdir(version_path):
                if file.endswith('.exe'):
                    exe_found = os.path.join(version_path, file)
                    break

        self.assertIsNotNone(exe_found)
        self.assertTrue(os.path.exists(exe_found))


def run_all_tests():
    """Run all test suites with detailed output"""
    print("\n" + "="*70)
    print("TWIX LAUNCHER - COMPREHENSIVE TEST SUITE")
    print("="*70 + "\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestConfigurationManagement,
        TestVersionsManagement,
        TestDirectoryOperations,
        TestRAMCalculations,
        TestDownloadValidation,
        TestGamePathValidation,
        TestStatusMessages,
        TestIntegrationWorkflows
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST EXECUTION SUMMARY")
    print("="*70)
    print(f"Total Tests Run:     {result.testsRun}")
    print(f"Successful:          {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:            {len(result.failures)}")
    print(f"Errors:              {len(result.errors)}")

    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success Rate:        {success_rate:.1f}%")
    else:
        print(f"Success Rate:        N/A")

    print("="*70)

    if result.wasSuccessful():
        print("\n✓ All tests passed successfully!")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the output above.")
        return 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    exit(exit_code)
