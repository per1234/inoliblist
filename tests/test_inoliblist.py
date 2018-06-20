# must specify UTF-8 encoding due to the non-ASCII characters in the ArduinoJSON description
# encoding: utf-8
# for opening the output file
import os
# for making custom command line arguments work in conjunction with the unittest module
import sys
# for unit testing
import unittest

# add the parent folder to the module search path
sys.path.append('../')
from inoliblist import *  # nopep8

# parse command line arguments
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--ghtoken", dest="github_token", help="GitHub personal access token", metavar="TOKEN")
argument_parser.add_argument("--verbose", dest="enable_verbosity", help="Enable verbose output", action="store_true")

# this is needed to use command line arguments in conjunction with the unittest module
# (it uses its own command line arguments).
# https://stackoverflow.com/a/44255084/7059512
# alternative solution: https://stackoverflow.com/a/44248445/7059512
argument_parser.add_argument('unittest_args', nargs='*')
argument = argument_parser.parse_args()
sys.argv[1:] = argument.unittest_args


class TestInoLibraryList(unittest.TestCase):
    # NOTE: the tests are run in order sorted by method name, not in the order below

    # uncomment for debugging
    if argument.enable_verbosity:
        set_verbosity(enable_verbosity_input=True)

    # get repository objects to share between tests (to reduce # of API requests)

    set_github_token(github_token_input=argument.github_token)

    # https://github.com/FirstBuild/Relay
    # invalid JSON
    # folder count:3
    # archived:n
    # library.properties:/
    # library.json:/
    # header:src
    # sketch in root:n
    # examples folder in root:y
    # license:MIT
    # contributor count:2
    repository_object_firstbuild_relay = get_json_from_url(url="https://api.github.com/repos/FirstBuild/Relay")

    # https://github.com/triatebr/aprenda-arduino
    # spaces in path:y
    # non-ASCII characters in path:y
    # folder count:40
    # archived:n
    # library.properties:n
    # library.json:n
    # header:n
    # sketch in root:n
    # examples folder in root:n
    # license:n
    # contributor count:1
    repository_object_triatebr_aprenda_arduino = get_json_from_url(
        url="https://api.github.com/repos/triatebr/aprenda-arduino"
    )

    # https://github.com/Alexed98/first
    # empty repository
    repository_object_alexed98_first = get_json_from_url(url="https://api.github.com/repos/Alexed98/first")

    # https://github.com/arduino/forum-issues
    # folder count:0
    # archived:n
    # library.properties:n
    # library.json:n
    # header:n
    # sketch in root:n
    # examples folder in root:n
    # license:n
    # contributor count:3
    repository_object_arduino_forum_issues = get_json_from_url(url="https://api.github.com/repos/arduino/forum-issues")

    # https://github.com/sparkfun/phant-arduino
    # folder count:2
    # archived:y
    # library.properties:/
    # library.json:n
    # header:src
    # sketch in root:n
    # examples folder in root:y
    # license:unrecognized
    # contributor count:2
    # unset the token so it can be used in test_get_json_from_url_token_not_defined
    set_github_token(github_token_input=None)
    repository_object_sparkfun_phant_arduino = get_json_from_url(
        url="https://api.github.com/repos/sparkfun/phant-arduino"
    )
    # set the token again for the subsequent sharedobject creations
    set_github_token(github_token_input=argument.github_token)

    # https://github.com/VEBERArnaud/ShiftRegister__ArduinoLibrary
    # folder count:0
    # archived:y
    # library.properties:n
    # library.json:n
    # header:/
    # sketch in root:n
    # examples folder in root:n
    # license:n
    # contributor count:0
    # set send_token=False so it can be used in test_get_json_from_url_unauthenticated
    repository_object_veberarnaud_shiftregister__arduinolibrary = get_json_from_url(
        url="https://api.github.com/repos/VEBERArnaud/ShiftRegister__ArduinoLibrary"
    )

    # https://github.com/spaceshipyard/ArduinoJsonRpc
    # folder count:3
    # archived:y
    # library.properties:n
    # library.json:/
    # header:src
    # sketch in root:n
    # examples folder in root:y
    # license:MIT
    # contributor count:1
    repository_object_spaceshipyard_arduinojsonrpc = get_json_from_url(
        url="https://api.github.com/repos/spaceshipyard/ArduinoJsonRpc"
    )

    # https://github.com/MHeironimus/ArduinoJoystickLibrary
    # folder count:1
    # archived:n
    # library.properties:Joystick
    # library.json:n
    # header:Joystick/src
    # sketch in root:n
    # examples folder in root:n
    # only administrative files in root:n
    # license:LGPL-3.0
    # contributor count:2
    repository_object_mheironimus_arduinojoysticklibrary = get_json_from_url(
        url="https://api.github.com/repos/MHeironimus/ArduinoJoystickLibrary"
    )

    # https://github.com/menan/SparkJson
    # folder count:1
    # archived:n
    # library.properties:n
    # library.json:n
    # header:firmware
    # sketch in root:n
    # examples folder in root:n
    # only administrative files in root:n
    # license:MIT
    # contributor count:1
    repository_object_menan_sparkjson = get_json_from_url(url="https://api.github.com/repos/menan/SparkJson"
                                                          )

    # https://github.com/chen-yumin/skittle-color-sorter
    # folder count:2
    # archived:n
    # library.properties:n
    # library.json:n
    # header:/
    # sketch in root:y
    # examples folder in root:n
    # license:MIT
    # contributor count:1
    repository_object_chen_yumin_skittle_color_sorter = get_json_from_url(
        url="https://api.github.com/repos/chen-yumin/skittle-color-sorter"
    )

    # https://github.com/bblanchon/ArduinoJson
    # folder count:6
    # archived:n
    # library.properties:/
    # library.json:/
    # header:src
    # sketch in root:n
    # examples folder in root:y
    # license:MIT
    # contributor count:9
    repository_object_bblanchon_arduinojson = get_json_from_url(
        url="https://api.github.com/repos/bblanchon/ArduinoJson"
    )

    # https://github.com/going-digital/Talkie
    # folder count:1
    # archived:n
    # active:n
    # library.properties:n
    # library.json:m
    # header:Talkie
    # sketch in root:n
    # examples folder in root:n
    # only administrative files in root:y
    # license:n
    # contributor count:2
    repository_object_going_digital_talkie = get_json_from_url(
        url="https://api.github.com/repos/going-digital/Talkie"
    )

    def setUp(self):
        set_github_token(github_token_input=argument.github_token)
        initialize_table()

    def test_set_github_token(self):
        set_github_token(github_token_input=None)
        self.assertEqual(get_github_token(), None)
        set_github_token(github_token_input=argument.github_token)
        self.assertEqual(get_github_token(), argument.github_token)

    def test_initialize_table(self):
        # populate the table headings
        # this is called by setUp()
        # initialize_table()
        # now there should be one row
        self.assertEqual(len(get_table()), 1)
        # the row should have Column.count columns
        self.assertEqual(len(get_table()[0]), Column.count)
        # sanity check on the table heading text
        self.assertEqual(get_table()[0][Column.repository_url], "Repository URL \x1b \x1b")

    def test_process_library_manager_index(self):
        # open an abbreviated local copy of the Library Manager index
        with open('data/library_index.json', encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        process_library_manager_index(json_data=json_data)
        self.assertEqual(get_table()[1][Column.repository_name], "Esplora")
        # check that duplicate removal works (there are two Esplora items in the index file)
        self.assertEqual(get_table()[2][Column.repository_name], "Audio")

    def test_get_github_api_response(self):
        # requirements: none
        json_object = get_github_api_response(request="repos/arduino/Arduino")
        self.assertEqual(json_object["json_data"]["name"], "Arduino")
        self.assertFalse(json_object["additional_pages"])
        self.assertEqual(json_object["page_count"], 1)

    def test_check_rate_limiting(self):
        check_rate_limiting(api_type="search")
        check_rate_limiting(api_type="core")

    def test_get_json_from_url(self):
        # requirements: none
        self.assertEqual(TestInoLibraryList.repository_object_arduino_forum_issues["json_data"]["name"], "forum-issues")
        self.assertFalse(TestInoLibraryList.repository_object_arduino_forum_issues["additional_pages"])
        self.assertEqual(TestInoLibraryList.repository_object_arduino_forum_issues["page_count"], 1)

    def test_get_json_from_url_token_not_defined(self):
        # GitHub Personal Access Token will not be defined during CI of pull requests
        self.assertEqual(TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"]["name"],
                         "phant-arduino")
        self.assertFalse(TestInoLibraryList.repository_object_sparkfun_phant_arduino["additional_pages"])
        self.assertEqual(TestInoLibraryList.repository_object_sparkfun_phant_arduino["page_count"], 1)

    def test_get_json_from_url_unauthenticated(self):
        # requirements: none
        self.assertEqual(
            TestInoLibraryList.repository_object_veberarnaud_shiftregister__arduinolibrary["json_data"]["name"],
            "ShiftRegister__ArduinoLibrary")
        self.assertFalse(
            TestInoLibraryList.repository_object_veberarnaud_shiftregister__arduinolibrary["additional_pages"])
        self.assertEqual(TestInoLibraryList.repository_object_veberarnaud_shiftregister__arduinolibrary["page_count"],
                         1)

    # disabled because it causes a delay
    # def test_determine_urlopen_retry_true(self):
    #     self.assertTrue(determine_urlopen_retry(exception="HTTP Error 502: Bad Gateway"))

    def test_determine_urlopen_retry_false(self):
        self.assertFalse(determine_urlopen_retry(exception="HTTP Error 404: Not Found"))

    def test_normalize_url_space(self):
        url = "https://api.github.com/repos/triatebr/aprenda-arduino/contents/Arduino -CodeIOT 19-05-2015"
        url = normalize_url(url=url)
        # without normalization this will give a 400 error
        with urllib.request.urlopen(url):
            pass

    def test_normalize_url_non_ascii_character(self):
        # this URL contains a latin-1 encoding character 227 (small a tilde). I must use the escape code for it (\xe3)
        # to allow this file to still have UTF-8 encoding
        url = "https://api.github.com/repos/triatebr/aprenda-arduino/contents/controle-bot\xe3o-LED"
        url = normalize_url(url=url)
        # without normalization this will cause an exception:
        # UnicodeEncodeError: 'ascii' codec can't encode character '\xe3' in position 57: ordinal not in range(128)
        with urllib.request.urlopen(url):
            pass

    def test_normalize_url_redundant_slashes(self):
        # multiple slashes don't cause an error but it's distracting
        url = "http://example.org/has///redundant-slashes/"
        url = normalize_url(url=url)
        self.assertEqual(url, "http://example.org/has/redundant-slashes/")

    def test_search_repositories(self):
        search_repositories(search_query="ethernet+in:name+org:arduino-libraries",
                            created_argument_list=["<2013-01-01", ">=2013-01-01"],
                            fork_argument="false",
                            verify=False)
        self.assertEqual(get_table()[1][Column.repository_url], "https://github.com/arduino-libraries/Ethernet")

    def test_search_repositories_created_argument_list(self):
        search_repositories(search_query="ethernet+in:name+org:arduino-libraries",
                            created_argument_list=["<2012-01-01", "2013-01-01..2014-01-01"],
                            fork_argument="false",
                            verify=False)
        # created_at == 2015-03-27T09:54:12Z so this will return no results if the created_argument_list handling is
        # correct
        self.assertEqual(len(get_table()), 1)

    def test_search_repositories_fork_argument(self):
        search_repositories(search_query="watchdoglog+in:name+user:per1234",
                            created_argument_list=["<2013-01-01", "2013-01-01..2018-06-06"],
                            fork_argument="only",
                            verify=False)
        # search defaults to fork:false so if fork_argument handling is not working this search would give no results
        self.assertEqual(len(get_table()), 2)

    def test_search_repositories_verify(self):
        search_repositories(search_query="eepromutility+in:name+user:per1234",
                            created_argument_list=["<2013-01-01", "2013-01-01..2018-06-06"],
                            fork_argument="false",
                            verify=True)
        # repository does not meet the verification requirements so it should not be added to the table
        self.assertEqual(len(get_table()), 1)

    def test_populate_row(self):
        # requirements: library.properties, library.json, contributor count >0
        repository_object = TestInoLibraryList.repository_object_bblanchon_arduinojson["json_data"]
        populate_row(repository_object=repository_object, in_library_manager=True, verify=False)
        self.assertEqual(get_table()[1][Column.repository_url], "https://github.com/bblanchon/ArduinoJson")
        self.assertEqual(get_table()[1][Column.repository_owner], "bblanchon")
        self.assertEqual(get_table()[1][Column.repository_name], "ArduinoJson")
        self.assertEqual(get_table()[1][Column.repository_default_branch], "master")
        self.assertEqual(get_table()[1][Column.library_path], "/")
        self.assertEqual(get_table()[1][Column.archived], "False")
        self.assertEqual(get_table()[1][Column.is_fork], "False")
        # self.assertEqual(get_table()[1][Column.fork_of], "")
        self.assertNotEqual(get_table()[1][Column.last_push_date], "")
        self.assertNotEqual(get_table()[1][Column.fork_count], "")
        self.assertNotEqual(get_table()[1][Column.star_count], "")
        self.assertNotEqual(get_table()[1][Column.contributor_count], "")
        self.assertNotEqual(get_table()[1][Column.contributor_count], "0")
        self.assertNotEqual(get_table()[1][Column.contributor_count], "")
        self.assertEqual(get_table()[1][Column.repository_license], "MIT")
        self.assertEqual(get_table()[1][Column.repository_language], "C++")
        self.assertNotEqual(get_table()[1][Column.repository_description], "")
        self.assertNotEqual(get_table()[1][Column.github_topics], "")
        self.assertEqual(get_table()[1][Column.in_library_manager_index], "True")
        # self.assertEqual(get_table()[1][Column.in_platformio_library_registry], "True")
        self.assertEqual(get_table()[1][Column.library_manager_name], "ArduinoJson")
        self.assertNotEqual(get_table()[1][Column.library_manager_version], "")
        self.assertEqual(get_table()[1][Column.library_manager_author], "Benoit Blanchon <blog.benoitblanchon.fr>")
        self.assertEqual(get_table()[1][Column.library_manager_maintainer], "Benoit Blanchon <blog.benoitblanchon.fr>")
        self.assertEqual(get_table()[1][Column.library_manager_sentence],
                         "An efficient and elegant JSON library for Arduino.")
        self.assertEqual(get_table()[1][Column.library_manager_paragraph],
                         "ArduinoJson supports ✔ serialization, ✔ deserialization, ✔ fixed allocation, " +
                         "✔ zero-copy, ✔ streams, and more. It is the most popular Arduino library on GitHub " +
                         "❤❤❤❤❤. Check out arduinojson.org for a comprehensive documentation."
                         )
        self.assertEqual(get_table()[1][Column.library_manager_category], "Data Processing")
        self.assertEqual(get_table()[1][Column.library_manager_url],
                         "https://arduinojson.org/?utm_source=meta&utm_medium=library.properties")
        self.assertEqual(get_table()[1][Column.library_manager_architectures], "*")
        self.assertEqual(get_table()[1][Column.platformio_name], "ArduinoJson")
        self.assertEqual(get_table()[1][Column.platformio_description],
                         "An elegant and efficient JSON library for embedded systems")
        self.assertEqual(get_table()[1][Column.platformio_keywords], "json, rest, http, web")
        self.assertEqual(get_table()[1][Column.platformio_authors], "Benoit Blanchon")
        self.assertEqual(get_table()[1][Column.platformio_repository], "https://github.com/bblanchon/ArduinoJson.git")
        self.assertNotEqual(get_table()[1][Column.platformio_version], "")
        self.assertEqual(get_table()[1][Column.platformio_license], "")
        self.assertEqual(get_table()[1][Column.platformio_download_url], "")
        self.assertEqual(get_table()[1][Column.platformio_homepage],
                         "https://arduinojson.org/?utm_source=meta&utm_medium=library.json")
        self.assertEqual(get_table()[1][Column.platformio_frameworks], "arduino")
        self.assertEqual(get_table()[1][Column.platformio_platforms], "*")

    def test_populate_row_no_verify(self):
        # requirements: fail verification, no subfolders
        repository_object = TestInoLibraryList.repository_object_arduino_forum_issues["json_data"]
        populate_row(repository_object=repository_object, in_library_manager=True, verify=False)
        # check the last row of the table for the populated row
        self.assertEqual(len(get_table()), 2)

    def test_populate_row_verify_pass(self):
        # requirements: pass verification
        repository_object = TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"]
        populate_row(repository_object=repository_object, in_library_manager=True, verify=True)
        self.assertEqual(len(get_table()), 2)

    def test_populate_row_verify_fail(self):
        # requirements: fail verification
        repository_object = TestInoLibraryList.repository_object_arduino_forum_issues["json_data"]
        populate_row(repository_object=repository_object, in_library_manager=True, verify=True)
        self.assertEqual(len(get_table()), 1)

    def test_find_library_folder_library_dot_properties_in_root(self):
        # requirements: library.properties in the root, no library.json in the root, no header in root
        repository_object = TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"]
        row_list = [""] * Column.count
        self.assertEqual(find_library_folder(repository_object=repository_object, row_list=row_list, verify=False), '/')

    def test_find_library_folder_library_dot_json_in_root(self):
        # requirements: library.json in the root, no library.properties in the root, no header in root
        repository_object = TestInoLibraryList.repository_object_spaceshipyard_arduinojsonrpc["json_data"]
        row_list = [""] * Column.count
        self.assertEqual(find_library_folder(repository_object=repository_object, row_list=row_list, verify=False), '/')

    def test_find_library_folder_header_in_root(self):
        # requirements: no metadata and a header file in the root
        repository_object = TestInoLibraryList.repository_object_veberarnaud_shiftregister__arduinolibrary["json_data"]
        row_list = [""] * Column.count
        self.assertEqual(find_library_folder(repository_object=repository_object, row_list=row_list, verify=False), '/')

    def test_find_library_folder_metadata_in_subfolder(self):
        # requirements: metadata in subfolder, no header in root, few subfolders
        repository_object = TestInoLibraryList.repository_object_mheironimus_arduinojoysticklibrary["json_data"]
        row_list = [""] * Column.count
        self.assertEqual(find_library_folder(repository_object=repository_object, row_list=row_list, verify=False),
                         "Joystick")

    def test_find_library_folder_header_in_subfolder(self):
        # requirements: no metadata, header in subfolder, few subfolders
        repository_object = TestInoLibraryList.repository_object_menan_sparkjson["json_data"]
        row_list = [""] * Column.count
        self.assertEqual(find_library_folder(repository_object=repository_object, row_list=row_list, verify=False),
                         "firmware")

    def test_find_library_folder_no_library(self):
        # requirements: no library in root or subfolder, few subfolders
        repository_object = TestInoLibraryList.repository_object_arduino_forum_issues["json_data"]
        row_list = [""] * Column.count
        self.assertIsNone(find_library_folder(repository_object=repository_object, row_list=row_list, verify=False))

    # TODO: this repo has way too many subfolders!
    # TODO: find one repo with space and one repo with non-ASCII characters, both with library in subfolder
    def test_find_library_folder_problematic_path_names(self):
        # requirements: non-ASCII characters and spaces in folder and filenames and no library
        repository_object = TestInoLibraryList.repository_object_triatebr_aprenda_arduino["json_data"]
        row_list = [""] * Column.count
        self.assertIsNone(find_library_folder(repository_object=repository_object, row_list=row_list, verify=False))

    def test_find_library_folder_verify_metadata_in_root(self):
        # requirements metadata and no header file in root
        repository_object = TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"]
        row_list = [""] * Column.count
        self.assertEqual(find_library_folder(repository_object=repository_object, row_list=row_list, verify=True), '/')

    def test_find_library_folder_verify_empty_repository(self):
        # requirements: empty repository
        repository_object = TestInoLibraryList.repository_object_alexed98_first["json_data"]
        row_list = [""] * Column.count
        self.assertIsNone(find_library_folder(repository_object=repository_object, row_list=row_list, verify=True))

    def test_find_library_folder_verify_header_and_sketch_in_root(self):
        # requirements: header and sketch file in root, no metadata in root
        repository_object = TestInoLibraryList.repository_object_chen_yumin_skittle_color_sorter["json_data"]
        row_list = [""] * Column.count
        self.assertIsNone(find_library_folder(repository_object=repository_object, row_list=row_list, verify=True))

    # TODO: find suitable repo
    # def test_find_library_folder_verify_header_and_sketch_and_examples_in_root(self):
    #   # requirements: (header, sketch file, and examples folder in root, no metadata in root
    #   repository_object = ["json_data"]
    #   self.assertEqual(find_library_folder(repository_object=repository_object, row_list=row_list, verify=True),'/')

    def test_find_library_folder_verify_not_in_root(self):
        # requirements: library in subfolder
        repository_object = TestInoLibraryList.repository_object_mheironimus_arduinojoysticklibrary["json_data"]
        row_list = [""] * Column.count
        self.assertIsNone(find_library_folder(repository_object=repository_object, row_list=row_list, verify=True))

    def test_find_library_folder_verify_only_administrative_files_in_root(self):
        # requirements: only administrative files in root, library in subfolder
        repository_object = TestInoLibraryList.repository_object_going_digital_talkie["json_data"]
        row_list = [""] * Column.count
        self.assertEqual(
            find_library_folder(repository_object=repository_object, row_list=row_list, verify=True),
            "Talkie"
        )

    def test_parse_library_dot_properties_success(self):
        # requirements: library.properties
        repository_object = TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"]
        # initialize the row list
        row_list = [""] * Column.count
        self.assertTrue(parse_library_dot_properties(metadata_folder="/",
                                                     repository_object=repository_object,
                                                     row_list=row_list)
                        )
        self.assertEqual(row_list[Column.library_manager_name], "Phant")

    def test_parse_library_dot_properties_fail(self):
        # initialize the row list
        row_list = [""] * Column.count
        # requirements: any folder (including root) without library.properties
        repository_object = TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"]
        self.assertFalse(parse_library_dot_properties(metadata_folder="src",
                                                      repository_object=repository_object,
                                                      row_list=row_list)
                         )

    # TODO: find suitable repo
    # def test_parse_library_dot_properties_field_name_trailing_space(self):
    #     # initialize the row list
    #     row_list = [""] * Column.count
    #     # requirements: has library.properties w/ trailing space on field name
    #     repository_object = ["json_data"]
    #     self.assertTrue(
    #         parse_library_dot_properties(metadata_folder="/", repository_object=repository_object, row_list=row_list)
    #     )
    #     self.assertEqual(row_list[Column.library_manager_name], "Adafruit DHT Unified")

    def test_parse_library_dot_json_success(self):
        # initialize the row list
        row_list = [""] * Column.count
        # requirements: metadata_folder contains valid library.json
        repository_object = TestInoLibraryList.repository_object_spaceshipyard_arduinojsonrpc["json_data"]
        self.assertTrue(parse_library_dot_json(metadata_folder='/',
                                               repository_object=repository_object,
                                               row_list=row_list)
                        )
        self.assertEqual(row_list[Column.platformio_name], "ArduinoJsonRpc")

    def test_parse_library_dot_json_invalid_formatting(self):
        # initialize the row list
        row_list = [""] * Column.count
        # requirements: metadata_folder contains library.json with invalid JSON formatting
        # NOTE: I have an open PR to fix this: https://github.com/FirstBuild/Relay/pull/3
        repository_object = TestInoLibraryList.repository_object_firstbuild_relay["json_data"]
        self.assertTrue(
            parse_library_dot_json(metadata_folder="/", repository_object=repository_object, row_list=row_list)
        )
        # if this assertion fails it indicates the JSON formatting of library.json was fixed and I need to find a
        # different test case
        self.assertFalse(row_list[Column.platformio_name] == "FirstBuild - Relay")

    def test_parse_library_dot_json_fail(self):
        # initialize the row list
        row_list = [""] * Column.count
        # requirements: metadata_folder doesn't contain library.json
        repository_object = TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"]
        self.assertFalse(parse_library_dot_json(metadata_folder="src",
                                                repository_object=repository_object,
                                                row_list=row_list)
                         )

    def test_get_repository_license_none(self):
        # requirements: no license file
        repository_object = TestInoLibraryList.repository_object_arduino_forum_issues["json_data"]
        self.assertEqual(get_repository_license(repository_object=repository_object), "none")

    def test_get_repository_license_unrecognized(self):
        # requirements: license file but not recognized
        repository_object = TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"]
        self.assertEqual(get_repository_license(repository_object=repository_object), "unrecognized")

    def test_get_repository_license_recognized(self):
        # requirements: recognized license file
        repository_object = TestInoLibraryList.repository_object_spaceshipyard_arduinojsonrpc["json_data"]
        self.assertEqual(get_repository_license(repository_object=repository_object), "MIT")

    def test_get_contributor_count(self):
        # requirements: >1 contributor
        repository_object = TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"]
        self.assertEqual(get_contributor_count(repository_object=repository_object), '2')

    def test_get_contributor_count_none(self):
        # requirements: 0 contributors
        repository_object = TestInoLibraryList.repository_object_veberarnaud_shiftregister__arduinolibrary["json_data"]
        self.assertEqual(get_contributor_count(repository_object=repository_object), '0')

    def test_create_output_file(self):
        populate_row(repository_object=TestInoLibraryList.repository_object_sparkfun_phant_arduino["json_data"],
                     in_library_manager=True,
                     verify=False)
        create_output_file()
        with open(file=output_filename, mode='r', encoding="utf-8") as csv_file:
            csv_data = csv.reader(csv_file, delimiter=output_file_delimiter, quotechar=output_file_quotechar)
            # convert to list so specific rows can be accessed
            csv_data = list(csv_data)
        self.assertEqual(csv_data, get_table())

    def test_create_output_file_empty(self):
        # remove existing file
        try:
            os.remove(output_filename)
        except FileNotFoundError:
            pass

        create_output_file()

        # create_output_file() should not write an output file with an empty list
        with self.assertRaises(FileNotFoundError):
            with open(file=output_filename, mode='r', encoding="utf-8"):
                pass


if __name__ == '__main__':
    unittest.main()
